"""
seed_role_sdg.py - Seed telos_sdc.role_sdg with curated occupation -> SDG mappings
Owner: Person A (Backend Lead) - Substep 5.2 (SDG Mapping)
Working directory: src/
Run: python -X utf8 supabase/seed_role_sdg.py

Strategy: Keyword-Based Auto-Tagger
    1. Define keyword rules per SDG goal (curated list of occupation keywords)
    2. Fetch all ESCO occupation labels from Supabase
    3. For each occupation, check which SDG keyword rules match its label
    4. Build role_sdg rows with relationship_type + impact_reasoning
    5. Upsert to telos_sdc.role_sdg in batches

Coverage Target:
    - Priority 17 demo-relevant SDG goals covered
    - Expected match rate: 40-60% of 3,039 occupations (1,200-1,800 rows)
    - All 17 SDG goals represented in the mapping
"""

import os
import re
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client
from tqdm import tqdm

SRC_DIR  = Path(__file__).parent.parent
ENV_FILE = SRC_DIR / ".env"

load_dotenv(ENV_FILE)

supabase: Client = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_SECRET_KEY"],
)

BATCH_SIZE = 200

# ── SDG Keyword Rules ───────────────────────────────────────────────────────────
#
# Format: (sdg_goal, sdg_target, relationship_type, impact_reasoning, [keywords])
#
# keywords: list of lowercase strings — if ANY appear in the occupation label,
#           the mapping is added. Each rule produces one row in role_sdg.
#
# source: curated by Person A based on UN SDG descriptions
#

