from psycopg2.extras import RealDictCursor


def get_location_overview(conn):
    sql = """
        SELECT
            location_id,
            city,
            address,
            postal_code,
            latitude,
            longitude,
            weather_time,
            air_temperature,
            wind_speed,
            wildfire_time,
            severity_level_id,
            brightness,
            confidence,
            frp,
            status
        FROM ingestion.v_location_overview
        WHERE latitude IS NOT NULL
          AND longitude IS NOT NULL
        ORDER BY city
    """

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql)
        return cur.fetchall()