import streamlit as st
import pandas as pd
from dashboard.components.ui_styles import inject_kpi_card_css
from dashboard.components.kpi_component import render_kpi_card


def render_notification_overview_section(notification_data: dict):
    st.subheader("Notifications")

    latest_rows = notification_data.get("latest", [])
    unread_count = notification_data.get("unread_count", 0)

    total_count = len(latest_rows)

    inject_kpi_card_css()
    metric_cols = st.columns(5)

    with metric_cols[0]:
        render_kpi_card(
            "Unread notifications",
            unread_count,
            "",
            "📩"
        )

    with metric_cols[1]:
        render_kpi_card(
            "Latest loaded",
            total_count,
            "",
            "📊"
        )


    if not latest_rows:
        st.info("No notifications found.")
        return

    st.markdown("### Latest notifications")

    for n in latest_rows:
        is_unread = not n["is_read"]
        emoji = "📩" if is_unread else "📬"
        title_color = "#111827" if is_unread else "#9ca3af"
        title_weight = "700" if is_unread else "400"

        time_text = ""
        if n.get("created_at"):
            time_text = pd.to_datetime(n["created_at"]).strftime("%b %d, %H:%M")

        col1, col2, col3 = st.columns([0.5, 6, 2])

        with col1:
            st.markdown(
                f"""
                <div style="
                    font-size: 24px;
                    line-height: 1;
                    padding-top: 6px;
                    text-align: center;
                ">{emoji}</div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            rule_name = n.get("rule_name", "-")
            target_name = n.get("target_name", "-")
            severity_name = n.get("severity_name", "-").lower()

            severity_color_map = {
                "low": "#10b981",
                "medium": "#f59e0b",
                "high": "#ef4444",
            }
            severity_color = severity_color_map.get(severity_name, "#6b7280")

            time_text = ""
            if n.get("created_at"):
                time_text = pd.to_datetime(n["created_at"]).strftime("%b %d, %H:%M")

            st.markdown(
                f"""
                <div style="
                    display:flex;
                    align-items:center;
                    justify-content:space-between;
                    gap:12px;
                ">

                <div style="
                    font-size:15px;
                    font-weight:{title_weight};
                    color:{title_color};
                    white-space: nowrap;
                    overflow: hidden;
                    text-overflow: ellipsis;
                    flex:1;
                ">
                    {rule_name}
                </div>

                <div>{target_name}</div>

                <div style="color:{severity_color}; font-weight:600;">
                    {severity_name}
                </div>
                </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

        with col3:
            st.markdown(
                f"""
                <div style="
                    text-align:right;
                    color:#6b7280;
                    font-size:13px;
                    padding-top:8px;
                ">
                    {time_text}
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("<hr style='margin: 0.3rem 0 0.7rem 0;'>", unsafe_allow_html=True)