import os
import sys

# Add the parent directory to sys.path so we can import from apps.api
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from apps.api.agents.ingestion_agent import fetch_biometrics
from apps.api.agents.compliance_agent import check_compliance
from apps.api.agents.recommendation_agent import get_recommendation
from apps.api.utils.opik_tracker import configure_opik

def test_chain():
    print("Initializing Opik...")
    configure_opik()
    
    print("\n--- 1. Ingestion Agent ---")
    biometrics = fetch_biometrics(user_id="test_user")
    print(f"Biometrics: {biometrics}")
    
    print("\n--- 2. Compliance Agent ---")
    compliance = check_compliance(biometrics)
    print(f"Compliance: {compliance}")
    
    print("\n--- 3. Recommendation Agent ---")
    plan = "High Intensity Interval Training"
    print(f"User Plan: {plan}")
    recommendation = get_recommendation(compliance, plan)
    print(f"Recommendation: {recommendation}")
    
    print("\n--- Full Chain Verification Complete ---")

if __name__ == "__main__":
    test_chain()
