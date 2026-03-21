import streamlit as st
import pandas as pd


def render_sensor_overview_section(sensor_data: dict):
    st.subheader("Sensor Data")

    if sensor_data["timeseries"]:
        df_chart = pd.DataFrame(sensor_data["timeseries"])
        df_chart["measured_at"] = pd.to_datetime(df_chart["measured_at"])
        df_chart["measurement"] = pd.to_numeric(df_chart["measurement"], errors="coerce")

        metrics = df_chart["sensor_type_name"].dropna().unique()
        cols = st.columns(len(metrics))
        for i, metric in enumerate(metrics):
            with cols[i]:
                st.markdown(f"### {metric}")

                sub_df = df_chart[df_chart["sensor_type_name"] == metric]

                pivot_df = sub_df.pivot_table(
                    index="measured_at",
                    columns="sensor_id",
                    values="measurement",
                    aggfunc="mean"
                ).sort_index()

                st.line_chart(pivot_df)
    else:
        st.info("No sensor data found.")

    if sensor_data["latest"]:
        df_table = pd.DataFrame(sensor_data["latest"])
        st.dataframe(df_table, use_container_width=True, hide_index=True)