Below are the **appropriate and verifiable** datasets for all 6 features. Core recommendation: use **ESCO** as the backbone for skills and occupations, **O*NET** as a complement for job tasks, cognitive metrics, and AI exposure data, **MASCO 2020** for Malaysian occupational localization, **OpenDOSM / Job Market Insights** for Malaysian labor signals, **UNSD SDG API** for official SDG mapping, and **BGE-M3** (BAAI) as the embedding model. Avoid CV datasets containing real resumes — hackathon rules prohibit real personal data.

---

## Dataset Map by Feature

| Feature | Primary Dataset(s) | Role in System |
|---|---|---|
| **1. Skills Profile Intake** | ESCO Skills/Competences + Synthetic Profiles (JSON) | Normalizes skills from CV/form into standardized ESCO IDs; embedding via BGE-M3 |
| **2. AI-Trend Signal Layer (CTCI)** | O*NET Database + AIOE / GPTs-are-GPTs / Webb Scores + OpenDOSM JMI | Computes Cognitive Task Compression Index; classifies Substitutive vs Complementary Compression |
| **3. Future-Role Matching + Skill Gap** | ESCO Occupations <-> Skills + O*NET Tasks + MASCO 2020 + DOSM JMI | Role catalogs, required skills, BGE-M3 hybrid search (Dense + Sparse + RRF), Malaysian context |
| **4. Personalised Reskilling Pathway** | O*NET Task Statements (Scenario Bank) | Generates fictionalized Micro-Task Simulation scenarios per skill gap |
| **5. SDG Mapping** | UNSD SDG API (Goals, Targets, Indicators) | Curated `role_sdg` metadata injection into Feature 3 JSON output |
| **6. Career Stress-Test Engine** | O*NET Cognitive Task Matrix + AIOE / Webb / Eloundou Disruption Penalties | Builds `occupation_disruption_matrix` for parameterized scenario reweighting |

---

## Feature 1: Skills Profile Intake

### 1. ESCO Skills and Competences — Primary Taxonomy Backbone

**Source:** European Commission, ESCO.
**URL:** https://esco.ec.europa.eu/en/use-esco/download
**Format:** CSV, JSON-LD, RDF/TTL, ODS, XML; also available via Web API and Local API.
**License:** CC BY 4.0

**Why Most Suitable:**
- Contains classifications of **occupations, skills, competences, and qualifications** — not merely raw skill lists.
- Multi-language support (24 EU languages + others) → normalizes "Data Analysis", "Data Analytics", "Data Processing" to the same concept.
- RDF/JSON-LD structure ideal for knowledge graphs: skills link to occupations, essential skills, optional skills, broader/narrower concepts.
- Distinguishes **Essential vs Optional competences** per occupation — directly powers the Set Difference skill gap algorithm.

**How to Use for Feature 1:**
- Create `skills` table: `esco_id`, `preferred_label`, `alt_labels`, `skill_type`, `description`, `broader_skill_id`
- Map extracted CV skills to `esco_id` (not raw text)
- Store `confidence_score` per mapping; do not force ESCO assignment if evidence is insufficient

**Verification:** Official European Commission dataset, free to download, latest version accessible via portal or API.

---

### 2. BGE-M3 Embedding Model — Dense + Sparse Vectors

**Source:** Beijing Academy of Artificial Intelligence (BAAI)
**HuggingFace:** https://huggingface.co/BAAI/bge-m3
**License:** MIT

**Why Critical:**
- A single forward pass produces **three retrieval modalities simultaneously:** Dense semantic vector, Sparse lexical vector (SPLADE-style), ColBERT multi-vector
- Supports 100+ languages: Bahasa Melayu, Mandarin, and English map to the same universal vector space — no translation layer needed
- Eliminates need to run separate embedding models for dense and sparse retrieval

**Deployment:** RunPod GPU ($25 credit) via vLLM container. Expose `/embed` endpoint returning `{ dense_vector, sparse_vector, colbert_vecs }`.

**Storage:** Supabase `pgvector`:
- `vector` type → dense embeddings
- `sparsevec` type → sparse embeddings (pgvector v0.7.0+, native in Supabase)

---

### 3. Synthetic CV / Profile Dataset — Demo Only

For demos, avoid all datasets claiming to contain real resumes. HuggingFace `datasetmaster/resumes` explicitly contains a mix of real and synthetic resumes → **PII violation risk under hackathon rules.**

