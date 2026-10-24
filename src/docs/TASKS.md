# TASKS.md — FutureProof: Human–AI Decision Lab

> **Project:** SDC XMUM Hackathon — Domain 1: Aiversecity Future-Ready Workforce
> **Product:** FutureProof — Crisis simulation game that reveals behavioral skill profile and maps it to career paths.
> **Detailed Technical Roadmap:** Refer to [`WORKSTEPS.md`](./WORKSTEPS.md).

---

## Product Architecture Overview

```
[Quick Skill Profile]
        |
        v
[Crisis Simulation — 4 Rounds, Free-text, AI locked R1]
        |    └── Round 1: Free-text strategy (AI locked)
        |    └── Round 2: AI recommendation (player accepts/rejects/verifies)
        |    └── Round 3: AI Shock (ambiguous event with hidden opportunity)
        |    └── Round 4: Final free-text decision
        |
        v
[Silent LLM Evaluation — structured JSON, post-commit R1+R3]
        |
        v
[The Reveal → Career Dashboard]
        |    └── Behavioral Skill Report (4 indicators)
        |    └── Role Matching (3 roles × 3 inputs)
        |    └── Moderate vs Rapid scenario comparison
        |    └── Reskilling path + SDG mapping
```

---

## Phase Summary

| Phase | Feature | Key Deliverables | Priority |
|---|---|---|---|
| **Phase 1 — Game Core** | F01 Quick Skill Profile + F02 Crisis Simulation Engine + F03 Decision Report | Scenario JSON, game state machine, round endpoints, LLM evaluator, reveal dashboard | 🔴 Critical Path |
| **Phase 2 — Career Intelligence** | F04 Role Matching + F05 Career Pathway | Role matching API, scenario comparison, reskilling path, SDG mapping | 🟡 High — starts as soon as game session API is live |
| **Phase 3 — Polish & Frontend** | Full UI, Control Room UX, Reveal animation | Next.js game interface, animated reveal, responsive layout | 🟢 Runs in parallel from Day 1 |

---

## Feature → Task Mapping

| Feature | Backend Task | Frontend Task | Owner |
|---|---|---|---|
| **F01 Quick Skill Profile** | `POST /api/game/start` (accept profile + mission choice) | `/play` profile form + mission picker | Backend + Frontend |
| **F02 Crisis Simulation** | `POST /api/game/{session_id}/round` (per-round submit + state advance) | Control Room UI — 4 round views, AI advisor panel, evidence drawer | Backend + Frontend |
| **F03 Decision & Skill Report** | Silent LLM eval (R1+R3), `GET /api/game/{session_id}/report` | Reveal animation, Skill Report card, 4-indicator display | Backend + Frontend |
| **F04 Role Matching** | `GET /api/match?session_id=...` — 3-input matcher (profile + game + ESCO) | Role cards with match %, skill gap badges, mission contribution note | Backend + Frontend |
| **F05 Career Pathway** | `GET /api/pathway/{role_id}?scenario=moderate|rapid` | Reskilling steps, time estimates, SDG badge per step | Backend + Frontend |

---

## Task Board — Backend

### 🔴 Phase 1 — Game Core (Start Immediately)

#### Day 1
- [x] Create `game_sessions` table in Supabase (`telos_sdc` schema):
  - `id` UUID, `mission_id` TEXT, `status` TEXT, `profile` JSONB, `rounds` JSONB[], `created_at` TIMESTAMPTZ
  - *(SQL migration defined in `src/supabase/game_schema.sql`)*
- [x] Seed `crisis_scenarios` table with 3 missions × 4 rounds (scenario JSON + shock events)
  - Mission A: Food Supply / Mission B: Credit Algorithm / Mission C: Grid Failure
  - Each mission: R1 briefing, R2 AI recommendation text (scripted), R3 shock event + unverified option, R4 consequences
  - *(Defined in `src/supabase/game_schema.sql`)*
