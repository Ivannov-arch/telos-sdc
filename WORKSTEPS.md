# WORKSTEPS - SDC XMUM Hackathon: Domain 1 (Aiversecity)

> **Context:** This document outlines the execution roadmap for all 6 core features of **Domain 1: The Aiversecity Future-Ready Workforce**.
> Based on [`algorithm_consideration.md`](./algorithm_consideration.md), [`deep_research.md`](./deep_research.md), and the judging rubric from [`src/Domain 1.md`](./src/Domain%201.md).
> Dataset sources refer to [`Datasets.md`](./Datasets.md).

---

## Core Paradigm: AI-Grounded Determinism (Zero AI Slop)

The foundational design principle for all features is a strict separation of responsibilities:

- **AI/LLM tasks only:** Named Entity Recognition (CV extraction), synonym normalization via embeddings, and isolated Micro-Task Simulation evaluator (Feature 4).
- **Deterministic / math tasks:** Match Score computation, Skill Gap analysis, Career Stress-Test, and SDG metadata injection — all governed by pure mathematical algorithms and vector space search, **never** free-form LLM narration.

This architecture guarantees reproducible, auditable, and hallucination-free outputs that will withstand scrutiny from hackathon judges.

---

## Timeline: 5-Day Hackathon

| Day | Primary Focus |
|---|---|
| Day 1 | Project setup, database schema, ESCO + O*NET seeding, MASCO crosswalk, SDG API seed, synthetic profiles |
| Day 2 | Feature 1: Skills Profile Intake (CV parser + Pydantic structured output + Dense Embedding) |
| Day 3 | Feature 3: BGE-M3 Hybrid Search + RRF + Skill Gap; Feature 2: CTCI signal layer |
| Day 4 | Feature 5: SDG Mapping; Feature 4: Micro-Task Simulation; Feature 6: Career Stress-Test slider |
| Day 5 | UI polish, demo recording, GitHub documentation, final submission |

---

## Infrastructure: Tripartite Execution Architecture

| Component | Role | Key Technologies |
|---|---|---|
| **Replit Core** (Frontend & Web API) | UI Dashboard, API routing, async PDF extraction | Next.js/React, pdfplumber (async background) |
| **Supabase PostgreSQL + pgvector** | Vector & relational data store, hybrid search | pgvector `sparsevec` v0.7.0+, PL/pgSQL RRF function |
| **RunPod GPU ($25 credit)** | Heavy ML inference (embeddings + LLM evaluator) | BGE-M3 via vLLM, Llama-3-8B/Qwen, Pydantic/Instructor |

**Data stored in Supabase:** ESCO taxonomy (skills, occupations), O*NET tasks & work activities, MASCO 2020 crosswalk, UNSD SDG metadata tables, occupation AI exposure indices.

**Services on RunPod:**
- BGE-M3 `/embed` endpoint → returns `{ dense_vector, sparse_vector, colbert_vecs }` in a single GPU forward pass
- LLM evaluator endpoint (Micro-Task Simulation, Feature 4) — closed, JSON-only output via Instructor

---

## FEATURE 1: Skills Profile Intake

> **Goal:** Extract skill data from user CV/form into a **structured profile vector (JSON)** normalized to ESCO IDs, ready for comparative matching.

### Feature 1 Goals

- [ ] Users can upload a CV (PDF) or fill out a form/questionnaire
- [ ] System extracts skills in a structured manner using Structured Outputs (no free-form text)
- [ ] Every extracted skill is mapped to an `esco_id` from the ESCO dataset
- [ ] User profile is persisted as standardized JSON in the database
- [ ] Profile embedding vectors (dense + sparse) computed and stored for Feature 3

---

### Feature 1 Sub-steps

#### 1.1 - Dataset Setup and Database Schema

