import os
from dotenv import load_dotenv
load_dotenv()

# Flask Configuration
SECRET_KEY = os.environ.get("SECRET_KEY", "your_secret_key")  # Default to a fallback key
#TODO check to set DATABASE_URL environment variable in .env
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///fact_checker.db")  # Use env variable or fallback to SQLite
SQLALCHEMY_TRACK_MODIFICATIONS = False

# API Configurations
FACT_CHECK_API_KEY = os.getenv("FACT_CHECK_API_KEY")  # Load API key from environment variable
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# API Validation fail-safes
if not FACT_CHECK_API_KEY:
    raise RuntimeError("FACT_CHECK_API_KEY is not set in the environment variables")

if not NEWS_API_KEY:
    raise RuntimeError("NEWS_API_KEY is not set in the environment variables")

