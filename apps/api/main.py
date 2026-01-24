from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agents.ingestion_agent import fetch_biometrics
from agents.compliance_agent import check_compliance
from agents.recommendation_agent import get_recommendation
from utils.opik_tracker import configure_opik
from typing import Optional

# Ensure Opik is configured globally
configure_opik()

app = FastAPI(title="Biometric Auditor API")

# Add CORS middleware to allow the frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CoachRequest(BaseModel):
    # Making these optional since we now fetch from ingestion agent
    sleep: Optional[float] = None
    hr: Optional[int] = None
    plan: str

@app.post("/coach")
async def get_coach_recommendation(request: CoachRequest):
    try:
        # 1. Ingestion Agent
        biometrics = fetch_biometrics()
        
        # 2. Compliance Agent
        compliance_result = check_compliance(biometrics)
        
        # 3. Recommendation Agent
        recommendation = get_recommendation(compliance_result, request.plan)
        
        return {
            "recommendation": recommendation,
            "biometrics": biometrics,
            "compliance": compliance_result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Biometric Auditor API is running (Refactored)"}
