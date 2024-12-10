from dotenv import load_dotenv
import os
import requests
import datetime

from flask import Flask, jsonify, make_response, Response, request
# from flask_cors import CORS

from meal_max.models.user_model import User
from meal_max.models import weather_model
from meal_max.db import db
from config import TestConfig



# Load environment variables from .env file
load_dotenv()

def create_app(config_class=TestConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)  # Initialize db with app
    with app.app_context():
        db.create_all()  # Recreate all tables

    user_model = User()


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

    @app.route('/api/set-favorite', methods=['POST'])
    def set_favorite_route() -> Response:
        """
        Route to set a favorite location for a user.

        Expected JSON Input:
            - username (int): The username of the user.
            - city_name (str): The name of the city.
            - latitude (float): The latitude of the city.
            - longitude (float): The longitude of the city.

        Returns:
            JSON response indicating the success of the operation.

        Raises:
            400 error if input validation fails.
            500 error if there is an issue setting the favorite location.
        """
        app.logger.info('Setting favorite location')
        try:
            # Get the JSON data from the request
            data = request.get_json()

            # Extract and validate required fields
            username = data.get('username')
            city_name = data.get('city_name')
            latitude = data.get('latitude')
            longitude = data.get('longitude')

            if not (username and city_name and latitude and longitude):
                return make_response(jsonify({'error': 'Invalid input, all fields are required'}), 400)

            # Call the user_model function to set the favorite location
            app.logger.info('Setting favorite location for user %s: %s', username, city_name)
            user_model.set_favorite(str(username), city_name, float(latitude), float(longitude))

            app.logger.info("Favorite location set for user %s: %s", username, city_name)
            return make_response(jsonify({'status': 'favorite location set', 'username': username, 'city_name': city_name}), 200)
        except Exception as e:
            app.logger.error("Failed to set favorite location: %s", str(e))
            return make_response(jsonify({'error': str(e)}), 500)


    @app.route('/api/current-weather', methods=['GET'])
    def fetch_current_weather_route():
        """
        route to fetch current weather data for the user's favorite location.

        Returns:
            JSON response containing the current weather data.

        Raises:
            500 error if there is an issue fetching the weather data.
        """
        username = request.args.get("username")
        try:
            current_weather_data = weather_model.fetch_current_weather(str(username))
            return make_response(jsonify(current_weather_data), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 500)
        
    @app.route('/api/forecast', methods=['GET'])
    def fetch_forecast_route():
        """
        route to fetch 7-day weather forecast for the user's favorite location.

        Returns:
            JSON response containing the weather forecast data.

        Raises:
            500 error if there is an issue fetching the forecast data.
        """
        username = request.args.get("username")
        try:
            forecast_data = weather_model.fetch_forecast(str(username))
            return make_response(jsonify(forecast_data), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 500)

    @app.route('/api/historical-weather', methods=['GET'])
    def fetch_historical_weather_route():
        """
        route to fetch historical weather data for the user's favorite location.

        Returns:
            JSON response containing the historical weather data.

        Raises:
            400 error if the date parameter is missing.
            500 error if there is an issue fetching the historical weather data.
        """
        username = request.args.get("username")
        query_date = request.args.get("date")
        if not query_date:
            return make_response(jsonify({"error": "Date parameter is required"}), 400)
        try:
            historical_weather_data = weather_model.fetch_historical_weather(str(username), query_date)
            return make_response(jsonify(historical_weather_data), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 500)

    @app.route('/api/air-quality', methods=['GET'])
    def fetch_air_quality_route():
        """
        route to fetch air quality data for the user's favorite location.

        Returns:
            JSON response containing the air quality data.

        Raises:
            500 error if there is an issue fetching the air quality data.
        """
        username = request.args.get("username")
        try:
            air_quality_data = weather_model.fetch_air_quality(username)
            return make_response(jsonify(air_quality_data), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 500)
        
    @app.route('/api/weather-overview', methods=['GET'])
    def fetch_weather_overview_route():
        """
        Route to fetch weather overview data for the user's favorite location.

        Returns:
            JSON response containing the weather overview data.

        Raises:
            500 error if there is an issue fetching the weather data.
        """
        username = request.args.get("username")
        try:
            weather_overview_data = weather_model.fetch_weather_overview(str(username))
            return make_response(jsonify(weather_overview_data), 200)
        except Exception as e:
            return make_response(jsonify({'error': str(e)}), 500)

    return app
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5050)