import streamlit as st
from core.db import get_db_conn
from dashboard.components.filter_bar import render_filter_bar
from dashboard.components.sensor_overview_section import render_sensor_overview_section
from dashboard.services.overview_service import load_overview_data

def show_overview_page():
    st.title("Overview")

    conn = get_db_conn()
    filters = render_filter_bar(conn)
    data = load_overview_data(conn, filters)

    render_sensor_overview_section(data["sensor"])

    # kpis = get_overview_kpis(conn, filters)
    # alarms = get_alarm_summary(conn, filters)
    # sensor_history = get_sensor_history(conn, filters)

    # col1, col2, col3 = st.columns(3)
    # col1.metric("Active Hives", kpis["active_hives"])
    # col2.metric("Sensors", kpis["sensor_count"])
    # col3.metric("Active Alarms", kpis["active_alarms"])

    # st.subheader("Alarm Summary")
    # st.dataframe(alarms, use_container_width=True)

    # st.subheader("Sensor History")
    # st.dataframe(sensor_history, use_container_width=True)

show_overview_page()