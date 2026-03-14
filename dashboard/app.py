import streamlit as st

from dashboard.pages.sensors import render_sensors_page


def main():

    st.sidebar.title("Beekeeper Monitor")

    page = st.sidebar.selectbox(
        "Page",
        [
            "Sensors",
        ],
    )

    if page == "Sensors":
        render_sensors_page()


if __name__ == "__main__":
    main()