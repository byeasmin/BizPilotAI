from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from idea_validator import IdeaValidator
import asyncio

app = FastAPI(title="BizPilotAI Backend", description="AI/ML powered business idea validation backend")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite dev server and potential production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI/ML validator
validator = IdeaValidator()

class IdeaRequest(BaseModel):
    idea: str
    category: str = ""
    target_audience: str = ""

class RoadmapResponse(BaseModel):
    roadmap: str
    feasibility_score: float

@app.post("/generate-roadmap", response_model=RoadmapResponse)
async def generate_roadmap(request: IdeaRequest):
    """
    Generate a business roadmap with AI/ML analysis.
    """
    try:
        # Generate roadmap using AI
        roadmap = validator.generate_roadmap(request.idea, request.category, request.target_audience)

        # Get feasibility score
        score = validator.score_feasibility(request.idea, request.category, request.target_audience)

        return RoadmapResponse(roadmap=roadmap, feasibility_score=score)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating roadmap: {str(e)}")

@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy", "service": "BizPilotAI Backend"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
