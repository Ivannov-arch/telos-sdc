# WORKSTEPS - SDC XMUM Hackathon: Domain 1 (Aiversecity)

> **Context:** This document outlines the execution roadmap for all 6 features of **Domain 1: The Aiversecity Future-Ready Workforce**, organized into 3 development phases.
> Based on [`algorithm_consideration.md`](./algorithm_consideration.md), [`deep_research.md`](./deep_research.md), and the judging rubric from [`src/Domain 1.md`](./src/Domain%201.md).
> Dataset sources refer to [`Datasets.md`](./Datasets.md). Team task division & daily schedules → [`TASKS.md`](./TASKS.md).

---

## Core Paradigm: AI-Grounded Determinism (Zero AI Slop)

The foundational design principle for all features is a strict separation of responsibilities:

- **AI/LLM tasks only:** Named Entity Recognition (CV extraction), synonym normalization via embeddings, and isolated Micro-Task Simulation evaluator (Feature 4).
- **Deterministic / math tasks:** Match Score computation, Skill Gap analysis, Career Stress-Test, and SDG metadata injection — all governed by pure mathematical algorithms and vector space search, **never** free-form LLM narration.

This architecture guarantees reproducible, auditable, and hallucination-free outputs that will withstand scrutiny from hackathon judges.

---

## Team Ownership & Role Legend

| Role Identifier | Primary Focus | Core Deliverables | Phase Assigned |
|---|---|---|---|
| **Person A (Backend Lead)** | Database, Vector Functions & Match Engine | Supabase pgvector, ESCO/MASCO seeding, RRF Hybrid Search, Skill Gap Set Difference, FastAPI `/api/match` | Phase 1 (MVP Core) |
| **Person B (AI/ML Engineer)** | Inference Infrastructure & Profile Parsing | RunPod BGE-M3 deployment, `pdfplumber` CV parser, Pydantic Structured Output, vector generation, vLLM LLM evaluator | Phase 1 (MVP Core) |
| **Person C (Frontend Lead)** | User Interface & SDG Visualization | Next.js App Router, Tailwind + shadcn/ui dashboard, `/profile` & `/results` pages, SDG badges & metadata, Framer Motion | Phase 1 (MVP Core) |
| **Person D (Phase 2 Owner)** | Reskilling Pathway & Simulation Engine | Feature 4 Micro-Task Simulation, O*NET task statement curation, rubric prompt engineering, `POST /api/simulate`, `/pathway/[roleId]` UI | Phase 2 (Reskilling) |
| **Person E (Phase 3 Owner)** | AI Risk Analytics & Stress-Test Engine | Feature 2 CTCI Index, Feature 6 Career Stress-Test, disruption penalty matrix, scenario reweighting logic, shock slider UI | Phase 3 (Analytical) |

---

## Development Phases

| Phase | Features | Days | Assigned To | Priority |
|---|---|---|---|---|
| **Phase 1 — MVP Core Pipeline** | Feature 1 (Skills Intake) + Feature 3 (Role Matching + Skill Gap) + Feature 5 (SDG Mapping) | Day 1–3 | Person A, Person B, Person C | 🔴 Critical Path — Demo must show this working |
| **Phase 2 — Reskilling Enrichment** | Feature 4 (Personalised Reskilling / Micro-Task Simulation) | Day 3–4 | Person D (prep Day 1–2, build Day 3–4) | 🟡 High — Starts as soon as Feature 3 Skill Gap output is ready |
| **Phase 3 — Analytical Overlay** | Feature 2 (AI-Trend Signal / CTCI) + Feature 6 (Career Stress-Test Engine) | Day 4–5 | Person E (prep Day 1–3, build Day 4–5) | 🟢 Nice-to-Have — Both share O*NET disruption data; built together |

### Phase Dependency Logic

```
Feature 1 (Skills Intake) [Person B]
    └──► Feature 3 (Role Matching + Skill Gap) [Person A]  ◄── Phase 1 critical path
              └──► Feature 5 (SDG Mapping) [Person C & A]      (must be demo-ready by Day 3)
              │
              └──► Feature 4 (Micro-Task Sim) [Person D]    ◄── Phase 2 starts Day 3
                        (consumes must_learn_skills[] from Feature 3)
              │
              └──► Feature 6 (Stress-Test) [Person E]        ◄── Phase 3 starts Day 4
                        (reweights Feature 3 scores)
                        │
Feature 2 (CTCI Signal) [Person E] ┘                         ◄── Phase 3 (feeds F6 penalty matrix)
    (O*NET cognitive data → disruption_penalty)
```

**Why Feature 4 in Phase 2 (not Phase 3)?**
Feature 4 directly consumes `must_learn_skills[]` produced by Feature 3. The moment Feature 3's skill gap output is wired (end of Day 3), Feature 4 can start building on top with no blocking dependency. It's a natural forward extension of the MVP pipeline.

**Why Features 2 & 6 together in Phase 3?**
Both features load the same O*NET cognitive task data (AIOE/Webb/Eloundou indices). Feature 2 computes the CTCI score; Feature 6 uses that same score to build the disruption penalty matrix. Building them in parallel in Phase 3 avoids redundant data loading and enables code reuse.

---

## Master Dependency & Blocking Crosswalk (Who Waits for Whom)

When executing any step, consult this matrix before proceeding. If a prerequisite step is marked **BLOCKED**, you cannot finalize your step until the listed person completes their handoff.

