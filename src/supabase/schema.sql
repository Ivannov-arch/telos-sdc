-- ============================================================
-- SDC XMUM Hackathon — Domain 1: Aiversecity
-- Supabase Database Schema
-- Schema: telos_sdc (NOT public)
-- Owner: Person A (Backend Lead)
-- Last Updated: Day 1
-- ============================================================

-- Enable pgvector extension (must be done in public schema, then used anywhere)
CREATE EXTENSION IF NOT EXISTS vector;

-- Create dedicated schema
CREATE SCHEMA IF NOT EXISTS telos_sdc;

-- Set default search path for this session
SET search_path TO telos_sdc, public;

-- ============================================================
-- PHASE 1 — ESCO TAXONOMY
-- Substep 1.1 | Owner: Person A
-- Unblocks: Person B (1.3), Person C (5.2), Person D (4.1)
-- ============================================================

-- ESCO Skills
-- Source: https://esco.ec.europa.eu/en/use-esco/download
CREATE TABLE telos_sdc.skills (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    esco_id         TEXT NOT NULL UNIQUE,          -- e.g. "http://data.europa.eu/esco/skill/S1.1.0"
    preferred_label TEXT NOT NULL,                 -- canonical English label
    alt_labels      TEXT[],                        -- synonyms / alternate labels
    skill_type      TEXT NOT NULL                  -- 'skill/competence' | 'knowledge' | 'attitude'
                    CHECK (skill_type IN ('skill/competence', 'knowledge', 'attitude')),
    description     TEXT,
    broader_skill_id TEXT,                         -- parent esco_id for hierarchy
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_skills_esco_id        ON telos_sdc.skills (esco_id);
CREATE INDEX idx_skills_preferred_label ON telos_sdc.skills USING gin (to_tsvector('english', preferred_label));

-- --------------------------------------------------------

-- ESCO Occupations
CREATE TABLE telos_sdc.occupations (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    esco_id          TEXT NOT NULL UNIQUE,          -- e.g. "http://data.europa.eu/esco/occupation/O1.2"
    preferred_label  TEXT NOT NULL,
    alt_labels       TEXT[],
    description      TEXT,
    isco_group       TEXT,                          -- ISCO-08 group code
    -- O*NET enrichment (added in Day 2 — Substep 3.1)
    onet_soc_code    TEXT,                          -- e.g. "15-1211.00"
    tasks            TEXT[],                        -- O*NET Tasks.txt
    work_activities  TEXT[],                        -- O*NET Work Activities.txt
    knowledge_areas  TEXT[],                        -- O*NET Knowledge.txt
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_occupations_esco_id  ON telos_sdc.occupations (esco_id);
CREATE INDEX idx_occupations_onet_soc ON telos_sdc.occupations (onet_soc_code);

-- --------------------------------------------------------

-- MASCO 2020 Crosswalk
-- Source: Department of Statistics Malaysia (DOSM)
-- Maps Malaysian occupational codes -> O*NET SOC -> ESCO IDs
CREATE TABLE telos_sdc.masco_crosswalk (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    masco_code      TEXT NOT NULL UNIQUE,     -- 6-digit MASCO 2020 unit group code
    masco_label     TEXT NOT NULL,
    isco_code       TEXT,                     -- ISCO-08 4-digit code
    onet_soc_code   TEXT,                     -- O*NET-SOC code
    esco_id         TEXT REFERENCES telos_sdc.occupations(esco_id) ON DELETE SET NULL,
    mapped_manually BOOLEAN DEFAULT FALSE,    -- TRUE if auto-mapping was incomplete
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_masco_onet ON telos_sdc.masco_crosswalk (onet_soc_code);
CREATE INDEX idx_masco_esco ON telos_sdc.masco_crosswalk (esco_id);

-- --------------------------------------------------------

-- Role Required Skills (ESCO occupation <-> skill relation)
-- Substep 3.1 | Populated after ESCO + O*NET enrichment
CREATE TABLE telos_sdc.role_required_skills (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    role_id      TEXT NOT NULL REFERENCES telos_sdc.occupations(esco_id) ON DELETE CASCADE,
    skill_id     TEXT NOT NULL REFERENCES telos_sdc.skills(esco_id) ON DELETE CASCADE,
    is_essential BOOLEAN NOT NULL DEFAULT TRUE,     -- TRUE = Core Gap if missing
    weight       FLOAT NOT NULL DEFAULT 1.0         -- relative importance weight
                 CHECK (weight > 0),
    UNIQUE (role_id, skill_id)
);

CREATE INDEX idx_rrs_role_id  ON telos_sdc.role_required_skills (role_id);
CREATE INDEX idx_rrs_skill_id ON telos_sdc.role_required_skills (skill_id);

-- ============================================================
-- PHASE 1 — USER PROFILES
-- Substep 1.3-1.5 | Owner: Person B (writes), Person A (reads)
-- ============================================================

-- User Profiles
-- Populated by Person B's pdfplumber + Pydantic pipeline
CREATE TABLE telos_sdc.user_profiles (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    -- Structured output fields (Pydantic schema)
    hard_skills      JSONB NOT NULL DEFAULT '[]',
    -- e.g. [{"esco_id": "...", "label": "Python", "confidence_score": 0.95}]
    soft_skills      JSONB NOT NULL DEFAULT '[]',
    experience_years INT NOT NULL DEFAULT 0,
    -- Raw source
    raw_cv_text      TEXT,
    source_type      TEXT NOT NULL DEFAULT 'form'
                     CHECK (source_type IN ('pdf', 'form')),
    is_synthetic     BOOLEAN NOT NULL DEFAULT FALSE,
    -- Embedding vectors (populated by Person B Substep 1.4)
    -- Waits for: Person B RunPod BGE-M3 /embed endpoint
    user_dense_vector  vector(1024),               -- BGE-M3 dense output (1024-dim)
    user_sparse_vector sparsevec(30000),            -- BGE-M3 SPLADE sparse output
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_user_profiles_dense  ON telos_sdc.user_profiles
    USING hnsw (user_dense_vector vector_cosine_ops);
CREATE INDEX idx_user_profiles_sparse ON telos_sdc.user_profiles
    USING hnsw (user_sparse_vector sparsevec_ip_ops);

-- ============================================================
-- PHASE 1 — ROLE VECTORS
-- Substep 3.1 | Owner: Person A
-- Waits for: Person B RunPod BGE-M3 /embed live
-- ============================================================

CREATE TABLE telos_sdc.role_vectors (
    id                 UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    role_id            TEXT NOT NULL UNIQUE REFERENCES telos_sdc.occupations(esco_id) ON DELETE CASCADE,
    role_dense_vector  vector(1024),               -- BGE-M3 dense (cosine similarity)
    role_sparse_vector sparsevec(30000),            -- BGE-M3 SPLADE sparse (inner product)
    embedded_at        TIMESTAMPTZ,
    created_at         TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_role_vectors_dense  ON telos_sdc.role_vectors
    USING hnsw (role_dense_vector vector_cosine_ops);
CREATE INDEX idx_role_vectors_sparse ON telos_sdc.role_vectors
    USING hnsw (role_sparse_vector sparsevec_ip_ops);

-- ============================================================
-- PHASE 1 — FEATURE 3: RRF HYBRID SEARCH FUNCTION
-- Substep 3.2 | Owner: Person A
-- ============================================================

CREATE OR REPLACE FUNCTION telos_sdc.hybrid_search(
    query_dense  vector,
    query_sparse sparsevec,
    k            INT DEFAULT 10,
    rrf_k        INT DEFAULT 60
)
RETURNS TABLE(role_id TEXT, rrf_score FLOAT)
LANGUAGE sql STABLE AS $$
    WITH dense_rank AS (
        SELECT
            rv.role_id,
            ROW_NUMBER() OVER (ORDER BY rv.role_dense_vector <=> query_dense) AS rank
        FROM telos_sdc.role_vectors rv
        WHERE rv.role_dense_vector IS NOT NULL
    ),
    sparse_rank AS (
        SELECT
            rv.role_id,
            ROW_NUMBER() OVER (ORDER BY rv.role_sparse_vector <#> query_sparse) AS rank
        FROM telos_sdc.role_vectors rv
        WHERE rv.role_sparse_vector IS NOT NULL
    )
    SELECT
        COALESCE(d.role_id, s.role_id)                              AS role_id,
        COALESCE(1.0 / (rrf_k + d.rank), 0.0)
            + COALESCE(1.0 / (rrf_k + s.rank), 0.0)                AS rrf_score
    FROM dense_rank d
    FULL OUTER JOIN sparse_rank s ON d.role_id = s.role_id
    ORDER BY rrf_score DESC
    LIMIT k;
$$;

-- ============================================================
-- PHASE 1 — FEATURE 5: SDG MAPPING
-- Substep 5.1 | Owner: Person A (tables) + Person C (seed data)
-- ============================================================

-- UN SDG Goals (17 goals)
-- Source: GET /v1/sdg/Goal/List
CREATE TABLE telos_sdc.sdg_goals (
    id          SERIAL PRIMARY KEY,
    goal_code   INT NOT NULL UNIQUE CHECK (goal_code BETWEEN 1 AND 17),
    title       TEXT NOT NULL,
    description TEXT,
    color_hex   TEXT,              -- official UN SDG color per goal
    icon_url    TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- UN SDG Targets (per goal)
-- Source: GET /v1/sdg/Goal/{goalCode}/Target/List
CREATE TABLE telos_sdc.sdg_targets (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    goal_code    INT NOT NULL REFERENCES telos_sdc.sdg_goals(goal_code) ON DELETE CASCADE,
    target_code  TEXT NOT NULL UNIQUE,   -- e.g. "4.4", "8.2"
    title        TEXT NOT NULL,
    description  TEXT,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_sdg_targets_goal ON telos_sdc.sdg_targets (goal_code);

-- UN SDG Indicators
-- Source: GET /v1/sdg/Indicator/List
CREATE TABLE telos_sdc.sdg_indicators (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    target_code     TEXT NOT NULL REFERENCES telos_sdc.sdg_targets(target_code) ON DELETE CASCADE,
    indicator_code  TEXT NOT NULL UNIQUE,  -- e.g. "4.4.1"
    description     TEXT NOT NULL,
    tier            INT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Role -> SDG Curated Mapping
-- Substep 5.2: Seeded by Person C (human-curated, NOT LLM-generated)
-- Substep 5.3: JOINed by Person A into /api/match response
CREATE TABLE telos_sdc.role_sdg (
    id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    role_id           TEXT NOT NULL REFERENCES telos_sdc.occupations(esco_id) ON DELETE CASCADE,
    sdg_goal          INT NOT NULL REFERENCES telos_sdc.sdg_goals(goal_code),
    sdg_target        TEXT REFERENCES telos_sdc.sdg_targets(target_code),
    relationship_type TEXT NOT NULL
                      CHECK (relationship_type IN ('supports', 'enables', 'contributes')),
    impact_reasoning  TEXT NOT NULL,       -- 1 concise sentence, human-curated
    source            TEXT NOT NULL DEFAULT 'UNSD SDG API',
    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (role_id, sdg_goal, sdg_target)
);

CREATE INDEX idx_role_sdg_role ON telos_sdc.role_sdg (role_id);
CREATE INDEX idx_role_sdg_goal ON telos_sdc.role_sdg (sdg_goal);

-- ============================================================
-- PHASE 2 STUB — FEATURE 4: MICRO-TASK SIMULATION
-- Substep 4.1 | Owner: Person D (populates), Person A (schema)
-- ============================================================

CREATE TABLE telos_sdc.simulation_tasks (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    skill_id        TEXT NOT NULL REFERENCES telos_sdc.skills(esco_id) ON DELETE CASCADE,
    scenario_text   TEXT NOT NULL,
    rubric_criteria JSONB NOT NULL,
    -- e.g. ["bias detection", "escalation procedure", "audit trail"]
    difficulty      TEXT NOT NULL DEFAULT 'medium'
                    CHECK (difficulty IN ('easy', 'medium', 'hard')),
    onet_task_ref   TEXT,                  -- source O*NET task statement ID
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_sim_tasks_skill ON telos_sdc.simulation_tasks (skill_id);

-- Simulation Results (user responses + evaluator feedback)
CREATE TABLE telos_sdc.simulation_results (
    id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id               UUID NOT NULL REFERENCES telos_sdc.user_profiles(id) ON DELETE CASCADE,
    task_id               UUID NOT NULL REFERENCES telos_sdc.simulation_tasks(id),
    user_response         TEXT NOT NULL,
    -- LLM evaluator output (Pydantic-validated)
    score_percent         INT CHECK (score_percent BETWEEN 0 AND 100),
    improvement_reasoning TEXT,
    missing_concepts      TEXT[],
    evaluated_at          TIMESTAMPTZ,
    created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================
-- PHASE 3 STUB — FEATURE 2: AI EXPOSURE (CTCI)
-- Substep 2.1 | Owner: Person E (populates), Person A (schema)
-- ============================================================

CREATE TABLE telos_sdc.occupation_ai_exposure (
    id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    onet_soc_code         TEXT NOT NULL UNIQUE,
    -- Raw academic indices
    aioe_score            FLOAT,
    gpts_score            FLOAT,
    webb_score            FLOAT,
    -- Derived CTCI: (0.5 * webb) + (0.25 * aioe) + (0.25 * gpts)
    ctci_score            FLOAT,
    reasoning_intensity   FLOAT,            -- from O*NET Abilities.txt
    compression_type      TEXT
                          CHECK (compression_type IN ('substitutive', 'complementary')),
    compression_reasoning TEXT,
    created_at            TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_ai_exposure_onet ON telos_sdc.occupation_ai_exposure (onet_soc_code);

-- Malaysian Job Market Signal
-- Source: OpenDOSM Job Market Insights
CREATE TABLE telos_sdc.occupation_my_signal (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    masco_code    TEXT NOT NULL,
    onet_soc_code TEXT,
    vacancy_count INT,
    period        TEXT NOT NULL,           -- e.g. "Q3 2025"
    state         TEXT,                    -- NULL = national
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (masco_code, period, state)
);

-- ============================================================
-- PHASE 3 STUB — FEATURE 6: DISRUPTION PENALTY MATRIX
-- Substep 6.1 | Owner: Person E (populates), Person A (schema)
-- ============================================================

CREATE TABLE telos_sdc.occupation_disruption_matrix (
    id                          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    onet_soc_code               TEXT NOT NULL UNIQUE,
    routine_cognitive_ratio     FLOAT NOT NULL DEFAULT 0.0
                                CHECK (routine_cognitive_ratio BETWEEN 0 AND 1),
    -- disruption_penalty_fast     = routine_cognitive_ratio * ctci (normalized)
    -- disruption_penalty_moderate = disruption_penalty_fast * 0.4
    disruption_penalty_fast     FLOAT NOT NULL DEFAULT 0.0
                                CHECK (disruption_penalty_fast BETWEEN 0 AND 1),
    disruption_penalty_moderate FLOAT NOT NULL DEFAULT 0.0
                                CHECK (disruption_penalty_moderate BETWEEN 0 AND 1),
    soft_skill_intensity        FLOAT NOT NULL DEFAULT 0.0
                                CHECK (soft_skill_intensity BETWEEN 0 AND 1),
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================
-- ROW LEVEL SECURITY (RLS)
-- service_role = FastAPI backend (full access)
-- anon         = read-only on taxonomy/reference tables only
-- ============================================================

ALTER TABLE telos_sdc.skills                       ENABLE ROW LEVEL SECURITY;
ALTER TABLE telos_sdc.occupations                  ENABLE ROW LEVEL SECURITY;
ALTER TABLE telos_sdc.masco_crosswalk              ENABLE ROW LEVEL SECURITY;
ALTER TABLE telos_sdc.role_required_skills         ENABLE ROW LEVEL SECURITY;
ALTER TABLE telos_sdc.user_profiles                ENABLE ROW LEVEL SECURITY;
ALTER TABLE telos_sdc.role_vectors                 ENABLE ROW LEVEL SECURITY;
ALTER TABLE telos_sdc.sdg_goals                    ENABLE ROW LEVEL SECURITY;
ALTER TABLE telos_sdc.sdg_targets                  ENABLE ROW LEVEL SECURITY;
ALTER TABLE telos_sdc.sdg_indicators               ENABLE ROW LEVEL SECURITY;
ALTER TABLE telos_sdc.role_sdg                     ENABLE ROW LEVEL SECURITY;
ALTER TABLE telos_sdc.simulation_tasks             ENABLE ROW LEVEL SECURITY;
ALTER TABLE telos_sdc.simulation_results           ENABLE ROW LEVEL SECURITY;
ALTER TABLE telos_sdc.occupation_ai_exposure       ENABLE ROW LEVEL SECURITY;
ALTER TABLE telos_sdc.occupation_my_signal         ENABLE ROW LEVEL SECURITY;
ALTER TABLE telos_sdc.occupation_disruption_matrix ENABLE ROW LEVEL SECURITY;

-- service_role: bypass everything
CREATE POLICY "service_role_all" ON telos_sdc.skills
    FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all" ON telos_sdc.occupations
    FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all" ON telos_sdc.masco_crosswalk
    FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all" ON telos_sdc.role_required_skills
    FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all" ON telos_sdc.user_profiles
    FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all" ON telos_sdc.role_vectors
    FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all" ON telos_sdc.sdg_goals
    FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all" ON telos_sdc.sdg_targets
    FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all" ON telos_sdc.sdg_indicators
    FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all" ON telos_sdc.role_sdg
    FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all" ON telos_sdc.simulation_tasks
    FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all" ON telos_sdc.simulation_results
    FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all" ON telos_sdc.occupation_ai_exposure
    FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all" ON telos_sdc.occupation_my_signal
    FOR ALL TO service_role USING (true) WITH CHECK (true);
CREATE POLICY "service_role_all" ON telos_sdc.occupation_disruption_matrix
    FOR ALL TO service_role USING (true) WITH CHECK (true);

-- anon: read-only on reference/taxonomy tables
CREATE POLICY "anon_read" ON telos_sdc.skills         FOR SELECT TO anon USING (true);
CREATE POLICY "anon_read" ON telos_sdc.occupations     FOR SELECT TO anon USING (true);
CREATE POLICY "anon_read" ON telos_sdc.sdg_goals       FOR SELECT TO anon USING (true);
CREATE POLICY "anon_read" ON telos_sdc.sdg_targets     FOR SELECT TO anon USING (true);
CREATE POLICY "anon_read" ON telos_sdc.sdg_indicators  FOR SELECT TO anon USING (true);
CREATE POLICY "anon_read" ON telos_sdc.simulation_tasks FOR SELECT TO anon USING (true);

-- ============================================================
-- GRANT USAGE ON SCHEMA
-- ============================================================

GRANT USAGE ON SCHEMA telos_sdc TO anon, authenticated, service_role;
GRANT ALL   ON ALL TABLES    IN SCHEMA telos_sdc TO service_role;
GRANT ALL   ON ALL SEQUENCES IN SCHEMA telos_sdc TO service_role;
GRANT ALL   ON ALL FUNCTIONS IN SCHEMA telos_sdc TO service_role;
GRANT SELECT ON ALL TABLES   IN SCHEMA telos_sdc TO anon, authenticated;
