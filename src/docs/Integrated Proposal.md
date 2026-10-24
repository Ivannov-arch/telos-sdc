# FutureProof — Integrated MVP Proposal

> **Core concept:** A crisis simulation game that reveals how you make decisions alongside AI, then connects that behavioral evidence — combined with your stated skills and interests — to career recommendations, skill gaps, and a personalised reskilling path.

---

## Overview

Most skill-assessment tools rely on self-reporting: fill in a CV, answer a 100-question psychometric test, tick boxes. FutureProof takes a different approach. Players are dropped into a live global crisis. Their *instincts* — whether they verify evidence, challenge AI advice, or adapt under pressure — are observed and turned into a skill profile. The result feels like a game; the output is a career intelligence report.

The jury pitch: *"We won't ask you to fill in a CV. Let's play your career future for 3 minutes."*

---

## The 5 MVP Features

### Feature 01 — Quick Skill Profile *(Required)*

**Purpose:** Establish a baseline before the game, so the final report can cross-reference what the player *claimed* versus what was *observed* in practice.

**What the player inputs:**
- Current skills and areas of strength (self-assessed)
- Career interests and target domains
- Available time for learning / upskilling

**What the system does with it:**
- Builds an initial profile used as one of three matching inputs for career roles (alongside game evidence and job skill requirements)
- Surfaces any gap between self-declared skills and observed decision behaviour — this contrast itself is informative
- Pre-populates the reskilling path with relevant starting points

**No login or CV required for demo.** The profile takes under 2 minutes.

---

### Feature 02 — Crisis Simulation *(Core feature)*

#### Mission Selection

Rather than a single fixed scenario, players choose one of three **SDG-linked crisis missions**:

| Mission | Crisis | SDG |
|---|---|---|
| **A — Supply Under Pressure** | Food supply chain collapse in Southeast Asia | SDG 2 — Zero Hunger |
| **B — The Credit Algorithm** | Financial credit algorithm leak causing systemic bias | SDG 10 — Reduced Inequalities |
| **C — Grid Failure** | Green energy network failure during peak demand | SDG 7 — Affordable & Clean Energy |

Each mission covers the same decision-making mechanics. Mission choice signals the player's domain interest and contributes to role matching.

#### Gameplay Loop (4 Rounds)

The UI looks like a **Control Room** or crisis terminal — not a job application form.

**Round 1 — Set Your Strategy (Free-form, No AI)**
The player reads the crisis briefing and types their own strategy in free text — no multiple-choice options, no prompts that hint at what a "good" answer looks like. The AI advisor is locked and unavailable. Once the player submits, their input is committed and cannot be changed.

Why free-form? Structured choices telegraph what the "correct" answer looks like just by existing on screen. Free-form input cannot be reverse-engineered. Because the player is in problem-solving mode — not test-taking mode — the response reflects genuine instincts rather than curated self-presentation.

After the player commits, the system makes a single silent LLM call to evaluate the response against the rubric. The player never sees this happening. The result is stored and revealed only at the end.

**Round 2 — AI Recommends**
The AI advisor unlocks. The system presents an AI recommendation (e.g., fastest distribution path, statistically optimal energy reroute). The player can:
- Accept the recommendation
- Reject it and override with their own decision
- First examine supporting data (route capacity, population impact, cost) before deciding

Some AI recommendations are correct. Some deliberately ignore critical evidence. The player does not know which — and that ambiguity is the point.

**Round 3 — The AI Shock (Plot Twist)**
A disruption event fires mid-game without warning. Each mission has its own shock, native to its crisis context — not a generic penalty applied to all three:

| Mission | AI Shock Event |
|---|---|
| **A — Food Supply** | Budget is cut and one route is now over capacity — but a community volunteer network just became available (unverified) |
| **B — Credit Algorithm** | A new regulation just made the current fix illegal; the press found out — but a whistleblower also leaked internal data that could accelerate the solution |
| **C — Grid Failure** | A neighbouring grid just went down, doubling the affected population — but an emergency interconnect line is available, though its stability data is unconfirmed |

