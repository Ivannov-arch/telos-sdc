"""
game_matcher.py — F04 Role Matching from game session (no BGE-M3 vectors required)
Feature 04 — Future Skills Radar & Role Matching

Matching uses 3 inputs combined:
  1. Profile (stated skills + interests from Quick Skill Profile)
  2. Game evidence (4 indicator scores from behavioral evaluator)
  3. Role skill requirements (static config for the 3 MVP roles)

This is a lightweight, demo-ready matcher that does NOT require vector embeddings.
It produces explainable, auditable scores from deterministic rules.

The 3 MVP roles and their indicator weights:
  AI Application Engineer    → Decision Quality (40%) + Adaptability (30%) + profile (30%)
  Data Analyst               → Critical Verification (40%) + Decision Quality (30%) + profile (30%)
  AI Governance/Risk Analyst → Calibrated AI Trust (40%) + Critical Verification (30%) + profile (30%)
"""

from __future__ import annotations

from typing import Any

# ── Role Definitions ───────────────────────────────────────────────────────────

MVP_ROLES = [
    {
        "id": "ai_application_engineer",
        "title": "AI Application Engineer",
        "esco_id": "esco:2513",
        "description": "Designs and develops AI-integrated applications and systems.",
        "skill_focus": ["Application development", "AI integration", "System testing"],
        # Which behavioral indicators matter most for this role (sum to 1.0)
        "indicator_weights": {
            "decision_quality": 0.40,
            "adaptability": 0.30,
            "critical_verification": 0.15,
            "calibrated_ai_trust": 0.15,
        },
        # Which mission choice biases toward this role
        "mission_affinity": {"A": 0.05, "B": 0.00, "C": 0.10},
        # Which stated interests map to this role
        "interest_keywords": [
            "software", "development", "engineering", "application", "ai", "tech",
            "programming", "infrastructure", "systems",
        ],
        # Which stated skills map to this role
        "skill_keywords": [
            "python", "programming", "development", "software", "api", "testing",
            "integration", "machine learning", "cloud",
        ],
        # Skill gaps to surface (role requirements the player likely lacks)
        "skill_gaps_template": [
            {"skill": "AI System Integration", "urgency": "high", "type": "core"},
            {"skill": "Model Deployment & MLOps", "urgency": "high", "type": "core"},
            {"skill": "API Design & Testing", "urgency": "medium", "type": "core"},
            {"skill": "Cloud Infrastructure (AWS/GCP/Azure)", "urgency": "medium", "type": "supporting"},
            {"skill": "Responsible AI Principles", "urgency": "low", "type": "supporting"},
        ],
        "sdg_goals": [
            {
                "sdg_goal": 9,
                "sdg_name": "Industry, Innovation and Infrastructure",
                "impact_reasoning": "Builds AI-integrated systems that drive industrial innovation and modern infrastructure.",
                "source": "UNSD SDG API",
            },
            {
                "sdg_goal": 4,
                "sdg_name": "Quality Education",
                "impact_reasoning": "AI applications increasingly power adaptive learning and educational access tools.",
                "source": "UNSD SDG API",
            },
        ],
    },
    {
        "id": "data_analyst",
        "title": "Data Analyst",
        "esco_id": "esco:2521",
        "description": "Collects, processes, and performs statistical analyses of data.",
        "skill_focus": ["Data analysis", "Interpretation", "Conclusion verification"],
        "indicator_weights": {
            "critical_verification": 0.40,
            "decision_quality": 0.30,
            "calibrated_ai_trust": 0.20,
            "adaptability": 0.10,
        },
        "mission_affinity": {"A": 0.05, "B": 0.10, "C": 0.05},
        "interest_keywords": [
            "data", "analytics", "statistics", "research", "insights", "reporting",
            "visualization", "business intelligence",
        ],
        "skill_keywords": [
            "data analysis", "sql", "excel", "statistics", "python", "data",
            "visualization", "tableau", "powerbi", "research",
        ],
        "skill_gaps_template": [
            {"skill": "Statistical Analysis & Hypothesis Testing", "urgency": "high", "type": "core"},
            {"skill": "Data Visualization (Tableau / Power BI)", "urgency": "high", "type": "core"},
            {"skill": "SQL & Database Querying", "urgency": "medium", "type": "core"},
            {"skill": "Python for Data Analysis (pandas, numpy)", "urgency": "medium", "type": "supporting"},
            {"skill": "AI Output Verification & Bias Detection", "urgency": "medium", "type": "supporting"},
        ],
        "sdg_goals": [
            {
                "sdg_goal": 17,
                "sdg_name": "Partnerships for the Goals",
                "impact_reasoning": "Data analysts enable evidence-based policymaking and cross-sector collaboration toward SDG targets.",
                "source": "UNSD SDG API",
            },
            {
                "sdg_goal": 8,
                "sdg_name": "Decent Work and Economic Growth",
                "impact_reasoning": "Labour market data analysis informs workforce planning and economic development decisions.",
                "source": "UNSD SDG API",
            },
        ],
    },
    {
        "id": "ai_governance_risk_analyst",
        "title": "AI Governance / Risk Analyst",
        "esco_id": "esco:2631",
        "description": "Evaluates risks of AI systems, ensures regulatory compliance, and audits algorithmic fairness.",
        "skill_focus": ["Risk assessment", "Evidence evaluation", "System impact review"],
        "indicator_weights": {
            "calibrated_ai_trust": 0.40,
            "critical_verification": 0.30,
            "decision_quality": 0.20,
            "adaptability": 0.10,
        },
        "mission_affinity": {"A": 0.00, "B": 0.15, "C": 0.05},
        "interest_keywords": [
            "ethics", "governance", "policy", "risk", "compliance", "regulation",
            "fairness", "auditing", "accountability", "law", "public policy",
        ],
        "skill_keywords": [
            "risk", "ethics", "compliance", "regulation", "audit", "policy",
            "critical thinking", "analysis", "law", "governance",
        ],
        "skill_gaps_template": [
            {"skill": "Regulatory Frameworks (EU AI Act, ISO 42001)", "urgency": "high", "type": "core"},
            {"skill": "Algorithmic Bias Testing & Auditing", "urgency": "high", "type": "core"},
            {"skill": "AI Risk Assessment Methodologies", "urgency": "medium", "type": "core"},
            {"skill": "Data Governance & Privacy Law (GDPR)", "urgency": "medium", "type": "supporting"},
            {"skill": "Stakeholder Communication & Policy Writing", "urgency": "low", "type": "supporting"},
        ],
        "sdg_goals": [
            {
                "sdg_goal": 10,
                "sdg_name": "Reduced Inequalities",
                "impact_reasoning": "Algorithmic bias auditing directly reduces AI-driven discrimination in credit, hiring, and public services.",
                "source": "UNSD SDG API",
            },
            {
                "sdg_goal": 16,
                "sdg_name": "Peace, Justice and Strong Institutions",
                "impact_reasoning": "AI governance ensures accountable, transparent, and fair automated decision-making in public institutions.",
                "source": "UNSD SDG API",
            },
        ],
    },
]

