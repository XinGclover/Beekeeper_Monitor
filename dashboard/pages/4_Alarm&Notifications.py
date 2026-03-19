import streamlit as st
import pandas as pd

from dashboard.services.notification_service import get_notifications, get_all_users
from dashboard.services.alarm_event_service import get_alarm_events,get_alarm_events_hourly 
from core.db import get_db_conn

from notification.repository import (
    get_notifications_for_user,
    get_unread_notifications_for_user,
    mark_notification_as_read,
)

st.title("Alarm Events & Notifications")

conn = get_db_conn()

tab1, tab2 = st.tabs(["Alarm Events", "Notifications"])

with tab1:
    st.subheader("Latest alarm events")
    alarm_data = get_alarm_events(conn)
    df_alarm = pd.DataFrame(alarm_data)
    st.dataframe(df_alarm)

    st.subheader("Hourly Alarm Events")
    alarm_hourly_data = get_alarm_events_hourly(conn)
    df_alarm_hourly = pd.DataFrame(alarm_hourly_data)
    st.line_chart(
    df_alarm_hourly,
    x="hour",
    y="alarm_count"
)

with tab2:
    st.subheader("Latest notifications")
    users = get_all_users(conn)

    if not users:
        st.info("No users found.")

    user_options = {f"{u['user_id']} - {u['username']}": u["user_id"] for u in users}
    selected_label = st.selectbox("Select user", list(user_options.keys()))
    selected_user_id = user_options[selected_label]

    unread_notifications = get_unread_notifications_for_user(conn, selected_user_id)
    all_notifications = get_notifications_for_user(conn, selected_user_id)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Unread notifications", len(unread_notifications))
    with col2:
        st.metric("Total notifications", len(all_notifications))

    st.markdown("### Latest notifications")

    if not all_notifications:
        st.info("This user has no notifications.")

    for n in all_notifications:
        with st.container(border=True):
            col1, col2 = st.columns([6, 2])

            with col1:
                st.markdown(f"**{n['notification_id']}**")
                st.markdown(f"**{n['title']}**")
                st.write(n["message"])
                st.caption(f"Created at: {n['created_at']}")
                st.caption(f"Read: {'Yes' if n['is_read'] else 'No'}")

            with col2:
                if not n["is_read"]:
                    if st.button(
                        "Mark as read",
                        key=f"mark_read_{n['notification_id']}"
                    ):
                        mark_notification_as_read(conn, n["notification_id"])
                        conn.commit()
                        st.rerun()
                else:
                    st.success("Read")