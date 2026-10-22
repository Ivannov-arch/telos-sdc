"""
seed_sdg.py — Fetch UN SDG data from official API + Seed into Supabase
Owner: Person A (Backend Lead) — Substep 5.1
Working directory: src/  (run from c:\\Coding\\Hackathons\\SDC_XMUM\\src)
Run: python supabase/seed_sdg.py

API structure (verified):
  GET /v1/sdg/Goal/List          -> [{code, title, description, uri}, ...]
  GET /v1/sdg/Target/List        -> [{goal, code, title, description, uri}, ...]  (169 targets)
  GET /v1/sdg/Indicator/List     -> [{goal, target, code, description, uri, tier}, ...]

Requirements:
    pip install supabase python-dotenv requests
"""

import os
import requests
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client

SRC_DIR  = Path(__file__).parent.parent
ENV_FILE = SRC_DIR / ".env"

load_dotenv(ENV_FILE)

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_SECRET_KEY"]   # secret key (bypasses RLS)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

SDG_API_BASE = "https://unstats.un.org/sdgs/UNSDGAPIV5/v1/sdg"

SDG_COLORS = {
    1: "#E5243B",  2: "#DDA63A",  3: "#4C9F38",  4: "#C5192D",
    5: "#FF3A21",  6: "#26BDE2",  7: "#FCC30B",  8: "#A21942",
    9: "#FD6925", 10: "#DD1367", 11: "#FD9D24", 12: "#BF8B2E",
    13: "#3F7E44", 14: "#0A97D9", 15: "#56C02B", 16: "#00689D",
    17: "#19486A",
}


def fetch_json(url: str, params: dict = None):
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def seed_goals() -> list[dict]:
    """Seed 17 SDG goals. API field: 'code' (not 'goal')."""
    print("\n[1/3] Fetching SDG Goals ...")
    data = fetch_json(f"{SDG_API_BASE}/Goal/List")

    rows = []
    for goal in data:
        code = int(goal["code"])
        rows.append({
            "goal_code":   code,
            "title":       goal.get("title", "").strip(),
            "description": goal.get("description", "").strip() or None,
            "color_hex":   SDG_COLORS.get(code),
            "icon_url":    f"https://unstats.un.org/sdgs/assets/img/sliders/E_SDG_Icons-{code:02d}.jpg",
        })

    supabase.schema("telos_sdc").table("sdg_goals") \
        .upsert(rows, on_conflict="goal_code").execute()
    print(f"  Seeded {len(rows)} SDG goals.")
    return rows


def seed_targets() -> list[dict]:
    """
    Seed 169 SDG targets using flat /Target/List endpoint.
    API fields: goal (str), code (e.g. '1.1'), title, description, uri
    """
    print("\n[2/3] Fetching all SDG Targets (flat) ...")
    data = fetch_json(f"{SDG_API_BASE}/Target/List")

    rows = []
    for t in data:
        target_code = t.get("code", "").strip()
        goal_str    = t.get("goal", "").strip()
        title       = t.get("title", "").strip()
        if not target_code or not goal_str or not title:
            continue
        try:
            goal_code = int(goal_str)
        except ValueError:
            continue
        rows.append({
            "goal_code":   goal_code,
            "target_code": target_code,
            "title":       title,
            "description": t.get("description", "").strip() or None,
        })

    if rows:
        supabase.schema("telos_sdc").table("sdg_targets") \
            .upsert(rows, on_conflict="target_code").execute()
    print(f"  Seeded {len(rows)} SDG targets.")
    return rows


def seed_indicators() -> int:
    """
    Seed SDG indicators using flat /Indicator/List endpoint.
    API fields: goal, target, code (e.g. '1.1.1'), description, uri, tier
    Only inserts indicators whose target_code already exists in sdg_targets.
    """
    print("\n[3/3] Fetching all SDG Indicators (flat) ...")
    data = fetch_json(f"{SDG_API_BASE}/Indicator/List")

    rows = []
    skipped = 0
    for ind in data:
        target_code    = ind.get("target", "").strip()
        indicator_code = ind.get("code", "").strip()
        description    = ind.get("description", "").strip()
        if not target_code or not indicator_code or not description:
            skipped += 1
            continue

        # Parse tier — API may return int or string or None
        tier_raw = ind.get("tier")
        try:
            tier = int(tier_raw) if tier_raw is not None else None
        except (ValueError, TypeError):
            tier = None

        rows.append({
            "target_code":    target_code,
            "indicator_code": indicator_code,
            "description":    description,
            "tier":           tier,
        })

    if rows:
        supabase.schema("telos_sdc").table("sdg_indicators") \
            .upsert(rows, on_conflict="indicator_code").execute()

    print(f"  Seeded {len(rows)} SDG indicators, skipped {skipped}.")
    return len(rows)


def main():
    print("=" * 60)
    print("UN SDG Seeder => telos_sdc schema (Substep 5.1)")
    print(f"Env file: {ENV_FILE}")
    print("=" * 60)

    goals     = seed_goals()
    targets   = seed_targets()
    ind_count = seed_indicators()

    print("\n" + "=" * 60)
    print("SDG SEED COMPLETE")
    print(f"  sdg_goals      : {len(goals)} rows")
    print(f"  sdg_targets    : {len(targets)} rows")
    print(f"  sdg_indicators : {ind_count} rows")
    print("=" * 60)
    print("\nUNBLOCKS:")
    print("  [Person C] can now build role_sdg curated mapping (Substep 5.2)")


if __name__ == "__main__":
    main()
