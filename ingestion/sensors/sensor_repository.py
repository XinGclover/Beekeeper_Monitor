from __future__ import annotations
import datetime

def fetch_sensors(conn, hive_id: int | None = None) -> list[dict]:
    sql = """
        SELECT
            s.sensor_id,
            s.hive_id,
            st.sensor_type_name
        FROM ingestion.sensor s
        JOIN ingestion.sensor_type st
            ON s.sensor_type_id = st.sensor_type_id
        WHERE (%s IS NULL OR s.hive_id = %s)
        ORDER BY s.sensor_id
    """
    with conn.cursor() as cur:
        cur.execute(sql, (hive_id, hive_id))
        rows = cur.fetchall()

    sensors = []
    for row in rows:
        sensors.append(
            {
                "sensor_id": row[0],
                "hive_id": row[1],
                "sensor_type_name": row[2],
            }
        )
    return sensors


def insert_sensor_data(
    conn,
    job_id: int,
    sensor_id: int,
    measurement: float,
    measured_at: datetime,
) -> None:
    sql = """
        INSERT INTO ingestion.sensor_data (
            job_id,
            sensor_id,
            measurement,
            measured_at
        )
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (sensor_id, measured_at) DO NOTHING
    """
    with conn.cursor() as cur:
        cur.execute(sql, (job_id, sensor_id, measurement, measured_at))