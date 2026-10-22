"""
embed_user_profiles.py — Substep 1.4: Generate user_dense_vector for user_profiles
Embeds user profiles using RunPod BGE-M3 and updates telos_sdc.user_profiles.
"""

import os
import requests
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client

SRC_DIR = Path(__file__).resolve().parent.parent
load_dotenv(SRC_DIR / ".env")

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_SECRET_KEY = os.environ["SUPABASE_SECRET_KEY"]
RUNPOD_API_KEY = os.environ["RUNPOD_API_KEY"]
RUNPOD_BGE_M3_URL = os.environ["RUNPOD_BGE_M3_URL"]

db: Client = create_client(SUPABASE_URL, SUPABASE_SECRET_KEY)


def build_profile_text(profile: dict) -> str:
    """Build a natural text string summarizing the profile skills for embedding."""
    if profile.get("raw_cv_text"):
        return profile["raw_cv_text"][:2000]

    hard = [s.get("label", "") for s in (profile.get("hard_skills") or []) if s.get("label")]
    soft = [s.get("label", "") for s in (profile.get("soft_skills") or []) if s.get("label")]
    years = profile.get("experience_years", 0)

    parts = []
    if hard:
        parts.append(f"Hard skills: {', '.join(hard)}")
    if soft:
        parts.append(f"Soft skills: {', '.join(soft)}")
    if years:
        parts.append(f"Experience: {years} years")

    return ". ".join(parts) if parts else "Professional worker"


def embed_texts(texts: list[str]) -> list[list[float]]:
    import time
    headers = {
        "Authorization": f"Bearer {RUNPOD_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {"input": {"model": "BAAI/bge-m3", "input": texts}}
    for attempt in range(1, 4):
        try:
            print(f"Calling RunPod BGE-M3 (attempt {attempt}/3, timeout=180s)...")
            resp = requests.post(RUNPOD_BGE_M3_URL, headers=headers, json=payload, timeout=180)
            resp.raise_for_status()
            result = resp.json()
            output = result.get("output", result)
            if isinstance(output, dict) and "data" in output:
                items = output["data"]
                items.sort(key=lambda x: x.get("index", 0))
                return [item["embedding"] for item in items]
            elif isinstance(output, list):
                return output
            else:
                raise ValueError(f"Unexpected response structure: {list(output.keys()) if isinstance(output, dict) else output}")
        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            if attempt < 3:
                time.sleep(5)
            else:
                raise


def main():
    print("Fetching user profiles without dense vectors...")
    res = (
        db.schema("telos_sdc")
        .table("user_profiles")
        .select("id, hard_skills, soft_skills, raw_cv_text, experience_years, user_dense_vector")
        .is_("user_dense_vector", "null")
        .execute()
    )
    profiles = res.data or []
    print(f"Found {len(profiles)} profiles needing embeddings.")

    if not profiles:
        print("All profiles already have vectors!")
        return

    texts = [build_profile_text(p) for p in profiles]
    print(f"Embedding {len(texts)} profiles via RunPod BGE-M3...")
    embeddings = embed_texts(texts)

    print(f"Updating {len(profiles)} user profiles in Supabase...")
    for p, emb in zip(profiles, embeddings):
        db.schema("telos_sdc").table("user_profiles").update(
            {"user_dense_vector": emb}
        ).eq("id", p["id"]).execute()

    print("[OK] Done! All user profiles embedded with user_dense_vector.")


if __name__ == "__main__":
    main()