- [ ] Download ESCO dataset from https://esco.ec.europa.eu/en/use-esco/download (CSV or JSON-LD format)
- [ ] Create `skills` table: `esco_id`, `preferred_label`, `alt_labels`, `skill_type`, `description`, `broader_skill_id`
- [ ] Create `occupations` table: `esco_id`, `preferred_label`, `description`, `skill_ids[]`
- [ ] Generate 20-50 synthetic demo profiles in JSON format (fictitious names, fictitious background, skills mapped to ESCO IDs)
- [ ] **Do NOT use real CV datasets** (e.g., HuggingFace `datasetmaster/resumes`) — PII violation risk

#### 1.2 - CV / Form Parser (`pdfplumber` — MIT License, Apache 2.0 Compatible)

- [ ] Implement PDF parser using `pdfplumber` (Python)
  - **Rationale:** pdfplumber uses pure-Python geometric character analysis (pdfminer.six), achieving high-precision table/column layout reconstruction from multi-column resumes. MIT license is fully compatible with Apache 2.0 repository requirements.
  - **Rejected alternatives:** PyMuPDF (AGPL-3.0 — license viral effect, incompatible with public Apache 2.0 repo); Kreuzberg (secondary option only if OCR/scanned PDF is needed)
- [ ] Build fallback form/questionnaire if user has no CV (manual entry: skills, years of experience, interests)
- [ ] Validate raw text extraction from PDF uploads
- [ ] Handle async loading in UI (loading skeletons) to mask pdfplumber's ~8-15s/100-page latency

#### 1.3 - Structured Output Extraction (Primary Algorithm: Pydantic Structured Outputs)

- [ ] Set up Pydantic schema (Python) or Zod schema (TypeScript) with 3 mandatory categories:
  - [ ] `hard_skills` (e.g., Python, SQL, Machine Learning)
  - [ ] `soft_skills` (e.g., Stakeholder Management, Communication)
  - [ ] `experience_years` (integer)
- [ ] Send extracted CV text to LLM with Structured Output instructions (output MUST be rigid JSON, never conversational prose)
  - LLM acts solely as a **Named Entity Recognition agent** — no free-form narration
- [ ] Record a `confidence_score` for each mapping; if confidence is low, do not force an ESCO ID assignment
- [ ] Validate output: ensure each skill resolves to a valid `esco_id` in the ESCO table
- [ ] Pydantic schema → PostgreSQL column compatibility eliminates intermediate data cleaning layers

#### 1.4 - Text Embedding (BGE-M3 Dense + Sparse Embeddings via RunPod)

- [ ] Deploy **BGE-M3** on RunPod GPU endpoint via vLLM container
  - A single forward pass produces simultaneously: **Dense vector** + **Sparse vector** + **ColBERT multi-vector**
  - Supports 100+ languages: Bahasa Melayu, Mandarin, and English all map to the same universal vector space without a translation layer
- [ ] Store `user_dense_vector` (type `vector`) and `user_sparse_vector` (type `sparsevec`) in Supabase pgvector
- [ ] Verify synonym resolution: "Data Analysis", "Data Processing", "Data Analytics" → closely clustered dense vectors

#### 1.5 - Output and Verification

- [ ] Final output per user: `user_id`, `hard_skills`, `soft_skills`, `experience_years`, `user_dense_vector`, `user_sparse_vector`
- [ ] Test with at least 3 distinct synthetic demo profiles
- [ ] Verify that no real/personal CV data is used in the demo

---

## FEATURE 2: AI-Trend Signal Layer (Cognitive Task Compression Index)

> **Goal:** Surface a nuanced AI disruption signal per occupation — distinguishing *Substitutive Compression* (repetitive cognitive tasks replaceable by AI) from *Complementary Compression* (high-reasoning tasks accelerated but not replaced by AI) — replacing passive job posting scraping with an academically grounded leading indicator.

### Feature 2 Goals

- [ ] Every occupation in the system has a **Cognitive Task Compression Index (CTCI)** score
- [ ] CTCI separates Substitutive Compression from Complementary Compression
- [ ] UI presents the signal as an informative indicator, not a scare metric
- [ ] Signal is based on validated academic indices (Felten AIOE, Eloundou GPTs-are-GPTs, Webb patent overlap), not web scraping

---

### Feature 2 Sub-steps

#### 2.1 - Academic AI Exposure Metrics Integration

