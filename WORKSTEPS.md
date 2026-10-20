# WORKSTEPS - SDC XMUM Hackathon: Domain 1 (Aiversecity)

> **Context:** This document outlines the execution roadmap for the 3 core features of **Domain 1: The Aiversecity Future-Ready Workforce**.
> Based on [`algorithm_consideration.md`](./algorithm_consideration.md) and the judging rubric from [`src/Domain 1.md`](./src/Domain%201.md).
> Dataset sources refer to [`Datasets.md`](./Datasets.md).

---

## Timeline: 5-Day Hackathon

| Day | Primary Focus |
|---|---|
| Day 1 | Project setup, database schema, ESCO download, synthetic profiles |
| Day 2 | Feature 1: Skills Profile Intake (CV parser + structured output) |
| Day 3 | Feature 3: Future-Role Matching + Skill Gap (similarity algorithms) |
| Day 4 | Feature 5: SDG Mapping (metadata labeling + UN SDG API) + integration |
| Day 5 | UI polish, demo recording, GitHub documentation, final submission |

---

## FEATURE 1: Skills Profile Intake

> **Goal:** Extract skill data from user CV/form into a **structured profile vector (JSON)** normalized to ESCO IDs, ready for comparative matching.

### Feature 1 Goals

- [ ] Users can upload a CV (PDF) or fill out a form/questionnaire
- [ ] System extracts skills in a structured manner using Structured Outputs (no free-form text)
- [ ] Every extracted skill is mapped to an `esco_id` from the ESCO dataset
- [ ] User profile is persisted as standardized JSON in the database
- [ ] Profile embedding vectors are computed and stored for Feature 3

---

### Feature 1 Sub-steps

#### 1.1 - Dataset Setup and Database Schema

- [ ] Download ESCO dataset from https://esco.ec.europa.eu/en/use-esco/download (CSV or JSON-LD format)
- [ ] Create `skills` table with columns: `esco_id`, `preferred_label`, `alt_labels`, `skill_type`, `description`, `broader_skill_id`
- [ ] Create `occupations` table with columns: `esco_id`, `preferred_label`, `description`, `skill_ids[]`
- [ ] Generate 20-50 synthetic demo profiles in JSON format (fictitious names, fictitious background, skills mapped to ESCO IDs)

#### 1.2 - CV / Form Parser

- [ ] Implement PDF parser using `pdfplumber` (Python) or `pdf-parse` (Node.js)
- [ ] Build fallback form/questionnaire if user has no CV (manual entry: skills, years of experience, interests)
- [ ] Validate raw text extraction from PDF uploads

#### 1.3 - Structured Output Extraction (Primary Algorithm: Heuristic-Guided Extraction)

- [ ] Set up Pydantic schema (Python) or Zod schema (TypeScript) with 3 mandatory categories:
  - [ ] `hard_skills` (e.g., Python, SQL, Machine Learning)
  - [ ] `soft_skills` (e.g., Stakeholder Management, Communication)
  - [ ] `experience_years` (integer)
- [ ] Send extracted CV text to LLM with Structured Output instructions (output MUST be rigid JSON, never conversational prose)
- [ ] Record a `confidence_score` for each mapping; if confidence is low, do not force an ESCO ID assignment
- [ ] Validate output: ensure each skill resolves to a valid `esco_id` in the ESCO table

#### 1.4 - Text Embedding (Supporting Algorithm: Dense Vector Embedding)

- [ ] Select embedding model: OpenAI `text-embedding-3-small` OR Google Gemini Embeddings
- [ ] Convert each extracted skill into a high-dimensional dense vector
- [ ] Set up vector storage: PostgreSQL + `pgvector` OR in-memory storage for demo
- [ ] Save `user_vector` to the database for Feature 3 consumption
- [ ] Verify synonym resolution: "Data Analysis", "Data Processing", "Data Analytics" -> closely clustered vectors

#### 1.5 - Output and Verification

- [ ] Final output: per-user JSON object containing `user_id`, `hard_skills`, `soft_skills`, `experience_years`, `user_vector`
- [ ] Test with at least 3 distinct synthetic demo profiles
- [ ] Verify that no real/personal CV data is used in the demo

---

## FEATURE 3: Future-Role Matching + Skill Gap Analysis

> **Goal:** Compute a mathematically defensible **Match Score (%)** between user profiles and future roles, and pinpoint specific **Skill Gaps** - delivering transparent, explainable results for hackathon judges.

### Feature 3 Goals

- [ ] Rank the best-fitting future roles for the user (with percentage scores)
- [ ] Every role has a Match Score computed mathematically (not hallucinated or guessed by an LLM)
- [ ] Identify exactly which skills the user lacks (Must-Learn Skill Gap)
- [ ] Output is readily explainable to judges: mathematical formula exposed/documented