| Substep | Step Name | Owner | ⏳ Blocking Dependency (Waits for...) | 🚀 Unblocks (Next in line) |
|---|---|---|---|---|
| **1.1** | DB Schema & ESCO/MASCO Seeding | **Person A** | None (Starts Day 1) | Person B (1.3, 1.4), Person C (5.2), Person D (4.1) |
| **1.2** | CV Parser (`pdfplumber`) & Form | **Person B** (& C) | None (Starts Day 1) | Person B (1.3 - feeds extracted text) |
| **1.3** | Structured Output Extraction (Pydantic) | **Person B** | ⏳ **Person A (Step 1.1)** [ESCO skills table] & **Person B (Step 1.2)** [raw CV text] | Person B (1.4 - structured profile to embed), Person A (3.4) |
| **1.4** | BGE-M3 Embeddings via RunPod | **Person B** | ⏳ **Person B (Day 1)** [RunPod endpoint live] & **Person A (Step 1.1)** [Supabase table schema] & **Person B (Step 1.3)** [user profile] | Person A (3.1 & 3.2 - hybrid search vectors ready) |
| **1.5** | Feature 1 Output & Verification | **Person B** (& A) | ⏳ **Person B (Step 1.4)** [user vector saved in Supabase] | Person A (3.2 - input to hybrid search) |
| **3.1** | Role & Skill Requirements Data Setup | **Person A** | ⏳ **Person B (Step 1.4 / Day 1)** [RunPod BGE-M3 `/embed` live to generate role vectors] | Person A (3.2), Person C (5.2) |
| **3.2** | BGE-M3 Hybrid Search (RRF in Supabase) | **Person A** | ⏳ **Person A (Step 3.1)** [role vectors in DB] & **Person B (Step 1.4)** [user vector] | Person A (3.3 - RRF candidate list) |
| **3.3** | Weighted Hybrid Scoring | **Person A** | ⏳ **Person A (Step 3.2)** [RRF rank score] | Person A (3.5 - composite score) |
| **3.4** | Skill Gap Analysis (Set Difference `T \ U`) | **Person A** | ⏳ **Person A (Step 3.1)** [`role_required_skills`] & **Person B (Step 1.3)** [`user.hard_skills`] | **Person D (Step 4.1 & 4.3)** [feeds `must_learn_skills[]`], Person C (F.4) |
| **3.5** | Feature 3 Verification & `GET /api/match` | **Person A** | ⏳ **Person A (Steps 3.3 & 3.4)** [scoring + skill gaps functional] | Person C (F.4 - results page), Person D (Phase 2 launch) |
| **5.1** | UN SDG API Setup & Tables | **Person A** (& C) | None (Can start Day 1-2) | Person C (5.2 - curated mapping table) |
| **5.2** | Role → SDG Curated Mapping Table | **Person C** | ⏳ **Person A (Step 1.1 / 3.1)** [ESCO occupations table populated] | Person A (5.3 - static JOIN in API) |
| **5.3** | Integration of SDG into `/api/match` | **Person A** | ⏳ **Person C (Step 5.2)** [`role_sdg` table seeded] & **Person A (Step 3.5)** [`/api/match` live] | Person C (5.4 - frontend badge display) |
| **5.4** | UI: SDG Badge Display Component | **Person C** | ⏳ **Person A (Step 5.3)** [`sdg_alignment[]` returned in API response] | Phase 1 visual demo complete |
| **5.5** | Feature 5 Verification | **Person C** (& A) | ⏳ **Person C (Step 5.4)** & **Person A (Step 5.3)** | Phase 1 Sign-Off |
| **4.1** | Scenario Bank from O*NET Tasks | **Person D** | ⏳ **Person A (Step 1.1)** [ESCO skill IDs] & **Person A (Step 3.4)** [target gap types] | Person D (4.3 - DB scenario lookup) |
| **4.2** | Isolated LLM Evaluator (RunPod) | **Person D** (& B) | ⏳ **Person B (Day 4 / Day 1)** [RunPod vLLM LLM server live with Instructor] | Person D (4.3 - simulation grading engine) |
| **4.3** | Backend API `POST /api/simulate` | **Person D** (& A) | ⏳ **Person D (Step 4.1 & 4.2)** [scenarios + evaluator live] & **Person A (Step 3.4)** [`must_learn_skills[]`] | Person D (4.4 - frontend pathway page) |
| **4.4** | Frontend `/pathway/[roleId]` Page | **Person D** (& C) | ⏳ **Person C (Step F.2/F.4)** [router & results UI] & **Person D (Step 4.3)** [`/api/simulate` API operational] | Phase 2 End-to-End Test complete |
| **2.1** | Academic AI Exposure Metrics | **Person E** | None (Day 1–3 prep: download AIOE/Webb/GPTs data) | Person E (2.2 - feeds CTCI formula) |
| **2.2** | CTCI Formulation & Classification | **Person E** | ⏳ **Person E (Step 2.1)** [raw exposure indices loaded] | Person E (2.3, 2.4), Person E (6.1) |
| **2.3** | O*NET + OpenDOSM Signal Enrichment | **Person E** (& A) | ⏳ **Person A (Step 3.1)** [MASCO crosswalk & occupations table in Supabase] | Person E (2.4 - CTCI + Malaysian demand data) |
| **2.4** | UI: CTCI Widget on Role Cards | **Person E** (& C) | ⏳ **Person E (Step 2.2/2.3)** [CTCI computed] & **Person C (Step F.4)** [`/results` dashboard ready] | Feature 2 UI complete |
| **6.1** | Disruption Penalty Matrix | **Person E** | ⏳ **Person E (Step 2.2)** [CTCI scores ready] & **Person E (Step 2.1)** [O*NET cognitive task data] | Person E (6.2 - scenario reweighting) |
| **6.2** | Parameterized Scenario Engine | **Person E** (& A) | ⏳ **Person A (Step 3.5)** [`GET /api/match` live] & **Person E (Step 6.1)** [penalty matrix in DB] | Person E (& C) (6.3 - shock slider UI) |
| **6.3** | UI: AI Shock Slider on `/results` | **Person E** (& C) | ⏳ **Person E (Step 6.2)** [`?scenario=fast` API live] & **Person C (Step F.4)** [`/results` page live] | Phase 3 Complete |
| **F.1-F.3**| Frontend Project Setup & `/profile` | **Person C** | ⏳ **Person B (Step 1.3 / Day 2)** [FastAPI `POST /api/profile` endpoint live] | User intake interactive |
| **F.4** | Results Dashboard `/results` | **Person C** | ⏳ **Person A (Step 3.5 / Day 3)** [FastAPI `GET /api/match` endpoint live] | Phase 1 Core UI interactive |

---

## Timeline: 5-Day Hackathon

| Day | Phase 1 (3 people: Person A, Person B, Person C) | Phase 2 & 3 (2 people: Person D, Person E) |
|---|---|---|
| **Day 1** | **Person A:** Supabase schema + ESCO seeding + pgvector.<br>**Person B:** RunPod GPU + BGE-M3 deploy.<br>**Person C:** Next.js project scaffold + shadcn/ui. | **Person D (Prep):** Read O*NET docs, plan scenario bank.<br>**Person E (Prep):** Acquire AIOE, GPTs, and Webb AI exposure datasets. |
| **Day 2** | **Person A:** O*NET task enrichment + synthetic user profiles.<br>**Person B:** `pdfplumber` + Pydantic schema + `POST /api/profile`.<br>**Person C:** `/profile` UI page + UN SDG API data tables. | **Person D (Prep):** Curate scenario prompts for top 10 ESCO skills.<br>**Person E (Prep):** Load O*NET abilities + pull OpenDOSM Job Market data. |
| **Day 3** | **Person A:** PL/pgSQL RRF hybrid search + Set Difference skill gap + `GET /api/match`.<br>**Person B:** BGE-M3 vector generation & Supabase sync.<br>**Person C:** `/results` dashboard page + `SdgBadge` component. | **PHASE 2 STARTS (Person D):** Seed `simulation_tasks`, draft evaluator prompts, wire `POST /api/simulate`.<br>**Person E (Prep):** Compute CTCI scores + MASCO crosswalk alignment. |
| **Day 4** | **Person A:** Integrate SDG JOIN into `/api/match`, assist Person D & E.<br>**Person B:** RunPod LLM evaluator deploy (vLLM Llama-3/Qwen for Person D).<br>**Person C:** Full frontend wiring (`@tanstack/react-query`) + `/results` state. | **Person D:** Build `/pathway/[roleId]` UI + test evaluator feedback.<br>**PHASE 3 STARTS (Person E):** Day 4 AM: CTCI widget; Day 4 PM: Disruption penalty matrix + `?scenario=fast`. |
| **Day 5** | **Person A:** Code review + API latency tuning + README.<br>**Person B:** RunPod health checks + embedding cache verification.<br>**Person C:** Responsive polish + dark mode + Lighthouse audit. | **Person D:** End-to-end pathway verification + edge cases.<br>**Person E:** AI Shock Slider on `/results` + framer-motion re-rank testing. |

