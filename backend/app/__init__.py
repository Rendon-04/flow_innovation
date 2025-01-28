import os
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from extensions import db, jwt
from app.config import Config
from app.models import initialize_database
from app.routes import register_blueprints  # Import register_blueprints, which already includes progress_bp

def create_app():
    # Initialize Flask app
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    # Initialize database
    with app.app_context():
        initialize_database(app)

    # Register blueprints
    register_blueprints(app)  # This already registers the progress blueprint as well

    return app