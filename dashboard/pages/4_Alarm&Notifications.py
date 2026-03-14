import streamlit as st
import pandas as pd

from dashboard.services.notification_service import get_notifications
from dashboard.services.alarm_event_service import get_alarm_events,get_alarm_events_hourly 
from db import get_db_conn


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
    notification_data = get_notifications(conn)
    df_notification = pd.DataFrame(notification_data)
    st.dataframe(df_notification)