import streamlit as st

from dashboard.utils.filter_utils import Filters
from dashboard.services.filter_service import get_filter_options
from dashboard.components.time_filter import render_time_filter


def _to_options(rows, id_key, label_key):
    options = {None: "All"}
    for row in rows:
        options[row[id_key]] = row[label_key]
    return options


def render_filter_bar() -> Filters:
    if "location_id" not in st.session_state:
        st.session_state.location_id = None
    if "apiary_id" not in st.session_state:
        st.session_state.apiary_id = None
    if "hive_id" not in st.session_state:
        st.session_state.hive_id = None
    if "sensor_id" not in st.session_state:
        st.session_state.sensor_id = None

    # Get all filter options in one API call
    filter_data = get_filter_options(
        location_id=st.session_state.location_id,
        apiary_id=st.session_state.apiary_id,
        hive_id=st.session_state.hive_id,
    )

    locations = filter_data.get("locations", [])
    apiaries = filter_data.get("apiaries", [])
    hives = filter_data.get("hives", [])
    sensors = filter_data.get("sensors", [])

    location_options = _to_options(locations, "location_id", "location_name")
    apiary_options = _to_options(apiaries, "apiary_id", "apiary_name")
    hive_options = _to_options(hives, "hive_id", "hive_name")
    sensor_options = _to_options(sensors, "sensor_id", "sensor_name")

    with st.container(key="sticky_top_filters"):
        # Row 1: Location, Apiary, Hive, Sensor filters
        col_location, col_apiary, col_hive, col_sensor = st.columns(4)

        with col_location:
            new_location = st.selectbox(
                "Location",
                options=list(location_options.keys()),
                format_func=lambda x: location_options[x],
                index=list(location_options.keys()).index(st.session_state.location_id)
                if st.session_state.location_id in location_options
                else 0,
            )

        if new_location != st.session_state.location_id:
            st.session_state.location_id = new_location
            st.session_state.apiary_id = None
            st.session_state.hive_id = None
            st.session_state.sensor_id = None
            st.rerun()

        with col_apiary:
            new_apiary = st.selectbox(
                "Apiary",
                options=list(apiary_options.keys()),
                format_func=lambda x: apiary_options[x],
                index=list(apiary_options.keys()).index(st.session_state.apiary_id)
                if st.session_state.apiary_id in apiary_options
                else 0,
            )

        if new_apiary != st.session_state.apiary_id:
            st.session_state.apiary_id = new_apiary
            st.session_state.hive_id = None
            st.session_state.sensor_id = None
            st.rerun()

        with col_hive:
            new_hive = st.selectbox(
                "Hive",
                options=list(hive_options.keys()),
                format_func=lambda x: hive_options[x],
                index=list(hive_options.keys()).index(st.session_state.hive_id)
                if st.session_state.hive_id in hive_options
                else 0,
            )

        if new_hive != st.session_state.hive_id:
            st.session_state.hive_id = new_hive
            st.session_state.sensor_id = None
            st.rerun()

        with col_sensor:
            new_sensor = st.selectbox(
                "Sensor",
                options=list(sensor_options.keys()),
                format_func=lambda x: sensor_options[x],
                index=list(sensor_options.keys()).index(st.session_state.sensor_id)
                if st.session_state.sensor_id in sensor_options
                else 0,
            )

        # Row 2: Time range selector (full width)
        render_time_filter()

    st.session_state.sensor_id = new_sensor

    return Filters(
        location_id=st.session_state.location_id,
        apiary_id=st.session_state.apiary_id,
        hive_id=st.session_state.hive_id,
        sensor_id=st.session_state.sensor_id,
        time_range=st.session_state.time_range,
    )
