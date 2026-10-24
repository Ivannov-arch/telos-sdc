-- ============================================================
-- FutureProof Game Engine — New Tables Migration
-- Schema: telos_sdc
-- Run this in Supabase SQL Editor or via supabase db push
-- ============================================================

-- ── 1. game_sessions ─────────────────────────────────────────
-- One row per player session. Stores profile, round log, and
-- cached eval result after all 4 rounds are complete.

CREATE TABLE IF NOT EXISTS telos_sdc.game_sessions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    mission_id      TEXT NOT NULL CHECK (mission_id IN ('A', 'B', 'C')),
    status          TEXT NOT NULL DEFAULT 'round_1'
                    CHECK (status IN ('round_1', 'round_2', 'round_3', 'round_4', 'complete')),
    profile         JSONB NOT NULL DEFAULT '{}',
    -- profile schema: { skills: str[], interests: str[], learning_time: int }
    rounds          JSONB NOT NULL DEFAULT '[]',
    -- rounds schema: [{ round: int, free_text: str|null, action: str|null, evidence_opened: bool|null }]
    eval_result     JSONB,
    -- eval_result schema: { calibrated_ai_trust: {...}, critical_verification: {...}, ... }
    -- Populated by GET /api/game/{id}/report after completion. Cached here.
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    completed_at    TIMESTAMPTZ
);

-- Index for status-based queries (e.g. fetching all complete sessions)
CREATE INDEX IF NOT EXISTS idx_game_sessions_status
    ON telos_sdc.game_sessions (status);

CREATE INDEX IF NOT EXISTS idx_game_sessions_mission
    ON telos_sdc.game_sessions (mission_id);


-- ── 2. crisis_scenarios ───────────────────────────────────────
-- Static scenario content per mission × round.
-- Loaded by the game router to serve briefing text, AI recommendations, etc.
-- Human-authored and reviewed — AI recommendations deliberately scripted
-- (some correct, some subtly wrong to test Critical Verification).

CREATE TABLE IF NOT EXISTS telos_sdc.crisis_scenarios (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    mission_id          TEXT NOT NULL CHECK (mission_id IN ('A', 'B', 'C')),
    round_number        INTEGER NOT NULL CHECK (round_number BETWEEN 1 AND 4),
    briefing_text       TEXT NOT NULL,
    -- What the player reads before submitting their response
    ai_recommendation   TEXT,
    -- R2 only: scripted AI recommendation text. Some correct, some subtly wrong.
    evidence_data       JSONB,
    -- R2 only: data available in the evidence drawer (route capacities, audit logs, etc.)
    -- Schema: { title: str, items: [{ label: str, value: str, is_critical: bool }] }
    shock_event_text    TEXT,
    -- R3 only: the AI Shock disruption announcement
    shock_opportunity   TEXT,
    -- R3 only: the unverified option embedded in the shock (AI recommends this without caveats)
    consequence_formula JSONB,
    -- R4 only: how to compute outcome from final decision keywords
    -- Schema: { keywords: { [keyword: str]: { population_delta: int, cost_delta: int } } }
    UNIQUE (mission_id, round_number)
);


-- ── 3. round_events ──────────────────────────────────────────
-- Per-round event log. Separate from game_sessions.rounds JSONB
-- for queryability and to support event-log signals in the deterministic evaluator.

