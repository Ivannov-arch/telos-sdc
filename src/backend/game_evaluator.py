"""
game_evaluator.py — Behavioral Skill Evaluator for FutureProof Crisis Simulation
Feature 03 — Decision & Skill Report

Design:
  - Batches R1 + R3 free-text evaluation into ONE LLM call after R4 completes
  - Returns structured JSON (booleans + evidence strings) — rubric is hardcoded
  - Falls back to deterministic keyword + event-log scoring if no LLM configured
  - LLM only fills evidence strings and observed booleans; final scores derived from booleans

The player NEVER sees this running during gameplay. The rubric is hidden until The Reveal.

Supported LLM providers (set one in .env):
  OPENAI_API_KEY       → uses gpt-4o-mini (cost-effective, structured output)
  GEMINI_API_KEY       → uses gemini-1.5-flash
  RUNPOD_LLM_URL       → uses vLLM endpoint (existing RunPod infra)
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

# ── Indicator Schema ───────────────────────────────────────────────────────────

INDICATOR_KEYS = [
    "calibrated_ai_trust",
    "critical_verification",
    "decision_quality",
    "adaptability",
]

EMPTY_INDICATORS: dict = {
    "calibrated_ai_trust": {"observed": None, "evidence": ""},
    "critical_verification": {"observed": None, "evidence": ""},
    "decision_quality": {"met_objectives": None, "note": ""},
    "adaptability": {"observed": None, "evidence": ""},
}

# Mission-specific rubric context for the LLM evaluator
MISSION_CONTEXT = {
    "A": (
        "Food supply chain collapse in Southeast Asia. "
        "Key constraints: limited budget, route capacity limits, population reach."
    ),
    "B": (
        "Credit algorithm bias causing systemic loan denial. "
        "Key constraints: regulatory compliance, customer impact, timeline."
    ),
    "C": (
        "Green energy grid failure. "
        "Key constraints: population affected, secondary failure risk, restoration time."
    ),
}

# Mission-specific keywords for deterministic fallback
MISSION_KEYWORDS = {
    "A": {
        "critical_verification": ["capacity", "data", "verify", "check", "confirm", "vetting", "unverified"],
        "decision_quality": ["route", "distribution", "budget", "population", "reach", "priority"],
        "ai_trust_skeptical": ["not sure", "verify", "check", "unverified", "concerned", "question", "data first"],
        "adaptability": ["changed", "revised", "updated", "different", "instead", "new approach", "shift", "volunteer"],
    },
    "B": {
        "critical_verification": ["verified", "authentic", "legal", "confirm", "validate", "source", "legitimacy"],
        "decision_quality": ["regulation", "compliance", "fix", "root cause", "bias", "customers", "legal"],
        "ai_trust_skeptical": ["verify", "check source", "authenticate", "not confirmed", "legally", "caution"],
        "adaptability": ["changed", "new regulation", "different approach", "revised", "reconsidered", "whistleblower"],
    },
    "C": {
        "critical_verification": ["stability", "integrity", "check", "verified", "inspection", "data", "review"],
        "decision_quality": ["restore", "hospital", "emergency", "population", "risk", "failure", "capacity"],
        "ai_trust_skeptical": ["verify", "check stability", "outdated data", "unconfirmed", "risk of failure"],
        "adaptability": ["northern line", "changed", "different route", "revised", "shifted", "emergency", "doubled"],
    },
}


# ── LLM Evaluators ─────────────────────────────────────────────────────────────


def _build_eval_prompt(r1_text: str, r3_text: str, mission_id: str) -> str:
    mission_ctx = MISSION_CONTEXT.get(mission_id, "")
    return f"""You are a silent behavioral analyst for a crisis simulation game.
The player does NOT know they are being evaluated on these criteria.
Evaluate both responses and return ONLY valid JSON matching the schema below.
Do not invent evidence. Extract only what is present in the text.

Schema (return this exact structure):
{{
  "calibrated_ai_trust": {{
    "observed": <true|false>,
    "evidence": "<direct quote or paraphrase showing whether player questioned or blindly followed AI>"
  }},
  "critical_verification": {{
    "observed": <true|false>,
    "evidence": "<direct quote or paraphrase showing whether player sought to verify before acting>"
  }},
  "decision_quality": {{
    "met_objectives": <true|false>,
    "note": "<one sentence: did the strategy address the mission constraints?>"
  }},
  "adaptability": {{
    "observed": <true|false>,
    "evidence": "<comparison between Round 1 and Round 3 showing whether strategy meaningfully shifted>"
  }}
}}

