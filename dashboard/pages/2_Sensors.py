import streamlit as st
import pandas as pd
import requests
from dashboard.utils.api_client import get_json, wait_for_backend

st.title("Sensor")

with st.spinner("Waking up backend..."):
    ready = wait_for_backend()

if not ready:
    st.warning("Backend still sleeping. Try again soon.")
    st.stop()

try:
    # -------- live sensor values --------

    st.subheader("Current sensor status")

    latest = get_json("/api/monitoring/sensors/latest")

    if latest:
        df_latest = pd.DataFrame(latest)
        st.dataframe(df_latest)
    else:
        df_latest = pd.DataFrame()
        st.info("No latest sensor data found.")

    st.subheader("Sensor Data Timeline")

    if df_latest.empty:
        st.info("No sensors available.")
    else:
        selected_sensor_id = st.selectbox(
            "Choose sensor",
            options=df_latest["sensor_id"],
            format_func=lambda x: f"Sensor {x}"
        )

        # -------- sensor timeline --------

        timeline = get_json(
            "/api/monitoring/sensors/timeline",
            params={"sensor_id": selected_sensor_id},
        )

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

        history = get_json(
            "/api/monitoring/sensors/history",
            params={"sensor_id": selected_sensor_id},
        )

        if not history:
            st.info("No sensor data yet.")
        else:
            df_history = pd.DataFrame(history)
            
            df_history["period_date"] = pd.to_datetime(df_history["period_date"])
            df_history["measurement_avg"] = pd.to_numeric(
                df_history["measurement_avg"], 
                errors="coerce").astype(float)

            st.line_chart(
                df_history.set_index("period_date")["measurement_avg"]
            )

            st.dataframe(df_history)

except requests.RequestException as exc:
    st.error(f"API request failed: {exc}")
except Exception as exc:
    st.error(f"Unexpected error: {exc}")