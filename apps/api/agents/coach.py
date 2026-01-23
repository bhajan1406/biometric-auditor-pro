import os
from google import genai
from opik import track
from opik.integrations.genai import track_genai
from utils.opik_tracker import configure_opik

# Ensure Opik is configured
configure_opik()

# Initialize Gemini Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
gemini_client = track_genai(client)

@track
def resolution_coach_agent(sleep: float, hr: int, plan: str):
    """
    The 'Biometric Auditor' Coach Agent:
    Analyzes sleep and heart rate to provide workout recommendations.
    """
    system_instruction = (
        "You are a Biometric Auditor Coach. Analyze the user's sleep and HR. "
        "If sleep < 6h or HR > 75, pivot to recovery/low-impact. "
        "Explain the scientific reason why to reduce user guilt."
    )
    
    input_text = f"Sleep: {sleep}h, HR: {hr}. Plan: {plan}"
    
    response = gemini_client.models.generate_content(
        model="gemini-flash-latest",
        contents=f"{system_instruction}\n\nUser Data: {input_text}"
    )
    return response.text