MISSION_LABEL = {
    "A": "Mission A — Food Supply Chain (SDG 2: Zero Hunger)",
    "B": "Mission B — Credit Algorithm Bias (SDG 10: Reduced Inequalities)",
    "C": "Mission C — Grid Failure (SDG 7: Affordable & Clean Energy)",
}

# ── Scoring Logic ──────────────────────────────────────────────────────────────


def _indicator_score(indicators: dict, key: str) -> float:
    """Convert indicator boolean to 0.0 or 1.0. None/missing = 0.5 (neutral)."""
    ind = indicators.get(key)
    if not isinstance(ind, dict):
        return 0.5
    val = ind.get("observed") if "observed" in ind else ind.get("met_objectives")
    if val is True:
        return 1.0
    if val is False:
        return 0.0
    return 0.5  # insufficient evidence


def _profile_score(role: dict, profile: dict) -> float:
    """Score profile match based on keyword overlap between stated skills/interests and role keywords."""
    stated_skills = [s.lower() for s in (profile.get("skills") or [])]
    stated_interests = [i.lower() for i in (profile.get("interests") or [])]
    combined = stated_skills + stated_interests

    skill_kw = role["skill_keywords"]
    interest_kw = role["interest_keywords"]
    all_kw = skill_kw + interest_kw

    if not all_kw:
        return 0.5

    hits = sum(
        1 for kw in all_kw
        if any(kw in token for token in combined)
    )
    return min(1.0, hits / max(len(all_kw) * 0.4, 1))  # normalize — 40% hit = full score


