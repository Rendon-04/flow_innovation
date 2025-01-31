from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import requests
from extensions import db
from app.models import Claim, Goal, Progress, User
from app.services.news_service import NewsService
import logging

# Blueprint for fact-checking, progress
fact_checker = Blueprint("fact_checker", __name__)
progress_bp = Blueprint('progress', __name__)

# Set up logging to capture API issues more effectively
logging.basicConfig(level=logging.DEBUG)

# Route for home page
@fact_checker.route("/")
def home():
    return jsonify({"message": "Welcome to the Fact-Checking API!"}), 200

# Route for checking claims
@fact_checker.route("/check_claim", methods=["GET", "POST"])
def check_claim():
    FACT_CHECK_API_KEY = current_app.config["FACT_CHECK_API_KEY"]
    logging.debug(f"API Key used: {FACT_CHECK_API_KEY}")

    if request.method == "GET":
        query = request.args.get("query", "")
        if not query:
            return jsonify({"error": "No query provided. Use ?query=<your_query>"}), 400
    elif request.method == "POST":
        data = request.json
        if not data or not data.get("claim"):
            return jsonify({"error": "Invalid or missing JSON payload. Provide a 'claim' field."}), 400
        query = data["claim"]

    url = f"https://factchecktools.googleapis.com/v1alpha1/claims:search?query={query}&key={FACT_CHECK_API_KEY}"
    try:
        response = requests.get(url)

        if response.status_code == 200:
            results = response.json()
            claim = Claim(claim_text=query, result=str(results))
            db.session.add(claim)
            db.session.commit()
            return jsonify(results), 200
        else:
            error_details = response.json().get('error', {})
            error_message = error_details.get('message', 'Unknown error')
            logging.error(f"Google API Error: {error_message}")
            return jsonify({"error": f"Failed to fetch data from the API: {error_message}"}), 500

    except requests.exceptions.RequestException as e:
        logging.error(f"Request exception: {str(e)}")
        return jsonify({"error": f"An error occurred while connecting to the API: {str(e)}"}), 500

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

# Route to retrieve user progress
@progress_bp.route('/progress/<int:user_id>', methods=['GET'])
@jwt_required()
def get_progress(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    progress = Progress.query.filter_by(user_id=user_id).all()
    progress_data = [{"id": p.id, "achievement": p.achievement, "created_at": p.created_at} for p in progress]

    return jsonify({"user_id": user_id, "progress": progress_data}), 200

# Route to create a goal for the user
@progress_bp.route('/goal', methods=['POST'])
@jwt_required()
def create_goal():
    # Get the user_id from the JWT identity
    user_id = get_jwt_identity()
    data = request.get_json()
    goal = data.get('goal')
    target_date = data.get('target_date')

    if not goal or not target_date:
        return jsonify({"error": "Goal and target_date are required"}), 400

    new_goal = Goal(user_id=user_id, goal=goal, target_date=target_date)
    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"message": "Goal created successfully"}), 200

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