**Safer Alternative:**
- Generate 20-50 synthetic demo profiles in JSON format adhering to ESCO schema
- Use fictitious names, fictitious experiences, and skills mapped to ESCO IDs
- Do not use any dataset sourced from real personal documents

**Verification Note:** Resume datasets on HuggingFace are generally not institutional sources; several blend real + synthetic data. Treat as experimental references only.

---

## Feature 2: AI-Trend Signal Layer (Cognitive Task Compression Index)

### 1. O*NET Database — Cognitive Task and Ability Data

**Source:** U.S. Department of Labor / O*NET Resource Center.
**URL:** https://www.onetcenter.org/database.html
**Format:** SQL, CSV, XML, RDF; also via Web Services API.
**License:** Public Domain (U.S. government)

**Why Critical for Feature 2:**
- O*NET decomposes occupations into **knowledge, skills, abilities, tasks, and work activities** — the granular substrate for computing cognitive task intensity.
- The `Abilities` and `Work Activities` files provide the exact variables used by Felten et al. (AIOE) and Rai (2026) to compute cognitive load per occupation.
- Task statements enable classification of repetitive vs judgment-intensive work, the foundation of the Substitutive vs Complementary Compression distinction.

**How to Use:**
- Load `Abilities.txt`, `Work Activities.txt`, `Tasks.txt` from O*NET database
- Compute `routine_cognitive_ratio` per O*NET-SOC occupation code
- Join with AIOE / Webb / Eloundou scores to produce full CTCI

---

### 2. Academic AI Exposure Indices

Three validated indices are used to compute the Cognitive Task Compression Index (CTCI):

#### a. AIOE — AI Occupational Exposure (Felten, Raj & Seamans)

**Source:** ResearchGate / arXiv
**Reference:** Occupational, industry, and geographic exposure to artificial intelligence — https://www.researchgate.net/publication/351174628
**Methodology:** Maps 10 AI application capabilities (NLP, image synthesis, reading comprehension, etc.) against O*NET ability dimensions.

> **Critical bias note (Rai 2026, arXiv 2606.23633):** AIOE correlates r=+0.85 with cognitive content intensity — not true AI replaceability (Human Judgment Halo Effect). High-reasoning roles (actuaries, lawyers, data analysts) score "High Exposure" simply due to cognitive density, not because AI can actually replace their work. Weight this index at 0.25 in CTCI; rely more heavily on Webb scores.

#### b. GPTs-are-GPTs (Eloundou et al., OpenAI)

**Source:** arXiv / ResearchGate
**Reference:** GPTs are GPTs — Labor market impact potential of LLMs — https://www.researchgate.net/publication/381581667
**Methodology:** Measures fraction of tasks in each occupation completable 50% faster by LLMs without quality degradation.

> **Same bias caveat as AIOE** — correlates with cognitive load more than AI substitutability. Weight at 0.25 in CTCI.

#### c. Webb Patent-Based AI Exposure Score

**Source:** arXiv
**Reference:** https://arxiv.org/html/2412.04924v1
**Methodology:** Purely lexical overlap between AI patent vocabulary and O*NET task descriptions — **lowest human-judgment bias** of the three indices.

> **Recommended:** Weight at 0.50 in CTCI computation due to lower halo-effect contamination.

**CTCI Formula:**
```
CTCI = (0.5 * Webb_score) + (0.25 * AIOE_score) + (0.25 * GPTs_score)
```

---

### 3. OpenDOSM / Job Market Insights — Malaysian Labor Signal

**Source:** Department of Statistics Malaysia (DOSM).
**Catalog URL:** https://open.dosm.gov.my/data-catalogue
**Labour Market Portal:** https://mylabourhub.dosm.gov.my
**Job Market Insights:** https://www.dosm.gov.my/bda-jmi
**My Job Profile:** https://myjobprofile.dosm.gov.my

**Why Essential for Feature 2:**
- Quarterly releases: job vacancies by occupation, economic activity, state, skills, and field of study
- Removes bias from Western-centric generalization; provides locally validated Malaysian vacancy signals
- TVET-related job openings categorized under MASCO
- Injects short-range factual relevance for local graduates monitoring the contemporary job market

**How to Use:**
- Pull latest quarterly release → `occupation_my_signal` table: `masco_code`, `vacancy_count`, `period`, `state`
- Display Malaysian vacancy trend as context alongside CTCI score in UI
- Clearly cite reporting period (do not claim real-time)

---

## Feature 3: Future-Role Matching + Skill Gap

