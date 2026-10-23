# TASKS.md — Team Task Division (5 People, 3 Phases)

> **Project:** SDC XMUM Hackathon — Domain 1: Aiversecity Future-Ready Workforce  
> **Team:** "Bluffing" (5 members)  
> **Strategy:** Assign Phase 1 (MVP Core) to **3 people minimum**, freeing **2 people** to begin Phase 2 and Phase 3 work in parallel starting Day 3.  
> **Detailed Substeps & Technical Roadmap:** Refer to [`WORKSTEPS.md`](./WORKSTEPS.md).

---

## Phase Summary

| Phase | Features | Assigned To | Starts | Priority |
|---|---|---|---|---|
| **Phase 1 — MVP Core** | F1 (Skills Intake) + F3 (Role Matching) + F5 (SDG Mapping) | Person A, Person B, Person C | Day 1 | 🔴 Critical Path |
| **Phase 2 — Reskilling Enrichment** | F4 (Micro-Task Simulation) | Person D | Day 1 (prep) → Day 3 (build) | 🟡 High |
| **Phase 3 — Analytical Overlay** | F2 (CTCI Signal) + F6 (Career Stress-Test) | Person E | Day 1 (prep) → Day 4 (build) | 🟢 Analytical Add-on |

> **Phase 2 & 3 members are NOT idle during Day 1–2.** They use that time for dataset prep, O*NET loading, and scenario curation — all of which are blocking prerequisites that cannot happen later.

---

## Master Blocking Dependency Matrix (Who Waits for Whom)

Use this table whenever you plan your day. If your task is listed under **Waiting Task**, you MUST confirm that the **Blocking Task** is delivered before finalizing your step.

