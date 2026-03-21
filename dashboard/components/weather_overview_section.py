import streamlit as st
import pandas as pd


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

    metric_cols = st.columns(3)

    with metric_cols[0]:
        st.metric("🌡 Temp", f"{latest['air_temperature']:.1f} °C")

    with metric_cols[1]:
        st.metric("💧 Humidity", f"{latest['relative_humidity']:.0f} %")

    with metric_cols[2]:
        st.metric("🌬 Wind", f"{latest['wind_speed']:.1f} m/s")

    chart_df = df.set_index("valid_time")[
        ["air_temperature", "relative_humidity", "wind_speed"]
    ]

    st.line_chart(chart_df, use_container_width=True)