### 1. ESCO Occupations <-> Skills — Matching Basis

**Source:** ESCO download/API (same as Feature 1).

**Key Components:**
- `occupations.csv` / occupation RDF
- `skills.csv` / skill RDF
- Occupation-skill relations: essential vs optional skills per occupation

**Why Critical:**
- Construct required skills vector per target role
- Skill gap computed as: `Gap = Required Skills \ User Skills` (Set Difference)
- Hierarchical relations separate core gaps from supporting gaps

---

### 2. O*NET Database — Role Enrichment

**Source:** https://www.onetcenter.org/database.html (same as Feature 2)
**Current version:** 31.0

**How to Use for Feature 3:**
- Enrich role descriptions: `occupation_title`, `tasks`, `skills`, `knowledge`, `work_activities`
- Maintain ESCO as canonical ID; map O*NET SOC to ESCO only where rigorously justifiable
- Avoid forcibly merging taxonomies — store both and cite respective sources

---

### 3. MASCO 2020 — Malaysian Occupational Classification

**Source:** Ministry of Human Resources Malaysia (MoHR).
**URL:** https://emasco.mohr.gov.my/intro
**PDF Reference:** https://emasco.mohr.gov.my/system-api/storage/uploads/masco_2020_en.pdf
**License:** Public, Malaysian government

**Why Critical for Malaysian Localization:**
- Synchronized with ISCO-08 (international standard) but adapted for Malaysia's Industry 4.0 context
- Hierarchical: 10 Major Groups → 6,366 Minor Unit Groups (6-digit codes)
- Links Malaysian occupational reality to international ESCO/O*NET taxonomy via crosswalk

**How to Use:**
- Load MASCO 2020 into `masco_occupations` table: `masco_code` (6-digit), `masco_title`, `isco_code`, `major_group`
- Build crosswalk: `masco_code` → `onet_soc_code` → `esco_id`
- Use MASCO codes to validate role relevance in the Malaysian market (alongside DOSM vacancy data)

**Verification:** Official Malaysian government publication (eMASCO portal), 2020 edition aligned with ISCO-08.

---

### 4. OpenDOSM / Job Market Insights — Malaysian Role Validation

(See Feature 2, Section 3 — same dataset, used here for role relevance validation.)

---

### 5. BGE-M3 for Role Vector Generation

(See Feature 1, Section 2 — same model. Role dense + sparse vectors generated via RunPod endpoint and stored in Supabase `pgvector`.)

**Supabase Hybrid Search:** Reciprocal Rank Fusion (RRF) PL/pgSQL function combines dense (Cosine) and sparse (inner product) rankings into a single composite score.
Reference: https://supabase.com/docs/guides/ai/hybrid-search

---

## Feature 4: Personalised Reskilling Pathway

### O*NET Task Statements — Simulation Scenario Bank

**Source:** O*NET Resource Center (same as Features 2 & 3).
**Relevant files:** `Tasks.txt`, `Task Statements by Occupation`

**How to Use:**
- Pull task statements per occupation for each identified skill gap
- Curate 1-3 fictionalized scenario prompts per ESCO skill category
- Store in `simulation_tasks`: `skill_id`, `scenario_text`, `rubric_criteria[]`

**LLM Evaluator:** Llama-3-8B or Qwen variant on RunPod via vLLM + Pydantic/Instructor.
- Closed evaluator — no open-ended generation
- Returns: `{ score_percent, improvement_reasoning, missing_concepts[] }` in strict JSON

---

## Feature 5: SDG Mapping

### UN SDG API — The Authoritative Official Source

**Source:** United Nations Statistics Division (UNSD).
**API Documentation:** https://unstats.un.org/sdgs/UNSDGAPIV5/swagger/index.html
**Official Metadata:** https://unstats.un.org/sdgs/metadata/

**Relevant Endpoints:**
- `GET /v1/sdg/Goal/List`
- `GET /v1/sdg/Goal/{goalCode}/Target/List`
- `GET /v1/sdg/Target/List`
- `GET /v1/sdg/Indicator/List`

**Why the Right Choice:**
- Official framework: 17 Goals, 169 Targets, global indicators for the 2030 Agenda
- Ingest `sdg_goals`, `sdg_targets`, `sdg_indicators` tables directly from the API
- Build `role_sdg` and `skill_sdg` curated relation tables
- Eliminates reliance on arbitrary LLM-generated SDG references

