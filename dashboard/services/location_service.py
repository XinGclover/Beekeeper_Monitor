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


def get_filter_options(conn, location_id=None, apiary_id=None, hive_id=None):
    """
    Get hierarchical filter options for location, apiary, hive, and sensor.
    
    Returns all available options based on the provided filters.
    """
    result = {
        "locations": [],
        "apiaries": [],
        "hives": [],
        "sensors": [],
    }
    
    # Get locations
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT DISTINCT location_id, location_name
            FROM ingestion.v_filter_options
            ORDER BY location_name
        """)
        result["locations"] = cur.fetchall()
    
    # Get apiaries
    apiary_sql = """
        SELECT DISTINCT apiary_id, apiary_name
        FROM ingestion.v_filter_options
        WHERE 1=1
    """
    apiary_params = []
    if location_id is not None:
        apiary_sql += " AND location_id = %s"
        apiary_params.append(location_id)
    apiary_sql += " ORDER BY apiary_name"
    
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(apiary_sql, apiary_params)
        result["apiaries"] = cur.fetchall()
    
    # Get hives
    hive_sql = """
        SELECT DISTINCT hive_id, hive_name
        FROM ingestion.v_filter_options
        WHERE 1=1
    """
    hive_params = []
    if location_id is not None:
        hive_sql += " AND location_id = %s"
        hive_params.append(location_id)
    if apiary_id is not None:
        hive_sql += " AND apiary_id = %s"
        hive_params.append(apiary_id)
    hive_sql += " ORDER BY hive_name"
    
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(hive_sql, hive_params)
        result["hives"] = cur.fetchall()
    
    # Get sensors
    sensor_sql = """
        SELECT DISTINCT sensor_id, sensor_name
        FROM ingestion.v_filter_options
        WHERE 1=1
    """
    sensor_params = []
    if location_id is not None:
        sensor_sql += " AND location_id = %s"
        sensor_params.append(location_id)
    if apiary_id is not None:
        sensor_sql += " AND apiary_id = %s"
        sensor_params.append(apiary_id)
    if hive_id is not None:
        sensor_sql += " AND hive_id = %s"
        sensor_params.append(hive_id)
    sensor_sql += " ORDER BY sensor_name"
    
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sensor_sql, sensor_params)
        result["sensors"] = cur.fetchall()
    
    return result