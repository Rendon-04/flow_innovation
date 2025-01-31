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



# Blueprint for fact-checking, progress
fact_checker = Blueprint("fact_checker", __name__)
progress_bp = Blueprint('progress', __name__)

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


# Function for AI recommendations
def get_goal_recommendations(user_id):
    user = User.query.get(user_id)
    if not user:
        return []

    # Fetch past goals from all users
    all_goals = [g.goal for g in Goal.query.all()]
    
    if len(all_goals) < 3:  # Not enough data to cluster
        return []

    # Convert text goals into numerical vectors
    vectorizer = TfidfVectorizer()
    goal_vectors = vectorizer.fit_transform(all_goals)

    # Cluster goals using K-Means
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    kmeans.fit(goal_vectors)

    # Get cluster of current user's last goal
    user_last_goal = Goal.query.filter_by(user_id=user_id).order_by(Goal.created_at.desc()).first()
    if not user_last_goal:
        return []

    user_goal_vector = vectorizer.transform([user_last_goal.goal])
    cluster_label = kmeans.predict(user_goal_vector)[0]

    # Recommend other goals from the same cluster
    recommended_goals = [all_goals[i] for i in range(len(all_goals)) if kmeans.labels_[i] == cluster_label]
    
    return recommended_goals[:3]  # Return top 3 recommendations


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