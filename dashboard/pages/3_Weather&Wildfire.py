import streamlit as st
import pandas as pd

from dashboard.services.weather_service import get_weather_data
from dashboard.services.wildfire_service import get_wildfire_data
from core.db import get_db_conn
import plotly.express as px 
from dashboard.services.location_service import fetch_location_overview

# avoid Streamlit reruning scripts all the time, so you can do:
@st.cache_data
def load_all_data():
    conn = get_db_conn()
    try:
        location_df = fetch_location_overview(conn)
        weather_df = get_weather_data(conn)
        wildfire_df = get_wildfire_data(conn)

        return location_df, weather_df, wildfire_df

    finally:
        conn.close()


location_df, weather_df, wildfire_df = load_all_data()

def format_value(value, suffix=""):
    if pd.isna(value):
        return "N/A"
    return f"{value}{suffix}"


def get_risk_color(severity):
    if severity == 3:
        return "red"
    elif severity == 2:
        return "orange"
    elif severity == 1:
        return "green"
    return "gray"


def show_location_map_page():
    st.title("Weather & Wildfire Map")

    if location_df.empty:
        st.info("No location data found.")
        return

    location_df["risk_color"] = location_df["severity_level_id"].apply(get_risk_color)
     
    st.subheader("Map")

    fig = px.scatter_map(
        location_df,
        lat="latitude",
        lon="longitude",
        hover_name="city",
        hover_data={
            "air_temperature":True,
            "wind_speed":True,
            "weather_time":True, 
            "severity_level_id":True,
            "brightness":True,
            "wildfire_time":True
        },
        color="risk_color", 
        size="frp",
        zoom=5,
        height=500
    )

    fig.update_layout(
    map_style="open-street-map",
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    )

    st.plotly_chart(fig)



tab1, tab2, tab3 = st.tabs(["Map", "Weather", "Wildfire"])

with tab1:
    show_location_map_page()

with tab2:
    st.subheader("Latest weather data")
    df_weather = pd.DataFrame(weather_df)
    st.caption(f"Last updated: {df_weather['fetched_at'].max()}")
    st.dataframe(df_weather) 

with tab3:
    st.subheader("Wildfire alerts / events")
    df_wildfire = pd.DataFrame(wildfire_df)
    st.caption(f"Last updated: {df_wildfire['fetched_at'].max()}")
    st.dataframe(df_wildfire)