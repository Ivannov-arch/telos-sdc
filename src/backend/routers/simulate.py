"""
routers/simulate.py — POST /api/simulate  (Feature 4 — Micro-Task Simulation)
Owner: Person A (scaffold) + Person D (prompts & evaluator logic)

Flow (scaffolded, Person D fills in LLM evaluator):
  1. Receive user_id + task_id + user_response
  2. Load simulation_task (scenario_text + rubric_criteria) from Supabase
  3. [Person D fills] Call RunPod LLM evaluator → Pydantic-validated score
  4. Write result to telos_sdc.simulation_results
  5. Return score_percent + improvement_reasoning + missing_concepts

Substep status:
  Done  Schema (telos_sdc.simulation_tasks, simulation_results) — Person A
  Done  POST /api/simulate request/response models — Person A
  TODO  LLM evaluator call at _evaluate_response() — Person D (Day 4)
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, HTTPException
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
    score_percent:         int | None = None         # 0-100; None if evaluator not yet wired
    improvement_reasoning: str | None = None
    missing_concepts:      list[str]  = []
    evaluated:             bool       = False        # False until Person D wires LLM evaluator


# ── LLM Evaluator Stub (Person D fills this in on Day 4) ─────────────────────


def _evaluate_response(
    scenario_text: str,
    rubric_criteria: list[Any],
    user_response: str,
) -> dict:
    """
    STUB — Person D replaces this with RunPod vLLM + Instructor call.

    Expected return shape:
    {
        "score_percent":          int (0–100),
        "improvement_reasoning":  str,
        "missing_concepts":       list[str],
    }

    Implementation note for Person D:
        1. Format a system prompt with scenario_text + rubric_criteria (JSON)
        2. Call RunPod endpoint (RUNPOD_LLM_URL from .env)
        3. Parse response with Pydantic + Instructor to enforce rigid JSON schema
        4. Return the dict above

    Until Person D wires this, the endpoint returns score_percent=None
    so Person C can build the UI without blocking on LLM output.
    """
    # Temporary: return None scores so the UI can be built
    return {
        "score_percent":          None,
        "improvement_reasoning":  "LLM evaluator not yet connected - Person D wires this on Day 4.",
        "missing_concepts":       [],
    }


# ── Main Endpoint ─────────────────────────────────────────────────────────────


@router.post("/simulate", response_model=SimulateResult)
def post_simulate(body: SimulateRequest):
    """
    POST /api/simulate

    Submit a user's response to a micro-task simulation scenario.
    Returns LLM-evaluated score and improvement feedback.

    Feature 4 — Substep 4.2 | Owner: Person D (evaluator), Person A (scaffold)
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

    # ── 3. Run LLM evaluator (stub until Person D wires Day 4) ───────────────
    eval_result = _evaluate_response(
        scenario_text=task["scenario_text"],
        rubric_criteria=task.get("rubric_criteria") or [],
        user_response=body.user_response,
    )

    evaluated = eval_result.get("score_percent") is not None

    # ── 4. Persist result ─────────────────────────────────────────────────────
    insert_payload = {
        "user_id":               body.user_id,
        "task_id":               body.task_id,
        "user_response":         body.user_response,
        "score_percent":         eval_result.get("score_percent"),
        "improvement_reasoning": eval_result.get("improvement_reasoning"),
        "missing_concepts":      eval_result.get("missing_concepts") or [],
        "evaluated_at":          datetime.now(timezone.utc).isoformat() if evaluated else None,
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
        score_percent=eval_result.get("score_percent"),
        improvement_reasoning=eval_result.get("improvement_reasoning"),
        missing_concepts=eval_result.get("missing_concepts") or [],
        evaluated=evaluated,
    )


# ── Convenience: GET /api/simulate/tasks (Person D: browse available tasks) ──


@router.get("/simulate/tasks")
def list_simulation_tasks(skill_id: str | None = None, limit: int = 20):
    """
    GET /api/simulate/tasks?skill_id=<esco_id>&limit=20

    Browse available simulation task scenarios.
    Person D uses this to verify tasks were seeded correctly (Substep 4.1).
    """
    db = get_supabase()
    query = (
        db.schema("telos_sdc")
        .table("simulation_tasks")
        .select("id, skill_id, scenario_text, difficulty, onet_task_ref")
        .limit(limit)
    )
    if skill_id:
        query = query.eq("skill_id", skill_id)
    resp = query.execute()
    return {"tasks": resp.data or [], "count": len(resp.data or [])}
