"""
routers/game.py — FutureProof Crisis Simulation Game Engine
Features: F01 (Quick Skill Profile) + F02 (Crisis Simulation) + F03 (Decision & Skill Report)
            F04 (Role Matching) + F05 (Career Pathway)

Endpoints:
  POST /api/game/start                          → create session, return R1 briefing
  POST /api/game/{session_id}/round             → submit round response, advance state
  GET  /api/game/{session_id}/state             → current round + briefing content
  GET  /api/game/{session_id}/evidence/{round}  → evidence drawer data
  GET  /api/game/{session_id}/report            → trigger LLM eval + behavioral report
  GET  /api/game/{session_id}/match             → F04 role matching (3 roles)
  GET  /api/game/pathway/{role_id}              → F05 reskilling path
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator

from fastapi import Query
from backend.db import get_supabase
from backend.game_evaluator import evaluate_session
from backend.game_matcher import match_from_session, MVP_ROLES
from backend.game_pathway import build_pathway

router = APIRouter()

# ── Constants ──────────────────────────────────────────────────────────────────

VALID_MISSIONS = {"A", "B", "C"}
ROUND_SEQUENCE = ["round_1", "round_2", "round_3", "round_4", "complete"]

# ── Request / Response Models ─────────────────────────────────────────────────


class QuickProfile(BaseModel):
    skills: list[str] = Field(..., min_length=1, description="Self-declared skills")
    interests: list[str] = Field(default_factory=list, description="Career interests")
    learning_time: int = Field(default=5, ge=1, le=40, description="Hours/week for upskilling")


class StartGameRequest(BaseModel):
    profile: QuickProfile
    mission_id: Literal["A", "B", "C"]


class StartGameResponse(BaseModel):
    session_id: str
    round: int
    briefing: str
    instructions: str


class RoundRequest(BaseModel):
    round: int = Field(..., ge=1, le=4)
    free_text: str | None = Field(None, description="Required for R1 and R3")
    action: Literal["accept", "reject", "verify"] | None = Field(None, description="Required for R2")
    evidence_opened: bool | None = Field(None, description="R2: did player open evidence drawer?")

    @field_validator("free_text")
    @classmethod
    def text_min_length(cls, v: str | None) -> str | None:
        if v is not None and len(v.strip()) < 10:
            raise ValueError("Response is too short. Tell us a bit more about your approach.")
        return v


class RoundResponse(BaseModel):
    session_id: str
    round_accepted: int
    next_round: int | None
    status: str
    next_briefing: str | None = None
    ai_recommendation: str | None = None
    evidence_available: bool = False
    shock_event: str | None = None
    shock_opportunity: str | None = None
    message: str = ""


class IndicatorResult(BaseModel):
    observed: bool
    evidence: str


class DecisionQualityResult(BaseModel):
    met_objectives: bool
    note: str


class BehavioralReport(BaseModel):
    session_id: str
    mission: str
    profile: dict
    indicators: dict[str, Any]
    self_vs_observed_gap: dict[str, Any]
    limitation_notice: str
    role_match_available: bool


# ── Fallback In-Memory Stores (Guarantees zero-failure operation) ─────────────

import json
from pathlib import Path

_MEMORY_SESSIONS: dict[str, dict] = {}
_MEMORY_EVENTS: list[dict] = []
_SCENARIOS_CACHE: list[dict] | None = None


def _load_fallback_scenarios() -> list[dict]:
    global _SCENARIOS_CACHE
    if _SCENARIOS_CACHE is None:
        for candidate in [
            Path(__file__).parent.parent / "game_scenarios.json",
            Path(__file__).parent / "game_scenarios.json",
        ]:
            if candidate.exists():
                try:
                    with open(candidate, "r", encoding="utf-8") as f:
                        _SCENARIOS_CACHE = json.load(f)
                        break
                except Exception:
                    pass
        if _SCENARIOS_CACHE is None:
            _SCENARIOS_CACHE = []
    return _SCENARIOS_CACHE


def _get_session(session_id: str) -> dict:
    try:
        db = get_supabase()
        resp = (
            db.schema("telos_sdc")
            .table("game_sessions")
            .select("*")
            .eq("id", session_id)
            .maybe_single()
            .execute()
        )
        if resp and getattr(resp, "data", None):
            return resp.data
    except Exception:
        pass

    if session_id in _MEMORY_SESSIONS:
        return _MEMORY_SESSIONS[session_id]
    raise HTTPException(status_code=404, detail=f"Session {session_id!r} not found")


def _get_scenario(mission_id: str, round_number: int) -> dict:
    try:
        db = get_supabase()
        resp = (
            db.schema("telos_sdc")
            .table("crisis_scenarios")
            .select("*")
            .eq("mission_id", mission_id)
            .eq("round_number", round_number)
            .maybe_single()
            .execute()
        )
        if resp and getattr(resp, "data", None):
            return resp.data
    except Exception:
        pass

    for s in _load_fallback_scenarios():
        if s.get("mission_id") == mission_id and s.get("round_number") == round_number:
            return s

    raise HTTPException(
        status_code=503,
        detail=f"Scenario data missing for mission {mission_id!r} round {round_number}.",
    )


def _status_for_round(round_number: int) -> str:
    if round_number > 4:
        return "complete"
    return f"round_{round_number}"


def _update_session(session_id: str, patch: dict) -> None:
    try:
        db = get_supabase()
        db.schema("telos_sdc").table("game_sessions").update(patch).eq("id", session_id).execute()
    except Exception:
        pass
    if session_id in _MEMORY_SESSIONS:
        _MEMORY_SESSIONS[session_id].update(patch)
    else:
        _MEMORY_SESSIONS[session_id] = patch


def _log_round_event(session_id: str, round_number: int, payload: dict) -> None:
    event = {
        "session_id": session_id,
        "round_number": round_number,
        "action": payload.get("action"),
        "free_text": payload.get("free_text"),
        "evidence_opened": payload.get("evidence_opened", False),
        "ai_trusted": payload.get("ai_trusted"),
    }
    try:
        db = get_supabase()
        db.schema("telos_sdc").table("round_events").insert(event).execute()
    except Exception:
        pass
    _MEMORY_EVENTS.append(event)


def _compute_self_vs_observed_gap(
    profile: dict, indicators: dict
) -> dict:
    """Surface contrast between self-declared skills and observed behavioural indicators."""
    claimed = profile.get("skills", [])
    observed_strengths = []
    observed_gaps = []

    indicator_labels = {
        "calibrated_ai_trust": "Calibrated AI Trust",
        "critical_verification": "Critical Verification",
        "decision_quality": "Decision Quality",
        "adaptability": "Adaptability",
    }

    for key, label in indicator_labels.items():
        ind = indicators.get(key, {})
        if isinstance(ind, dict):
            if ind.get("observed") is True or ind.get("met_objectives") is True:
                observed_strengths.append(label)
            elif ind.get("observed") is False or ind.get("met_objectives") is False:
                observed_gaps.append(label)

    note = ""
    if observed_strengths:
        note = f"Your observed behaviour showed strength in: {', '.join(observed_strengths)}."
    if observed_gaps:
        note += f" Areas to develop: {', '.join(observed_gaps)}."

    return {
        "claimed_skills": claimed,
        "observed_strengths": observed_strengths,
        "observed_gaps": observed_gaps,
        "note": note,
    }


# ── Endpoints ─────────────────────────────────────────────────────────────────


@router.post("/game/start", response_model=StartGameResponse)
def start_game(body: StartGameRequest):
    """
    POST /api/game/start

    Create a new game session with the player's Quick Skill Profile and chosen mission.
    Returns the Round 1 crisis briefing.

    Feature 01 + Feature 02 — Session init
    """
    # Load R1 scenario
    scenario = _get_scenario(body.mission_id, round_number=1)
    session_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()

    session_data = {
        "id": session_id,
        "mission_id": body.mission_id,
        "status": "round_1",
        "profile": body.profile.model_dump(),
        "rounds": [],
        "created_at": now,
    }
    _MEMORY_SESSIONS[session_id] = session_data

    try:
        db = get_supabase()
        db.schema("telos_sdc").table("game_sessions").insert(session_data).execute()
    except Exception:
        pass

    return StartGameResponse(
        session_id=session_id,
        round=1,
        briefing=scenario["briefing_text"],
        instructions=(
            "What is your strategy? There is no wrong answer — "
            "just tell us what you would do. (AI advisor is unavailable in Round 1)"
        ),
    )


@router.post("/game/{session_id}/round", response_model=RoundResponse)
def submit_round(session_id: str, body: RoundRequest):
    """
    POST /api/game/{session_id}/round

    Submit a player's round response. Advances game state.
    - R1: free_text required (AI locked)
    - R2: action required (accept | reject | verify); evidence_opened tracked
    - R3: free_text required (shock event response)
    - R4: free_text required (final decision, triggers eval queue)

    Feature 02 — Crisis Simulation state machine
    """
    session = _get_session(session_id)
    current_status = session["status"]
    mission_id = session["mission_id"]
    expected_round = int(current_status.split("_")[-1]) if current_status != "complete" else 5

    if current_status == "complete":
        raise HTTPException(status_code=400, detail="Session is already complete.")

    if body.round != expected_round:
        raise HTTPException(
            status_code=400,
            detail=f"Expected round {expected_round}, got {body.round}.",
        )

    # ── Validate round-specific inputs ────────────────────────────────────────
    if body.round in (1, 3):
        if not body.free_text or len(body.free_text.strip()) < 10:
            raise HTTPException(
                status_code=422,
                detail="Free text response required for this round. Minimum 10 characters.",
            )

    if body.round == 2:
        if not body.action:
            raise HTTPException(
                status_code=422,
                detail="Action (accept | reject | verify) required for Round 2.",
            )

    # ── Log round event ───────────────────────────────────────────────────────
    event_payload: dict[str, Any] = {
        "free_text": body.free_text,
        "action": body.action,
        "evidence_opened": body.evidence_opened or False,
    }

    if body.round == 2:
        event_payload["ai_trusted"] = body.action == "accept"

    _log_round_event(session_id, body.round, event_payload)

    # ── Advance round ─────────────────────────────────────────────────────────
    next_round = body.round + 1
    next_status = _status_for_round(next_round)

    rounds = session.get("rounds") or []
    rounds.append(
        {
            "round": body.round,
            "free_text": body.free_text,
            "action": body.action,
            "evidence_opened": body.evidence_opened,
        }
    )

    patch: dict[str, Any] = {"status": next_status, "rounds": rounds}
    if next_status == "complete":
        patch["completed_at"] = datetime.now(timezone.utc).isoformat()

    _update_session(session_id, patch)

    # ── Build response ────────────────────────────────────────────────────────
    if next_status == "complete":
        return RoundResponse(
            session_id=session_id,
            round_accepted=body.round,
            next_round=None,
            status="complete",
            message="Game complete. Retrieve your report at GET /api/game/{session_id}/report",
        )

    next_scenario = _get_scenario(mission_id, next_round)

    return RoundResponse(
        session_id=session_id,
        round_accepted=body.round,
        next_round=next_round,
        status=next_status,
        next_briefing=next_scenario.get("briefing_text"),
        ai_recommendation=next_scenario.get("ai_recommendation"),
        evidence_available=bool(next_scenario.get("evidence_data")),
        shock_event=next_scenario.get("shock_event_text"),
        shock_opportunity=next_scenario.get("shock_opportunity"),
        message=f"Round {body.round} recorded. Proceed to Round {next_round}.",
    )


@router.get("/game/{session_id}/state")
def get_game_state(session_id: str):
    """
    GET /api/game/{session_id}/state

    Returns the current round and its scenario content for the frontend to render.
    Used for page refresh recovery and initial load after session creation.

    Feature 02 — Crisis Simulation state
    """
    session = _get_session(session_id)
    mission_id = session["mission_id"]
    status = session["status"]

    if status == "complete":
        return {
            "session_id": session_id,
            "status": "complete",
            "mission_id": mission_id,
            "rounds_completed": len(session.get("rounds") or []),
            "report_url": f"/api/game/{session_id}/report",
        }

    current_round = int(status.split("_")[-1])
    scenario = _get_scenario(mission_id, current_round)

    return {
        "session_id": session_id,
        "status": status,
        "mission_id": mission_id,
        "current_round": current_round,
        "briefing": scenario.get("briefing_text"),
        "ai_recommendation": scenario.get("ai_recommendation"),
        "evidence_available": bool(scenario.get("evidence_data")),
        "shock_event": scenario.get("shock_event_text"),
        "shock_opportunity": scenario.get("shock_opportunity"),
    }


@router.get("/game/{session_id}/evidence/{round_number}")
def get_evidence(session_id: str, round_number: int):
    """
    GET /api/game/{session_id}/evidence/{round_number}

    Returns the evidence drawer data for R2 (and optionally R3).
    Call is logged as an indicator signal for Critical Verification scoring.

    Feature 02 — Evidence Drawer
    """
    session = _get_session(session_id)
    scenario = _get_scenario(session["mission_id"], round_number)

    evidence = scenario.get("evidence_data")
    if not evidence:
        raise HTTPException(
            status_code=404,
            detail=f"No evidence data available for round {round_number}.",
        )

    # Log evidence access (used in Critical Verification scoring)
    _log_round_event(
        session_id,
        round_number,
        {"action": "evidence_viewed", "evidence_opened": True},
    )

    return {"round": round_number, "evidence": evidence}


@router.get("/game/{session_id}/report", response_model=BehavioralReport)
def get_report(session_id: str):
    """
    GET /api/game/{session_id}/report

    Triggers LLM behavioral evaluation (batched R1 + R3 in one call) and returns the
    full Decision & Skill Report. Safe to call multiple times — result is cached in DB.

    Feature 03 — Decision & Skill Report + The Reveal
    """
    session = _get_session(session_id)

    if session["status"] != "complete":
        raise HTTPException(
            status_code=400,
            detail=(
                f"Session is not complete (status: {session['status']}). "
                "Complete all 4 rounds before retrieving the report."
            ),
        )

    # Return cached result if already evaluated
    if session.get("eval_result"):
        indicators = session["eval_result"]
    else:
        events = []
        try:
            db = get_supabase()
            events_resp = (
                db.schema("telos_sdc")
                .table("round_events")
                .select("*")
                .eq("session_id", session_id)
                .order("round_number")
                .execute()
            )
            events = events_resp.data or []
        except Exception:
            events = [e for e in _MEMORY_EVENTS if e.get("session_id") == session_id]

        # Evaluate using batched LLM + event log
        indicators = evaluate_session(
            session=session,
            round_events=events,
            mission_id=session["mission_id"],
        )

        # Cache in DB
        _update_session(session_id, {"eval_result": indicators})

    profile = session.get("profile", {})
    self_gap = _compute_self_vs_observed_gap(profile, indicators)

    return BehavioralReport(
        session_id=session_id,
        mission=session["mission_id"],
        profile=profile,
        indicators=indicators,
        self_vs_observed_gap=self_gap,
        limitation_notice=(
            "This evidence comes from one 4-round simulation. "
            "It is not sufficient to conclude your professional ability in general."
        ),
        role_match_available=True,
    )


@router.get("/game/{session_id}/match")
def get_role_match(session_id: str):
    """
    GET /api/game/{session_id}/match

    Feature 04 — Future Skills Radar & Role Matching.
    Returns top 3 role matches ranked by behavioral evidence + profile + mission affinity.
    Requires the session to be complete and evaluated (GET /report must have been called first,
    or is called automatically here).
    """
    session = _get_session(session_id)

    if session["status"] != "complete":
        raise HTTPException(
            status_code=400,
            detail=f"Session must be complete before role matching (status: {session['status']}).",
        )

    # Ensure eval_result is populated
    if not session.get("eval_result"):
        db = get_supabase()
        events_resp = (
            db.schema("telos_sdc")
            .table("round_events")
            .select("*")
            .eq("session_id", session_id)
            .order("round_number")
            .execute()
        )
        events = events_resp.data or []
        indicators = evaluate_session(
            session=session,
            round_events=events,
            mission_id=session["mission_id"],
        )
        _update_session(session_id, {"eval_result": indicators})
        session["eval_result"] = indicators

    indicators = session["eval_result"]
    roles = match_from_session(session, indicators)

    return {
        "session_id": session_id,
        "mission": session["mission_id"],
        "roles": roles,
        "data_source": "ESCO v1.2 (2023) + Behavioral Evaluation",
        "data_date": "2023-06-01",
        "guardrail": (
            "This profile is based on one simulation session. "
            "It is a directional signal, not a professional assessment."
        ),
    }


@router.get("/game/pathway/{role_id}")
def get_pathway(
    role_id: str,
    session_id: str = Query(..., description="Session ID to load skill gaps from"),
    scenario: str = Query("moderate", description="'moderate' or 'rapid'"),
):
    """
    GET /api/game/pathway/{role_id}?session_id={uuid}&scenario=moderate|rapid

    Feature 05 — Future Career Pathway.
    Returns a sequential reskilling path built from skill gaps identified in F04.
    Two scenarios: Moderate (core gaps first) vs Rapid (judgment/governance skills up-ranked).
    All time estimates are labeled as estimates, not predictions.
    """
    if scenario not in ("moderate", "rapid"):
        raise HTTPException(status_code=422, detail="scenario must be 'moderate' or 'rapid'")

    # Find the role definition
    role_def = next((r for r in MVP_ROLES if r["id"] == role_id), None)
    if not role_def:
        valid_ids = [r["id"] for r in MVP_ROLES]
        raise HTTPException(
            status_code=404,
            detail=f"Role '{role_id}' not found. Valid IDs: {valid_ids}",
        )

    # Load session for skill gap context
    session = _get_session(session_id)
    if session["status"] != "complete":
        raise HTTPException(
            status_code=400,
            detail="Session must be complete before generating a pathway.",
        )

    # Get skill gaps — recompute match to get filtered gaps for this role
    indicators = session.get("eval_result") or {}
    roles = match_from_session(session, indicators)
    role_match = next((r for r in roles if r["id"] == role_id), None)

    if not role_match:
        # Fallback: use full template gaps
        skill_gaps = role_def["skill_gaps_template"]
    else:
        skill_gaps = role_match.get("skill_gaps") or role_def["skill_gaps_template"]

    pathway = build_pathway(
        role_id=role_id,
        skill_gaps=skill_gaps,
        scenario=scenario,
    )

    return {
        "role_id": role_id,
        "role_title": role_def["title"],
        "session_id": session_id,
        **pathway,
    }
