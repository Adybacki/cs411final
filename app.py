from dotenv import load_dotenv
import os
import requests
import datetime

from flask import Flask, jsonify, make_response, Response, request
# from flask_cors import CORS

from meal_max.models import user_model
from meal_max.models import weather_model
from meal_max.utils.sql_utils import check_database_connection, check_table_exists


# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# This bypasses standard security stuff we'll talk about later
# If you get errors that use words like cross origin or flight,
# uncomment this
# CORS(app)


####################################################
#
# Healthchecks
#
####################################################


@app.route('/api/health', methods=['GET'])
def healthcheck() -> Response:
    """
    Health check route to verify the service is running.

    Returns:
        JSON response indicating the health status of the service.
    """
    app.logger.info('Health check')
    return make_response(jsonify({'status': 'healthy'}), 200)

@app.route('/api/db-check', methods=['GET'])
def db_check() -> Response:
    """
    Route to check if the database connection and meals table are functional.

    Returns:
        JSON response indicating the database health status.
    Raises:
        404 error if there is an issue with the database.
    """
    try:
        app.logger.info("Checking database connection...")
        check_database_connection()
        app.logger.info("Database connection is OK.")
        app.logger.info("Checking if meals table exists...")
        check_table_exists("meals")
        app.logger.info("meals table exists.")
        return make_response(jsonify({'database_status': 'healthy'}), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 404)


##########################################################
#
# User Management
#
##########################################################

@app.route('/api/create-account', methods=['POST'])
def create_account() -> Response:
    """
    Route to create a new user account.

    Expected JSON Input:
        - username (str): The username for the new account.
        - password (str): The password for the new account.

    Returns:
        JSON response indicating the success of the account creation.
    Raises:
        400 error if input validation fails.
        500 error if there is an issue creating the account.
    """
    app.logger.info('Creating new account')
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Extract and validate required fields
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return make_response(jsonify({'error': 'Invalid input, both username and password are required'}), 400)

        # Call the user_model function to create the account
        app.logger.info('Creating account: %s', username)
        user_model.create_account(username, password)

        app.logger.info("Account created: %s", username)
        return make_response(jsonify({'status': 'account created', 'username': username}), 201)
    except Exception as e:
        app.logger.error("Failed to create account: %s", str(e))
        return make_response(jsonify({'error': str(e)}), 500)

@app.route('/api/update-password', methods=['POST'])
def update_password() -> Response:
    """
    Route to update the password for a user account.

    Expected JSON Input:
        - username (str): The username for the account.
        - password (str): The new password for the account.

    Returns:
        JSON response indicating the success of the password update.
    Raises:
        400 error if input validation fails.
        500 error if there is an issue updating the password.
    """
    app.logger.info('Updating password')
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Extract and validate required fields
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return make_response(jsonify({'error': 'Invalid input, both username and password are required'}), 400)

        # Call the user_model function to update the password
        app.logger.info('Updating password for account: %s', username)
        user_model.update_password(username, password)

        app.logger.info("Password updated for account: %s", username)
        return make_response(jsonify({'status': 'password updated', 'username': username}), 200)
    except Exception as e:
        app.logger.error("Failed to update password: %s", str(e))
        return make_response(jsonify({'error': str(e)}), 500)

@app.route('/api/login', methods=['POST'])
def login() -> Response:
    """
    Route to validate a user's login credentials.

    Expected JSON Input:
        - username (str): The username for the account.
        - password (str): The password for the account.

    Returns:
        JSON response indicating the success of the login.
    Raises:
        400 error if input validation fails.
        500 error if there is an issue with the login.
    """
    app.logger.info('Logging in')
    try:
        # Get the JSON data from the request
        data = request.get_json()

        # Extract and validate required fields
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return make_response(jsonify({'error': 'Invalid input, both username and password are required'}), 400)

        # Call the user_model function to validate the login
        app.logger.info('Logging in with username: %s', username)
        success = user_model.login(username, password)

        if success:
            app.logger.info("Login successful for account: %s", username)
            return make_response(jsonify({'status': 'login successful', 'username': username}), 200)
        else:
            app.logger.info("Login failed for account: %s", username)
            return make_response(jsonify({'error': 'login failed'}), 401)
    except Exception as e:
        app.logger.error("Failed to login: %s", str(e))
        return make_response(jsonify({'error': str(e)}), 500)
    
##########################################################
#
# Favorite Location Management
#
##########################################################

@app.route('/api/current-weather', methods=['GET'])
def fetch_current_weather_route():
    user_id = request.args.get("user_id")
    try:
        current_weather_data = weather_model.fetch_current_weather(int(user_id))
        return make_response(jsonify(current_weather_data), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)
    
@app.route('/api/forecast', methods=['GET'])
def fetch_forecast_route():
    user_id = request.args.get("user_id")
    try:
        forecast_data = weather_model.fetch_forecast(int(user_id))
        return make_response(jsonify(forecast_data), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)

@app.route('/api/historical-weather', methods=['GET'])
def fetch_historical_weather_route():
    user_id = request.args.get("user_id")
    query_date = request.args.get("date")
    if not query_date:
        return make_response(jsonify({"error": "Date parameter is required"}), 400)
    try:
        historical_weather_data = weather_model.fetch_historical_weather(int(user_id), query_date)
        return make_response(jsonify(historical_weather_data), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)

@app.route('/api/air-quality', methods=['GET'])
def fetch_air_quality_route():
    user_id = request.args.get("user_id")
    try:
        air_quality_data = weather_model.fetch_air_quality(int(user_id))
        return make_response(jsonify(air_quality_data), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)