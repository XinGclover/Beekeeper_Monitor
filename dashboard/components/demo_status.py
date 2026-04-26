import streamlit as st
from dashboard.utils.api_client import get_json


def render_demo_status_sidebar():
    """Render live demo status in the sidebar for multipage apps."""
    with st.sidebar:
        st.divider()
        st.markdown("### 🧪 Live Demo Status")

        try:
            status = get_json("/api/demo/status")
        except Exception:
            st.warning("⚠️ Backend not reachable")
            return

        if status.get("running"):
            remaining = status.get("remaining_seconds", 0)
            minutes = remaining // 60
            st.success(f"🟢 Running · {minutes} min left")
        else:
            st.info("⚪ Not running")
