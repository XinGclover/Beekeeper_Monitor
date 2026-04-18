from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))


def main():
    import streamlit as st

    st.title("🐝 Beekeeper Monitoring System")

    st.markdown("""
    ### Project Overview

    This application demonstrates a **data monitoring system for beehives** developed as a **group project**.

    The system collects and analyzes data from multiple sources to help beekeepers monitor hive conditions and detect potential risks.
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

    Incoming data is stored in a **PostgreSQL database** and continuously analyzed.

    When abnormal conditions are detected, such as:

    • unusually high hive temperature  
    • strong wind conditions  
    • nearby wildfire events  

    the system generates **alarm events** and sends **notifications** to beekeepers.
    """)

    st.markdown("""
    ### Explore the Dashboard

    Use the navigation pages to explore different parts of the system:

    **Sensors**  
    View real-time and historical hive sensor data.

    **Weather & Wildfire**  
    Monitor external environmental conditions affecting the apiary.

    **Alarms & Notifications**  
    Track abnormal events detected by the system.

    **Data Models**  
    View the conceptual, logical, and physical database models.
    """)

    st.markdown("""
    ### Project Context

    This system was developed as part of a **Database design and modeling** course group project.  
    The **conceptual, logical, and physical data models**, as well as the **system diagrams**,
    were designed collaboratively by the project group.
                
    This dashboard demonstrates the system architecture, data pipeline,
    and monitoring interface built on top of the group’s database design.
    """)
   
    st.markdown("### System Architecture")

    tab1, tab2, tab3 = st.tabs(["Conceptual Model", "Logical Model", "Physical Model"])

    with tab1:
        st.subheader("Conceptual Model")
        st.image("assets/conceptual_model.png", width="stretch")

    with tab2:
        st.subheader("Logical Model")
        st.image("assets/logical_model.svg", width="stretch")

    with tab3:
        st.subheader("Physical Model")
        st.image("assets/physical_model.svg", width="stretch")

if __name__ == "__main__":
    main()