Below are the **appropriate and verifiable** datasets for Feature 1, 3, and 5. Core recommendation: use **ESCO** as the backbone for skills and occupations, **O*NET** as a complement for job tasks/skills details, **OpenDOSM / Job Market Insights** for Malaysian local context, and the **UN SDG API** for official SDG mapping. Avoid CV datasets containing real resumes, as hackathon rules prohibit real personal data. [esco.ec.europa](https://esco.ec.europa.eu/en/use-esco/download)

## Dataset Map by Feature

| Feature | Primary Dataset | Role in System | Verification Status |
|---|---|---|---|
| 1. Skills Profile Intake | ESCO Skills/Competences + synthetic CV profiles | Normalizes skills from CV/form into standardized skill IDs | Official, free, multi-format, multi-lingual. [esco.ec.europa](https://esco.ec.europa.eu/en/use-esco/download) |
| 3. Future-Role Matching + Skill Gap | ESCO Occupations ? Skills, O*NET Skills/Tasks, DOSM Job Market Insights | Role catalogs, required skills, skill weights/urgency, Malaysia context validation | Official and downloadable/API. [onetcenter](https://www.onetcenter.org/database.html) |
| 5. SDG Mapping | UN SDG API / UNSD SDG framework | Official goals, targets, and indicators for role/skill tagging | Official UN source with Goal/Target/Indicator endpoints. [unstats.un](https://unstats.un.org/sdgs/UNSDGAPIV5/swagger/index.html) |

## Feature 1: Skills Profile Intake

### 1. ESCO Skills and Competences — Primary Choice

**Source:** European Commission, ESCO.  
**URL:** [https://esco.ec.europa.eu/en/use-esco/download](https://esco.ec.europa.eu/en/use-esco/download)  
**Format:** CSV, JSON-LD, RDF/TTL, ODS, XML; also available via Web API and Local API. [esco.ec.europa](https://esco.ec.europa.eu/en/use-esco/download)

**Why It Is Most Suitable:**
- ESCO contains classifications of **occupations, skills, competences, and qualifications**, not merely raw skill lists. [esco.ec.europa](https://esco.ec.europa.eu/en/use-esco/download)
- Available in multiple languages, facilitating the normalization of terms like "Data Analysis", "Data Analytics", or "Data Processing" to equivalent concepts. [esco.ec.europa](https://esco.ec.europa.eu/en/use-esco/download)
- Its RDF/JSON-LD structure is ideal for knowledge graphs: skills can be linked to occupations, essential skills, optional skills, and broader/narrower skills. [esco.ec.europa](https://esco.ec.europa.eu/en/use-esco/download)

**How to Use for Feature 1:**
- Create a `skills` table with columns: `esco_id`, `preferred_label`, `alt_labels`, `skill_type`, `description`, `broader_skill_id`.
- When a CV/form is extracted, map extracted items to `esco_id` rather than storing only raw text.
- Store a confidence score for each mapping; do not force LLMs to assign a skill if evidence is insufficient.

**Verification:** Official European Commission dataset, free to download, with latest versions accessible via portal or API. [esco.ec.europa](https://esco.ec.europa.eu/en/use-esco/download)

### 2. Synthetic CV / Profile Dataset — Synthetic Only

For demos, avoid datasets claiming to contain "real and synthetic resumes". Hugging Face datasets such as `datasetmaster/resumes` explicitly state that they contain a mix of real and synthetic resumes, thereby **risking a violation of the rule "do not use real personal data or real CVs"**. [huggingface](https://huggingface.co/datasets/datasetmaster/resumes)

**Safer Alternatives:**
- Generate 20–50 synthetic demo profiles in JSON format adhering to the ESCO schema.
- Use fictitious names, fictitious experiences, and skills mapped to ESCO IDs.
- For extraction training/evaluation datasets, use only explicitly synthetic-only datasets and verify their licenses and provenance before use.

**Verification Note:** Resume datasets on Hugging Face are generally not institutional sources and several contain blended real + synthetic data; treat them as experimental references only, not primary product datasets. [huggingface](https://huggingface.co/datasets/datasetmaster/resumes)

## Feature 3: Future-Role Matching + Skill Gap

### 1. ESCO Occupations ? Skills — Matching Basis

**Source:** ESCO download/API.  
**Components to Extract:**
- `occupations.csv` / occupation RDF
- `skills.csv` / skill RDF
- Occupation–skill relations, including essential vs optional skills where available in the ESCO structure. [esco.ec.europa](https://esco.ec.europa.eu/en/use-esco/download)

**Why It Is Critical:**
- For every target role, you can construct a required skills vector.
- Skill gaps can be computed as:
  $$
  \text{Gap} = \text{Required Skills} \setminus \text{User Skills}
  $$
- Because ESCO features hierarchical relations, gaps can be separated into *core gaps* and *supporting gaps*, rather than an undifferentiated list of missing skills. [esco.ec.europa](https://esco.ec.europa.eu/en/use-esco/download)

### 2. O*NET Database — Occupation, Skill, and Task Details

**Source:** U.S. Department of Labor / O*NET Resource Center.  
**URL:** [https://www.onetcenter.org/database.html](https://www.onetcenter.org/database.html)  
**Format:** Relational database/SQL, CSV, XML, and RDF; also available via Web Services API. [onetcenter](https://www.onetcenter.org/database.html)

**Why It Is Useful:**
- O*NET defines occupations through **knowledge, skills, abilities, tasks, and work activities**. [dol](https://www.dol.gov/agencies/eta/onet)
- The `Skills` file maps O*NET-SOC occupation codes to skill ratings. [onetcenter](https://www.onetcenter.org/dictionary/22.3/mysql/skills.html)
- Task-level data enables analysis of "which tasks are likely to change due to AI", moving beyond simple job title matching.

**How to Use:**
- Enrich role descriptions with O*NET: `occupation_title`, `tasks`, `skills`, `knowledge`, `work_activities`.
- Maintain ESCO as the canonical ID; map O*NET SOC to ESCO only where the mapping is rigorously justifiable.
- Avoid forcibly merging the two taxonomies; it is safer to store both and clearly cite the respective source of each.

**Verification:** Maintained by the U.S. Department of Labor, updated periodically, with the latest database release currently designated as version 31.0. [onetcenter](https://www.onetcenter.org/database.html)

### 3. OpenDOSM / Job Market Insights — Malaysian Context

**Source:** Department of Statistics Malaysia (DOSM).  
**Catalog URL:** [https://open.dosm.gov.my/data-catalogue](https://open.dosm.gov.my/data-catalogue)  
**Labour Market Portal:** [https://mylabourhub.dosm.gov.my](https://mylabourhub.dosm.gov.my)  
**Job Market Insights:** [https://www.dosm.gov.my/bda-jmi](https://www.dosm.gov.my/bda-jmi)  
**My Job Profile:** [https://myjobprofile.dosm.gov.my](https://myjobprofile.dosm.gov.my) [dosm.gov](https://www.dosm.gov.my/portal-main/release-content/big-data-analytics-job-market-insights-and-my-job-profile-q42023)

**Why It Is Essential for a Malaysian Hackathon:**
- Job Market Insights and My Job Profile are quarterly releases derived from online job postings across popular recruitment portals. [dosm.gov](https://www.dosm.gov.my/portal-main/release-content/big-data-analytics-job-market-insights-and-my-job-profile-q42023)
- Releases report job vacancies broken down by **occupation, economic activity, state, skills, and field of studies**. [dosm.gov](https://www.dosm.gov.my/portal-main/release-content/big-data-analytics-job-market-insights-and-my-job-profile-q42023)
- My Job Profile includes TVET-related job openings data categorized under MASCO. [myjobprofile.dosm.gov](http://myjobprofile.dosm.gov.my/bda-myjobprofile/tvet)

**How to Use:**
- Use for **local validation**, not as a replacement for ESCO/O*NET.
- Display Malaysian context: number of openings per job category, state, sector, or skill category.
- Do not claim this data is real-time if derived from quarterly releases; state the reporting period and update date clearly.

**Verification:** DOSM is the official statistics authority of Malaysia; the OpenDOSM catalog and Job Market Insights portals are publicly accessible, with recent releases noted through August 2026. [open.dosm.gov](https://open.dosm.gov.my/data-catalogue)

## Feature 5: SDG Mapping

### UN SDG API — The Authoritative Official Source

**Source:** United Nations Statistics Division.  
**API Documentation:** [https://unstats.un.org/sdgs/UNSDGAPIV5/swagger/index.html](https://unstats.un.org/sdgs/UNSDGAPIV5/swagger/index.html)  
**Official Metadata:** [https://unstats.un.org/sdgs/metadata/](https://unstats.un.org/sdgs/metadata/) [unstats.un](https://unstats.un.org/sdgs/UNSDGAPIV5/swagger/index.html)

**Relevant Endpoints:**
- `GET /v1/sdg/Goal/List`
- `GET /v1/sdg/Goal/{goalCode}/Target/List`
- `GET /v1/sdg/Target/List`
- `GET /v1/sdg/Indicator/List` [unstats.un](https://unstats.un.org/sdgs/UNSDGAPIV5/swagger/index.html)

**Why It Is the Right Choice:**
- Provides the official framework of **17 Goals, 169 Targets, and global indicators** for the 2030 Agenda. [data.unesco](https://data.unesco.org/explore/dataset/sdg001/api/?flg=en-us)
- Ingest `sdg_goals`, `sdg_targets`, and `sdg_indicators` tables directly from the API, then build `role_sdg` and `skill_sdg` relation tables.
- Eliminates reliance on arbitrary LLM-generated SDG references.

**Recommended Minimum Schema:**

```json
{
  "role_id": "esco:2512",
  "role_title": "AI Governance / Responsible AI Specialist",
  "sdg_alignment": [
    {
      "sdg_goal": 8,
      "sdg_target": "8.2",
      "source": "UNSD SDG API",
      "relationship_type": "supports",
      "evidence": "Role supports innovation and productivity through responsible AI adoption."
    }
  ]
}
```

**Important:** The UN API supplies goal/target/indicator definitions, but **does not provide automated "role ? SDG" mappings**. The role/skill to SDG mapping must be maintained as an auditable curated table with verifiable justifications and sources. [unstats.un](https://unstats.un.org/sdgs/UNSDGAPIV5/swagger/index.html)

## Most Realistic Stack for a 5-Day Hackathon

1. **ESCO** as the primary canon for `skill_id`, `occupation_id`, and occupation–skill relations. [esco.ec.europa](https://esco.ec.europa.eu/en/use-esco/download)
2. **O*NET** as a complement for tasks, work activities, and detailed role descriptions. [onetcenter](https://www.onetcenter.org/database.html)
3. **OpenDOSM Job Market Insights** for Malaysian local signals and role relevance validation. [dosm.gov](https://www.dosm.gov.my/portal-main/release-content/big-data-analytics-job-market-insights-and-my-job-profile-q42023)
4. **UN SDG API** as the official authority for SDG goals, targets, and indicators. [unstats.un](https://unstats.un.org/sdgs/UNSDGAPIV5/swagger/index.html)
5. **In-house synthetic user profiles** for Feature 1 demo purposes, avoiding real CV datasets. [huggingface](https://huggingface.co/datasets/datasetmaster/resumes)

## Verification Checklist Before Deployment

- **License and Attribution:** Review terms of use for ESCO, O*NET, DOSM, and UNSD prior to publishing the repository.
- **Version and Timestamps:** Record `dataset_version`, `retrieved_at`, and source URLs in the repository.
- **Language Support:** ESCO supports multiple languages; use English as the canonical technical representation while retaining alternative labels for Bahasa Malaysia/Chinese where available. [esco.ec.europa](https://esco.ec.europa.eu/en/use-esco/download)
- **Mapping Quality:** Never allow the LLM to invent `skill ? SDG` relations without a curated reference table; ungrounded links risk penalization as hallucinations.
- **CV Data:** Strictly use self-generated synthetic profiles; avoid datasets containing real resumes. [huggingface](https://huggingface.co/datasets/datasetmaster/resumes)

The combination of **ESCO + O*NET + DOSM + UNSD SDG API** is the most defensible architecture: official, open, structured, citable, and comprehensive enough to power intake, matching, skill gaps, and SDG alignment without compromising privacy. [esco.ec.europa](https://esco.ec.europa.eu/en/use-esco/download)