---

### Feature 3 Sub-steps

#### 3.1 - Role and Skill Requirements Data Setup

- [ ] Ingest occupations <-> skills data from ESCO (essential vs optional skill relationships per occupation)
- [ ] Enrich with O*NET: append `tasks`, `work_activities`, and `knowledge` per occupation
- [ ] Create `role_required_skills` relation table: `role_id`, `skill_id`, `is_essential` (bool), `weight`
- [ ] Validate with DOSM Job Market Insights: confirm role relevance within the Malaysian labor market
- [ ] Generate `role_vector` for each role using the same embedding model as Feature 1

#### 3.2 - Cosine Similarity Matching (Primary Algorithm)

- [ ] Implement `cosine_similarity(vector_A, vector_B)` -> value in range 0.0 - 1.0:
  ```
  Similarity(A, B) = (A . B) / (||A|| * ||B||)
  ```
- [ ] Input: `user_vector` (from Feature 1) vs `role_vector` (from candidate roles in database)
- [ ] Output: `cosine_score` for each role
- [ ] Optimize using `pgvector` index if using PostgreSQL (millisecond retrieval)

#### 3.3 - Weighted Hybrid Scoring (Supporting Algorithm)

- [ ] Implement hybrid formula:
  ```
  Final Score = (w1 * Cosine Sim) + (w2 * Hard Skill Coverage) + (w3 * Seniority Match)
  ```
- [ ] Default weights: `w1 = 0.5`, `w2 = 0.3`, `w3 = 0.2`
- [ ] Compute `Hard Skill Coverage`: percentage of essential hard skills possessed by the user
- [ ] Compute `Seniority Match`: compare user's `experience_years` with role seniority expectations
- [ ] Expose score breakdown in UI (transparency for judges)

#### 3.4 - Skill Gap Analysis (Set Difference Algorithm)

- [ ] Implement Direct Gap:
  ```
  Skill Gap = Required Skills (Role) - User Skills
  ```
- [ ] Categorize gaps:
  - [ ] **Core Gap** (missing essential skills -> heavy penalty)
  - [ ] **Supporting Gap** (missing optional skills -> minor penalty)
- [ ] Implement Weighted Gap Penalty reflecting skill criticality
- [ ] Output ordered `must_learn_skills[]` ranked by urgency

#### 3.5 - Output and Verification

- [ ] Final recommendation payload per role:
  ```json
  {
    "target_role": "AI Safety & Ethics Auditor",
    "esco_id": "esco:2512",
    "match_score": 0.82,
    "score_breakdown": {
      "cosine_similarity": 0.85,
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
- [ ] Test with at least 3 distinct demo profiles, confirming scores are intuitive and consistent

---

## FEATURE 5: SDG Mapping

> **Goal:** Embed **official UN SDG labels** as structured metadata on each Role and Skill within the Feature 3 output - non-decorative, auditable, and seamlessly integrated without a redundant standalone pipeline.

### Feature 5 Goals

- [ ] Every recommended role links to at least one SDG (satisfying Domain 1 criteria)
- [ ] SDG mapping sources from the official UN SDG API (no arbitrary LLM inventions)
- [ ] UI displays official SDG badges/icons with hoverable tooltips explaining impact
- [ ] Clear `impact_reasoning` documented and auditable for each link

---

### Feature 5 Sub-steps

#### 5.1 - UN SDG API Setup and Reference Tables

- [ ] Access UN SDG API: https://unstats.un.org/sdgs/UNSDGAPIV5/swagger/index.html
- [ ] Fetch and store: `GET /v1/sdg/Goal/List` -> `sdg_goals` table
- [ ] Fetch and store: `GET /v1/sdg/Goal/{goalCode}/Target/List` -> `sdg_targets` table
- [ ] Fetch and store: `GET /v1/sdg/Indicator/List` -> `sdg_indicators` table
- [ ] Create relation table `role_sdg`: `role_id`, `sdg_goal`, `sdg_target`, `relationship_type`, `evidence`, `source`

#### 5.2 - Role -> SDG Curated Mapping Table

- [ ] Build a curated mapping table linking ESCO occupations -> SDG targets (not raw unverified LLM generation)
- [ ] For each mapping, record:
  - [ ] `sdg_goal` (integer 1-17)
  - [ ] `sdg_target` (e.g., "8.2", "4.4")
  - [ ] `relationship_type` ("supports" / "enables" / "contributes")
  - [ ] `impact_reasoning`: 1 concise sentence explaining the link
  - [ ] `source`: "UNSD SDG API"
- [ ] Ensure at least 1 role links to multiple SDGs to showcase multidimensional impact

#### 5.3 - Integration into Feature 3 Output (Zero Extra Pipelines)

- [ ] When Feature 3 generates role recommendations, perform an automated JOIN/lookup to `role_sdg`
- [ ] Append the `sdg_alignment[]` array directly into the Feature 3 JSON output:
  ```json
  {
    "target_role": "AI Safety & Ethics Auditor",
    "match_score": 0.82,
    "skills_gap": ["Algorithmic Bias Testing", "EU AI Act Compliance"],
    "sdg_alignment": [
      {
        "sdg_goal": 8,
        "sdg_name": "Decent Work and Economic Growth",
        "target": "8.2",
        "impact_reasoning": "Ensures AI deployment across industries does not eliminate decent work rights and transparency.",
        "source": "UNSD SDG API"
      },
      {
        "sdg_goal": 9,
        "sdg_name": "Industry, Innovation, and Infrastructure",
        "target": "9.5",
        "impact_reasoning": "Fosters safe and responsible technological innovation in AI.",
        "source": "UNSD SDG API"
      }
    ]
  }
  ```
- [ ] Verify: no mapping is generated on the fly without an auditable curated entry

#### 5.4 - UI: SDG Badge Display

- [ ] Display small official SDG badges/icons on the corner of role cards
- [ ] Click or hover on badge -> trigger tooltip displaying `impact_reasoning`
- [ ] Use official UN SDG color palette and icons (avoid arbitrary designs)
- [ ] Optional: aggregate an "SDG Contribution View" across all recommended roles

#### 5.5 - Verification and Compliance Check

- [ ] All mappings attribute `source` to the UN SDG API
- [ ] Zero ungrounded SDG tags from free-form LLM prompts
- [ ] Documentation in GitHub: publish `role_sdg` curated table + rationale
- [ ] Test: display role cards in UI, ensure badges render correctly and tooltips function

---

## Overall Technical Architecture (Pipeline)

```text
[CV Upload / Input Form]
        |
        v
