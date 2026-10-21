# TASKS.md — Team Task Division (5 People, 3 Phases)

> **Project:** SDC XMUM Hackathon — Domain 1: Aiversecity Future-Ready Workforce
> **Team:** "Bluffing" (5 members)
> **Strategy:** Assign Phase 1 (MVP Core) to **3 people minimum**, freeing **2 people** to begin Phase 2 and Phase 3 work in parallel starting Day 3.

---

## Phase Summary

| Phase | Features | Assigned To | Starts |
|---|---|---|---|
| **Phase 1 — MVP Core** | F1 (Skills Intake) + F3 (Role Matching) + F5 (SDG Mapping) | Person A, Person B, Person C | Day 1 |
| **Phase 2 — Reskilling Enrichment** | F4 (Micro-Task Simulation) | Person D | Day 1 (prep) → Day 3 (build) |
| **Phase 3 — Analytical Overlay** | F2 (CTCI Signal) + F6 (Career Stress-Test) | Person E | Day 1 (prep) → Day 4 (build) |

> **Phase 2 & 3 people are NOT idle during Day 1–2.** They use that time for dataset prep, O*NET loading, and scenario curation — all of which are blocking prerequisites that cannot happen later.

---

## Person A — Backend Lead (Phase 1)

**Scope:** Infrastructure setup + Feature 3 core algorithm + Supabase vector functions

### Day 1
- [ ] Initialize Supabase project, enable `pgvector` extension (v0.7.0+)
- [ ] Create all database tables:
  - `skills`, `occupations`, `role_required_skills`
  - `role_vectors` (with `vector` and `sparsevec` columns)
  - `sdg_goals`, `sdg_targets`, `sdg_indicators`, `role_sdg`
  - `occupation_ai_exposure`, `occupation_my_signal`, `occupation_disruption_matrix` *(stub for Phase 3)*
  - `simulation_tasks` *(stub for Phase 2)*
- [ ] Seed ESCO skills + occupations CSV into Supabase
- [ ] Seed MASCO 2020 crosswalk: `masco_code` → `onet_soc_code` → `esco_id`

### Day 2
- [ ] Implement O*NET enrichment: load `Tasks.txt` + `Work Activities.txt` + `Abilities.txt`
- [ ] Build `role_required_skills` relation: ESCO occupation → essential/optional skills + weight
- [ ] Generate 20-50 synthetic user profiles (JSON with ESCO IDs)

### Day 3
- [ ] Implement PL/pgSQL **RRF hybrid search function** in Supabase
- [ ] Implement weighted scoring logic: `Final Score = (0.5 * RRF) + (0.3 * HardSkillCoverage) + (0.2 * SeniorityMatch)`
- [ ] Implement Set Difference Skill Gap: `T \ U` → `must_learn_skills[]` with `core` / `supporting` categories
- [ ] Build FastAPI endpoint `GET /api/match?user_id=...&scenario=moderate`
- [ ] Validate Feature 3 end-to-end with 3 synthetic profiles

### Day 4
- [ ] Integrate `sdg_alignment[]` JOIN into `/api/match` response
- [ ] Add `?scenario=` parameter support in `/api/match` for Phase 3 (stub, returns unmodified score for now)
- [ ] Support Person D (Phase 2): wire `POST /api/simulate` backend scaffold

### Day 5
- [ ] Code review + bug fixes
- [ ] GitHub repo cleanup + README documentation
- [ ] Demo script preparation

---

## Person B — AI/ML Engineer (Phase 1)

**Scope:** RunPod BGE-M3 deployment + Feature 1 CV extraction pipeline

### Day 1
- [ ] Provision RunPod GPU instance ($25 credit)
- [ ] Deploy **BGE-M3** via vLLM container on RunPod
- [ ] Expose `/embed` endpoint: input text → `{ dense_vector, sparse_vector, colbert_vecs }`
- [ ] Test endpoint with sample skill strings ("Data Analysis", "Python", "Stakeholder Management")
- [ ] Verify synonym clustering: "Data Analysis" ≈ "Data Processing" ≈ "Data Analytics" (dense vectors)

### Day 2
- [ ] Implement `pdfplumber` CV parser (Python, MIT license)
  - Handle multi-column resume layout
  - Build fallback manual entry form (skills, years of experience, interests)
- [ ] Implement Pydantic schema for structured output:
  - Fields: `hard_skills[]`, `soft_skills[]`, `experience_years`
  - LLM acts as NER agent only — no free-form narration
- [ ] Wire LLM call → Pydantic validation → ESCO ID resolution per skill
- [ ] Store `confidence_score` per skill mapping
- [ ] Build FastAPI endpoint `POST /api/profile` (accepts PDF or JSON)

