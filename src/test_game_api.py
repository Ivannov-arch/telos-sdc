"""
test_game_api.py — End-to-End Automated Test for FutureProof Game Simulation & Career Intelligence

Tests:
  1. Service health (/health)
  2. POST /api/game/start — Quick Skill Profile & Round 1 initialization
  3. POST /api/game/{id}/round — Round 1 submission (free-text strategy)
  4. GET  /api/game/{id}/evidence/2 — Evidence drawer access in Round 2
  5. POST /api/game/{id}/round — Round 2 submission (AI recommendation verification)
  6. POST /api/game/{id}/round — Round 3 submission (shock event adaptation)
  7. POST /api/game/{id}/round — Round 4 submission (final strategy commitment)
  8. GET  /api/game/{id}/report — Silent LLM behavioral evaluation (Gemini 2.5 Flash)
  9. GET  /api/game/{id}/match — F04 Role Matching (3 MVP roles)
 10. GET  /api/game/pathway/{role_id} — F05 Career Pathway (Moderate vs Rapid)
"""

import os
import sys
import json
from pathlib import Path

# Ensure UTF-8 output on Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Ensure src/ is on sys.path
SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from dotenv import load_dotenv
load_dotenv(SRC_DIR / ".env")

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

# Use API_ACCESS_TOKEN for authentication header
TOKEN = os.environ.get("API_ACCESS_TOKEN", "telos-sdc-dev-key-2026")
HEADERS = {"Authorization": f"Bearer {TOKEN}"}


def banner(title: str):
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)


