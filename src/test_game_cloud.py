"""
test_game_cloud.py — Live Cloud Verification of FutureProof Endpoints on Render
Target: https://telos-sdc.onrender.com
"""

import os
import sys
import json
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

load_dotenv(Path(__file__).parent / ".env")

BASE_URL = os.environ.get("CLOUD_BASE_URL", "https://telos-sdc.onrender.com")
TOKEN = os.environ.get("API_ACCESS_TOKEN", "telos-sdc-dev-key-2026")
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}

def banner(title: str):
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)

def run_cloud_test():
    banner(f"RUNNING LIVE CLOUD VERIFICATION ON: {BASE_URL}")

    # 1. Health
    print("\n▶ [1] Health Check (/health)")
    t0 = time.time()
    r = requests.get(f"{BASE_URL}/health", timeout=30)
    print(f"  Status: {r.status_code} ({time.time()-t0:.2f}s) -> {r.json()}")
    assert r.status_code == 200

    # 2. Start Game
    print("\n▶ [2] POST /api/game/start (Mission A: Food Supply Under Pressure)")
    payload_start = {
        "profile": {
            "skills": ["Data Analysis", "Python", "Risk Management", "System Design"],
            "interests": ["AI Safety", "Infrastructure Operations", "Policy"],
            "learning_time": 8,
        },
        "mission_id": "A",
    }
    t0 = time.time()
    r = requests.post(f"{BASE_URL}/api/game/start", json=payload_start, headers=HEADERS, timeout=30)
    print(f"  Status: {r.status_code} ({time.time()-t0:.2f}s)")
    assert r.status_code == 200, f"Start failed: {r.status_code} {r.text}"
    start_data = r.json()
    session_id = start_data["session_id"]
    print(f"  ✓ Session Created on Render: {session_id}")
    print(f"  ✓ Briefing: {start_data['briefing'][:100]}...")

    # 3. Round 1
    print("\n▶ [3] POST /api/game/{id}/round (Round 1: Free-text strategy)")
    payload_r1 = {
        "round": 1,
        "free_text": (
            "My priority is to immediately establish baseline monitoring across all 4 corridors. "
            "I will allocate 40% of the budget to Route B because of high population density, "
            "but reserve emergency buffer capacity on Routes A and C to prevent single-point congestion failure."
        ),
    }
    t0 = time.time()
    r = requests.post(f"{BASE_URL}/api/game/{session_id}/round", json=payload_r1, headers=HEADERS, timeout=30)
    print(f"  Status: {r.status_code} ({time.time()-t0:.2f}s)")
    assert r.status_code == 200, f"Round 1 failed: {r.status_code} {r.text}"
    r1_data = r.json()
    print(f"  ✓ Round Accepted: {r1_data['round_accepted']} -> Next: {r1_data['next_round']}")
    print(f"  ✓ AI Recommendation: {r1_data.get('ai_recommendation')}")

    # 4. Evidence Drawer
    print("\n▶ [4] GET /api/game/{id}/evidence/2 (Evidence Drawer)")
    t0 = time.time()
    r = requests.get(f"{BASE_URL}/api/game/{session_id}/evidence/2", headers=HEADERS, timeout=30)
    print(f"  Status: {r.status_code} ({time.time()-t0:.2f}s)")
    assert r.status_code == 200
    ev = r.json().get("evidence", {})
    print(f"  ✓ Evidence Drawer Title: {ev.get('title')}")

    # 5. Round 2
    print("\n▶ [5] POST /api/game/{id}/round (Round 2: Decision on AI advice)")
    payload_r2 = {
        "round": 2,
        "action": "verify",
        "evidence_opened": True,
    }
    t0 = time.time()
    r = requests.post(f"{BASE_URL}/api/game/{session_id}/round", json=payload_r2, headers=HEADERS, timeout=30)
    print(f"  Status: {r.status_code} ({time.time()-t0:.2f}s)")
    assert r.status_code == 200
    r2_data = r.json()
    print(f"  ✓ Round 2 Accepted -> Next: {r2_data['next_round']}")
    print(f"  ✓ Shock Event: {r2_data.get('shock_event')[:80]}...")

    # 6. Round 3
    print("\n▶ [6] POST /api/game/{id}/round (Round 3: Adaptation to shock)")
    payload_r3 = {
        "round": 3,
        "free_text": (
            "Since Route B is halted and budget is cut by 50%, we must adapt immediately. "
            "I will not deploy the unvetted volunteer network to critical hospital shipments due to chain-of-custody risks, "
            "but I will deploy vetted volunteer teams exclusively on low-risk peripheral Route D distribution, "
            "while redirecting official logistics to Route A and C after verifying warehouse capacities."
        ),
    }
    t0 = time.time()
    r = requests.post(f"{BASE_URL}/api/game/{session_id}/round", json=payload_r3, headers=HEADERS, timeout=30)
    print(f"  Status: {r.status_code} ({time.time()-t0:.2f}s)")
    assert r.status_code == 200

    # 7. Round 4
    print("\n▶ [7] POST /api/game/{id}/round (Round 4: Final strategy)")
    payload_r4 = {
        "round": 4,
        "free_text": (
            "Final strategy committed: Deploy dual-pipeline supply model. Route A carries essential medical supplies; "
            "Route C carries food staples with regional depot staging. Volunteer network supports final-mile handoffs "
            "with identity checks. Cost reduced 48%, population covered 82%."
        ),
    }
    t0 = time.time()
    r = requests.post(f"{BASE_URL}/api/game/{session_id}/round", json=payload_r4, headers=HEADERS, timeout=30)
    print(f"  Status: {r.status_code} ({time.time()-t0:.2f}s)")
    assert r.status_code == 200
    print(f"  ✓ Game Complete: status={r.json().get('status')}")

    # 8. Report
    print("\n▶ [8] GET /api/game/{id}/report (Triggering Evaluation on Render)")
    t0 = time.time()
    r = requests.get(f"{BASE_URL}/api/game/{session_id}/report", headers=HEADERS, timeout=60)
    print(f"  Status: {r.status_code} ({time.time()-t0:.2f}s)")
    assert r.status_code == 200, f"Report failed: {r.status_code} {r.text}"
    report = r.json()
    print("\n" + "-" * 50)
    print(" 🎯 LIVE CLOUD BEHAVIORAL REPORT (F03)")
    print("-" * 50)
    for k, v in report.get("indicators", {}).items():
        if isinstance(v, dict):
            status = "✓" if (v.get("observed") or v.get("met_objectives")) else "✗"
            detail = v.get("evidence") or v.get("note") or ""
            print(f"  {status} {k.upper()}: {detail}")
    print(f"\n  • Strengths: {report.get('self_vs_observed_gap', {}).get('observed_strengths')}")
    print(f"  • Growth Areas: {report.get('self_vs_observed_gap', {}).get('observed_gaps')}")

    # 9. Matching
    print("\n▶ [9] GET /api/game/{id}/match (F04: Career Matching on Render)")
    t0 = time.time()
    r = requests.get(f"{BASE_URL}/api/game/{session_id}/match", headers=HEADERS, timeout=30)
    print(f"  Status: {r.status_code} ({time.time()-t0:.2f}s)")
    assert r.status_code == 200
    roles = r.json().get("roles", [])
    top_role_id = roles[0]["id"] if roles else None
    print("\n" + "-" * 50)
    print(" 🚀 TOP MATCHED ROLES FROM RENDER")
    print("-" * 50)
    for i, role in enumerate(roles, 1):
        print(f"  #{i} {role['title']} — Match: {role.get('match_percentage')}%")
        print(f"     Reasoning: {role.get('reasoning')}")

    # 10. Pathway
    if top_role_id:
        print(f"\n▶ [10] GET /api/game/pathway/{top_role_id} (F05: Pathway on Render)")
        t0 = time.time()
        r = requests.get(f"{BASE_URL}/api/game/pathway/{top_role_id}?session_id={session_id}&scenario=moderate", headers=HEADERS, timeout=30)
        print(f"  Status: {r.status_code} ({time.time()-t0:.2f}s)")
        assert r.status_code == 200
        pw = r.json()
        print(f"  ✓ Total Estimated Weeks: {pw.get('total_estimated_weeks')}")
        for step in pw.get("reskilling_path", [])[:2]:
            print(f"    Step {step['step_order']}: {step['skill']} (~{step['estimated_hours']}h)")

    banner("✅ ALL LIVE CLOUD TESTS PASSED ON RENDER!")

if __name__ == "__main__":
    run_cloud_test()
