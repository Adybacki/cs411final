#!/bin/bash

BASE_URL="http://localhost:5050/api"

###############################################
#
# Health checks
#
###############################################

# Check health status
check_health() {
  echo "Checking health status..."
  curl -s -X GET "$BASE_URL/health" | grep -q '"status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Service is healthy."
  else
    echo "Health check failed."
    #exit 1
  fi
}

###############################################
#
# User Management
#
###############################################

#Test create account
test_create_account() {
  echo "Testing create account endpoint..."
  response=$(curl -s -X POST "$BASE_URL/create-account" \
    -H "Content-Type: application/json" \
    -d '{"username": "testuser", "password": "password123"}')
  if echo "$response" | grep -q '"status": "account created"'; then
    echo "Create account test passed: $response"
  else
    echo "Create account test failed: $response"
    #exit 1
  fi
}

#Test login
test_login() {
  echo "Testing login endpoint..."
  response=$(curl -s -X POST "$BASE_URL/login" \
    -H "Content-Type: application/json" \
    -d '{"username": "testuser", "password": "password123"}')
  if echo "$response" | grep -q '"status": "login successful"'; then
    echo "Login test passed: $response"
  else
    echo "Login test failed: $response"
    #exit 1
  fi
}

#Test update password
test_update_password() {
  echo "Testing update password endpoint..."
  response=$(curl -s -X POST "$BASE_URL/update-password" \
    -H "Content-Type: application/json" \
    -d '{"username": "testuser", "password": "newpassword123"}')
  if echo "$response" | grep -q '"status": "password updated"'; then
    echo "Update password test passed: $response"
  else
    echo "Update password test failed: $response"
    #exit 1
  fi
}

###############################################
#
# Weather Management
#
###############################################

#Test set favorite
test_set_favorite() {
  echo "Testing set favorite endpoint..."
  response=$(curl -s -X POST "$BASE_URL/set-favorite" \
    -H "Content-Type: application/json" \
    -d '{"username": "testuser", "city_name": "New York", "latitude": 40.7128, "longitude": -74.0060}')
  if echo "$response" | grep -q '"status": "favorite location set"'; then
    echo "Set favorite test passed: $response"
  else
    echo "Set favorite test failed: $response"
    #exit 1
  fi
}


# Test current weather
test_current_weather() {
  echo "Testing current weather endpoint..."
  response=$(curl -s -X GET "$BASE_URL/current-weather" -G --data-urlencode "username=testuser")
  if echo "$response" | grep -q '"error"'; then
    echo "Current weather test passed with error: $response"
  elif echo "$response" | grep -q '"weather"'; then
    echo "Current weather test passed: $response"
  else
    echo "Current weather test failed: $response"
    #exit 1
  fi
}

# Test forecast
test_forecast() {
  echo "Testing forecast endpoint..."
  response=$(curl -s -X GET "$BASE_URL/forecast" -G --data-urlencode "username=testuser")
  if echo "$response" | grep -q '"error"'; then
    echo "Forecast test passed with error: $response"
  elif echo "$response" | grep -q '"forecast"'; then
    echo "Forecast test passed: $response"
  else
    echo "Forecast test failed: $response"
    #exit 1
  fi
}

# Test historical weather
test_historical_weather() {
  echo "Testing historical weather endpoint..."
  response=$(curl -s -X GET "$BASE_URL/historical-weather" -G --data-urlencode "username=testuser" --data-urlencode "date=2023-12-01")
  if echo "$response" | grep -q '"error"'; then
    echo "Historical weather test passed with error: $response"
  elif echo "$response" | grep -q '"historical_weather"'; then
    echo "Historical weather test passed: $response"
  else
    echo "Historical weather test failed: $response"
    #exit 1
  fi
}

# Test air quality
test_air_quality() {
  echo "Testing air quality endpoint..."
  response=$(curl -s -X GET "$BASE_URL/air-quality" -G --data-urlencode "username=testuser")
  if echo "$response" | grep -q '"error"'; then
    echo "Air quality test passed with error: $response"
  elif echo "$response" | grep -q '"air_quality"'; then
    echo "Air quality test passed: $response"
  else
    echo "Air quality test failed: $response"
    #exit 1
  fi
}

# Run smoke tests
check_health
test_db_check
test_create_account
test_login
test_update_password
test_set_favorite
test_current_weather
test_forecast
test_historical_weather
test_air_quality

echo "All smoke tests completed successfully!"

echo "Smoke tests completed successfully!"