---

## Infrastructure: Tripartite Execution Architecture

| Component | Role | Key Technologies | Assigned Lead |
|---|---|---|---|
| **Replit Core** (Frontend & Web API) | UI Dashboard, API routing, async PDF extraction | Next.js/React, FastAPI, pdfplumber (async background) | **Person C** (Frontend) & **Person A** (API) |
| **Supabase PostgreSQL + pgvector** | Vector & relational data store, hybrid search | pgvector `sparsevec` v0.7.0+, PL/pgSQL RRF function | **Person A** (Backend Lead) |
| **RunPod GPU ($25 credit)** | Heavy ML inference (embeddings + LLM evaluator) | BGE-M3 via vLLM, Llama-3-8B/Qwen, Pydantic/Instructor | **Person B** (AI/ML Engineer) |

**Data stored in Supabase:** ESCO taxonomy (skills, occupations), O*NET tasks & work activities, MASCO 2020 crosswalk, UNSD SDG metadata tables, occupation AI exposure indices (AIOE/Webb/Eloundou), CTCI scores, disruption penalty matrix.

**Services on RunPod:**
- BGE-M3 `/embed` endpoint → returns `{ dense_vector, sparse_vector, colbert_vecs }` in a single GPU forward pass
- LLM evaluator endpoint (Micro-Task Simulation, Feature 4) — closed, JSON-only output via Instructor

---

---

# PHASE 1 — MVP Core Pipeline (Day 1–3)

> **Features:** 1 (Skills Profile Intake) + 3 (Future-Role Matching + Skill Gap) + 5 (SDG Mapping)  
> **Team Members Assigned:** Person A (Backend Lead), Person B (AI/ML Engineer), Person C (Frontend Lead)  
> **Exit Criteria:** End-to-end demo: user uploads CV → ranked roles with match scores, skill gaps, and SDG badges visible in UI.

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

#### 1.1 - Dataset Setup and Database Schema [Person A - Backend Lead]

> 👤 **Assigned To:** Person A (Backend Lead)  
> ⏳ **Blocking Dependency:** None (Starts Day 1 morning)  
> 🚀 **Unblocks:** Person B (Substeps 1.3, 1.4), Person C (Substep 5.2), Person D (Substep 4.1)

- [ ] Download ESCO dataset from https://esco.ec.europa.eu/en/use-esco/download (CSV or JSON-LD format)
- [ ] Create `skills` table: `esco_id`, `preferred_label`, `alt_labels`, `skill_type`, `description`, `broader_skill_id`
- [ ] Create `occupations` table: `esco_id`, `preferred_label`, `description`, `skill_ids[]`
- [ ] Generate 20-50 synthetic demo profiles in JSON format (fictitious names, fictitious background, skills mapped to ESCO IDs)
- [ ] **Do NOT use real CV datasets** (e.g., HuggingFace `datasetmaster/resumes`) — PII violation risk

#### 1.2 - CV / Form Parser (`pdfplumber` — MIT License, Apache 2.0 Compatible) [Person B - AI/ML & Person C - Frontend]

> 👤 **Assigned To:** Person B (AI/ML Engineer) for PDF extraction; Person C (Frontend Lead) for fallback UI form  
> ⏳ **Blocking Dependency:** None (Starts Day 1-2)  
> 🚀 **Unblocks:** Person B (Substep 1.3 - feeds raw text into structured extractor)

- [ ] Implement PDF parser using `pdfplumber` (Python)
  - **Rationale:** pdfplumber uses pure-Python geometric character analysis (pdfminer.six), achieving high-precision table/column layout reconstruction from multi-column resumes. MIT license is fully compatible with Apache 2.0 repository requirements.
  - **Rejected alternatives:** PyMuPDF (AGPL-3.0 — license viral effect, incompatible with public Apache 2.0 repo); Kreuzberg (secondary option only if OCR/scanned PDF is needed)
- [ ] Build fallback form/questionnaire if user has no CV (manual entry: skills, years of experience, interests)
- [ ] Validate raw text extraction from PDF uploads
- [ ] Handle async loading in UI (loading skeletons) to mask pdfplumber's ~8-15s/100-page latency

#### 1.3 - Structured Output Extraction (Primary Algorithm: Pydantic Structured Outputs) [Person B - AI/ML Engineer]

> 👤 **Assigned To:** Person B (AI/ML Engineer)  
> ⏳ **Blocking Dependency:** Waits for **Person A (Substep 1.1)** [ESCO database seeded] AND **Person B (Substep 1.2)** [raw CV text extracted]  
> 🚀 **Unblocks:** Person B (Substep 1.4 - vector embedding), Person A (Substep 3.4 - user skill gap comparison)

- [ ] Set up Pydantic schema (Python) or Zod schema (TypeScript) with 3 mandatory categories:
  - [ ] `hard_skills` (e.g., Python, SQL, Machine Learning)
  - [ ] `soft_skills` (e.g., Stakeholder Management, Communication)
  - [ ] `experience_years` (integer)
- [ ] Send extracted CV text to LLM with Structured Output instructions (output MUST be rigid JSON, never conversational prose)
  - LLM acts solely as a **Named Entity Recognition agent** — no free-form narration
- [ ] Record a `confidence_score` for each mapping; if confidence is low, do not force an ESCO ID assignment
- [ ] Validate output: ensure each skill resolves to a valid `esco_id` in the ESCO table
- [ ] Pydantic schema → PostgreSQL column compatibility eliminates intermediate data cleaning layers

#### 1.4 - Text Embedding (BGE-M3 Dense + Sparse Embeddings via RunPod) [Person B - AI/ML Engineer]

