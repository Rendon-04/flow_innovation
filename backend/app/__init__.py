import os
from dotenv import load_dotenv

# ✅ Load .env variables early
load_dotenv()

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from extensions import db, jwt
from app.config import Config
from app.models import initialize_database
from app.routes import register_blueprints  # This already includes progress_bp

def create_app():
    app = Flask(__name__)

    # ✅ Apply Global CORS (No need to do it per blueprint)
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

    # Load configurations
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # Initialize database
    with app.app_context():
        initialize_database(app)

    # ✅ Register blueprints (No need to register them again manually)
    register_blueprints(app)

    return app

# Create the WSGI application instance
app = create_app()
