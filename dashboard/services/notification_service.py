from psycopg2.extras import RealDictCursor
from dashboard.utils.filter_utils import Filters, build_filter_conditions


def get_notifications(conn):

    sql = """
    SELECT *
    FROM ingestion.notification
    ORDER BY created_at DESC
    LIMIT 100
    """

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql)
        return cur.fetchall()
    

def get_all_users(conn):
    sql = """
    SELECT *
    FROM ingestion.user
    """

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql)
        return cur.fetchall()
    


# Overview page
def get_notifications_latest(conn, filters: Filters | None = None):
    where_sql, params = build_filter_conditions(filters, time_column="created_at")

    sql = f"""
        select *
        from ingestion.v_notification_latest
        {where_sql}
        order by created_at desc
        limit 10
    """

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql, params)
        return cur.fetchall()


def get_unread_notification_count(conn, filters: Filters | None = None):
    where_sql, params = build_filter_conditions(filters, time_column="created_at")

    if where_sql:
        where_sql += " and is_read = false"
    else:
        where_sql = " where is_read = false"

    sql = f"""
        select count(*) as unread_count
        from ingestion.v_notification_latest
        {where_sql}
    """

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql, params)
        row = cur.fetchone()
        return row["unread_count"] if row else 0