> 👤 **Assigned To:** Person B (AI/ML Engineer)  
> ⏳ **Blocking Dependency:** Waits for **Person B (Day 1)** [RunPod GPU live with BGE-M3 `/embed`] AND **Person A (Substep 1.1)** [Supabase `role_vectors` schema] AND **Person B (Substep 1.3)** [extracted user profile]  
> 🚀 **Unblocks:** Person A (Substeps 3.1 & 3.2 - hybrid search vectors ready)

- [ ] Deploy **BGE-M3** on RunPod GPU endpoint via vLLM container
  - A single forward pass produces simultaneously: **Dense vector** + **Sparse vector** + **ColBERT multi-vector**
  - Supports 100+ languages: Bahasa Melayu, Mandarin, and English all map to the same universal vector space without a translation layer
- [ ] Store `user_dense_vector` (type `vector`) and `user_sparse_vector` (type `sparsevec`) in Supabase pgvector
- [ ] Verify synonym resolution: "Data Analysis", "Data Processing", "Data Analytics" → closely clustered dense vectors

#### 1.5 - Output and Verification [Person B - AI/ML & Person A - Backend]

> 👤 **Assigned To:** Person B (AI/ML Engineer) & Person A (Backend Lead)  
> ⏳ **Blocking Dependency:** Waits for **Person B (Substep 1.4)** [dense + sparse vectors stored in Supabase]  
> 🚀 **Unblocks:** Person A (Substep 3.2 - ready for hybrid search query)

- [ ] Final output per user: `user_id`, `hard_skills`, `soft_skills`, `experience_years`, `user_dense_vector`, `user_sparse_vector`
- [ ] Test with at least 3 distinct synthetic demo profiles
- [ ] Verify that no real/personal CV data is used in the demo

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

#### 3.1 - Role and Skill Requirements Data Setup [Person A - Backend Lead]

> 👤 **Assigned To:** Person A (Backend Lead)  
> ⏳ **Blocking Dependency:** Waits for **Person B (Substep 1.4 / Day 1)** [RunPod BGE-M3 `/embed` endpoint live to compute `role_vectors`]  
> 🚀 **Unblocks:** Person A (Substep 3.2 - hybrid search target space), Person C (Substep 5.2 - occupation metadata)

- [ ] Ingest ESCO occupations <-> skills (essential vs optional per occupation)
- [ ] Enrich with O*NET: append `tasks`, `work_activities`, `knowledge` per occupation
- [ ] Create `role_required_skills`: `role_id`, `skill_id`, `is_essential` (bool), `weight`
- [ ] Load **MASCO 2020 crosswalk**: map `masco_code` (6-digit, 6,366 unit groups) to `onet_soc_code` and `esco_id`
- [ ] Validate role relevance with DOSM Job Market Insights (Malaysian labor market)
- [ ] Generate `role_dense_vector` and `role_sparse_vector` for each role via BGE-M3 RunPod endpoint

#### 3.2 - BGE-M3 Hybrid Search: Dense + Sparse + RRF (Primary Algorithm) [Person A - Backend Lead]

> 👤 **Assigned To:** Person A (Backend Lead)  
> ⏳ **Blocking Dependency:** Waits for **Person A (Substep 3.1)** [role vectors in DB] AND **Person B (Substep 1.4)** [user vector generated]  
> 🚀 **Unblocks:** Person A (Substep 3.3 - raw RRF candidate rankings)

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

#### 3.3 - Weighted Hybrid Scoring (Supporting Algorithm) [Person A - Backend Lead]

> 👤 **Assigned To:** Person A (Backend Lead)  
> ⏳ **Blocking Dependency:** Waits for **Person A (Substep 3.2)** [RRF rankings output]  
> 🚀 **Unblocks:** Person A (Substep 3.5 - final composite match scores)

- [ ] Compute final composite score:
  ```
  Final Score = (0.5 * RRF_Score) + (0.3 * Hard_Skill_Coverage) + (0.2 * Seniority_Match)
  ```
- [ ] `Hard_Skill_Coverage`: % of essential hard skills possessed by user (Set Intersection / ESCO essential flags)
- [ ] `Seniority_Match`: compare user `experience_years` with role seniority band
- [ ] Expose full score breakdown in UI (transparency for judges)

#### 3.4 - Skill Gap Analysis (Set Difference Algorithm) [Person A - Backend Lead]

> 👤 **Assigned To:** Person A (Backend Lead)  
> ⏳ **Blocking Dependency:** Waits for **Person A (Substep 3.1)** [`role_required_skills`] AND **Person B (Substep 1.3)** [`user.hard_skills`]  
> 🚀 **Unblocks:** **Person D (Substep 4.1 & 4.3)** [feeds `must_learn_skills[]` to Feature 4 Simulation], Person C (Substep F.4)

- [ ] Implement:
  ```
  Skill Gap = Role Required Skills — User Skills   [Set Difference: T \ U]
  ```
- [ ] Categorize:
  - **Core Gap:** missing ESCO essential skills → heavy penalty, labeled "Must Learn"
  - **Supporting Gap:** missing optional skills → minor penalty, labeled "Recommended"
- [ ] Output ordered `must_learn_skills[]` ranked by urgency

#### 3.5 - Output and Verification [Person A - Backend Lead]

