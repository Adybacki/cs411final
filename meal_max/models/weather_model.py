from dataclasses import dataclass
import logging
import sqlite3
from typing import Any
import requests
from dotenv import load_dotenv
import os
from datetime import datetime


from meal_max.models.user_model import User, get_favorite
from meal_max.utils.sql_utils import get_db_connection
from meal_max.utils.logger import configure_logger

load_dotenv()

logger = logging.getLogger(__name__)
configure_logger(logger)

def fetch_current_weather(user_id: int):
    """
    Fetches current weather data for the user's favorite location.

    Args:
        user_id (int): The ID of the user.

    Returns:
        dict: Current weather data.
    """

    #Error handling for location (What if location returned an empty array etc?)
    location = get_favorite(user_id)
    if not location or None in location or len(location) < 3:
        raise ValueError("Invalid location data provided.")


    #Error checking for the API handling (What i)
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

def fetch_forecast(user_id: int):
    """
    Fetches a 7-day weather forecast for the user's favorite location.

    Args:
        user_id (int): The ID of the user.

    Returns:
        dict: Weather forecast data.
    """
    location = get_favorite(user_id)

    api_key = os.getenv("OPENWEATHER_API_KEY")
    
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

def fetch_historical_weather(user_id: int, query_date: str):
    """
    Fetches historical weather data for the user's favorite location.

    Args:
        user_id (int): The ID of the user.
        query_date (str): The date in YYYY-MM-DD format.

    Returns:
        dict: Historical weather data.
    """
    location = get_favorite(user_id)
    
    unix_timestamp = int(datetime.strptime(query_date, "%Y-%m-%d").timestamp())
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
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
        "historical_weather": response.json().get("current", {})
    }

def fetch_air_quality(user_id: int):
    """
    Fetches air quality data for the user's favorite location.

    Args:
        user_id (int): The ID of the user.

    Returns:
        dict: Air quality data.
    """
    location = get_favorite(user_id)
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
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

