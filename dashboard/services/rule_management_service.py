from psycopg2.extras import RealDictCursor

def fetch_alarm_rules(conn):
    sql = """
        SELECT
            rule_id,
            rule_name,
            metric_type_id,
            condition_type,
            threshold,
            severity_level_id,
            is_active
        FROM ingestion.alarm_rule
        ORDER BY rule_id
    """

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql)
        return cur.fetchall()


def update_alarm_rule(conn, rule_id: int, threshold, is_active: bool):
    sql = """
        UPDATE ingestion.alarm_rule
        SET
            threshold = %s,
            is_active = %s
        WHERE rule_id = %s
    """

    with conn.cursor() as cur:
        cur.execute(sql, (threshold, is_active, rule_id))
    conn.commit()

    return {"updated": 1, "rule_id": rule_id}