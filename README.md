# README

## Application Overview
The application is a Flask-based RESTful API designed to provide user account management and weather-related services. Users can create accounts, log in, and access weather data (current, forecast, historical) and air quality information based on their favorite locations.

---

## Routes Description

### Health Checks
#### **Health Check**  
**Path**: `/api/health`  
**Request Type**: `GET`  
**Purpose**: Verifies that the service is running and healthy.  
**Request Format**: None  
**Response Format**:
```json
{
  "status": "healthy"
}
```
**Example**:
```bash
curl -X GET http://localhost:5000/api/health
```
Response:
Service is healthy.

---

### User Management
#### **Create Account**  
**Path**: `/api/create-account`  
**Request Type**: `POST`  
**Purpose**: Creates a new user account.  
**Request Format** (JSON body):
```json
{
  "username": "testuser",
  "password": "password123"
}
```
**Response Format**:
```json
{
  "status": "account created",
  "username": "testuser"
}
```
or:
```json
{
  "error": "Error message"
}
```
**Example**:
```bash
curl -X POST http://localhost:5000/api/create-account \
-H "Content-Type: application/json" \
-d '{"username":"testuser", "password":"password123"}'
```

#### **Update Password**  
**Path**: `/api/update-password`  
**Request Type**: `POST`  
**Purpose**: Updates the password for an existing user account.  
**Request Format** (JSON body):
```json
{
  "username": "testuser",
  "password": "newpassword123"
}
```
**Response Format**:
```json
{
  "status": "password updated",
  "username": "testuser"
}
```
or:
```json
{
  "error": "Error message"
}
```
**Example**:
```bash
curl -X POST http://localhost:5000/api/update-password \
-H "Content-Type: application/json" \
-d '{"username":"testuser", "password":"newpassword123"}'
```

#### **Login**  
**Path**: `/api/login`  
**Request Type**: `POST`  
**Purpose**: Authenticates a user with their username and password.  
**Request Format** (JSON body):
```json
{
  "username": "testuser",
  "password": "password123"
}
```
**Response Format**:
```json
{
  "status": "login successful",
  "username": "testuser"
}
```
or:
```json
{
  "error": "login failed"
}
```
**Example**:
```bash
curl -X POST http://localhost:5000/api/login \
-H "Content-Type: application/json" \
-d '{"username":"testuser", "password":"password123"}'
```
---

#### **Set Favorite**  
**Path**: `/api/set-favorite`  
**Request Type**: `POST`  
**Purpose**: Sets the user's favorite city along with its latitude and longitude coordinates.  
**Request Format** (JSON body):
```json
{
  "username": "testuser",
  "city_name": "New York",
  "longitude": 40.7128,
  "latitude": -74.0060
}
```
**Response Format**:
```json
{
  "city_name": "New York",
  "status": "favorite location set",
  "username": "testuser"
}
```
or:
```json
{
  "error": "failed to set favorite location"
}
```
**Example**:
```bash
curl -X POST http://localhost:5000/api/set-favorite \
-H "Content-Type: application/json" \
-d '{"username":"testuser", "city_name": "New York", "longitude": 40.7128, "latitude": -74.0060}'
```

---

### Weather Services
#### **Current Weather**  
**Path**: `/api/current-weather`  
**Request Type**: `GET`  
**Purpose**: Fetches current weather data for the user's favorite location.  
**Request Format** (Query parameters):
- `username` (str): Username
**Response Format**:
```json
{
 "current_weather": {
    "base": "stations",
    "clouds": {
      "all": 100
    },
    "cod": 200,
    "coord": {
      "lat": 40.7145,
      "lon": -74.0114
    },
    "dt": 1733804545,
    "id": 5128581,
    "main": {
      "feels_like": 7.32,
      "grnd_level": 1014,
      "humidity": 91,
      "pressure": 1015,
      "sea_level": 1015,
      "temp": 8.77,
      "temp_max": 9.54,
      "temp_min": 7.11
    },
    "name": "New York",
    "sys": {
      "country": "US",
      "id": 2008776,
      "sunrise": 1733746131,
      "sunset": 1733779721,
      "type": 2
    },
    "timezone": -18000,
    "visibility": 9656,
    "weather": [
      {
        "description": "mist",
        "icon": "50n",
        "id": 701,
        "main": "Mist"
      }
    ],
    "wind": {
      "deg": 50,
      "speed": 2.57
    }
  },
  "location": "New York"
}
```
or:
```json
{
  "error": "Error message"
}
```
**Example**:
```bash
curl -X GET "http://localhost:5000/api/current-weather?username=testuser"
```

#### **Weather Forecast**  
**Path**: `/api/forecast`  
**Request Type**: `GET`  
**Purpose**: Fetches a 7-day weather forecast for the user's favorite location.  
**Request Format** (Query parameters):
- `username` (str): Username
**Response Format**:
```json
{
  "forecast": [
    {"day": "Monday", "temperature": 70, "condition": "Rainy"},
    {"day": "Tuesday", "temperature": 75, "condition": "Cloudy"}
  ]
}
```
**Example**:
```bash
curl -X GET "http://localhost:5000/api/forecast?user_id=1"
```

#### **Historical Weather**  
**Path**: `/api/historical-weather`  
**Request Type**: `GET`  
**Purpose**: Fetches historical weather data for a specified date.  
**Request Format** (Query parameters):
- `username` (str): Username
- `date` (string): Date in `YYYY-MM-DD` format
**Response Format**:
```json
{
  "historical_weather": {
    "date": "2023-12-01",
    "temperature": 65,
    "condition": "Clear"
  }
}
```
**Example**:
```bash
curl -X GET "http://localhost:5000/api/historical-weather?user_id=1&date=2023-12-01"
```

#### **Air Quality**  
**Path**: `/api/air-quality`  
**Request Type**: `GET`  
**Purpose**: Fetches air quality data for the user's favorite location.  
**Request Format** (Query parameters):
- `username` (str): Username
**Response Format**:
```json
{
  "air_quality": {
    "coord": {
      "lat": 40.7128,
      "lon": -74.006
    },
    "list": [
      {
        "components": {
          "co": 500.68,
          "nh3": 0.65,
          "no": 7.94,
          "no2": 50.72,
          "o3": 1.33,
          "pm10": 23.07,
          "pm2_5": 18.66,
          "so2": 2.41
        },
        "dt": 1733804469,
        "main": {
          "aqi": 2
        }
      }
    ]
  },
  "location": "New York"
}
```
**Example**:
```bash
curl -X GET "http://localhost:5000/api/air-quality?username=testuser"
```
