from notification.repository import create_notifications


def process_notifications(conn):
  
    # 1 skapa notification records
    create_notifications(conn)

    # 2 markera event som notifierade
    #mark_events_notified(conn)

    # 3 skicka email / push
    #send_pending_notifications(conn)