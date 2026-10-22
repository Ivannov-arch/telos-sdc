"""
enrich_onet.py - Enrich telos_sdc.occupations with O*NET Task + Work Activity data
Owner: Person A (Backend Lead) - Substep 3.1 (O*NET Enrichment)
Working directory: src/
Run: python -X utf8 supabase/enrich_onet.py

Strategy (REVISED - Title-Based Fuzzy Crosswalk):
    ESCO v1.2.0 does NOT include onet_soc_code. All rows are NULL.
    Instead, we build a crosswalk purely from occupation title text:

    1. Build SOC -> tasks[]         from task_statements.csv  (Core tasks, top 10)
    2. Build SOC -> work_activities[] from work_activities.csv (IM scale, top 8)
    3. Build title->SOC index from O*NET (unique occupation titles)
    4. For each ESCO occupation:
       a. Attempt exact lowercase match against O*NET titles
       b. Fuzzy fallback via difflib.get_close_matches (cutoff 0.72)
    5. Batch-update telos_sdc.occupations (onet_soc_code, tasks, work_activities)

Files expected at src/data/onet/:
    - task_statements.csv
    - work_activities.csv
"""

import os
import csv
import difflib
import re
from pathlib import Path
from collections import defaultdict

from dotenv import load_dotenv
from supabase import create_client, Client
from tqdm import tqdm

# ── Paths & Config ─────────────────────────────────────────────────────────────

SRC_DIR  = Path(__file__).parent.parent
DATA_DIR = SRC_DIR / "data" / "onet"
ENV_FILE = SRC_DIR / ".env"

load_dotenv(ENV_FILE)

supabase: Client = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_SECRET_KEY"],
)

TASK_LIMIT     = 10   # top N core tasks per occupation
ACTIVITY_LIMIT = 8    # top N work activities by importance
BATCH_SIZE     = 50   # Supabase PATCH batch size
FUZZY_CUTOFF   = 0.72 # difflib similarity threshold (0-1)
FUZZY_N        = 1    # return top 1 fuzzy match


# ── Helpers ────────────────────────────────────────────────────────────────────

def normalize(text: str) -> str:
    """
    Normalize a job title for matching:
    - lowercase
    - strip punctuation except hyphens
    - collapse whitespace
    """
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)   # remove punctuation except hyphens
    text = re.sub(r"\s+", " ", text)
    return text


# ── Step 1: Build SOC -> tasks dict ────────────────────────────────────────────

