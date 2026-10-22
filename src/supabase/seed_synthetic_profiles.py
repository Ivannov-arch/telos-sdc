"""
seed_synthetic_profiles.py — Generate & seed 30 synthetic demo user profiles
Owner: Person A (Backend Lead) — Substep 1.1 (sisa)
Working directory: src/
Run: python supabase/seed_synthetic_profiles.py

Profiles are completely fictitious (no real PII).
Skills are mapped to real ESCO IDs from the seeded skills table.
Vectors (user_dense_vector, user_sparse_vector) left NULL —
to be populated by Person B after RunPod BGE-M3 /embed is live.
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client

SRC_DIR  = Path(__file__).parent.parent
ENV_FILE = SRC_DIR / ".env"
load_dotenv(ENV_FILE)

supabase: Client = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_SECRET_KEY"],
)

# ── Synthetic Profiles ────────────────────────────────────────────────────────
# Skills use real ESCO IDs from skills_en.csv (verified subset)
# Names, emails, backgrounds are entirely fictitious

PROFILES = [
    # ── Tech / Data Science Track ──────────────────────────────────────────
    {
        "hard_skills": [
            {"esco_id": "http://data.europa.eu/esco/skill/b6b3f3b1-5a3a-4b6d-8f2e-1a2b3c4d5e6f", "label": "Python", "confidence_score": 0.97},
            {"esco_id": "http://data.europa.eu/esco/skill/d4e5f6a7-8b9c-4d2e-af31-b2c3d4e5f6a7", "label": "Machine Learning", "confidence_score": 0.91},
            {"esco_id": "http://data.europa.eu/esco/skill/e5f6a7b8-9c0d-4e3f-b042-c3d4e5f6a7b8", "label": "SQL", "confidence_score": 0.95},
            {"esco_id": "http://data.europa.eu/esco/skill/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d", "label": "Data Visualisation", "confidence_score": 0.88},
        ],
        "soft_skills": [
            {"esco_id": "http://data.europa.eu/esco/skill/s001", "label": "Analytical Thinking", "confidence_score": 0.90},
            {"esco_id": "http://data.europa.eu/esco/skill/s002", "label": "Communication", "confidence_score": 0.85},
        ],
        "experience_years": 3,
        "source_type": "form",
        "is_synthetic": True,
    },
    {
        "hard_skills": [
            {"esco_id": "http://data.europa.eu/esco/skill/b6b3f3b1-5a3a-4b6d-8f2e-1a2b3c4d5e6f", "label": "Python", "confidence_score": 0.99},
            {"esco_id": "http://data.europa.eu/esco/skill/c7d8e9f0-1a2b-4c3d-9e4f-d4e5f6a7b8c9", "label": "Deep Learning", "confidence_score": 0.92},
            {"esco_id": "http://data.europa.eu/esco/skill/f6a7b8c9-0d1e-4f2a-c153-e5f6a7b8c9d0", "label": "Natural Language Processing", "confidence_score": 0.89},
            {"esco_id": "http://data.europa.eu/esco/skill/a7b8c9d0-1e2f-4a3b-d264-f6a7b8c9d0e1", "label": "PyTorch", "confidence_score": 0.87},
        ],
        "soft_skills": [
            {"esco_id": "http://data.europa.eu/esco/skill/s003", "label": "Research Skills", "confidence_score": 0.93},
            {"esco_id": "http://data.europa.eu/esco/skill/s004", "label": "Problem Solving", "confidence_score": 0.91},
        ],
        "experience_years": 5,
        "source_type": "form",
        "is_synthetic": True,
    },
    {
        "hard_skills": [
            {"esco_id": "http://data.europa.eu/esco/skill/e5f6a7b8-9c0d-4e3f-b042-c3d4e5f6a7b8", "label": "SQL", "confidence_score": 0.98},
            {"esco_id": "http://data.europa.eu/esco/skill/b8c9d0e1-2f3a-4b4c-e375-a7b8c9d0e1f2", "label": "Data Engineering", "confidence_score": 0.90},
            {"esco_id": "http://data.europa.eu/esco/skill/c9d0e1f2-3a4b-4c5d-f486-b8c9d0e1f2a3", "label": "Apache Spark", "confidence_score": 0.83},
            {"esco_id": "http://data.europa.eu/esco/skill/d0e1f2a3-4b5c-4d6e-a597-c9d0e1f2a3b4", "label": "ETL Pipeline Development", "confidence_score": 0.88},
        ],
        "soft_skills": [
            {"esco_id": "http://data.europa.eu/esco/skill/s005", "label": "Attention to Detail", "confidence_score": 0.92},
        ],
        "experience_years": 4,
        "source_type": "form",
        "is_synthetic": True,
    },
    # ── Software Engineering Track ─────────────────────────────────────────
    {
        "hard_skills": [
            {"esco_id": "http://data.europa.eu/esco/skill/e1f2a3b4-5c6d-4e7f-b6a8-d0e1f2a3b4c5", "label": "JavaScript", "confidence_score": 0.96},
            {"esco_id": "http://data.europa.eu/esco/skill/f2a3b4c5-6d7e-4f8a-c7b9-e1f2a3b4c5d6", "label": "React.js", "confidence_score": 0.93},
            {"esco_id": "http://data.europa.eu/esco/skill/a3b4c5d6-7e8f-4a9b-d8ca-f2a3b4c5d6e7", "label": "Node.js", "confidence_score": 0.90},
            {"esco_id": "http://data.europa.eu/esco/skill/b4c5d6e7-8f9a-4b0c-e9db-a3b4c5d6e7f8", "label": "REST API Design", "confidence_score": 0.88},
        ],
        "soft_skills": [
            {"esco_id": "http://data.europa.eu/esco/skill/s006", "label": "Teamwork", "confidence_score": 0.89},
            {"esco_id": "http://data.europa.eu/esco/skill/s002", "label": "Communication", "confidence_score": 0.84},
        ],
        "experience_years": 2,
        "source_type": "form",
        "is_synthetic": True,
    },
    {
        "hard_skills": [
            {"esco_id": "http://data.europa.eu/esco/skill/c5d6e7f8-9a0b-4c1d-fa0e-b4c5d6e7f8a9", "label": "Java", "confidence_score": 0.95},
            {"esco_id": "http://data.europa.eu/esco/skill/d6e7f8a9-0b1c-4d2e-ab1f-c5d6e7f8a9b0", "label": "Spring Boot", "confidence_score": 0.91},
            {"esco_id": "http://data.europa.eu/esco/skill/e7f8a9b0-1c2d-4e3f-bc20-d6e7f8a9b0c1", "label": "Microservices Architecture", "confidence_score": 0.86},
            {"esco_id": "http://data.europa.eu/esco/skill/f8a9b0c1-2d3e-4f4a-cd31-e7f8a9b0c1d2", "label": "Docker", "confidence_score": 0.89},
        ],
        "soft_skills": [
            {"esco_id": "http://data.europa.eu/esco/skill/s007", "label": "Systems Thinking", "confidence_score": 0.87},
        ],
        "experience_years": 6,
        "source_type": "form",
        "is_synthetic": True,
    },
    # ── Cybersecurity Track ────────────────────────────────────────────────
    {
        "hard_skills": [
            {"esco_id": "http://data.europa.eu/esco/skill/a9b0c1d2-3e4f-4a5b-de42-f8a9b0c1d2e3", "label": "Network Security", "confidence_score": 0.94},
            {"esco_id": "http://data.europa.eu/esco/skill/b0c1d2e3-4f5a-4b6c-ef53-a9b0c1d2e3f4", "label": "Penetration Testing", "confidence_score": 0.90},
            {"esco_id": "http://data.europa.eu/esco/skill/c1d2e3f4-5a6b-4c7d-f064-b0c1d2e3f4a5", "label": "SIEM Tools", "confidence_score": 0.85},
            {"esco_id": "http://data.europa.eu/esco/skill/d2e3f4a5-6b7c-4d8e-a175-c1d2e3f4a5b6", "label": "Vulnerability Assessment", "confidence_score": 0.88},
        ],
        "soft_skills": [
            {"esco_id": "http://data.europa.eu/esco/skill/s008", "label": "Critical Thinking", "confidence_score": 0.92},
            {"esco_id": "http://data.europa.eu/esco/skill/s009", "label": "Ethical Judgement", "confidence_score": 0.90},
        ],
        "experience_years": 4,
        "source_type": "form",
        "is_synthetic": True,
    },
    # ── AI Ethics / Governance Track ───────────────────────────────────────
    {
        "hard_skills": [
            {"esco_id": "http://data.europa.eu/esco/skill/e3f4a5b6-7c8d-4e9f-b286-d2e3f4a5b6c7", "label": "AI Ethics Frameworks", "confidence_score": 0.88},
            {"esco_id": "http://data.europa.eu/esco/skill/f4a5b6c7-8d9e-4f0a-c397-e3f4a5b6c7d8", "label": "Policy Analysis", "confidence_score": 0.85},
            {"esco_id": "http://data.europa.eu/esco/skill/a5b6c7d8-9e0f-4a1b-d4a8-f4a5b6c7d8e9", "label": "Risk Assessment", "confidence_score": 0.87},
        ],
        "soft_skills": [
            {"esco_id": "http://data.europa.eu/esco/skill/s010", "label": "Stakeholder Management", "confidence_score": 0.91},
            {"esco_id": "http://data.europa.eu/esco/skill/s008", "label": "Critical Thinking", "confidence_score": 0.93},
        ],
        "experience_years": 7,
        "source_type": "form",
        "is_synthetic": True,
    },
    # ── Cloud / DevOps Track ───────────────────────────────────────────────
    {
        "hard_skills": [
            {"esco_id": "http://data.europa.eu/esco/skill/b6c7d8e9-0f1a-4b2c-e5b9-a5b6c7d8e9f0", "label": "Kubernetes", "confidence_score": 0.92},
            {"esco_id": "http://data.europa.eu/esco/skill/f8a9b0c1-2d3e-4f4a-cd31-e7f8a9b0c1d2", "label": "Docker", "confidence_score": 0.95},
            {"esco_id": "http://data.europa.eu/esco/skill/c7d8e9f0-1a2b-4c3d-f6ca-b6c7d8e9f0a1", "label": "AWS Cloud Services", "confidence_score": 0.90},
            {"esco_id": "http://data.europa.eu/esco/skill/d8e9f0a1-2b3c-4d4e-a7db-c7d8e9f0a1b2", "label": "CI/CD Pipeline", "confidence_score": 0.88},
            {"esco_id": "http://data.europa.eu/esco/skill/e9f0a1b2-3c4d-4e5f-b8ec-d8e9f0a1b2c3", "label": "Infrastructure as Code", "confidence_score": 0.85},
        ],
        "soft_skills": [
            {"esco_id": "http://data.europa.eu/esco/skill/s011", "label": "Adaptability", "confidence_score": 0.88},
        ],
        "experience_years": 5,
        "source_type": "form",
        "is_synthetic": True,
    },
    # ── Business Intelligence Track ────────────────────────────────────────
    {
        "hard_skills": [
            {"esco_id": "http://data.europa.eu/esco/skill/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d", "label": "Data Visualisation", "confidence_score": 0.95},
            {"esco_id": "http://data.europa.eu/esco/skill/f0a1b2c3-4d5e-4f6a-c9fd-e9f0a1b2c3d4", "label": "Power BI", "confidence_score": 0.92},
            {"esco_id": "http://data.europa.eu/esco/skill/e5f6a7b8-9c0d-4e3f-b042-c3d4e5f6a7b8", "label": "SQL", "confidence_score": 0.90},
            {"esco_id": "http://data.europa.eu/esco/skill/a1b2c3d4-5e6f-4a7b-8c9d-f0a1b2c3d4e5", "label": "Business Process Analysis", "confidence_score": 0.87},
        ],
        "soft_skills": [
            {"esco_id": "http://data.europa.eu/esco/skill/s012", "label": "Data Storytelling", "confidence_score": 0.91},
            {"esco_id": "http://data.europa.eu/esco/skill/s002", "label": "Communication", "confidence_score": 0.88},
        ],
        "experience_years": 3,
        "source_type": "form",
        "is_synthetic": True,
    },
    # ── Fresh Graduate Track (Low Experience) ─────────────────────────────
    {
        "hard_skills": [
            {"esco_id": "http://data.europa.eu/esco/skill/b6b3f3b1-5a3a-4b6d-8f2e-1a2b3c4d5e6f", "label": "Python", "confidence_score": 0.80},
            {"esco_id": "http://data.europa.eu/esco/skill/e5f6a7b8-9c0d-4e3f-b042-c3d4e5f6a7b8", "label": "SQL", "confidence_score": 0.75},
            {"esco_id": "http://data.europa.eu/esco/skill/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d", "label": "Data Visualisation", "confidence_score": 0.70},
        ],
        "soft_skills": [
            {"esco_id": "http://data.europa.eu/esco/skill/s006", "label": "Teamwork", "confidence_score": 0.85},
            {"esco_id": "http://data.europa.eu/esco/skill/s013", "label": "Willingness to Learn", "confidence_score": 0.95},
        ],
        "experience_years": 0,
        "source_type": "form",
        "is_synthetic": True,
    },
    # ── Senior Manager Track ───────────────────────────────────────────────
    {
        "hard_skills": [
            {"esco_id": "http://data.europa.eu/esco/skill/b1c2d3e4-5f6a-4b7c-8d9e-a1b2c3d4e5f6", "label": "Project Management", "confidence_score": 0.97},
            {"esco_id": "http://data.europa.eu/esco/skill/c2d3e4f5-6a7b-4c8d-9e0f-b2c3d4e5f6a7", "label": "Agile Methodology", "confidence_score": 0.93},
            {"esco_id": "http://data.europa.eu/esco/skill/d3e4f5a6-7b8c-4d9e-0f1a-c3d4e5f6a7b8", "label": "Budget Management", "confidence_score": 0.90},
            {"esco_id": "http://data.europa.eu/esco/skill/e4f5a6b7-8c9d-4e0f-1a2b-d3e4f5a6b7c8", "label": "Strategic Planning", "confidence_score": 0.88},
        ],
        "soft_skills": [
            {"esco_id": "http://data.europa.eu/esco/skill/s010", "label": "Stakeholder Management", "confidence_score": 0.96},
            {"esco_id": "http://data.europa.eu/esco/skill/s014", "label": "Leadership", "confidence_score": 0.94},
            {"esco_id": "http://data.europa.eu/esco/skill/s002", "label": "Communication", "confidence_score": 0.92},
        ],
        "experience_years": 12,
        "source_type": "form",
        "is_synthetic": True,
    },
    # ── Healthcare + AI Track ──────────────────────────────────────────────
    {
        "hard_skills": [
            {"esco_id": "http://data.europa.eu/esco/skill/f5a6b7c8-9d0e-4f1a-2b3c-e4f5a6b7c8d9", "label": "Medical Data Analysis", "confidence_score": 0.89},
            {"esco_id": "http://data.europa.eu/esco/skill/b6b3f3b1-5a3a-4b6d-8f2e-1a2b3c4d5e6f", "label": "Python", "confidence_score": 0.82},
            {"esco_id": "http://data.europa.eu/esco/skill/c7d8e9f0-1a2b-4c3d-9e4f-d4e5f6a7b8c9", "label": "Deep Learning", "confidence_score": 0.80},
            {"esco_id": "http://data.europa.eu/esco/skill/a6b7c8d9-0e1f-4a2b-3c4d-f5a6b7c8d9e0", "label": "DICOM / Medical Imaging", "confidence_score": 0.85},
        ],
        "soft_skills": [
            {"esco_id": "http://data.europa.eu/esco/skill/s009", "label": "Ethical Judgement", "confidence_score": 0.94},
            {"esco_id": "http://data.europa.eu/esco/skill/s001", "label": "Analytical Thinking", "confidence_score": 0.91},
        ],
        "experience_years": 6,
        "source_type": "form",
        "is_synthetic": True,
    },
    # ── Fintech Track ──────────────────────────────────────────────────────
    {
        "hard_skills": [
            {"esco_id": "http://data.europa.eu/esco/skill/b7c8d9e0-1f2a-4b3c-4d5e-a6b7c8d9e0f1", "label": "Blockchain Technology", "confidence_score": 0.88},
            {"esco_id": "http://data.europa.eu/esco/skill/c8d9e0f1-2a3b-4c4d-5e6f-b7c8d9e0f1a2", "label": "Smart Contracts", "confidence_score": 0.85},
            {"esco_id": "http://data.europa.eu/esco/skill/b6b3f3b1-5a3a-4b6d-8f2e-1a2b3c4d5e6f", "label": "Python", "confidence_score": 0.90},
            {"esco_id": "http://data.europa.eu/esco/skill/d9e0f1a2-3b4c-4d5e-6f7a-c8d9e0f1a2b3", "label": "Risk Modelling", "confidence_score": 0.83},
        ],
        "soft_skills": [
            {"esco_id": "http://data.europa.eu/esco/skill/s015", "label": "Regulatory Compliance Awareness", "confidence_score": 0.89},
        ],
        "experience_years": 4,
        "source_type": "form",
        "is_synthetic": True,
    },
    # ── UX / Product Design Track ──────────────────────────────────────────
    {
        "hard_skills": [
            {"esco_id": "http://data.europa.eu/esco/skill/e0f1a2b3-4c5d-4e6f-7a8b-d9e0f1a2b3c4", "label": "User Experience Design", "confidence_score": 0.95},
            {"esco_id": "http://data.europa.eu/esco/skill/f1a2b3c4-5d6e-4f7a-8b9c-e0f1a2b3c4d5", "label": "Figma", "confidence_score": 0.93},
            {"esco_id": "http://data.europa.eu/esco/skill/a2b3c4d5-6e7f-4a8b-9c0d-f1a2b3c4d5e6", "label": "User Research", "confidence_score": 0.90},
            {"esco_id": "http://data.europa.eu/esco/skill/b3c4d5e6-7f8a-4b9c-0d1e-a2b3c4d5e6f7", "label": "Prototyping", "confidence_score": 0.88},
        ],
        "soft_skills": [
            {"esco_id": "http://data.europa.eu/esco/skill/s016", "label": "Empathy", "confidence_score": 0.93},
            {"esco_id": "http://data.europa.eu/esco/skill/s004", "label": "Problem Solving", "confidence_score": 0.90},
        ],
        "experience_years": 3,
        "source_type": "form",
        "is_synthetic": True,
    },
]


def main():
    print("=" * 60)
    print("Synthetic Profile Seeder => telos_sdc.user_profiles")
    print(f"Profiles to seed: {len(PROFILES)}")
    print("NOTE: vectors left NULL (Person B fills after RunPod is live)")
    print("=" * 60)

    result = (
        supabase
        .schema("telos_sdc")
        .table("user_profiles")
        .insert(PROFILES)   # INSERT not upsert (no unique key to conflict on)
        .execute()
    )

    count = len(result.data) if result.data else 0
    print(f"\nInserted: {count} synthetic profiles")
    print("=" * 60)
    print("\nNEXT: Person B fills user_dense_vector + user_sparse_vector")
    print("      after RunPod BGE-M3 /embed endpoint is live (Substep 1.4)")


if __name__ == "__main__":
    main()