- [ ] Acquire **AIOE** data (Felten, Raj & Seamans): maps 10 AI capabilities against O*NET ability scores per occupation
- [ ] Acquire **GPTs-are-GPTs** exposure data (Eloundou et al.): ratio of tasks completable 50% faster by LLMs without quality degradation
- [ ] Acquire **Webb patent-based AI exposure scores**: purely lexical overlap between AI patent vocabulary and O*NET task descriptions (lowest human-judgment bias)
- [ ] Store all three in `occupation_ai_exposure`: `onet_soc_code`, `aioe_score`, `gpts_score`, `webb_score`

#### 2.2 - Critical Bias Awareness and CTCI Formulation

> **Key research finding (Rai 2026):** AIOE and GPTs scores correlate r=+0.85 with cognitive content intensity, NOT true AI replaceability — the "Human Judgment Halo Effect". Webb patent score is more objective; weight it more heavily.

- [ ] Compute **CTCI** per occupation:
  ```
  CTCI = (0.5 * Webb_score) + (0.25 * AIOE_score) + (0.25 * GPTs_score)
  ```
- [ ] Classify each occupation:
  - **Substitutive Compression:** High CTCI + low O*NET reasoning complexity → AI replaces repetitive execution
  - **Complementary Compression:** High CTCI + high O*NET reasoning complexity → AI accelerates execution but cannot replace judgment/leadership

#### 2.3 - O*NET + OpenDOSM Signal Enrichment

- [ ] Join `occupation_ai_exposure` with O*NET task-level data to compute reasoning intensity per occupation
- [ ] Pull latest OpenDOSM Job Market Insights (quarterly) for Malaysian vacancy counts per occupation
- [ ] Store in `occupation_my_signal`: `masco_code`, `onet_soc_code`, `vacancy_count`, `period`, `state`

#### 2.4 - UI Display: CTCI Widget (Embedded in Feature 3 Role Cards)

- [ ] Display CTCI score alongside each recommended role
- [ ] Show compression type label: "Substitutive" (amber indicator) vs "Complementary" (green indicator)
- [ ] Tooltip: brief `compression_reasoning` explaining the distinction (non-alarmist framing)
- [ ] Show Malaysian vacancy trend from DOSM as local demand context

---

## FEATURE 3: Future-Role Matching + Skill Gap Analysis

> **Goal:** Compute a mathematically defensible **Match Score (%)** between user profiles and future roles using BGE-M3 Hybrid Search (Dense + Sparse + RRF), and pinpoint specific **Skill Gaps** — delivering transparent, explainable, hallucination-free results.

### Feature 3 Goals

- [ ] Rank the best-fitting future roles for the user (with percentage scores)
- [ ] Every role has a Match Score computed deterministically (not hallucinated or guessed by an LLM)
- [ ] Identify exactly which skills the user lacks (Must-Learn Skill Gap)
- [ ] Output is readily explainable to judges: mathematical formula exposed/documented
- [ ] MASCO 2020 crosswalk used for Malaysian occupational context validation

---

### Feature 3 Sub-steps

#### 3.1 - Role and Skill Requirements Data Setup

- [ ] Ingest ESCO occupations <-> skills (essential vs optional per occupation)
- [ ] Enrich with O*NET: append `tasks`, `work_activities`, `knowledge` per occupation
- [ ] Create `role_required_skills`: `role_id`, `skill_id`, `is_essential` (bool), `weight`
- [ ] Load **MASCO 2020 crosswalk**: map `masco_code` (6-digit, 6,366 unit groups) to `onet_soc_code` and `esco_id`
- [ ] Validate role relevance with DOSM Job Market Insights (Malaysian labor market)
- [ ] Generate `role_dense_vector` and `role_sparse_vector` for each role via BGE-M3 RunPod endpoint

#### 3.2 - BGE-M3 Hybrid Search: Dense + Sparse + RRF (Primary Algorithm)

