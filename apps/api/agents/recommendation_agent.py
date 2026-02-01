import os
from dotenv import load_dotenv
from google import genai
from opik import track
from history_manager import get_history_manager

load_dotenv()

# Initialize client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Fallback recommendations when AI is unavailable
FALLBACK_RECOMMENDATIONS = {
    "Critical": (
        "⚠️ CRITICAL STATUS DETECTED.\n\n"
        "Your biometrics indicate you need immediate rest.\n"
        "• Do NOT train today.\n"
        "• Focus on sleep (aim for 8+ hours).\n"
        "• Stay hydrated and eat nutrient-dense foods.\n"
        "• Re-check your biometrics tomorrow before training."
    ),
    "Warning": (
        "⚡ WARNING STATUS DETECTED.\n\n"
        "Your biometrics suggest caution today.\n"
        "• Consider a lighter workout than planned.\n"
        "• Focus on mobility, stretching, or yoga.\n"
        "• Prioritize recovery - sleep early tonight.\n"
        "• Monitor how you feel during exercise."
    ),
    "Optimal": (
        "✅ OPTIMAL STATUS - You're cleared for training!\n\n"
        "Your biometrics look great today.\n"
        "• Proceed with your planned workout.\n"
        "• Push yourself, but listen to your body.\n"
        "• Stay hydrated throughout your session.\n"
        "• Log your workout completion afterward."
    )
}

@track
def get_recommendation(compliance_result: dict, user_plan: str) -> str:
    """
    Generates AI coaching recommendation using Gemini.
    Includes historical trend analysis in the prompt.
    """
    status = compliance_result["status"]
    reasons = compliance_result.get("reasons", [])
    biometrics = compliance_result.get("biometrics", {})
    priority_message = compliance_result.get("priority_message", "")
    user_id = biometrics.get("user_id", "default")

    # --- FETCH HISTORY FOR TREND CONTEXT ---
    history_context = "No previous history available (first session)."
    try:
        hm = get_history_manager()
        past_audits = hm.get_user_history(user_id, limit=5)
        if past_audits:
            history_context = "\n".join([
                f"- {h['timestamp'][:10]}: "
                f"Status: {h['compliance']['status']}, "
                f"Sleep: {h['biometrics']['sleep_hours']}h, "
                f"HR: {h['biometrics']['resting_hr']} bpm, "
                f"Recovery: {h['biometrics']['recovery_score']}/100"
                for h in past_audits
            ])
    except Exception as e:
        print(f"⚠️ Could not fetch history: {e}")

    # --- BUILD ENHANCED PROMPT ---
    system_instruction = (
        "You are an elite Biometric Auditor Coach. "
        "Your job is to analyze an athlete's current biometrics AND historical trends "
        "to provide personalized, science-based coaching advice. "
        "Be encouraging but prioritize health and safety above all else. "
        "Keep your response under 200 words."
    )

    input_text = f"""
CURRENT STATUS: {status}
PRIORITY: {priority_message}

CURRENT BIOMETRICS:
- Sleep: {biometrics.get('sleep_hours', 'N/A')}h
- Resting HR: {biometrics.get('resting_hr', 'N/A')} bpm
- Recovery Score: {biometrics.get('recovery_score', 'N/A')}/100

COMPLIANCE REASONS:
{chr(10).join(reasons) if reasons else "All checks passed."}

HISTORICAL TRENDS (Last 5 Sessions):
{history_context}

PLANNED WORKOUT:
{user_plan}

TASK:
1. Analyze today's biometrics against the status.
2. Compare today's data to the HISTORICAL TRENDS.
3. If recovery scores are declining over recent sessions, advise caution even if today is Optimal.
4. Provide actionable, personalized coaching for today.
"""

    # --- CALL GEMINI ---
    try:
        response = client.models.generate_content(
            model="models/gemini-3-flash-preview",
            contents=f"{system_instruction}\n\n{input_text}"
        )
        return response.text

    except Exception as e:
        print(f"❌ Gemini API error: {type(e).__name__} - {e}")
        # Return fallback recommendation based on status
        return FALLBACK_RECOMMENDATIONS.get(status, FALLBACK_RECOMMENDATIONS["Optimal"])