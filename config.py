"""
config.py — all settings loaded from environment / .env file.
No secrets live in code.
"""

import os
from dotenv import load_dotenv

load_dotenv()  # reads .env in the project root if present

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.3"))