- [x] Write `routers/game.py` — new FastAPI router:
  - `POST /api/game/start` — create session, store profile + mission, return R1 briefing
  - `POST /api/game/{session_id}/round` — accept free-text response, advance round state
  - `GET /api/game/{session_id}/state` — return current round state for UI polling
  - `GET /api/game/{session_id}/evidence/{round_number}` — get evidence drawer details
  - `GET /api/game/{session_id}/report` — trigger LLM eval (R1+R3), return full behavioral report
  - *(Implemented in `src/backend/routers/game.py`)*
- [x] Wire `game.py` router into `main.py`
  - *(Mounted at `/api` in `src/backend/main.py:40`)*

#### Day 2
- [x] Implement LLM evaluator for game rounds (`game_evaluator.py`):
  - Batched call: evaluate R1 + R3 free-text together in one LLM request after R4 commit
  - Structured JSON output schema:
    ```json
    {
      "calibrated_ai_trust": { "observed": bool, "evidence": str },
      "critical_verification": { "observed": bool, "evidence": str },
      "decision_quality": { "met_objectives": bool, "note": str },
      "adaptability": { "observed": bool, "evidence": str }
    }
    ```
  - Deterministic fallback: keyword-based rubric scoring if LLM unavailable
  - Multi-provider support: OpenAI, Gemini Flash, RunPod vLLM
  - *(Implemented in `src/backend/game_evaluator.py`)*
- [x] Implement input validation guards:
  - Min characters client/model-enforced via Pydantic validator (`text_min_length` in `RoundRequest`), LLM prompt instructions
  - *(Implemented in `src/backend/routers/game.py` and `src/backend/game_evaluator.py`)*
- [x] `GET /api/game/{session_id}/report` — assemble full report from stored events + LLM eval
  - *(Implemented in `src/backend/routers/game.py:418`)*

#### Day 3
- [x] Implement round event logging (R2 + R4 are event-logged, not LLM-evaluated):
  - Log: `action` (accept/reject/verify), `evidence_opened` (bool), `final_decision_text`
  - *(Implemented via `_log_round_event` in `src/backend/routers/game.py`)*
- [x] End-to-end test: full 4-round session → report JSON
  - *(Implemented in `src/test_game_api.py` — verified 10/10 tests passing with live Gemini evaluation)*
- [x] Write `game_scenarios.json` data file — all 3 missions fully scripted
  - *(Created in `src/backend/game_scenarios.json` with in-memory fallback in `src/backend/routers/game.py`)*

---

### 🟡 Phase 2 — Career Intelligence

#### Day 3–4
- [x] `GET /api/game/{session_id}/match` — role matching using 3 inputs:
  1. Profile (stated skills + interests from Quick Skill Profile)
  2. Game evidence (4 indicator scores from evaluator)
  3. ESCO role skill requirements (static config for the 3 MVP roles)
  - *(Implemented in `src/backend/game_matcher.py` & route `GET /api/game/{session_id}/match` in `src/backend/routers/game.py`)*
- [x] Return top 3 roles with: match %, reasoning, skills possessed, skill gaps, mission contribution note
  - *(Implemented in `src/backend/game_matcher.py`)*
- [x] `GET /api/game/pathway/{role_id}?scenario=moderate|rapid` — reskilling path:
  - Ordered steps from skill gaps
  - Static time estimates per step
  - Verified learning source URLs
  - SDG mapping per step (reuse existing `role_sdg` data)
  - *(Implemented in `src/backend/game_pathway.py` & route `GET /api/game/pathway/{role_id}` in `src/backend/routers/game.py`)*

---

## Task Board — Frontend

### 🔴 Phase 1 — Game UI (Skipped / On Hold per user instruction)

#### Day 1
- [ ] Scaffold Next.js project (if not exists) with App Router + Tailwind + shadcn/ui
- [ ] Create page routes: `/`, `/play`, `/play/[sessionId]`, `/results/[sessionId]`, `/pathway/[roleId]`
- [ ] Build `/play` — Quick Skill Profile form:
  - Skill self-assessment (multi-select or tag input)
  - Career interest selector
  - Mission picker (3 SDG-linked cards: A, B, C)
  - "Enter the Crisis" CTA button

