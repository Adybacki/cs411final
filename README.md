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
```json
{
  "status": "healthy"
}
```

#### **Database Check**  
**Path**: `/api/db-check`  
**Request Type**: `GET`  
**Purpose**: Ensures the database connection is established and the `meals` table exists.  
**Request Format**: None  
**Response Format**:
```json
{
  "database_status": "healthy"
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
curl -X GET http://localhost:5000/api/db-check
```
Response:
```json
{
  "database_status": "healthy"
}
```

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

### Weather Services
#### **Current Weather**  
**Path**: `/api/current-weather`  
**Request Type**: `GET`  
**Purpose**: Fetches current weather data for the user's favorite location.  
**Request Format** (Query parameters):
- `user_id` (int): User ID
**Response Format**:
```json
{
  "temperature": 72,
  "condition": "Sunny"
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
curl -X GET "http://localhost:5000/api/current-weather?user_id=1"
```

#### **Weather Forecast**  
**Path**: `/api/forecast`  
**Request Type**: `GET`  
**Purpose**: Fetches a 7-day weather forecast for the user's favorite location.  
**Request Format** (Query parameters):
- `user_id` (int): User ID
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
- `user_id` (int): User ID
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
- `user_id` (int): User ID
**Response Format**:
```json
{
  "air_quality": {
    "pm2_5": 12,
    "pm10": 20,
    "o3": 15
  }
}
```
**Example**:
```bash
curl -X GET "http://localhost:5000/api/air-quality?user_id=1"
```

---

## Getting Started
1. Clone the repository and navigate to the project directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the server:
   ```bash
   python app.py
   ```
4. Access the API at `http://localhost:5000/api`.

