from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class WildfireObservation:
    job_id: int
    latitude: float | None
    longitude: float | None
    detected_at: datetime
    location_id: int | None = None
    brightness: float | None = None
    confidence: str | None = None
    frp: float | None = None
    satellite: str | None = None
    instrument: str | None = None
    daynight: str | None = None
    severity_level_id: int | None = None
    status: str | None = None