**Why Hybrid Search over plain Cosine Similarity:**
- Dense vectors alone fail on exact technical keywords: "React.js" vs "Vue.js" cluster too close; "OAuth2" vs "SAML" appear semantically interchangeable — they are NOT
- Sparse vectors (SPLADE-style) do exact keyword matching with statistical significance weights
- BGE-M3 produces dense + sparse + ColBERT in a **single GPU forward pass** — no extra inference cost

- [ ] Deploy BGE-M3 on RunPod via vLLM; expose `/embed` endpoint returning `{ dense_vector, sparse_vector, colbert_vecs }`
- [ ] Store role vectors in Supabase:
  - `vector` type → dense embeddings
  - `sparsevec` type → sparse embeddings (pgvector v0.7.0+)
- [ ] Implement **Reciprocal Rank Fusion (RRF)** PL/pgSQL function in Supabase:
  ```sql
  -- RRF: 1/(k + rank) summed across dense and sparse rank lists
  CREATE OR REPLACE FUNCTION hybrid_search(
    query_dense vector, query_sparse sparsevec, k int DEFAULT 10
  )
  RETURNS TABLE(role_id text, rrf_score float) AS $$
    WITH dense_rank AS (
      SELECT role_id, ROW_NUMBER() OVER (ORDER BY dense_vector <=> query_dense) AS rank
      FROM role_vectors
    ),
    sparse_rank AS (
      SELECT role_id, ROW_NUMBER() OVER (ORDER BY sparse_vector <#> query_sparse) AS rank
      FROM role_vectors
    )
    SELECT COALESCE(d.role_id, s.role_id),
           COALESCE(1.0/(60+d.rank), 0) + COALESCE(1.0/(60+s.rank), 0) AS rrf_score
    FROM dense_rank d FULL OUTER JOIN sparse_rank s ON d.role_id = s.role_id
    ORDER BY rrf_score DESC LIMIT k;
  $$ LANGUAGE sql;
  ```
- [ ] Input: `user_dense_vector` + `user_sparse_vector` (from Feature 1) vs all roles
- [ ] Output: ranked `(role_id, rrf_score)` list

#### 3.3 - Weighted Hybrid Scoring (Supporting Algorithm)

- [ ] Compute final composite score:
  ```
  Final Score = (0.5 * RRF_Score) + (0.3 * Hard_Skill_Coverage) + (0.2 * Seniority_Match)
  ```
- [ ] `Hard_Skill_Coverage`: % of essential hard skills possessed by user (Set Intersection / ESCO essential flags)
- [ ] `Seniority_Match`: compare user `experience_years` with role seniority band
- [ ] Expose full score breakdown in UI (transparency for judges)

#### 3.4 - Skill Gap Analysis (Set Difference Algorithm)

- [ ] Implement:
  ```
  Skill Gap = Role Required Skills — User Skills   [Set Difference: T \ U]
  ```
- [ ] Categorize:
  - **Core Gap:** missing ESCO essential skills → heavy penalty, labeled "Must Learn"
  - **Supporting Gap:** missing optional skills → minor penalty, labeled "Recommended"
- [ ] Output ordered `must_learn_skills[]` ranked by urgency

#### 3.5 - Output and Verification

- [ ] Final recommendation payload per role:
  ```json
  {
    "target_role": "AI Safety & Ethics Auditor",
    "esco_id": "esco:2512",
    "match_score": 0.82,
    "score_breakdown": {
      "rrf_score": 0.85,
      "hard_skill_coverage": 0.75,
      "seniority_match": 0.90
    },
    "skills_gap": [
      {"skill": "Algorithmic Bias Testing", "type": "core", "urgency": "high"},
      {"skill": "EU AI Act Compliance", "type": "supporting", "urgency": "medium"}
    ],
    "sdg_alignment": [],
    "ctci": {
      "score": 0.72,
      "compression_type": "Complementary",
      "reasoning": "High-reasoning AI governance role — AI accelerates documentation but cannot replace ethical judgment."
    }
  }
  ```
- [ ] Display top 3-5 matched roles on UI
- [ ] Test with at least 3 distinct demo profiles

---

## FEATURE 4: Personalised Reskilling Pathway (Micro-Task Simulation)

