"""
db.py — Supabase client singleton for FastAPI backend
"""

import os
from functools import lru_cache
from dotenv import load_dotenv
from supabase import create_client, Client
from pathlib import Path

load_dotenv(Path(__file__).parent.parent / ".env")


@lru_cache(maxsize=1)
def get_supabase() -> Client:
    url = os.environ["SUPABASE_URL"]
    key = os.environ["SUPABASE_SECRET_KEY"]
    return create_client(url, key)
