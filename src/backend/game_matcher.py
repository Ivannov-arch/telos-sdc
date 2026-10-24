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
    {
        "id": "emergency_logistics_coordinator",
        "title": "Emergency Logistics & Supply Chain Coordinator",
        "esco_id": "esco:4321",
        "description": "Orchestrates critical relief supply chains, allocates constrained distribution resources, and navigates acute route bottlenecks during systemic disruptions.",
        "skill_focus": ["Supply chain continuity", "Crisis resource allocation", "Operational routing"],
        "indicator_weights": {
            "decision_quality": 0.35,
            "adaptability": 0.35,
            "critical_verification": 0.20,
            "calibrated_ai_trust": 0.10,
        },
        "mission_affinity": {"A": 0.15, "B": 0.00, "C": 0.05},
        "interest_keywords": [
            "logistics", "supply chain", "agriculture", "food", "transportation",
            "operations", "distribution", "emergency", "inventory", "procurement",
        ],
        "skill_keywords": [
            "project management", "problem solving", "leadership", "logistics",
            "teamwork", "communication", "operations", "resource planning",
        ],
        "skill_gaps_template": [
            {"skill": "Emergency Supply Chain Resilience & Routing", "urgency": "high", "type": "core"},
            {"skill": "Crisis Resource Allocation & Budgeting", "urgency": "high", "type": "core"},
            {"skill": "Humanitarian Logistics Standards (Sphere / UN)", "urgency": "medium", "type": "core"},
            {"skill": "Fleet & Multi-Modal Freight Optimization", "urgency": "medium", "type": "supporting"},
            {"skill": "Cross-Agency Stakeholder Coordination", "urgency": "low", "type": "supporting"},
        ],
        "sdg_goals": [
            {
                "sdg_goal": 2,
                "sdg_name": "Zero Hunger",
                "impact_reasoning": "Secures resilient food delivery channels and prevents famine during systemic transport breakdowns.",
                "source": "UNSD SDG API",
            },
            {
                "sdg_goal": 12,
                "sdg_name": "Responsible Consumption and Production",
                "impact_reasoning": "Minimizes food loss and waste across emergency supply chains through optimized distribution.",
                "source": "UNSD SDG API",
            },
        ],
    },
    {
        "id": "public_policy_advisor",
        "title": "Public Policy & Government Technology Advisor",
        "esco_id": "esco:2422",
        "description": "Analyzes civic impact of automated systems, drafts regulatory safeguards, and ensures public service algorithms uphold citizen rights and equitable access.",
        "skill_focus": ["Civic impact analysis", "Algorithmic accountability", "Legislative drafting"],
        "indicator_weights": {
            "calibrated_ai_trust": 0.35,
            "critical_verification": 0.30,
            "decision_quality": 0.20,
            "adaptability": 0.15,
        },
        "mission_affinity": {"A": 0.05, "B": 0.15, "C": 0.05},
        "interest_keywords": [
            "government", "policy", "public", "civic", "regulation", "law",
            "democracy", "administration", "diplomacy", "public service",
        ],
        "skill_keywords": [
            "communication", "writing", "research", "critical thinking",
            "policy", "ethics", "leadership", "stakeholder management",
        ],
        "skill_gaps_template": [
            {"skill": "Public Sector Algorithmic Governance", "urgency": "high", "type": "core"},
            {"skill": "Equitable Policy Impact Assessment", "urgency": "high", "type": "core"},
            {"skill": "Civic Data Ethics & Transparency", "urgency": "medium", "type": "core"},
            {"skill": "Public Consultation & Stakeholder Engagement", "urgency": "medium", "type": "supporting"},
            {"skill": "Crisis Communication for Public Institutions", "urgency": "low", "type": "supporting"},
        ],
        "sdg_goals": [
            {
                "sdg_goal": 16,
                "sdg_name": "Peace, Justice and Strong Institutions",
                "impact_reasoning": "Fosters transparent, inclusive, and accountable public decision-making frameworks.",
                "source": "UNSD SDG API",
            },
            {
                "sdg_goal": 10,
                "sdg_name": "Reduced Inequalities",
                "impact_reasoning": "Protects marginalized communities from algorithmic discrimination in social safety and public welfare programs.",
                "source": "UNSD SDG API",
            },
        ],
    },
    {
        "id": "sustainable_finance_risk_manager",
        "title": "Sustainable Finance & Risk Manager",
        "esco_id": "esco:2412",
        "description": "Audits financial risk frameworks, stress-tests institutional credit models against bias and systemic shocks, and steers investments toward sustainable capital projects.",
        "skill_focus": ["Systemic risk assessment", "Credit fairness auditing", "ESG portfolio integration"],
        "indicator_weights": {
            "critical_verification": 0.35,
            "decision_quality": 0.30,
            "calibrated_ai_trust": 0.25,
            "adaptability": 0.10,
        },
        "mission_affinity": {"A": 0.00, "B": 0.15, "C": 0.05},
        "interest_keywords": [
            "finance", "banking", "esg", "investment", "risk", "economics",
            "sustainability", "capital", "markets", "accounting", "portfolio",
        ],
        "skill_keywords": [
            "excel", "data analysis", "critical thinking", "problem solving",
            "risk", "finance", "compliance", "research", "statistics",
        ],
        "skill_gaps_template": [
            {"skill": "ESG Risk Scoring & Disclosure Standards", "urgency": "high", "type": "core"},
            {"skill": "Financial Model Validation & Bias Auditing", "urgency": "high", "type": "core"},
            {"skill": "Systemic Stress Testing Methodologies", "urgency": "medium", "type": "core"},
            {"skill": "Sustainable Capital Allocation Frameworks", "urgency": "medium", "type": "supporting"},
            {"skill": "Regulatory Financial Compliance (Basel / TCFD)", "urgency": "low", "type": "supporting"},
        ],
        "sdg_goals": [
            {
                "sdg_goal": 8,
                "sdg_name": "Decent Work and Economic Growth",
                "impact_reasoning": "Promotes sound, inclusive financial systems that drive equitable economic productivity.",
                "source": "UNSD SDG API",
            },
            {
                "sdg_goal": 10,
                "sdg_name": "Reduced Inequalities",
                "impact_reasoning": "Eliminates systemic underwriting and credit bias across lending institutions.",
                "source": "UNSD SDG API",
            },
        ],
    },
    {
        "id": "climate_resilience_lead",
        "title": "Climate Resilience & Energy Transition Lead",
        "esco_id": "esco:2133",
        "description": "Develops regional grid decarbonization plans, evaluates environmental vulnerability to extreme shocks, and designs climate-resilient infrastructure systems.",
        "skill_focus": ["Vulnerability mapping", "Grid decarbonization strategy", "Environmental risk mitigation"],
        "indicator_weights": {
            "decision_quality": 0.35,
            "adaptability": 0.30,
            "critical_verification": 0.20,
            "calibrated_ai_trust": 0.15,
        },
        "mission_affinity": {"A": 0.05, "B": 0.00, "C": 0.15},
        "interest_keywords": [
            "climate", "energy", "sustainability", "environment", "renewable",
            "infrastructure", "green", "carbon", "ecology", "conservation",
        ],
        "skill_keywords": [
            "research", "data analysis", "problem solving", "critical thinking",
            "leadership", "project management", "systems thinking",
        ],
        "skill_gaps_template": [
            {"skill": "Climate Vulnerability Assessment & Scenario Modelling", "urgency": "high", "type": "core"},
            {"skill": "Renewable Energy Grid Integration & Storage", "urgency": "high", "type": "core"},
            {"skill": "Carbon Accounting & Greenhouse Gas Protocols", "urgency": "medium", "type": "core"},
            {"skill": "Environmental Disaster Preparedness Planning", "urgency": "medium", "type": "supporting"},
            {"skill": "Community Resilience Stakeholder Engagement", "urgency": "low", "type": "supporting"},
        ],
        "sdg_goals": [
            {
                "sdg_goal": 7,
                "sdg_name": "Affordable and Clean Energy",
                "impact_reasoning": "Accelerates the transition to reliable, modern, and renewable energy grids.",
                "source": "UNSD SDG API",
            },
            {
                "sdg_goal": 13,
                "sdg_name": "Climate Action",
                "impact_reasoning": "Builds operational adaptive capacity and strengthens resilience against climate-related hazards.",
                "source": "UNSD SDG API",
            },
        ],
    },
    {
        "id": "digital_health_operations_lead",
        "title": "Digital Health Operations Specialist",
        "esco_id": "esco:2263",
        "description": "Optimizes clinical service continuity during medical surges, audits diagnostic decision-support tools for safety, and safeguards patient data privacy.",
        "skill_focus": ["Clinical workflow continuity", "Medical decision-support auditing", "Patient data governance"],
        "indicator_weights": {
            "decision_quality": 0.35,
            "critical_verification": 0.30,
            "adaptability": 0.20,
            "calibrated_ai_trust": 0.15,
        },
        "mission_affinity": {"A": 0.05, "B": 0.10, "C": 0.05},
        "interest_keywords": [
            "healthcare", "health", "medical", "medicine", "clinical",
            "hospital", "patient", "biotech", "care", "wellbeing",
        ],
        "skill_keywords": [
            "communication", "teamwork", "problem solving", "customer service",
            "data analysis", "ethics", "critical thinking", "project management",
        ],
        "skill_gaps_template": [
            {"skill": "Clinical Decision Support Systems (CDSS) Auditing", "urgency": "high", "type": "core"},
            {"skill": "Hospital Operations & Surge Capacity Management", "urgency": "high", "type": "core"},
            {"skill": "Healthcare Data Privacy & Interoperability (HIPAA / HL7)", "urgency": "medium", "type": "core"},
            {"skill": "Biomedical Ethics & Patient Consent Frameworks", "urgency": "medium", "type": "supporting"},
            {"skill": "Interprofessional Healthcare Team Coordination", "urgency": "low", "type": "supporting"},
        ],
        "sdg_goals": [
            {
                "sdg_goal": 3,
                "sdg_name": "Good Health and Well-Being",
                "impact_reasoning": "Protects patient outcomes and enhances equitable healthcare delivery during emergency surges.",
                "source": "UNSD SDG API",
            },
            {
                "sdg_goal": 9,
                "sdg_name": "Industry, Innovation and Infrastructure",
                "impact_reasoning": "Fosters safe, reliable technological innovation in health infrastructure.",
                "source": "UNSD SDG API",
            },
        ],
    },
    {
        "id": "edtech_curriculum_designer",
        "title": "Future Learning & Workforce Transition Strategist",
        "esco_id": "esco:2351",
        "description": "Designs adaptive, AI-augmented educational curricula and workforce reskilling programs to prepare displaced workers for resilient digital-age careers.",
        "skill_focus": ["Curriculum development", "Adult workforce pedagogy", "Digital learning analytics"],
        "indicator_weights": {
            "decision_quality": 0.30,
            "adaptability": 0.35,
            "calibrated_ai_trust": 0.20,
            "critical_verification": 0.15,
        },
        "mission_affinity": {"A": 0.05, "B": 0.10, "C": 0.00},
        "interest_keywords": [
            "education", "learning", "teaching", "training", "edtech",
            "workforce", "schools", "pedagogy", "curriculum", "upskilling",
        ],
        "skill_keywords": [
            "writing", "communication", "design", "research", "project management",
            "teamwork", "leadership", "critical thinking",
        ],
        "skill_gaps_template": [
            {"skill": "Adaptive Learning Systems & Pedagogy", "urgency": "high", "type": "core"},
            {"skill": "Workforce Reskilling & Competency Frameworks", "urgency": "high", "type": "core"},
            {"skill": "Learning Analytics & Educational Assessment", "urgency": "medium", "type": "core"},
            {"skill": "Digital Instructional Media Design", "urgency": "medium", "type": "supporting"},
            {"skill": "Adult Learner Mentorship & Coaching", "urgency": "low", "type": "supporting"},
        ],
        "sdg_goals": [
            {
                "sdg_goal": 4,
                "sdg_name": "Quality Education",
                "impact_reasoning": "Expands inclusive, equitable lifelong learning and practical skill development.",
                "source": "UNSD SDG API",
            },
            {
                "sdg_goal": 8,
                "sdg_name": "Decent Work and Economic Growth",
                "impact_reasoning": "Bridges skill mismatches to empower vulnerable workers facing technological disruption.",
                "source": "UNSD SDG API",
            },
        ],
    },
    {
        "id": "smart_agriculture_analyst",
        "title": "Smart Agriculture & Food Systems Analyst",
        "esco_id": "esco:2132",
        "description": "Combines agronomic modeling, satellite sensory data, and supply chain telemetry to build climate-resilient crop yields and buffer food systems against shocks.",
        "skill_focus": ["Agronomic data modeling", "Crop resilience planning", "Food security assessment"],
        "indicator_weights": {
            "decision_quality": 0.40,
            "critical_verification": 0.30,
            "adaptability": 0.20,
            "calibrated_ai_trust": 0.10,
        },
        "mission_affinity": {"A": 0.15, "B": 0.00, "C": 0.05},
        "interest_keywords": [
            "agriculture", "farming", "food", "crops", "soil", "rural",
            "agritech", "sustainability", "climate", "nutrition",
        ],
        "skill_keywords": [
            "research", "data analysis", "problem solving", "critical thinking",
            "project management", "excel", "planning",
        ],
        "skill_gaps_template": [
            {"skill": "Precision Agriculture & Remote Sensing", "urgency": "high", "type": "core"},
            {"skill": "Crop Yield Climate Stress Modelling", "urgency": "high", "type": "core"},
            {"skill": "Agri-Food Supply Chain Telemetry", "urgency": "medium", "type": "core"},
            {"skill": "Sustainable Agroecology & Soil Health", "urgency": "medium", "type": "supporting"},
            {"skill": "Rural Farmer Extension & Capacity Building", "urgency": "low", "type": "supporting"},
        ],
        "sdg_goals": [
            {
                "sdg_goal": 2,
                "sdg_name": "Zero Hunger",
                "impact_reasoning": "Strengthens food production resilience and reduces crop vulnerability to climate shocks.",
                "source": "UNSD SDG API",
            },
            {
                "sdg_goal": 15,
                "sdg_name": "Life on Land",
                "impact_reasoning": "Promotes sustainable soil management and preserves terrestrial agroecosystems.",
                "source": "UNSD SDG API",
            },
        ],
    },
    {
        "id": "human_ai_ux_designer",
        "title": "Human-AI Interaction & UX Product Designer",
        "esco_id": "esco:2513.2",
        "description": "Designs intuitive, ethical user experiences for complex AI-driven control rooms and automated decision workflows, ensuring human operators maintain situational clarity.",
        "skill_focus": ["Human-AI interface design", "Cognitive load optimization", "User research & prototyping"],
        "indicator_weights": {
            "critical_verification": 0.35,
            "adaptability": 0.30,
            "decision_quality": 0.20,
            "calibrated_ai_trust": 0.15,
        },
        "mission_affinity": {"A": 0.05, "B": 0.10, "C": 0.05},
        "interest_keywords": [
            "design", "ux", "ui", "product", "technology", "interface",
            "creative", "visual", "interaction", "multimedia", "accessibility",
        ],
        "skill_keywords": [
            "design", "communication", "writing", "problem solving",
            "teamwork", "customer service", "critical thinking",
        ],
        "skill_gaps_template": [
            {"skill": "Explainable AI (XAI) Interface Design", "urgency": "high", "type": "core"},
            {"skill": "Cognitive Ergonomics & Decision-Room UX", "urgency": "high", "type": "core"},
            {"skill": "Accessible Design Standards (WCAG 2.2)", "urgency": "medium", "type": "core"},
            {"skill": "Rapid Interactive Prototyping (Figma / Web)", "urgency": "medium", "type": "supporting"},
            {"skill": "Qualitative User Research & Usability Testing", "urgency": "low", "type": "supporting"},
        ],
        "sdg_goals": [
            {
                "sdg_goal": 9,
                "sdg_name": "Industry, Innovation and Infrastructure",
                "impact_reasoning": "Improves human control and safety within critical industrial automation systems.",
                "source": "UNSD SDG API",
            },
            {
                "sdg_goal": 10,
                "sdg_name": "Reduced Inequalities",
                "impact_reasoning": "Ensures technological tools and digital interfaces remain universally accessible to all abilities.",
                "source": "UNSD SDG API",
            },
        ],
    },
    {
        "id": "sustainability_communications_strategist",
        "title": "Sustainability Communications & Brand Strategist",
        "esco_id": "esco:2431",
        "description": "Translates complex sustainability data, crisis briefs, and climate initiatives into authentic public campaigns, eliminating greenwashing and building community trust.",
        "skill_focus": ["ESG storytelling", "Public campaign strategy", "Stakeholder brand advocacy"],
        "indicator_weights": {
            "critical_verification": 0.30,
            "calibrated_ai_trust": 0.30,
            "adaptability": 0.25,
            "decision_quality": 0.15,
        },
        "mission_affinity": {"A": 0.05, "B": 0.05, "C": 0.10},
        "interest_keywords": [
            "marketing", "communications", "sustainability", "media",
            "branding", "public relations", "advocacy", "advertising", "climate",
        ],
        "skill_keywords": [
            "marketing", "writing", "communication", "leadership",
            "customer service", "design", "teamwork", "research",
        ],
        "skill_gaps_template": [
            {"skill": "ESG Reporting & Anti-Greenwashing Standards", "urgency": "high", "type": "core"},
            {"skill": "Crisis Public Relations & Narrative Strategy", "urgency": "high", "type": "core"},
            {"skill": "Audience Segmentation & Impact Analytics", "urgency": "medium", "type": "core"},
            {"skill": "Multimedia Digital Campaign Production", "urgency": "medium", "type": "supporting"},
            {"skill": "Community Coalition Building", "urgency": "low", "type": "supporting"},
        ],
        "sdg_goals": [
            {
                "sdg_goal": 12,
                "sdg_name": "Responsible Consumption and Production",
                "impact_reasoning": "Educates consumers and holds organizations accountable for genuine sustainable practices.",
                "source": "UNSD SDG API",
            },
            {
                "sdg_goal": 17,
                "sdg_name": "Partnerships for the Goals",
                "impact_reasoning": "Rallies cross-sector public support for high-impact sustainable development goals.",
                "source": "UNSD SDG API",
            },
        ],
    },
    {
        "id": "service_operations_resilience_lead",
        "title": "Customer Operations & Service Resilience Lead",
        "esco_id": "esco:2434",
        "description": "Leads frontline service continuity during severe institutional crises, de-escalating critical client emergencies and integrating automated triage with human empathy.",
        "skill_focus": ["High-stakes customer de-escalation", "Omnichannel service continuity", "Customer empathy & crisis support"],
        "indicator_weights": {
            "decision_quality": 0.35,
            "adaptability": 0.35,
            "critical_verification": 0.15,
            "calibrated_ai_trust": 0.15,
        },
        "mission_affinity": {"A": 0.10, "B": 0.05, "C": 0.05},
        "interest_keywords": [
            "customer", "service", "operations", "client", "support",
            "finance", "healthcare", "logistics", "consumer",
        ],
        "skill_keywords": [
            "customer service", "communication", "teamwork", "problem solving",
            "leadership", "writing", "management",
        ],
        "skill_gaps_template": [
            {"skill": "Crisis Customer De-escalation & Conflict Resolution", "urgency": "high", "type": "core"},
            {"skill": "Service Continuity & Emergency Escalation Protocols", "urgency": "high", "type": "core"},
            {"skill": "Customer Journey & AI Triage Integration", "urgency": "medium", "type": "core"},
            {"skill": "Service Quality Metrics & NPS Analytics", "urgency": "medium", "type": "supporting"},
            {"skill": "Empathetic Communication Coaching", "urgency": "low", "type": "supporting"},
        ],
        "sdg_goals": [
            {
                "sdg_goal": 8,
                "sdg_name": "Decent Work and Economic Growth",
                "impact_reasoning": "Fosters safe, humane, and dignified frontline work environments during system crises.",
                "source": "UNSD SDG API",
            },
            {
                "sdg_goal": 9,
                "sdg_name": "Industry, Innovation and Infrastructure",
                "impact_reasoning": "Ensures uninterrupted essential service delivery across critical commercial infrastructure.",
                "source": "UNSD SDG API",
            },
        ],
    },
    {
        "id": "cyber_infrastructure_analyst",
        "title": "Cybersecurity & Critical Infrastructure Defense Analyst",
        "esco_id": "esco:2529",
        "description": "Guards critical utility grids, financial rails, and emergency networks against cyber attacks, systemic failures, and adversarial automated exploits.",
        "skill_focus": ["Critical infrastructure defense", "Incident containment", "Adversarial threat analysis"],
        "indicator_weights": {
            "critical_verification": 0.40,
            "decision_quality": 0.30,
            "calibrated_ai_trust": 0.20,
            "adaptability": 0.10,
        },
        "mission_affinity": {"A": 0.00, "B": 0.05, "C": 0.15},
        "interest_keywords": [
            "cybersecurity", "security", "energy", "infrastructure", "defense",
            "technology", "government", "networks", "utilities", "systems",
        ],
        "skill_keywords": [
            "problem solving", "critical thinking", "data analysis", "python",
            "risk", "systems thinking", "project management",
        ],
        "skill_gaps_template": [
            {"skill": "Industrial Control Systems (ICS / SCADA) Defense", "urgency": "high", "type": "core"},
            {"skill": "Cyber Threat Intelligence & Incident Response", "urgency": "high", "type": "core"},
            {"skill": "Zero Trust Architecture & Network Hardening", "urgency": "medium", "type": "core"},
            {"skill": "AI Security & Adversarial Robustness", "urgency": "medium", "type": "supporting"},
            {"skill": "Disaster Recovery & Redundant Grid Failover", "urgency": "low", "type": "supporting"},
        ],
        "sdg_goals": [
            {
                "sdg_goal": 9,
                "sdg_name": "Industry, Innovation and Infrastructure",
                "impact_reasoning": "Protects vital energy, transport, and communication backbones from malicious destabilization.",
                "source": "UNSD SDG API",
            },
            {
                "sdg_goal": 16,
                "sdg_name": "Peace, Justice and Strong Institutions",
                "impact_reasoning": "Safeguards essential state infrastructure and institutions against cyber warfare.",
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

    # Sort by match score descending, assign ranks to top 3 best matches
    results.sort(key=lambda r: r["match_score"], reverse=True)
    top_results = results[:3]
    for i, r in enumerate(top_results):
        r["rank"] = i + 1

    return top_results
