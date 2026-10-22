"""
seed_esco.py — Seed ESCO v1.2.0 CSV into Supabase (schema: telos_sdc)
Owner: Person A (Backend Lead)
Working directory: src/  (run from c:\\Coding\\Hackathons\\SDC_XMUM\\src)
Run: python supabase/seed_esco.py

CSV files expected at: src/data/
    - skills_en.csv
    - occupations_en.csv
    - occupationSkillRelations_en.csv

Requirements:
    pip install supabase python-dotenv tqdm
"""

import os
import csv
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client
from tqdm import tqdm

# ── Paths ────────────────────────────────────────────────────────────────────

# Script lives at src/supabase/seed_esco.py
# .env lives at src/.env
# data lives at src/data/
SRC_DIR  = Path(__file__).parent.parent          # c:/.../src/
DATA_DIR = SRC_DIR / "data"
ENV_FILE = SRC_DIR / ".env"

load_dotenv(ENV_FILE)

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_SECRET_KEY"]    # secret key (bypasses RLS)

BATCH_SIZE = 500

# ── Client ───────────────────────────────────────────────────────────────────

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def upsert(table: str, rows: list[dict], conflict: str = "esco_id") -> None:
    if not rows:
        return
    supabase.schema("telos_sdc").table(table).upsert(rows, on_conflict=conflict).execute()


# ── Skills ───────────────────────────────────────────────────────────────────
# Actual columns: conceptType, conceptUri, skillType, reuseLevel,
#                 preferredLabel, altLabels, hiddenLabels, status,
#                 modifiedDate, scopeNote, definition, inScheme, description

