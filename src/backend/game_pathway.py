"""
game_pathway.py — F05 Future Career Pathway
Feature 05 — Career Pathway + SDG Mapping + Moderate vs Rapid Scenario

Builds a sequential reskilling path from skill gaps identified in F04.
Two scenarios: Moderate (core gaps first) vs Rapid (soft/judgment skills up-ranked).

No LLM call — entirely deterministic parameter-switching.
All outputs labeled as estimates, not predictions.
"""

from __future__ import annotations

# ── Learning Sources ───────────────────────────────────────────────────────────
# HUMAN INTERVENTION: Verify all URLs are live and publicly accessible before demo.

LEARNING_SOURCES: dict[str, list[dict]] = {
    "Regulatory Frameworks (EU AI Act, ISO 42001)": [
        {
            "title": "EU AI Act — Official Text (European Commission)",
            "url": "https://artificialintelligenceact.eu/",
            "type": "official_doc",
        },
        {
            "title": "ISO/IEC 42001 AI Management System — Overview",
            "url": "https://www.iso.org/standard/81230.html",
            "type": "standard",
        },
    ],
    "Algorithmic Bias Testing & Auditing": [
        {
            "title": "Responsible AI Practices — Google AI",
            "url": "https://ai.google/responsibility/responsible-ai-practices/",
            "type": "guide",
        },
        {
            "title": "AI Fairness 360 — IBM Open Source Toolkit",
            "url": "https://aif360.res.ibm.com/",
            "type": "tool",
        },
    ],
    "AI Risk Assessment Methodologies": [
        {
            "title": "NIST AI Risk Management Framework (AI RMF 1.0)",
            "url": "https://airc.nist.gov/RMF/about",
            "type": "framework",
        },
        {
            "title": "AI Risk Management — Coursera (DeepLearning.AI)",
            "url": "https://www.coursera.org/learn/ai-risk-management",
            "type": "course",
        },
    ],
    "Data Governance & Privacy Law (GDPR)": [
        {
            "title": "GDPR Official Regulation — EUR-Lex",
            "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32016R0679",
            "type": "official_doc",
        },
        {
            "title": "Data Privacy Fundamentals — Coursera (University of Michigan)",
            "url": "https://www.coursera.org/learn/data-privacy-fundamentals",
            "type": "course",
        },
    ],
    "Stakeholder Communication & Policy Writing": [
        {
            "title": "Technical Communication — edX (MIT OpenCourseWare)",
            "url": "https://ocw.mit.edu/courses/21g-225-writing-and-communication-center/",
            "type": "course",
        },
    ],
    "Statistical Analysis & Hypothesis Testing": [
        {
            "title": "Statistics and R — edX (Harvard University)",
            "url": "https://www.edx.org/course/statistics-and-r",
            "type": "course",
        },
        {
            "title": "Inferential Statistics — Coursera (Duke University)",
            "url": "https://www.coursera.org/learn/inferential-statistics-intro",
            "type": "course",
        },
    ],
    "Data Visualization (Tableau / Power BI)": [
        {
            "title": "Data Visualization with Tableau — Coursera (UC Davis)",
            "url": "https://www.coursera.org/specializations/data-visualization",
            "type": "course",
        },
        {
            "title": "Microsoft Power BI — Microsoft Learn (Free)",
            "url": "https://learn.microsoft.com/en-us/training/powerplatform/power-bi",
            "type": "course",
        },
    ],
    "SQL & Database Querying": [
        {
            "title": "SQL for Data Science — Coursera (UC Davis)",
            "url": "https://www.coursera.org/learn/sql-for-data-science",
            "type": "course",
        },
    ],
    "Python for Data Analysis (pandas, numpy)": [
        {
            "title": "Python for Data Analysis — Real Python",
            "url": "https://realpython.com/pandas-dataframe/",
            "type": "guide",
        },
        {
            "title": "Data Analysis with Python — freeCodeCamp",
            "url": "https://www.freecodecamp.org/learn/data-analysis-with-python/",
            "type": "course",
        },
    ],
    "AI Output Verification & Bias Detection": [
        {
            "title": "Evaluating and Debugging Generative AI — DeepLearning.AI",
            "url": "https://www.deeplearning.ai/short-courses/evaluating-debugging-generative-ai/",
            "type": "course",
        },
    ],
    "AI System Integration": [
        {
            "title": "Building AI Products — Coursera (DeepLearning.AI)",
            "url": "https://www.coursera.org/specializations/ai-for-everyone",
            "type": "course",
        },
    ],
    "Model Deployment & MLOps": [
        {
            "title": "MLOps Specialization — Coursera (DeepLearning.AI)",
            "url": "https://www.coursera.org/specializations/machine-learning-engineering-for-production-mlops",
            "type": "course",
        },
    ],
    "API Design & Testing": [
        {
            "title": "REST API Design Best Practices — freeCodeCamp",
            "url": "https://www.freecodecamp.org/news/rest-api-best-practices-rest-endpoint-design-examples/",
            "type": "guide",
        },
    ],
    "Cloud Infrastructure (AWS/GCP/Azure)": [
        {
            "title": "Google Cloud Skills Boost — Free Tier",
            "url": "https://cloudskillsboost.google/",
            "type": "course",
        },
        {
            "title": "AWS Skill Builder — Free Digital Training",
            "url": "https://skillbuilder.aws/",
            "type": "course",
        },
    ],
    "Responsible AI Principles": [
        {
            "title": "Responsible AI for Developers — Google",
            "url": "https://ai.google/responsibility/responsible-ai-practices/",
            "type": "guide",
        },
        {
            "title": "Ethics of AI — University of Helsinki (Free)",
            "url": "https://ethics-of-ai.mooc.fi/",
            "type": "course",
        },
    ],
}

# ── SDG Step Mapping ───────────────────────────────────────────────────────────
# Maps skill → SDG goal that the skill supports

SKILL_SDG_MAP: dict[str, dict] = {
    "Regulatory Frameworks (EU AI Act, ISO 42001)": {
        "sdg_goal": 16,
        "sdg_name": "Peace, Justice and Strong Institutions",
        "rationale": "Understanding AI regulation supports accountable, transparent governance of automated systems.",
    },
    "Algorithmic Bias Testing & Auditing": {
        "sdg_goal": 10,
        "sdg_name": "Reduced Inequalities",
        "rationale": "Detecting and removing algorithmic bias directly reduces AI-driven discrimination.",
    },
    "AI Risk Assessment Methodologies": {
        "sdg_goal": 16,
        "sdg_name": "Peace, Justice and Strong Institutions",
        "rationale": "Systematic AI risk assessment supports safe and accountable deployment of automated systems.",
    },
    "Data Governance & Privacy Law (GDPR)": {
        "sdg_goal": 16,
        "sdg_name": "Peace, Justice and Strong Institutions",
        "rationale": "Data privacy law protects individuals from unauthorized use of their data by automated systems.",
    },
    "Statistical Analysis & Hypothesis Testing": {
        "sdg_goal": 17,
        "sdg_name": "Partnerships for the Goals",
        "rationale": "Evidence-based analysis underpins credible data sharing and monitoring of SDG indicators.",
    },
    "AI Output Verification & Bias Detection": {
        "sdg_goal": 10,
        "sdg_name": "Reduced Inequalities",
        "rationale": "Verifying AI outputs for bias prevents automated systems from reinforcing existing inequalities.",
    },
    "Python for Data Analysis (pandas, numpy)": {
        "sdg_goal": 4,
        "sdg_name": "Quality Education",
        "rationale": "Programming literacy for data analysis is a core 21st-century skill enabling lifelong learning.",
    },
    "Model Deployment & MLOps": {
        "sdg_goal": 9,
        "sdg_name": "Industry, Innovation and Infrastructure",
        "rationale": "Reliable AI deployment infrastructure is foundational to responsible industrial innovation.",
    },
    "AI System Integration": {
        "sdg_goal": 9,
        "sdg_name": "Industry, Innovation and Infrastructure",
        "rationale": "Integrating AI into existing systems drives inclusive innovation in public and private sectors.",
    },
    "Responsible AI Principles": {
        "sdg_goal": 10,
        "sdg_name": "Reduced Inequalities",
        "rationale": "Embedding responsible AI practices ensures technology development does not widen inequality gaps.",
    },
}

