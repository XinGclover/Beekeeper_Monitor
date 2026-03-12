from __future__ import annotations

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

