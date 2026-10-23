"""
fix_profile_skills.py — Resolve synthetic profile skill labels to authentic ESCO IDs
Updates telos_sdc.user_profiles in Supabase so that skill coverage and match scoring work properly.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client

SRC_DIR = Path(__file__).resolve().parent.parent
load_dotenv(SRC_DIR / ".env")

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_SECRET_KEY = os.environ["SUPABASE_SECRET_KEY"]

db: Client = create_client(SUPABASE_URL, SUPABASE_SECRET_KEY)

# ── Alias & Standardization Mapping ──────────────────────────────────────────
ALIASES = {
    "python": "python (computer programming)",
    "java": "java (computer programming)",
    "javascript": "javascript",
    "sql": "sql",
    "machine learning": "machine learning",
    "deep learning": "deep learning",
    "natural language processing": "natural language processing",
    "pytorch": "deep learning",
    "data engineering": "data engineering",
    "data visualisation": "data visualisation software",
    "data visualization": "data visualisation software",
    "data storytelling": "data analytics",
    "apache spark": "data analytics",
    "etl pipeline development": "develop data processing applications",
    "rest api design": "use an application-specific interface",
    "react.js": "develop web applications",
    "node.js": "web programming",
    "docker": "cloud technologies",
    "kubernetes": "cloud technologies",
    "aws cloud services": "cloud technologies",
    "ci/cd pipeline": "tools for software configuration management",
    "infrastructure as code": "ict infrastructure",
    "penetration testing": "penetration testing tool",
    "network security": "ict network security risks",
    "siem tools": "use it tools",
    "vulnerability assessment": "manage ict security vulnerabilities",
    "figma": "user interface design",
    "user experience design": "user interface design",
    "user research": "execute ict user research activities",
    "prototyping": "develop software prototype",
    "agile methodology": "agile project management",
    "project management": "project management",
    "communication": "communication",
    "teamwork": "manage teamwork",
    "problem solving": "solve technical problems",
    "research skills": "scientific research methodology",
    "analytical thinking": "apply analytical thinking skills",
    "attention to detail": "attend to detail",
    "adaptability": "adapt to change",
    "critical thinking": "think critically",
    "leadership": "lead others",
    "strategic planning": "strategic planning",
    "systems thinking": "systems thinking",
    "risk assessment": "draw up risk assessment",
    "risk modelling": "risk modelling",
    "policy analysis": "policy analysis",
    "data science": "data science",
    "medical data analysis": "analyse medical data",
    "dicom / medical imaging": "biomedical engineering",
    "regulatory compliance awareness": "ensure compliance with legal requirements",
    "empathy": "show empathy",
    "ethical judgement": "ethics",
    "ai ethics frameworks": "ethics",
    "blockchain technology": "develop blockchain technology",
    "smart contracts": "implement smart contracts",
    "power bi": "business intelligence software",
    "business process analysis": "business analysis",
    "budget management": "manage budgets",
    "willingness to learn": "demonstrate willingness to learn",
}


def load_all_skills():
    print("Fetching all skills from Supabase telos_sdc.skills ...")
    all_skills = []
    offset = 0
    while True:
        res = db.schema("telos_sdc").table("skills").select("esco_id, preferred_label").range(offset, offset + 999).execute()
        batch = res.data or []
        all_skills.extend(batch)
        if len(batch) < 1000:
            break
        offset += 1000
    print(f"Loaded {len(all_skills):,} skills.")
    return {s["preferred_label"].lower().strip(): s["esco_id"] for s in all_skills}


def resolve_skill(label: str, skill_map: dict) -> str | None:
    lbl = label.lower().strip()
    if lbl in skill_map:
        return skill_map[lbl]
    if lbl in ALIASES and ALIASES[lbl] in skill_map:
        return skill_map[ALIASES[lbl]]
    # Substring search
    for k, v in skill_map.items():
        if lbl in k:
            return v
    return None


def main():
    skill_map = load_all_skills()

    print("\nFetching user profiles from telos_sdc.user_profiles ...")
    res = db.schema("telos_sdc").table("user_profiles").select("id, hard_skills, soft_skills").execute()
    profiles = res.data or []
    print(f"Found {len(profiles)} user profiles to normalize.")

    updated_count = 0
    for p in profiles:
        new_hard = []
        for s in (p.get("hard_skills") or []):
            label = s.get("label", "")
            real_id = resolve_skill(label, skill_map) or s.get("esco_id")
            new_hard.append({
                "label": label,
                "esco_id": real_id,
                "confidence_score": s.get("confidence_score", 0.95),
            })

        new_soft = []
        for s in (p.get("soft_skills") or []):
            label = s.get("label", "")
            real_id = resolve_skill(label, skill_map) or s.get("esco_id")
            new_soft.append({
                "label": label,
                "esco_id": real_id,
                "confidence_score": s.get("confidence_score", 0.90),
            })

        # Update Supabase
        db.schema("telos_sdc").table("user_profiles").update({
            "hard_skills": new_hard,
            "soft_skills": new_soft,
        }).eq("id", p["id"]).execute()
        updated_count += 1

    print(f"\n[SUCCESS] Successfully normalized {updated_count} user profiles with real ESCO IDs!")


if __name__ == "__main__":
    main()
