from __future__ import annotations

from typing import Any

import requests

from ingestion.weather.models import WeatherObservation

BASE_URL = "https://opendata-download-metfcst.smhi.se/api"

def build_forecast_url(lon: float, lat: float) -> str:
    return (
        f"{BASE_URL}/category/snow1g/version/1/"
        f"geotype/point/lon/{lon}/lat/{lat}/data.json"
    )

REQUEST_TIMEOUT = 20

def get_param(parameters, name):
    for p in parameters:
        if p["name"] == name:
            return p["values"][0]
    return None


def fetch_smhi_forecast(lat: float, lon: float) -> dict[str, Any]:
    url = build_forecast_url(lon, lat)
    response = requests.get(url, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.json()

def parse_forecast(location_id: int, job_id: int, payload: dict) -> WeatherObservation:
    series = payload["timeSeries"][0]
    data = series["data"]

    return WeatherObservation(
        job_id=job_id,
        location_id=location_id,
        air_temperature=data.get("air_temperature"),
        relative_humidity=data.get("relative_humidity"),
        wind_speed=data.get("wind_speed"),
        wind_direction=data.get("wind_from_direction"),
        valid_time=series["time"],
    )


def _get_parameter_value(parameters: list[dict[str, Any]], name: str) -> float | int | None:
    for param in parameters:
        if param.get("name") == name:
            values = param.get("values", [])
            return values[0] if values else None
    return None


def _to_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _to_int(value: Any) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None