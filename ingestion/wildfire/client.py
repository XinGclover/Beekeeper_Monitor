from __future__ import annotations

import csv
import io
from datetime import datetime
from typing import Any

import requests

from ingestion.wildfire.models import WildfireObservation

FIRMS_AREA_CSV_URL = (
    "https://firms.modaps.eosdis.nasa.gov/api/area/csv/"
    "{api_key}/{dataset}/{area}/{days}"
)

REQUEST_TIMEOUT = 20
DEFAULT_DATASET = "VIIRS_SNPP_NRT"


def fetch_firms_csv(
    api_key: str,
    area: str,
    days: int = 1,
    dataset: str = DEFAULT_DATASET,
) -> str:
    url = FIRMS_AREA_CSV_URL.format(
        api_key=api_key,
        dataset=dataset,
        area=area,
        days=days,
    )
    response = requests.get(url, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.text


def parse_firms_csv(csv_text: str, job_id: int) -> list[WildfireObservation]:
    reader = csv.DictReader(io.StringIO(csv_text))
    observations: list[WildfireObservation] = []

    for row in reader:
        observations.append(parse_firms_row(row=row, job_id=job_id))

    return observations


def parse_firms_row(row: dict[str, Any], job_id: int) -> WildfireObservation:
    detected_at = _parse_detected_at(
        acq_date=row["acq_date"],
        acq_time=row["acq_time"],
    )

    return WildfireObservation(
        job_id=job_id,
        latitude=_to_float(row.get("latitude")),
        longitude=_to_float(row.get("longitude")),
        brightness=_to_float(row.get("bright_ti4")),
        confidence=_to_str(row.get("confidence")),
        frp=_to_float(row.get("frp")),
        satellite=_to_str(row.get("satellite")),
        instrument=_to_str(row.get("instrument")),
        daynight=_to_str(row.get("daynight")),
        detected_at=detected_at,
    )


def fetch_wildfire_observations(
    api_key: str,
    area: str,
    job_id: int,
    days: int = 1,
    dataset: str = DEFAULT_DATASET,
) -> list[WildfireObservation]:
    csv_text = fetch_firms_csv(
        api_key=api_key,
        area=area,
        days=days,
        dataset=dataset,
    )
    return parse_firms_csv(csv_text=csv_text, job_id=job_id)


def _parse_detected_at(acq_date: str, acq_time: str) -> datetime:
    return datetime.strptime(
        f"{acq_date} {acq_time.zfill(4)}",
        "%Y-%m-%d %H%M",
    )


def _to_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _to_str(value: Any) -> str | None:
    if value is None:
        return None

    text = str(value).strip()
    return text if text else None