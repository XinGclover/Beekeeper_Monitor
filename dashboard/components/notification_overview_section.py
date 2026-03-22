import streamlit as st
import pandas as pd


def render_notification_overview_section(notification_data: dict):
    st.subheader("Notifications")

    st.metric("Unread", notification_data["unread_count"])

    if notification_data["latest"]:
        df = pd.DataFrame(notification_data["latest"])
        st.dataframe(df, width='stretch', hide_index=True)
    else:
        st.info("No notifications found.")