> 👤 **Assigned To:** Person A (Backend Lead)  
> ⏳ **Blocking Dependency:** Waits for **Person A (Substeps 3.3 & 3.4)** [Scoring and gap analysis compiled into `/api/match`]  
> 🚀 **Unblocks:** Person C (Substep F.4 - results page data fetch), Person D (Phase 2 integration)

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
    "sdg_alignment": []
  }
  ```
- [ ] Display top 3-5 matched roles on UI
- [ ] Test with at least 3 distinct demo profiles

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

#### 5.1 - UN SDG API Setup and Reference Tables [Person A - Backend & Person C - Frontend]

> 👤 **Assigned To:** Person A (DB tables) & Person C (Frontend Lead — API fetch & seeding)  
> ⏳ **Blocking Dependency:** None (Starts Day 1-2)  
> 🚀 **Unblocks:** Person C (Substep 5.2 - curated mapping table)

- [ ] Access UN SDG API: https://unstats.un.org/sdgs/UNSDGAPIV5/swagger/index.html
- [ ] Fetch and store: `GET /v1/sdg/Goal/List` → `sdg_goals` table
- [ ] Fetch and store: `GET /v1/sdg/Goal/{goalCode}/Target/List` → `sdg_targets` table
- [ ] Fetch and store: `GET /v1/sdg/Indicator/List` → `sdg_indicators` table
- [ ] Create `role_sdg`: `role_id`, `sdg_goal`, `sdg_target`, `relationship_type`, `evidence`, `source`

#### 5.2 - Role → SDG Curated Mapping Table [Person C - Frontend Lead]

> 👤 **Assigned To:** Person C (Frontend Lead)  
> ⏳ **Blocking Dependency:** Waits for **Person A (Substep 1.1 / 3.1)** [ESCO `occupations` table populated]  
> 🚀 **Unblocks:** Person A (Substep 5.3 - static JOIN in `/api/match`)

- [ ] Build curated mapping: ESCO occupations → SDG targets (no unverified LLM generation)
- [ ] Per mapping, record:
  - `sdg_goal` (integer 1-17)
  - `sdg_target` (e.g., "8.2", "4.4")
  - `relationship_type` ("supports" / "enables" / "contributes")
  - `impact_reasoning`: 1 concise sentence
  - `source`: "UNSD SDG API"
- [ ] Priority SDGs: 4 (Quality Education), 8 (Decent Work), 9 (Industry & Innovation), 10 (Reduced Inequalities)
- [ ] At least 1 role must link to multiple SDGs (showcase multidimensional impact)

#### 5.3 - Integration into Feature 3 Output (Zero Extra Pipelines) [Person A - Backend Lead]

> 👤 **Assigned To:** Person A (Backend Lead)  
> ⏳ **Blocking Dependency:** Waits for **Person C (Substep 5.2)** [`role_sdg` table seeded] AND **Person A (Substep 3.5)** [`/api/match` endpoint live]  
> 🚀 **Unblocks:** Person C (Substep 5.4 - renders SDG badges on UI)

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

#### 5.4 - UI: SDG Badge Display [Person C - Frontend Lead]

> 👤 **Assigned To:** Person C (Frontend Lead)  
> ⏳ **Blocking Dependency:** Waits for **Person A (Substep 5.3)** [`sdg_alignment[]` returned in API response]  
> 🚀 **Unblocks:** Phase 1 visual demo complete

- [ ] Reusable `SdgBadge` component: `sdg_goal` prop → official UN color + number
- [ ] Hover/click → shadcn Dialog: `sdg_name`, `target`, `impact_reasoning`
- [ ] Use official UN SDG color palette and icons only
- [ ] Optional: "SDG Contribution View" aggregated across all recommended roles

#### 5.5 - Verification [Person C - Frontend & Person A - Backend]

> 👤 **Assigned To:** Person C (Frontend Lead) & Person A (Backend Lead)  
> ⏳ **Blocking Dependency:** Waits for **Person C (Substep 5.4)** & **Person A (Substep 5.3)**  
> 🚀 **Unblocks:** Phase 1 Sign-Off

- [ ] All mappings attribute `source: "UNSD SDG API"`
- [ ] Zero ungrounded SDG tags from free-form LLM
- [ ] Publish `role_sdg` curated table in GitHub repo with rationale
- [ ] Test: badges render, tooltips function

---

---

# PHASE 2 — Reskilling Enrichment (Day 3–4)

> **Feature:** 4 (Personalised Reskilling Pathway — Micro-Task Simulation)  
> **Team Member Assigned:** Person D (Phase 2 Owner), supported by Person B (vLLM container) & Person C (UI components)  
> **Dependency:** Requires Feature 3's `must_learn_skills[]` output to be wired. Starts immediately after Feature 3 skill gap endpoint is live (end of Day 3).  
> **Exit Criteria:** User can click a skill gap → see a simulation scenario → submit a response → receive JSON evaluator feedback.

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

#### 4.1 - Scenario Bank from O*NET Task Statements [Person D - Phase 2 Owner]

> 👤 **Assigned To:** Person D (Phase 2 Owner)  
> ⏳ **Blocking Dependency:** None for initial curation (Day 1-2 prep). Final mapping waits for **Person A (Substep 1.1)** [ESCO skill IDs] AND **Person A (Substep 3.4)** [target gap types]  
> 🚀 **Unblocks:** Person D (Substep 4.3 - DB scenario lookup)

- [ ] Pull O*NET task statements for each skill gap identified in Feature 3
- [ ] Curate 1-3 fictionalized scenario prompts per ESCO skill category
  - Example: *"Given this code snippet with a bias vulnerability, propose a 5-line governance policy"*
- [ ] Store in `simulation_tasks`: `skill_id`, `scenario_text`, `rubric_criteria[]`

#### 4.2 - Isolated LLM Evaluator (RunPod) [Person D - Phase 2 Owner & Person B - AI/ML Engineer]

> 👤 **Assigned To:** Person D (Prompts & Pydantic schema) & Person B (RunPod GPU deployment)  
> ⏳ **Blocking Dependency:** Waits for **Person B (Day 4 / Day 1)** [RunPod vLLM LLM server live with Instructor enforcement]  
> 🚀 **Unblocks:** Person D (Substep 4.3 - simulation grading engine)

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

#### 4.3 - Backend API (`POST /api/simulate`) [Person D - Phase 2 Owner & Person A - Backend Lead]

> 👤 **Assigned To:** Person D (Phase 2 Owner) with Person A (Backend schema/routing support)  
> ⏳ **Blocking Dependency:** Waits for **Person D (Substeps 4.1 & 4.2)** [scenarios seeded + evaluator online] AND **Person A (Substep 3.4)** [`must_learn_skills[]` schema]  
> 🚀 **Unblocks:** Person D (Substep 4.4 - interactive frontend pathway page)

- [ ] Implement `POST /api/simulate`: `{ skill_id, user_response }` → returns `SimulationResult`
- [ ] Fetch scenario from `simulation_tasks` by `skill_id`
- [ ] Call RunPod LLM evaluator with scenario rubric + user response
- [ ] Return structured JSON to frontend

#### 4.4 - Frontend: Micro-Task Simulation Page (`/pathway/[roleId]`) [Person D - Phase 2 Owner & Person C - Frontend]

> 👤 **Assigned To:** Person D (Phase 2 Owner) with Person C (Component scaffolding & theme support)  
> ⏳ **Blocking Dependency:** Waits for **Person C (Substep F.2/F.4)** [page routing & results UI] AND **Person D (Substep 4.3)** [`POST /api/simulate` API operational]  
> 🚀 **Unblocks:** Phase 2 End-to-End Test complete

- [ ] Display one simulation card per missing skill (from Feature 3 skill gap)
- [ ] Text input or code editor for user response
- [ ] On submit: POST `/api/simulate` with `{ skill_id, user_response }`
- [ ] Feedback card: `score_percent` bar + `improvement_reasoning` + `missing_concepts[]`
- [ ] Allow retry per simulation

---

---

# PHASE 3 — Analytical Overlay (Day 4–5)

> **Features:** 2 (AI-Trend Signal / CTCI) + 6 (Career Stress-Test Engine)  
> **Team Member Assigned:** Person E (Phase 3 Owner), supported by Person A (FastAPI parameters) & Person C (UI widgets)  
> **Dependency:** Both features share O*NET cognitive task data. Feature 2 CTCI scores feed into Feature 6 disruption penalty matrix. Build F2 first (Day 4 AM), then F6 (Day 4 PM – Day 5).  
> **Exit Criteria:** Each role card displays a CTCI indicator; the scenario slider on `/results` produces visibly different rankings between Moderate and Fast Disruption.

---

## FEATURE 2: AI-Trend Signal Layer (Cognitive Task Compression Index)

> **Goal:** Surface a nuanced AI disruption signal per occupation — distinguishing *Substitutive Compression* (repetitive cognitive tasks replaceable by AI) from *Complementary Compression* (high-reasoning tasks accelerated but not replaced by AI).

### Feature 2 Goals

- [ ] Every occupation has a **Cognitive Task Compression Index (CTCI)** score
- [ ] CTCI separates Substitutive Compression from Complementary Compression
- [ ] UI presents the signal as an informative indicator, not a scare metric
- [ ] Signal based on validated academic indices (Felten AIOE, Eloundou GPTs, Webb patent overlap)

---

### Feature 2 Sub-steps

#### 2.1 - Academic AI Exposure Metrics Integration [Person E - Phase 3 Owner]

> 👤 **Assigned To:** Person E (Phase 3 Owner)  
> ⏳ **Blocking Dependency:** None (Starts Day 1–3 prep: download AIOE/Webb/GPTs data)  
> 🚀 **Unblocks:** Person E (Substep 2.2 - feeds CTCI formula)

- [ ] Load O*NET `Abilities.txt` and `Work Activities.txt` for reasoning intensity computation
- [ ] Acquire AIOE scores (Felten, Raj & Seamans) — maps 10 AI capabilities against O*NET abilities
- [ ] Acquire GPTs-are-GPTs scores (Eloundou et al.) — fraction of tasks 50% faster by LLMs
- [ ] Acquire Webb patent-based AI exposure scores — lexical overlap, lowest human-judgment bias
- [ ] Store in `occupation_ai_exposure`: `onet_soc_code`, `aioe_score`, `gpts_score`, `webb_score`

#### 2.2 - CTCI Formulation [Person E - Phase 3 Owner]

> 👤 **Assigned To:** Person E (Phase 3 Owner)  
> ⏳ **Blocking Dependency:** Waits for **Person E (Substep 2.1)** [raw exposure indices loaded]  
> 🚀 **Unblocks:** Person E (Substep 2.3 & 2.4 - CTCI indicators), Person E (Substep 6.1 - penalty matrix)

> **Key insight (Rai 2026):** AIOE and GPTs scores correlate r=+0.85 with cognitive content intensity — NOT true AI replaceability (Human Judgment Halo Effect). Weight Webb score more heavily.

- [ ] Compute CTCI per occupation:
  ```
  CTCI = (0.5 * Webb_score) + (0.25 * AIOE_score) + (0.25 * GPTs_score)
  ```
- [ ] Classify:
  - **Substitutive Compression:** High CTCI + low O*NET reasoning → AI replaces repetitive execution
  - **Complementary Compression:** High CTCI + high O*NET reasoning → AI accelerates but cannot replace judgment

#### 2.3 - O*NET + OpenDOSM Signal Enrichment [Person E - Phase 3 Owner & Person A - Backend Lead]

> 👤 **Assigned To:** Person E (Phase 3 Owner) with Person A (Supabase schema alignment)  
> ⏳ **Blocking Dependency:** Waits for **Person A (Substep 3.1)** [MASCO crosswalk & occupations table in Supabase]  
> 🚀 **Unblocks:** Person E (Substep 2.4 - complete CTCI + Malaysian demand data payload)

- [ ] Join `occupation_ai_exposure` with O*NET task data for reasoning intensity
- [ ] Pull latest OpenDOSM Job Market Insights → `occupation_my_signal`: `masco_code`, `vacancy_count`, `period`, `state`

#### 2.4 - UI: CTCI Widget on Role Cards [Person E - Phase 3 Owner & Person C - Frontend Lead]

> 👤 **Assigned To:** Person E (Phase 3 Owner) with Person C (Role card UI integration)  
> ⏳ **Blocking Dependency:** Waits for **Person E (Substeps 2.2 & 2.3)** [CTCI computed] AND **Person C (Substep F.4)** [`/results` dashboard ready]  
> 🚀 **Unblocks:** Feature 2 UI complete

- [ ] Display CTCI score per role in `/results` role cards
- [ ] Compression type label: "Substitutive" (amber) / "Complementary" (green)
- [ ] Tooltip: brief `compression_reasoning` (non-alarmist framing)
- [ ] Malaysian vacancy trend as local demand context

---

## FEATURE 6: Handling Uncertainty (Career Stress-Test Engine)

> **Goal:** Parameterized Career Stress-Test — interactive slider shifts role rankings under Moderate vs Fast AI Disruption, using O*NET cognitive task matrices (built in Feature 2) as the penalty engine.

### Feature 6 Goals

- [ ] UI exposes interactive scenario toggle: "Moderate AI Adoption" vs "Fast AI Disruption"
- [ ] Changing scenario dynamically reweights role rankings
- [ ] Promotes Defensive Reskilling (soft skills, complex management) under fast disruption
- [ ] All disruption logic is fully deterministic — no LLM in scenario modeling

---

### Feature 6 Sub-steps

#### 6.1 - Disruption Penalty Matrix (Builds on Feature 2 CTCI data) [Person E - Phase 3 Owner]

> 👤 **Assigned To:** Person E (Phase 3 Owner)  
> ⏳ **Blocking Dependency:** Waits for **Person E (Substep 2.2)** [CTCI scores ready] AND **Person E (Substep 2.1)** [O*NET cognitive task data]  
> 🚀 **Unblocks:** Person E (Substep 6.2 - scenario reweighting engine)

- [ ] Use O*NET cognitive task data (already loaded for F2) to compute `routine_cognitive_ratio`
- [ ] Derive `disruption_penalty_fast` and `disruption_penalty_moderate` per occupation from AIOE/Webb/Eloundou
- [ ] Store in `occupation_disruption_matrix`: `onet_soc_code`, `routine_cognitive_ratio`, `disruption_penalty_fast`, `disruption_penalty_moderate`

#### 6.2 - Parameterized Scenario Engine [Person E - Phase 3 Owner & Person A - Backend Lead]

> 👤 **Assigned To:** Person E (Phase 3 Owner) with Person A (FastAPI router & score recalculation)  
> ⏳ **Blocking Dependency:** Waits for **Person A (Substep 3.5)** [`GET /api/match` live] AND **Person E (Substep 6.1)** [penalty matrix in DB]  
> 🚀 **Unblocks:** Person E (& C) (Substep 6.3 - shock slider UI)

- [ ] Scenario logic:
  ```
  Moderate:        Final Score = standard Feature 3 hybrid score (no penalty)
  Fast Disruption: Final Score = hybrid_score * (1 - disruption_penalty_fast)
                   + bonus_amplifier for soft_skill_intensity
  ```
- [ ] Under "Fast AI Disruption": high `routine_cognitive_ratio` roles drop; complex judgment / stakeholder management roles rise
- [ ] All score modifications exposed in `score_breakdown` payload
- [ ] Implement `GET /api/match?user_id=...&scenario=fast` parameter

#### 6.3 - UI: AI Shock Slider [Person E - Phase 3 Owner & Person C - Frontend Lead]

> 👤 **Assigned To:** Person E (Phase 3 Owner) with Person C (Slider component & Framer Motion reordering)  
> ⏳ **Blocking Dependency:** Waits for **Person E (Substep 6.2)** [`?scenario=fast` API live] AND **Person C (Substep F.4)** [`/results` page live]  
> 🚀 **Unblocks:** Feature 6 demo-ready

- [ ] Scenario toggle/slider on `/results` page
- [ ] On toggle: re-fetch with `?scenario=fast` or `?scenario=moderate`
- [ ] Animated role card reordering (framer-motion staggered transition)
- [ ] Delta indicators: roles that rose (↑) or fell (↓) between scenarios
- [ ] Callout: "Under Fast AI Disruption, roles requiring complex human judgment are prioritized"

---

---

# Overall Technical Architecture (Pipeline)

```text
[CV Upload / Input Form]                                           PHASE 1 (Person B & C)
        |
        v
