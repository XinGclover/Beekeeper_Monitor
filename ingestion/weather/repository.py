from __future__ import annotations

from psycopg2.extras import execute_batch

from ingestion.weather.models import WeatherLocation, WeatherObservation


def fetch_locations(conn) -> list[WeatherLocation]:
    sql = """
        SELECT
            location_id,
            latitude,
            longitude
        FROM ingestion.location
        WHERE latitude IS NOT NULL
          AND longitude IS NOT NULL
        ORDER BY location_id
    """
    with conn.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()

    return [
        WeatherLocation(
            location_id =row[0],
            latitude=float(row[1]),
            longitude=float(row[2]),
        )
        for row in rows
    ]


def insert_weather_data(conn, observations):
    sql = """
        INSERT INTO ingestion.weather_data (
            job_id,
            location_id,
            air_temperature,
            relative_humidity,
            wind_speed,
            wind_direction,
            valid_time
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (location_id, valid_time)
        DO UPDATE SET
            job_id = EXCLUDED.job_id,
            air_temperature = EXCLUDED.air_temperature,
            relative_humidity = EXCLUDED.relative_humidity,
            wind_speed = EXCLUDED.wind_speed,
            wind_direction = EXCLUDED.wind_direction,
            fetched_at = current_timestamp
    """

    with conn.cursor() as cur:
        for obs in observations:
            cur.execute(
                sql,
                (
                    obs.job_id,
                    obs.location_id,
                    obs.air_temperature,
                    obs.relative_humidity,
                    obs.wind_speed,
                    obs.wind_direction,
                    obs.valid_time,
                ),
            )


def create_scraping_job(conn, source_id: int) -> int:
    sql = """
        INSERT INTO ingestion.scraping_job (source_id, status)
        VALUES (%s, 'running')
        RETURNING job_id
    """

    with conn.cursor() as cur:
        cur.execute(sql, (source_id,))
        job_id = cur.fetchone()[0]

    return job_id

def update_scraping_job_status(conn, job_id: int, status: str):
    sql = """
        UPDATE ingestion.scraping_job
        SET status = %s
        WHERE job_id = %s
    """

    with conn.cursor() as cur:
        cur.execute(sql, (status, job_id))
