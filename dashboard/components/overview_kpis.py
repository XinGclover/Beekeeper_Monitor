import streamlit as st
from dashboard.components.ui_styles import inject_kpi_card_css
from dashboard.components.kpi_component import render_kpi_card

def format_kpi_value(kpi: dict) -> str:
    value = kpi.get("value")
    unit = kpi.get("unit", "")

    if value is None:
        return "-"

    return f"{value}{unit}"

def get_kpi_emoji(label: str) -> str:
    label = label.lower()

    if "temperature" in label:
        return "🌡️"
    if "humidity" in label:
        return "💧"
    if "alarm" in label:
        return "⚠️"
    if "wildfire" in label:
        return "🔥"
    if "notification" in label:
        return "🔔"

    return "📊"


def render_kpi_row(kpis: dict):
    inject_kpi_card_css()
    cols = st.columns(len(kpis))

    for col, (_, kpi) in zip(cols, kpis.items()):
        label = kpi.get("label", "")
        value = kpi.get("value", "-")
        unit = kpi.get("unit", "")

        emoji = get_kpi_emoji(label)

        with col:
            render_kpi_card(label, value, unit, emoji)