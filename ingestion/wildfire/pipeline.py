from __future__ import annotations

import logging

from ingestion.common.jobs import create_scraping_job, update_scraping_job_status
from ingestion.common.location_repository import fetch_locations
from ingestion.wildfire.client import fetch_wildfire_observations
from ingestion.wildfire.models import WildfireObservation
from ingestion.wildfire.repository import insert_wildfire_data
from core.db import get_db_conn
import os

FIRMS_API_KEY = os.getenv("FIRMS_API_KEY")

SWEDEN_BBOX = "10,55,25,70"


def setup_logger() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )


def run_wildfire_pipeline() -> None:
    setup_logger()
    logging.info("Starting wildfire pipeline")

    conn = None
    job_id = None

    try:
        conn = get_db_conn()
        job_id = create_scraping_job(conn, source_id=2)

        locations = fetch_locations(conn)
        logging.info("Loaded %s locations", len(locations))

        raw_observations = fetch_wildfire_observations(
            api_key=FIRMS_API_KEY,
            area=SWEDEN_BBOX,
            job_id=job_id,
            days=1,
        )
        logging.info("Fetched %s wildfire observations", len(raw_observations))

        observations = []

        for obs in raw_observations:
            try:
                location_id = _find_nearest_location_id(
                    obs.latitude,
                    obs.longitude,
                    locations,
                )

                severity_level_id = _map_severity_level(obs.confidence, obs.frp)

                enriched_obs = WildfireObservation(
                    job_id=obs.job_id,
                    location_id=location_id,
                    latitude=obs.latitude,
                    longitude=obs.longitude,
                    brightness=obs.brightness,
                    confidence=obs.confidence,
                    frp=obs.frp,
                    satellite=obs.satellite,
                    instrument=obs.instrument,
                    daynight=obs.daynight,
                    severity_level_id=severity_level_id,
                    status="detected",
                    detected_at=obs.detected_at,
                )

                observations.append(enriched_obs)

            except Exception as e:
                logging.exception(
                    "Failed to process wildfire observation lat=%s lon=%s: %s",
                    obs.latitude,
                    obs.longitude,
                    e,
                )

        insert_wildfire_data(conn, observations)
        update_scraping_job_status(conn, job_id, "success")
        conn.commit()

    except Exception:
        if conn is not None:
            conn.rollback()

        if conn is not None and job_id is not None:
            update_scraping_job_status(conn, job_id, "failed")
            conn.commit()

        raise

    finally:
        if conn is not None:
            conn.close()


def _find_nearest_location_id(lat: float, lon: float, locations: list) -> int | None:
    nearest_location_id = None
    nearest_distance = None

    for loc in locations:
        distance = (loc.latitude - lat) ** 2 + (loc.longitude - lon) ** 2

        if nearest_distance is None or distance < nearest_distance:
            nearest_distance = distance
            nearest_location_id = loc.location_id

    return nearest_location_id


def _map_severity_level(confidence: str | None, frp: float | None) -> int | None:
    if confidence == "h":
        return 3
    if confidence == "n":
        return 2
    if confidence == "l":
        return 1

    if frp is not None:
        if frp >= 10:
            return 3
        if frp >= 5:
            return 2
        return 1

    return None


if __name__ == "__main__":
    run_wildfire_pipeline()