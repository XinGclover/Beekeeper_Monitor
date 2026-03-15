#!/bin/bash

set -e

echo "Starting live demo..."

cleanup() {
  echo ""
  echo "Stopping services..."

  kill $SIM_PID 2>/dev/null || true
  kill $RULE_PID 2>/dev/null || true

  echo "Stopped."
  exit 0
}

trap cleanup INT TERM

echo "Starting sensor simulator..."
uv run python -m ingestion.sensors.hive_sensor_simulator &
SIM_PID=$!

echo "Starting rule engine..."
uv run python -m app.main &
RULE_PID=$!

sleep 5

echo "Starting Streamlit dashboard..."
uv run streamlit run dashboard/app.py

cleanup