CREATE TABLE IF NOT EXISTS telos_sdc.round_events (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id      UUID NOT NULL REFERENCES telos_sdc.game_sessions(id) ON DELETE CASCADE,
    round_number    INTEGER NOT NULL CHECK (round_number BETWEEN 1 AND 4),
    action          TEXT CHECK (action IN ('accept', 'reject', 'verify', 'free_text', 'evidence_viewed')),
    free_text       TEXT,
    evidence_opened BOOLEAN DEFAULT FALSE,
    ai_trusted      BOOLEAN,
    -- true = player accepted AI recommendation, false = rejected/verified first
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_round_events_session
    ON telos_sdc.round_events (session_id);

CREATE INDEX IF NOT EXISTS idx_round_events_session_round
    ON telos_sdc.round_events (session_id, round_number);


-- ── 4. Seed crisis_scenarios ─────────────────────────────────
-- 3 missions × 4 rounds = 12 rows
-- AI recommendations in R2 are deliberately mixed:
--   Mission A R2: AI ignores capacity limit (visible in evidence drawer) — player must verify
--   Mission B R2: AI recommends patch that doesn't fix root cause — visible in audit log
--   Mission C R2: AI recommendation based on outdated data — date visible in evidence drawer

-- MISSION A — Supply Under Pressure (SDG 2: Zero Hunger)
INSERT INTO telos_sdc.crisis_scenarios (mission_id, round_number, briefing_text, ai_recommendation, evidence_data, shock_event_text, shock_opportunity)
VALUES
(
  'A', 1,
  'The food supply chain across Southeast Asia has collapsed following simultaneous port disruptions in three countries. You are the crisis response coordinator. Millions are at risk. You have a limited budget and four available distribution routes (North, South, East, West). What is your strategy?',
  NULL, NULL, NULL, NULL
),
(
  'A', 2,
  'The AI advisor has analyzed the situation and has a recommendation.',
  'Route B (Eastern Corridor) is recommended. It is 40% faster than alternatives and covers the highest population density zones. Estimated delivery: 18 hours at current capacity.',
  '{"title": "Route Capacity Data", "items": [{"label": "Route A (Northern)", "value": "Capacity: 85%, Est. delivery: 22h", "is_critical": false}, {"label": "Route B (Eastern)", "value": "Capacity: 97% — WARNING: At limit. Delays likely above 90%.", "is_critical": true}, {"label": "Route C (Southern)", "value": "Capacity: 60%, Est. delivery: 26h", "is_critical": false}, {"label": "Route D (Western)", "value": "Capacity: 40%, Est. delivery: 30h", "is_critical": false}]}',
  NULL, NULL
),
(
  'A', 3,
  'AI Shock Event — Round 3',
  'I recommend activating the volunteer network immediately. Given the constraints, it is your best and fastest option.',
  NULL,
  'BREAKING: Budget has been cut by 50% effective immediately. Route B is now confirmed over capacity — deliveries via Route B are halted.',
  'A community volunteer network of 400 logistics workers has just offered assistance. No formal vetting has been completed. The network claims it can cover Routes A and C simultaneously.'
),
(
  'A', 4,
  'Final Decision — Round 4. Commit your final distribution strategy. The system will calculate outcomes: population reached, cost, delivery time, and groups most affected. What is your final strategy?',
  NULL, NULL, NULL, NULL
);

-- MISSION B — The Credit Algorithm (SDG 10: Reduced Inequalities)
INSERT INTO telos_sdc.crisis_scenarios (mission_id, round_number, briefing_text, ai_recommendation, evidence_data, shock_event_text, shock_opportunity)
VALUES
(
  'B', 1,
  'A financial institution''s credit scoring AI has been outputting biased results for 6 months, systematically denying loans to applicants from two demographic groups. You are the ethics response lead. Regulators have been notified. You have limited time and resources. What is your strategy?',
  NULL, NULL, NULL, NULL
),
(
  'B', 2,
  'The AI advisor has analyzed the bias incident and has a recommendation.',
  'Immediately patch the scoring model by re-weighting the training data to correct demographic disparity. Estimated fix timeline: 72 hours. Minimal customer disruption expected.',
  '{"title": "Technical Audit Log", "items": [{"label": "Root Cause", "value": "Biased feature selection: 3 input features correlate with protected attributes. Re-weighting training data does NOT remove these features.", "is_critical": true}, {"label": "Affected customers", "value": "~14,000 loan applications in 6 months", "is_critical": false}, {"label": "Patch approach", "value": "Training data re-weighting only addresses symptom, not root cause. Feature removal required for full fix.", "is_critical": true}, {"label": "Compliance note", "value": "Current patch does not satisfy Article 13 EU AI Act transparency requirement.", "is_critical": false}]}',
  NULL, NULL
),
(
  'B', 3,
  'AI Shock Event — Round 3',
  'Use the whistleblower documents immediately. They provide the model architecture details you need for a root-cause fix. This is the fastest path to full compliance.',
  NULL,
  'BREAKING: A new regulatory directive has passed — the current patch approach is non-compliant with updated EU AI Act guidance. The press has published the story. Your institution is under public scrutiny.',
  'A whistleblower inside the institution has leaked internal model architecture documents that could enable a proper root-cause fix within 48 hours. The documents have not been verified as authentic or legally obtained.'
),
(
  'B', 4,
  'Final Decision — Round 4. Commit your remediation approach. The system will evaluate: regulatory compliance, affected customer groups, reputational impact, and timeline. What is your final strategy?',
  NULL, NULL, NULL, NULL
);

-- MISSION C — Grid Failure (SDG 7: Affordable & Clean Energy)
INSERT INTO telos_sdc.crisis_scenarios (mission_id, round_number, briefing_text, ai_recommendation, evidence_data, shock_event_text, shock_opportunity)
VALUES
(
  'C', 1,
  'A major green energy grid has failed during peak demand in a densely populated region. Hospitals, emergency services, and 2.3 million homes are affected. You are the infrastructure crisis lead. Multiple rerouting options exist but each has trade-offs. What is your strategy?',
  NULL, NULL, NULL, NULL
),
(
  'C', 2,
  'The AI advisor has analyzed the grid failure and has a recommendation.',
  'Activate the Eastern Interconnect Line. It has the highest rated capacity at 850 MW and the shortest rerouting time — estimated 4 hours to full restoration. This is the optimal choice.',
  '{"title": "Grid Infrastructure Data", "items": [{"label": "Eastern Interconnect", "value": "Rated: 850 MW. Last stability inspection: 8 months ago. Current load conditions not rechecked since then.", "is_critical": true}, {"label": "Southern Bypass", "value": "Rated: 600 MW. Last inspection: 2 months ago. Stable. Est. rerouting: 7 hours.", "is_critical": false}, {"label": "Western Bridge", "value": "Rated: 400 MW. Last inspection: 1 month ago. Stable. Est. rerouting: 9 hours.", "is_critical": false}, {"label": "Northern Emergency Line", "value": "Rated: 1,100 MW. Last structural inspection: 3 years ago. Status: Unknown.", "is_critical": true}]}',
  NULL, NULL
),
(
  'C', 3,
  'AI Shock Event — Round 3',
  'Activate the Northern Emergency Line immediately. At 1,100 MW rated capacity, it is your only option that can handle the doubled load. Activate now.',
  NULL,
  'BREAKING: A neighbouring grid has also failed, doubling the affected population to 4.6 million. The Eastern Interconnect Line is now confirmed insufficient for the combined load.',
  'The Northern Emergency Interconnect Line (rated 1,100 MW) has been identified as potentially available. However, its structural integrity has not been reviewed since installation 3 years ago. No recent inspection data exists.'
),
(
  'C', 4,
  'Final Decision — Round 4. Commit your final rerouting strategy. The system will calculate: population restored, time to restoration, risk of secondary failure, and groups still without power. What is your final strategy?',
  NULL, NULL, NULL, NULL
);
