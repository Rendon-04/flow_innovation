import os
import json
import logging
import requests
import spacy
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from extensions import db
from app.models import Claim, Goal, Progress, User
from app.services.news_service import NewsService
from flask_cors import cross_origin


# ✅ Define Blueprints
fact_checker = Blueprint("fact_checker", __name__)
auth_bp = Blueprint("auth", __name__)
progress_bp = Blueprint("progress", __name__)
wolfram_bp = Blueprint("wolfram", __name__)

# ✅ Load NLP Model
nlp = spacy.load("en_core_web_sm")

# Define the Blueprint
wolfram_bp = Blueprint("wolfram", __name__)

@wolfram_bp.route("/wolfram/progress_insights", methods=["GET"])
@jwt_required()  # Ensure the user is authenticated
def wolfram_progress_insights():
    """Sends user progress data to Wolfram for analysis."""
    
    user_id = get_jwt_identity()  # Extract user ID from JWT token
    
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

    # ✅ Get API URL and APPID
    WOLFRAM_API_URL = current_app.config.get("WOLFRAM_API_URL", "").strip()
    WOLFRAM_APPID = current_app.config.get("WOLFRAM_APPID", "").strip()

    if not WOLFRAM_APPID:
        return jsonify({"error": "Wolfram API AppID is missing"}), 500

    # ✅ Convert user data into a query-friendly format
    query_text = f"Analyze progress: timestamps={timestamps}, achievements={achievements}, goals={goal_texts}"

    # ✅ Prepare the GET request with `input` parameter
    url = f"{WOLFRAM_API_URL}?appid={WOLFRAM_APPID}&input={query_text}&output=json"

    logging.info(f"🚀 Sending request to Wolfram API: {url}")

    try:
        response = requests.get(url)

        logging.info(f"🌍 Wolfram API Response Status: {response.status_code}")

        if response.status_code != 200:
            logging.error(f"❌ Wolfram API Error {response.status_code}: {response.text}")
            return jsonify({"error": f"Wolfram API Error: {response.status_code}"}), response.status_code

        # ✅ Ensure the response is JSON
        try:
            wolfram_result = response.json()
        except requests.exceptions.JSONDecodeError:
            logging.error(f"❌ Wolfram API Response was not JSON. Raw response: {response.text}")
            return jsonify({"error": "Invalid response from Wolfram API", "raw_response": response.text}), 500

        # ✅ Extract and return relevant results
        return jsonify({
            "message": "Wolfram Analysis Complete",
            "next_milestone": wolfram_result.get("NextMilestoneDate", "N/A"),
            "innovation_score": wolfram_result.get("InnovationScore", "N/A"),
            "recommended_goals": wolfram_result.get("RecommendedGoals", []),
            "progress_graph": wolfram_result.get("ProgressGraph", ""),
            "future_insights": wolfram_result.get("FutureInsights", []),
            "suggestions": wolfram_result.get("Suggestions", [])
        }), 200

    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Wolfram API Request Failed: {str(e)}")
        return jsonify({"error": f"Error fetching data: {str(e)}"}), 500



# Set up logging to capture API issues more effectively
logging.basicConfig(level=logging.DEBUG)

# Helper function to clean and preprocess text
def preprocess_text(text):
    doc = nlp(text.lower())  # Convert to lowercase and tokenize
    return " ".join([token.lemma_ for token in doc if not token.is_stop])  # Lemmatization & remove stopwords

# Route for home page
@fact_checker.route("/")
def home():
    return jsonify({"message": "Welcome to the Fact-Checking API!"}), 200


@fact_checker.route("/check_claim", methods=["GET", "POST"])
def check_claim():
    FACT_CHECK_API_KEY = current_app.config["FACT_CHECK_API_KEY"]
    
    try:
        logging.debug("🟢 Received request to /check_claim")

        # Extract query
        if request.method == "GET":
            query = request.args.get("query", "").strip()
            if not query:
                logging.error("🔴 No query provided in GET request")
                return jsonify({"error": "No query provided."}), 400
        elif request.method == "POST":
            data = request.get_json()
            if not data or not data.get("claim"):
                logging.error("🔴 Invalid or missing JSON payload in POST request")
                return jsonify({"error": "Invalid JSON payload. Provide a 'claim' field."}), 400
            query = data["claim"].strip()

        logging.debug(f"🔍 Processing query: {query}")

        # Check for cached claims
        past_claims = Claim.query.all()
        past_texts = [c.claim_text for c in past_claims]

        if past_texts:
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform(past_texts + [query])
            similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
            max_similarity = max(similarities[0]) if similarities[0].size > 0 else 0

            if max_similarity > 0.7:
                similar_claim = past_claims[similarities[0].argmax()]
                
                # ✅ Ensure JSON is properly formatted
                try:
                    cached_result = json.loads(similar_claim.result)
                except json.JSONDecodeError as e:
                    logging.error(f"⚠️ JSON Decode Error in Cached Result: {str(e)}")
                    return jsonify({"error": "Cached result contains invalid JSON."}), 500

                
                logging.info(f"✅ Returning cached result for query: {query}")
                return jsonify({"cached_result": cached_result}), 200

        # Fetch new data from Google API
        url = f"https://factchecktools.googleapis.com/v1alpha1/claims:search?query={query}&key={FACT_CHECK_API_KEY}"
        logging.debug(f"🌍 Sending request to Google API: {url}")

        response = requests.get(url)
        
        if response.status_code != 200:
            logging.error(f"🔴 Google API Error {response.status_code}: {response.text}")
            return jsonify({"error": f"Google API Error: {response.status_code}"}), response.status_code

        results = response.json()
        logging.debug(f"📝 Google API Response: {json.dumps(results, indent=2)}")

        # ✅ Store result in database with valid JSON format
        try:
            formatted_json = json.dumps(results, ensure_ascii=False)
            json.loads(formatted_json)  # Validate JSON before storing
            new_claim = Claim(claim_text=query, result=formatted_json)
            db.session.add(new_claim)
            db.session.commit()
        except json.JSONDecodeError as e:
            logging.error(f"🔴 JSON Encoding Error: {str(e)}")
            return jsonify({"error": "Failed to store result due to JSON formatting issue."}), 500


    except json.JSONDecodeError as e:
        logging.error(f"🔴 JSON Decode Error: {str(e)}")
        return jsonify({"error": f"JSON Decode Error: {str(e)}"}), 500
    except requests.RequestException as e:
        logging.error(f"🔴 Request Exception: {str(e)}")
        return jsonify({"error": f"Error fetching data: {str(e)}"}), 500
    except Exception as e:
        logging.error(f"🔴 Unexpected server error: {str(e)}", exc_info=True)
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500



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

    access_token = create_access_token(identity=str(user.id))  # 🔥 Ensure it's a string

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



