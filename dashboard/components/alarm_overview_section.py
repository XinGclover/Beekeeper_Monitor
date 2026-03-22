import pandas as pd
import streamlit as st


def render_alarm_overview_section(alarm_data: dict):
    st.subheader("Alarm Events")

    latest_rows = alarm_data.get("latest", [])
    hourly_rows = alarm_data.get("hourly", [])

    if not latest_rows and not hourly_rows:
        st.info("No alarm events found.")
        return

    if hourly_rows:
        df_hourly = pd.DataFrame(hourly_rows)
        df_hourly["hour"] = pd.to_datetime(df_hourly["hour"])
        df_hourly = df_hourly.sort_values("hour")

        chart_df = df_hourly.set_index("hour")[["alarm_count"]]
        st.bar_chart(chart_df, use_container_width=True)

    if latest_rows:
        df_latest = pd.DataFrame(latest_rows).copy()

        if "created_at" in df_latest.columns:
            df_latest["created_at"] = pd.to_datetime(df_latest["created_at"])
            df_latest["created_at"] = df_latest["created_at"].dt.strftime("%b %d, %H:%M")

        show_cols = ["event_id", "rule_name", "target_name", "status","observed_value","triggered_at"]
        show_cols = [col for col in show_cols if col in df_latest.columns]

        st.dataframe(
            df_latest[show_cols],
            use_container_width=True,
            hide_index=True,
        )