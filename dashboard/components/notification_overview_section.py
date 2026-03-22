import streamlit as st
import pandas as pd


def render_notification_overview_section(notification_data: dict):
    st.subheader("Notifications")

    latest_rows = notification_data.get("latest", [])
    unread_count = notification_data.get("unread_count", 0)

    total_count = len(latest_rows)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Unread notifications", unread_count)
    with col2:
        st.metric("Latest loaded", total_count)

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
            subtitle = ""
            if n.get("target_name") and n.get("severity_name"):
                subtitle = f"{n['target_name']} · {n['severity_name']}"

            st.markdown(
                f"""
                <div style="padding-top:4px;">
                    <div style="
                        color:{title_color};
                        font-size:15px;
                        font-weight:{title_weight};
                        white-space: nowrap;
                        overflow: hidden;
                        text-overflow: ellipsis;
                    ">
                        {n["title"]}
                    </div>
                    <div style="
                        color:#6b7280;
                        font-size:13px;
                        margin-top:2px;
                        white-space: nowrap;
                        overflow: hidden;
                        text-overflow: ellipsis;
                    ">
                        {subtitle}
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