| Blocked Person | Blocked Task / Substep | ⏳ Waits For (Person X, Step Y) | Why / Handoff Artifact | Target Delivery |
|---|---|---|---|---|
| **Person B** | Substep 1.3: Pydantic Structured Output | **Person A (Substep 1.1)** & **Person B (Substep 1.2)** | Needs ESCO `skills` table to resolve `esco_id` + raw CV text from `pdfplumber` | End of Day 2 |
| **Person B** | Substep 1.4: User Embeddings | **Person B (Day 1)** & **Person A (Substep 1.1)** & **Person B (Substep 1.3)** | Needs RunPod BGE-M3 `/embed` live + Supabase `role_vectors` table + structured user profile | Day 2 PM / Day 3 AM |
| **Person A** | Substep 3.1: Role Required Skills Vectors | **Person B (Substep 1.4 / Day 1)** | Needs RunPod BGE-M3 `/embed` endpoint active to generate dense & sparse role vectors | Day 2 PM |
| **Person A** | Substep 3.2: PL/pgSQL RRF Hybrid Search | **Person A (Substep 3.1)** & **Person B (Substep 1.4)** | Needs both role vectors in DB and user profile vector query | Day 3 AM |
| **Person A** | Substep 3.4: Set Difference Skill Gap | **Person A (Substep 3.1)** & **Person B (Substep 1.3)** | Needs `role_required_skills` in DB and user's extracted `hard_skills[]` | Day 3 AM |
| **Person A** | Substep 5.3: Integrate SDG into `/api/match` | **Person C (Substep 5.2)** & **Person A (Substep 3.5)** | Needs curated `role_sdg` table seeded in Supabase to perform static JOIN | Day 4 AM |
| **Person C** | Substep 5.2: Role → SDG Curated Mapping | **Person A (Substep 1.1 / 3.1)** | Needs final list of ESCO occupations from DB to curate SDG linkages | Day 2 PM |
| **Person C** | Substep F.3: `/profile` Page Integration | **Person B (Substep 1.3 / Day 2)** | Needs FastAPI `POST /api/profile` endpoint live to accept uploads | End of Day 2 |
| **Person C** | Substep F.4: `/results` Dashboard Integration | **Person A (Substep 3.5 / Day 3)** | Needs FastAPI `GET /api/match` endpoint live with JSON response | End of Day 3 |
| **Person C** | Substep F.5: `SdgBadge` Live Data | **Person A (Substep 5.3)** | Needs `sdg_alignment[]` array present in `/api/match` JSON payload | Day 4 AM |
| **Person D** | Substep 4.1: Scenario Bank Finalization | **Person A (Substep 1.1 & 3.4)** | Needs ESCO skill IDs & Feature 3 `must_learn_skills[]` category schema | Day 2 / Day 3 AM |
| **Person D** | Substep 4.2: Isolated Evaluator Server | **Person B (Day 4 / Day 1)** | Needs RunPod vLLM LLM container running with Instructor enforcement | Day 3 PM |
| **Person D** | Substep 4.3: Backend `POST /api/simulate` | **Person D (Substeps 4.1 & 4.2)** & **Person A (Substep 3.4)** | Needs scenarios seeded in Supabase + evaluator server live + skill gap format | End of Day 3 |
| **Person D** | Substep 4.4 / F.7: `/pathway/[roleId]` UI | **Person C (Substeps F.2 & F.4)** & **Person D (Substep 4.3)** | Needs frontend routing & layout shell + `POST /api/simulate` API operational | Day 4 PM |
| **Person E** | Substep 2.2: CTCI Formulation | **Person E (Substep 2.1)** | Needs AIOE, GPTs, and Webb raw exposure scores downloaded | Day 3 PM |
| **Person E** | Substep 2.3: O*NET + OpenDOSM DB Merge | **Person A (Substep 3.1)** | Needs MASCO 2020 crosswalk & occupations table seeded in Supabase | Day 3 PM |
| **Person E** | Substep 2.4: CTCI Widget on UI | **Person E (Substep 2.2)** & **Person C (Substep F.4)** | Needs computed CTCI scores + `/results` role card component | Day 4 AM |
| **Person E** | Substep 6.1: Disruption Penalty Matrix | **Person E (Substep 2.2 & 2.1)** | Needs CTCI scores + O*NET cognitive routine ratios | Day 4 AM |
| **Person E** | Substep 6.2: Scenario Reweighting API | **Person A (Substep 3.5)** & **Person E (Substep 6.1)** | Needs base `/api/match` endpoint live + `occupation_disruption_matrix` seeded | Day 4 PM |
| **Person E** | Substep 6.3: AI Shock Slider on UI | **Person E (Substep 6.2)** & **Person C (Substep F.4)** | Needs `/api/match?scenario=fast` working + `/results` dashboard page | Day 5 AM |

---

## Person A — Backend Lead (Phase 1)

**Scope:** Infrastructure setup + Feature 3 core algorithm + Supabase vector functions + API routing

### Day 1
- [x] Initialize Supabase project, enable `pgvector` extension (v0.7.0+)
- [x] Create all database tables (Substep 1.1):
  - `skills`, `occupations`, `role_required_skills`
  - `role_vectors` (with `vector` and `sparsevec` columns)
  - `sdg_goals`, `sdg_targets`, `sdg_indicators`, `role_sdg`
  - `occupation_ai_exposure`, `occupation_my_signal`, `occupation_disruption_matrix` *(stub for Phase 3)*
  - `simulation_tasks` *(stub for Phase 2)*
- [x] Seed ESCO skills + occupations CSV into Supabase *(🚀 Unblocks: Person B Substep 1.3, Person C Substep 5.2, Person D Substep 4.1)*
- [x] Seed MASCO 2020 crosswalk: `masco_code` → `onet_soc_code` → `esco_id`

### Day 2
- [x] Implement O*NET enrichment: load `Tasks.txt` + `Work Activities.txt` + `Abilities.txt` (via fuzzy title crosswalk `enrich_onet.py`)
- [x] Build `role_required_skills` relation: ESCO occupation → essential/optional skills + weight (Substep 3.1)
- [x] Generate 20-50 synthetic user profiles (JSON with ESCO IDs)
- [x] Compute & store `role_vectors` in Supabase *(Completed: 1,000 ESCO role vectors embedded via RunPod BGE-M3)*