SDG_RULES: list[tuple[int, str, str, str, list[str]]] = [

    # ── SDG 1: No Poverty ───────────────────────────────────────────────────────
    (1, "1.1", "contributes",
     "Provides income-generating employment that lifts individuals above the poverty line.",
     ["social worker", "welfare officer", "community development", "poverty", "aid worker",
      "microfinance", "social protection", "livelihood"]),

    (1, "1.3", "supports",
     "Administers social protection programs that reduce vulnerability to economic shocks.",
     ["benefits officer", "social security", "public assistance", "welfare administrator",
      "insurance officer", "pension administrator"]),

    # ── SDG 2: Zero Hunger ──────────────────────────────────────────────────────
    (2, "2.3", "supports",
     "Improves agricultural productivity and food security through technical expertise.",
     ["farmer", "agronomist", "agricultural", "crop", "livestock", "horticulturist",
      "food production", "irrigation", "agronomy", "viticulturist", "apiarist"]),

    (2, "2.4", "enables",
     "Promotes sustainable food systems and resilient agricultural practices.",
     ["food safety", "food technologist", "food scientist", "nutritionist",
      "food quality", "food engineer", "aquaculture", "fisheries"]),

    # ── SDG 3: Good Health and Well-Being ────────────────────────────────────────
    (3, "3.1", "supports",
     "Reduces maternal mortality and improves reproductive health outcomes.",
     ["midwife", "obstetrician", "gynaecologist", "gynecologist", "maternal",
      "neonatal", "prenatal"]),

    (3, "3.2", "supports",
     "Prevents child mortality through pediatric care and vaccination programs.",
     ["paediatrician", "pediatrician", "child health", "neonatal nurse",
      "school nurse", "health visitor"]),

    (3, "3.4", "contributes",
     "Reduces premature mortality from non-communicable diseases through treatment and prevention.",
     ["doctor", "physician", "surgeon", "cardiologist", "oncologist", "neurologist",
      "psychiatrist", "psychologist", "therapist", "counsellor", "counselor",
      "physiotherapist", "occupational therapist", "speech therapist",
      "pharmacist", "nurse", "paramedic", "medical", "healthcare", "radiologist",
      "anaesthetist", "anesthesiologist", "dermatologist", "endocrinologist",
      "gastroenterologist", "rheumatologist", "urologist", "ophthalmologist",
      "dentist", "dental", "optometrist", "clinical"]),

    (3, "3.8", "enables",
     "Expands universal health coverage by delivering essential health services.",
     ["general practitioner", "community nurse", "health worker", "health assistant",
      "ambulance", "emergency medical", "first aider", "community health"]),

    # ── SDG 4: Quality Education ─────────────────────────────────────────────────
    (4, "4.1", "supports",
     "Delivers quality primary and secondary education to build foundational skills.",
     ["teacher", "educator", "instructor", "lecturer", "professor", "tutor",
      "teaching assistant", "school principal", "headteacher", "primary school",
      "secondary school", "kindergarten", "preschool"]),

    (4, "4.3", "enables",
     "Expands access to vocational training and higher education opportunities.",
     ["trainer", "training officer", "vocational", "curriculum developer",
      "instructional designer", "e-learning", "education coordinator",
      "university lecturer", "academic", "adult education"]),

    (4, "4.4", "contributes",
     "Develops technical and vocational skills needed for employment in a digital economy.",
     ["software", "programmer", "developer", "data scientist", "data analyst",
      "machine learning", "artificial intelligence", "cybersecurity", "cloud",
      "devops", "it specialist", "information technology", "computer", "web developer",
      "database administrator", "network engineer", "systems analyst", "ux designer",
      "ui designer", "product manager", "scrum master", "agile coach"]),

    # ── SDG 5: Gender Equality ───────────────────────────────────────────────────
    (5, "5.1", "contributes",
     "Promotes gender equality through policy implementation and advocacy.",
     ["gender", "equality officer", "diversity", "inclusion officer", "women",
      "feminist", "equal opportunity"]),

    (5, "5.5", "supports",
     "Increases women's participation in leadership and decision-making roles.",
     ["chief executive", "director", "executive", "manager", "administrator",
      "head of department", "senior officer", "coordinator", "supervisor"]),

    # ── SDG 6: Clean Water and Sanitation ────────────────────────────────────────
    (6, "6.1", "supports",
     "Ensures safe drinking water access through water management and treatment systems.",
     ["water engineer", "hydrologist", "water treatment", "water quality",
      "water supply", "water resources", "hydrogeologist", "environmental engineer"]),

    (6, "6.2", "enables",
     "Improves sanitation infrastructure and hygiene practice through engineering solutions.",
     ["sanitation", "wastewater", "sewage", "plumber", "civil engineer",
      "public health engineer", "drainage engineer"]),

    # ── SDG 7: Affordable and Clean Energy ───────────────────────────────────────
    (7, "7.2", "supports",
     "Expands renewable energy capacity through technical design, installation and operation.",
     ["solar", "wind turbine", "renewable energy", "photovoltaic", "energy engineer",
      "power engineer", "electrical engineer", "electrician", "energy consultant",
      "sustainable energy", "green energy", "biomass", "geothermal", "hydropower"]),

    (7, "7.3", "enables",
     "Improves energy efficiency across industries by applying engineering and design expertise.",
     ["energy auditor", "energy manager", "efficiency", "sustainable", "hvac",
      "building services", "mechanical engineer", "insulation"]),

    # ── SDG 8: Decent Work and Economic Growth ────────────────────────────────────
    (8, "8.3", "supports",
     "Promotes entrepreneurship and job creation through business development support.",
     ["entrepreneur", "business developer", "startup", "innovation manager",
      "venture", "incubator", "accelerator", "self-employed"]),

    (8, "8.5", "contributes",
     "Provides skilled employment and productive work opportunities that drive economic growth.",
     ["engineer", "technician", "specialist", "analyst", "consultant", "accountant",
      "economist", "financial", "actuary", "auditor", "legal", "lawyer", "architect",
      "designer", "project manager", "operations manager", "logistics",
      "supply chain", "procurement"]),

    (8, "8.6", "enables",
     "Reduces youth unemployment by providing technical training and employability skills.",
     ["career counsellor", "career advisor", "employment officer", "job coach",
      "recruitment", "human resources", "talent acquisition", "workforce"]),

    # ── SDG 9: Industry, Innovation and Infrastructure ────────────────────────────
    (9, "9.1", "supports",
     "Develops and maintains quality infrastructure that enables economic participation.",
     ["civil engineer", "structural engineer", "infrastructure", "construction manager",
      "project engineer", "quantity surveyor", "urban planner", "transport engineer",
      "road engineer", "bridge engineer", "rail engineer"]),

    (9, "9.2", "enables",
     "Drives industrial production and manufacturing innovation.",
     ["manufacturing", "production", "industrial engineer", "process engineer",
      "quality engineer", "operations", "factory", "assembly", "machinist",
      "welder", "fabricator", "toolmaker"]),

    (9, "9.4", "contributes",
     "Upgrades industrial processes to be more sustainable and resource-efficient.",
     ["environmental", "sustainability", "green", "circular economy", "waste management",
      "recycling", "pollution control", "emissions"]),

    (9, "9.5", "supports",
     "Advances scientific research and technological innovation for industrial development.",
     ["researcher", "scientist", "research engineer", "r&d", "laboratory",
      "innovation", "physicist", "chemist", "biologist", "biotechnologist",
      "material scientist", "nanotechnology"]),

    # ── SDG 10: Reduced Inequalities ─────────────────────────────────────────────
    (10, "10.2", "contributes",
     "Promotes social and economic inclusion for marginalized groups.",
     ["social inclusion", "disability", "accessibility", "sign language", "interpreter",
      "community organizer", "refugee", "migrant worker", "integration officer"]),

    (10, "10.4", "supports",
     "Implements fiscal and social policies that reduce inequality.",
     ["tax", "fiscal", "budget analyst", "public policy", "economist",
      "social policy", "public finance"]),

    # ── SDG 11: Sustainable Cities and Communities ────────────────────────────────
    (11, "11.1", "supports",
     "Improves housing quality and access to safe, affordable urban settlements.",
     ["urban planner", "architect", "housing", "property developer", "real estate",
      "building inspector", "zoning", "land use planner"]),

    (11, "11.2", "enables",
     "Expands safe and affordable public transport access in cities.",
     ["transport", "public transit", "logistics", "traffic engineer", "mobility",
      "urban mobility", "bus driver", "train operator", "metro", "aviation"]),

    (11, "11.6", "contributes",
     "Reduces environmental impact of cities through waste management and air quality control.",
     ["waste management", "recycling", "sanitation", "environmental health",
      "air quality", "noise pollution", "urban greening", "parks"]),

    # ── SDG 12: Responsible Consumption and Production ────────────────────────────
    (12, "12.2", "supports",
     "Promotes sustainable management of natural resources across supply chains.",
     ["supply chain", "procurement", "sustainable sourcing", "circular economy",
      "material", "inventory", "logistics manager", "resource efficiency"]),

    (12, "12.4", "enables",
     "Manages chemicals and waste responsibly to minimize environmental harm.",
     ["chemical engineer", "hazardous waste", "environmental compliance",
      "laboratory technician", "safety officer", "toxicologist"]),

    (12, "12.5", "contributes",
     "Reduces waste generation through recycling and sustainable product design.",
     ["product designer", "packaging", "upcycling", "waste reduction",
      "eco-design", "sustainable design", "green product"]),

    # ── SDG 13: Climate Action ───────────────────────────────────────────────────
    (13, "13.1", "supports",
     "Strengthens resilience and adaptive capacity to climate-related disasters.",
     ["climate", "disaster management", "emergency", "risk assessment",
      "resilience", "flood", "drought", "meteorologist", "climatologist"]),

    (13, "13.2", "enables",
     "Integrates climate change measures into national policies and planning.",
     ["environmental policy", "climate policy", "carbon", "ghg", "greenhouse",
      "net zero", "decarbonisation", "carbon footprint", "climate consultant"]),

    (13, "13.3", "contributes",
     "Raises awareness and builds capacity on climate change mitigation and adaptation.",
     ["environmental educator", "sustainability officer", "csr", "esg",
      "corporate sustainability", "green building", "leed"]),

    # ── SDG 14: Life Below Water ─────────────────────────────────────────────────
    (14, "14.1", "supports",
     "Reduces marine pollution and protects ocean ecosystems.",
     ["marine biologist", "oceanographer", "marine", "fisheries", "aquaculture",
      "coastal", "maritime", "coral reef", "marine pollution"]),

    (14, "14.2", "enables",
     "Manages and protects marine and coastal ecosystems sustainably.",
     ["marine ecologist", "coastal engineer", "marine conservationist",
      "environmental scientist", "wetlands"]),

    # ── SDG 15: Life on Land ─────────────────────────────────────────────────────
    (15, "15.1", "supports",
     "Conserves terrestrial ecosystems including forests, wetlands and mountains.",
     ["ecologist", "conservationist", "forester", "biodiversity", "wildlife",
      "botanist", "zoologist", "park ranger", "nature reserve", "environmental"]),

    (15, "15.2", "enables",
     "Promotes sustainable forest management and halts deforestation.",
     ["forester", "forest manager", "arborist", "silviculture", "timber",
      "logging", "reforestation", "land management"]),

    (15, "15.3", "contributes",
     "Combats desertification and restores degraded land and soil.",
     ["soil scientist", "geologist", "land rehabilitator", "land reclamation",
      "mining engineer", "geotechnical"]),

    # ── SDG 16: Peace, Justice and Strong Institutions ────────────────────────────
    (16, "16.1", "supports",
     "Reduces violence and promotes safety through law enforcement and justice services.",
     ["police", "law enforcement", "security", "detective", "border control",
      "correctional", "probation officer", "forensic", "criminologist"]),

    (16, "16.3", "enables",
     "Promotes rule of law and access to justice through legal services.",
     ["lawyer", "judge", "magistrate", "barrister", "solicitor", "legal",
      "paralegal", "court", "notary", "arbitrator", "mediator"]),

    (16, "16.6", "contributes",
     "Develops effective and accountable institutions through public administration.",
     ["public administrator", "civil servant", "government", "policy analyst",
      "regulatory", "compliance officer", "auditor", "inspector"]),

    (16, "16.9", "supports",
     "Provides legal identity services for universal birth registration and documentation.",
     ["registrar", "immigration officer", "civil registrar", "notary",
      "documentation officer", "id", "passport"]),

    # ── SDG 17: Partnerships for the Goals ────────────────────────────────────────
    (17, "17.6", "contributes",
     "Facilitates international technology sharing and scientific cooperation.",
     ["international", "diplomat", "ambassador", "trade officer", "international relations",
      "un ", "ngo", "development officer", "aid coordinator"]),

    (17, "17.17", "supports",
     "Promotes public-private partnerships that mobilize resources for sustainable development.",
     ["partnership manager", "stakeholder", "public relations", "communications",
      "csr manager", "business development", "external relations"]),
]


