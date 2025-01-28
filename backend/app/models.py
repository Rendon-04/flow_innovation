from extensions import db
from datetime import datetime
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash

class Claim(db.Model):
    __tablename__ = 'claims'  # Explicitly name the table (optional but good practice)
    id = db.Column(db.Integer, primary_key=True)
    claim_text = db.Column(db.String(500), nullable=False)
    result = db.Column(db.Text, nullable=True)  # Use Text for potentially larger JSON responses
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Use datetime.utcnow instead of db.func.now()

    def __repr__(self):
        return f"<Claim(id={self.id}, claim_text='{self.claim_text}', timestamp={self.timestamp})>"

# Enter models for "Progress"
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    progress = db.relationship('Progress', back_populates='user', cascade="all, delete-orphan")
    goals = db.relationship('Goal', back_populates='user', cascade="all, delete-orphan")
    community_progress = db.relationship('CommunityProgress', back_populates='user', cascade="all, delete-orphan")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    achievement = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', back_populates="progress")


class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String(500), nullable=False)
    target_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', back_populates="goals")


class CommunityProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    progress_story = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', back_populates="community_progress")


# Initialize the database schema
def initialize_database(app):
    with app.app_context():  # Ensure the app context is available
        db.create_all()  # This will create the tables if they do not exist