from __future__ import annotations


def insert_wildfire_data(conn, observations) -> None:
    sql = """
        INSERT INTO ingestion.wildfire_data (
            job_id,
            location_id,
            latitude,
            longitude,
            brightness,
            confidence,
            frp,
            satellite,
            instrument,
            daynight,
            severity_level_id,
            status,
            detected_at
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (latitude, longitude, detected_at)
        DO UPDATE SET
            job_id = EXCLUDED.job_id,
            location_id = EXCLUDED.location_id,
            brightness = EXCLUDED.brightness,
            confidence = EXCLUDED.confidence,
            frp = EXCLUDED.frp,
            satellite = EXCLUDED.satellite,
            instrument = EXCLUDED.instrument,
            daynight = EXCLUDED.daynight,
            severity_level_id = EXCLUDED.severity_level_id,
            status = EXCLUDED.status,
            fetched_at = current_timestamp
    """

    with conn.cursor() as cur:
        for obs in observations:
            cur.execute(
                sql,
                (
                    obs.job_id,
                    obs.location_id,
                    obs.latitude,
                    obs.longitude,
                    obs.brightness,
                    obs.confidence,
                    obs.frp,
                    obs.satellite,
                    obs.instrument,
                    obs.daynight,
                    obs.severity_level_id,
                    obs.status,
                    obs.detected_at,
                ),
            )