# ── Helpers ────────────────────────────────────────────────────────────────────

def label_matches(label: str, keywords: list[str]) -> bool:
    """
    Return True if any keyword appears as a word/phrase in the occupation label.
    Uses word-boundary matching to avoid partial matches (e.g. 'nurse' matches
    'community nurse' but not 'nursery manager' unless 'nursery' is also listed).
    """
    label_lower = label.lower()
    for kw in keywords:
        kw_lower = kw.lower().strip()
        # Simple substring for multi-word phrases, else word-boundary
        if " " in kw_lower or kw_lower.endswith(" "):
            if kw_lower in label_lower:
                return True
        else:
            # word boundary match
            if re.search(r'\b' + re.escape(kw_lower) + r'\b', label_lower):
                return True
    return False


# ── Fetch occupations ────────────────────────────────────────────────────────────

def fetch_all_occupations() -> list[dict]:
    """Paginate through all ESCO occupations and return esco_id + preferred_label."""
    print("\n[1/3] Fetching all ESCO occupations ...")
    all_rows: list[dict] = []
    page_size = 1000
    offset    = 0

    while True:
        resp = (
            supabase.schema("telos_sdc")
            .table("occupations")
            .select("esco_id, preferred_label")
            .range(offset, offset + page_size - 1)
            .execute()
        )
        batch = resp.data or []
        all_rows.extend(batch)
        if len(batch) < page_size:
            break
        offset += page_size

    print(f"  Fetched {len(all_rows):,} occupations.")
    return all_rows


