import streamlit as st


def render_overview_kpis(kpis: dict):
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Avg Temperature", kpis["avg_temperature"])

    with col2:
        st.metric("Avg Humidity", kpis["avg_humidity"])

    with col3:
        st.metric("Active Alarms", kpis["active_alarms"])

    with col4:
        st.metric("Wildfire Risk", kpis["wildfire_risk"])

    with col5:
        st.metric("Notifications", kpis["notifications"])