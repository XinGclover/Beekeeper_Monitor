import streamlit as st


def render_time_filter():
    return st.segmented_control(
        "Time Range",
        options=["1h", "6h", "24h", "7d", "30d"],
        format_func=lambda x: {
            "1h": "1 Hours",
            "6h": "6 Hours",
            "24h": "24 Hours",
            "7d": "7 Days",
            "30d": "30 Days",
        }[x],
        default=st.session_state.get("time_range", "6h"),
        key="time_range",
        selection_mode="single",
        label_visibility="collapsed",
        width="stretch",
    )