def seed_skills(csv_path: Path) -> int:
    print(f"\n[skills] Seeding from {csv_path.name} ...")
    batch: list[dict] = []
    total = skipped = 0

    with open(csv_path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in tqdm(reader, desc="  skills"):
            esco_id = row.get("conceptUri", "").strip()
            label   = row.get("preferredLabel", "").strip()
            if not esco_id or not label:
                skipped += 1
                continue

            # Normalize skillType → CHECK constraint
            raw_type = row.get("skillType", "").strip().lower()
            if "knowledge" in raw_type:
                skill_type = "knowledge"
            elif "attitude" in raw_type:
                skill_type = "attitude"
            else:
                skill_type = "skill/competence"

            # alt_labels: newline or pipe separated in ESCO CSVs
            alt_raw = row.get("altLabels", "").strip()
            alt_labels = (
                [lbl.strip() for lbl in alt_raw.replace("|", "\n").splitlines() if lbl.strip()]
                if alt_raw else []
            )

            batch.append({
                "esco_id":         esco_id,
                "preferred_label": label,
                "alt_labels":      alt_labels,
                "skill_type":      skill_type,
                "description":     row.get("description", "").strip() or None,
                "broader_skill_id": None,   # ESCO hierarchy in separate file; skip for now
            })
            total += 1

            if len(batch) >= BATCH_SIZE:
                upsert("skills", batch)
                batch.clear()

    upsert("skills", batch)
    print(f"  Done: {total:,} inserted, {skipped} skipped.")
    return total


# ── Occupations ──────────────────────────────────────────────────────────────
# Actual columns: conceptType, conceptUri, iscoGroup, preferredLabel,
#                 altLabels, hiddenLabels, status, modifiedDate,
#                 regulatedProfessionNote, scopeNote, definition,
#                 inScheme, description, code

def seed_occupations(csv_path: Path) -> int:
    print(f"\n[occupations] Seeding from {csv_path.name} ...")
    batch: list[dict] = []
    total = skipped = 0

    with open(csv_path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in tqdm(reader, desc="  occupations"):
            esco_id = row.get("conceptUri", "").strip()
            label   = row.get("preferredLabel", "").strip()
            if not esco_id or not label:
                skipped += 1
                continue

            alt_raw = row.get("altLabels", "").strip()
            alt_labels = (
                [lbl.strip() for lbl in alt_raw.replace("|", "\n").splitlines() if lbl.strip()]
                if alt_raw else []
            )

            batch.append({
                "esco_id":         esco_id,
                "preferred_label": label,
                "alt_labels":      alt_labels,
                "description":     row.get("description", "").strip() or None,
                "isco_group":      row.get("iscoGroup", "").strip() or None,
                # onet_soc_code, tasks, work_activities, knowledge_areas
                # → populated later (Day 2 O*NET enrichment, Substep 3.1)
            })
            total += 1

            if len(batch) >= BATCH_SIZE:
                upsert("occupations", batch)
                batch.clear()

    upsert("occupations", batch)
    print(f"  Done: {total:,} inserted, {skipped} skipped.")
    return total


# ── Role Required Skills ─────────────────────────────────────────────────────
# Actual columns: occupationUri, relationType, skillType, skillUri

def seed_role_required_skills(csv_path: Path) -> int:
    print(f"\n[role_required_skills] Seeding from {csv_path.name} ...")
    print("  (This file is ~22 MB — may take a minute...)")
    # Use a dict keyed on (role_id, skill_id) to deduplicate within each batch.
    # PostgreSQL raises '21000' if the same constrained key appears twice in
    # a single ON CONFLICT DO UPDATE command.
    batch_dict: dict[tuple, dict] = {}
    total = skipped = 0

    def flush(d: dict) -> None:
        if d:
            supabase.schema("telos_sdc").table("role_required_skills") \
                .upsert(list(d.values()), on_conflict="role_id,skill_id").execute()
            d.clear()

    with open(csv_path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in tqdm(reader, desc="  relations"):
            role_id  = row.get("occupationUri", "").strip()
            skill_id = row.get("skillUri", "").strip()
            rel_type = row.get("relationType", "essential").strip().lower()

            if not role_id or not skill_id:
                skipped += 1
                continue

            key = (role_id, skill_id)
            batch_dict[key] = {
                "role_id":      role_id,
                "skill_id":     skill_id,
                "is_essential": rel_type == "essential",
                "weight":       1.0 if rel_type == "essential" else 0.5,
            }
            total += 1

            if len(batch_dict) >= BATCH_SIZE:
                flush(batch_dict)

    flush(batch_dict)

    print(f"  Done: {total:,} inserted, {skipped} skipped.")
    return total


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("ESCO v1.2.0 Seeder => telos_sdc schema")
    print(f"Data dir : {DATA_DIR}")
    print(f"Env file : {ENV_FILE}")
    print("=" * 60)

    # Locate CSVs
    skills_csv    = DATA_DIR / "skills_en.csv"
    occ_csv       = DATA_DIR / "occupations_en.csv"
    rel_csv       = DATA_DIR / "occupationSkillRelations_en.csv"

    for f in [skills_csv, occ_csv, rel_csv]:
        if not f.exists():
            raise FileNotFoundError(f"Missing: {f}")
        print(f"  Found: {f.name} ({f.stat().st_size / 1_000_000:.1f} MB)")

    # Seed
    s = seed_skills(skills_csv)
    o = seed_occupations(occ_csv)
    r = seed_role_required_skills(rel_csv)

    # Summary
    print("\n" + "=" * 60)
    print("SEED COMPLETE")
    print(f"  skills               : {s:,} rows")
    print(f"  occupations          : {o:,} rows")
    print(f"  role_required_skills : {r:,} rows")
    print("=" * 60)
    print("\nUNBLOCKS:")
    print("  [Person B] ESCO skills table live (Substep 1.3 can start)")
    print("  [Person C] occupations table live (Substep 5.2 can start)")
    print("  [Person D] skill IDs available   (Substep 4.1 prep can finalize)")
    print("\nNEXT: run seed_sdg.py")


if __name__ == "__main__":
    main()