@progress_bp.route('/progress/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_progress(user_id):
    """Fetch progress for a specific user (admin use case)."""
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    progress = Progress.query.filter_by(user_id=user_id).all()
    progress_data = [
        {"id": p.id, "achievement": p.achievement, "created_at": p.created_at.isoformat()}
        for p in progress
    ]

    # Get AI-based progress prediction
    prediction = predict_goal_completion(user_id)

    return jsonify({
        "user_id": user_id,
        "progress": progress_data,
        "prediction": prediction
    }), 200

@progress_bp.route('/progress', methods=['GET'])
@jwt_required()
def get_progress():
    """Fetch all progress for the logged-in user."""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    progress = Progress.query.filter_by(user_id=user_id).all()
    progress_data = [
        {"id": p.id, "achievement": p.achievement, "created_at": p.created_at.isoformat()}
        for p in progress
    ]

    return jsonify({"progress": progress_data}), 200


def get_goal_recommendations(user_id):
    """
    Fetches goal recommendations for a user by leveraging the Wolfram API for clustering.
    """
    user = User.query.get(user_id)
    if not user:
        logging.warning(f"⚠️ User {user_id} not found.")
        return []

    all_goals = [g.goal for g in Goal.query.all()]

    if len(all_goals) < 3:
        logging.warning("⚠️ Not enough goals available for clustering. Need at least 3.")
        return []

    WOLFRAM_API_URL = current_app.config.get("WOLFRAM_API_URL")

    try:
        response = requests.post(WOLFRAM_API_URL, json={"goals": all_goals})
        wolfram_result = response.json()

        logging.debug(f"🔍 AI Goal Recommendations Response: {json.dumps(wolfram_result, indent=2)}")

        return wolfram_result.get("recommended_goals", [])

    except Exception as e:
        logging.error(f"🔴 AI Recommendation Error: {str(e)}")
        return []



@progress_bp.route('/goal', methods=['POST'])
@jwt_required()
def create_goal():
    """Handles goal creation with AI recommendations."""
    user_id = get_jwt_identity()
    data = request.get_json()

    logging.info(f"🚀 Received Goal Creation Request: {data}")

    # Validate data
    goal = data.get('goal')
    target_date = data.get('target_date')

    if not goal or not target_date:
        return jsonify({"error": "Goal and target_date are required"}), 400

    # Convert `target_date` from string to datetime
    try:
        target_date = datetime.strptime(target_date, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    new_goal = Goal(user_id=user_id, goal=goal, target_date=target_date)
    db.session.add(new_goal)
    db.session.commit()

    # 🔥 Fetch AI-based goal recommendations
    recommendations = get_goal_recommendations(user_id)

    logging.info(f"✅ Goal Saved! AI Recommendations: {recommendations}")

    return jsonify({
        "message": "Goal created successfully!",
        "recommended_goals": recommendations
    }), 200


@progress_bp.route('/goals', methods=['GET'])
@jwt_required()
def get_goals():
    """Fetch all goals for the logged-in user."""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    goals = Goal.query.filter_by(user_id=user_id).all()
    goals_data = [
        {"id": goal.id, "goal": goal.goal, "target_date": goal.target_date.strftime("%Y-%m-%d"), "created_at": goal.created_at}
        for goal in goals
    ]

    return jsonify({"goals": goals_data}), 200


@progress_bp.route("/progress/community", methods=["GET"])
def get_community_progress():
    """Fetch progress for all users to display in the community progress tracker."""
    all_progress = Progress.query.all()

    if not all_progress:
        return jsonify({"message": "No community progress found"}), 200

    progress_data = [
        {"id": p.id, "achievement": p.achievement, "user_id": p.user_id, "created_at": p.created_at.isoformat()}
        for p in all_progress
    ]

    return jsonify({"progress": progress_data}), 200


# Function to register all blueprints
def register_blueprints(app):
    app.register_blueprint(fact_checker)  # Register the fact-checker blueprint
    app.register_blueprint(auth_bp)       # Register the auth blueprint
    app.register_blueprint(progress_bp)  # Register the progress blueprint
    app.register_blueprint(wolfram_bp)  # Register the wolfram blueprint