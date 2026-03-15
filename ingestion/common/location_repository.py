from ingestion.common.models import Location

def fetch_locations(conn) -> list[Location]:
    sql = """
        SELECT
            location_id,
            latitude,
            longitude
        FROM ingestion.location
        WHERE latitude IS NOT NULL
          AND longitude IS NOT NULL
        ORDER BY location_id
    """
    with conn.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()

    return [
        Location(
            location_id =row[0],
            latitude=float(row[1]),
            longitude=float(row[2]),
        )
        for row in rows
    ]


def find_nearest_location(conn, lat: float, lon: float) -> int | None:
    sql = """
        SELECT location_id
        FROM ingestion.location
        ORDER BY
            (latitude - %s)^2 + (longitude - %s)^2
        LIMIT 1
    """

    with conn.cursor() as cur:
        cur.execute(sql, (lat, lon))
        row = cur.fetchone()

    return row[0] if row else None
