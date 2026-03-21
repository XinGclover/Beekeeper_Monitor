from psycopg2.extras import RealDictCursor
from dashboard.utils.filter_utils import Filters, build_filter_conditions, get_time_from


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
    

# overview page
def get_sensor_data_timeline_overview(conn, filters: Filters | None = None):
    where_sql, params = build_filter_conditions(filters, time_column="measured_at")

    sql = f"""
        select *
        from ingestion.v_sensor_data_timeline
        {where_sql}
        order by measured_at desc
        limit 500
    """

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql, params)
        return cur.fetchall()
    
def get_latest_sensor_data_overview(conn, filters: Filters | None = None):
    where_sql, params = build_filter_conditions(filters, time_column="measured_at")

    where_sql = where_sql or ""

    sql = f"""
        select *
        from ingestion.v_sensor_latest
        {where_sql}
        order by measured_at desc
        limit 20
    """

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql, params)
        return cur.fetchall()