**Recommended Minimum Schema:**
```json
{
  "role_id": "esco:2512",
  "role_title": "AI Governance / Responsible AI Specialist",
  "sdg_alignment": [
    {
      "sdg_goal": 8,
      "sdg_target": "8.2",
      "source": "UNSD SDG API",
      "relationship_type": "supports",
      "evidence": "Role supports innovation and productivity through responsible AI adoption."
    }
  ]
}
```

> **Important:** The UN API supplies goal/target/indicator definitions but does **NOT** provide automated "role → SDG" mappings. The role/skill to SDG mapping must be maintained as an auditable curated table with verifiable justifications. Never allow LLMs to invent SDG links without a curated reference entry.

**Priority SDG targets to curate:**
- **SDG 4.4** — Increase youth/adults with technical and vocational skills
- **SDG 8.2** — Achieve higher economic productivity through diversification and technology
- **SDG 9.5** — Enhance scientific research and upgrade technological capabilities
- **SDG 10.2** — Empower and promote the social, economic, and political inclusion of all

---

## Feature 6: Career Stress-Test Engine

### O*NET Cognitive Task Matrix + AI Exposure Indices

**Source:** O*NET (same as Features 2-4) + AIOE / Webb / Eloundou indices (same as Feature 2).

**How to Use for Feature 6:**
- Use O*NET `Work Activities` and `Abilities` to compute `routine_cognitive_ratio` per occupation
- Combine with AIOE, Webb, and Eloundou scores to derive `disruption_penalty_fast` and `disruption_penalty_moderate`
- Store in `occupation_disruption_matrix`: `onet_soc_code`, `routine_cognitive_ratio`, `disruption_penalty_fast`, `disruption_penalty_moderate`

**Scenario Engine:**
```
Moderate:       Final Score = standard Feature 3 hybrid score (no penalty applied)
Fast Disruption: Final Score = hybrid_score * (1 - disruption_penalty_fast)
                 + bonus_amplifier for soft_skill_intensity
```

All reweighting is fully deterministic — no LLM involved in scenario modeling.

---

## Most Realistic Stack for a 5-Day Hackathon

1. **ESCO** — primary canon for `skill_id`, `occupation_id`, occupation-skill relations (Features 1, 3, 5)
2. **BGE-M3 (BAAI)** — hybrid embedding model for dense + sparse vectors (Features 1, 3) via RunPod
3. **O*NET** — tasks, work activities, cognitive abilities, task statements (Features 2, 3, 4, 6)
4. **MASCO 2020** — Malaysian occupational crosswalk, ISCO-08 aligned (Feature 3)
5. **OpenDOSM Job Market Insights** — Malaysian vacancy signals and role relevance validation (Features 2, 3)
6. **AIOE / GPTs-are-GPTs / Webb Scores** — academic AI exposure indices for CTCI (Features 2, 6)
7. **UN SDG API** — official goals, targets, indicators for SDG metadata (Feature 5)
8. **In-house synthetic user profiles** — Feature 1 demo purposes only; avoid all real CV datasets

---

## Verification Checklist Before Deployment

- **License and Attribution:** Review ESCO (CC BY 4.0), O*NET (Public Domain), DOSM (Malaysian Govt Open Data), UNSD (UN Open Data), BGE-M3 (MIT) before publishing.
- **Version and Timestamps:** Record `dataset_version`, `retrieved_at`, and source URLs in the repository for every dataset.
- **Language Support:** ESCO supports multiple languages; use English as the canonical technical representation while retaining alternative labels for Bahasa Malaysia/Chinese where available.
- **MASCO Crosswalk Quality:** Document every `masco_code` → `onet_soc_code` → `esco_id` mapping with justification; do not blindly auto-generate crosswalks.
- **Mapping Quality:** Never allow the LLM to invent `skill → SDG` relations without a curated reference table.
- **CV Data:** Strictly use self-generated synthetic profiles; avoid all datasets containing real resumes.
- **AI Exposure Bias:** Always document the Rai (2026) bias caveat when presenting CTCI scores — frame as Cognitive Task Compression, not a "job survival probability" score.

---

The combination of **ESCO + BGE-M3 + O*NET + MASCO 2020 + DOSM JMI + UNSD SDG API** is the most defensible architecture: official, open, structured, citable, multilingual, and comprehensive enough to power skills intake, hybrid role matching, skill gaps, AI disruption signals, reskilling simulations, SDG alignment, and career stress-testing — without compromising privacy or hallucinating data.