### Day 3
- [x] Implement PL/pgSQL **RRF hybrid search function** in Supabase (Substep 3.2)
- [x] Implement weighted scoring logic: `Final Score = (0.5 * RRF) + (0.3 * HardSkillCoverage) + (0.2 * SeniorityMatch)` (Substep 3.3)
- [x] Implement Set Difference Skill Gap: `T \ U` → `must_learn_skills[]` with `core` / `supporting` categories (Substep 3.4) *(🚀 Unblocks: Person D Substeps 4.1 & 4.3)*
- [x] Build FastAPI endpoint `GET /api/match?user_id=...&scenario=moderate` (Substep 3.5) *(🚀 Unblocks: Person C Substep F.4)*
- [x] Validate Feature 3 end-to-end with 3 synthetic profiles (verified via `test_match_api.py`)

### Day 4
- [x] Integrate `sdg_alignment[]` static JOIN into `/api/match` response (Substep 5.3) *(Completed ahead of schedule with 2,054 SDG mappings + official hex colors)*
- [x] Add `?scenario=` query parameter support in `/api/match` (Substep 6.2 stub, ready for Person E)
- [x] Support Person D (Phase 2): wire `POST /api/simulate` backend scaffold in FastAPI *(scaffolded in simulate.py + seeded task)*

### Day 5
- [ ] Code review + API query latency tuning (pgvector index optimization)
- [ ] GitHub repo cleanup + README technical documentation
- [ ] Joint demo script preparation with all members

---

## Person B — AI/ML Engineer (Phase 1)

**Scope:** RunPod BGE-M3 deployment + Feature 1 CV extraction pipeline + vLLM LLM evaluator

### Day 1
- [x] Provision RunPod GPU instance ($25 credit)
- [x] Deploy **BGE-M3** via infinity-embedding container on RunPod (Substep 1.4)
- [x] Expose `/embed` endpoint: input text → `{ dense_vector, ... }` *(🚀 Unblocks: Person A Substeps 3.1 & 3.2)*
- [x] Test endpoint with sample skill strings ("Data Analysis", "Python", "Stakeholder Management")
- [x] Verify synonym clustering: "Data Analysis" ≈ "Data Processing" ≈ "Data Analytics" (dense vectors)

### Day 2
- [x] Implement `pdfplumber` CV parser (Python, MIT license) (Substep 1.2)
  - Handle multi-column resume layout
  - Coordinate with Person C for fallback manual entry form
- [x] Implement Pydantic schema for structured output (Substep 1.3):
  - Fields: `hard_skills[]`, `soft_skills[]`, `experience_years`
  - NER extraction + deterministic ESCO taxonomy matching
  - *(Completed: verified via `test_profile_api.py`)*
- [x] Wire extraction → Pydantic validation → ESCO ID resolution per skill
- [x] Store `confidence_score` per skill mapping (leave None if low confidence)
- [x] Build FastAPI endpoint `POST /api/profile` (accepts PDF or JSON) *(🚀 Unblocks: Person C Substep F.3)*

### Day 3
- [x] Generate `user_dense_vector` via RunPod BGE-M3 for synthetic user profiles (Substep 1.4)
- [x] Store all vectors in Supabase `role_vectors` and `user_profiles` table
- [x] Full Feature 1 → Feature 3 pipeline integration test with Person A (verified via `test_match_api.py`)

### Day 4
- [ ] Deploy Llama-3-8B or Qwen on RunPod (same GPU instance, separate vLLM process) (Substep 4.2)
  - Scaffold LLM evaluator with Pydantic/Instructor enforcement *(🚀 Unblocks: Person D Substeps 4.2 & 4.3)*
- [ ] Optimize BGE-M3 batching for multiple role vectors

### Day 5
- [ ] Performance testing: vector generation latency acceptable for live demo (< 500ms)
- [ ] RunPod endpoint health check + automatic fallback handling

---

## Person C — Frontend Lead (Phase 1)

