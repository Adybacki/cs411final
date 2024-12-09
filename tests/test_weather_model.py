import pytest
from unittest.mock import MagicMock
from meal_max.models.weather_model import fetch_current_weather, fetch_forecast, fetch_historical_weather, fetch_air_quality
from datetime import datetime



def test_fetch_current_weather(mocker):
    user_id = 1

    # Mock get_favorite
    mock_get_favorite = mocker.patch("meal_max.models.weather_model.get_favorite")
    mock_get_favorite.return_value = ("Boston", 42.3601, -71.0589)

    # Mock os.getenv to return a valid API key
    mocker.patch("os.getenv", return_value="mock_api_key")

    # Mock requests.get
    mock_requests_get = mocker.patch("meal_max.models.weather_model.requests.get")
    mock_response = MagicMock()
    mock_response.json.return_value = {"weather": [{"description": "clear sky"}], "main": {"temp": 10}}
    mock_response.raise_for_status = MagicMock()
    mock_requests_get.return_value = mock_response

    # Call the function
    result = fetch_current_weather(user_id)

    # Assertions
    assert result["location"] == "Boston"
    assert "current_weather" in result
    assert result["current_weather"]["main"]["temp"] == 10
    mock_get_favorite.assert_called_once_with(user_id)
    mock_requests_get.assert_called_once()


def test_fetch_forecast(mocker):
    user_id = 2

    # Mock get_favorite
    mock_get_favorite = mocker.patch("meal_max.models.weather_model.get_favorite")
    mock_get_favorite.return_value = ("Los Angeles", 34.0522, -118.2437)

    # Mock requests.get
    mock_requests_get = mocker.patch("meal_max.models.weather_model.requests.get")
    mock_response = MagicMock()
    mock_response.json.return_value = {"daily": [{"temp": {"day": 25}, "weather": [{"description": "sunny"}]}]}
    mock_response.raise_for_status = MagicMock()
    mock_requests_get.return_value = mock_response

    # Call the function
    result = fetch_forecast(user_id)

    # Assertions
    assert result["location"] == "Los Angeles"
    assert "forecast" in result
    assert result["forecast"][0]["temp"]["day"] == 25
    mock_get_favorite.assert_called_once_with(user_id)
    mock_requests_get.assert_called_once()



def test_fetch_historical_weather(mocker):
    user_id = 3
    query_date = "2023-12-01"

    # Mock get_favorite
    mock_get_favorite = mocker.patch("meal_max.models.weather_model.get_favorite")
    mock_get_favorite.return_value = ("San Francisco", 37.7749, -122.4194)

    # Mock requests.get
    mock_requests_get = mocker.patch("meal_max.models.weather_model.requests.get")
    mock_response = MagicMock()
    mock_response.json.return_value = {"current": {"temp": 15, "weather": [{"description": "cloudy"}]}}
    mock_response.raise_for_status = MagicMock()
    mock_requests_get.return_value = mock_response

    # Call the function
    result = fetch_historical_weather(user_id, query_date)

    # Assertions
    assert result["location"] == "San Francisco"
    assert result["date"] == query_date
    assert "historical_weather" in result
    assert result["historical_weather"]["temp"] == 15
    mock_get_favorite.assert_called_once_with(user_id)
    mock_requests_get.assert_called_once()


def test_fetch_air_quality(mocker):
    user_id = 4

    # Mock get_favorite
    mock_get_favorite = mocker.patch("meal_max.models.weather_model.get_favorite")
    mock_get_favorite.return_value = ("Seattle", 47.6062, -122.3321)

    # Mock requests.get
    mock_requests_get = mocker.patch("meal_max.models.weather_model.requests.get")
    mock_response = MagicMock()
    mock_response.json.return_value = {"list": [{"main": {"aqi": 3}, "components": {"pm2_5": 12.0}}]}
    mock_response.raise_for_status = MagicMock()
    mock_requests_get.return_value = mock_response

    # Call the function
    result = fetch_air_quality(user_id)

    # Assertions
    assert result["location"] == "Seattle"
    assert "air_quality" in result
    assert result["air_quality"]["list"][0]["main"]["aqi"] == 3
    mock_get_favorite.assert_called_once_with(user_id)
    mock_requests_get.assert_called_once()


#------------------------------------ Working on edge cases ---------------------------------------------------------
def test_fetch_current_weather_missing_api_key(mocker):
    user_id = 1

    # Mock get_favorite
    mocker.patch("meal_max.models.weather_model.get_favorite", return_value=("Boston", 42.3601, -71.0589))

    # Mock os.getenv to simulate missing API key
    mocker.patch("os.getenv", return_value=None)

    # Assert ValueError is raised
    with pytest.raises(ValueError, match="API key is missing or invalid."):
        fetch_current_weather(user_id)

def test_fetch_current_weather_invalid_location(mocker):
    user_id = 1

    # Mock get_favorite to return invalid location
    mocker.patch("meal_max.models.weather_model.get_favorite", return_value=(None, None, None))

    # Assert ValueError is raised
    with pytest.raises(ValueError, match="Invalid location data provided."):
        fetch_current_weather(user_id)

def test_fetch_forecast_empty_response(mocker):
    user_id = 2

    # Mock get_favorite
    mocker.patch("meal_max.models.weather_model.get_favorite", return_value=("Los Angeles", 34.0522, -118.2437))

    # Mock requests.get to return an empty forecast response
    mock_response = mocker.Mock()
    mock_response.json.return_value = {}
    mock_response.raise_for_status = mocker.Mock()
    mocker.patch("requests.get", return_value=mock_response)

    # Call the function
    result = fetch_forecast(user_id)

    # Assertions
    assert result["location"] == "Los Angeles"
    assert result["forecast"] == []

def test_fetch_historical_weather_invalid_date(mocker):
    user_id = 3
    query_date = "not-a-date"

    # Mock get_favorite
    mocker.patch("meal_max.models.weather_model.get_favorite", return_value=("San Francisco", 37.7749, -122.4194))

    # Assert ValueError is raised
    with pytest.raises(ValueError, match="time data 'not-a-date' does not match format '%Y-%m-%d'"):
        fetch_historical_weather(user_id, query_date)

