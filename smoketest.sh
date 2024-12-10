#!bin/bash

BASE_URL = "http://localhost:5000/api"

#!/bin/bash

BASE_URL="http://localhost:5000/api"

# Check health status
check_health() {
  echo "Checking health status..."
  curl -s -X GET "$BASE_URL/health" | grep -q '"status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Service is healthy."
  else
    echo "Health check failed."
    exit 1
  fi
}

# Test current weather
test_current_weather() {
  echo "Testing current weather endpoint..."
  response=$(curl -s -X GET "$BASE_URL/current-weather" -G --data-urlencode "user_id=1")
  if echo "$response" | grep -q '"error"'; then
    echo "Current weather test passed with error: $response"
  elif echo "$response" | grep -q '"weather"'; then
    echo "Current weather test passed: $response"
  else
    echo "Current weather test failed: $response"
    exit 1
  fi
}

# Test forecast
test_forecast() {
  echo "Testing forecast endpoint..."
  response=$(curl -s -X GET "$BASE_URL/forecast" -G --data-urlencode "user_id=1")
  if echo "$response" | grep -q '"error"'; then
    echo "Forecast test passed with error: $response"
  elif echo "$response" | grep -q '"forecast"'; then
    echo "Forecast test passed: $response"
  else
    echo "Forecast test failed: $response"
    exit 1
  fi
}

# Test historical weather
test_historical_weather() {
  echo "Testing historical weather endpoint..."
  response=$(curl -s -X GET "$BASE_URL/historical-weather" -G --data-urlencode "user_id=1" --data-urlencode "date=2023-12-01")
  if echo "$response" | grep -q '"error"'; then
    echo "Historical weather test passed with error: $response"
  elif echo "$response" | grep -q '"historical_weather"'; then
    echo "Historical weather test passed: $response"
  else
    echo "Historical weather test failed: $response"
    exit 1
  fi
}

# Test air quality
test_air_quality() {
  echo "Testing air quality endpoint..."
  response=$(curl -s -X GET "$BASE_URL/air-quality" -G --data-urlencode "user_id=1")
  if echo "$response" | grep -q '"error"'; then
    echo "Air quality test passed with error: $response"
  elif echo "$response" | grep -q '"air_quality"'; then
    echo "Air quality test passed: $response"
  else
    echo "Air quality test failed: $response"
    exit 1
  fi
}

# Run smoke tests
check_health
test_current_weather
test_forecast
test_historical_weather
test_air_quality

echo "Smoke tests completed successfully!"
