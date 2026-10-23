"""
seed_simulation_tasks.py — Seed curated micro-task simulation scenarios
for Feature 4 (Personalised Reskilling Pathway).
Owner: Person D (scenarios) & Person A (seeding execution)
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client

SRC_DIR = Path(__file__).resolve().parent.parent
load_dotenv(SRC_DIR / ".env")

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_SECRET_KEY = os.environ["SUPABASE_SECRET_KEY"]

db: Client = create_client(SUPABASE_URL, SUPABASE_SECRET_KEY)

SIMULATION_TASKS = [
    {
        "skill_id": "http://data.europa.eu/esco/skill/ccd0a1d9-afda-43d9-b901-96344886e14d",  # Python
        "scenario_text": "You are given a legacy Python data ingestion script that loads 50GB CSV files row-by-row into memory, causing frequent Out-Of-Memory (OOM) crashes in production. Outline your refactoring strategy to make this memory-efficient, robust to schema anomalies, and easily testable.",
        "rubric_criteria": [
            "memory-efficient processing (e.g. streaming generators, chunked reading, Polars/DuckDB/Pandas chunking)",
            "input validation and schema enforcement (e.g. Pydantic, Cerberus, or type checks)",
            "exception handling and corrupt row quarantine / dead-letter logging",
            "modular architecture with unit-testable components"
        ],
        "difficulty": "medium",
        "onet_task_ref": "15-1252.00-Task-01",
    },
    {
        "skill_id": "http://data.europa.eu/esco/skill/598de5b0-5b58-4ea7-8058-a4bc4d18c742",  # SQL
        "scenario_text": "An analytical query aggregating daily customer order value and lifetime spend joins a 50M-row orders table with customers and payment transactions, taking over 15 seconds to execute. Explain step-by-step how you diagnose and optimize this query.",
        "rubric_criteria": [
            "query execution plan diagnosis (EXPLAIN ANALYZE, identifying sequential scans vs index scans)",
            "indexing strategies (composite B-tree indexes on join keys and filter columns)",
            "query refactoring (avoiding SELECT *, eliminating correlated subqueries, using CTEs or window functions)",
            "partitioning or materialized view strategies for pre-aggregation"
        ],
        "difficulty": "medium",
        "onet_task_ref": "15-1243.00-Task-03",
    },
    {
        "skill_id": "http://data.europa.eu/esco/skill/bd14968e-e409-45af-b362-3495ed7b10e0",  # Cloud Technologies
        "scenario_text": "Your organization is migrating a mission-critical backend service to a cloud Kubernetes cluster. Describe your containerization and deployment architecture, focusing on security, zero-downtime updates, and automated scaling.",
        "rubric_criteria": [
            "multi-stage Docker build minimizing container image attack surface and size",
            "Kubernetes resource requests/limits and Horizontal Pod Autoscaler (HPA) configuration",
            "zero-downtime deployment strategy (rolling update, blue-green, or canary with readiness probes)",
            "secure secrets management (e.g. External Secrets Operator, Cloud KMS, or Vault)"
        ],
        "difficulty": "hard",
        "onet_task_ref": "15-1244.00-Task-02",
    },
    {
        "skill_id": "http://data.europa.eu/esco/skill/f9670490-8aa4-4540-b121-d440a8294aab",  # Develop data processing applications
        "scenario_text": "Design an automated, idempotent ETL pipeline that extracts transactional events from multiple third-party payment gateways into a centralized data warehouse. How do you guarantee exact-once processing semantics, handle API rate limits, and recover from partial network failures?",
        "rubric_criteria": [
            "idempotency design (upserts, unique deduplication keys, atomic staging tables)",
            "resilient rate limiting and exponential backoff retry mechanisms",
            "dead-letter queue (DLQ) for malformed payloads and alert triggers",
            "data freshness monitoring and pipeline observability (logging, metrics)"
        ],
        "difficulty": "hard",
        "onet_task_ref": "15-1251.00-Task-04",
    },
    {
        "skill_id": "http://data.europa.eu/esco/skill/3a2d5b45-56e4-4f5a-a55a-4a4a65afdc43",  # Machine Learning
        "scenario_text": "A machine learning fraud detection model deployed in production exhibits significant performance decay: precision drops by 25% over a three-month period. Detail your root cause analysis procedure and your design for a continuous model monitoring and automated retraining framework.",
        "rubric_criteria": [
            "data drift and concept drift detection methodology (e.g. KS-test, PSI, embedding drift)",
            "evaluation metrics appropriate for extreme class imbalance (PR-AUC, F1-Score, cost-weighted loss)",
            "re-training trigger mechanisms and shadow deployment validation before promotion",
            "feature store integration preventing train-serve skew"
        ],
        "difficulty": "hard",
        "onet_task_ref": "15-1299.08-Task-01",
    },
    {
        "skill_id": "http://data.europa.eu/esco/skill/97bd1c21-66b2-4b7e-ad0f-e3cda590e378",  # Data Analytics
        "scenario_text": "Executive leadership needs an analytical model to evaluate user drop-off across an onboarding funnel. Explain how you would structure cohort-based retention analysis, formulate actionable hypotheses, and present the findings to non-technical stakeholders.",
        "rubric_criteria": [
            "cohort retention matrix construction and survivorship bias controls",
            "statistical hypothesis testing comparing drop-off factors across user segments",
            "formulation of high-impact business metrics (activation rate, churn velocity)",
            "executive data storytelling with clear visualization recommendations"
        ],
        "difficulty": "medium",
        "onet_task_ref": "15-2051.01-Task-02",
    },
    {
        "skill_id": "http://data.europa.eu/esco/skill/9d2e926f-53d9-41f5-98f3-19dfaa687f3f",  # Software Configuration Management / CI-CD
        "scenario_text": "Design an automated continuous integration and continuous deployment (CI/CD) workflow for a distributed microservices platform. Detail the stages from pull request validation to staging and production release.",
        "rubric_criteria": [
            "automated pipeline stages (linting, unit tests, integration tests, build artifact creation)",
            "automated security checks (SAST, secret scanning, dependency vulnerability audit)",
            "automated environment promotion and semantic versioning",
            "automated rollback triggers upon failed health checks or smoke tests"
        ],
        "difficulty": "medium",
        "onet_task_ref": "15-1252.00-Task-05",
    },
    {
        "skill_id": "http://data.europa.eu/esco/skill/ecc4552a-92c5-4222-b18d-faf5ac841080",  # Deep Learning
        "scenario_text": "You are tasked with adapting an open-weights large language model (e.g. Llama-3-8B) to answer domain-specific compliance questions within strict enterprise hardware limits. Explain your strategy using parameter-efficient fine-tuning (PEFT) and quantization.",
        "rubric_criteria": [
            "PEFT methodology (LoRA / QLoRA with 4-bit NF4 quantization) to minimize VRAM footprint",
            "selection of rank (r), alpha, and target modules for tuning attention matrices",
            "curation of instruction-tuning datasets and domain loss evaluation",
            "preventing catastrophic forgetting of general reasoning capabilities"
        ],
        "difficulty": "hard",
        "onet_task_ref": "15-1299.08-Task-04",
    },
    {
        "skill_id": "http://data.europa.eu/esco/skill/143769cb-b61e-47d8-a61e-eedfbec1016c",  # Business Intelligence
        "scenario_text": "A retail business wants to migrate from disconnected Excel spreadsheets into a unified cloud BI warehouse. Propose a dimensional data model (Star Schema) and data governance framework to support automated self-service analytics.",
        "rubric_criteria": [
            "star schema design with clear separation of fact tables and conforming dimension tables",
            "handling historical changes through Slowly Changing Dimensions (SCD Type 2)",
            "definition of a single source of truth semantic layer for core business KPIs",
            "role-based access control (RBAC) and row-level security for sensitive commercial data"
        ],
        "difficulty": "medium",
        "onet_task_ref": "15-1243.01-Task-01",
    },
]

def main():
    print("=" * 60)
    print("Seeding Feature 4 Micro-Task Simulation Scenarios")
    print("=" * 60)

    inserted_count = 0
    for task in SIMULATION_TASKS:
        # Check if already exists for this skill
        existing = (
            db.schema("telos_sdc")
            .table("simulation_tasks")
            .select("id")
            .eq("skill_id", task["skill_id"])
            .maybe_single()
            .execute()
        )
        if existing and getattr(existing, "data", None):
            print(f"[SKIP] Task for skill {task['skill_id'][-12:]} already exists.")
            continue

        resp = (
            db.schema("telos_sdc")
            .table("simulation_tasks")
            .insert(task)
            .execute()
        )
        if resp.data:
            inserted_count += 1
            print(f"[OK] Seeded task for {task['onet_task_ref']} -> {task['scenario_text'][:60]}...")

    print(f"\nCompleted! Seeded {inserted_count} new simulation tasks.")

if __name__ == "__main__":
    main()
