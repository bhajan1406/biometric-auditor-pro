from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from agents.ingestion_agent import fetch_biometrics
from agents.compliance_agent import check_compliance
from agents.recommendation_agent import get_recommendation
from history_manager import get_history_manager
from utils.opik_tracker import configure_opik
from typing import Optional
import os

# Ensure Opik is configured globally
configure_opik()

# Initialize History Manager
history_manager = get_history_manager()
app = FastAPI(
    title="Biometric Auditor API V2",
    description="AI-powered biometric analysis with historical tracking",
    version="2.0.0"
)

# CORS configuration
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CoachRequest(BaseModel):
    """Request model for coaching recommendations."""
    sleep: Optional[float] = Field(None, ge=0, le=16, description="Sleep hours (0-16)")
    hr: Optional[int] = Field(None, ge=30, le=150, description="Resting heart rate (30-150 bpm)")
    plan: str = Field(..., min_length=5, max_length=500, description="Planned workout description")
    user_id: Optional[str] = Field("default", description="User identifier")
    save_history: Optional[bool] = Field(True, description="Save to history")

    @validator('plan')
    def validate_plan(cls, v):
        if not v or not v.strip():
            raise ValueError('Workout plan cannot be empty')
        return v.strip()

class CoachResponse(BaseModel):
    """Response model for coaching recommendations."""
    recommendation: str
    biometrics: dict
    compliance: dict
    status: str
    message: str = "Success"
    history_entry_id: Optional[int] = None

class WorkoutCompletionRequest(BaseModel):
    """Request to mark workout as completed."""
    user_id: str = Field(..., description="User identifier")
    entry_id: int = Field(..., description="History entry ID")
    completed: bool = Field(..., description="Whether workout was completed")
@app.post(
    "/coach",
    response_model=CoachResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Personalized Coaching Recommendation"
)
async def get_coach_recommendation(request: CoachRequest):
    """
    Main endpoint - three-agent pipeline + history tracking:
    1. Ingestion Agent - Processes biometric data
    2. Compliance Agent - Checks safety thresholds
    3. Recommendation Agent - Generates AI coaching advice
    4. History Manager - Saves entry to history
    """
    try:
        # 1. Ingestion Agent
        biometrics = fetch_biometrics(
            sleep_hours=request.sleep,
            resting_hr=request.hr,
            user_id=request.user_id
        )

        # 2. Compliance Agent
        compliance_result = check_compliance(biometrics)

        # 3. Recommendation Agent
        recommendation = get_recommendation(compliance_result, request.plan)

        # 4. History Manager - Save to history
        history_entry_id = None
        if request.save_history:
            entry = history_manager.add_entry(
                user_id=request.user_id,
                biometrics=biometrics,
                compliance=compliance_result,
                workout_plan=request.plan,
                recommendation=recommendation,
                completed=False
            )
            history_entry_id = entry["id"]

        return CoachResponse(
            recommendation=recommendation,
            biometrics=biometrics,
            compliance=compliance_result,
            status=compliance_result.get("status", "Unknown"),
            message="Recommendation generated successfully",
            history_entry_id=history_entry_id
        )

    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Validation error: {str(ve)}"
        )

    except Exception as e:
        print(f"❌ Error in /coach endpoint: {type(e).__name__} - {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your request."
        )
@app.get(
    "/history/{user_id}",
    summary="Get User History"
)
async def get_history(
    user_id: str,
    limit: Optional[int] = None,
    days: Optional[int] = None
):
    """Get user's biometric and workout history."""
    try:
        entries = history_manager.get_user_history(user_id, limit=limit, days=days)
        return {
            "user_id": user_id,
            "total_entries": len(entries),
            "entries": entries
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.get(
    "/trends/{user_id}",
    summary="Get Biometric Trends"
)
async def get_trends(user_id: str, days: int = 30):
    """Analyze biometric trends and get insights."""
    try:
        trends = history_manager.get_trends(user_id, days=days)
        return trends
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
@app.get(
    "/stats/{user_id}",
    summary="Get User Statistics"
)
async def get_stats(user_id: str):
    """Get user workout statistics and achievements."""
    try:
        stats = history_manager.get_stats(user_id)
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.post(
    "/workout/complete",
    summary="Mark Workout as Completed"
)
async def mark_workout_complete(request: WorkoutCompletionRequest):
    """Mark a workout as completed or not completed."""
    try:
        entry = history_manager.update_workout_completion(
            user_id=request.user_id,
            entry_id=request.entry_id,
            completed=request.completed
        )
        return {
            "message": "Workout status updated successfully",
            "entry": entry
        }
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
@app.get(
    "/health",
    summary="Health Check"
)
async def health_check():
    """API health check with system info."""
    return {
        "status": "healthy",
        "api_version": "2.0.0",
        "features": {
            "history_tracking": True,
            "trend_analysis": True,
            "workout_completion": True,
            "opik_monitoring": True
        },
        "history_manager": {
            "enabled": True,
            "data_file": str(history_manager.history_file)
        }
    }

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Biometric Auditor API V2!",
        "docs": "/docs",
        "health": "/health"
    }