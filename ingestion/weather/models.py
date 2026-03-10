from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class WeatherLocation:
    location_id: int
    latitude: float
    longitude: float


@dataclass
class WeatherObservation:
    job_id: int
    location_id: int
    air_temperature: float | None
    relative_humidity: float | None
    wind_speed: float | None
    wind_direction: float | None
    valid_time: str