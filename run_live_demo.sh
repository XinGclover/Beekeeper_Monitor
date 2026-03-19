#!/bin/bash

set -e

echo "Starting live demo..."

cleanup() {
  echo ""
  echo "Stopping services..."

  kill $SIM_PID 2>/dev/null || true
  kill $WEATHER_PID 2>/dev/null || true
  kill $WILDFIRE_PID 2>/dev/null || true
  kill $RULE_PID 2>/dev/null || true

  echo "Stopped."
  exit 0
}

trap cleanup INT TERM

run_loop() {
  local name=$1
  local interval=$2
  shift 2

  while true; do
    echo "[$name] Running..."
    "$@" || echo "[$name] Failed"
    sleep "$interval"
  done
}

echo "Starting sensor simulator..."
uv run python -m ingestion.sensors.hive_sensor_simulator --interval 120 &
SIM_PID=$!

echo "Starting weather pipeline loop..."
run_loop "weather" 600 uv run python -m ingestion.weather.pipeline &
WEATHER_PID=$!

echo "Starting wildfire pipeline loop..."
run_loop "wildfire" 1200 uv run python -m ingestion.wildfire.pipeline &
WILDFIRE_PID=$!

echo "Starting rule engine..."
uv run python -m core.main &
RULE_PID=$!

sleep 5

echo "Starting Streamlit dashboard..."
uv run streamlit run dashboard/app.py

cleanup