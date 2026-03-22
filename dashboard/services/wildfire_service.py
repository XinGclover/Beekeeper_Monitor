from psycopg2.extras import RealDictCursor

from dashboard.utils.filter_utils import build_filter_conditions, Filters


def get_wildfire_data(conn):

    sql = """
    SELECT *
    FROM ingestion.wildfire_data
    ORDER BY detected_at DESC
    LIMIT 100
    """

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql)
        return cur.fetchall()
    

def get_wildfire_map_points(conn, filters: Filters | None = None):
    where_sql, params = build_filter_conditions(filters, time_column="detected_at")

    sql = f"""
        select
            w.wildfire_id,
            w.location_id,
            l.city,
            l.latitude,
            l.longitude,
            w.brightness,
            w.frp,
            w.detected_at,
            s.severity_level_id,
            s.severity_name
        from ingestion.wildfire_data w
        join ingestion.location l
            on w.location_id = l.location_id
        join ingestion.severity_level s
            on w.severity_level_id = s.severity_level_id
        {where_sql}
        order by w.detected_at desc
        limit 100
    """

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql, params)
        return cur.fetchall()


def get_latest_wildfire_events(conn, filters: Filters | None = None):
    where_sql, params = build_filter_conditions(filters, time_column="detected_at")

    sql = f"""
        select
            w.wildfire_id,
            w.location_id,
            l.city,
            w.brightness,
            w.frp,
            w.detected_at,
            s.severity_level_id,
            s.severity_name
        from ingestion.wildfire_data w
        join ingestion.location l
            on w.location_id = l.location_id
        join ingestion.severity_level s
            on w.severity_level_id = s.severity_level_id
        {where_sql}
        order by w.detected_at desc
        limit 10
    """

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql, params)
        return cur.fetchall()