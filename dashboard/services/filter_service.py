from psycopg2.extras import RealDictCursor


def get_locations(conn):
    sql = """
        select distinct location_id, location_name
        from ingestion.v_filter_options
        order by location_name
    """
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql)
        return cur.fetchall()


def get_apiaries(conn, location_id=None):
    sql = """
        select distinct apiary_id, apiary_name
        from ingestion.v_filter_options
        where 1=1
    """
    params = []

    if location_id:
        sql += " and location_id = %s"
        params.append(location_id)

    sql += " order by apiary_name"

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql, params)
        return cur.fetchall()


def get_hives(conn, location_id=None, apiary_id=None):
    sql = """
        select distinct hive_id, hive_name
        from ingestion.v_filter_options
        where 1=1
    """
    params = []

    if location_id:
        sql += " and location_id = %s"
        params.append(location_id)

    if apiary_id:
        sql += " and apiary_id = %s"
        params.append(apiary_id)

    sql += " order by hive_name"

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql, params)
        return cur.fetchall()


def get_sensors(conn, location_id=None, apiary_id=None, hive_id=None):
    sql = """
        select distinct sensor_id, sensor_name
        from ingestion.v_filter_options
        where 1=1
    """
    params = []

    if location_id:
        sql += " and location_id = %s"
        params.append(location_id)

    if apiary_id:
        sql += " and apiary_id = %s"
        params.append(apiary_id)

    if hive_id:
        sql += " and hive_id = %s"
        params.append(hive_id)

    sql += " order by sensor_name"

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql, params)
        return cur.fetchall()
    
