from psycopg2.extras import RealDictCursor

def create_notifications(conn):
    sql = """
        insert into ingestion.notification
        (user_id, event_id, title, message)
        select
          uar.user_id,
          ae.event_id,
          ar.name,
          ar.name || ' triggered'
        from ingestion.alarm_event ae
        join ingestion.alarm_rule ar
          on ae.rule_id = ar.rule_id
        join ingestion.user_alarm_rule uar
          on ae.rule_id = uar.rule_id
        left join ingestion.notification n
          on n.user_id = uar.user_id
          and n.event_id = ae.event_id
        where n.notification_id is null
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
    with conn.cursor() as cur:
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
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(sql, (notification_id,))