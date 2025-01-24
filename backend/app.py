import os
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from extensions import db 
# Import Blueprints
from routes import fact_checker
from models import initialize_database


# Initialize Flask app and database
app = Flask(__name__)
CORS(app)
app.config.from_object("config")

# Initialize extensions
db.init_app(app)  # Bind SQLAlchemy to the app
migrate = Migrate(app, db)  # Bind Flask-Migrate to the app and db

# Register Blueprints
app.register_blueprint(fact_checker)

if __name__ == "__main__":
    app.config['ENV'] = 'development'
    #app.run(debug=os.getenv("FLASK_DEBUG", False))  # Use environment variable for debug mode
