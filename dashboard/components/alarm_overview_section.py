import streamlit as st
import pandas as pd


def render_alarm_overview_section(alarm_data: dict):
    st.subheader("Alarm Events")

    if alarm_data["hourly"]:
        df_hourly = pd.DataFrame(alarm_data["hourly"])
        st.bar_chart(df_hourly, x="hour", y="alarm_count")
    else:
        st.info("No alarm events found.")

    if alarm_data["latest"]:
        df_latest = pd.DataFrame(alarm_data["latest"])
        st.dataframe(df_latest, width='stretch', hide_index=True)