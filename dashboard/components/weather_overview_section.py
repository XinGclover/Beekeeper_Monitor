import streamlit as st
import pandas as pd
from dashboard.components.ui_styles import inject_kpi_card_css
from dashboard.components.kpi_component import render_kpi_card
import plotly.express as px



def render_weather_overview_section(weather_data: dict):
    st.subheader("Weather Data")

    data = weather_data["timeseries"]

    if not data:
        st.info("No weather data found.")
        return

    df = pd.DataFrame(data)

    df["valid_time"] = pd.to_datetime(df["valid_time"])
    df["air_temperature"] = pd.to_numeric(df["air_temperature"], errors="coerce")
    df["relative_humidity"] = pd.to_numeric(df["relative_humidity"], errors="coerce")
    df["wind_speed"] = pd.to_numeric(df["wind_speed"], errors="coerce")

    df = df.sort_values("valid_time")

    latest = df.iloc[-1]

    inject_kpi_card_css()
    metric_cols = st.columns(5)

    with metric_cols[0]:
        render_kpi_card(
            "Temperature",
            f"{latest['air_temperature']:.1f} °C",
            "",
            "🌡"
        )

    with metric_cols[1]:
        render_kpi_card(
            "Humidity",
            f"{latest['relative_humidity']:.0f} %",
            "",
            "💧"
        )

    with metric_cols[2]:
        render_kpi_card(
            "Wind",
            f"{latest['wind_speed']:.1f} m/s",
            "",
            "🌬"
        )
    
    st.caption("&nbsp;")

    fig = px.scatter(
        df,
        x="valid_time",
        y=["air_temperature", "relative_humidity", "wind_speed"],
    )

    # lägg till linje också (utan spline!)
    fig.update_traces(mode="lines+markers")

    st.plotly_chart(fig, use_container_width=True)