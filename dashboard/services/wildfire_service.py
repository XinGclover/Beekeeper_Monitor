from psycopg2.extras import RealDictCursor

from dashboard.utils.filter_utils import build_location_time_filter, Filters


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
    

# Overview page
def get_wildfire_map_points(conn, filters: Filters | None = None):
    where_sql, params = build_location_time_filter(filters, time_column="detected_at")

    sql = f"""
        select *
        from ingestion.v_wildfire_events
        {where_sql}
        order by detected_at desc
        limit 100
    """

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql, params)
        return cur.fetchall()


def get_latest_wildfire_events(conn, filters: Filters | None = None):
    where_sql, params = build_location_time_filter(filters, time_column="detected_at")

    sql = f"""
        select *
        from ingestion.v_wildfire_events
        {where_sql}
        order by detected_at desc
        limit 10
    """

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql, params)
        return cur.fetchall()