(1. PDF Parser: pdfplumber) ──> Raw text extraction [Person B]
        |
        v
(2. Structured Output: Pydantic Schema) ──> JSON (hard, soft, years) [Person B]
        |  (Waits for Person A Substep 1.1 ESCO tables)
        v
(3. ESCO Normalization) ──> Map to esco_id [Person B]
        |
        v
(4. BGE-M3 via RunPod) ──> user_dense_vector + user_sparse_vector [Person B]
        |
        v
(5. Hybrid Search: Supabase pgvector RRF) ──> Ranked roles [Person A]
        |  (Waits for Person B Substep 1.4 User Vector)
        v
(6. Weighted Hybrid Scoring) ──> Final Score (%) + Ranking [Person A]
        |
        v
(7. Set Difference: Gap Analysis) ──> must_learn_skills[] [Person A]
        |
        v
(8. JOIN role_sdg) ──> sdg_alignment[] appended [Person A & C]     PHASE 1
        |  (Waits for Person C Substep 5.2 Curated SDG table)
        v
[Phase 1 Output: Ranked Roles + Match Score + Skill Gap + SDG Badges]
        |
        +---> Feature 4: Simulation task per skill gap             PHASE 2 (Person D)
        |          ──> LLM Evaluator JSON feedback
        |          (Waits for Person A Substep 3.4 must_learn_skills[])
        |
        +---> JOIN occupation_disruption_matrix                    PHASE 3 (Person E)
        |          ──> ctci + compression_type appended
        |          ──> Scenario reweighting (?scenario=fast)
        |          (Waits for Person A Substep 3.5 & Person E Substep 6.1)
        |