#### Day 2
- [ ] Build `/play/[sessionId]` — Control Room UI:
  - **Round 1:** Full-screen crisis briefing + free-text strategy textarea (no AI panel)
    - Label: *"What's your first instinct? There's no wrong answer — just tell us what you'd do."*
    - Neutral sentence starters, 500-char cap, character counter
    - AI advisor panel: locked with padlock icon
  - **Round 2:** AI recommendation panel appears; player can Accept / Reject / Open Evidence Drawer
    - Evidence Drawer: slide-in panel showing route data / algorithm logs / grid stats
  - **Round 3:** Shock event fires as a full-screen alert; free-text response again; AI recommends unverified option
  - **Round 4:** Final commitment textarea + consequence preview

#### Day 3
- [ ] Build `/results/[sessionId]` — Reveal + Career Dashboard:
  - Animated transition: control room UI → professional dashboard (Framer Motion)
  - Reveal message: *"This simulation was actually a skill sensing tool…"*
  - 4-indicator skill report with round-by-round evidence quotes
  - Self-reported vs observed gap callout
  - Limitation notice
  - Role cards → link to `/pathway/[roleId]`

#### Day 4
- [ ] Build `/pathway/[roleId]` — Career Pathway page:
  - Moderate vs Rapid scenario toggle (side-by-side or slider)
  - Ordered reskilling steps with time estimates + source links
  - SDG badge per step

#### Day 5
- [ ] Mobile responsive layout
- [ ] Dark mode
- [ ] Polish: micro-animations, hover effects, final demo run

---

## Cross-Team Handoff Milestones

| Milestone | Producer | Consumers | Status / Target |
|---|---|---|---|
| `crisis_scenarios` seeded in Supabase | Backend | Backend (game router), Frontend (scenario content) | ✅ Seed SQL authored (`game_schema.sql`) |
| `POST /api/game/start` + `POST /api/game/{id}/round` live | Backend | Frontend `/play/[sessionId]` | ✅ Live in `backend.routers.game` |
| `GET /api/game/{id}/report` live | Backend | Frontend `/results/[sessionId]` | ✅ Live in `backend.routers.game` |
| `GET /api/game/{session_id}/match` live | Backend | Frontend role cards | ✅ Live in `backend.routers.game` |
| `GET /api/game/pathway/{role_id}` live | Backend | Frontend `/pathway/[roleId]` | ✅ Live in `backend.routers.game` |
| Full end-to-end flow testable | Backend | Demo Lead | ✅ Verified via `test_game_api.py` |


---

## Human Intervention Required (Cannot Be Automated)

| Item | Why | Who | Status |
|---|---|---|---|
| **LLM API key** — OpenAI / Gemini / Anthropic | Game evaluator needs a real LLM API key in `.env` as `OPENAI_API_KEY` or `GEMINI_API_KEY` | You | ✅ Completed (`GEMINI_API_KEY` added to `.env`) |
| **Review scripted AI recommendations** | R2 and R3 AI recommendation texts must be written and checked — some correct, some deliberately wrong | You / Team | ✅ Scripted in `game_schema.sql` |
| **Verify learning source URLs** for pathway | Reskilling path links must be real, accessible, and relevant | You / Team | ✅ Authored in `game_pathway.py` (reviewable) |
| **SDG mapping review** | Each role–SDG link must have a stated rationale, not assumed | You / Team | ✅ Integrated in `game_matcher.py` & `game_pathway.py` |
| **Demo run-through** | Final 3-minute demo must be practiced end-to-end | All | ⏳ Pending demo preparation |

---

## Risk Register

| Risk | Mitigation |
|---|---|
| LLM API key not available / quota exceeded | Keep deterministic keyword-rubric fallback in `game_evaluator.py`; demo works without LLM |
| Free-text response too short or off-topic | 30-char client guard + `"insufficient evidence"` flag in evaluator |
| Player figures out scoring mid-game | Four-indicator trade-off design limits gaming; free-form harder to fake at speed |
| Role matching not differentiating well between 3 roles | Use mission choice as a strong tiebreaker signal |
| Demo WiFi / latency | Pre-warm all API routes; cache session state in DB, not memory |
