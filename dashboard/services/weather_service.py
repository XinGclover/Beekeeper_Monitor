from psycopg2.extras import RealDictCursor
from dashboard.utils.filter_utils import Filters, build_location_time_filter


def get_weather_data(conn):

    sql = """
    SELECT *
    FROM ingestion.weather_data
    ORDER BY valid_time DESC
    LIMIT 100
    """

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql)
        return cur.fetchall()
    

# Overview page
def get_weather_timeline(conn, filters=None):
    where_sql, params = build_location_time_filter(filters, time_column="fetched_at")

    sql = f"""
        select *
        from ingestion.v_weather_timeline
        {where_sql}
        order by fetched_at desc
        limit 500
    """

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql, params)
        return cur.fetchall()