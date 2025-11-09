from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Optional: OpenAI API key
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()
templates = Jinja2Templates(directory=".")

# Placeholder financial & AI data
FINANCE_SUMMARY = {
    "income": 5000,
    "expense": 2000,
    "profit": 3000,
    "ai_score": 85
}

TRANSACTIONS = [
    {"desc": "Salary", "amount": 3000},
    {"desc": "Office Rent", "amount": -1000},
    {"desc": "Marketing", "amount": -500},
    {"desc": "Freelance", "amount": 2000},
]

AI_SCORE_HISTORY = [
    {"date": "2025-11-01", "score": 80},
    {"date": "2025-11-02", "score": 82},
    {"date": "2025-11-03", "score": 85},
]

@app.get("/", response_class=HTMLResponse)
def get_dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "finance": FINANCE_SUMMARY,
            "transactions": TRANSACTIONS,
            "history": AI_SCORE_HISTORY
        }
    )

@app.post("/chat", response_class=HTMLResponse)
def chat_dashboard(request: Request, message: str = Form(...)):
    # Placeholder AI response
    reply = f"You asked: {message} | BizBot says: Hello! This is a demo reply."
    
    # Uncomment below for real OpenAI response
    # response = openai.Completion.create(
    #     model="text-davinci-003",
    #     prompt=message,
    #     max_tokens=50
    # )
    # reply = response.choices[0].text.strip()
    
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "reply": reply,
            "finance": FINANCE_SUMMARY,
            "transactions": TRANSACTIONS,
            "history": AI_SCORE_HISTORY
        }
    )
