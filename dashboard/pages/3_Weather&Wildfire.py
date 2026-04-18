import pandas as pd
import plotly.express as px
import streamlit as st

from dashboard.utils.ui import get_risk_color
from dashboard.utils.api_client import get_json, wait_for_backend

with st.spinner("Waking up backend..."):
    ready = wait_for_backend()

if not ready:
    st.warning("Backend still sleeping. Try again soon.")
    st.stop()

# avoid Streamlit reruning scripts all the time, so you can do:
@st.cache_data
def load_all_data():
    location_data = get_json("/api/monitoring/locations/overview")
    weather_data = get_json("/api/monitoring/weather")
    wildfire_data = get_json("/api/monitoring/wildfire")

    location_df = pd.DataFrame(location_data)
    weather_df = pd.DataFrame(weather_data)
    wildfire_df = pd.DataFrame(wildfire_data)

    return location_df, weather_df, wildfire_df

location_df, weather_df, wildfire_df = load_all_data()


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
        height=500,
        color_discrete_map={
            "red": "red",
            "orange": "orange",
            "green": "green",
            "gray": "gray",
            "darkred": "darkred",
            "yellow": "yellow"
        }
    )

    fig.update_layout(
    map_style="open-street-map",
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    )

    fig.update_traces(marker=dict(opacity=0.8))

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