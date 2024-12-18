from dataclasses import dataclass
import logging
import sqlite3
from typing import Any
import requests
from dotenv import load_dotenv
import os
from datetime import datetime


from meal_max.models.user_model import User
from meal_max.utils.logger import configure_logger

load_dotenv()

logger = logging.getLogger(__name__)
configure_logger(logger)

def fetch_current_weather(username: str):
    """
    Fetches current weather data for the user's favorite location.

    Args:
        user_id (int): The ID of the user.

    Returns:
        dict: Current weather data.
    """

    #Error handling for location (What if location returned an empty array etc?)
    location = User.get_favorite(username)
    if not location or None in location or len(location) < 3:
        raise ValueError("Invalid location data provided.")


    #Error checking for the API handling 
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise ValueError("API key is missing or invalid.")

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": location[1],
        "lon": location[2],
        "units": "metric",
        "appid": api_key,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return {
        "location": location[0],
        "current_weather": response.json()
    }

def fetch_weather_overview(username: str):
    """
    Fetches weather overview data for the user's favorite location.

    Args:
        username (str): The username of the user.

    Returns:
        dict: Weather overview data.
    """
    # Error handling for location
    location = User.get_favorite(username)
    if not location or None in location or len(location) < 3:
        raise ValueError("Invalid location data provided.")

    # Error checking for the API key
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise ValueError("API key is missing or invalid.")

    url = "https://api.openweathermap.org/data/3.0/onecall/overview"
    params = {
        "lat": location[1],
        "lon": location[2],
        "appid": api_key,
    }
    
    # Sending the GET request to the OpenWeather API
    response = requests.get(url, params=params)
    response.raise_for_status()  # This will raise an error if the API call fails
    
    # Return the response data along with the location
    return {
        "location": location[0],
        "weather_overview": response.json()  # JSON response from OpenWeather API
    }


def fetch_forecast(username: str):
    """
    Fetches a 7-day weather forecast for the user's favorite location.

    Args:
        user_id (int): The ID of the user.

    Returns:
        dict: Weather forecast data.
    """
    location = User.get_favorite(username)

    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise ValueError("API key is missing or invalid.")
    
    url = "https://api.openweathermap.org/data/3.0/onecall"
    params = {
        "lat": location[1],
        "lon": location[2],
        "exclude": "current,minutely,hourly",
        "units": "metric",
        "appid": api_key,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return {
        "location": location[0],
        "forecast": response.json().get("daily", [])
    }

def fetch_historical_weather(username: str, query_date: str):
    """
    Fetches historical weather data for the user's favorite location.

    Args:
        user_id (int): The ID of the user.
        query_date (str): The date in YYYY-MM-DD format.

    Returns:
        dict: Historical weather data.
    """
    location = User.get_favorite(username)
    
    unix_timestamp = int(datetime.strptime(query_date, "%Y-%m-%d").timestamp())
    #end_timestamp = int(datetime.now().timestamp())

    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise ValueError("API key is missing or invalid.")
    
    url = "https://api.openweathermap.org/data/3.0/onecall/timemachine"
    params = {
        "lat": location[1],
        "lon": location[2],
        "dt": unix_timestamp,
        "units": "metric",
        "appid": api_key,
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    return {
        "location": location[0],
        "date": query_date,
        "historical_weather": response.json()
    }

def fetch_air_quality(username: str):
    """
    Fetches air quality data for the user's favorite location.

    Args:
        user_id (int): The ID of the user.

    Returns:
        dict: Air quality data.
    """
    location = User.get_favorite(username)
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise ValueError("API key is missing or invalid.")
    
    url = "https://api.openweathermap.org/data/2.5/air_pollution"
    params = {
        "lat": location[1],
        "lon": location[2],
        "appid": api_key,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return {
        "location": location[0],
        "air_quality": response.json()
    }

