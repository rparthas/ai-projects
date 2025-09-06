import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class Settings:
    """
    Application settings are loaded from environment variables.
    Create a .env file in the root directory to set these values for local development.
    """
    # Example:
    # OPEN_METEO_API_URL = os.getenv("OPEN_METEO_API_URL", "https://api.open-meteo.com/v1/forecast")
    pass

settings = Settings()
