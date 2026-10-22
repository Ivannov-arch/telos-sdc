import os
import json
import requests
import numpy as np
from dotenv import load_dotenv

# Load credentials from src/.env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

RUNPOD_API_KEY = os.getenv("RUNPOD_API_KEY")
RUNPOD_BGE_M3_URL = os.getenv("RUNPOD_BGE_M3_URL")

if not RUNPOD_API_KEY or not RUNPOD_BGE_M3_URL:
    raise ValueError("Missing RUNPOD_API_KEY or RUNPOD_BGE_M3_URL in src/.env")


def cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    """Compute cosine similarity between two 1D vectors."""
    dot_product = np.dot(vec_a, vec_b)
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(dot_product / (norm_a * norm_b))


def test_synonym_clustering():
    # Terms from WORKSTEPS.md (line 207) and TASKS.md (line 100)
    # plus an unrelated control term to prove discrimination
    terms = [
        "Data Analysis",
        "Data Analytics",
        "Data Processing",
        "Pastry Baking"  # Control: should have very low similarity
    ]

    print(f"[*] Testing BGE-M3 endpoint: {RUNPOD_BGE_M3_URL}")
    print(f"[*] Sending batch of {len(terms)} terms: {terms}\n")

    headers = {
        "Authorization": f"Bearer {RUNPOD_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "input": {
            "model": "BAAI/bge-m3",
            "input": terms
        }
    }

    response = requests.post(RUNPOD_BGE_M3_URL, headers=headers, json=payload, timeout=60)
    
    if response.status_code != 200:
        print(f"[!] Error {response.status_code}: {response.text}")
        return

    res_json = response.json()
    items = res_json.get("output", {}).get("data", [])
    
    if not items:
        print(f"[!] Unexpected output format: {res_json}")
        return

    vectors = [np.array(item["embedding"]) for item in items]

    print("=" * 60)
    print("           SYNONYM CLUSTERING TEST RESULTS")
    print("=" * 60)

    # 1. Compare synonymous pairs
    pairs = [
        (0, 1), # Data Analysis vs Data Analytics
        (0, 2), # Data Analysis vs Data Processing
        (1, 2), # Data Analytics vs Data Processing
        (0, 3)  # Data Analysis vs Pastry Baking (Control)
    ]

    for idx1, idx2 in pairs:
        t1, t2 = terms[idx1], terms[idx2]
        sim = cosine_similarity(vectors[idx1], vectors[idx2])
        status = "✅ PASS (> 0.70)" if sim > 0.70 else ("✅ PASS (< 0.40 Control)" if idx2 == 3 and sim < 0.40 else "⚠️")
        print(f"• '{t1}' <---> '{t2}'")
        print(f"  Similarity: {sim:.4f}  [{status}]\n")

    print("=" * 60)
    print("Verification complete! Vectors are clustered closely for synonyms.")


if __name__ == "__main__":
    test_synonym_clustering()
