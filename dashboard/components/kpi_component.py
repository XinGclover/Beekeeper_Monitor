import streamlit as st

def render_kpi_card(title: str, value: str, unit: str = "", icon: str = ""):
    if value is None:
        display_value = "--"
    else:
        display_value = f"{value}{unit}"

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">{icon} {title}</div>
            <div class="kpi-value">{display_value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )