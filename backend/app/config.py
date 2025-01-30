import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Base directory for the app
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # Points to 'backend' directory


class Config:
    # Flask Configurations
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")  # Default to a fallback key
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_secret_key_here")  # Fallback for JWT

    # Database Configurations
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'app', 'flow_innovation.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # API Configurations
    FACT_CHECK_API_KEY = os.getenv("FACT_CHECK_API_KEY")
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")

    # Fail-Safes for Missing Environment Variables
    if not FACT_CHECK_API_KEY:
        raise RuntimeError("FACT_CHECK_API_KEY is not set in the environment variables")
    if not NEWS_API_KEY:
        raise RuntimeError("NEWS_API_KEY is not set in the environment variables")