[Final Output: + CTCI Signal + Career Stress-Test Slider]
```

---

# Final Submission Checklist

- [ ] GitHub repository public / accessible to judges
- [ ] Live demo: Feature 3 working end-to-end (Phase 1 exit criteria)
- [ ] Every recommendation cites a credible source (no fabricated jobs, statistics)
- [ ] Solution framed as AI supporting human career decisions, not replacing judgment
- [ ] Exclusively uses public, open, or synthetic data — no real CVs or personal data
- [ ] All datasets: version, retrieval date, source URLs documented in repo
- [ ] **Phase 1:** SDG linkages meaningful and contextualized, never decorative
- [ ] **Phase 2:** Feature 4 simulation evaluator returns structured JSON (not free prose)
- [ ] **Phase 3:** CTCI signal clearly distinguishes Substitutive vs Complementary Compression
- [ ] **Phase 3:** Career Stress-Test slider produces visibly different rankings between scenarios
- [ ] BGE-M3 RunPod endpoint live, returning dense + sparse vectors
- [ ] Supabase RRF hybrid search function deployed and tested
- [ ] MASCO 2020 crosswalk loaded and mapped to ESCO/O*NET codes

---

> **References:**
> - [`TASKS.md`](./TASKS.md) — Team task division (5 people, 3 phases)
> - [`algorithm_consideration.md`](./algorithm_consideration.md) — Algorithm architecture
> - [`deep_research.md`](./deep_research.md) — Full architectural rationale and academic citations
> - [`deep_research_summary.md`](./deep_research_summary.md) — Concise method + dataset mapping per feature
> - [`Datasets.md`](./Datasets.md) — Recommended datasets per feature
> - [`src/Domain 1.md`](./src/Domain%201.md) — Problem statement and judging rubric

---

## FRONTEND: Next.js + Tailwind CSS + shadcn/ui

> **Goal:** Build a clean, responsive dashboard from CV upload to ranked future roles with match scores, skill gaps, SDG badges, CTCI signal, and Career Stress-Test slider.

### Full Tech Stack (Frontend)

| Layer | Library / Tool | Purpose | Assigned Lead |
|---|---|---|---|
| Framework | next.js (App Router) | Pages, routing, server-side API calls | **Person C** |
| Styling | tailwindcss | Utility-first CSS, responsive layout | **Person C** |
| UI Components | shadcn/ui | Card, Badge, Progress, Tabs, Dialog, Slider, Skeleton | **Person C** |
| Icons | lucide-react | Icon set (bundled with shadcn) | **Person C** |
| Data Visualization | recharts | Match score bar, skill gap radar, CTCI signal | **Person C** |
| File Upload | react-dropzone | Drag-and-drop CV/PDF upload | **Person C** |
| Data Fetching | @tanstack/react-query | Async fetching, caching, loading/error states | **Person C** |
| Animations | framer-motion | Card entrance, scenario re-rank transitions | **Person C** (& E) |
| HTTP Client | axios | Typed API calls to FastAPI backend | **Person C** |

### Missing Libraries (must install explicitly)

| Library | Phase needed | Reason |
|---|---|---|
| recharts | Phase 1 | Match score bars, skill gap radar chart |
| react-dropzone | Phase 1 | Drag-and-drop CV upload UX |
| @tanstack/react-query | Phase 1 | Async state management |
| framer-motion | Phase 1 / Phase 3 | Card animations + scenario slider transitions |
| axios | Phase 1 | HTTP calls to FastAPI backend |

---

### Frontend Sub-steps

#### F.1 - Project Initialization (Phase 1) [Person C - Frontend Lead]

> 👤 **Assigned To:** Person C (Frontend Lead)  
> ⏳ **Blocking Dependency:** None (Starts Day 1)  
> 🚀 **Unblocks:** Person C (Substep F.2)

- [ ] `npx create-next-app@latest frontend --typescript --tailwind --app --src-dir`
- [ ] `npx shadcn@latest init`
- [ ] `npm install recharts react-dropzone @tanstack/react-query framer-motion axios`
- [ ] `npx shadcn@latest add card badge progress tabs dialog button input skeleton slider`
- [ ] Configure `.env.local`: `NEXT_PUBLIC_API_URL=http://localhost:8000`