def test_full_game_loop():
    banner("FUTUREPROOF HUMAN-AI DECISION LAB — END-TO-END VERIFICATION")

    # ──────────────────────────────────────────────────────────────────────────
    # 1. Healthcheck
    # ──────────────────────────────────────────────────────────────────────────
    print("\n▶ [1] Health Check")
    resp = client.get("/health")
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.text}"
    print(f"  ✓ /health OK: {resp.json()}")

    # ──────────────────────────────────────────────────────────────────────────
    # 2. Start Game (F01 Profile + F02 Mission Choice)
    # ──────────────────────────────────────────────────────────────────────────
    print("\n▶ [2] POST /api/game/start (Starting Mission A: Food Supply Under Pressure)")
    start_payload = {
        "profile": {
            "skills": ["Data Analysis", "Python", "Risk Management", "System Design"],
            "interests": ["AI Safety", "Infrastructure Operations", "Policy"],
            "learning_time": 8,
        },
        "mission_id": "A",
    }
    resp = client.post("/api/game/start", json=start_payload, headers=HEADERS)
    assert resp.status_code == 200, f"Start game failed: {resp.status_code} {resp.text}"
    start_data = resp.json()
    session_id = start_data["session_id"]
    print(f"  ✓ Session Created: {session_id}")
    print(f"  ✓ Round: {start_data['round']}")
    print(f"  ✓ Briefing Snippet: {start_data['briefing'][:120]}...")

    # ──────────────────────────────────────────────────────────────────────────
    # 3. Round 1 Submission (Initial Instinct before AI)
    # ──────────────────────────────────────────────────────────────────────────
    print("\n▶ [3] POST /api/game/{id}/round (Round 1: Free-text Strategy)")
    r1_payload = {
        "round": 1,
        "free_text": (
            "My priority is to immediately establish baseline monitoring across all 4 corridors. "
            "I will allocate 40% of the budget to Route B because of high population density, "
            "but reserve emergency buffer capacity on Routes A and C to prevent single-point congestion failure."
        ),
    }
    resp = client.post(f"/api/game/{session_id}/round", json=r1_payload, headers=HEADERS)
    assert resp.status_code == 200, f"Round 1 submit failed: {resp.text}"
    r1_data = resp.json()
    print(f"  ✓ Round Accepted: {r1_data['round_accepted']} -> Next: {r1_data['next_round']}")
    print(f"  ✓ AI Recommendation: {r1_data.get('ai_recommendation')}")
    print(f"  ✓ Evidence Drawer Available: {r1_data.get('evidence_available')}")

    # ──────────────────────────────────────────────────────────────────────────
    # 4. Round 2: Evidence Drawer Check & Action
    # ──────────────────────────────────────────────────────────────────────────
    print("\n▶ [4] GET /api/game/{id}/evidence/2 (Inspecting Evidence Drawer)")
    resp_ev = client.get(f"/api/game/{session_id}/evidence/2", headers=HEADERS)
    assert resp_ev.status_code == 200, f"Evidence query failed: {resp_ev.text}"
    ev_data = resp_ev.json()
    print(f"  ✓ Evidence Drawer Title: {ev_data.get('evidence', {}).get('title')}")
    for item in ev_data.get("evidence", {}).get("items", [])[:2]:
        critical_flag = " [CRITICAL]" if item.get("is_critical") else ""
        print(f"    - {item['label']}: {item['value']}{critical_flag}")

    print("\n▶ [5] POST /api/game/{id}/round (Round 2 Decision: Verifying AI recommendation)")
    # Player checks evidence drawer and decides to verify/reject rather than blindly accept
    r2_payload = {
        "round": 2,
        "action": "verify",
        "evidence_opened": True,
    }
    resp = client.post(f"/api/game/{session_id}/round", json=r2_payload, headers=HEADERS)
    assert resp.status_code == 200, f"Round 2 submit failed: {resp.text}"
    r2_data = resp.json()
    print(f"  ✓ Round 2 Accepted -> Next: {r2_data['next_round']}")
    print(f"  ✓ AI Shock Event Received: {r2_data.get('shock_event')}")
    print(f"  ✓ Ambiguous Shock Opportunity: {r2_data.get('shock_opportunity')}")

    # ──────────────────────────────────────────────────────────────────────────
    # 5. Round 3 Submission (Adapting to Shock Event)
    # ──────────────────────────────────────────────────────────────────────────
    print("\n▶ [6] POST /api/game/{id}/round (Round 3: Adapting to Budget Cut & Volunteer Offer)")
    r3_payload = {
        "round": 3,
        "free_text": (
            "Since Route B is halted and budget is cut by 50%, we must adapt immediately. "
            "I will not deploy the unvetted volunteer network to critical hospital shipments due to chain-of-custody risks, "
            "but I will deploy vetted volunteer teams exclusively on low-risk peripheral Route D distribution, "
            "while redirecting official logistics to Route A and C after verifying warehouse capacities."
        ),
    }
    resp = client.post(f"/api/game/{session_id}/round", json=r3_payload, headers=HEADERS)
    assert resp.status_code == 200, f"Round 3 submit failed: {resp.text}"
    r3_data = resp.json()
    print(f"  ✓ Round 3 Accepted -> Next: {r3_data['next_round']}")
    print(f"  ✓ Round 4 Final Briefing: {r3_data.get('next_briefing')}")

    # ──────────────────────────────────────────────────────────────────────────
    # 6. Round 4 Submission (Final Commitment)
    # ──────────────────────────────────────────────────────────────────────────
    print("\n▶ [7] POST /api/game/{id}/round (Round 4: Final Strategy Commitment)")
    r4_payload = {
        "round": 4,
        "free_text": (
            "Final strategy committed: Deploy dual-pipeline supply model. Route A carries essential medical supplies; "
            "Route C carries food staples with regional depot staging. Volunteer network supports final-mile handoffs "
            "with identity checks. Cost reduced 48%, population covered 82%."
        ),
    }
    resp = client.post(f"/api/game/{session_id}/round", json=r4_payload, headers=HEADERS)
    assert resp.status_code == 200, f"Round 4 submit failed: {resp.text}"
    r4_data = resp.json()
    print(f"  ✓ Game Status: {r4_data['status']}")

    # ──────────────────────────────────────────────────────────────────────────
    # 7. The Reveal — Behavioral Skill Report (F03)
    # ──────────────────────────────────────────────────────────────────────────
    print("\n▶ [8] GET /api/game/{id}/report (Triggering LLM Evaluator)")
    resp_report = client.get(f"/api/game/{session_id}/report", headers=HEADERS)
    assert resp_report.status_code == 200, f"Report query failed: {resp_report.text}"
    report = resp_report.json()

    print("\n" + "-" * 50)
    print(" 🎯 BEHAVIORAL SKILL REPORT (F03)")
    print("-" * 50)
    print(f"Session: {report['session_id']} | Mission: {report['mission']}")
    indicators = report["indicators"]
    for k, v in indicators.items():
        if isinstance(v, dict):
            status_symbol = "✓" if (v.get("observed") or v.get("met_objectives")) else "✗"
            detail = v.get("evidence") or v.get("note") or ""
            print(f"  {status_symbol} {k.upper()}: {detail}")

    print("\n  [Self-Reported vs Observed Contrast]:")
    print(f"  • Observed Strengths: {report['self_vs_observed_gap'].get('observed_strengths')}")
    print(f"  • Growth Areas:       {report['self_vs_observed_gap'].get('observed_gaps')}")
    print(f"  • Summary Note:       {report['self_vs_observed_gap'].get('note')}")

    # ──────────────────────────────────────────────────────────────────────────
    # 8. Role Matching (F04)
    # ──────────────────────────────────────────────────────────────────────────
    print("\n▶ [9] GET /api/game/{id}/match (F04: Career Matching)")
    resp_match = client.get(f"/api/game/{session_id}/match", headers=HEADERS)
    assert resp_match.status_code == 200, f"Role matching failed: {resp_match.text}"
    match_data = resp_match.json()

    print("\n" + "-" * 50)
    print(" 🚀 TOP MATCHED ROLES (F04)")
    print("-" * 50)
    top_role_id = None
    roles_list = match_data.get("roles", [])
    assert len(roles_list) > 0, "Expected at least 1 matched role"
    for i, role in enumerate(roles_list, 1):
        if i == 1:
            top_role_id = role["id"]
        print(f"\n  #{i} {role['title']} — Match: {role.get('match_percentage', role.get('match_score'))}%")
        print(f"     Reasoning: {role.get('reasoning')}")
        print(f"     Skills Possessed: {role.get('skills_possessed')}")
        print(f"     Skill Gaps: {[g['skill'] for g in role.get('skill_gaps', [])[:3]]}")

    # ──────────────────────────────────────────────────────────────────────────
    # 9. Career Pathway (F05)
    # ──────────────────────────────────────────────────────────────────────────
    if top_role_id:
        print(f"\n▶ [10] GET /api/game/pathway/{top_role_id} (F05: Learning Pathways)")
        for scenario in ["moderate", "rapid"]:
            resp_pw = client.get(
                f"/api/game/pathway/{top_role_id}?session_id={session_id}&scenario={scenario}",
                headers=HEADERS,
            )
            assert resp_pw.status_code == 200, f"Pathway failed for {scenario}: {resp_pw.text}"
            pw_data = resp_pw.json()
            print(f"\n  [Scenario: {scenario.upper()}] — Total Est: {pw_data.get('total_estimated_weeks')} weeks")
            for step in pw_data.get("reskilling_path", [])[:2]:
                print(f"    Step {step['step_order']}: {step['skill']} (~{step['estimated_hours']}h)")
                for src in step.get("learning_sources", [])[:1]:
                    print(f"      🔗 {src['title']} ({src['url']})")

    banner("✅ ALL BACKEND TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    test_full_game_loop()
