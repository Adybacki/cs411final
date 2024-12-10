# README

## Application Overview
The application is a Flask-based RESTful API designed to provide user account management and weather-related services. Users can create accounts, log in, and access weather data (current, forecast, historical, air quality, and overview) and air quality information based on their favorite location.

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
**Purpose**: Fetches a 8-day weather forecast for the user's favorite location.  
**Request Format** (Query parameters):
- `username` (str): Username
**Response Format**:
```json
{
  "forecast": [
    {
      "clouds": 100,
      "dew_point": 6.71,
      "dt": 1733846400,
      "feels_like": {
        "day": 6.87,
        "eve": 8.12,
        "morn": 7.32,
        "night": 10.61
      },
      "humidity": 88,
      "moon_phase": 0.33,
      "moonrise": 1733854260,
      "moonset": 1733812140,
      "pop": 1,
      "pressure": 1019,
      "rain": 2.03,
      "summary": "You can expect partly cloudy in the morning, with rain in the afternoon",
      "sunrise": 1733832579,
      "sunset": 1733866123,
      "temp": {
        "day": 8.68,
        "eve": 9.74,
        "max": 10.88,
        "min": 7.89,
        "morn": 8.24,
        "night": 10.88
      },
      "uvi": 0.39,
      "weather": [
        {
          "description": "moderate rain",
          "icon": "10d",
          "id": 501,
          "main": "Rain"
        }
      ],
      "wind_deg": 159,
      "wind_gust": 10.09,
      "wind_speed": 4.08
    },
    {
      "clouds": 100,
      "dew_point": 12.76,
      "dt": 1733932800,
      "feels_like": {
        "day": 13.06,
        "eve": 14.68,
        "morn": 14.04,
        "night": 2.62
      },
      "humidity": 98,
      "moon_phase": 0.36,
      "moonrise": 1733942220,
      "moonset": 1733902980,
      "pop": 1,
      "pressure": 1006,
      "rain": 36.93,
      "summary": "Expect a day of partly cloudy with rain",
      "sunrise": 1733919027,
      "sunset": 1733952529,
      "temp": {
        "day": 13.13,
        "eve": 14.63,
        "max": 14.63,
        "min": 7.01,
        "morn": 14.21,
        "night": 7.01
      },
      "uvi": 0.45,
      "weather": [
        {
          "description": "heavy intensity rain",
          "icon": "10d",
          "id": 502,
          "main": "Rain"
        }
      ],
      "wind_deg": 175,
      "wind_gust": 22.62,
      "wind_speed": 10.07
    },
    {
      "clouds": 2,
      "dew_point": -9.27,
      "dt": 1734019200,
      "feels_like": {
        "day": -3.52,
        "eve": -3.56,
        "morn": -3.34,
        "night": -5.75
      },
      "humidity": 42,
      "moon_phase": 0.4,
      "moonrise": 1734030420,
      "moonset": 1733994060,
      "pop": 0.8,
      "pressure": 1021,
      "summary": "Expect a day of partly cloudy with clear spells",
      "sunrise": 1734005473,
      "sunset": 1734038938,
      "temp": {
        "day": 2.44,
        "eve": 1.86,
        "max": 6.59,
        "min": -0.24,
        "morn": 2.42,
        "night": -0.24
      },
      "uvi": 1.4,
      "weather": [
        {
          "description": "clear sky",
          "icon": "01d",
          "id": 800,
          "main": "Clear"
        }
      ],
      "wind_deg": 273,
      "wind_gust": 16.24,
      "wind_speed": 9.33
    },
    {
      "clouds": 2,
      "dew_point": -13.68,
      "dt": 1734105600,
      "feels_like": {
        "day": -3.07,
        "eve": 2.5,
        "morn": -5.64,
        "night": 2.32
      },
      "humidity": 36,
      "moon_phase": 0.44,
      "moonrise": 1734119100,
      "moonset": 1734085200,
      "pop": 0,
      "pressure": 1041,
      "summary": "Expect a day of partly cloudy with clear spells",
      "sunrise": 1734091918,
      "sunset": 1734125348,
      "temp": {
        "day": -0.26,
        "eve": 2.5,
        "max": 2.5,
        "min": -1.01,
        "morn": -0.91,
        "night": 2.32
      },
      "uvi": 1.48,
      "weather": [
        {
          "description": "clear sky",
          "icon": "01d",
          "id": 800,
          "main": "Clear"
        }
      ],
      "wind_deg": 281,
      "wind_gust": 9.84,
      "wind_speed": 5.73
    },
    {
      "clouds": 100,
      "dew_point": -8.73,
      "dt": 1734192000,
      "feels_like": {
        "day": 0.27,
        "eve": 2.98,
        "morn": 0.19,
        "night": 2.85
      },
      "humidity": 41,
      "moon_phase": 0.48,
      "moonrise": 1734208380,
      "moonset": 1734176280,
      "pop": 0,
      "pressure": 1044,
      "summary": "There will be partly cloudy today",
      "sunrise": 1734178361,
      "sunset": 1734211761,
      "temp": {
        "day": 3.4,
        "eve": 5.86,
        "max": 6.16,
        "min": 1.64,
        "morn": 1.64,
        "night": 6.16
      },
      "uvi": 2,
      "weather": [
        {
          "description": "overcast clouds",
          "icon": "04d",
          "id": 804,
          "main": "Clouds"
        }
      ],
      "wind_deg": 118,
      "wind_gust": 8.26,
      "wind_speed": 4.86
    },
    {
      "clouds": 100,
      "dew_point": 5.57,
      "dt": 1734278400,
      "feels_like": {
        "day": 5.77,
        "eve": 7.02,
        "morn": 3.96,
        "night": 8.35
      },
      "humidity": 80,
      "moon_phase": 0.5,
      "moonrise": 1734298260,
      "moonset": 1734267000,
      "pop": 1,
      "pressure": 1036,
      "rain": 12.21,
      "summary": "Expect a day of partly cloudy with rain",
      "sunrise": 1734264802,
      "sunset": 1734298176,
      "temp": {
        "day": 8.93,
        "eve": 9.33,
        "max": 9.94,
        "min": 6.74,
        "morn": 7.12,
        "night": 9.94
      },
      "uvi": 2,
      "weather": [
        {
          "description": "moderate rain",
          "icon": "10d",
          "id": 501,
          "main": "Rain"
        }
      ],
      "wind_deg": 114,
      "wind_gust": 11.44,
      "wind_speed": 6.42
    },
    {
      "clouds": 100,
      "dew_point": 9.88,
      "dt": 1734364800,
      "feels_like": {
        "day": 9.81,
        "eve": 11.01,
        "morn": 9.25,
        "night": 10.67
      },
      "humidity": 99,
      "moon_phase": 0.55,
      "moonrise": 1734388740,
      "moonset": 1734357000,
      "pop": 1,
      "pressure": 1026,
      "rain": 3.51,
      "summary": "Expect a day of partly cloudy with rain",
      "sunrise": 1734351242,
      "sunset": 1734384593,
      "temp": {
        "day": 10.15,
        "eve": 11.29,
        "max": 11.47,
        "min": 9.25,
        "morn": 9.25,
        "night": 10.98
      },
      "uvi": 2,
      "weather": [
        {
          "description": "light rain",
          "icon": "10d",
          "id": 500,
          "main": "Rain"
        }
      ],
      "wind_deg": 176,
      "wind_gust": 10.31,
      "wind_speed": 3.84
    },
    {
      "clouds": 100,
      "dew_point": 4.28,
      "dt": 1734451200,
      "feels_like": {
        "day": 8.94,
        "eve": 6.58,
        "morn": 10.25,
        "night": 2.22
      },
      "humidity": 68,
      "moon_phase": 0.58,
      "moonrise": 1734479340,
      "moonset": 1734446280,
      "pop": 1,
      "pressure": 1012,
      "rain": 12.96,
      "summary": "You can expect rain in the morning, with partly cloudy in the afternoon",
      "sunrise": 1734437679,
      "sunset": 1734471012,
      "temp": {
        "day": 10.1,
        "eve": 9.41,
        "max": 10.88,
        "min": 6.13,
        "morn": 10.55,
        "night": 6.13
      },
      "uvi": 2,
      "weather": [
        {
          "description": "moderate rain",
          "icon": "10d",
          "id": 501,
          "main": "Rain"
        }
      ],
      "wind_deg": 278,
      "wind_gust": 11.75,
      "wind_speed": 6.34
    }
  ],
  "location": "New York"

}
```
**Example**:
```bash
curl -X GET "http://localhost:5000/api/forecast?username=testuser"
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
   "date": "2023-12-01",
  "historical_weather": {
    "data": [
      {
        "clouds": 0,
        "dew_point": 0,
        "dt": 1701406800,
        "feels_like": 4.38,
        "humidity": 60,
        "pressure": 1021,
        "sunrise": 1701432038,
        "sunset": 1701466183,
        "temp": 7.24,
        "visibility": 10000,
        "weather": [
          {
            "description": "clear sky",
            "icon": "01n",
            "id": 800,
            "main": "Clear"
          }
        ],
        "wind_deg": 154,
        "wind_gust": 7.6,
        "wind_speed": 4.47
      }
    ],
    "lat": 40.7128,
    "lon": -74.006,
    "timezone": "America/New_York",
    "timezone_offset": -18000
  },
  "location": "New York"

}
```
**Example**:
```bash
curl -X GET "http://localhost:5000/api/historical-weather?username=testuser&date=2023-12-01"
```

