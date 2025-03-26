import streamlit as st
import os
from dotenv import load_dotenv

# Check if Streamlit Secrets exists without causing an error
try:
    streamlit_secrets = st.secrets._secrets  # Access private `_secrets` to check if it's set
    running_in_streamlit = bool(streamlit_secrets)
except Exception:
    running_in_streamlit = False  # If accessing secrets fails, assume running locally

# Load .env only if running locally
if not running_in_streamlit:
    load_dotenv()

def get_secret(key, default=None):
    """Retrieve secret from Streamlit secrets or environment variables."""
    if running_in_streamlit:
        return st.secrets.get(key, default)
    return os.getenv(key, default)

# Test: Print API Key only when running locally
if __name__ == '__main__':
    print(f"TAVILY_API_KEY: {get_secret('TAVILY_API_KEY', 'Not Found')}")
