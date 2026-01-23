from opik import track

@track
def check_compliance(biometrics: dict) -> dict:
    """
    Analyzes biometric data against physiological thresholds for heavy training.
    """
    sleep = biometrics.get("sleep_hours", 0)
    recovery = biometrics.get("recovery_score", 0)
    
    status = "Optimal"
    reasons = []

    if sleep < 7.0:
        status = "Warning"
        reasons.append(f"Sleep ({sleep}h) is below 7h threshold.")
    
    if recovery < 40:
        status = "Warning"
        reasons.append(f"Recovery score ({recovery}) is low.")

    return {
        "status": status,
        "reasons": reasons,
        "biometrics": biometrics
    }