#### **Air Quality**  
**Path**: `/api/air-quality`  
**Request Type**: `GET`  
**Purpose**: Fetches air quality data for the user's favorite location.  
**Request Format** (Query parameters):
`username` (str): Username\
**Response Format**:\
`coord` Coordinates from the specified location (latitude, longitude)\
`list`\
- `dt` Date and time, Unix, UTC\
- `main`\
- - `main.aqi` Air Quality Index. Possible values: 1, 2, 3, 4, 5. Where 1 = Good, 2 = Fair, 3 = Moderate, 4 = Poor, 5 = Very Poor. \

**Request Example**:
```bash
curl -X GET "http://localhost:5000/api/air-quality?username=testuser"
```
**Response Example**:
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


#### **Weather Overview**  
**Path**: `/api/weather-overview`  
**Request Type**: `GET`  
**Purpose**: Fetches weather overview for the user's favorite location.  
**Request Format** (Query parameters):
`username` (str): Username\
**Response Format**:<br>
`lat` Latitude of the location, decimal (−90; 90)<br>
`lon` Longitude of the location, decimal (-180; 180)<br>
`tz`  Timezone in the ±XX:XX format<br>
`date`  Date for which summary is generated in the format YYYY-MM-DD<br>
`units`  Units of measurement specified in the request<br>
`weather_overview`  AI generated weather overview for the requested date<br>

**Request Example**:
```bash
curl -X GET "http://localhost:5000/api/weather-overview?username=testuser"
```
**Response Example**:
```json
{
  "location": "New York",
  "weather_overview": {
    "date": "2024-12-10",
    "lat": 40.7128,
    "lon": -74.006,
    "tz": "-05:00",
    "units": "standard",
    "weather_overview": "Currently, the temperature is 282K with a real feel of 279K. The air pressure is at 1016 hPa, and the humidity is quite high at 93%. The dew point is at 281K, and the visibility is at 9656 meters. The wind speed is at 4 m/s coming from the northeast at 50 degrees. The sky is mostly cloudy with mist in the air. It is advised to be cautious while driving or going outside due to reduced visibility caused by the mist. Make sure to dress warmly and be prepared for damp conditions. Overall, it's a chilly and misty day with fairly calm winds. Stay safe and enjoy your day!"
  }
}
```

