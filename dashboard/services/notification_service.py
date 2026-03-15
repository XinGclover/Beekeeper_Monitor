from psycopg2.extras import RealDictCursor


def get_notifications(conn):

    sql = """
    SELECT *
    FROM ingestion.notification
    ORDER BY sent_at DESC
    LIMIT 100
    """

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql)
        return cur.fetchall()