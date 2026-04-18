import os
import streamlit as st
from dotenv import load_dotenv

# Execute only once
load_dotenv()


def get_api_base_url():
    url = os.getenv("API_BASE_URL") or st.secrets.get("API_BASE_URL")

    if not url:
        st.error("Missing API_BASE_URL")
        st.stop()

    return url