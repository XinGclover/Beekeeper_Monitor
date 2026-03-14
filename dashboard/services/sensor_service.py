from psycopg2.extras import RealDictCursor


def get_latest_sensor_data(conn):
    sql = """
        select *
        from ingestion.v_sensor_latest
        order by sensor_id
    """

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql)
        return cur.fetchall()


def get_sensor_history(conn, sensor_id=None):
    sql = """
        select *
        from ingestion.v_sensor_history
    """

    params = []

    if sensor_id:
        sql += " where sensor_id = %s"
        params.append(sensor_id)

    sql += " order by period_date desc"

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql, params)
        return cur.fetchall()
    

def get_sensor_data_timeline(conn, sensor_id=None):
    sql = """
        select *
        from ingestion.v_sensor_data_timeline
        where (%s is null or sensor_id = %s)
        order by measured_at desc
        limit 500
    """

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql, (sensor_id, sensor_id))
        return cur.fetchall()