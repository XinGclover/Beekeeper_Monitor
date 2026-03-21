import streamlit as st
import pandas as pd


def render_weather_overview_section(weather_data: dict):
    st.subheader("Weather Data")

    metric_cols = st.columns(3)

    with metric_cols[0]:
        st.metric("Temperature", weather_data["summary"]["temperature"])

    with metric_cols[1]:
        st.metric("Humidity", weather_data["summary"]["humidity"])

    with metric_cols[2]:
        st.metric("Wind Speed", weather_data["summary"]["wind_speed"])

    if weather_data["timeseries"]:
        df_chart = pd.DataFrame(weather_data["timeseries"])
        st.line_chart(
            df_chart,
            x="recorded_at",
            y=["temperature", "humidity", "wind_speed"],
        )
    else:
        st.info("No weather data found.")