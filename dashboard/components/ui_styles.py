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

import streamlit as st

# Overview layout
def inject_page_compact_css():
    st.markdown(
        """
        <style>
        .main .block-container {
            padding-top: 0.8rem;
            padding-bottom: 1rem;
            padding-left: 0.8rem;
            padding-right: 0.8rem;
            max-width: 100%;
        }

        div[data-testid="stVerticalBlock"] {
            gap: 0.75rem;
        }

        h1 {
            margin-top: 0rem;
            margin-bottom: 1rem;
        }

        h2, h3 {
            margin-top: 0.5rem;
            margin-bottom: 0.5rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# kpi card style
def inject_kpi_card_css():
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