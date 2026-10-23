"""
test_match_api.py — Verify Priority 2: live RRF Hybrid Search via /api/match
"""

import json
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

PROFILES_TO_TEST = [
    ("587479a6-04d5-4371-a57f-c3b39c9b7be2", "AI / NLP Engineer Profile"),
    ("146f103d-946f-4619-9fa0-ba0b4fdfe84c", "Data Engineering Profile"),
]

for user_id, title in PROFILES_TO_TEST:
    print("=" * 60)
    print(f"Testing {title} (ID: {user_id})")
    print("=" * 60)
    resp = client.get(f"/api/match?user_id={user_id}&top_k=3")

    print(f"Status Code: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        print(f"User ID:  {data['user_id']}")
        print(f"Scenario: {data['scenario']}")
        print(f"Total roles matched: {len(data['results'])}\n")
        for i, r in enumerate(data["results"], 1):
            print(f"[{i}] {r['target_role']} - Match Score: {round(r['match_score'] * 100, 2)}% (raw: {r['match_score']})")
            print(f"    RRF Candidate Score: {r['score_breakdown']['rrf_score']}")
            print(f"    Skill Coverage:      {r['score_breakdown']['hard_skill_coverage']}")
            print(f"    Seniority Match:     {r['score_breakdown']['seniority_match']}")
            gaps = [s['skill'] for s in r.get('skills_gap', [])]
            print(f"    Skills Gap ({len(gaps)}): {gaps[:4]}")
            sdgs = [g['sdg_name'] for g in r.get('sdg_alignment', [])]
            print(f"    SDGs: {sdgs}")
            print()
    else:
        print("Error:", resp.text)

