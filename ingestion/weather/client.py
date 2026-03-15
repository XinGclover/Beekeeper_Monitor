from __future__ import annotations

from typing import Any

import requests

from ingestion.weather.models import WeatherObservation

SMHI_FORECAST_URL = (
    "https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/"
    "geotype/point/lon/{lon}/lat/{lat}/data.json"
)

REQUEST_TIMEOUT = 20

def get_param(parameters, name):
    for p in parameters:
        if p["name"] == name:
            return p["values"][0]
    return None


def fetch_smhi_forecast(lat: float, lon: float) -> dict[str, Any]:
    url = SMHI_FORECAST_URL.format(lat=lat, lon=lon)
    response = requests.get(url, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.json()

def parse_forecast(location_id: int, job_id: int, payload: dict) -> WeatherObservation:
    series = payload["timeSeries"][0]
    parameters = series["parameters"]
    valid_time = series["validTime"]

    return WeatherObservation(
        job_id=job_id,
        location_id=location_id,
        air_temperature=get_param(parameters, "t"),
        relative_humidity=get_param(parameters, "r"),
        wind_speed=get_param(parameters, "ws"),
        wind_direction=get_param(parameters, "wd"),
        valid_time=valid_time,
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