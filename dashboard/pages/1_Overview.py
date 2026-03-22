import streamlit as st
from core.db import get_db_conn
from dashboard.services.overview_service import load_overview_data
from dashboard.components.filter_bar import render_filter_bar
from dashboard.components.sensor_overview_section import render_sensor_overview_section
from dashboard.components.overview_kpis import render_kpi_row
from dashboard.components.weather_overview_section import render_weather_overview_section
from dashboard.components.wildfire_overview_section import render_wildfire_overview_section
from dashboard.components.alarm_overview_section import render_alarm_overview_section
from dashboard.components.notification_overview_section import render_notification_overview_section
from dashboard.components.ui_styles import inject_sticky_topbar_css

def show_overview_page():
    st.title("Overview")
    inject_sticky_topbar_css()

    conn = get_db_conn()
    filters = render_filter_bar(conn)
    data = load_overview_data(conn, filters)

    render_kpi_row(data["kpis"])
    render_sensor_overview_section(data["sensor"])

    render_weather_overview_section(data["weather"])
    render_wildfire_overview_section(data["wildfire"])
    render_alarm_overview_section(data["alarms"])
    render_notification_overview_section(data["notifications"])
   

show_overview_page()