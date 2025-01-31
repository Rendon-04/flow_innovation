import json
import logging
import numpy as np
import pandas as pd
import spacy
import requests
from app.models import Claim, Goal, Progress, User
from app.services.news_service import NewsService
from extensions import db
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans


# Blueprint for fact-checking, progress, wolfram
fact_checker = Blueprint("fact_checker", __name__)
progress_bp = Blueprint('progress', __name__)
wolfram_bp = Blueprint('wolfram', __name__)

@wolfram_bp.route("/wolfram/progress_insights", methods=["POST"])
def wolfram_progress_insights():
    """ Sends user progress data to Wolfram for analysis. """
    data = request.get_json()

    if not data.get("user_id"):
        return jsonify({"error": "User ID is required"}), 400
    
    user_id = data["user_id"]
    
    # Retrieve user progress and goals from the database
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Collect progress timestamps and achievements
    progress = Progress.query.filter_by(user_id=user_id).all()
    timestamps = [p.created_at.isoformat() for p in progress]  # Ensure timestamps are formatted
    achievements = [p.achievement for p in progress]

    # Collect user goals
    goals = Goal.query.filter_by(user_id=user_id).all()
    goal_texts = [g.goal for g in goals]
    
    # Send relevant data to Wolfram API
    WOLFRAM_API_URL = current_app.config.get("WOLFRAM_API_URL")
    
    try:
        response = requests.post(WOLFRAM_API_URL, json={
            "timestamps": timestamps,
            "achievements": achievements,
            "goals": goal_texts
        })

        wolfram_result = response.json()

        # Return the results to the client
        return jsonify({
            "message": "Wolfram Analysis Complete",
            "next_milestone": wolfram_result.get("NextMilestoneDate"),
            "innovation_score": wolfram_result.get("InnovationScore"),
            "recommended_goals": wolfram_result.get("RecommendedGoals"),
            "progress_graph": wolfram_result.get("ProgressGraph"),
            "future_insights": wolfram_result.get("FutureInsights"),
            "suggestions": wolfram_result.get("Suggestions")
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Set up logging to capture API issues more effectively
logging.basicConfig(level=logging.DEBUG)

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Helper function to clean and preprocess text
def preprocess_text(text):
    doc = nlp(text.lower())  # Convert to lowercase and tokenize
    return " ".join([token.lemma_ for token in doc if not token.is_stop])  # Lemmatization & remove stopwords

# Route for home page
@fact_checker.route("/")
def home():
    return jsonify({"message": "Welcome to the Fact-Checking API!"}), 200


# Route for checking claims (GET and POST)
@fact_checker.route("/check_claim", methods=["GET", "POST"])
def check_claim():
    FACT_CHECK_API_KEY = current_app.config["FACT_CHECK_API_KEY"]
    logging.debug(f"API Key used: {FACT_CHECK_API_KEY}")

    # Extract query based on request method
    if request.method == "GET":
        query = request.args.get("query", "").strip()
        if not query:
            return jsonify({"error": "No query provided. Use ?query=<your_query>"}), 400
    elif request.method == "POST":
        data = request.json
        if not data or not data.get("claim"):
            return jsonify({"error": "Invalid or missing JSON payload. Provide a 'claim' field."}), 400
        query = data["claim"].strip()

    query_cleaned = preprocess_text(query)

    # Retrieve past claims
    past_claims = Claim.query.all()
    past_texts = [preprocess_text(c.claim_text) for c in past_claims]

    if past_texts:
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(past_texts + [query_cleaned])
        
        similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
        max_similarity = max(similarities[0]) if similarities[0].size > 0 else 0

        if max_similarity > 0.7:  # High similarity threshold
            similar_claim = past_claims[similarities[0].argmax()]
            return jsonify({"cached_result": similar_claim.result}), 200

    # If no match, call Google API
    url = f"https://factchecktools.googleapis.com/v1alpha1/claims:search?query={query_cleaned}&key={FACT_CHECK_API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise error for non-200 responses

        results = response.json()
        new_claim = Claim(claim_text=query_cleaned, result=str(results))
        db.session.add(new_claim)
        db.session.commit()

        return jsonify(results), 200

    except requests.exceptions.RequestException as e:
        logging.error(f"Request Exception: {str(e)}")
        return jsonify({"error": f"An error occurred while connecting to the API: {str(e)}"}), 500

    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500


# Route to get innovation news
@fact_checker.route("/innovation_news", methods=["GET"])
def innovation_news():
    query = request.args.get("query", "innovation")
    news_service = NewsService()
    articles = news_service.get_innovation_articles(query=query)

    if "error" in articles:
        return jsonify({"error": articles["error"]}), 500
    return jsonify({"articles": articles}), 200


# New Route for Coming Soon Features
@fact_checker.route("/coming_soon", methods=["GET"])
def coming_soon():
    upcoming_features = [
        {"feature": "User Profile Management", "status": "In Development"},
        {"feature": "Achievements Leaderboard", "status": "Planned"},
        {"feature": "Real-Time Notifications", "status": "In Planning"}
    ]
    return jsonify({"coming_soon": upcoming_features}), 200


# Auth Blueprint for user authentication routes
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400

    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid username or password"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({"message": "Login successful", "access_token": access_token}), 200


@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify({"message": f"Hello, {user.username}!"}), 200


# Route to create or update user progress
@progress_bp.route('/progress', methods=['POST'])
@jwt_required()
def update_progress():
    # Get the user_id from the JWT identity
    user_id = get_jwt_identity()
    data = request.get_json()
    achievement = data.get('achievement')

    if not achievement:
        return jsonify({"error": "Achievement is required"}), 400

    # Check if the user already has progress
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    new_progress = Progress(user_id=user_id, achievement=achievement)
    db.session.add(new_progress)
    db.session.commit()

    return jsonify({"message": "Progress updated successfully"}), 200


def predict_goal_completion(user_id):
    progress_entries = Progress.query.filter_by(user_id=user_id).all()
    if len(progress_entries) < 3:
        return "Not enough data for predictions"

    # Convert progress timestamps to numerical format
    dates = [p.created_at.timestamp() for p in progress_entries]
    values = list(range(1, len(dates) + 1))  # Representing progress numerically

    # Convert to numpy arrays for ML model
    X = np.array(dates).reshape(-1, 1)
    y = np.array(values)

    # Train a simple Linear Regression model
    model = LinearRegression()
    model.fit(X, y)

    # Predict future completion date
    future_value = len(values) + 1  # Next expected progress step
    predicted_time = model.predict(np.array([[max(dates) + (86400 * 7)]]))  # Predict 1 week ahead

    return f"At your current pace, you'll complete your next milestone by {pd.to_datetime(predicted_time[0], unit='s')}."


# Route to retrieve user progress
@progress_bp.route('/progress/<int:user_id>', methods=['GET'])
@jwt_required()
def get_progress(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    progress = Progress.query.filter_by(user_id=user_id).all()
    progress_data = [{"id": p.id, "achievement": p.achievement, "created_at": p.created_at} for p in progress]

    # Get AI-based progress prediction
    prediction = predict_goal_completion(user_id)

    return jsonify({
        "user_id": user_id,
        "progress": progress_data,
        "prediction": prediction
    }), 200

# This function fetches goal recommendations for a user by sending all available goals
# to the Wolfram API for clustering analysis. If there are fewer than 3 goals, no
# recommendations are made. It returns a list of recommended goals based on Wolfram's analysis.
def get_goal_recommendations(user_id):
    """
    Fetches goal recommendations for a user by leveraging the Wolfram API for clustering.

    Parameters:
        user_id (int): The ID of the user requesting recommendations.

    Returns:
        list: A list of recommended goal clusters if available, otherwise an empty list.
    """

    # Retrieve the user from the database
    user = User.query.get(user_id)
    if not user:
        return []  # Return an empty list if the user doesn't exist

    # Fetch all goals from the database
    all_goals = [g.goal for g in Goal.query.all()]

    # Ensure there are enough goals to perform clustering (Wolfram's FindClusters requires at least 3)
    if len(all_goals) < 3:
        return []

    # Get the Wolfram API URL from the app configuration
    WOLFRAM_API_URL = current_app.config.get("WOLFRAM_API_URL")

    try:
        # Send a request to the Wolfram API with the list of goals
        response = requests.post(WOLFRAM_API_URL, json={"goals": all_goals})

        # Parse the response as JSON
        wolfram_result = response.json()

        # Extract and return the recommended goal clusters from the response
        return wolfram_result.get("recommended_goals", [])

    except Exception as e:
        # Return an empty list if an error occurs (e.g., API failure, network issues)
        return []


# Route to create a goal for the user and show AI recommendations
@progress_bp.route('/goal', methods=['POST'])
@jwt_required()
def create_goal():
    # We get the user_id from the JWT identity
    user_id = get_jwt_identity()
    data = request.get_json()
    goal = data.get('goal')
    target_date = data.get('target_date')

    if not goal or not target_date:
        return jsonify({"error": "Goal and target_date are required"}), 400

    new_goal = Goal(user_id=user_id, goal=goal, target_date=target_date)
    db.session.add(new_goal)
    db.session.commit()

    # Get AI-based recommendations
    recommendations = get_goal_recommendations(user_id)

    return jsonify({
        "message": "Goal created successfully!",
        "recommended_goals": recommendations
    }), 200


# Route to retrieve user's goals
@progress_bp.route('/goals', methods=['GET'])
@jwt_required()
def get_goals():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    goals = Goal.query.filter_by(user_id=user_id).all()
    goals_data = [{"id": goal.id, "goal": goal.goal, "target_date": goal.target_date, "created_at": goal.created_at} for goal in goals]

    return jsonify({"user_id": user_id, "goals": goals_data}), 200


# Function to register all blueprints
def register_blueprints(app):
    app.register_blueprint(fact_checker)  # Register the fact-checker blueprint
    app.register_blueprint(auth_bp)       # Register the auth blueprint
    app.register_blueprint(progress_bp)  # Register the progress blueprint
    app.register_blueprint(wolfram_bp)  # Register the wolfram blueprint