> **Goal:** Replace passive course-link directories with **Interactive Micro-Task Simulation (Proof-of-Capability)** — users are tested directly on skill gap scenarios, and a sandboxed LLM evaluator returns structured JSON feedback (score + constructive reasoning).

### Feature 4 Goals

- [ ] Users receive a contextual skill simulation task (not a reading list) per identified skill gap
- [ ] Isolated LLM evaluator (no free-form generative capability) assesses user responses
- [ ] Evaluator returns structured JSON: `{ score_percent, improvement_reasoning, missing_concepts[] }`
- [ ] Zero "AI slop" — LLM acts only as a rubric-based evaluator, never as a content generator

---

### Feature 4 Sub-steps

#### 4.1 - Scenario Bank from O*NET Task Statements

- [ ] Pull O*NET task statements for each skill gap identified in Feature 3
- [ ] Curate 1-3 fictionalized scenario prompts per ESCO skill category
  - Example: *"Given this code snippet with a bias vulnerability, propose a 5-line governance policy"*
- [ ] Store in `simulation_tasks`: `skill_id`, `scenario_text`, `rubric_criteria[]`

#### 4.2 - Isolated LLM Evaluator (RunPod — same container as embedding server)

- [ ] Deploy Llama-3-8B or Qwen variant on RunPod via vLLM + Pydantic/Instructor output enforcement
- [ ] Prompt-injection restrictions: closed evaluator, no open-ended generation allowed
- [ ] Evaluator input: `{ user_response, rubric_criteria[], skill_context }` → returns:
  ```json
  {
    "score_percent": 72,
    "improvement_reasoning": "Policy addresses bias detection but lacks an escalation procedure.",
    "missing_concepts": ["escalation matrix", "audit trail documentation"]
  }
  ```
- [ ] Validate output against Pydantic schema before returning to frontend

#### 4.3 - UI Integration

- [ ] Display simulation task card per skill gap on `/pathway/[roleId]`
- [ ] Text input or code editor for user response
- [ ] Show evaluator feedback: score bar + improvement_reasoning + missing_concepts[]
- [ ] Allow retry for failed simulations

---

## FEATURE 5: SDG Mapping

> **Goal:** Embed **official UN SDG labels** as structured metadata on each Role within the Feature 3 output — non-decorative, auditable, and seamlessly integrated with zero extra pipelines.

### Feature 5 Goals

- [ ] Every recommended role links to at least one SDG
- [ ] SDG mapping sourced from the official UN SDG API (no arbitrary LLM inventions)
- [ ] UI displays official SDG badges/icons with hoverable tooltips explaining impact
- [ ] Every link has auditable `impact_reasoning`

---

### Feature 5 Sub-steps

#### 5.1 - UN SDG API Setup and Reference Tables

- [ ] Access UN SDG API: https://unstats.un.org/sdgs/UNSDGAPIV5/swagger/index.html
- [ ] Fetch and store: `GET /v1/sdg/Goal/List` → `sdg_goals` table
- [ ] Fetch and store: `GET /v1/sdg/Goal/{goalCode}/Target/List` → `sdg_targets` table
- [ ] Fetch and store: `GET /v1/sdg/Indicator/List` → `sdg_indicators` table
- [ ] Create `role_sdg`: `role_id`, `sdg_goal`, `sdg_target`, `relationship_type`, `evidence`, `source`

#### 5.2 - Role → SDG Curated Mapping Table

- [ ] Build curated mapping: ESCO occupations → SDG targets (no unverified LLM generation)
- [ ] Per mapping, record:
  - `sdg_goal` (integer 1-17)
  - `sdg_target` (e.g., "8.2", "4.4")
  - `relationship_type` ("supports" / "enables" / "contributes")
  - `impact_reasoning`: 1 concise sentence
  - `source`: "UNSD SDG API"
- [ ] Priority SDGs: 4 (Quality Education), 8 (Decent Work), 9 (Industry & Innovation), 10 (Reduced Inequalities)
- [ ] At least 1 role must link to multiple SDGs (showcase multidimensional impact)