**Scope:** Next.js project + UI dashboard + Feature 5 SDG mapping + SDG badge component

### Day 1
- [ ] Scaffold Next.js project: `npx create-next-app@latest frontend --typescript --tailwind --app --src-dir` (Substep F.1)
- [ ] `npx shadcn@latest init`
- [ ] Install: `npm install recharts react-dropzone @tanstack/react-query framer-motion axios`
- [ ] `npx shadcn@latest add card badge progress tabs dialog button input skeleton slider`
- [ ] Configure `.env.local`: `NEXT_PUBLIC_API_URL=http://localhost:8000`
- [ ] Create `lib/api.ts` with typed axios stubs: `uploadProfile`, `getMatchResults`, `getReskillPathway`
- [ ] Set up page structure (Substep F.2): `/`, `/profile`, `/results`, `/pathway/[roleId]`

### Day 2
- [ ] Build `/profile` page (Substep F.3):
  - Drag-and-drop zone (react-dropzone, PDF only)
  - Fallback manual skills form
  - Loading skeleton while backend processes
  - *(⏳ Waits for: Person B Substep 1.3 / Day 2 — `POST /api/profile` live)*
- [ ] Build landing `/` page: hero section + "Get Started" CTA
- [ ] Seed UN SDG API → `sdg_goals`, `sdg_targets`, `sdg_indicators` tables in Supabase (Substep 5.1)
- [ ] Build curated `role_sdg` mapping table (Substep 5.2, min. 5 ESCO occupations, priority SDGs 4/8/9/10) *(⏳ Waits for: Person A Substep 1.1/3.1 — occupations table; 🚀 Unblocks: Person A Substep 5.3)*

### Day 3
- [ ] Build `/results` page (Phase 1 version, Substep F.4):
  - Role cards (shadcn Card): title + ESCO ID + match score bar + skill gap badges
  - Score breakdown tooltip (RRF / Hard Skill / Seniority weights)
  - SDG badges with Dialog popup (`impact_reasoning`)
  - recharts BarChart: match score comparison
  - framer-motion staggered card entrance animation
  - *(⏳ Waits for: Person A Substep 3.5 — `GET /api/match` live)*
- [ ] Build reusable `SdgBadge` component (official UN colors + Dialog popup) (Substep 5.4 / F.5)

### Day 4
- [ ] Integrate `GET /api/match` with `@tanstack/react-query`
- [ ] Handle loading, error, and empty states on `/results`
- [ ] Wire `/profile` form → `POST /api/profile` → redirect to `/results`
- [ ] Add `/pathway/[roleId]` page scaffold (stub, ready for Person D)
- [ ] Integrate SDG badges with live `sdg_alignment[]` data *(⏳ Waits for: Person A Substep 5.3)*

### Day 5
- [ ] Mobile-responsive layout (Tailwind breakpoints: sm, md, lg)
- [ ] Dark mode via `next-themes`
- [ ] Support Person E with AI Shock Slider integration on `/results` (Substep 6.3)
- [ ] Lighthouse audit: target Performance > 80, Accessibility > 90
- [ ] Final UI polish + demo run-through

---

## Person D — Phase 2 Owner: Feature 4 (Micro-Task Simulation)

**Scope:** Feature 4 — Personalised Reskilling Pathway. Prep during Day 1–2, build Day 3–4.

### Day 1 (Prep — while Phase 1 sets up infra)
- [x] Read O*NET Task Statements documentation and download `Tasks.txt`
- [x] Map O*NET task statements to ESCO skill categories (manual curation, ~20 skills) *(⏳ Waits for: Person A Substep 1.1 — ESCO taxonomy)*
- [x] Draft 1-3 fictionalized scenario prompts per ESCO skill category (Substep 4.1)
  - Example: *"Given this AI audit report excerpt, write a 3-bullet remediation plan"*
- [x] Define `rubric_criteria[]` per scenario (2-4 evaluation dimensions)

