# SDC Hackathon — Technical Tools & Datasets Declaration

**Project:** Telos / Aiversecity (Domain 1: Future-Ready Workforce)  
**Reference Template:** [`2. SDC Hackathon_ Technical Tools Declaration Template.md`](file:///c:/Coding/Hackathons/SDC_XMUM/src/docs/2.%20SDC%20Hackathon_%20Technical%20Tools%20Declaration%20Template.md)

---

### Feature-by-Feature Mapping: AI Tools & Datasets (Where They Are Used)

| Feature | AI Tool / Model Used | Dataset(s) Used | Code Location / Component |
|---|---|---|---|
| **Feature 1: Skills Profile Intake** | • **BGE-M3** (Dense 1024-d + Sparse 30k-d vectors)<br>• **Llama-3-8B / Qwen** (Structured NER Extractor) | • **ESCO Skills & Competences** (`skills_en.csv`)<br>• **Synthetic Demo Profiles** (Fictitious JSON) | [seed_synthetic_profiles.py](file:///c:/Coding/Hackathons/SDC_XMUM/src/supabase/seed_synthetic_profiles.py)<br>[schema.sql: L105-128](file:///c:/Coding/Hackathons/SDC_XMUM/src/supabase/schema.sql#L105-L128) |
| **Feature 2: AI-Trend Signal Layer (CTCI)** | • **CTCI Formula & Reasoning Classifier** (Substitutive vs. Complementary Compression) | • **O\*NET Database** (`abilities.csv`, `work_activities.csv`)<br>• **AIOE / GPTs-are-GPTs / Webb Scores**<br>• **OpenDOSM Job Market Insights** | [schema.sql: L284-314](file:///c:/Coding/Hackathons/SDC_XMUM/src/supabase/schema.sql#L284-L314)<br>[DATASETS.md: L74-150](file:///c:/Coding/Hackathons/SDC_XMUM/src/docs/DATASETS.md#L74-L150) |
| **Feature 3: Future-Role Matching & Skill Gap** | • **BGE-M3** (Multi-modal retrieval)<br>• **RRF Hybrid Search** (Dense + Sparse in `pgvector`)<br>• **Set Difference Algorithm** ($T \setminus U$) | • **ESCO Occupations & Skills** (`occupations_en.csv`, `occupationSkillRelations_en.csv`)<br>• **MASCO 2020** (Malaysian standard crosswalk)<br>• **O\*NET Tasks** (`task_statements.csv`) | [match.py: L218-316](file:///c:/Coding/Hackathons/SDC_XMUM/src/backend/routers/match.py#L218-L316)<br>[schema.sql: L154-184](file:///c:/Coding/Hackathons/SDC_XMUM/src/supabase/schema.sql#L154-L184)<br>[enrich_onet.py](file:///c:/Coding/Hackathons/SDC_XMUM/src/supabase/enrich_onet.py) |
| **Feature 4: Personalised Reskilling Pathway** | • **Llama-3-8B / Qwen via vLLM + Instructor** (Rigid Rubric Evaluator) | • **O\*NET Task Statements** (`task_statements.csv`)<br>• **Curated Micro-Task Scenarios** (`simulation_tasks`) | [schema.sql: L251-277](file:///c:/Coding/Hackathons/SDC_XMUM/src/supabase/schema.sql#L251-L277)<br>[TASKS.md: L179-220](file:///c:/Coding/Hackathons/SDC_XMUM/src/docs/TASKS.md#L179-L220) |
| **Feature 5: SDG Mapping** | • *Deterministic Curated Rule Mapper* (Non-hallucinative keyword & taxonomy anchor) | • **UNSD SDG API v5** (Official 17 Goals, 169 Targets, Indicators)<br>• **Curated `role_sdg` Table** (2,054 verified mappings) | [seed_sdg.py](file:///c:/Coding/Hackathons/SDC_XMUM/src/supabase/seed_sdg.py)<br>[seed_role_sdg.py](file:///c:/Coding/Hackathons/SDC_XMUM/src/supabase/seed_role_sdg.py)<br>[match.py: L139-158](file:///c:/Coding/Hackathons/SDC_XMUM/src/backend/routers/match.py#L139-L158) |
| **Feature 6: Career Stress-Test Engine** | • **Deterministic Scenario Reweighting Matrix** (Disruption Penalty Engine) | • **O\*NET Cognitive Routine Ratio**<br>• **AIOE / Webb AI Exposure Penalties** | [schema.sql: L320-334](file:///c:/Coding/Hackathons/SDC_XMUM/src/supabase/schema.sql#L320-L334)<br>[match.py: L161-178](file:///c:/Coding/Hackathons/SDC_XMUM/src/backend/routers/match.py#L161-L178) |

---

## Technical Declaration (SDC Official Format)

### Section 2. ARCHITECTURE & TECHNOLOGY STACK

#### 2.1. System Architecture Overview
The Telos system connects an end-to-end workforce intelligence pipeline:
1. **Intake Layer:** User profiles (PDF CV or structured form) are ingested via FastAPI and parsed into validated Pydantic models containing ESCO skill IDs.
2. **Embedding & Retrieval Engine:** Profile skills and target ESCO occupations are transformed into dense (1024-d) and sparse (30,000-d) vectors via BGE-M3 hosted on RunPod vLLM. Supabase `pgvector` executes Reciprocal Rank Fusion (RRF) hybrid search.
3. **Scoring & Gap Analysis:** Matches are evaluated via a composite formula combining RRF semantic similarity (0.5), essential hard skill coverage (0.3), and seniority heuristics (0.2). Skill gaps are computed using strict set difference ($T \setminus U$).
4. **Enrichment & Simulation Layer:** Ranked roles are statically joined with UNSD SDG targets and O\*NET task statements. Personalised reskilling pathways present simulated micro-tasks evaluated by a local LLM under strict JSON rubrics.

#### 2.2. Languages, Frameworks & Libraries

| Name & Version | Purpose in Project | License |
| --- | --- | --- |
| **Python 3.11+** | Backend service logic, data ETL, and seeding pipelines | PSF License |
| **FastAPI 0.115+** | High-performance asynchronous REST API backend | MIT License |
| **Pydantic v2** | Data contract validation, schema enforcement, and JSON parsing | MIT License |
| **pdfplumber 0.11+** | Text and table extraction from multi-column CV PDFs | MIT License |
| **Supabase-py 2.10+** | Python client for Supabase database operations and RPC invocation | MIT License |
| **vLLM 0.6+** | High-throughput GPU inference engine for BGE-M3 embeddings & LLM evaluation | Apache 2.0 |
| **Next.js 14 / React 18** | Frontend user dashboard and interactive pathway visualization | MIT License |

---

### Section 3. APIs & CLOUD SERVICES

#### 3.1. External APIs

| API and Provider | Purpose in Project | Access Tier (free / paid / sponsor-provided) |
| --- | --- | --- |
| **UNSD SDG API v5** (United Nations Statistics Division) | Ingestion of official 17 Goals, 169 Targets, and global indicator descriptions | Free / Public |
| **RunPod Serverless / Pod API** (RunPod) | Hosting vLLM GPU inference containers for BGE-M3 embeddings (`/embed`) and simulation evaluation | Sponsor-provided ($25 credits) / Paid |

#### 3.2. Cloud Platforms & Deployment

| Service & Provider | Purpose in Project | Plan / Region |
| --- | --- | --- |
| **Supabase** (PostgreSQL + `pgvector`) | Relational database, dedicated `telos_sdc` schema, dense & sparse vector storage, HNSW indexing, RRF hybrid search function, and RLS security | Free Tier / Southeast Asia (Singapore) |
| **RunPod GPU Cloud** | Compute engine hosting NVIDIA A40 / RTX 4090 GPUs for real-time embedding generation | Community Cloud / Sponsor Credits |

---

### Section 4. AI TOOLS, MODELS & DATASETS

#### 4.1. AI Models Used in the Solution

| Model & Version | Source / Provider | Usage (pre-trained / fine-tuned / self-trained) | License / Terms |
| --- | --- | --- | --- |
| **BGE-M3** (`BAAI/bge-m3`) | Beijing Academy of Artificial Intelligence (BAAI) / Hugging Face | Pre-trained | MIT License |
| **Meta Llama 3 8B Instruct** (or **Qwen 2.5 7B Instruct**) | Meta AI / Alibaba Cloud (via Hugging Face & vLLM) | Pre-trained | Meta Llama 3 Community License / Apache 2.0 |

> **Implementation Details:**
> 1. **BGE-M3:** Deployed on RunPod GPU serverless via a standardized `/embed` endpoint. It outputs both 1024-dimensional dense vectors and 30,000-dimensional sparse vectors (SPLADE format) in a single forward pass across multiple languages (English, Malay, Chinese). Vectors are stored in Supabase `pgvector` to drive Reciprocal Rank Fusion (RRF) hybrid retrieval.
> 2. **Llama 3 8B / Qwen 2.5:** Deployed as an isolated, rubric-anchored evaluator using vLLM and Pydantic/Instructor schema validation. Used strictly for structured NER extraction in Feature 1 and closed rubric assessment in Feature 4 (Micro-Task Simulation feedback). Free-form, ungrounded generation is prohibited to eliminate hallucinations.

---

#### 4.2. Datasets

| Dataset Name | Source / URL | Type (public / private / self-collected / synthetic) | License | Personal Data? (Y/N) |
| --- | --- | --- | --- | --- |
| **ESCO Classification v1.2.0** (`skills_en.csv`, `occupations_en.csv`, `occupationSkillRelations_en.csv`) | European Commission ([ESCO Portal](https://esco.ec.europa.eu/en/use-esco/download)) | Public | CC BY 4.0 | **N** |
| **O\*NET Database v31.0** (`task_statements.csv`, `work_activities.csv`, `abilities.csv`) | U.S. Department of Labor / O\*NET Resource Center ([O\*NET Center](https://www.onetcenter.org/database.html)) | Public | Public Domain (U.S. Govt) | **N** |
| **MASCO 2020** (Malaysian Standard Classification of Occupations) | Ministry of Human Resources Malaysia ([eMASCO](https://emasco.mohr.gov.my/intro)) | Public | Public / Malaysian Government Open Data | **N** |
| **OpenDOSM Job Market Insights (JMI)** | Department of Statistics Malaysia ([OpenDOSM](https://open.dosm.gov.my/data-catalogue)) | Public | Open Data Commons Attribution (ODC-BY) | **N** |
| **Academic AI Exposure Indices** (AIOE, GPTs-are-GPTs, Webb Patent Scores) | Felten et al. (ResearchGate), Eloundou et al. (arXiv:2303.10130), Webb (arXiv:2412.04924) | Public | Academic Open Access / Research Use | **N** |
| **UNSD SDG Database & Metadata API v5** | United Nations Statistics Division ([UNSD API](https://unstats.un.org/sdgs/UNSDGAPIV5/v1/sdg)) | Public | UN Open Data Terms | **N** |
| **Synthetic Profile Dataset** (30 demo profiles) | In-house generator ([seed_synthetic_profiles.py](file:///c:/Coding/Hackathons/SDC_XMUM/src/supabase/seed_synthetic_profiles.py)) | Synthetic | MIT (Project repository) | **N** |

> **Data Privacy & Compliance Note:**  
> Real resume datasets (such as scraped LinkedIn profiles or public CV corpora) were strictly avoided in compliance with hackathon regulations to eliminate any exposure to Personally Identifiable Information (PII). All demonstration profiles were generated synthetically and mapped directly to canonical ESCO skill identifiers.

---

#### 4.3. AI-Assisted Development Tools

**Did your team use any generative-AI tool to help create code, design, text, or other project material?**  
`[X] Yes` `[ ] No`

**If yes, list them below:**

| Tool & Version | Used For | Extent of Use (minor / moderate / major) |
| --- | --- | --- |
| **Google Antigravity IDE (Gemini 2.5 / 3.8)** | Scaffolding FastAPI backend endpoints, `pgvector` SQL schemas, RRF stored procedures, data seeding scripts, and architectural documentation | **Major** |
| **Claude 3.5 Sonnet / ChatGPT Plus** | Comparative methodology review of academic AI exposure literature (Rai 2026, Felten, Webb) and drafting micro-task simulation rubrics | **Moderate** |

**Briefly describe how your team reviewed, tested, and took responsibility for AI-generated output:**  
*(Maximum 100 words)*
> Every AI-generated script, database migration, and algorithm implementation was reviewed by team members through strict verification steps. We validated SQL DDL and RRF PL/pgSQL functions directly in Supabase, tested FastAPI endpoints with automated schemas, and verified vector outputs against expected dimensions (1024-dim dense, 30k-dim sparse). Domain mappings (such as SDG targets and MASCO crosswalks) were anchored to official government/UN taxonomies rather than accepting ungrounded LLM completions. All algorithmic formulas (CTCI and weighted role scoring) were mathematically audited and verified with unit tests using synthetic profile data.

---

### Section 5. SPONSOR-PROVIDED RESOURCES

**Did your project use any official SDC sponsor-provided resource?**  
`[X] Yes` `[ ] No`

| Sponsor | Resource (API / credits / platform / data) | How It Was Used in the Project |
| --- | --- | --- |
| **RunPod** | GPU Compute Credits ($25 credits) | Provisioning a GPU-accelerated container to host the vLLM inference engine for BGE-M3 embeddings (`/embed`) and LLM simulation evaluation |

**Was the sponsor resource essential to the core functionality of the prototype, or could it be replaced? Explain briefly:**  
*(Maximum 100 words)*
> RunPod GPU compute was essential for deploying high-throughput, low-latency BGE-M3 dense and sparse vector generation during development. Without dedicated GPU infrastructure, running dense 1024-d and sparse 30k-d vectorization alongside LLM evaluation locally on CPU would introduce unacceptable latency for interactive matching. However, the architecture is modular: the backend consumes standardized REST endpoints (`/embed`), allowing RunPod to be seamlessly replaced with other containerized GPU platforms (e.g., AWS SageMaker, GCP Vertex AI, or local Ollama) without modifying core application logic.

---

### Section 6. SECURITY, PRIVACY & RESPONSIBLE USE

#### 6.1. Data Handling & Privacy
*(Maximum 150 words)*
> Telos adheres to privacy-by-design principles:
> 1. **Zero Real PII Storage:** No personal resumes or user identifiers are permanently harvested. Testing and live demonstrations exclusively utilize synthetic applicant profiles.
> 2. **Ephemeral CV Extraction:** Uploaded PDF resumes are parsed in-memory, converted to structured ESCO skill IDs, and immediately discarded without storing raw document files on disk.
> 3. **Row-Level Security (RLS):** Supabase database tables enforce strict RLS policies, restricting write permissions exclusively to the backend service role while granting public anonymous clients read-only access to taxonomy reference tables.
> 4. **API Key Security:** All cloud credentials and API keys are managed through server-side environment variables and are never bundled in frontend distributions or public code repositories.

#### 6.2. Known Limitations & Risks
*(Maximum 150 words)*
> 1. **AI Exposure Metric Bias:** As documented by Rai (2026), raw academic indices like AIOE correlate strongly with cognitive content intensity rather than true labor replaceability (Human Judgment Halo Effect). We mitigate this by weighting patent-based Webb scores at 0.50 and explicitly framing the metric as Cognitive Task Compression (CTCI) rather than job survival probability.
> 2. **Crosswalk Granularity:** Bridging MASCO 2020, O\*NET-SOC, and ESCO involves minor taxonomic discrepancies across jurisdictions. We resolve this by using title-based string normalization, strict fuzzy thresholding (cutoff $\ge 0.72$), and manual curation for ambiguous classifications.
> 3. **Closed Evaluation Bounds:** Simulation scoring relies on pre-defined rubrics to avoid LLM hallucinations, which may limit open-ended creative evaluation.

---

### Section 7. COMPLIANCE & READINESS

- [x] All APIs, cloud services, AI tools, models, and datasets used in the project are declared in this document.
- [x] All third-party code, datasets, and models are used in accordance with their licenses, and attribution is provided where required.
- [x] No API keys, passwords, or other credentials are exposed in the code repository, prototype, or this document.
- [x] Any use of generative-AI tools for development has been disclosed and reviewed by the team.
- [x] Any use of official SDC sponsor resources has been declared in Section 5.
- [x] All fields in this template have been completed within the word limits stated.