#### 5.3 - Integration into Feature 3 Output (Zero Extra Pipelines)

- [ ] Feature 3 role recommendation → automated JOIN to `role_sdg` → append `sdg_alignment[]` to JSON output
- [ ] Metadata injection is a static JOIN — zero runtime LLM call, zero latency overhead
- [ ] Sample output:
  ```json
  {
    "sdg_alignment": [
      {
        "sdg_goal": 8,
        "sdg_name": "Decent Work and Economic Growth",
        "target": "8.2",
        "impact_reasoning": "Ensures AI deployment does not eliminate decent work rights and transparency.",
        "source": "UNSD SDG API"
      }
    ]
  }
  ```
- [ ] Verify: no mapping generated on-the-fly without an auditable curated entry

#### 5.4 - UI: SDG Badge Display

- [ ] Reusable `SdgBadge` component: `sdg_goal` prop → official UN color + number
- [ ] Hover/click → shadcn Dialog: `sdg_name`, `target`, `impact_reasoning`
- [ ] Use official UN SDG color palette and icons only
- [ ] Optional: "SDG Contribution View" aggregated across all recommended roles

#### 5.5 - Verification

- [ ] All mappings attribute `source: "UNSD SDG API"`
- [ ] Zero ungrounded SDG tags from free-form LLM
- [ ] Publish `role_sdg` curated table in GitHub repo with rationale
- [ ] Test: badges render, tooltips function

---

## FEATURE 6: Handling Uncertainty (Career Stress-Test Engine)

> **Goal:** Model career trajectory divergence under different AI disruption scenarios through a **parameterized Career Stress-Test** — interactive slider shifts role rankings and skill recommendations under Moderate vs Fast AI Disruption, using O*NET cognitive task matrices as the penalty engine.

### Feature 6 Goals

- [ ] UI exposes interactive scenario toggle: "Moderate AI Adoption" vs "Fast AI Disruption"
- [ ] Changing scenario dynamically reweights role rankings and skill recommendations
- [ ] Promotes Defensive Reskilling (soft skills, complex management) under fast disruption
- [ ] All disruption logic is fully deterministic — no LLM in scenario modeling

---

### Feature 6 Sub-steps

#### 6.1 - Disruption Penalty Matrix

- [ ] Use O*NET cognitive task data to compute **Task Compression Ratio** per occupation:
  - High repetitive cognitive routine → high penalty multiplier under fast disruption
  - Low routine + high complex judgment → low penalty (complementary, resilient)
- [ ] Store in `occupation_disruption_matrix`: `onet_soc_code`, `routine_cognitive_ratio`, `disruption_penalty_fast`, `disruption_penalty_moderate`
- [ ] Base penalties on AIOE / Webb / Eloundou indices from Feature 2

#### 6.2 - Parameterized Scenario Engine

- [ ] Scenario logic:
  ```
  Moderate:        Final Score = standard Feature 3 hybrid score (no penalty)
  Fast Disruption: Final Score = hybrid_score * (1 - disruption_penalty_fast)
                   + bonus_amplifier for soft_skill_intensity
  ```
- [ ] Under "Fast AI Disruption": high `routine_cognitive_ratio` roles drop; complex judgment / negotiation / stakeholder management roles rise via RRF amplification
- [ ] All score modifications exposed in `score_breakdown` payload

#### 6.3 - UI: AI Shock Slider

- [ ] Scenario toggle/slider on `/results` page
- [ ] On toggle: re-fetch `GET /api/match?user_id=...&scenario=fast`
- [ ] Animated role card reordering (framer-motion staggered transition)
- [ ] Delta indicators: roles that rose (↑) or fell (↓) between scenarios
- [ ] Explanatory callout: "Under Fast AI Disruption, roles requiring complex human judgment are prioritized"

---

## Overall Technical Architecture (Pipeline)

