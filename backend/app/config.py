import os
from dotenv import load_dotenv

# ✅ Load .env file explicitly
load_dotenv()

# Base directory for the app
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # Points to 'backend' directory

class Config:
    # Flask Configurations
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key").strip()
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_secret_key_here").strip()

    # Database Configurations
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'app', 'flow_innovation.db')}"
    ).strip()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # API Configurations
    FACT_CHECK_API_KEY = os.getenv("FACT_CHECK_API_KEY", "").strip()
    NEWS_API_KEY = os.getenv("NEWS_API_KEY", "").strip()
    WOLFRAM_API_URL = os.getenv("WOLFRAM_API_URL", "").strip()
    WOLFRAM_APPID = os.getenv("WOLFRAM_APPID", "").strip()

    # Debugging: Print environment variables to confirm they are loaded
    print(f"🔍 WOLFRAM_API_URL: {WOLFRAM_API_URL}")
    print(f"🔍 WOLFRAM_APPID: {WOLFRAM_APPID}")

    # Ensure environment variables are properly loaded
    if not FACT_CHECK_API_KEY:
        raise RuntimeError("❌ FACT_CHECK_API_KEY is missing from the .env file")
    if not NEWS_API_KEY:
        raise RuntimeError("❌ NEWS_API_KEY is missing from the .env file")
    if not WOLFRAM_API_URL:
        raise RuntimeError("❌ WOLFRAM_API_URL is missing from the .env file")
    if not WOLFRAM_APPID:
        raise RuntimeError("❌ WOLFRAM_APPID is missing from the .env file")