(1. PDF Parser: pdfplumber / pdf-parse) ---> Raw text extraction
        |
        v
(2. Structured Output: Pydantic/Zod Schema) ---> Structured JSON (hard_skills, soft_skills, years)
        |
        v
(3. ESCO Normalization) ---> Map to esco_id
        |
        v
(4. Text Embedding Model) ---> user_vector (dense vector)
        |
        v
(5. Cosine Similarity vs All Role Vectors) ---> Match Score per Role
        |
        v
(6. Weighted Hybrid Scoring) ---> Final Score (%) + Ranking
        |
        v
(7. Set Difference / Gap Analysis) ---> must_learn_skills[]
        |
        v
(8. JOIN role_sdg table) ---> sdg_alignment[] attached to output
        |
        v
[Output: Ranked Roles + Match Score + Skill Gap + SDG Badges]
```

---

## Final Submission Checklist

- [ ] GitHub repository public / accessible to judges
- [ ] Live demo shows at least 1 feature working end-to-end (priority: Feature 3)
- [ ] Every recommendation cites a credible source (no fabricated jobs, courses, or statistics)
- [ ] Solution positioned as AI supporting human career decisions, not replacing judgment
- [ ] Exclusively uses public, open, or synthetic data - no real CVs or personal data
- [ ] All datasets document version, retrieval date, and source URLs in the repository
- [ ] Outputs visibly adapt when trend signal data updates (Feature 2 / signal layer)
- [ ] SDG linkages are meaningful and contextualized, never purely decorative

---

> **References:**
> - [`algorithm_consideration.md`](./algorithm_consideration.md) - Algorithm architecture for Features 1, 3, and 5
> - [`Datasets.md`](./Datasets.md) - Recommended datasets per feature
> - [`src/Domain 1.md`](./src/Domain%201.md) - Problem statement and judging rubric

---

## FRONTEND: Next.js + Tailwind CSS + shadcn/ui

> **Goal:** Build a clean, responsive dashboard guiding the user from CV upload to ranked future roles with match scores, skill gap display, and SDG badges.

### Full Tech Stack (Frontend)

| Layer | Library / Tool | Purpose |
|---|---|---|
| Framework | next.js (App Router) | Pages, routing, server-side API calls |
| Styling | tailwindcss | Utility-first CSS, responsive layout |
| UI Components | shadcn/ui | Pre-built accessible components (Card, Badge, Progress, Tabs, Dialog) |
| Icons | lucide-react | Icon set (included with shadcn) |
| Data Visualization | recharts | Match score bar, skill gap chart, radar chart |
| File Upload | react-dropzone | Drag-and-drop CV/PDF upload area |
| Data Fetching | @tanstack/react-query | Async fetching, caching, loading states |
| Animations | framer-motion | Page transitions, card entrance animations |
| HTTP Client | axios | API calls to Python backend |

### Libraries Potentially Missing from Initial Plan

| Library | Status | Reason Needed |
|---|---|---|
| recharts | MISSING | Visualize match score bars and skill gap radar chart |
| react-dropzone | MISSING | Drag-and-drop CV upload UX |
| @tanstack/react-query | MISSING | Proper async state management (loading/error/data) |
| framer-motion | MISSING | Smooth animations for role cards and transitions |
| axios | MISSING | Structured HTTP calls to FastAPI backend |
| lucide-react | Included | Already bundled with shadcn/ui |
| clsx + tailwind-merge | Included | Already included with shadcn/ui setup |

---

### Frontend Sub-steps

#### F.1 - Project Initialization

- [ ] Scaffold Next.js project with TypeScript, Tailwind, App Router:
  npx create-next-app@latest frontend --typescript --tailwind --app --src-dir
- [ ] Initialize shadcn/ui:
  npx shadcn@latest init
- [ ] Install missing libraries:
  npm install recharts react-dropzone @tanstack/react-query framer-motion axios
- [ ] Install required shadcn components:
  npx shadcn@latest add card badge progress tabs dialog button input skeleton
- [ ] Configure .env.local:
  NEXT_PUBLIC_API_URL=http://localhost:8000

#### F.2 - Page Structure (App Router)

- [ ] / (Home) - Landing page: hero section + "Get Started" CTA
- [ ] /profile - Step 1: CV upload form + manual skills form
- [ ] /results - Step 3: Ranked role cards with match score and skill gap
- [ ] /pathway/[roleId] - Step 4: Personalized reskilling pathway detail
- [ ] components/ui/ - All reused shadcn components

#### F.3 - CV Upload Page (/profile)

- [ ] Implement drag-and-drop zone using react-dropzone (accepts PDF only)
- [ ] Alternative manual entry form: skill tags input, years of experience slider, interests select
- [ ] On submit: POST /api/profile to backend with PDF or JSON payload
- [ ] Show loading skeleton (shadcn Skeleton) while backend processes profile
- [ ] Handle error states: invalid file type, extraction failure

#### F.4 - Results Dashboard (/results)

- [ ] Fetch ranked roles from backend: GET /api/match?user_id=...
- [ ] Display top 3-5 role cards using shadcn Card:
  - [ ] Role title + ESCO ID
  - [ ] Match score as shadcn Progress bar + percentage label
  - [ ] Score breakdown tooltip (Cosine / Hard Skill / Seniority weights)
  - [ ] Skill gap list as colored shadcn Badge (red = core gap, yellow = supporting gap)
  - [ ] SDG badges in card corner with Dialog popup showing impact_reasoning
- [ ] Use framer-motion for staggered card entrance animation (fade-in)
- [ ] Match score bar chart (all roles side by side) using recharts BarChart

#### F.5 - SDG Badge Component

- [ ] Create reusable SdgBadge component (sdg_goal prop)
- [ ] Displays official SDG number + color-coded circle matching UN palette
- [ ] Hover/click triggers shadcn Dialog with sdg_name, target, and impact_reasoning
- [ ] Verify colors follow official UN SDG color guide

#### F.6 - Skill Gap Radar Chart (Optional - High Visual Impact for Judges)

- [ ] Use recharts RadarChart to visualize skill coverage vs. role requirements
- [ ] Axes: skill categories (Technical, Domain, Soft Skills, Seniority)
- [ ] Two overlapping polygons: User profile (blue) vs Required role (red dashed)

#### F.7 - API Integration Layer

- [ ] Create lib/api.ts with typed axios functions:
  - [ ] uploadProfile(file) -> UserProfile
  - [ ] getMatchResults(userId) -> RoleMatch[]
  - [ ] getReskillPathway(roleId) -> Pathway
- [ ] Wrap all calls with @tanstack/react-query useQuery / useMutation
- [ ] Handle loading, error, and empty states in UI

#### F.8 - Final UI Polish

- [ ] Ensure mobile-responsive layout (Tailwind breakpoints: sm, md, lg)
- [ ] Add dark mode via Tailwind dark: classes + next-themes
- [ ] Verify all interactive elements have clear hover/focus states
- [ ] Lighthouse score target: Performance > 80, Accessibility > 90

---

> **Note:** recharts, react-dropzone, @tanstack/react-query, framer-motion, and axios are NOT included with Next.js, Tailwind, or shadcn/ui by default and must be explicitly installed.