```text
[CV Upload / Input Form]
        |
        v
(1. PDF Parser: pdfplumber) ──> Raw text extraction
        |
        v
(2. Structured Output: Pydantic Schema) ──> JSON (hard_skills, soft_skills, years)
        |
        v
(3. ESCO Normalization) ──> Map to esco_id
        |
        v
(4. BGE-M3 via RunPod) ──> user_dense_vector + user_sparse_vector
        |
        v
(5. Hybrid Search: Supabase pgvector RRF) ──> Ranked roles (Dense + Sparse + RRF)
        |
        v
(6. Weighted Hybrid Scoring) ──> Final Score (%) + Ranking
        |
        v
(7. Set Difference: Gap Analysis) ──> must_learn_skills[]
        |
        v
(8. JOIN role_sdg) ──> sdg_alignment[] appended
        |
        v
(9. JOIN occupation_disruption_matrix) ──> ctci + compression_type appended
        |
        v
[Output: Ranked Roles + Match Score + Skill Gap + SDG Badges + CTCI Signal]
        |
        +---> Feature 4: Simulation task per skill gap --> LLM Evaluator JSON feedback
        +---> Feature 6: Scenario toggle --> re-rank with disruption penalty matrix
```

---

## Final Submission Checklist

- [ ] GitHub repository public / accessible to judges
- [ ] Live demo: at least Feature 3 working end-to-end
- [ ] Every recommendation cites a credible source (no fabricated jobs, statistics)
- [ ] Solution framed as AI supporting human career decisions, not replacing judgment
- [ ] Exclusively uses public, open, or synthetic data — no real CVs or personal data
- [ ] All datasets: version, retrieval date, source URLs documented in repo
- [ ] CTCI signal clearly distinguishes Substitutive vs Complementary Compression
- [ ] SDG linkages are meaningful and contextualized, never decorative
- [ ] Career Stress-Test slider functional: visibly different rankings between scenarios
- [ ] BGE-M3 RunPod endpoint live, returning dense + sparse vectors
- [ ] Supabase RRF hybrid search function deployed and tested
- [ ] MASCO 2020 crosswalk loaded and mapped to ESCO/O*NET codes

---

> **References:**
> - [`algorithm_consideration.md`](./algorithm_consideration.md) — Algorithm architecture
> - [`deep_research.md`](./deep_research.md) — Full architectural rationale, algorithm justifications, academic citations
> - [`deep_research_summary.md`](./deep_research_summary.md) — Concise method + dataset mapping per feature
> - [`Datasets.md`](./Datasets.md) — Recommended datasets per feature
> - [`src/Domain 1.md`](./src/Domain%201.md) — Problem statement and judging rubric

---

## FRONTEND: Next.js + Tailwind CSS + shadcn/ui

> **Goal:** Build a clean, responsive dashboard guiding the user from CV upload to ranked future roles with match scores, skill gap display, SDG badges, CTCI signal, and Career Stress-Test slider.

### Full Tech Stack (Frontend)

| Layer | Library / Tool | Purpose |
|---|---|---|
| Framework | next.js (App Router) | Pages, routing, server-side API calls |
| Styling | tailwindcss | Utility-first CSS, responsive layout |
| UI Components | shadcn/ui | Card, Badge, Progress, Tabs, Dialog, Slider, Skeleton |
| Icons | lucide-react | Icon set (bundled with shadcn) |
| Data Visualization | recharts | Match score bar, skill gap radar, CTCI signal |
| File Upload | react-dropzone | Drag-and-drop CV/PDF upload |
| Data Fetching | @tanstack/react-query | Async fetching, caching, loading/error states |
| Animations | framer-motion | Card entrance, scenario re-rank transitions |
| HTTP Client | axios | Typed API calls to FastAPI backend |

### Missing Libraries (must install)

| Library | Reason |
|---|---|
| recharts | Match score bars, skill gap radar chart |
| react-dropzone | Drag-and-drop CV upload UX |
| @tanstack/react-query | Async state management |
| framer-motion | Animations for role cards and scenario transitions |
| axios | Structured HTTP calls to FastAPI backend |

---

### Frontend Sub-steps

#### F.1 - Project Initialization

- [ ] Scaffold Next.js project:
  `npx create-next-app@latest frontend --typescript --tailwind --app --src-dir`
