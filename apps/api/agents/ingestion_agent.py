import random
from opik import track

@track
def fetch_biometrics(user_id: str = "default") -> dict:
    """
    Simulates fetching data from a wearable API (e.g., Fitbit).
    """
    # Mock data with some randomization for variety
    mock_data = {
        "user_id": user_id,
        "sleep_hours": round(random.uniform(5.0, 9.0), 1),
        "resting_hr": random.randint(45, 75),
        "recovery_score": random.randint(20, 100)
    }
    return mock_data