### Day 3
- [ ] Generate `user_dense_vector` + `user_sparse_vector` via RunPod BGE-M3 for each profile
- [ ] Generate `role_dense_vector` + `role_sparse_vector` for all ESCO occupations
- [ ] Store all vectors in Supabase `role_vectors` table
- [ ] Full Feature 1 → Feature 3 pipeline integration test

### Day 4
- [ ] Deploy Llama-3-8B or Qwen on RunPod (same GPU instance, separate vLLM process)
  - Scaffold LLM evaluator with Pydantic/Instructor enforcement *(for Person D / Phase 2)*
- [ ] Optimize BGE-M3 batching for multiple role vectors

### Day 5
- [ ] Performance testing: vector generation latency acceptable for demo
- [ ] RunPod endpoint health check + fallback handling

---

## Person C — Frontend Lead (Phase 1)

**Scope:** Next.js project + UI dashboard + Feature 5 SDG mapping + SDG badge component

### Day 1
- [ ] Scaffold Next.js project: `npx create-next-app@latest frontend --typescript --tailwind --app --src-dir`
- [ ] `npx shadcn@latest init`
- [ ] Install: `npm install recharts react-dropzone @tanstack/react-query framer-motion axios`
- [ ] `npx shadcn@latest add card badge progress tabs dialog button input skeleton slider`
- [ ] Configure `.env.local`: `NEXT_PUBLIC_API_URL=http://localhost:8000`
- [ ] Create `lib/api.ts` with typed axios stubs: `uploadProfile`, `getMatchResults`, `getReskillPathway`
- [ ] Set up page structure: `/`, `/profile`, `/results`, `/pathway/[roleId]`

### Day 2
- [ ] Build `/profile` page:
  - Drag-and-drop zone (react-dropzone, PDF only)
  - Fallback manual skills form
  - Loading skeleton while backend processes
- [ ] Build landing `/` page: hero section + "Get Started" CTA
- [ ] Seed UN SDG API → `sdg_goals`, `sdg_targets`, `sdg_indicators` tables in Supabase
- [ ] Build curated `role_sdg` mapping table (min. 5 ESCO occupations, priority SDGs 4/8/9/10)

### Day 3
- [ ] Build `/results` page (Phase 1 version):
  - Role cards (shadcn Card): title + ESCO ID + match score bar + skill gap badges
  - Score breakdown tooltip (RRF / Hard Skill / Seniority weights)
  - SDG badges with Dialog popup (`impact_reasoning`)
  - recharts BarChart: match score comparison
  - framer-motion staggered card entrance animation
- [ ] Build reusable `SdgBadge` component (official UN colors + Dialog)

### Day 4
- [ ] Integrate `GET /api/match` with `@tanstack/react-query`
- [ ] Handle loading, error, and empty states on `/results`
- [ ] Wire `/profile` form → `POST /api/profile` → redirect to `/results`
- [ ] Add `/pathway/[roleId]` page scaffold (stub, ready for Person D)

### Day 5
- [ ] Mobile-responsive layout (Tailwind breakpoints)
- [ ] Dark mode via `next-themes`
- [ ] Lighthouse audit: target Performance > 80, Accessibility > 90
- [ ] Final UI polish + demo run-through

---

## Person D — Phase 2 Owner: Feature 4 (Micro-Task Simulation)

**Scope:** Feature 4 — Personalised Reskilling Pathway. Prep during Day 1–2, build Day 3–4.

### Day 1 (Prep — while Phase 1 sets up infra)
- [ ] Read O*NET Task Statements documentation and download `Tasks.txt`
- [ ] Map O*NET task statements to ESCO skill categories (manual curation, ~20 skills)
- [ ] Draft 1-3 fictionalized scenario prompts per ESCO skill category
  - Example: *"Given this AI audit report excerpt, write a 3-bullet remediation plan"*
- [ ] Define `rubric_criteria[]` per scenario (2-4 evaluation dimensions)

### Day 2 (Prep — finalize scenario bank)
- [ ] Finalize curated `simulation_tasks` entries (min. 10 scenarios across 5+ skill categories)
- [ ] Prepare Pydantic schema for evaluator output: `{ score_percent, improvement_reasoning, missing_concepts[] }`
- [ ] Review Person B's RunPod LLM evaluator scaffold (coordinate prompt format)

### Day 3 (Build starts — Feature 3 skill gap output now available)
- [ ] Load `simulation_tasks` into Supabase (coordinate schema with Person A)
- [ ] Implement evaluator prompt template (closed, rubric-anchored, no open generation)
- [ ] Implement `POST /api/simulate`: `{ skill_id, user_response }` → `SimulationResult`
- [ ] Test evaluator: submit 3 dummy responses, verify JSON output structure

