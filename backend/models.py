from extensions import db
from datetime import datetime
from flask import current_app

class Claim(db.Model):
    __tablename__ = 'claims'  # Explicitly name the table (optional but good practice)
    id = db.Column(db.Integer, primary_key=True)
    claim_text = db.Column(db.String(500), nullable=False)
    result = db.Column(db.Text, nullable=True)  # Use Text for potentially larger JSON responses
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Use datetime.utcnow instead of db.func.now()

    def __repr__(self):
        return f"<Claim(id={self.id}, claim_text='{self.claim_text}', timestamp={self.timestamp})>"

# Initialize the database schema
def initialize_database(app):
    with app.app_context():  # Ensure the app context is available
        db.create_all()  # This will create the tables if they do not exist