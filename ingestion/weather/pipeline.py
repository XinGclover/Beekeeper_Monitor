from __future__ import annotations

import logging

from ingestion.weather.client import fetch_smhi_forecast, parse_forecast
from ingestion.common.location_repository import fetch_locations
from ingestion.common.jobs import create_scraping_job ,update_scraping_job_status
from ingestion.weather.repository import insert_weather_data
from app.db import get_db_conn



def setup_logger() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )


def run_weather_pipeline() -> None:
    setup_logger()
    logging.info("Starting weather pipeline")

    conn = None
    job_id = None
    try:
        conn = get_db_conn()
        job_id = create_scraping_job(conn, source_id=1)
        locations = fetch_locations(conn)
        logging.info("Loaded %s locations", len(locations))

        observations = []

        for loc in locations:
            try:
                payload = fetch_smhi_forecast(loc.latitude, loc.longitude)

                obs = parse_forecast(loc.location_id, job_id, payload)

                observations.append(obs)

                logging.info(
                    "Fetched weather for location_id=%s",
                    loc.location_id
                )
            except Exception as e:
                logging.exception(
                    "Failed for location_id=%s: %s",
                    loc.location_id,
                    e,
                )

        insert_weather_data(conn, observations)
        update_scraping_job_status(conn, job_id, "success")
        conn.commit()


    except Exception as e:

        if conn is not None:
            conn.close()

        update_scraping_job_status(conn, job_id, "failed")

        conn.commit()

        raise

    if conn is not None:
        conn.close()

if __name__ == "__main__":
    run_weather_pipeline()