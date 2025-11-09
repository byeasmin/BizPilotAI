# main.py
import os
import json
from typing import List
from fastapi import FastAPI, HTTPException, Form, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from dotenv import load_dotenv
import httpx
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set in environment")


app = FastAPI(title="BizPilot AI - Business Co-Pilot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class IdeaValidationResponse(BaseModel):
    business_type: str
    location: str
    ai_score: int
    market_trend: str
    main_competitors: List[str]
    business_opportunities: str
    monthly_estimates: dict


async def call_gemini_raw(prompt: str, model: str = "gemini-2.0-flash", timeout: float = 30.0) -> str:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    async with httpx.AsyncClient(timeout=timeout) as client:
        r = await client.post(f"{url}?key={GEMINI_API_KEY}", headers=headers, json=payload)
        r.raise_for_status()
        data = r.json()
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        return json.dumps({"error": "unexpected gemini response", "raw": data})

def try_parse_json_like(text: str):
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
    first = cleaned.find("{")
    last = cleaned.rfind("}")
    if first != -1 and last != -1 and last > first:
        candidate = cleaned[first:last+1]
        try:
            return json.loads(candidate)
        except:
            pass
    try:
        return json.loads(cleaned)
    except:
        return None


async def fetch_competitors_google_places(business_type: str, location: str, limit: int = 3) -> List[str]:
    if not GOOGLE_PLACES_API_KEY:
        return []
    query = f"{business_type} near {location}"
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {"query": query, "key": GOOGLE_PLACES_API_KEY}
    async with httpx.AsyncClient() as client:
        r = await client.get(url, params=params, timeout=10.0)
        r.raise_for_status()
        data = r.json()
    results = data.get("results", [])[:limit]
    return [res.get("name") for res in results if res.get("name")]

def build_idea_prompt(business_type: str, location: str, competitors: List[str]) -> str:
    competitors_text = ", ".join(competitors) if competitors else "No reliable competitor data available"
    prompt = f"""
You are a helpful business analyst specialized in Bangladesh startups.

Given:
- Business type: {business_type}
- Target location: {location}
- Known competitors: {competitors_text}

Analyze the business idea and return ONLY valid JSON:

{{
  "ai_score": <integer 0-100>,
  "market_trend": "<short text summarizing demand and trend>",
  "main_competitors": ["...","..."],
  "business_opportunities": "<short text describing where to stand out>",
  "monthly_estimates": {{"income": <number>, "expense": <number>, "currency": "BDT"}}
}}
"""
    return prompt

@app.post("/idea_validation", response_model=IdeaValidationResponse)
async def idea_validation(
    business_type: str = Form(...),
    location: str = Form(...),
):
    try:
        competitors = await fetch_competitors_google_places(business_type, location, limit=5)
    except Exception:
        competitors = []

    prompt = build_idea_prompt(business_type, location, competitors)
    raw = await call_gemini_raw(prompt)
    parsed = try_parse_json_like(raw)

    if parsed is None:
        # fallback
        parsed = {
            "ai_score": 0,
            "market_trend": "unknown",
            "main_competitors": competitors if competitors else [],
            "business_opportunities": "unknown",
            "monthly_estimates": {"income":0,"expense":0,"currency":"BDT"}
        }

    return {
        "business_type": business_type,
        "location": location,
        "ai_score": int(parsed.get("ai_score", 0)),
        "market_trend": parsed.get("market_trend", ""),
        "main_competitors": parsed.get("main_competitors", competitors if competitors else []),
        "business_opportunities": parsed.get("business_opportunities", ""),
        "monthly_estimates": parsed.get("monthly_estimates", {"income":0,"expense":0,"currency":"BDT"}),
    }

# websocket...
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/bizbot")
async def websocket_bizbot(websocket: WebSocket):
    await manager.connect(websocket)
    context = []
    try:
        while True:
            user_text = await websocket.receive_text()
            context.append({"role": "user", "text": user_text})

            # Build prompt for AI
            messages_text = "You are BizBot, an expert business assistant for Bangladesh startups.\n"
            for m in context[-6:]:
                messages_text += f"{m['role'].upper()}: {m['text']}\n"
            messages_text += """
User wants a complete roadmap for their business. Respond ONLY in valid JSON:

{
  "registration_steps": ["..."],
  "tax_steps": ["..."],
  "market_segments": ["..."],
  "potential_investors": ["..."],
  "estimated_startup_costs": {"minimum": <number>, "maximum": <number>, "currency": "BDT"}
}
Be practical and concise for Bangladesh startups.
"""

            raw_reply = await call_gemini_raw(messages_text)
            parsed_reply = try_parse_json_like(raw_reply)

            if parsed_reply is None:
                parsed_reply = {
                    "registration_steps": [],
                    "tax_steps": [],
                    "market_segments": [],
                    "potential_investors": [],
                    "estimated_startup_costs": {"minimum":0,"maximum":0,"currency":"BDT"}
                }

            await manager.send_personal_message(json.dumps(parsed_reply, ensure_ascii=False, indent=2), websocket)
            context.append({"role":"assistant","text":raw_reply})

            if len(context) > 20:
                context = context[-20:]

    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        try:
            await manager.send_personal_message(f"Error: {str(e)}", websocket)
        except:
            pass
        manager.disconnect(websocket)

@app.get("/")
async def root():
    return {"message": "BizPilot AI Co-Pilot Backend is running"}

