from psycopg2.extras import RealDictCursor


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