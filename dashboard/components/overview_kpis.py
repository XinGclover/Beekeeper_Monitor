import streamlit as st

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
    st.markdown(
        """
        <style>
        .kpi-container {
            display: flex;
            gap: 16px;
        }
        .kpi-card {
            flex: 1;
            background-color: #f8f9fa;
            border-radius: 12px;
            padding: 16px 20px;
            border: 1px solid #e5e7eb;
        }
        .kpi-title {
            font-size: 13px;
            color: #6b7280;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .kpi-value {
            font-size: 28px;
            font-weight: 600;
            margin-top: 8px;
            color: #111827;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
   
    cols = st.columns(len(kpis))

    for col, (_, kpi) in zip(cols, kpis.items()):
        label = kpi.get("label", "")
        value = kpi.get("value", "-")
        unit = kpi.get("unit", "")

        emoji = get_kpi_emoji(label)

        with col:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-title">
                        {emoji} {label}
                    </div>
                    <div class="kpi-value">
                        {value}{unit}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )