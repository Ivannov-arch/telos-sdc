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
    # Supply Chain & Logistics
    "Emergency Supply Chain Resilience & Routing": [
        {"title": "Supply Chain Resilience — MIT Center for Transportation & Logistics", "url": "https://ctl.mit.edu/research/supply-chain-resilience", "type": "research"},
        {"title": "Humanitarian Supply Chain Management — Coursera (Rutgers)", "url": "https://www.coursera.org/learn/supply-chain-logistics", "type": "course"},
    ],
    "Crisis Resource Allocation & Budgeting": [
        {"title": "Disaster Financial Management & Resource Planning — FEMA", "url": "https://www.fema.gov/emergency-managers/national-preparedness/plan", "type": "guide"},
        {"title": "Crisis Management & Operations Strategy — edX (Wharton)", "url": "https://www.edx.org/learn/business-administration", "type": "course"},
    ],
    "Humanitarian Logistics Standards (Sphere / UN)": [
        {"title": "The Sphere Handbook: Humanitarian Standards", "url": "https://www.spherestandards.org/handbook/", "type": "standard"},
        {"title": "Emergency Logistics Operations — UN World Food Programme", "url": "https://www.wfp.org/logistics", "type": "official_doc"},
    ],
    "Fleet & Multi-Modal Freight Optimization": [
        {"title": "Freight & Fleet Management Fundamentals — CILT", "url": "https://ciltinternational.org/", "type": "guide"},
        {"title": "Logistics & Transport Modelling — Coursera", "url": "https://www.coursera.org/learn/supply-chain-operations", "type": "course"},
    ],
    "Cross-Agency Stakeholder Coordination": [
        {"title": "Multi-Agency Incident Command System — FEMA NIMS", "url": "https://www.fema.gov/emergency-managers/nims", "type": "framework"},
        {"title": "Crisis Negotiation & Strategic Alignment — Harvard Kennedy School", "url": "https://www.hks.harvard.edu/", "type": "guide"},
    ],
    # Public Policy & Governance
    "Public Sector Algorithmic Governance": [
        {"title": "AI in the Public Sector — OECD AI Policy Observatory", "url": "https://oecd.ai/en/wonk/public-sector", "type": "framework"},
        {"title": "Civic AI & Algorithmic Accountability — Harvard Berkman Klein", "url": "https://cyber.harvard.edu/", "type": "guide"},
    ],
    "Equitable Policy Impact Assessment": [
        {"title": "Human Rights & Algorithmic Impact Assessment — Council of Europe", "url": "https://www.coe.int/en/web/artificial-intelligence", "type": "official_doc"},
        {"title": "Public Policy Analysis — London School of Economics", "url": "https://www.lse.ac.uk/study-at-lse/online-learning/courses/public-policy-analysis", "type": "course"},
    ],
    "Civic Data Ethics & Transparency": [
        {"title": "Open Government Partnership: Algorithmic Transparency", "url": "https://www.opengovpartnership.org/", "type": "guide"},
        {"title": "Data Ethics for Public Leaders — University of Michigan", "url": "https://www.coursera.org/learn/data-ethics", "type": "course"},
    ],
    "Public Consultation & Stakeholder Engagement": [
        {"title": "Public Participation Spectrum — IAP2 International", "url": "https://www.iap2.org/", "type": "standard"},
        {"title": "Deliberative Democracy & Civic Co-Design — OECD", "url": "https://www.oecd.org/gov/innovative-citizen-participation.htm", "type": "framework"},
    ],
    "Crisis Communication for Public Institutions": [
        {"title": "Crisis and Emergency Risk Communication (CERC) — CDC", "url": "https://emergency.cdc.gov/cerc/", "type": "framework"},
        {"title": "Strategic Communication in Government — edX", "url": "https://www.edx.org/learn/communication", "type": "course"},
    ],
    # Sustainable Finance & Risk
    "ESG Risk Scoring & Disclosure Standards": [
        {"title": "IFRS Sustainability Disclosure Standards (ISSB)", "url": "https://www.ifrs.org/issued-standards/sustainability-standards/", "type": "standard"},
        {"title": "Sustainable Finance & ESG Investing — Coursera (Erasmus University)", "url": "https://www.coursera.org/learn/sustainable-finance", "type": "course"},
    ],
    "Financial Model Validation & Bias Auditing": [
        {"title": "Supervisory Guidance on Model Risk Management (SR 11-7) — Federal Reserve", "url": "https://www.federalreserve.gov/supervisionreg/srletters/sr1107.htm", "type": "official_doc"},
        {"title": "Credit Risk Scoring & Algorithmic Fairness — Wharton", "url": "https://www.coursera.org/learn/wharton-credit-risk-management", "type": "course"},
    ],
    "Systemic Stress Testing Methodologies": [
        {"title": "Macroprudential Stress Testing Principles — IMF", "url": "https://www.imf.org/en/Publications/WP/Issues/2017/02/28/A-Guide-to-IMF-Stress-Testing-44673", "type": "guide"},
        {"title": "Financial Risk Management (FRM) Frameworks — GARP", "url": "https://www.garp.org/", "type": "framework"},
    ],
    "Sustainable Capital Allocation Frameworks": [
        {"title": "Principles for Responsible Investment (UN PRI)", "url": "https://www.unpri.org/", "type": "standard"},
        {"title": "Climate Finance & Green Bonds — World Bank Open Learning", "url": "https://olc.worldbank.org/", "type": "course"},
    ],
    "Regulatory Financial Compliance (Basel / TCFD)": [
        {"title": "Basel Committee on Banking Supervision Standards — BIS", "url": "https://www.bis.org/bcbs/", "type": "standard"},
        {"title": "Task Force on Climate-Related Financial Disclosures (TCFD)", "url": "https://www.fsb-tcfd.org/", "type": "official_doc"},
    ],
    # Climate Resilience & Energy
    "Climate Vulnerability Assessment & Scenario Modelling": [
        {"title": "IPCC Guidelines for Climate Vulnerability & Adaptation", "url": "https://www.ipcc.ch/", "type": "standard"},
        {"title": "Climate Change Adaptation — edX (World Bank)", "url": "https://www.edx.org/learn/climate-change", "type": "course"},
    ],
    "Renewable Energy Grid Integration & Storage": [
        {"title": "Grid Modernization & Renewable Integration — NREL", "url": "https://www.nrel.gov/grid/", "type": "guide"},
        {"title": "Electric Power Systems & Energy Transition — Coursera (University at Buffalo)", "url": "https://www.coursera.org/learn/electric-power-systems", "type": "course"},
    ],
    "Carbon Accounting & Greenhouse Gas Protocols": [
        {"title": "The Greenhouse Gas Protocol (GHG Protocol Corporate Standard)", "url": "https://ghgprotocol.org/", "type": "standard"},
        {"title": "Carbon Footprint Measurement — Coursera (University of Edinburgh)", "url": "https://www.coursera.org/learn/carbon-footprint", "type": "course"},
    ],
    "Environmental Disaster Preparedness Planning": [
        {"title": "Sendai Framework for Disaster Risk Reduction — UNDRR", "url": "https://www.undrr.org/implementing-sendai-framework", "type": "standard"},
        {"title": "Disaster Risk Reduction and Management — edX", "url": "https://www.edx.org/", "type": "course"},
    ],
    "Community Resilience Stakeholder Engagement": [
        {"title": "Community-Based Adaptation to Climate Change — IIED", "url": "https://www.iied.org/", "type": "guide"},
        {"title": "Inclusive Climate Action Planning — C40 Cities", "url": "https://www.c40.org/", "type": "framework"},
    ],
    # Healthcare Operations
    "Clinical Decision Support Systems (CDSS) Auditing": [
        {"title": "Artificial Intelligence in Healthcare — Stanford Medicine", "url": "https://online.stanford.edu/courses/som-ycoc0001-ai-healthcare-fundamentals", "type": "course"},
        {"title": "FDA Good Machine Learning Practice for Medical Device Development", "url": "https://www.fda.gov/medical-devices/software-and-mobile-medical-devices", "type": "official_doc"},
    ],
    "Hospital Operations & Surge Capacity Management": [
        {"title": "Hospital Emergency Response Checklist — WHO", "url": "https://www.who.int/publications/i/item/hospital-emergency-response-checklist", "type": "standard"},
        {"title": "Healthcare Operations Management — Coursera (Yale)", "url": "https://www.coursera.org/learn/healthcare-operations", "type": "course"},
    ],
    "Healthcare Data Privacy & Interoperability (HIPAA / HL7)": [
        {"title": "HL7 FHIR Interoperability Standard", "url": "https://www.hl7.org/fhir/", "type": "standard"},
        {"title": "Health Data Privacy & Security — Coursera (Johns Hopkins)", "url": "https://www.coursera.org/learn/healthcare-data-security", "type": "course"},
    ],
    "Biomedical Ethics & Patient Consent Frameworks": [
        {"title": "Ethics and Governance of AI for Health — WHO Guidance", "url": "https://www.who.int/publications/i/item/9789240029200", "type": "official_doc"},
        {"title": "Bioethics: An Introduction — Georgetown University (edX)", "url": "https://www.edx.org/learn/bioethics", "type": "course"},
    ],
    "Interprofessional Healthcare Team Coordination": [
        {"title": "Interprofessional Collaborative Practice — WHO Guidelines", "url": "https://www.who.int/publications/i/item/framework-for-action-on-interprofessional-education-collaborative-practice", "type": "standard"},
        {"title": "Teamwork in Healthcare Organizations — Coursera", "url": "https://www.coursera.org/learn/healthcare-teams", "type": "course"},
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
    # Multi-domain skill SDGs
    "Emergency Supply Chain Resilience & Routing": {
        "sdg_goal": 2,
        "sdg_name": "Zero Hunger",
        "rationale": "Secures food logistics channels to prevent famine during severe supply disruption.",
    },
    "Crisis Resource Allocation & Budgeting": {
        "sdg_goal": 12,
        "sdg_name": "Responsible Consumption and Production",
        "rationale": "Optimizes emergency relief resources to eliminate waste under acute budget constraints.",
    },
    "Humanitarian Logistics Standards (Sphere / UN)": {
        "sdg_goal": 2,
        "sdg_name": "Zero Hunger",
        "rationale": "Enforces international minimum standards for humanitarian food and aid distribution.",
    },
    "Public Sector Algorithmic Governance": {
        "sdg_goal": 16,
        "sdg_name": "Peace, Justice and Strong Institutions",
        "rationale": "Guarantees public systems act transparently, accountably, and without automated prejudice.",
    },
    "Equitable Policy Impact Assessment": {
        "sdg_goal": 10,
        "sdg_name": "Reduced Inequalities",
        "rationale": "Protects underrepresented groups from algorithmic and structural policy harms.",
    },
    "Civic Data Ethics & Transparency": {
        "sdg_goal": 16,
        "sdg_name": "Peace, Justice and Strong Institutions",
        "rationale": "Builds civic trust through open, ethically managed public data systems.",
    },
    "ESG Risk Scoring & Disclosure Standards": {
        "sdg_goal": 8,
        "sdg_name": "Decent Work and Economic Growth",
        "rationale": "Channels capital investments toward sustainable and responsible enterprises.",
    },
    "Financial Model Validation & Bias Auditing": {
        "sdg_goal": 10,
        "sdg_name": "Reduced Inequalities",
        "rationale": "Eliminates discriminatory credit barriers for disadvantaged populations.",
    },
    "Systemic Stress Testing Methodologies": {
        "sdg_goal": 8,
        "sdg_name": "Decent Work and Economic Growth",
        "rationale": "Preserves institutional macroeconomic stability during catastrophic events.",
    },
    "Climate Vulnerability Assessment & Scenario Modelling": {
        "sdg_goal": 13,
        "sdg_name": "Climate Action",
        "rationale": "Strengthens adaptive infrastructure against extreme climate disasters.",
    },
    "Renewable Energy Grid Integration & Storage": {
        "sdg_goal": 7,
        "sdg_name": "Affordable and Clean Energy",
        "rationale": "Expands clean, dependable electrification to communities worldwide.",
    },
    "Carbon Accounting & Greenhouse Gas Protocols": {
        "sdg_goal": 13,
        "sdg_name": "Climate Action",
        "rationale": "Drives measurable emissions reduction across industrial value chains.",
    },
    "Clinical Decision Support Systems (CDSS) Auditing": {
        "sdg_goal": 3,
        "sdg_name": "Good Health and Well-Being",
        "rationale": "Assures patient diagnostic safety and eliminates clinical algorithmic bias.",
    },
    "Hospital Operations & Surge Capacity Management": {
        "sdg_goal": 3,
        "sdg_name": "Good Health and Well-Being",
        "rationale": "Preserves critical hospital survival capacity during pandemic or emergency surges.",
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
    "Public Sector Algorithmic Governance",
    "Equitable Policy Impact Assessment",
    "Civic Data Ethics & Transparency",
    "Crisis Resource Allocation & Budgeting",
    "Cross-Agency Stakeholder Coordination",
    "ESG Risk Scoring & Disclosure Standards",
    "Financial Model Validation & Bias Auditing",
    "Climate Vulnerability Assessment & Scenario Modelling",
    "Clinical Decision Support Systems (CDSS) Auditing",
    "Biomedical Ethics & Patient Consent Frameworks",
    "Interprofessional Healthcare Team Coordination",
}

# Skills that are DOWN-RANKED under Rapid AI adoption (more automatable)
RAPID_DEPRIORITIZED_SKILLS = {
    "SQL & Database Querying",
    "Python for Data Analysis (pandas, numpy)",
    "API Design & Testing",
    "Fleet & Multi-Modal Freight Optimization",
    "Carbon Accounting & Greenhouse Gas Protocols",
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
