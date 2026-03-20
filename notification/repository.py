from psycopg2.extras import RealDictCursor

def create_notifications(conn):
    sql = """
        INSERT INTO ingestion.notification
        (user_id, event_id, title, message)
        SELECT
          uar.user_id,
          ae.event_id,
          ar.rule_name AS title,
          CASE
            WHEN ae.sensor_data_id IS NOT NULL THEN
              'Sensor alert'
              || ' | rule: ' || ar.rule_name
              || ' | observed: ' || COALESCE(ae.observed_value::text, 'n/a')
              || ' | threshold: ' || COALESCE(ae.threshold_value::text, 'n/a')

            WHEN ae.weather_id IS NOT NULL THEN
              'Weather alert'
              || ' | rule: ' || ar.rule_name
              || ' | observed: ' || COALESCE(ae.observed_value::text, 'n/a')
              || ' | threshold: ' || COALESCE(ae.threshold_value::text, 'n/a')

            WHEN ae.wildfire_id IS NOT NULL THEN
              'Wildfire alert'
              || ' | rule: ' || ar.rule_name
              || ' | observed: ' || COALESCE(ae.observed_value::text, 'n/a')
              || ' | threshold: ' || COALESCE(ae.threshold_value::text, 'n/a')

            ELSE
              ar.rule_name || ' triggered'
          END AS message
        FROM ingestion.alarm_event ae
        JOIN ingestion.alarm_rule ar
          ON ae.rule_id = ar.rule_id
        JOIN ingestion.user_alarm_rule uar
          ON ae.rule_id = uar.rule_id
        LEFT JOIN ingestion.notification n
          ON n.user_id = uar.user_id
          AND n.event_id = ae.event_id
        WHERE n.notification_id IS NULL
    """

    with conn.cursor() as cur:
        cur.execute(sql)
        return cur.rowcount


def get_notifications_for_user(conn, user_id: int):
    sql = """
        select
          n.notification_id,
          n.title,
          n.message,
          n.created_at,
          n.is_read
        from ingestion.notification n
        where n.user_id = %s
        order by n.created_at desc
    """
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql, (user_id,))
        return cur.fetchall()

def get_unread_notifications_for_user(conn, user_id: int):
    sql = """
        select
          n.notification_id,
          n.title,
          n.message,
          n.created_at,
          n.is_read
        from ingestion.notification n
        where n.user_id = %s
          and n.is_read = false
        order by n.created_at desc
    """
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql, (user_id,))
        return cur.fetchall()

def mark_notification_as_read(conn, notification_id: int):
    sql = """
        update ingestion.notification
        set
          is_read = true,
          read_at = current_timestamp
        where notification_id = %s
    """
    with conn.cursor() as cur:
        cur.execute(sql, (notification_id,))
        return cur.rowcount