### Day 2 (Prep — finalize scenario bank)
- [x] Finalize curated `simulation_tasks` entries (min. 10 scenarios across 5+ skill categories)
- [x] Prepare Pydantic schema for evaluator output: `{ score_percent, improvement_reasoning, missing_concepts[] }`
- [x] Coordinate with Person B on RunPod LLM evaluator scaffold (prompt format & JSON enforcement)

### Day 3 (Build starts — Feature 3 skill gap output now available)
- [x] Load `simulation_tasks` into Supabase (coordinate schema with Person A)
- [x] Implement evaluator prompt template (closed, rubric-anchored, no open generation)
- [x] Implement `POST /api/simulate`: `{ skill_id, user_response }` → `SimulationResult` (Substep 4.3)
  - *(⏳ Waits for: Person B Day 4 / Day 1 — RunPod LLM server live)*
  - *(⏳ Waits for: Person A Substep 3.4 — Feature 3 `must_learn_skills[]` schema)*
- [x] Test evaluator: submit 3 dummy responses, verify rigid JSON output structure

### Day 4 (Frontend Integration)
- [ ] Build `/pathway/[roleId]` frontend page (Substep 4.4 / F.7):
  - Fetch skill gaps from Feature 3 output
  - Display one simulation card per `must_learn_skills[]` item
  - Text input / code editor for user response
  - On submit: POST `/api/simulate` → render feedback card
  - Allow retry
  - *(⏳ Waits for: Person C Substeps F.2 & F.4 — page layout and routing)*
- [ ] Wire `submitSimulation(skillId, response)` in `lib/api.ts`
- [ ] Wrap with `@tanstack/react-query` `useMutation`

### Day 5
- [ ] End-to-end test: full user flow from `/results` skill gap → `/pathway/[roleId]` → simulation → feedback
- [ ] Handle edge cases: evaluator timeout, no scenario available for a skill
- [ ] Document Feature 4 in GitHub README

---

## Person E — Phase 3 Owner: Feature 2 + Feature 6 (CTCI + Stress-Test)

**Scope:** Feature 2 (Cognitive Task Compression Index) + Feature 6 (Career Stress-Test Engine). Prep Day 1–3, build Day 4–5.

### Day 1 (Prep)
- [ ] Download O*NET database: `Abilities.txt`, `Work Activities.txt`, `Tasks.txt` (Substep 2.1)
- [ ] Acquire AIOE, GPTs-are-GPTs, and Webb AI exposure datasets:
  - AIOE: Felten, Raj & Seamans (10 AI capabilities vs abilities)
  - GPTs-are-GPTs: Eloundou et al. (fraction of tasks accelerated)
  - Webb: Patent-based exposure (lexical overlap, minimal human bias)
- [ ] Extract scores per O*NET-SOC occupation code

### Day 2 (Prep)
- [ ] Load O*NET `Abilities.txt` + `Work Activities.txt` into Supabase (Substep 2.3)
- [ ] Compute preliminary `reasoning_intensity` per O*NET-SOC code
- [ ] Pull OpenDOSM Job Market Insights quarterly data → `occupation_my_signal` table

### Day 3 (Prep — finalize data & MASCO crosswalk)
- [ ] Merge AIOE / GPTs / Webb scores into `occupation_ai_exposure` table (Substep 2.1)
- [ ] Apply MASCO 2020 crosswalk to map `masco_code` → `onet_soc_code` for all occupations *(⏳ Waits for: Person A Substep 3.1)*
- [ ] Validate: every ESCO occupation in `role_vectors` has a corresponding `onet_soc_code` + CTCI score

### Day 4 AM — Feature 2 Build
- [ ] Compute CTCI per occupation (Substep 2.2):
  ```
  CTCI = (0.5 * Webb_score) + (0.25 * AIOE_score) + (0.25 * GPTs_score)
  ```
- [ ] Classify: Substitutive vs Complementary Compression (threshold: O*NET reasoning intensity median)
- [ ] Store `ctci_score` + `compression_type` + `compression_reasoning` in `occupation_ai_exposure`
- [ ] Add CTCI JOIN to `GET /api/match` response payload with Person A
- [ ] Coordinate with Person C: add CTCI widget to role cards on `/results` (Substep 2.4) *(⏳ Waits for: Person C Substep F.4)*

