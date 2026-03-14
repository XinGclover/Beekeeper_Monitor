import pandas as pd
from psycopg2.extras import RealDictCursor


def get_alarm_events(conn):

    sql = """
    SELECT *
    FROM ingestion.alarm_event
    ORDER BY triggered_at DESC
    LIMIT 100
    """

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql)
        return cur.fetchall()