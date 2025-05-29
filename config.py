# config.py

import os

try:
    # ✅ For Streamlit Cloud
    import streamlit as st
    OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
    NOTION_API_KEY = st.secrets["NOTION_API_KEY"]
    NOTION_DATABASE_ID = st.secrets["NOTION_DATABASE_ID"]
    FIRECRAWL_API_KEY = st.secrets["FIRECRAWL_API_KEY"]

except ImportError:
    # ✅ For local development
    from dotenv import load_dotenv
    load_dotenv()

    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    NOTION_API_KEY = os.getenv("NOTION_API_KEY")
    NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
    FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")

# You can also define model-related constants here
BASE_URL = "https://openrouter.ai/api/v1"
MODEL_NAME = "openai/gpt-3.5-turbo"
