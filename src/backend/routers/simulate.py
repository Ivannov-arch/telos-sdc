"""
routers/simulate.py — POST /api/simulate & GET /api/simulate/tasks  (Feature 4 — Micro-Task Simulation)
Owner: Person D (prompts & evaluator logic) + Person A (backend schema & routing)

Flow:
  1. Receive user_id + task_id + user_response
  2. Load simulation_task (scenario_text + rubric_criteria) from Supabase
  3. Evaluate response via RunPod LLM evaluator (or deterministic rubric semantic evaluator fallback)
  4. Write result to telos_sdc.simulation_results
  5. Return score_percent (0-100) + improvement_reasoning + missing_concepts
"""

from __future__ import annotations

import os
import re
import json
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from backend.db import get_supabase

router = APIRouter()


# ── Request / Response Models ─────────────────────────────────────────────────


class SimulateRequest(BaseModel):
    user_id:       str = Field(..., description="UUID of the user profile")
    task_id:       str = Field(..., description="UUID of the simulation_task to attempt")
    user_response: str = Field(..., min_length=1, description="User's free-text answer to the scenario")


class SimulateResult(BaseModel):
    simulation_id:         str
    task_id:               str
    scenario_text:         str
    score_percent:         int = Field(..., description="Rubric evaluation score (0-100)")
    improvement_reasoning: str
    missing_concepts:      list[str] = []
    evaluated:             bool = True


# ── LLM & Rubric Evaluator Engine ─────────────────────────────────────────────


def _evaluate_with_remote_llm(
    scenario_text: str,
    rubric_criteria: list[Any],
    user_response: str,
) -> dict | None:
    """Attempt evaluation via external vLLM / RunPod endpoint if configured."""
    llm_url = os.environ.get("RUNPOD_LLM_ENDPOINT_URL") or os.environ.get("RUNPOD_LLM_URL")
    api_key = os.environ.get("RUNPOD_API_KEY")
    if not llm_url or "yyyyyyyy" in llm_url:
        return None

    try:
        import httpx
        headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
        prompt = (
            f"You are a strict, objective technical hiring evaluator.\n"
            f"Scenario: {scenario_text}\n"
            f"Rubric Criteria:\n" + "\n".join(f"- {c}" for c in rubric_criteria) + "\n\n"
            f"Candidate Response: {user_response}\n\n"
            f"Evaluate whether the candidate thoroughly addressed each rubric criterion.\n"
            f"Return ONLY valid JSON matching this schema:\n"
            f'{{"score_percent": <int 0-100>, "improvement_reasoning": "<concise constructive feedback>", "missing_concepts": ["<concept>", ...]}}'
        )
        resp = httpx.post(llm_url, json={"input": {"prompt": prompt}}, headers=headers, timeout=10.0)
        if resp.status_code == 200:
            data = resp.json()
            output = data.get("output") or data
            if isinstance(output, str):
                match = re.search(r'\{.*\}', output, re.DOTALL)
                if match:
                    parsed = json.loads(match.group(0))
                    return {
                        "score_percent": max(0, min(100, int(parsed.get("score_percent", 50)))),
                        "improvement_reasoning": str(parsed.get("improvement_reasoning", "")),
                        "missing_concepts": list(parsed.get("missing_concepts", [])),
                    }
    except Exception:
        pass
    return None


def _evaluate_rubric_deterministic(
    scenario_text: str,
    rubric_criteria: list[Any],
    user_response: str,
) -> dict:
    """
    Deterministic rubric-anchored semantic evaluator.
    Evaluates concept coverage, keywords, technical depth, and identifies missing concepts.
    """
    resp_lower = user_response.lower()
    total_criteria = len(rubric_criteria) if rubric_criteria else 1
    matched_criteria = 0
    missing_concepts = []

    for item in rubric_criteria:
        criterion_str = str(item).lower()
        # Extract keywords from criterion
        words = re.findall(r'[a-zA-Z0-9_\-\+]+', criterion_str)
        stopwords = {"and", "or", "the", "in", "with", "for", "to", "of", "a", "an", "e", "g", "e.g", "such", "as"}
        keywords = [w for w in words if len(w) > 2 and w not in stopwords]

        # Check keyword hits in user response
        hits = sum(1 for kw in keywords if kw in resp_lower)
        coverage_ratio = hits / len(keywords) if keywords else 0

        if coverage_ratio >= 0.4:
            matched_criteria += 1
        else:
            missing_concepts.append(str(item))

    # Base score from rubric criteria coverage (70% weight)
    rubric_score = (matched_criteria / total_criteria) * 70.0

    # Depth & quality score (30% weight) based on response length and technical vocabulary
    words_count = len(user_response.split())
    if words_count >= 80:
        depth_score = 30.0
    elif words_count >= 45:
        depth_score = 24.0
    elif words_count >= 20:
        depth_score = 16.0
    else:
        depth_score = 6.0

    final_score = int(round(rubric_score + depth_score))
    final_score = max(10, min(100, final_score))

    if missing_concepts:
        improvement = (
            f"Addressed {matched_criteria} of {total_criteria} required criteria. "
            f"To achieve full proficiency, strengthen your explanation on: {'; '.join(missing_concepts[:3])}."
        )
    else:
        improvement = (
            f"Excellent comprehensive response covering all {total_criteria} required criteria "
            "with sound technical reasoning and practical architectural considerations."
        )

    return {
        "score_percent": final_score,
        "improvement_reasoning": improvement,
        "missing_concepts": missing_concepts,
    }