Mission context: {mission_ctx}

Round 1 response (player's initial strategy, written before seeing AI):
\"\"\"{r1_text}\"\"\"

Round 3 response (player's response to the AI Shock disruption event):
\"\"\"{r3_text}\"\"\"

Return ONLY the JSON object. No explanation, no markdown, no preamble."""


def _parse_llm_json(raw_output: str) -> dict | None:
    """Extract and validate JSON from LLM response."""
    match = re.search(r'\{.*\}', raw_output, re.DOTALL)
    if not match:
        return None
    try:
        parsed = json.loads(match.group(0))
        # Validate expected keys are present
        for key in INDICATOR_KEYS:
            if key not in parsed:
                return None
        return parsed
    except (json.JSONDecodeError, ValueError):
        return None


def _evaluate_with_openai(r1_text: str, r3_text: str, mission_id: str) -> dict | None:
    """Evaluate using OpenAI API (gpt-4o-mini for cost efficiency)."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key or "sk-" not in api_key:
        return None
    try:
        import httpx
        prompt = _build_eval_prompt(r1_text, r3_text, mission_id)
        resp = httpx.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0,
                "response_format": {"type": "json_object"},
            },
            timeout=30.0,
        )
        if resp.status_code == 200:
            content = resp.json()["choices"][0]["message"]["content"]
            return _parse_llm_json(content)
    except Exception:
        pass
    return None


