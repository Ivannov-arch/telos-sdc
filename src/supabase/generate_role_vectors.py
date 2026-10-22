"""
generate_role_vectors.py — Substep 3.1 (Person A)
Embed all ESCO occupations via RunPod BGE-M3 /embed and store in telos_sdc.role_vectors.

Run from the project root:
    python src/supabase/generate_role_vectors.py

Prerequisites:
    - src/.env must have: SUPABASE_URL, SUPABASE_SECRET_KEY, RUNPOD_API_KEY, RUNPOD_BGE_M3_URL
    - telos_sdc.occupations must be seeded (run seed_esco.py first)
    - pip install supabase python-dotenv requests tqdm

Cost note:
    BGE-M3 embedding costs one forward pass per batch.
    Batch size 32 minimises RunPod GPU time. Run ONCE and rely on cached vectors — never re-embed.
"""

import os
import time
import requests
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client
from tqdm import tqdm

# ── Config ────────────────────────────────────────────────────────────────────

SRC_DIR  = Path(__file__).parent.parent          # .../src/
ENV_FILE = SRC_DIR / ".env"

load_dotenv(ENV_FILE)

SUPABASE_URL       = os.environ["SUPABASE_URL"]
SUPABASE_SECRET    = os.environ["SUPABASE_SECRET_KEY"]
RUNPOD_API_KEY     = os.environ["RUNPOD_API_KEY"]
RUNPOD_BGE_M3_URL  = os.environ["RUNPOD_BGE_M3_URL"]

EMBED_BATCH_SIZE   = 32          # Max texts per RunPod request (cost-efficient)
RETRY_LIMIT        = 3           # Retries on transient RunPod errors
RETRY_WAIT_SECS    = 10

db = create_client(SUPABASE_URL, SUPABASE_SECRET)

# ── BGE-M3 Embedding ─────────────────────────────────────────────────────────

def embed_batch(texts: list[str]) -> list[dict]:
    """
    Send a batch of texts to RunPod BGE-M3 endpoint.
    Returns list of {"dense": [...]} per text.

    Infinity worker response format:
        {"output": {"data": [{"embedding": [...], "index": 0}, ...]}}
    Note: Infinity returns dense vectors. Sparse vectors stored as NULL.
    Dense-only cosine similarity is sufficient for the demo RRF hybrid search.
    """
    headers = {
        "Authorization": f"Bearer {RUNPOD_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "input": {
            "model": "BAAI/bge-m3",
            "input": texts,
        }
    }

    for attempt in range(1, RETRY_LIMIT + 1):
        try:
            resp = requests.post(RUNPOD_BGE_M3_URL, headers=headers, json=payload, timeout=120)
            resp.raise_for_status()
            data = resp.json()

            items = data.get("output", {}).get("data", [])
            if not items:
                raise ValueError(f"Unexpected RunPod response format: {data}")

            # Sort by index to maintain order
            items.sort(key=lambda x: x["index"])
            return [{"dense": item["embedding"]} for item in items]

        except (requests.RequestException, ValueError) as exc:
            print(f"  ⚠️  Attempt {attempt}/{RETRY_LIMIT} failed: {exc}")
            if attempt < RETRY_LIMIT:
                time.sleep(RETRY_WAIT_SECS)
            else:
                raise


def build_occupation_text(occ: dict) -> str:
    """
    Compose a rich text representation of an ESCO occupation for embedding.
    Concatenating label + description + tasks produces a more semantically
    meaningful vector than embedding the title alone.
    """
    parts = [occ.get("preferred_label", "")]
    if occ.get("description"):
        parts.append(occ["description"][:300])   # cap description to 300 chars
    if occ.get("tasks"):
        task_excerpt = "; ".join(occ["tasks"][:5])  # first 5 O*NET tasks
        parts.append(task_excerpt)
    return ". ".join(p for p in parts if p).strip()


# ── Vector → pgvector format ──────────────────────────────────────────────────

def dense_to_pg(vec: list[float]) -> str:
    """Convert Python list to pgvector literal: '[0.1,0.2,...]'"""
    return "[" + ",".join(str(v) for v in vec) + "]"


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  Substep 3.1 — Role Vector Generation")
    print("  Owner: Person A | BGE-M3 via RunPod")
    print("=" * 60)

    # 1. Fetch all occupations from Supabase
    print("\n[1/4] Fetching occupations from telos_sdc.occupations ...")
    occ_resp = (
        db.schema("telos_sdc")
        .table("occupations")
        .select("esco_id, preferred_label, description, tasks")
        .execute()
    )
    occupations = occ_resp.data or []
    print(f"      Found {len(occupations)} occupations.")

    if not occupations:
        print("  ❌ No occupations found. Run seed_esco.py first.")
        return

    # 2. Check which role_ids already have vectors (resume support)
    print("\n[2/4] Checking existing role_vectors (skip already-embedded) ...")
    existing_resp = (
        db.schema("telos_sdc")
        .table("role_vectors")
        .select("role_id")
        .execute()
    )
    already_done = {r["role_id"] for r in (existing_resp.data or [])}
    pending = [o for o in occupations if o["esco_id"] not in already_done]
    print(f"      Already embedded: {len(already_done)} | Pending: {len(pending)}")

    if not pending:
        print("  ✅ All occupations already embedded. Nothing to do.")
        return

    # 3. Embed in batches
    print(f"\n[3/4] Embedding {len(pending)} occupations in batches of {EMBED_BATCH_SIZE} ...")
    rows_to_upsert = []

    for i in tqdm(range(0, len(pending), EMBED_BATCH_SIZE), desc="Embedding"):
        batch = pending[i : i + EMBED_BATCH_SIZE]
        texts = [build_occupation_text(occ) for occ in batch]

        embeddings = embed_batch(texts)

        for occ, emb in zip(batch, embeddings):
            rows_to_upsert.append({
                "role_id":            occ["esco_id"],
                "role_dense_vector":  dense_to_pg(emb["dense"]),
                # sparse: NULL — Infinity worker returns dense only.
                # Dense cosine similarity is sufficient for the demo.
                "role_sparse_vector": None,
                "embedded_at":        "now()",
            })

    # 4. Upsert into role_vectors
    print(f"\n[4/4] Upserting {len(rows_to_upsert)} rows into telos_sdc.role_vectors ...")
    UPSERT_BATCH = 100
    for i in tqdm(range(0, len(rows_to_upsert), UPSERT_BATCH), desc="Upserting"):
        chunk = rows_to_upsert[i : i + UPSERT_BATCH]
        db.schema("telos_sdc").table("role_vectors").upsert(
            chunk, on_conflict="role_id"
        ).execute()

    print("\n[OK] Done! role_vectors populated.")
    print(f"   Total rows embedded: {len(rows_to_upsert)}")
    print("\n[NOTE] Next step: verify hybrid_search() by running GET /api/match with a real user_id.")


if __name__ == "__main__":
    main()
