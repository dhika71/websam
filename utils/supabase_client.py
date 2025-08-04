# utils/supabase_client.py

from supabase import create_client
import os

# Ambil URL dan KEY dari environment variable atau Streamlit secrets
SUPABASE_URL = os.getenv("SUPABASE_URL") or st.secrets["SUPABASE_URL"]
SUPABASE_KEY = os.getenv("SUPABASE_KEY") or st.secrets["SUPABASE_KEY"]

def get_supabase_client():
    return create_client(SUPABASE_URL, SUPABASE_KEY)