def _evaluate_response(
    scenario_text: str,
    rubric_criteria: list[Any],
    user_response: str,
) -> dict:
    """Evaluates response using RunPod LLM when configured, falling back to deterministic rubric evaluator."""
    llm_result = _evaluate_with_remote_llm(scenario_text, rubric_criteria, user_response)
    if llm_result is not None:
        return llm_result
    return _evaluate_rubric_deterministic(scenario_text, rubric_criteria, user_response)


# ── Main Endpoints ────────────────────────────────────────────────────────────


@router.post("/simulate", response_model=SimulateResult)
def post_simulate(body: SimulateRequest):
    """
    POST /api/simulate

    Submit a user's response to a micro-task simulation scenario.
    Returns LLM-evaluated score and improvement feedback.

    Feature 4 — Substep 4.2 | Owner: Person D (evaluator), Person A (backend)
    """
    db = get_supabase()

    # ── 1. Validate user exists ───────────────────────────────────────────────
    user_resp = (
        db.schema("telos_sdc")
        .table("user_profiles")
        .select("id")
        .eq("id", body.user_id)
        .maybe_single()
        .execute()
    )
    if not user_resp or not getattr(user_resp, "data", None):
        raise HTTPException(status_code=404, detail=f"User profile {body.user_id!r} not found")

    # ── 2. Load simulation task ───────────────────────────────────────────────
    task_resp = (
        db.schema("telos_sdc")
        .table("simulation_tasks")
        .select("id, scenario_text, rubric_criteria, difficulty, skill_id")
        .eq("id", body.task_id)
        .maybe_single()
        .execute()
    )
    if not task_resp or not getattr(task_resp, "data", None):
        raise HTTPException(status_code=404, detail=f"Simulation task {body.task_id!r} not found")

    task = task_resp.data

    # ── 3. Run evaluator ──────────────────────────────────────────────────────
    eval_result = _evaluate_response(
        scenario_text=task["scenario_text"],
        rubric_criteria=task.get("rubric_criteria") or [],
        user_response=body.user_response,
    )

    # ── 4. Persist result ─────────────────────────────────────────────────────
    now_iso = datetime.now(timezone.utc).isoformat()
    insert_payload = {
        "user_id":               body.user_id,
        "task_id":               body.task_id,
        "user_response":         body.user_response,
        "score_percent":         eval_result["score_percent"],
        "improvement_reasoning": eval_result["improvement_reasoning"],
        "missing_concepts":      eval_result["missing_concepts"],
        "evaluated_at":          now_iso,
    }

    insert_resp = (
        db.schema("telos_sdc")
        .table("simulation_results")
        .insert(insert_payload)
        .execute()
    )
    inserted = (insert_resp.data or [{}])[0]
    sim_id = inserted.get("id", "unknown")

    # ── 5. Return ─────────────────────────────────────────────────────────────
    return SimulateResult(
        simulation_id=sim_id,
        task_id=body.task_id,
        scenario_text=task["scenario_text"],
        score_percent=eval_result["score_percent"],
        improvement_reasoning=eval_result["improvement_reasoning"],
        missing_concepts=eval_result["missing_concepts"],
        evaluated=True,
    )


@router.get("/simulate/tasks")
def list_simulation_tasks(skill_id: str | None = None, limit: int = 20):
    """
    GET /api/simulate/tasks?skill_id=<esco_id>&limit=20

    Browse available simulation task scenarios.
    Frontend uses this to load simulations for missing skills identified in Feature 3.
    """
    db = get_supabase()
    query = (
        db.schema("telos_sdc")
        .table("simulation_tasks")
        .select("id, skill_id, scenario_text, rubric_criteria, difficulty, onet_task_ref, skills(preferred_label)")
        .limit(limit)
    )
    if skill_id:
        query = query.eq("skill_id", skill_id)
    resp = query.execute()

    tasks = []
    for t in (resp.data or []):
        tasks.append({
            "id": t["id"],
            "skill_id": t["skill_id"],
            "skill_name": t.get("skills", {}).get("preferred_label", "") if t.get("skills") else "",
            "scenario_text": t["scenario_text"],
            "rubric_criteria": t.get("rubric_criteria") or [],
            "difficulty": t["difficulty"],
            "onet_task_ref": t.get("onet_task_ref"),
        })
    return {"tasks": tasks, "count": len(tasks)}


@router.get("/simulate/history")
def get_simulation_history(user_id: str = Query(..., description="UUID of the user profile")):
    """
    GET /api/simulate/history?user_id=<uuid>

    Retrieve past simulation task attempts and scores for a user profile.
    Used for tracking the Skill Gap Reduction Rate KPI.
    """
    db = get_supabase()
    resp = (
        db.schema("telos_sdc")
        .table("simulation_results")
        .select("id, task_id, user_response, score_percent, improvement_reasoning, missing_concepts, evaluated_at, created_at, simulation_tasks(skill_id, scenario_text, difficulty)")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )
    return {"history": resp.data or [], "total_attempts": len(resp.data or [])}
