from psycopg2.extras import RealDictCursor


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