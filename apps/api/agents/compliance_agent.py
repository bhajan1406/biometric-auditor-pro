from opik import track

@track
def check_compliance(biometrics: dict) -> dict:
    """
    Analyzes biometric data against physiological thresholds.
    
    Thresholds (Medical Convention):
        Sleep: <6h = Warning, <5h = Critical
        Resting HR: >80 = Warning, >95 = Critical
        Recovery: <60 = Warning, <40 = Critical
    """
    sleep = biometrics.get("sleep_hours", 0)
    hr = biometrics.get("resting_hr", 0)
    recovery = biometrics.get("recovery_score", 0)

    status = "Optimal"
    severity_score = 0
    reasons = []
    priority_message = "All biometric indicators are within optimal range."

    # --- SLEEP CHECKS ---
    if sleep < 5.0:
        status = "Critical"
        severity_score += 3
        reasons.append(f"CRITICAL: Sleep ({sleep}h) is dangerously low. Minimum 5h required.")
    elif sleep < 6.0:
        if status != "Critical":
            status = "Warning"
        severity_score += 1
        reasons.append(f"Warning: Sleep ({sleep}h) is below the optimal 6h threshold.")

    # --- RESTING HEART RATE CHECKS ---
    if hr > 95:
        status = "Critical"
        severity_score += 3
        reasons.append(f"CRITICAL: Resting HR ({hr} bpm) is dangerously elevated. Rest immediately.")
    elif hr > 80:
        if status != "Critical":
            status = "Warning"
        severity_score += 1
        reasons.append(f"Warning: Resting HR ({hr} bpm) is above the 80 bpm threshold.")

    # --- RECOVERY SCORE CHECKS ---
    if recovery < 40:
        status = "Critical"
        severity_score += 3
        reasons.append(f"CRITICAL: Recovery score ({recovery}/100) is critically low.")
    elif recovery < 60:
        if status != "Critical":
            status = "Warning"
        severity_score += 1
        reasons.append(f"Warning: Recovery score ({recovery}/100) is below optimal 60 threshold.")

    # --- SET PRIORITY MESSAGE ---
    if status == "Critical":
        priority_message = "⚠️ CRITICAL: Immediate rest is recommended. Do not train today."
    elif status == "Warning":
        priority_message = "⚡ WARNING: Proceed with caution. Consider a lighter workout."
    else:
        priority_message = "✅ OPTIMAL: All systems green. You're cleared for training!"

    return {
        "status": status,
        "severity_score": severity_score,
        "reasons": reasons,
        "priority_message": priority_message,
        "biometrics": biometrics
    }