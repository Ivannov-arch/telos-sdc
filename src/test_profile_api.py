"""
test_profile_api.py — Verification of Feature 1 (Person B Day 2 Deliverable)
Tests:
  1. PDF resume upload (pdfplumber parsing + ESCO resolution + BGE-M3 embedding + Supabase persistence)
  2. Manual form submission (JSON mode)
  3. Profile retrieval by ID (GET /api/profile/{user_id})
  4. End-to-End Pipeline integration (POST /api/profile -> GET /api/match)
"""

import io
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def build_synthetic_pdf() -> bytes:
    """Generate a clean synthetic PDF resume for testing without external PDF tools."""
    lines = [
        "Alex Rivera - Senior Data Engineer",
        "5 years of experience building scalable ETL pipelines and machine learning infrastructure.",
        "Technical Skills: Python, SQL, Machine Learning, Apache Spark, Docker",
        "Soft Skills: Team Leadership, Stakeholder Management, Communication",
    ]
    bt_commands = ["BT", "/F1 12 Tf"]
    y = 750
    for line in lines:
        bt_commands.append(f"1 0 0 1 50 {y} Tm ({line}) Tj")
        y -= 25
    bt_commands.append("ET")
    stream_content = "\n".join(bt_commands)
    stream_bytes = stream_content.encode("latin1")

    pdf_bytes = (
        b"%PDF-1.4\n"
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 5 0 R >> >> /MediaBox [0 0 612 792] /Contents 4 0 R >>\nendobj\n"
        b"4 0 obj\n<< /Length " + str(len(stream_bytes)).encode("ascii") + b" >>\nstream\n" + stream_bytes + b"\nendstream\nendobj\n"
        b"5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n"
        b"xref\n0 6\n0000000000 65535 f \n"
        b"trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n500\n%%EOF"
    )
    return pdf_bytes


def test_cv_pdf_upload():
    print("\n" + "=" * 60)
    print("TEST 1: CV PDF Upload & Extraction (Substep 1.2 & 1.3)")
    print("=" * 60)

    pdf_data = build_synthetic_pdf()
    files = {"file": ("alex_rivera_cv.pdf", pdf_data, "application/pdf")}

    response = client.post("/api/profile/upload", files=files)
    assert response.status_code == 200, f"Upload failed: {response.status_code} - {response.text}"

    data = response.json()
    profile_id = data["id"]
    print(f"[OK] Profile created with ID: {profile_id}")
    print(f"     Source type: {data['source_type']}")
    print(f"     Experience years: {data['experience_years']}")
    print(f"     BGE-M3 Dense Vector generated: {data['has_dense_vector']}")

    print("\nExtracted Hard Skills:")
    for skill in data["hard_skills"]:
        esco = skill.get("esco_id") or "UNRESOLVED"
        print(f"  * {skill['skill_name']} -> ESCO: {esco} (conf: {skill['confidence_score']:.2f})")

    print("\nExtracted Soft Skills:")
    for skill in data["soft_skills"]:
        esco = skill.get("esco_id") or "UNRESOLVED"
        print(f"  * {skill['skill_name']} -> ESCO: {esco} (conf: {skill['confidence_score']:.2f})")

    assert data["experience_years"] == 5, f"Expected 5 years, got {data['experience_years']}"
    assert len(data["hard_skills"]) > 0, "No hard skills extracted"
    assert data["has_dense_vector"] is True, "BGE-M3 vector was not generated"

    return profile_id


def test_manual_form_submission():
    print("\n" + "=" * 60)
    print("TEST 2: Manual Form Intake (JSON Mode)")
    print("=" * 60)

    payload = {
        "hard_skills": ["Python", "SQL", "Data Analysis"],
        "soft_skills": ["Communication", "Problem Solving"],
        "experience_years": 3,
        "raw_text": "Experienced Python data analyst with strong SQL background.",
    }

    response = client.post("/api/profile", json=payload)
    assert response.status_code == 200, f"Manual intake failed: {response.status_code} - {response.text}"

    data = response.json()
    profile_id = data["id"]
    print(f"[OK] Manual Profile created with ID: {profile_id}")
    print(f"     Source type: {data['source_type']}")
    print(f"     Experience years: {data['experience_years']}")
    print(f"     BGE-M3 Vector generated: {data['has_dense_vector']}")

    assert data["experience_years"] == 3
    assert len(data["hard_skills"]) == 3
    assert data["has_dense_vector"] is True

    return profile_id


def test_profile_retrieval(profile_id: str):
    print("\n" + "=" * 60)
    print("TEST 3: Profile Retrieval (GET /api/profile/{id})")
    print("=" * 60)

    response = client.get(f"/api/profile/{profile_id}")
    assert response.status_code == 200, f"Get profile failed: {response.status_code} - {response.text}"
    data = response.json()
    print(f"[OK] Successfully retrieved profile {data['id']}")
    print(f"     Hard skills count: {len(data['hard_skills'])}")
    print(f"     Has dense vector: {data['has_dense_vector']}")
    assert data["id"] == profile_id


def test_end_to_end_matching(profile_id: str):
    print("\n" + "=" * 60)
    print("TEST 4: End-to-End Handshake (Feature 1 -> Feature 3)")
    print("=" * 60)
    print(f"Calling GET /api/match?user_id={profile_id} ...")

    response = client.get(f"/api/match?user_id={profile_id}&top_k=3")
    assert response.status_code == 200, f"Matching failed: {response.status_code} - {response.text}"

    data = response.json()
    results = data.get("results", [])
    print(f"[OK] Hybrid search returned {len(results)} ranked future roles:")

    for i, role in enumerate(results, 1):
        print(f"\n  #{i} {role['target_role']} (Match Score: {role['match_score']:.1%})")
        print(f"     RRF: {role['score_breakdown']['rrf_score']:.3f} | Skill Cov: {role['score_breakdown']['hard_skill_coverage']:.1%} | Seniority: {role['score_breakdown']['seniority_match']:.2f}")
        print(f"     Skill Gaps ({len(role['skills_gap'])}): {[g['skill'] for g in role['skills_gap'][:3]]}")
        if role.get("sdg_alignment"):
            sdg_strs = [f"SDG {s['sdg_goal']} ({s['sdg_name']})" for s in role["sdg_alignment"][:2]]
            print(f"     SDGs: {sdg_strs}")

    assert len(results) > 0, "No matching roles returned"
    print("\n[SUCCESS] Feature 1 -> Feature 3 End-to-End Pipeline fully verified!")


if __name__ == "__main__":
    try:
        pdf_profile_id = test_cv_pdf_upload()
        form_profile_id = test_manual_form_submission()
        test_profile_retrieval(pdf_profile_id)
        test_end_to_end_matching(pdf_profile_id)
        print("\n" + "=" * 60)
        print("[SUCCESS] ALL DAY 2 VERIFICATION TESTS PASSED SUCCESSFULLY!")
        print("=" * 60)
    except Exception as e:
        print(f"\n[FAIL] Test error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