The player must respond in free text under the new conditions. This tests whether they adapt, anchor to Round 1 reasoning, or recognise the hidden opportunity embedded in the disruption.

#### Shock Type Design

Not all shocks are pure disadvantages. Each shock is designed to be **ambiguous** — containing both a constraint and a potential upside that requires verification:

| Shock Type | What it looks like | What it actually measures |
|---|---|---|
| **Constraint** | Budget halved, route closed, timeline compressed | Adaptability under pressure |
| **Opportunity** | New resource unlocked, faster route available, unexpected ally | Whether the player pivots to capture upside, or stays anchored to the old plan |
| **Ambiguous** *(MVP default)* | A new option appears — but the data supporting it is unverified | Critical Verification + Calibrated AI Trust: does the player check before acting, especially when the AI recommends it enthusiastically? |

For MVP, each mission uses **one ambiguous shock** — this tests adaptability *and* critical verification in a single event, without adding complexity. Pure disadvantage shocks are the easiest to design but the least revealing.

> **Design rule:** The AI advisor in Round 3 should recommend the new unverified option without flagging the data uncertainty. This creates a direct test of whether the player trusts the AI or verifies independently before acting.

**Round 4 — Final Decision**
The player commits to a final strategy in free text. The system calculates consequences: people reached, cost, time, and affected groups.

> **Important implementation note:** AI recommendations must be scenario-controlled. Some should be correct; some should deliberately ignore key evidence. Do not rely on a language model to make mistakes randomly — script the error cases.

#### What the Player Sees vs. What the System Does

| Round | Player Experience | System Action (hidden) |
|---|---|---|
| **Round 1** | "Describe your strategy" — free text, no AI, no options | Silent LLM call evaluates and tags reasoning post-commit |
| **Round 2** | AI recommendation appears; player accepts, rejects, or checks data | Logs whether evidence was verified before deciding |
| **Round 3** | AI Shock fires with a constraint + hidden opportunity; AI recommends the unverified option | Logs adaptation, anchoring, and whether the player verified before acting |
| **Round 4** | Final free-text commitment | Scores all four rounds; queues the Reveal |

---

### Feature 03 — Decision & Skill Report *(Required)*

#### How Scoring Works

Every round logs: initial decision, AI recommendation, evidence checked, final decision, outcome. Four indicators are scored against a pre-defined rubric. The LLM evaluates free-text responses and returns a **structured JSON output** (not prose) — it tags observations per indicator but does not assign the final score unilaterally. The rubric is hardcoded; the LLM only fills in the evidence.

| Indicator | What is measured |
|---|---|
| **Calibrated AI Trust** | Did the player adjust their reliance on AI based on evidence quality? |
| **Critical Verification** | Did the player check relevant data before deciding? |
| **Decision Quality** | Did the final decision meet the mission objectives within constraints? |
| **Adaptability** | Did the player revise strategy after the AI Shock event? |

**Important:** The score is entirely self-referential. It describes *your* decision pattern across four rounds — not a ranking against other players, not a pass/fail. There is no leaderboard, no percentile, no comparison. The report is a mirror, not a grade.

The rubric is never shown to the player during the game. The player does not know what is being observed. This is intentional — once a metric is visible, people optimise for the metric instead of behaving naturally (Goodhart's Law). The Reveal is the first moment the player learns what was being measured.

#### The Reveal

After the game ends, the win/loss screen transitions — the game UI slowly transforms into a **Professional Career Dashboard**. The system then discloses:

> *"This simulation was actually a skill sensing tool. Based on how you made decisions, we detected the following…"*

This moment works precisely because the player did not know the rubric existed. Free-form input in Round 1 and Round 3 makes the reveal feel genuine rather than like a rigged multiple-choice test.

#### Report Format

- Specific behavioural observations with round-by-round examples (not generic personality labels)
- Skill scores with a brief description (e.g., *Ethical Judgement — High, System Thinking — Moderate*)
- Contrast between self-declared skills (from Quick Skill Profile) and observed behaviour — gaps here are themselves informative
- Explicit limitation notice: *"This evidence comes from one simulation. It is not sufficient to conclude your professional ability in general."*

---

### Feature 04 — Future Skills Radar & Role Matching *(Required)*

#### Matching Inputs

Role recommendations use **three inputs combined**, not just the game result alone:

1. **Initial profile** — stated skills, interests, and available learning time
2. **Game evidence** — observed indicators from the simulation
3. **Job skill requirements** — verified skill lists per role, sourced from a single updatable dataset (e.g., ESCO or O\*NET taxonomy, supplemented with a labour market signal source that carries a data date)

The system must display its data source and the date of the dataset. Taxonomy alone does not prove current demand; a market signal source is also required.

#### The Three Roles (MVP)

| Role | Skill Focus |
|---|---|
| **AI Application Engineer** | Application development, AI integration, system testing |
| **Data Analyst** | Data analysis, interpretation, conclusion verification |
| **AI Governance / Risk Analyst** | Risk assessment, evidence evaluation, system impact review |

Each role recommendation includes:
- Match percentage and reasoning
- Skills the player already has
- Identified skill gaps
- How the mission chosen (A, B, or C) informed the match

> **Guardrail:** Do not conclude that someone is or is not suited to a role based solely on four rounds of a game. The profile is one signal, not a verdict.

---

### Feature 05 — Future Career Pathway *(Required)*

#### Two Scenarios

Once a role is selected, the system presents two AI adoption futures side-by-side:

| Scenario | Question answered |
|---|---|
| **Moderate** | How does the career path look if AI adoption grows gradually? |
| **Rapid** | How might skill requirements change if AI adoption accelerates? |

Scenario parameters are transparent — no complex forecasting model needed for MVP. Results must be labelled as *estimates*, not predictions. The system recalculates skill relevance and recommendations based on the differing assumptions.

#### Reskilling Path

Built from the identified skill gaps, the path includes:

- Ordered learning steps (sequential, not a dump of courses)
- Time estimates per step
- Verified, real learning sources with links
- SDG mapping per skill and role, with a clear rationale

**Example SDG mapping:** A role involving algorithmic bias review can be linked to SDG 10 (Reduced Inequalities) *if* the job description genuinely supports reducing inequality — the connection must be stated, not assumed.

---

## Tech Stack

| Layer | Choice |
|---|---|
| **Frontend** | Next.js + React |
| **Backend** | API routes or FastAPI |
| **Database** | Supabase / PostgreSQL |
| **Game engine** | State machine + scenario JSON |
| **AI** | Single LLM API, controlled |
| **Trend data** | One updatable source with data date |

Not needed for MVP: LangGraph, multi-agent architecture, multiplayer, or complex graphical simulation.

---

## Problems Introduced by Free-form Input (Option B) and How to Solve Them

Free-form input is the right design choice — but it introduces real engineering and UX problems. Each is solvable.

### Problem 1 — LLM Evaluation Is Non-Deterministic

**Risk:** The same response evaluated twice might produce slightly different scores.

**Solution:** Force structured output. The LLM call returns a JSON schema, not prose:
```json
{
  "calibrated_ai_trust": { "observed": true, "evidence": "Player overrode AI in Round 2 after checking capacity data" },
  "critical_verification": { "observed": false, "evidence": "No evidence data was opened before Round 2 decision" },
  "decision_quality": { "met_objectives": true, "note": "Reached 94% of target population within budget" },
  "adaptability": { "observed": true, "evidence": "Strategy changed significantly between Round 1 and Round 3" }
}
```
The rubric is hardcoded. The LLM only fills the `evidence` field and the boolean `observed`. Final indicator labels are derived from the booleans, not from the LLM's prose.

---

### Problem 2 — Player Writes Nonsense, Off-topic, or Blank Input

**Risk:** A player types "idk lol" or submits an empty field, breaking the evaluation pipeline.

**Solution:** Two-layer guard:
1. **Client-side:** Minimum character count (e.g., 30 characters) and a basic check that the input contains words. Block submission with a prompt: *"Tell us a bit more about your approach — what would you prioritise?"*
2. **LLM-side:** If the structured JSON evaluation returns `null` or low-confidence on all indicators, the system flags the round as *"insufficient evidence"* and excludes it from scoring rather than guessing. The report notes: *"Round 1 did not produce enough information to evaluate this indicator."*

---

### Problem 3 — Players Figure Out They're Being Measured Mid-Game

**Risk:** A savvy player notices the pattern ("they're testing whether I check evidence") and starts performing for the rubric.

**Solution:** This is partly unavoidable, but the damage is limited:
- The rubric has **four indicators** — a player optimising for one (e.g., always checking data) will inevitably trade off against another (e.g., decision quality suffers from over-analysis)
- Free-form responses are harder to fake convincingly at the speed of a 3-minute game than clicking the "correct" multiple-choice option
- The Quick Skill Profile data still grounds the report — even if the game is partially gamed, the self-reported vs. observed gap remains informative

---

### Problem 4 — Token Cost at Scale

**Risk:** Each user makes multiple free-text LLM calls. At volume, this becomes expensive.

**Solution:**
- **Cap input length** client-side (e.g., 500 characters per round) — this bounds the token count per call
- **Batch evaluation** where possible: evaluate Round 1 and Round 3 (both free-text rounds) together in a single LLM call after Round 4 completes, rather than calling after each round
- Rounds 2 and 4 are **event-logged** (accept/reject/check data), not LLM-evaluated — only free-text rounds require an LLM call
- For MVP: 1–2 LLM calls per full game session is acceptable

---

### Problem 5 — Player Anxiety About Free Text

**Risk:** Some players freeze when faced with a blank text box, especially in a high-stakes-feeling simulation. "I don't know what to write."

**Solution:** UI framing matters more than the input format:
- Label the field: *"What's your first instinct? There's no wrong answer — just tell us what you'd do."*
- Show a character count, not a word limit
- Display 1–2 example sentence starters that are **domain-neutral** and don't hint at scoring criteria (e.g., *"I'd focus on..." / "My first step would be..."*)
- Time pressure (the crisis framing itself) actually helps here — players in a crisis mindset write faster and more naturally than players who feel they're being assessed

---

### Problem 6 — Multilingual Input

**Risk:** Players write in their native language (Bahasa, Tagalog, etc.), breaking the evaluation LLM if it expects English.

**Solution:** Modern LLMs (GPT-4o, Gemini 1.5) handle multilingual input natively. The structured JSON output schema is language-agnostic — the LLM evaluates meaning, not language. For MVP, no additional translation layer is needed. The `evidence` field in the JSON may be in the player's language; that's acceptable since it is only stored, not displayed.

---

## UI / UX Options for the Simulation Arena

Three interface styles are viable for the crisis simulation screen. All use the same backend logic:

| Style | Description | Best for |
|---|---|---|
| **Swipe Cards** *(Reigns-style)* | Player reads a crisis card, swipes right to agree/execute or left to reject/override | Fast mobile MVP |
| **Chat Terminal** *(Hacknet / AI Copilot-style)* | Text-based interaction; player types instructions to an AI assistant that sometimes makes deliberate errors | Developer-friendly, strong immersion |
| **Dashboard Manager** *(Strategy sim-style)* | Player has sliders for budget, time, and AI allocation; must keep multiple metrics balanced | Most data-visible; closest to a real ops context |

---

## Definition of Done

The MVP is complete when a user can:

1. Start from an empty profile (no login, no CV)
2. Complete a Quick Skill Profile in under 2 minutes
3. Choose a mission and complete all four rounds
4. See an evidence-based skill report with behavioural observations and explicit limitations
5. Receive three role recommendations with explained reasoning, skill matches, and gaps
6. Compare two AI adoption scenarios
7. Get a sequential reskilling path with time estimates, real sources, and SDG mapping

**The most important demo proof point:** Changing the trend data source must visibly change the role recommendations. This proves FutureProof is not just a game with a generic AI dashboard bolted on.
