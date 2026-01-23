# Biometric Auditor v1 Stable Snapshot

This document provides a summary of the current working code for the **Biometric Auditor** project as of 2026-01-19.

## Overview
The Biometric Auditor is a full-stack AI application that analyzes user biometrics (sleep, heart rate) to provide personalized workout recommendations, pivoting to recovery if fatigue levels are high.

---

## 1. Backend (`apps/api`)

### `main.py`
The FastAPI entry point handling the API routing and CORS configuration.

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents.coach import resolution_coach_agent
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Biometric Auditor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CoachRequest(BaseModel):
    sleep: float
    hr: int
    plan: str

@app.post("/coach")
async def get_coach_recommendation(request: CoachRequest):
    try:
        recommendation = resolution_coach_agent(
            sleep=request.sleep, 
            hr=request.hr, 
            plan=request.plan
        )
        return {"recommendation": recommendation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Biometric Auditor API is running (Refactored)"}
```

### `agents/coach.py`
The core AI logic utilizing Google Gemini and Opik tracking.

```python
import os
from google import genai
from opik import track
from opik.integrations.genai import track_genai
from utils.opik_tracker import configure_opik

configure_opik()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
gemini_client = track_genai(client)

@track
def resolution_coach_agent(sleep: float, hr: int, plan: str):
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
```

### `utils/opik_tracker.py`
Configuration utility for Opik tracing.

```python
import os
import opik
from opik import Opik
from dotenv import load_dotenv

load_dotenv()

def configure_opik():
    api_key = os.getenv("OPIK_API_KEY")
    if api_key:
        opik.configure(api_key=api_key, use_local=False, force=True)
    return Opik(api_key=api_key)
```

---

## 2. Frontend (`apps/web`)

### `app/page.tsx`
A modern Next.js dashboard with glassmorphism and framer-motion animations.

```typescript
"use client";
import { useState } from "react";
import { Activity, Moon, Dumbbell, Brain, Send, Loader2 } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

export default function Dashboard() {
    const [sleep, setSleep] = useState<number>(7);
    const [hr, setHr] = useState<number>(60);
    const [plan, setPlan] = useState<string>("Heavy Leg Day");
    const [recommendation, setRecommendation] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    const getRecommendation = async () => {
        setLoading(true);
        setRecommendation(null);
        try {
            const response = await fetch("http://127.0.0.1:8000/coach", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    sleep: Number(sleep),
                    hr: Number(hr),
                    plan
                }),
            });
            const data = await response.json();
            setRecommendation(data.recommendation);
        } catch (error) {
            setRecommendation("Failed to connect to the Biometric Auditor API.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <main className="min-h-screen p-8 flex flex-col items-center justify-center bg-[#050510]">
             {/* ... UI Implementation ... */}
        </main>
    );
}
```

---

## 3. Configuration

### `apps/api/requirements.txt`
```text
fastapi
uvicorn
pydantic
google-genai
opik
python-dotenv
```

### `apps/web/package.json`
```json
{
    "dependencies": {
        "react": "^18",
        "react-dom": "^18",
        "next": "14.2.3",
        "lucide-react": "^0.378.0",
        "framer-motion": "^11.1.7",
        "clsx": "^2.1.1",
        "tailwind-merge": "^2.3.0"
    }
}
```
