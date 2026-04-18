import pandas as pd
from psycopg2.extras import RealDictCursor
from dashboard.utils.filter_utils import Filters, build_filter_conditions


def get_alarm_events(conn, limit=100, offset=0):
    sql = """
        SELECT *
        FROM ingestion.alarm_event
        ORDER BY triggered_at DESC
        LIMIT %s OFFSET %s
    """

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql, (limit, offset))
        return cur.fetchall()
    

def get_alarm_events_hourly(conn, limit=100):
    sql = """
        SELECT *
        FROM ingestion.v_alarm_event_hourly
        ORDER BY hour DESC
        LIMIT %s
    """

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql, (limit,))
        return cur.fetchall()
    
# overview page

def get_alarm_events_latest(conn, filters: Filters | None = None):
    where_sql, params = build_filter_conditions(filters, time_column="triggered_at")

    sql = f"""
        select *
        from ingestion.v_alarm_event_latest
        {where_sql}
        order by triggered_at desc
        limit 20
    """

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql, params)
        return cur.fetchall()
    
    
def get_alarm_events_hourly_overview(conn, filters: Filters | None = None):
    where_sql, params = build_filter_conditions(filters, time_column="hour")

    sql = f"""
        select *
        from ingestion.v_alarm_event_hourly_overview
        {where_sql}
        order by hour asc
    """

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql, params)
        return cur.fetchall()