#### F.2 - Page Structure (App Router) [Person C - Frontend Lead]

> 👤 **Assigned To:** Person C (Frontend Lead)  
> ⏳ **Blocking Dependency:** Waits for **Person C (Substep F.1)**  
> 🚀 **Unblocks:** Person C (Substeps F.3, F.4), Person D (Substep F.7)

- [ ] `/` — Landing page: hero + "Get Started" CTA *(Phase 1)*
- [ ] `/profile` — CV upload form + manual skills form *(Phase 1)*
- [ ] `/results` — Ranked role cards + match scores + skill gaps + SDG badges *(Phase 1)*, + CTCI + scenario slider *(Phase 3)*
- [ ] `/pathway/[roleId]` — Micro-Task Simulation cards per skill gap *(Phase 2)*

#### F.3 - CV Upload Page `/profile` (Phase 1) [Person C - Frontend Lead]

> 👤 **Assigned To:** Person C (Frontend Lead)  
> ⏳ **Blocking Dependency:** Waits for **Person B (Substep 1.3 / Day 2)** [FastAPI `POST /api/profile` endpoint live]  
> 🚀 **Unblocks:** Complete user CV intake journey

- [ ] Drag-and-drop zone: react-dropzone (PDF only)
- [ ] Fallback manual form: skill tags, years of experience slider, interests select
- [ ] POST `/api/profile` with PDF or JSON payload
- [ ] Loading skeleton while backend processes (covers pdfplumber latency)

#### F.4 - Results Dashboard `/results` (Phase 1 → Phase 3) [Person C - Frontend Lead]

> 👤 **Assigned To:** Person C (Frontend Lead)  
> ⏳ **Blocking Dependency:** Waits for **Person A (Substep 3.5 / Day 3)** [FastAPI `GET /api/match` endpoint live]  
> 🚀 **Unblocks:** Phase 1 Core UI demo; Unblocks Person E (Substep 2.4 & 6.3)

- [ ] Fetch: `GET /api/match?user_id=...&scenario=moderate`
- [ ] Display top 3-5 role cards:
  - [ ] Role title + ESCO ID
  - [ ] Match score: shadcn Progress bar + percentage *(Phase 1)*
  - [ ] Score breakdown tooltip *(Phase 1)*
  - [ ] Skill gap Badges (red = core, yellow = supporting) *(Phase 1)*
  - [ ] SDG badges + Dialog popup *(Phase 1)*
  - [ ] CTCI indicator: Substitutive (amber) / Complementary (green) *(Phase 3)*
- [ ] recharts BarChart: match scores across roles *(Phase 1)*
- [ ] **Career Stress-Test Slider:** "Moderate" ↔ "Fast Disruption" *(Phase 3)*

#### F.5 - SDG Badge Component (Phase 1) [Person C - Frontend Lead]

> 👤 **Assigned To:** Person C (Frontend Lead)  
> ⏳ **Blocking Dependency:** Waits for **Person A (Substep 5.3)** [`sdg_alignment[]` returned in `/api/match`]  
> 🚀 **Unblocks:** Complete visual SDG presentation

- [ ] Reusable `SdgBadge`: official UN color circle + number
- [ ] Hover/click → shadcn Dialog: `sdg_name`, `target`, `impact_reasoning`

#### F.6 - Skill Gap Radar Chart (Optional — Phase 1) [Person C - Frontend Lead]

> 👤 **Assigned To:** Person C (Frontend Lead)  
> ⏳ **Blocking Dependency:** Waits for **Person C (Substep F.4)**  
> 🚀 **Unblocks:** Enhanced UI polish

- [ ] recharts RadarChart: user profile (blue) vs role requirements (red dashed)
- [ ] Axes: Technical, Domain, Soft Skills, Seniority

#### F.7 - Micro-Task Simulation Page `/pathway/[roleId]` (Phase 2) [Person D - Phase 2 Owner]

> 👤 **Assigned To:** Person D (Phase 2 Owner) with Person C  
> ⏳ **Blocking Dependency:** Waits for **Person C (Substep F.2/F.4)** [page routing & layout] AND **Person D (Substep 4.3)** [`POST /api/simulate` API operational]  
> 🚀 **Unblocks:** Phase 2 interactive simulation demonstration

- [ ] One simulation card per missing skill
- [ ] Text input or code editor for response
- [ ] POST `/api/simulate` → feedback card: score + improvement_reasoning + missing_concepts[]
- [ ] Allow retry

#### F.8 - API Integration Layer [Person C - Frontend Lead]

> 👤 **Assigned To:** Person C (Frontend Lead)  
> ⏳ **Blocking Dependency:** Waits for **Person A (Substep 3.5)**, **Person D (Substep 4.3)**, **Person E (Substep 6.2)** as respective APIs go live  
> 🚀 **Unblocks:** Continuous client-server sync

- [ ] `lib/api.ts` typed axios functions:
  - `uploadProfile(file)` → `UserProfile` *(Phase 1)*
  - `getMatchResults(userId, scenario)` → `RoleMatch[]` *(Phase 1, extended Phase 3)*
  - `getReskillPathway(roleId)` → `Pathway` *(Phase 1)*
  - `submitSimulation(skillId, response)` → `SimulationResult` *(Phase 2)*
- [ ] Wrap with `@tanstack/react-query` `useQuery` / `useMutation`

#### F.9 - Final UI Polish (Phase 3 / Day 5) [Person C - Frontend Lead]

> 👤 **Assigned To:** Person C (Frontend Lead)  
> ⏳ **Blocking Dependency:** Waits for all feature components to be merged  
> 🚀 **Unblocks:** Hackathon presentation and recording

- [ ] Mobile-responsive layout (Tailwind breakpoints: sm, md, lg)
- [ ] Dark mode via Tailwind `dark:` + next-themes
- [ ] Lighthouse target: Performance > 80, Accessibility > 90