# ── Build role_sdg rows ───────────────────────────────────────────────────────

def build_mappings(occupations: list[dict]) -> list[dict]:
    """
    Apply SDG keyword rules to each occupation.
    Returns list of role_sdg row dicts ready for upsert.
    Uses a set to deduplicate (role_id, sdg_goal, sdg_target) tuples.
    """
    print(f"\n[2/3] Applying {len(SDG_RULES)} SDG rules to {len(occupations):,} occupations ...")
    seen: set[tuple] = set()
    rows: list[dict] = []

    for occ in tqdm(occupations, desc="  tagging"):
        esco_id = occ["esco_id"]
        label   = occ.get("preferred_label", "") or ""

        for (goal, target, rel_type, reasoning, keywords) in SDG_RULES:
            if not label_matches(label, keywords):
                continue

            key = (esco_id, goal, target)
            if key in seen:
                continue
            seen.add(key)

            rows.append({
                "role_id":           esco_id,
                "sdg_goal":          goal,
                "sdg_target":        target,
                "relationship_type": rel_type,
                "impact_reasoning":  reasoning,
                "source":            "keyword-tagger-v1",
            })

    print(f"  Generated {len(rows):,} role->SDG mappings across {len(seen):,} unique pairs.")
    return rows


# ── Upsert to Supabase ────────────────────────────────────────────────────────