def _filter_skill_gaps(role: dict, profile: dict) -> list[dict]:
    """
    Remove skill gaps the player has already stated they possess.
    Returns gaps with esco_id filled from template (no DB call needed for MVP).
    """
    stated_lower = {s.lower() for s in (profile.get("skills") or [])}
    gaps = []
    for gap in role["skill_gaps_template"]:
        skill_lower = gap["skill"].lower()
        # Simple keyword match — if any word in the skill name matches stated skills, skip
        already_has = any(
            word in stated_lower
            for word in skill_lower.split()
            if len(word) > 3
        )
        if not already_has:
            gaps.append({
                "skill": gap["skill"],
                "esco_id": f"{role['esco_id']}/gap/{gap['skill'].lower().replace(' ', '_')}",
                "type": gap["type"],
                "urgency": gap["urgency"],
            })
    return gaps[:5]  # cap at 5 gaps for readability


def match_from_session(session: dict, indicators: dict) -> list[dict]:
    """
    Compute role matches from a completed game session.

    Returns a ranked list of role match objects ready for the API response.
    """
    profile = session.get("profile") or {}
    mission_id = session.get("mission_id", "A")

    results = []
    for role in MVP_ROLES:
        # ── Behavioral score (60% of total) ───────────────────────────────────
        behavioral_score = sum(
            weight * _indicator_score(indicators, key)
            for key, weight in role["indicator_weights"].items()
        )

        # ── Profile score (30% of total) ──────────────────────────────────────
        profile_score = _profile_score(role, profile)

        # ── Mission affinity bonus (10% of total) ─────────────────────────────
        mission_bonus = role["mission_affinity"].get(mission_id, 0.0)

        # ── Final match score ─────────────────────────────────────────────────
        final_score = (0.60 * behavioral_score) + (0.30 * profile_score) + (0.10 * (1.0 + mission_bonus))
        final_score = round(min(0.99, max(0.30, final_score)), 3)

        # ── Skill gaps ────────────────────────────────────────────────────────
        gaps = _filter_skill_gaps(role, profile)

        # ── Mission contribution note ─────────────────────────────────────────
        affinity = role["mission_affinity"].get(mission_id, 0)
        if affinity > 0:
            mission_note = (
                f"{MISSION_LABEL[mission_id]} directly relates to the core challenges of this role."
            )
        else:
            mission_note = (
                f"Your behavioral evidence from {MISSION_LABEL[mission_id]} was evaluated against this role's requirements."
            )

        # ── Build reasoning ───────────────────────────────────────────────────
        top_indicator = max(
            role["indicator_weights"].items(),
            key=lambda kv: kv[1] * _indicator_score(indicators, kv[0])
        )
        top_key = top_indicator[0].replace("_", " ").title()
        top_observed = _indicator_score(indicators, top_indicator[0]) >= 0.5

        if top_observed:
            reasoning = (
                f"Your observed {top_key} behaviour aligns with this role's primary requirement. "
                f"{mission_note}"
            )
        else:
            reasoning = (
                f"This role requires strong {top_key}. Your simulation showed room to develop this further. "
                f"{mission_note}"
            )

        results.append({
            "rank": 0,  # filled after sorting
            "id": role["id"],
            "title": role["title"],
            "esco_id": role["esco_id"],
            "description": role["description"],
            "match_score": final_score,
            "reasoning": reasoning,
            "skills_possessed": [
                s for s in (profile.get("skills") or [])
                if any(kw in s.lower() for kw in role["skill_keywords"])
            ][:5],
            "skill_gaps": gaps,
            "mission_contribution": mission_note,
            "sdg_alignment": role["sdg_goals"],
            "score_breakdown": {
                "behavioral_score": round(behavioral_score, 3),
                "profile_score": round(profile_score, 3),
                "mission_bonus": round(mission_bonus, 3),
            },
        })

    # Sort by match score descending, assign ranks
    results.sort(key=lambda r: r["match_score"], reverse=True)
    for i, r in enumerate(results):
        r["rank"] = i + 1

    return results
