import os
import opik
from opik import Opik
from dotenv import load_dotenv

load_dotenv()

def configure_opik():
    """Configure Opik tracking with API key from environment."""
    api_key = os.getenv("OPIK_API_KEY")
    if api_key:
        opik.configure(api_key=api_key, use_local=False, force=True)
    
    # Return a client instance for explicit usage if needed
    return Opik(api_key=api_key)

# Initialize configuration on import
if __name__ == "__main__":
    configure_opik()
