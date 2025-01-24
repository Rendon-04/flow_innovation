from flask import Blueprint, jsonify, request, current_app
import requests
from extensions import db
from models import Claim
import logging

# Blueprint for routes
fact_checker = Blueprint("fact_checker", __name__)

# Set up logging to capture API issues more effectively
logging.basicConfig(level=logging.DEBUG)

@fact_checker.route("/")
def home():
    return jsonify({"message": "Welcome to the Fact-Checking API!"}), 200


@fact_checker.route("/check_claim", methods=["GET", "POST"])
def check_claim():
    """
    Unified endpoint for fact-checking claims via GET or POST.
    """
    # Access the API key dynamically from the app's context
    FACT_CHECK_API_KEY = current_app.config["FACT_CHECK_API_KEY"]

    # Log the API key to ensure it's being retrieved correctly
    logging.debug(f"API Key used: {FACT_CHECK_API_KEY}")

    # Handle GET request
    if request.method == "GET":
        query = request.args.get("query", "")
        if not query:
            return jsonify({"error": "No query provided. Use ?query=<your_query>"}), 400
    # Handle POST request
    elif request.method == "POST":
        data = request.json
        if not data or not data.get("claim"):
            return jsonify({"error": "Invalid or missing JSON payload. Provide a 'claim' field."}), 400
        query = data["claim"]

    # Query the Google Fact Check API
    url = f"https://factchecktools.googleapis.com/v1alpha1/claims:search?query={query}&key={FACT_CHECK_API_KEY}"
    try:
        response = requests.get(url)

        # Check the response status
        if response.status_code == 200:
            results = response.json()

            # Optionally save the query and response to the database
            claim = Claim(claim_text=query, result=str(results))
            db.session.add(claim)
            db.session.commit()

            return jsonify(results), 200
        else:
            # Log the error returned by the Google API
            error_details = response.json().get('error', {})
            error_message = error_details.get('message', 'Unknown error')
            logging.error(f"Google API Error: {error_message}")

            # Return a more descriptive error response
            return jsonify({"error": f"Failed to fetch data from the API: {error_message}"}), 500

    except requests.exceptions.RequestException as e:
        # Catch any other request exceptions, e.g., connection errors
        logging.error(f"Request exception: {str(e)}")
        return jsonify({"error": f"An error occurred while connecting to the API: {str(e)}"}), 500
