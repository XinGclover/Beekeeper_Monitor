import streamlit as st


def inject_sticky_topbar_css():
    st.markdown(
        """
        <style>
        div[data-testid="stVerticalBlock"] > div:has(> div.st-key-sticky_top_filters) {
            position: sticky;
            top: 3.6rem;
            z-index: 999;
            background: #f8f9fa;
            padding: 0.5rem;
            border-bottom: 1px solid rgba(255,255,255,0.08);
            margin-top: 0.5rem;
            border-radius: 10px;
        }
        .st-key-sticky_top_filters {
            background: transparent;
        }

        .st-key-sticky_top_filters .stSelectbox,
        .st-key-sticky_top_filters .stSegmentedControl {
            margin-bottom: 5px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )