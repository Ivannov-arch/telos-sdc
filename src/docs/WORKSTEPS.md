# WORKSTEPS — FutureProof: Human–AI Decision Lab

> **Context:** Technical execution roadmap for all 5 features of the FutureProof MVP.
> **Core proposal:** [`Integrated Proposal.md`](./Integrated%20Proposal.md)
> **Team task division and daily schedule:** [`TASKS.md`](./TASKS.md)

---

## Core Design Principle: Behavioral Evidence, Not Self-Report

Every technical decision in this codebase serves one goal: capture genuine decision-making behavior, not curated self-presentation.

- **Free-text input in R1 + R3:** Ungameable because the player doesn't see the rubric.
- **LLM evaluation is post-commit and silent:** Player never knows evaluation is happening during gameplay.
- **Structured JSON output from LLM:** Rubric is hardcoded; LLM fills evidence strings and booleans only. Final scores derived deterministically.
- **Scoring is self-referential:** A mirror of the player's own behavior, not a ranking against others.
- **Reveal moment:** The dashboard appears only after R4. The game-to-dashboard transition is the product's differentiator.

---

## Phase Overview

| Phase | Features | Days | Priority |
|---|---|---|---|
| **Phase 1 — Game Core** | F01 (Quick Skill Profile) + F02 (Crisis Simulation) + F03 (Decision & Skill Report) | Day 1–3 | 🔴 Critical path — must be demo-ready |
| **Phase 2 — Career Intelligence** | F04 (Role Matching) + F05 (Career Pathway + SDG) | Day 3–4 | 🟡 High — starts immediately after game session API is live |
| **Phase 3 — UI Polish** | Full game UI + Reveal animation + Responsive | Day 1–5 (parallel) | 🟢 Parallel track |

---

## Dependency Graph

```
F01: Quick Skill Profile (profile form + mission select)
        |
        └──► F02: Crisis Simulation (game state machine + 4 rounds)
                    |
                    └──► F03: Decision Report (LLM evaluator + reveal)
                                |
                                └──► F04: Role Matching (3-input matcher)
                                              |
                                              └──► F05: Career Pathway (steps + SDG + scenarios)
```

---

## Database Schema (Supabase — `telos_sdc` schema)

### New Tables (Game Engine)

#### `game_sessions`
```sql
CREATE TABLE telos_sdc.game_sessions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    mission_id      TEXT NOT NULL,          -- 'A' | 'B' | 'C'
    status          TEXT NOT NULL DEFAULT 'round_1',
                                            -- round_1 | round_2 | round_3 | round_4 | complete
    profile         JSONB NOT NULL,         -- { skills[], interests[], learning_time }
    rounds          JSONB NOT NULL DEFAULT '[]',
                                            -- array of round event objects
    eval_result     JSONB,                  -- filled after R4 by LLM evaluator
    created_at      TIMESTAMPTZ DEFAULT now(),
    completed_at    TIMESTAMPTZ
);
```

#### `crisis_scenarios`
```sql
CREATE TABLE telos_sdc.crisis_scenarios (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    mission_id          TEXT NOT NULL,      -- 'A' | 'B' | 'C'
    round_number        INTEGER NOT NULL,   -- 1 | 2 | 3 | 4
    briefing_text       TEXT NOT NULL,      -- what the player reads
    ai_recommendation   TEXT,              -- R2 only: scripted AI recommendation text
    evidence_data       JSONB,             -- R2 only: data available in evidence drawer
    shock_event_text    TEXT,              -- R3 only: the disruption announcement
    shock_opportunity   TEXT,             -- R3 only: unverified option text
    consequence_formula JSONB              -- R4 only: how to compute outcome from decision
);
```

#### `round_events`
```sql
CREATE TABLE telos_sdc.round_events (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id      UUID REFERENCES telos_sdc.game_sessions(id),
    round_number    INTEGER NOT NULL,
    action          TEXT,                  -- 'accept' | 'reject' | 'verify' | 'free_text'
    free_text       TEXT,                  -- R1, R3 free-text responses
    evidence_opened BOOLEAN DEFAULT FALSE, -- did player open evidence drawer in R2
    ai_trusted      BOOLEAN,              -- did player follow AI recommendation in R2/R3
    created_at      TIMESTAMPTZ DEFAULT now()
);
```

### Existing Tables (Reuse for Career Intelligence)
- `skills`, `occupations`, `role_required_skills` — ESCO taxonomy (already seeded)
- `role_sdg` — SDG mappings (already seeded with 2,054 mappings)
- `role_vectors` — BGE-M3 embeddings (already generated)

---

# PHASE 1 — Game Core (Day 1–3)

## FEATURE 01: Quick Skill Profile

> **Goal:** Capture player's self-declared starting point in under 2 minutes — no login, no CV upload required.

### What it collects
- `skills[]` — multi-select from predefined list (30–50 common skills, not ESCO IDs for UX simplicity)
- `interests[]` — career domain interests (e.g., "AI ethics", "data analysis", "infrastructure")
- `learning_time` — hours per week available for upskilling
- `mission_id` — chosen crisis mission (A, B, or C)

### API
**`POST /api/game/start`**
```json
Request:
{
  "profile": {
    "skills": ["Python", "Critical Thinking", "Data Analysis"],
    "interests": ["AI Governance", "Public Policy"],
    "learning_time": 5
  },
  "mission_id": "A"
}

Response:
{
  "session_id": "uuid",
  "round": 1,
  "briefing": "Southeast Asia food supply chains have collapsed...",
  "instructions": "What is your strategy? There is no wrong answer — just tell us what you would do."
}
```

### Implementation Notes
- Profile is stored as JSONB in `game_sessions.profile` — no normalization to ESCO IDs at this stage
- ESCO mapping happens later during role matching (F04), not at intake
- Mission choice (A/B/C) is stored and used as a strong signal in role matching

---

## FEATURE 02: Crisis Simulation (Game State Machine)

> **Goal:** 4-round game loop with free-text R1+R3, event-logged R2+R4, scripted AI recommendations, and one ambiguous shock per mission.

### Round State Machine
```
round_1 (free-text) → round_2 (AI rec + accept/reject/verify) → round_3 (shock + free-text) → round_4 (final free-text) → complete
```

### API
**`POST /api/game/{session_id}/round`**
```json
Request (R1 example):
{
  "round": 1,
  "free_text": "I would prioritize the northern routes first because...",
  "action": null,
  "evidence_opened": null
}

Request (R2 example):
{
  "round": 2,
  "action": "verify",        // "accept" | "reject" | "verify"
  "evidence_opened": true,
  "free_text": null
}

Response (all rounds):
{
  "session_id": "uuid",
  "round_accepted": 1,
  "next_round": 2,
  "next_briefing": "The AI advisor has a recommendation...",
  "ai_recommendation": "Route via corridor B is 40% faster...",  // R2 only
  "evidence_available": true,                                     // R2 only
  "shock_event": null                                             // R3 only when round=3
}
```

**`GET /api/game/{session_id}/state`** — returns current round + briefing content

### Round Content (Scripted per Mission)

Each mission's rounds are loaded from `crisis_scenarios` table. Key design rules:
- **R1:** No AI recommendation, no options list. Briefing sets the crisis scene.
- **R2:** AI recommendation appears. Some missions: AI is correct. Some: AI ignores a critical data point in the evidence drawer. Player doesn't know which.
- **R3:** Shock fires. AI advisor immediately recommends the unverified option without noting the uncertainty. Player must decide whether to check before acting.
- **R4:** Final commitment. System computes consequences from decision text (keyword-based consequence lookup, not LLM).

### Input Validation
- R1 + R3 minimum 30 characters client-side
- 500 character cap client-side (bounds LLM token cost)
- Backend: if free_text < 10 words, flag as `"insufficient_evidence"` for that round

---

## FEATURE 03: Decision & Skill Report

> **Goal:** After R4 is committed, batch-evaluate R1 + R3 free-text in one LLM call. Return a structured behavioral report. Never show the rubric during gameplay.

### The 4 Indicators
| Indicator | Measured via |
|---|---|
| **Calibrated AI Trust** | R2: did player override AI after checking evidence? R3: did player question the AI's unverified recommendation? |
| **Critical Verification** | R2: was evidence drawer opened before deciding? R3: was unverified option questioned? |
| **Decision Quality** | R1 + R4: did strategy text address mission constraints? Did R4 decision address R3 shock constraints? |
| **Adaptability** | R1 vs R3: did strategy meaningfully shift after the shock event? |

### LLM Evaluator (`game_evaluator.py`)

**Batched call design:** R1 and R3 free-text are sent in a single LLM call after R4 is committed.

**System prompt structure:**
```
You are a silent behavioral analyst. You have two player responses from a crisis simulation game.
The player does NOT know they are being evaluated on these criteria.
Evaluate each indicator and return ONLY valid JSON matching the schema below.
Do not invent evidence. Only extract what is present in the text.

Schema:
{
  "calibrated_ai_trust": { "observed": <bool>, "evidence": "<direct quote or paraphrase from text>" },
  "critical_verification": { "observed": <bool>, "evidence": "<direct quote or paraphrase>" },
  "decision_quality": { "met_objectives": <bool>, "note": "<one sentence>" },
  "adaptability": { "observed": <bool>, "evidence": "<comparison between R1 and R3 text>" }
}

Round 1 response: {r1_text}
Round 3 response: {r3_text}
Mission context: {mission_context}
```

**Fallback (no LLM):** Keyword-based deterministic evaluator:
- Calibrated AI Trust: did response text contain words like "verify", "check", "data", "uncertain", "not sure about AI"
- Critical Verification: did R2 event log show `evidence_opened=true`
- Decision Quality: rubric keyword coverage (mission-specific keyword list)
- Adaptability: Levenshtein similarity between R1 and R3 texts (low similarity = high adaptability)

**`GET /api/game/{session_id}/report`**
```json
Response:
{
  "session_id": "uuid",
  "mission": "A",
  "profile": { ... },
  "indicators": {
    "calibrated_ai_trust": { "observed": true, "evidence": "In Round 3, you questioned the AI before accepting..." },
    "critical_verification": { "observed": true, "evidence": "You opened the capacity data before deciding in Round 2." },
    "decision_quality": { "met_objectives": true, "note": "Final strategy covered population reach and budget constraints." },
    "adaptability": { "observed": true, "evidence": "Strategy shifted from centralized routing to distributed approach after the shock." }
  },
  "self_vs_observed_gap": {
    "claimed_skills": ["Critical Thinking", "Data Analysis"],
    "observed_strengths": ["Critical Verification", "Adaptability"],
    "note": "Your observed behavior aligns with your stated data analysis skills."
  },
  "limitation_notice": "This evidence comes from one 4-round simulation. It is not sufficient to conclude your professional ability in general.",
  "role_match_available": true
}
```

---

# PHASE 2 — Career Intelligence (Day 3–4)

## FEATURE 04: Future Skills Radar & Role Matching

> **Goal:** Match player to 3 roles using 3 combined inputs. Display match %, reasoning, gaps, and how the mission choice contributed.

### 3-Input Matching

| Input | Source | Weight |
|---|---|---|
| **Profile** | Stated skills + interests from Quick Skill Profile | ~30% |
| **Game evidence** | Indicator scores from F03 evaluator | ~40% |
| **Role requirements** | ESCO skill lists from existing `role_required_skills` table | ~30% |

### The 3 MVP Roles
| Role | ESCO Reference | Key Indicators |
|---|---|---|
| **AI Application Engineer** | ESCO: Software Developer / AI specialist | Decision Quality + Adaptability |
| **Data Analyst** | ESCO: Data Analyst | Critical Verification + Decision Quality |
| **AI Governance / Risk Analyst** | ESCO: Risk Analyst / Ethics Auditor | Calibrated AI Trust + Critical Verification |

### Role–Mission Contribution Signal
Mission choice (A/B/C) biases the match:
- Mission A (Food Supply) → supply chain / operations roles
- Mission B (Credit Algorithm) → ethics / governance / financial risk roles
- Mission C (Grid Failure) → infrastructure / systems / engineering roles

### API
**`GET /api/match?session_id={uuid}`**
```json
Response:
{
  "roles": [
    {
      "rank": 1,
      "title": "AI Governance / Risk Analyst",
      "esco_id": "esco:2631",
      "match_score": 0.84,
      "reasoning": "Your critical verification behaviour and calibrated AI trust align strongly with this role's core requirements.",
      "skills_possessed": ["Critical Thinking", "Data Analysis"],
      "skill_gaps": [
        { "skill": "Regulatory Frameworks (EU AI Act)", "urgency": "high" },
        { "skill": "Algorithmic Bias Testing", "urgency": "medium" }
      ],
      "mission_contribution": "Mission B (Credit Algorithm bias) directly maps to AI fairness auditing.",
      "sdg_alignment": [
        { "sdg_goal": 10, "sdg_name": "Reduced Inequalities", "impact_reasoning": "..." }
      ]
    }
  ],
  "data_source": "ESCO v1.2 (2023)",
  "data_date": "2023-06-01",
  "guardrail": "This profile is one signal from one simulation. It is not a professional assessment."
}
```

---

## FEATURE 05: Future Career Pathway

> **Goal:** Build a sequential reskilling path from skill gaps, with time estimates, verified sources, and SDG mapping. Show under two AI adoption scenarios.

### Two Scenarios
| Scenario | Logic |
|---|---|
| **Moderate** | Standard skill gap ranking — learn core gaps first |
| **Rapid** | Soft skills and judgment-intensive skills are up-ranked; routine technical skills de-prioritized |

Scenario logic is transparent parameter-switching, not a forecasting model. All outputs labeled as "estimates".

### API
**`GET /api/pathway/{role_id}?scenario=moderate|rapid&session_id={uuid}`**
```json
Response:
{
  "role": "AI Governance / Risk Analyst",
  "scenario": "moderate",
  "steps": [
    {
      "step": 1,
      "skill": "Regulatory Frameworks (EU AI Act)",
      "urgency": "high",
      "time_estimate_weeks": 3,
      "sources": [
        { "title": "EU AI Act Overview — European Commission", "url": "https://..." }
      ],
      "sdg": { "goal": 16, "name": "Peace, Justice and Strong Institutions", "rationale": "..." }
    }
  ],
  "total_estimated_weeks": 12,
  "scenario_note": "Under Moderate AI adoption, technical regulatory knowledge is the priority gap to close."
}
```

### Learning Sources (Human Intervention Required)
Sources must be manually verified. Use:
- Coursera, edX, LinkedIn Learning for courses
- Official EU/UN documentation for regulatory skills
- Google / Microsoft AI skills programs
- Each URL must be live and publicly accessible

---

# Technical Architecture

## Backend Stack
| Layer | Technology |
|---|---|
| **Web framework** | FastAPI (Python) |
| **Database** | Supabase / PostgreSQL (`telos_sdc` schema) |
| **LLM evaluation** | OpenAI GPT-4o-mini or Gemini Flash (single batched call per session) |
| **Fallback evaluator** | Deterministic keyword + event-log based scoring (no LLM required) |
| **Game state** | Stored in `game_sessions.rounds` JSONB — stateless API, DB-backed |

## New Router: `routers/game.py`
Endpoints:
```
POST /api/game/start                   → create session, return R1 briefing
POST /api/game/{session_id}/round      → submit round response, advance state
GET  /api/game/{session_id}/state      → current round + briefing for UI
GET  /api/game/{session_id}/report     → trigger LLM eval, return full behavioral report
GET  /api/match?session_id=...         → role matching (3-input)
GET  /api/pathway/{role_id}?scenario=  → reskilling path
```

## Existing Routers (Kept, No Breaking Changes)
- `routers/profile.py` — `POST /api/profile` (CV upload) — kept for old pipeline
- `routers/match.py` — `GET /api/match?user_id=...` — kept, new `session_id` param added
- `routers/simulate.py` — `POST /api/simulate` (micro-task eval) — kept for F04 pathway micro-tasks

---

# Scenario Data: `crisis_scenarios` Seed File

## Mission A — Supply Under Pressure

**R1 Briefing:**
> "The food supply chain across Southeast Asia has collapsed following simultaneous port disruptions in three countries. You are the crisis response coordinator. Millions are at risk. You have a limited budget and four available distribution routes. What is your strategy?"

**R2 AI Recommendation (scripted):**
> "AI Advisor recommends Route B — it is 40% faster than alternatives and covers the highest population density zones. Estimated delivery: 18 hours."
> *(Note: Route B has an unreported capacity limit of 60% — visible in evidence drawer, NOT mentioned by AI)*

**R3 Shock Event:**
> "BREAKING: Budget has been cut by 50% effective immediately. Route B is now confirmed over capacity. However, a community volunteer network of 400 logistics workers has just offered assistance — no formal vetting completed yet."
> *(AI Advisor: "I recommend activating the volunteer network immediately — it's your best option given the constraints.")*
> *(Note: Volunteer network is unverified — capacity, reliability, and food safety compliance unknown)*

**R4 Final:**
> "Commit your final distribution strategy. The system will calculate outcomes: population reached, cost, delivery time, and groups most affected."

---

## Mission B — The Credit Algorithm

**R1 Briefing:**
> "A financial institution's credit scoring AI has been leaking biased outputs for 6 months, systematically denying loans to applicants from two demographic groups. You are the ethics response lead. Regulators are watching. You have limited time and resources. What is your strategy?"

**R2 AI Recommendation (scripted):**
> "AI Advisor recommends immediately patching the scoring model with re-weighted training data. Estimated fix: 72 hours, minimal customer disruption."
> *(Note: The patch does not address root cause — biased feature selection — visible in technical audit log in evidence drawer)*

**R3 Shock Event:**
> "A new regulation just passed making your current patch approach non-compliant. The press has published the story. However, a whistleblower inside the institution has leaked internal model architecture documents that could allow a proper root-cause fix in 48 hours."
> *(AI Advisor: "Use the whistleblower documents immediately — the fastest path to compliance.")*
> *(Note: Whistleblower documents have not been verified as authentic or legally obtained)*

**R4 Final:**
> "Commit your remediation approach. The system will evaluate: regulatory compliance, affected customer groups, reputational impact, and timeline."

---

## Mission C — Grid Failure

**R1 Briefing:**
> "A major green energy grid has failed during peak demand in a densely populated region. Hospitals, emergency services, and 2.3 million homes are affected. You are the infrastructure crisis lead. Multiple rerouting options exist but each has trade-offs. What is your strategy?"

**R2 AI Recommendation (scripted):**
> "AI Advisor recommends activating the eastern interconnect line — it has the highest rated capacity and shortest rerouting time of 4 hours."
> *(Note: Eastern line stability data is 8 months old — grid conditions may have changed. Available in technical data drawer.)*

**R3 Shock Event:**
> "A neighboring grid has just failed, doubling the affected population to 4.6 million. Eastern line is now confirmed insufficient. An emergency interconnect line from the northern sector is available — it could handle the load, but its structural integrity data has not been reviewed since installation."
> *(AI Advisor: "Activate the northern emergency line immediately — it is your only viable option.")*
> *(Note: Northern line integrity is unverified — last inspection: 3 years ago)*

**R4 Final:**
> "Commit your final rerouting strategy. The system will calculate: population restored, time to restoration, risk of secondary failure, and groups still without power."

---

# Checklist: Definition of Done

### Phase 1 — Game Core
- [ ] `game_sessions` and `crisis_scenarios` tables live in Supabase
- [ ] All 3 missions × 4 rounds seeded in `crisis_scenarios`
- [ ] `POST /api/game/start` → returns R1 briefing
- [ ] `POST /api/game/{id}/round` → advances state, validates input, logs events
- [ ] `GET /api/game/{id}/report` → returns structured behavioral report (LLM or fallback)
- [ ] End-to-end: full 4-round session → report JSON working

### Phase 2 — Career Intelligence
- [ ] `GET /api/match?session_id=...` → returns 3 ranked roles with gaps + SDG
- [ ] `GET /api/pathway/{role_id}?scenario=...` → returns ordered steps with sources
- [ ] Moderate vs Rapid produces visibly different step ordering

### Phase 3 — UI
- [ ] `/play` — profile form + mission picker
- [ ] `/play/[sessionId]` — all 4 round views working
- [ ] `/results/[sessionId]` — reveal animation + full report + role cards
- [ ] `/pathway/[roleId]` — reskilling steps + scenario toggle + SDG badges
- [ ] Mobile responsive + dark mode

### Human Intervention Checklist
- [ ] LLM API key set in `.env` (`OPENAI_API_KEY` or `GEMINI_API_KEY`)
- [ ] Scripted AI recommendation texts reviewed for each mission (correct vs. subtly wrong)
- [ ] Learning source URLs manually verified and live
- [ ] SDG mappings reviewed for stated rationale
- [ ] Final demo run-through completed