def load_tasks(csv_path: Path):
    """
    Returns ({soc_code: [task_text, ...]}, {soc_code: title}).
    Core tasks only, capped at TASK_LIMIT.
    """
    print(f"\n[1/5] Loading task statements from {csv_path.name} ...")
    soc_tasks: dict[str, list[str]]  = defaultdict(list)
    soc_title: dict[str, str]        = {}

    with open(csv_path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            soc       = row["O*NET-SOC Code"].strip()
            title     = row["Title"].strip()
            task      = row["Task"].strip()
            task_type = row.get("Task Type", "").strip().lower()

            # Record first title seen for this SOC
            if soc not in soc_title:
                soc_title[soc] = title

            if task and task_type == "core":
                soc_tasks[soc].append(task)

    # Cap at TASK_LIMIT
    result = {soc: tasks[:TASK_LIMIT] for soc, tasks in soc_tasks.items()}
    print(f"  Loaded tasks for {len(result):,} SOC codes.")
    print(f"  Title index has {len(soc_title):,} unique SOC titles.")
    return result, soc_title


# ── Step 2: Build SOC -> work_activities dict ───────────────────────────────────

def load_work_activities(csv_path: Path) -> dict:
    """
    Returns {soc_code: [activity_name, ...]}
    Importance scale (IM), top ACTIVITY_LIMIT by Data Value descending.
    """
    print(f"\n[2/5] Loading work activities from {csv_path.name} ...")
    soc_activities: dict[str, list] = defaultdict(list)

    with open(csv_path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            soc      = row["O*NET-SOC Code"].strip()
            scale_id = row.get("Scale ID", "").strip()
            suppress = row.get("Recommend Suppress", "").strip().upper()

            if scale_id != "IM" or suppress == "Y":
                continue

            name = row["Element Name"].strip()
            try:
                score = float(row["Data Value"])
            except ValueError:
                continue
            soc_activities[soc].append((score, name))

    # Sort by importance descending, deduplicate, cap
    result: dict[str, list[str]] = {}
    for soc, items in soc_activities.items():
        seen: set[str] = set()
        top: list[str] = []
        for _, name in sorted(items, reverse=True):
            if name not in seen and len(top) < ACTIVITY_LIMIT:
                seen.add(name)
                top.append(name)
        result[soc] = top

    print(f"  Loaded work activities for {len(result):,} SOC codes.")
    return result


# ── Step 3: Build title -> SOC crosswalk ────────────────────────────────────────

def build_title_crosswalk(soc_title: dict):
    """
    Returns:
        norm_to_soc: {normalized_title: soc_code}  for O(1) exact lookup
        norm_titles : [normalized_title, ...]        for difflib fuzzy search
    """
    print(f"\n[3/5] Building title-based crosswalk for {len(soc_title):,} O*NET occupations ...")
    norm_to_soc: dict[str, str] = {}

    for soc, title in soc_title.items():
        norm = normalize(title)
        norm_to_soc[norm] = soc

    norm_titles = list(norm_to_soc.keys())
    print(f"  Crosswalk ready ({len(norm_titles):,} normalized O*NET titles).")
    return norm_to_soc, norm_titles


def match_title(esco_label: str, norm_to_soc: dict, norm_titles: list):
    """
    Find best matching O*NET SOC code for an ESCO preferred_label.
    Returns (soc_code, match_type) where match_type: 'exact', 'fuzzy', or 'none'.
    """
    norm = normalize(esco_label)

    # 1. Exact match
    if norm in norm_to_soc:
        return norm_to_soc[norm], "exact"

    # 2. Fuzzy match
    matches = difflib.get_close_matches(norm, norm_titles, n=FUZZY_N, cutoff=FUZZY_CUTOFF)
    if matches:
        return norm_to_soc[matches[0]], "fuzzy"

    return None, "none"


# ── Step 4: Fetch ESCO occupations from Supabase ────────────────────────────────

def fetch_esco_occupations() -> list:
    """
    Fetch all ESCO occupations. Returns list of {esco_id, preferred_label}.
    Paginates in pages of 1000 until exhausted.
    """
    print("\n[4/5] Fetching ESCO occupations from Supabase ...")
    all_rows: list = []
    page_size = 1000
    offset    = 0

    while True:
        resp = (
            supabase.schema("telos_sdc")
            .table("occupations")
            .select("esco_id, preferred_label")
            .range(offset, offset + page_size - 1)
            .execute()
        )
        batch = resp.data or []
        all_rows.extend(batch)
        if len(batch) < page_size:
            break
        offset += page_size

    print(f"  Fetched {len(all_rows):,} ESCO occupations.")
    return all_rows


# ── Step 5: Match + Batch-update Supabase ───────────────────────────────────────

def enrich_occupations(
    esco_rows:      list,
    soc_tasks:      dict,
    soc_activities: dict,
    norm_to_soc:    dict,
    norm_titles:    list,
):
    """
    For each ESCO occupation:
        - Match its preferred_label to an O*NET SOC code (exact then fuzzy)
        - Build update payload with onet_soc_code + tasks + work_activities
        - Push to Supabase in batches

    Returns (exact_count, fuzzy_count, skipped_count)
    """
    print(f"\n[5/5] Matching + enriching {len(esco_rows):,} ESCO occupations ...")

    exact_count = fuzzy_count = skipped_count = 0
    batch_updates: list = []  # [(esco_id, patch)]

    for row in tqdm(esco_rows, desc="  matching"):
        esco_id = row["esco_id"]
        label   = row.get("preferred_label", "") or ""

        soc_code, match_type = match_title(label, norm_to_soc, norm_titles)

        if not soc_code:
            skipped_count += 1
            continue

        patch: dict = {"onet_soc_code": soc_code}

        tasks = soc_tasks.get(soc_code)
        if tasks:
            patch["tasks"] = tasks

        activities = soc_activities.get(soc_code)
        if activities:
            patch["work_activities"] = activities

        # Only update if we have enrichment data beyond just the SOC code
        if len(patch) == 1:
            skipped_count += 1
            continue

        batch_updates.append((esco_id, patch))

        if match_type == "exact":
            exact_count += 1
        else:
            fuzzy_count += 1

    # Send to Supabase in batches
    total_to_push = len(batch_updates)
    print(f"\n  Sending {total_to_push:,} updates to Supabase ...")
    print(f"  Exact matches : {exact_count:,}")
    print(f"  Fuzzy matches : {fuzzy_count:,}")
    print(f"  Skipped       : {skipped_count:,}")

    for i in tqdm(range(0, total_to_push, BATCH_SIZE), desc="  uploading"):
        chunk = batch_updates[i : i + BATCH_SIZE]
        for esco_id, patch in chunk:
            (
                supabase.schema("telos_sdc")
                .table("occupations")
                .update(patch)
                .eq("esco_id", esco_id)
                .execute()
            )

    return exact_count, fuzzy_count, skipped_count


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("O*NET Enrichment => telos_sdc.occupations")
    print("Strategy: Title-Based Fuzzy Crosswalk")
    print(f"Data dir : {DATA_DIR}")
    print("=" * 60)

    tasks_csv    = DATA_DIR / "task_statements.csv"
    activity_csv = DATA_DIR / "work_activities.csv"

    for f in [tasks_csv, activity_csv]:
        if not f.exists():
            raise FileNotFoundError(f"Missing file: {f}")
        print(f"  Found: {f.name} ({f.stat().st_size / 1_000_000:.1f} MB)")

    soc_tasks, soc_title     = load_tasks(tasks_csv)
    soc_activities           = load_work_activities(activity_csv)
    norm_to_soc, norm_titles = build_title_crosswalk(soc_title)

    esco_rows = fetch_esco_occupations()

    exact, fuzzy, skipped = enrich_occupations(
        esco_rows, soc_tasks, soc_activities, norm_to_soc, norm_titles
    )

    total_enriched = exact + fuzzy
    print("\n" + "=" * 60)
    print("O*NET ENRICHMENT COMPLETE")
    print(f"  Occupations enriched  : {total_enriched:,}")
    print(f"    - Exact title match : {exact:,}")
    print(f"    - Fuzzy title match : {fuzzy:,}")
    print(f"  Skipped (no match)    : {skipped:,}")
    print("=" * 60)
    print("\nUNBLOCKS:")
    print("  [Person B] tasks + work_activities text ready for BGE-M3 embedding")
    print("  [Self]     Proceed to seed_role_sdg.py (Substep 5.2)")


if __name__ == "__main__":
    main()
