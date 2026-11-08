"""
config.py — all settings loaded from environment / .env file.
No secrets live in code.
"""

# import os
# from dotenv import load_dotenv

# load_dotenv()  # reads .env in the project root if present

# # GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
# # MODEL = os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b")
# # TEMPERATURE = float(os.getenv("TEMPERATURE", "0.3"))

import os
from dotenv import load_dotenv

load_dotenv()


def get_setting(name, default=""):
    # First check local .env
    value = os.getenv(name)

    if value:
        return value

    # Then check Streamlit Cloud Secrets
    try:
        import streamlit as st
        return st.secrets.get(name, default)
    except Exception:
        return default


GEMINI_API_KEY = get_setting("GEMINI_API_KEY")
MODEL = get_setting("GEMINI_MODEL", "gemini-3.5-flash-lite")
TEMPERATURE = float(get_setting("TEMPERATURE", "0.3"))

