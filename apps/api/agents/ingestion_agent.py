from opik import track

@track
def fetch_biometrics(sleep_hours: float = None, resting_hr: int = None, user_id: str = "default") -> dict:
    """
    Processes biometric data from user input or simulates it for testing.
    """
    # Use provided values or generate mock data for testing
    biometric_data = {
        "user_id": user_id,
        "sleep_hours": sleep_hours if sleep_hours is not None else 7.0,
        "resting_hr": resting_hr if resting_hr is not None else 60,
        "recovery_score": calculate_recovery_score(sleep_hours, resting_hr)
    }
    return biometric_data

def calculate_recovery_score(sleep_hours: float = None, resting_hr: int = None) -> int:
    """
    Calculate a recovery score based on sleep and heart rate.
    Simple formula: Better sleep + lower HR = higher recovery
    """
    if sleep_hours is None or resting_hr is None:
        return 70  # Default score
    
    # Score calculation (0-100)
    # Sleep component (0-50): 7+ hours is optimal
    sleep_score = min(50, (sleep_hours / 8.0) * 50)
    
    # Heart rate component (0-50): Lower is better (50-70 optimal range)
    # Normalize: 50 bpm = 50 points, 70 bpm = 25 points, 90+ bpm = 0 points
    if resting_hr <= 50:
        hr_score = 50
    elif resting_hr <= 70:
        hr_score = 50 - ((resting_hr - 50) * 1.25)
    else:
        hr_score = max(0, 25 - ((resting_hr - 70) * 1.25))
    
    return round(sleep_score + hr_score)
