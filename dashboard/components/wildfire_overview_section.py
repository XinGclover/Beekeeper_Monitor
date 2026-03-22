import pandas as pd
import plotly.express as px
import streamlit as st


def get_risk_color(severity_name: str) -> str:
    severity = (severity_name or "").lower()

    if severity == "high":
        return "red"
    if severity == "medium":
        return "orange"
    if severity == "low":
        return "green"
    return "gray"


def render_wildfire_overview_section(wildfire_data: dict):
    st.subheader("Wildfire Events")

    map_rows = wildfire_data.get("map_points", [])
    latest_rows = wildfire_data.get("latest", [])

    if not map_rows and not latest_rows:
        st.info("No wildfire data found.")
        return

    if map_rows:
        df_map = pd.DataFrame(map_rows)

        df_map["detected_at"] = pd.to_datetime(df_map["detected_at"])
        df_map["frp"] = pd.to_numeric(df_map["frp"], errors="coerce")
        df_map["brightness"] = pd.to_numeric(df_map["brightness"], errors="coerce")
        df_map["risk_color"] = df_map["severity_name"].apply(get_risk_color)

        center = {
            "lat": df_map["latitude"].mean(),
            "lon": df_map["longitude"].mean(),
        }

        fig = px.scatter_map(
            df_map,
            lat="latitude",
            lon="longitude",
            hover_name="city",
            hover_data={
                "severity_name": True,
                "frp": True,
                "brightness": True,
                "detected_at": True,
                "latitude": False,
                "longitude": False,
                "risk_color": False,
            },
            color="risk_color",
            size="frp",
            zoom=8,
            center=center,
            height=350,
            color_discrete_map={
                "green": "green",
                "orange": "orange",
                "red": "red",
                "gray": "gray",
            },
        )

        fig.update_layout(
            map_style="open-street-map",
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
        )

        fig.update_traces(marker=dict(opacity=0.8))

        st.plotly_chart(fig, use_container_width=True)

    if latest_rows:
        df_latest = pd.DataFrame(latest_rows).copy()

        if "detected_at" in df_latest.columns:
            df_latest["detected_at"] = pd.to_datetime(df_latest["detected_at"])
            df_latest["detected_at"] = df_latest["detected_at"].dt.strftime("%b %d, %H:%M")

        show_cols = ["severity_name", "frp", "detected_at"]
        show_cols = [col for col in show_cols if col in df_latest.columns]

        st.dataframe(
            df_latest[show_cols],
            use_container_width=True,
            hide_index=True,
        )