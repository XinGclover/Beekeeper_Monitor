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
        is_unread = not n["is_read"]

        emoji = "📩" if is_unread else "📬"
        title_style = "font-weight:bold;" if is_unread else "color:#9ca3af;"
        time_text = n["created_at"].strftime("%b %d, %H:%M")

        col1, col2, col3, col4 = st.columns([0.4, 6, 2, 2])

        with col1:
            st.markdown(
                f"""
                <div style="
                    font-size: 26px;
                    line-height: 1;
                    margin-top: 2px;
                    text-align: center;
                ">{emoji}</div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                f"""
                <div style="
                    color: {title_style};
                    font-size: 16px;
                    padding-top: 6px;
                    white-space: nowrap;
                    overflow: hidden;
                    text-overflow: ellipsis;
                ">
                    {n["title"]}
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col3:
            st.markdown(
                f"""
                <div style="
                    text-align: right;
                    color: #6b7280;
                    font-size: 14px;
                    padding-top: 6px;
                ">
                    {time_text}
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col4:
            if is_unread:
                if st.button("Mark read", key=f"mark_read_{n['notification_id']}"):
                    mark_notification_as_read(conn, n["notification_id"])
                    conn.commit()
                    st.rerun()
            else:
                st.markdown(
                    "<div style='color:#9ca3af; font-size:13px; padding-top:8px;'>Read</div>",
                    unsafe_allow_html=True,
                )

        st.markdown("<hr style='margin: 0.2rem 0 0.2rem 0;'>", unsafe_allow_html=True)