### Day 4 PM — Feature 6 Build
- [ ] Compute disruption penalty matrix from CTCI data (Substep 6.1):
  - `disruption_penalty_fast` = `routine_cognitive_ratio * CTCI` (normalized 0–1)
  - `disruption_penalty_moderate` = `disruption_penalty_fast * 0.4` (softened)
- [ ] Store in `occupation_disruption_matrix`
- [ ] Implement scenario reweighting in `/api/match?scenario=fast` (Substep 6.2):
  ```
  Fast Disruption: Final Score = hybrid_score * (1 - disruption_penalty_fast)
                                + bonus_amplifier for soft_skill_intensity
  ```
  *(⏳ Waits for: Person A Substep 3.5 — base `/api/match` live)*
- [ ] Test: same profile, Moderate vs Fast — role rankings should visibly differ

### Day 5
- [ ] Coordinate with Person C: add AI Shock Slider to `/results` page (framer-motion reorder animation) (Substep 6.3)
- [ ] Validate: delta indicators (↑ / ↓) display correctly between scenarios
- [ ] Document CTCI formula + bias caveat (Rai 2026) in GitHub README
- [ ] Final end-to-end test: slider produces different role ranking

---

## Cross-Team Coordination Points & Handoff Milestones

| Milestone | Producer | Consumers | ⏳ Blocking Condition | Target Deadline |
|---|---|---|---|---|
| **BGE-M3 `/embed` endpoint live** | Person B | Person A | Person A cannot embed role vectors or test search without this | End of Day 1 |
| **Supabase schema + ESCO seeded** | Person A | All | Blocks Person B (1.3), Person C (5.2), Person D (4.1) | End of Day 1 |
| **Feature 1 `POST /api/profile` live** | Person B | Person C | Person C cannot test `/profile` upload without this | End of Day 2 |
| **Feature 3 `GET /api/match` live** | Person A | Person C, D, E | Person C `/results`, Person D skill gaps, Person E scenario slider all wait on this | End of Day 3 |
| **`simulation_tasks` schema agreed** | Person A & D | Person D | Person D cannot seed scenarios into DB | Start of Day 3 |
| **RunPod LLM evaluator wired** | Person B & D | Person D | Person D cannot test simulation feedback | Day 3 PM |
| **O*NET data in Supabase** | Person E | Person A | Person A aligns schema for CTCI & disruption tables | End of Day 3 |
| **CTCI JOIN in `/api/match`** | Person E & A | Person C | Person C displays CTCI indicators on role cards | Day 4 AM |
| **`/pathway/[roleId]` page live** | Person D & C | Demo Lead | Completes Phase 2 end-to-end flow | Day 4 PM |
| **Feature 6 slider UI** | Person E & C | Demo Lead | Completes Phase 3 dynamic stress-testing | Day 5 AM |

---

## Risk Register

| Risk | Owner | Mitigation |
|---|---|---|
| RunPod GPU credit exhausted early | Person B | Batch all BGE-M3 role vector generation in a single session; cache vectors — never re-embed same text twice |
| AIOE/Webb scores not available in downloadable form | Person E | Use GPTs-are-GPTs O*NET mapping (OpenAI published) as primary; derive simplified Webb proxy from patent keyword overlap |
| pdfplumber slow on large PDFs | Person B | Async processing + loading skeleton; cap accepted PDF size at 5MB in UI |
| MASCO crosswalk incomplete | Person A + Person E | Manual mapping for top 50 occupations only; flag unmapped roles as "Internationally Classified" |
| Phase 2 / Phase 3 not finished by Day 5 | Person D, Person E | Phase 1 demo is self-sufficient; Phase 2 and 3 are additive enrichment, not blockers |
| LLM evaluator hallucinations in Feature 4 | Person D | Strict Pydantic/Instructor enforcement; rubric_criteria is always pre-provided, never LLM-generated |