def upsert_mappings(rows: list[dict]) -> int:
    """Upsert role_sdg rows in batches. Returns total upserted."""
    if not rows:
        print("  No rows to upsert.")
        return 0

    print(f"\n[3/3] Upserting {len(rows):,} rows to telos_sdc.role_sdg ...")
    total = 0

    for i in tqdm(range(0, len(rows), BATCH_SIZE), desc="  upserting"):
        chunk = rows[i : i + BATCH_SIZE]
        (
            supabase.schema("telos_sdc")
            .table("role_sdg")
            .upsert(chunk, on_conflict="role_id,sdg_goal,sdg_target")
            .execute()
        )
        total += len(chunk)

    return total


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("Role->SDG Mapping => telos_sdc.role_sdg")
    print("Strategy: Keyword-Based Auto-Tagger")
    print(f"SDG rules defined: {len(SDG_RULES)}")
    print("=" * 60)

    occupations = fetch_all_occupations()
    rows        = build_mappings(occupations)
    total       = upsert_mappings(rows)

    # Coverage stats
    matched_roles = len(set(r["role_id"] for r in rows))
    total_roles   = len(occupations)
    pct           = matched_roles / total_roles * 100 if total_roles else 0

    print("\n" + "=" * 60)
    print("ROLE->SDG MAPPING COMPLETE")
    print(f"  Rows upserted         : {total:,}")
    print(f"  Unique roles matched  : {matched_roles:,} / {total_roles:,} ({pct:.1f}%)")
    print(f"  SDG goals covered     : all 17 (if occupations exist for each)")
    print("=" * 60)
    print("\nUNBLOCKS:")
    print("  [Self]     /api/match can now return SDG impact badges")
    print("  [Person C] Extend with additional curated mappings as needed")


if __name__ == "__main__":
    main()
