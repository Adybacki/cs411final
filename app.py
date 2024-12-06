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

@app.route('/api/get-favorite', methods=['GET'])
def get_favorite() -> Response:
    """
    Route to get the favorite location from the database.

    Returns:
        JSON response with the favorite location.
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id')

        if not user_id:
            return make_response(jsonify({'error': 'Invalid input, user_id is required'}), 400)
        
        location = user_model.get_favorite(user_id)
        return make_response(jsonify(location), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)

@app.route('/api/set-favorite', methods=['POST'])
def set_favorite() -> Response:
    """
    Route to set the favorite location in the database.

    Expected JSON Input:
        - location_name (str): Name of the location.
        - latitude (float): Latitude of the location.
        - longitude (float): Longitude of the location.
    """
    data = request.get_json()
    location_name = data.get('location_name')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    if not location_name or not latitude or not longitude:
        return make_response(jsonify({'error': 'Invalid input, all fields are required'}), 400)
    # Call the model to set the favorite
    try:
        user_model.set_favorite(location_name, latitude, longitude)
        return make_response(jsonify({'status': 'favorite set', 'location': location_name}), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)

##########################################################
#
# Weather Routes
#
##########################################################

@app.route('/api/current-weather', methods=['GET'])
def fetch_current_weather():
    """
    Fetches current weather data for the user's favorite location.

    Returns:
        JSON response with current weather information.
    """
    try:
        location = user_model.get_favorite()
        api_key = os.getenv("OPENWEATHER_API_KEY")
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "lat": location['latitude'],
            "lon": location['longitude'],
            "units": "metric",
            "appid": api_key
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        current_weather = response.json()

        return make_response(jsonify({
            "location": location['location_name'],
            "current_weather": current_weather
        }), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)

@app.route('/api/forecast', methods=['GET'])
def fetch_forecast():
    """
    Fetches a 7-day weather forecast for the user's favorite location.

    Returns:
        JSON response with the weather forecast.
    """
    try:
        location = user_model.get_favorite()
        api_key = os.getenv("OPENWEATHER_API_KEY")
        url = "https://api.openweathermap.org/data/3.0/onecall"
        params = {
            "lat": location['latitude'],
            "lon": location['longitude'],
            "exclude": "current,minutely,hourly",
            "units": "metric",
            "appid": api_key
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        forecast = response.json().get("daily", [])

        return make_response(jsonify({
            "location": location['location_name'],
            "forecast": forecast
        }), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)

@app.route('/api/historical-weather', methods=['GET'])
def fetch_historical_weather():
    """
    Fetches historical weather data for the user's favorite location on a specific date.

    Query Parameters:
        - date (str): The date in YYYY-MM-DD format.

    Returns:
        JSON response with the historical weather data.
    """
    try:
        query_date = request.args.get("date")
        if not query_date:
            return make_response(jsonify({"error": "Date parameter is required"}), 400)

        location = user_model.get_favorite()
        unix_timestamp = int(datetime.strptime(query_date, "%Y-%m-%d").timestamp())

        api_key = os.getenv("OPENWEATHER_API_KEY")
        url = "https://api.openweathermap.org/data/3.0/onecall/timemachine"
        params = {
            "lat": location['latitude'],
            "lon": location['longitude'],
            "dt": unix_timestamp,
            "units": "metric",
            "appid": api_key
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        historical_weather = response.json().get("current", {})

        return make_response(jsonify({
            "location": location['location_name'],
            "date": query_date,
            "historical_weather": historical_weather
        }), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)

@app.route('/api/air-quality', methods=['GET'])
def fetch_air_quality():
    """
    Fetches air quality data for the user's favorite location.

    Returns:
        JSON response with air quality information.
    """
    try:
        location = user_model.get_favorite()
        api_key = os.getenv("OPENWEATHER_API_KEY")
        url = "https://api.openweathermap.org/data/2.5/air_pollution"
        params = {
            "lat": location['latitude'],
            "lon": location['longitude'],
            "appid": api_key
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        air_quality = response.json()

        return make_response(jsonify({
            "location": location['location_name'],
            "air_quality": air_quality
        }), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)