def _evaluate_with_gemini(r1_text: str, r3_text: str, mission_id: str) -> dict | None:
    """Evaluate using Google Gemini Flash API."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
    try:
        import httpx
        prompt = _build_eval_prompt(r1_text, r3_text, mission_id)
        for model in ["gemini-2.5-flash", "gemini-flash-latest"]:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
            resp = httpx.post(
                url,
                json={"contents": [{"parts": [{"text": prompt}]}]},
                timeout=30.0,
            )
            if resp.status_code == 200:
                content = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
                parsed = _parse_llm_json(content)
                if parsed:
                    return parsed
    except Exception:
        pass
    return None


def _evaluate_with_runpod(r1_text: str, r3_text: str, mission_id: str) -> dict | None:
    """Evaluate using existing RunPod vLLM endpoint."""
    llm_url = os.environ.get("RUNPOD_LLM_ENDPOINT_URL") or os.environ.get("RUNPOD_LLM_URL")
    api_key = os.environ.get("RUNPOD_API_KEY")
    if not llm_url or "yyyyyyyy" in llm_url:
        return None
    try:
        import httpx
        headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
        prompt = _build_eval_prompt(r1_text, r3_text, mission_id)
        resp = httpx.post(
            llm_url,
            json={"input": {"prompt": prompt, "format": "json"}},
            headers=headers,
            timeout=30.0,
        )
        if resp.status_code == 200:
            data = resp.json()
            raw = data.get("output") or data
            if isinstance(raw, list) and raw:
                raw = raw[0].get("text") or raw[0].get("response") or str(raw[0])
            elif isinstance(raw, dict):
                raw = raw.get("text") or raw.get("response") or json.dumps(raw)
            return _parse_llm_json(str(raw))
    except Exception:
        pass
    return None


# ── Deterministic Fallback ─────────────────────────────────────────────────────


def _deterministic_evaluate(
    r1_text: str,
    r3_text: str,
    mission_id: str,
    round_events: list[dict],
) -> dict:
    """
    Fallback behavioral evaluation using keyword matching + event log signals.
    Used when no LLM API is configured. Results are less nuanced but deterministic.
    """
    kw = MISSION_KEYWORDS.get(mission_id, MISSION_KEYWORDS["A"])

    r1_lower = r1_text.lower() if r1_text else ""
    r3_lower = r3_text.lower() if r3_text else ""
    combined_lower = r1_lower + " " + r3_lower

    # --- Critical Verification ---
    # Primary signal: did player open evidence drawer in R2? (event log)
    r2_event = next((e for e in round_events if e.get("round_number") == 2), {})
    evidence_opened = r2_event.get("evidence_opened", False)
    r3_verify_keywords = any(kw in r3_lower for kw in kw["critical_verification"])

    critical_verification_observed = evidence_opened or r3_verify_keywords
    critical_verification_evidence = (
        "Evidence drawer was opened before the Round 2 decision." if evidence_opened
        else "Round 3 response contained verification-seeking language." if r3_verify_keywords
        else "No evidence of verification behaviour detected in event log or response text."
    )

    # --- Calibrated AI Trust ---
    # Did player show skepticism toward AI in R2 or R3?
    r2_trusted = r2_event.get("ai_trusted")  # False = rejected/verified (skeptical)
    r3_ai_skeptical = any(kw in r3_lower for kw in kw["ai_trust_skeptical"])

    calibrated_trust_observed = (r2_trusted is False) or r3_ai_skeptical
    calibrated_trust_evidence = (
        "Player did not blindly accept the AI recommendation in Round 2." if r2_trusted is False
        else "Round 3 response showed caution toward the AI-recommended unverified option." if r3_ai_skeptical
        else "Player accepted AI recommendations without apparent skepticism."
    )

    # --- Decision Quality ---
    quality_keywords = kw["decision_quality"]
    r1_quality_hits = sum(1 for kw_item in quality_keywords if kw_item in r1_lower)
    r4_event = next((e for e in round_events if e.get("round_number") == 4), {})
    r4_text = (r4_event.get("free_text") or "").lower()
    r4_quality_hits = sum(1 for kw_item in quality_keywords if kw_item in r4_text)

    met_objectives = (r1_quality_hits + r4_quality_hits) >= 2
    quality_note = (
        f"Strategy addressed {r1_quality_hits + r4_quality_hits} of {len(quality_keywords)} key mission constraints."
    )

    # --- Adaptability ---
    # Did R3 response meaningfully differ from R1?
    adapt_keywords = kw["adaptability"]
    r3_adaptation_hits = sum(1 for kw_item in adapt_keywords if kw_item in r3_lower)

    # Also check semantic divergence: very similar texts = anchoring, not adaptation
    r1_words = set(r1_lower.split())
    r3_words = set(r3_lower.split())
    overlap_ratio = (
        len(r1_words & r3_words) / max(len(r1_words | r3_words), 1)
    )
    adapted = r3_adaptation_hits >= 2 or overlap_ratio < 0.5

    adaptability_evidence = (
        "Round 3 strategy showed meaningful divergence from Round 1 approach." if adapted
        else "Round 3 strategy closely mirrored Round 1, suggesting anchoring to initial plan despite new conditions."
    )

    return {
        "calibrated_ai_trust": {
            "observed": calibrated_trust_observed,
            "evidence": calibrated_trust_evidence,
        },
        "critical_verification": {
            "observed": critical_verification_observed,
            "evidence": critical_verification_evidence,
        },
        "decision_quality": {
            "met_objectives": met_objectives,
            "note": quality_note,
        },
        "adaptability": {
            "observed": adapted,
            "evidence": adaptability_evidence,
        },
    }


# ── Main Entry Point ───────────────────────────────────────────────────────────


def evaluate_session(
    session: dict,
    round_events: list[dict],
    mission_id: str,
) -> dict:
    """
    Evaluate a completed game session.
    Tries LLM providers in order: OpenAI → Gemini → RunPod → Deterministic fallback.

    Called by GET /api/game/{session_id}/report after all 4 rounds are complete.
    Result is cached in game_sessions.eval_result to avoid duplicate LLM calls.
    """
    # Extract R1 and R3 free-text from round events or session.rounds
    rounds = session.get("rounds") or []
    r1_text = next(
        (r.get("free_text") or "" for r in rounds if r.get("round") == 1), ""
    )
    r3_text = next(
        (r.get("free_text") or "" for r in rounds if r.get("round") == 3), ""
    )

    # Guard: if either free-text round is missing/too short, mark as insufficient
    if len(r1_text.strip()) < 10:
        r1_text = "[insufficient evidence — Round 1 response too short]"
    if len(r3_text.strip()) < 10:
        r3_text = "[insufficient evidence — Round 3 response too short]"

    # Try LLM providers in order
    llm_result = (
        _evaluate_with_openai(r1_text, r3_text, mission_id)
        or _evaluate_with_gemini(r1_text, r3_text, mission_id)
        or _evaluate_with_runpod(r1_text, r3_text, mission_id)
    )

    if llm_result:
        # Add evaluation method tag for transparency
        llm_result["_evaluated_by"] = "llm"
        return llm_result

    # Fallback: deterministic keyword + event-log scoring
    result = _deterministic_evaluate(r1_text, r3_text, mission_id, round_events)
    result["_evaluated_by"] = "deterministic_fallback"
    return result
