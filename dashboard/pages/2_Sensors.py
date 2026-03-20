import streamlit as st
import pandas as pd

from core.db import get_db_conn
from dashboard.services.sensor_service import get_sensor_history,get_latest_sensor_data,get_sensor_data_timeline

st.title("Sensor")

conn = get_db_conn()

try:
    # -------- live sensor values --------

    st.subheader("Current sensor status")

    latest = get_latest_sensor_data(conn)

    if latest:
        df_latest = pd.DataFrame(latest)
        st.dataframe(df_latest)

    st.subheader("Sensor Data Timeline")

    selected_sensor_id = st.selectbox(
        "Choose sensor",
        options=df_latest["sensor_id"],
        format_func=lambda x: f"Sensor {x}"
    )

    timeline = get_sensor_data_timeline(conn, sensor_id=selected_sensor_id)

    if timeline:
        df_timeline = pd.DataFrame(timeline)

        df_timeline["measured_at"] = pd.to_datetime(df_timeline["measured_at"])
        df_timeline["measurement"] = pd.to_numeric(
            df_timeline["measurement"],
            errors="coerce"
        ).astype(float)

        # senaste 1 timme
        hours = st.slider("Time window (hours)", 1, 24, 1)

        cutoff = pd.Timestamp.now() - pd.Timedelta(hours=hours)

        df_recent = df_timeline[df_timeline["measured_at"] >= cutoff]

        chart_df = (
            df_recent[["measured_at", "measurement"]]
            .dropna()
            .sort_values("measured_at")
            .set_index("measured_at")
        )

        st.dataframe(chart_df)
        st.line_chart(chart_df)
    else:
        st.info("No sensor timeline found.")
    # -------- sensor history --------

    st.subheader("Sensor history")

    history = get_sensor_history(conn)

    if not history:
        st.info("No sensor data yet.")

    df = pd.DataFrame(history)

    sensor_ids = df["sensor_id"].unique()
    selected_sensor = st.selectbox("Select sensor", sensor_ids)

    df = df[df["sensor_id"] == selected_sensor]
    df["period_date"] = pd.to_datetime(df["period_date"])
    df["measurement_avg"] = pd.to_numeric(df["measurement_avg"], errors="coerce").astype(float)

    st.line_chart(
        df.set_index("period_date")["measurement_avg"]
    )

    st.dataframe(df)

finally:
    conn.close()