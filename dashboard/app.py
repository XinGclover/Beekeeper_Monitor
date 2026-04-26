import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st

from dashboard.utils.api_client import post_json
from dashboard.components.demo_status import render_demo_status_sidebar


def main():

    st.title("🐝 Beekeeper Monitoring System")

    with st.sidebar:
        st.header("Live Demo")

        if st.button("Start 30-minute live demo"):
            try:
                response = post_json("/api/demo/start")
                if response.get("running"):
                    st.success(response.get("message", "Live demo started."))
                else:
                    st.error(response.get("message", "Unable to start live demo."))
            except Exception as error:
                st.error(f"Failed to start live demo: {error}")
    
    render_demo_status_sidebar()

    st.markdown("""
    ### Project Overview

    **Beekeeper Monitor** is a data monitoring application for beehive environments.

    The original database design was developed as a **group project** in the course  
    **Databasdesign och modellering**. The project focuses on collecting and organizing
    data from hive sensors, weather APIs, and wildfire sources to support beekeepers in
    monitoring hive conditions and detecting environmental risks.
    """)

    st.markdown("""
    ### Data Sources

    The system integrates several types of data:

    • **Hive sensors** – temperature, humidity, and hive weight  
    • **Weather data** – collected from external weather APIs  
    • **Wildfire data** – monitoring nearby wildfire activity
    """)

    st.markdown("""
    ### System Functionality

    Incoming data is stored in a **PostgreSQL database** and analyzed to detect abnormal
    conditions.

    Examples of detected risks include:

    • unusually high hive temperature  
    • abnormal humidity or weight changes  
    • strong wind conditions  
    • nearby wildfire events  

    When a risk is detected, the system generates **alarm events** and creates
    **notifications** for beekeepers.
    """)

    st.markdown("""
    ### Explore the Dashboard

    Use the navigation pages to explore different parts of the system:

    **Sensors**  
    View latest and historical hive sensor measurements.

    **Weather & Wildfire**  
    Monitor external environmental conditions affecting the apiary.

    **Alarms & Notifications**  
    Track abnormal events and generated notifications.

    **Data Models**  
    View the database models and the dimensional model used for analytics.
    """)

    st.markdown("""
    ### Project Context

    The **conceptual model**, **logical model**, and **physical model** were created
    collaboratively as part of the group assignment for the course  
    **Databasdesign och modellering**.

    Building on top of that group database design, I independently developed the
    extended system implementation, including:

    • the PostgreSQL database setup and data ingestion pipelines  
    • the Streamlit monitoring dashboard  
    • the alarm and notification features  
    • the API/dashboard integration  
    • the dimensional model for analytical reporting  

    This application demonstrates how the original database design can be extended into
    a more complete data engineering and monitoring platform.
    """)

    st.markdown("### System Architecture")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Conceptual Model", "Logical Model", "Physical Model", "Dimensional Model"]
    )

    with tab1:
        st.subheader("Conceptual Model")
        st.caption("Group project work – Databasdesign och modellering")
        st.image("assets/conceptual_model.png", width="stretch")

    with tab2:
        st.subheader("Logical Model")
        st.caption("Group project work – Databasdesign och modellering")
        st.image("assets/logical_model.svg", width="stretch")

    with tab3:
        st.subheader("Physical Model")
        st.caption("Group project work – Databasdesign och modellering")
        st.image("assets/physical_model.svg", width="stretch")

    with tab4:
        st.subheader("Dimensional Model")
        st.caption("Individually extended analytical model")
        st.image("assets/dimensional_model.svg", width="stretch")


if __name__ == "__main__":
    main()