- [ ] Initialize shadcn/ui:
  `npx shadcn@latest init`
- [ ] Install missing libraries:
  `npm install recharts react-dropzone @tanstack/react-query framer-motion axios`
- [ ] Install shadcn components:
  `npx shadcn@latest add card badge progress tabs dialog button input skeleton slider`
- [ ] Configure `.env.local`:
  `NEXT_PUBLIC_API_URL=http://localhost:8000`

#### F.2 - Page Structure (App Router)

- [ ] `/` (Home) — Landing page: hero section + "Get Started" CTA
- [ ] `/profile` — CV upload form + manual skills form
- [ ] `/results` — Ranked role cards + match scores + skill gaps + scenario slider
- [ ] `/pathway/[roleId]` — Micro-Task Simulation cards per skill gap
- [ ] `components/ui/` — Reused shadcn components

#### F.3 - CV Upload Page (`/profile`)

- [ ] Drag-and-drop zone: react-dropzone (PDF only)
- [ ] Fallback manual form: skill tags, years of experience slider, interests select
- [ ] POST `/api/profile` with PDF or JSON payload
- [ ] Loading skeleton while backend processes (covers pdfplumber latency)
- [ ] Handle errors: invalid file type, extraction failure

#### F.4 - Results Dashboard (`/results`)

- [ ] Fetch ranked roles: `GET /api/match?user_id=...&scenario=moderate`
- [ ] Display top 3-5 role cards:
  - [ ] Role title + ESCO ID
  - [ ] Match score as shadcn Progress bar + percentage
  - [ ] Score breakdown tooltip (RRF / Hard Skill / Seniority weights)
  - [ ] Skill gap Badges (red = core, yellow = supporting)
  - [ ] SDG badges + Dialog popup (`impact_reasoning`)
  - [ ] CTCI indicator: Substitutive (amber) / Complementary (green) + score
- [ ] framer-motion staggered card entrance animation
- [ ] recharts BarChart: match score comparison across roles
- [ ] **Career Stress-Test Slider** (Feature 6): "Moderate" ↔ "Fast Disruption" — re-fetch + animated reorder

#### F.5 - SDG Badge Component

- [ ] Reusable `SdgBadge` component (prop: `sdg_goal`)
- [ ] Official SDG number + UN color-coded circle
- [ ] Hover/click → shadcn Dialog: `sdg_name`, `target`, `impact_reasoning`

#### F.6 - Skill Gap Radar Chart (Optional — High Visual Impact)

- [ ] recharts RadarChart: user profile (blue) vs role requirements (red dashed)
- [ ] Axes: Technical, Domain, Soft Skills, Seniority

#### F.7 - Micro-Task Simulation Page (`/pathway/[roleId]`)

- [ ] One simulation card per missing skill
- [ ] Text input or code editor for response
- [ ] POST `/api/simulate` with `{ skill_id, user_response }`
- [ ] Feedback card: score_percent bar + improvement_reasoning + missing_concepts[]
- [ ] Allow retry

#### F.8 - API Integration Layer

- [ ] `lib/api.ts` with typed axios functions:
  - `uploadProfile(file)` → `UserProfile`
  - `getMatchResults(userId, scenario)` → `RoleMatch[]`
  - `getReskillPathway(roleId)` → `Pathway`
  - `submitSimulation(skillId, response)` → `SimulationResult`
- [ ] Wrap with `@tanstack/react-query` `useQuery` / `useMutation`
- [ ] Handle loading, error, and empty states

#### F.9 - Final UI Polish

- [ ] Mobile-responsive layout (Tailwind breakpoints: sm, md, lg)
- [ ] Dark mode via Tailwind `dark:` + next-themes
- [ ] Clear hover/focus states on all interactive elements
- [ ] Lighthouse target: Performance > 80, Accessibility > 90

---

> **Note:** recharts, react-dropzone, @tanstack/react-query, framer-motion, and axios are NOT included with Next.js, Tailwind, or shadcn/ui by default and must be explicitly installed.