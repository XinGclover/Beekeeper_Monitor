import streamlit as st
import pandas as pd

from dashboard.services.weather_service import get_weather_data
from dashboard.services.wildfire_service import get_wildfire_data
from core.db import get_db_conn
from streamlit_autorefresh import st_autorefresh


st.title("Weather & Wildfire")
refresh_count = st_autorefresh(interval=600000, key="sensor_refresh")
st.write("Refresh count:", refresh_count)

conn = get_db_conn()

tab1, tab2 = st.tabs(["Weather", "Wildfire"])

with tab1:
    st.subheader("Latest weather data")
    weather_data = get_weather_data(conn)
    df_weather = pd.DataFrame(weather_data)
    st.caption(f"Last updated: {df_weather['fetched_at'].max()}")
    st.dataframe(df_weather) 

with tab2:
    st.subheader("Wildfire alerts / events")
    wildfire_data = get_wildfire_data(conn)
    df_wildfire = pd.DataFrame(wildfire_data)
    st.caption(f"Last updated: {df_wildfire['fetched_at'].max()}")
    st.dataframe(df_wildfire)