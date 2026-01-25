🏃‍♂️ Biometric Auditor Pro
A Multi-Agent AI system that analyzes athlete biometric data and provides personalized training recommendations using Google's Gemini 3 Flash Preview.

🎯 Overview
Biometric Auditor Pro uses a three-agent architecture to process biometric data, assess compliance with safe training thresholds, and generate intelligent coaching recommendations. The system integrates with Opik for comprehensive trace logging and monitoring.

🤖 Multi-Agent Architecture
1. Ingestion Agent (ingestion_agent.py)
Processes raw biometric data
Validates and structures input
Extracts key metrics: sleep hours, resting heart rate, recovery score
2. Compliance Agent (compliance_agent.py)
Evaluates biometric data against safe training thresholds
Determines athlete readiness status: Optimal, Warning, or Critical
Provides specific reasons for non-optimal conditions
3. Recommendation Agent (recommendation_agent.py)
Powered by Gemini 3 Flash Preview
Generates personalized training advice based on compliance status
Considers athlete's planned workout and current biometric state
Delivers detailed, actionable coaching guidance

🚀 Technologies Used
Google Gemini 3 Flash Preview – Advanced AI model for reasoning and recommendations
Opik – Trace logging, monitoring, and live evaluation rules
Google Antigravity – AI‑native environment for scaling, orchestration, and deployment
Python 3.11 – Core application language
FastAPI + OpenAPI – API framework with schema validation and documentation
python‑dotenv – Environment variable management

📊 How It Works
python
# 1. Ingest biometric data
biometrics = ingest_biometrics(user_id, sleep, hr, recovery)
# 2. Check compliance
compliance = check_compliance(biometrics)
# 3. Get AI-powered recommendation
recommendation = get_recommendation(compliance, user_plan)

🛠️ Installation & Setup
Prerequisites
Python 3.11+
Google Gemini API Key
Opik Account (optional, for trace logging)

Steps
Clone the repository
bash
git clone https://github.com/bhajan1406/biometric-auditor-pro.git
cd biometric-auditor-pro
Create virtual environment
bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux
Install dependencies
bash
pip install -r apps/api/requirements.txt
Set up environment variables
Create a .env file in the root directory:

env
GEMINI_API_KEY=your_gemini_api_key_here
Run the test chain
bash
cd apps/api
python test_chain.py

📝 Example Output
--- 1. Ingestion Agent ---
Biometrics: {'user_id': 'test_user', 'sleep_hours': 8.1, 'resting_hr': 55, 'recovery_score': 75}

--- 2. Compliance Agent ---
Compliance: {'status': 'Optimal', 'reasons': [], 'biometrics': {...}}

--- 3. Recommendation Agent ---
User Plan: High Intensity Interval Training
Recommendation: Alright, Athlete, this is your Biometric Auditor Coach.

Reviewing your current biometric data, the picture is exceptionally clear:
- Sleep Hours: 8.1 - Excellent. Optimal restorative sleep...
- Resting HR: 55 bpm - Outstanding cardiovascular fitness...
- Recovery Score: 75 - Very good systemic recovery...

Your status is unequivocally Optimal.

[Detailed personalized training guidance follows...]
🔍 Project Structure
biometric-auditor-pro/
├── apps/
│   ├── api/
│   │   ├── agents/
│   │   │   ├── ingestion_agent.py
│   │   │   ├── compliance_agent.py
│   │   │   └── recommendation_agent.py
│   │   ├── test_chain.py
│   │   ├── main.py
│   │   └── requirements.txt
│   └── web/
├── .env
├── .gitignore
└── README.md
🎓 Key Features
Real-time Biometric Analysis - Instant processing of athlete data
AI-Powered Coaching - Personalized recommendations using Gemini 2.5 Flash
Safety-First Approach - Compliance checks prevent overtraining
Trace Logging - Full observability with Opik integration
Scalable Architecture - Modular agent design for easy expansion
🔐 Safety Thresholds
The Compliance Agent uses the following thresholds:

Sleep: Minimum 7 hours (Warning), 5 hours (Critical)
Resting Heart Rate: Maximum 75 bpm (Warning), 85 bpm (Critical)
Recovery Score: Minimum 60 (Warning), 40 (Critical)
📈 Future Enhancements
 Web dashboard for visualization
 Historical data tracking
 Multi-user support
 Integration with wearable devices
 Advanced ML models for predictive insights

👨‍💻 Author
Saptarshi Dutta (@bhajan1406)

Created for the Mid-Hackathon Submission

Built with ❤️ using Google Gemini 3 Flash Preview

Why It Matters
Most people abandon fitness resolutions within weeks. Biometric Auditor Pro prevents that by adapting workouts to your real‑time condition, ensuring resolutions become sustainable habits. 
