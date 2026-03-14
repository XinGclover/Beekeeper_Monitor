import streamlit as st
import pandas as pd

from db import get_db_conn
from dashboard.services.sensor_service import get_sensor_history,get_latest_sensor_data


st.title("Sensor")

conn = get_db_conn()

try:
    # -------- live sensor values --------

    st.subheader("Current sensor status")

    latest = get_latest_sensor_data(conn)

    if latest:
        df_latest = pd.DataFrame(latest)
        st.dataframe(df_latest)


    # -------- sensor history --------

    st.subheader("Sensor history")

    history = get_sensor_history(conn)

    if not history:
        st.info("No sensor data yet.")

    df = pd.DataFrame(history)

    sensor_ids = df["sensor_id"].unique()
    selected_sensor = st.selectbox("Select sensor", sensor_ids)

    df = df[df["sensor_id"] == selected_sensor]

    st.line_chart(
        df.set_index("period_date")["measurement_avg"]
    )

    st.dataframe(df)

finally:
    conn.close()