### Day 4
- [ ] Build `/pathway/[roleId]` frontend page:
  - Fetch skill gaps from Feature 3 output
  - Display one simulation card per `must_learn_skills[]` item
  - Text input / code editor for user response
  - On submit: POST `/api/simulate` → render feedback card
  - Allow retry
- [ ] Wire `submitSimulation(skillId, response)` in `lib/api.ts`
- [ ] Wrap with `@tanstack/react-query` `useMutation`

### Day 5
- [ ] End-to-end test: full flow from `/results` skill gap → `/pathway/[roleId]` → simulation → feedback
- [ ] Handle edge cases: evaluator timeout, no scenario available for a skill
- [ ] Document Feature 4 in GitHub README

---

## Person E — Phase 3 Owner: Feature 2 + Feature 6 (CTCI + Stress-Test)

**Scope:** Feature 2 (Cognitive Task Compression Index) + Feature 6 (Career Stress-Test Engine). Prep Day 1–3, build Day 4–5.

### Day 1 (Prep)
- [ ] Download O*NET database: `Abilities.txt`, `Work Activities.txt`, `Tasks.txt`
- [ ] Research AIOE, GPTs-are-GPTs, and Webb AI exposure datasets:
  - AIOE: https://www.researchgate.net/publication/351174628
  - GPTs-are-GPTs: https://arxiv.org/abs/2303.10130
  - Webb: https://arxiv.org/html/2412.04924v1
- [ ] Download/scrape available scores per O*NET-SOC occupation code

### Day 2 (Prep)
- [ ] Load O*NET `Abilities.txt` + `Work Activities.txt` into Supabase (coordinate with Person A for schema)
- [ ] Compute preliminary `reasoning_intensity` per O*NET-SOC code
- [ ] Pull OpenDOSM Job Market Insights quarterly data → `occupation_my_signal` table

### Day 3 (Prep — finalize data, Feature 3 pipeline now available for testing)
- [ ] Merge AIOE / GPTs / Webb scores into `occupation_ai_exposure` table
- [ ] Apply MASCO 2020 crosswalk to map `masco_code` → `onet_soc_code` for all occupations
- [ ] Validate: every ESCO occupation in `role_vectors` has a corresponding `onet_soc_code` + CTCI score

### Day 4 AM — Feature 2 Build
- [ ] Compute CTCI per occupation:
  ```
  CTCI = (0.5 * Webb_score) + (0.25 * AIOE_score) + (0.25 * GPTs_score)
  ```
- [ ] Classify: Substitutive vs Complementary Compression (threshold: O*NET reasoning intensity median)
- [ ] Store `ctci_score` + `compression_type` + `compression_reasoning` in `occupation_ai_exposure`
- [ ] Add CTCI JOIN to `GET /api/match` response payload
- [ ] Coordinate with Person C: add CTCI widget to role cards on `/results`

### Day 4 PM — Feature 6 Build
- [ ] Compute disruption penalty matrix from CTCI data:
  - `disruption_penalty_fast` = `routine_cognitive_ratio * CTCI` (normalized 0–1)
  - `disruption_penalty_moderate` = `disruption_penalty_fast * 0.4` (softened)
- [ ] Store in `occupation_disruption_matrix`
- [ ] Implement scenario reweighting in `/api/match?scenario=fast`:
  ```
  Fast Disruption: Final Score = hybrid_score * (1 - disruption_penalty_fast)
                                + bonus_amplifier for soft_skill_intensity
  ```
- [ ] Test: same profile, Moderate vs Fast — role rankings should visibly differ

### Day 5
- [ ] Coordinate with Person C: add AI Shock Slider to `/results` page (framer-motion reorder animation)
- [ ] Validate: delta indicators (↑ / ↓) display correctly between scenarios
- [ ] Document CTCI formula + bias caveat (Rai 2026) in GitHub README
- [ ] Final end-to-end test: slider produces different role ranking

---

## Cross-Team Coordination Points

| Milestone | Involves | Target |
|---|---|---|
| BGE-M3 `/embed` endpoint live | Person B → Person A | End of Day 1 |
| Supabase schema + ESCO seeded | Person A → all | End of Day 1 |
| Feature 1 `POST /api/profile` live | Person B → Person C | End of Day 2 |
| Feature 3 `GET /api/match` live | Person A → Person C, Person D, Person E | End of Day 3 |
| `simulation_tasks` schema agreed | Person A + Person D | Start of Day 3 |
| RunPod LLM evaluator wired | Person B + Person D | Day 3 |
| O*NET data in Supabase | Person E → Person A (schema align) | End of Day 3 |
| CTCI JOIN added to `/api/match` | Person E → Person A | Day 4 AM |
| `/pathway/[roleId]` page live | Person D → Person C | Day 4 |
| Feature 6 slider UI | Person E → Person C | Day 5 |

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
