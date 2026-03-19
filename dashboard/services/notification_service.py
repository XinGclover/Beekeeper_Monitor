from psycopg2.extras import RealDictCursor


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