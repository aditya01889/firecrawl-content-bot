# config.py

import os

try:
    # ✅ For Streamlit Cloud
    import streamlit as st
    OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
    NOTION_API_KEY = st.secrets["NOTION_API_KEY"]
    NOTION_DATABASE_ID = st.secrets["NOTION_DATABASE_ID"]
    FIRECRAWL_API_KEY = st.secrets["FIRECRAWL_API_KEY"]
    BASE_URL = st.secrets.get("BASE_URL", "https://openrouter.ai/api/v1")
    MODEL_NAME = st.secrets.get("MODEL_NAME", "openai/gpt-3.5-turbo")

except (ImportError, KeyError):
    # ✅ For local development
    from dotenv import load_dotenv
    load_dotenv()

    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY not found in environment variables")
        
    NOTION_API_KEY = os.getenv("NOTION_API_KEY")
    NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
    FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
    BASE_URL = os.getenv("BASE_URL", "https://openrouter.ai/api/v1")
    MODEL_NAME = os.getenv("MODEL_NAME", "openai/gpt-3.5-turbo")