# ── Scenario Skill Reranking ───────────────────────────────────────────────────

# Skills that are UP-RANKED under Rapid AI adoption (judgment, soft, governance)
RAPID_PRIORITY_SKILLS = {
    "Algorithmic Bias Testing & Auditing",
    "AI Risk Assessment Methodologies",
    "Regulatory Frameworks (EU AI Act, ISO 42001)",
    "Responsible AI Principles",
    "Stakeholder Communication & Policy Writing",
    "Data Governance & Privacy Law (GDPR)",
    "AI Output Verification & Bias Detection",
}

# Skills that are DOWN-RANKED under Rapid AI adoption (more automatable)
RAPID_DEPRIORITIZED_SKILLS = {
    "SQL & Database Querying",
    "Python for Data Analysis (pandas, numpy)",
    "API Design & Testing",
}

# Time estimates (weeks) per skill by urgency
TIME_BY_URGENCY = {"high": 3, "medium": 2, "low": 1}


def build_pathway(
    role_id: str,
    skill_gaps: list[dict],
    scenario: str,
) -> dict:
    """
    Build a sequential reskilling pathway from skill gaps.

    Args:
        role_id: e.g. 'ai_governance_risk_analyst'
        skill_gaps: list of gap dicts from game_matcher (skill, urgency, type)
        scenario: 'moderate' | 'rapid'

    Returns:
        Pathway dict with ordered steps, time estimates, sources, SDG per step.
    """
    if scenario not in ("moderate", "rapid"):
        scenario = "moderate"

    # ── Rerank gaps by scenario ────────────────────────────────────────────────
    def _scenario_priority(gap: dict) -> tuple:
        skill = gap["skill"]
        urgency_order = {"high": 0, "medium": 1, "low": 2}
        base = urgency_order.get(gap.get("urgency", "low"), 2)

        if scenario == "rapid":
            if skill in RAPID_PRIORITY_SKILLS:
                return (base - 1, gap["type"] != "core")  # up-rank
            if skill in RAPID_DEPRIORITIZED_SKILLS:
                return (base + 1, gap["type"] != "core")  # down-rank

        return (base, gap["type"] != "core")

    sorted_gaps = sorted(skill_gaps, key=_scenario_priority)

    # ── Build steps ────────────────────────────────────────────────────────────
    steps = []
    total_weeks = 0
    for i, gap in enumerate(sorted_gaps, start=1):
        skill = gap["skill"]
        urgency = gap.get("urgency", "medium")
        time_weeks = TIME_BY_URGENCY.get(urgency, 2)

        if scenario == "rapid" and skill in RAPID_PRIORITY_SKILLS:
            time_weeks = max(1, time_weeks - 1)  # Rapid: slightly compressed timeline

        sources = LEARNING_SOURCES.get(skill, [])
        sdg = SKILL_SDG_MAP.get(skill)

        total_weeks += time_weeks

        steps.append({
            "step": i,
            "skill": skill,
            "urgency": urgency,
            "type": gap.get("type", "core"),
            "time_estimate_weeks": time_weeks,
            "sources": sources if sources else [
                {"title": f"Search: '{skill} course'", "url": f"https://www.coursera.org/search?query={skill.replace(' ', '+')}", "type": "search"}
            ],
            "sdg": sdg,
        })

    # ── Scenario note ──────────────────────────────────────────────────────────
    if scenario == "moderate":
        scenario_note = (
            "Under Moderate AI adoption, core technical gaps are prioritized. "
            "AI tools will augment your work rather than replace it — "
            "focus on depth in your primary skill area first."
        )
    else:
        scenario_note = (
            "Under Rapid AI adoption, governance, ethics, and judgment-intensive skills "
            "are the most resilient. Technical execution skills that AI can automate are "
            "de-prioritized. Lead with oversight and accountability skills."
        )

    return {
        "role_id": role_id,
        "scenario": scenario,
        "steps": steps,
        "total_estimated_weeks": total_weeks,
        "scenario_note": scenario_note,
        "estimate_disclaimer": (
            "These time estimates are indicative only and depend on your current baseline "
            "and learning pace. All outcomes are estimates, not predictions."
        ),
    }
