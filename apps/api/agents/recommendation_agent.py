import os
from dotenv import load_dotenv
from google import genai
from opik import track

load_dotenv()

# Initialize client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ADD THIS CODE HERE - to see available models
print("Available models:")
for model in client.models.list():
    print(f"Model: {model.name}")
print("\n")

@track
def get_recommendation(compliance_result: dict, user_plan: str) -> str:
    status = compliance_result["status"]
    reasons = compliance_result.get("reasons", [])
    biometrics = compliance_result.get("biometrics", {})
    
    system_instruction = (
        "You are an elite Biometric Auditor Coach. "
        "Advise the athlete based on their status."
    )
    
    input_text = f"Plan: {user_plan}, Status: {status}, Data: {biometrics}"
    
    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=f"{system_instruction}\n\n{input_text}"
    )
    
    return response.text
