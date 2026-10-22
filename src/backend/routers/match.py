"""
routers/match.py -- GET /api/match  (Feature 3 -- Role Matching + Skill Gap)
Owner: Person A (Backend Lead) -- Substep 3.5

Flow:
  1. Load user profile from telos_sdc.user_profiles
  2. Call telos_sdc.hybrid_search(dense_vector, sparse_vector) -> ranked role_ids  [RRF]
  3. Compute weighted score: 0.5*RRF + 0.3*HardSkillCoverage + 0.2*SeniorityMatch
  4. Compute skill gap: role_required_skills minus user.hard_skills  (Set Difference)
  5. JOIN role_sdg -> append sdg_alignment[]
  6. Return top-k results

Substep status:
  Done 3.3 Weighted scoring formula ready
  Done 3.4 Skill gap set difference ready
  Wait 3.2 hybrid_search() -- waits for role_vectors (Person B RunPod BGE-M3)
  Wait 5.3 SDG JOIN -- waits for role_sdg seeded (Person C Substep 5.2)
"""

from __future__ import annotations
import json
from typing import Literal
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from backend.db import get_supabase

router = APIRouter()

# ── Response Models ──────────────────────────────────────────────────────────

class SkillGapItem(BaseModel):
    skill:   str
    esco_id: str
    type:    Literal["core", "supporting"]
    urgency: Literal["high", "medium", "low"]

class ScoreBreakdown(BaseModel):
    rrf_score:           float
    hard_skill_coverage: float
    seniority_match:     float

class SdgAlignment(BaseModel):
    sdg_goal:         int
    sdg_name:         str
    target:           str | None
    impact_reasoning: str
    source:           str
    color_hex:        str | None = None

class MatchResult(BaseModel):
    target_role:     str
    esco_id:         str
    match_score:     float
    score_breakdown: ScoreBreakdown
    skills_gap:      list[SkillGapItem]
    sdg_alignment:   list[SdgAlignment]
    ctci_score:      float | None = None          # Phase 3 — Person E fills
    compression_type: str | None  = None          # Phase 3

class MatchResponse(BaseModel):
    user_id:  str
    scenario: str
    results:  list[MatchResult]

# ── Helpers ──────────────────────────────────────────────────────────────────

SENIORITY_BANDS = {
    "junior":   (0, 2),
    "mid":      (3, 5),
    "senior":   (6, 10),
    "lead":     (11, 99),
}

def seniority_match(user_years: int, role_esco_id: str) -> float:
    """
    Simple heuristic: infer expected seniority from ESCO occupation label.
    Returns 0.0–1.0 (1.0 = perfect match).
    Phase 2: replace with proper seniority_band column on occupations table.
    """
    if user_years <= 2:
        expected = "junior"
    elif user_years <= 5:
        expected = "mid"
    elif user_years <= 10:
        expected = "senior"
    else:
        expected = "lead"
    # Placeholder: all roles score 0.7 until DB has seniority band column
    return 0.7


def compute_hard_skill_coverage(
    user_skill_ids: set[str],
    role_id: str,
    db,
) -> tuple[float, list[dict]]:
    """
    Hard Skill Coverage = |essential_role_skills ∩ user_skills| / |essential_role_skills|
    Also returns skill gap list (T \\ U).
    """
    resp = (
        db.schema("telos_sdc")
        .table("role_required_skills")
        .select("skill_id, is_essential, weight, skills(preferred_label)")
        .eq("role_id", role_id)
        .execute()
    )
    required = resp.data or []

    essential     = [r for r in required if r["is_essential"]]
    supporting    = [r for r in required if not r["is_essential"]]
    essential_ids = {r["skill_id"] for r in essential}

    covered = essential_ids & user_skill_ids
    coverage = len(covered) / len(essential_ids) if essential_ids else 1.0

    # Build skill gap list
    gap: list[dict] = []
    for r in essential:
        if r["skill_id"] not in user_skill_ids:
            gap.append({
                "skill":   r["skills"]["preferred_label"] if r.get("skills") else r["skill_id"],
                "esco_id": r["skill_id"],
                "type":    "core",
                "urgency": "high",
            })
    for r in supporting:
        if r["skill_id"] not in user_skill_ids:
            gap.append({
                "skill":   r["skills"]["preferred_label"] if r.get("skills") else r["skill_id"],
                "esco_id": r["skill_id"],
                "type":    "supporting",
                "urgency": "medium",
            })

    return coverage, gap


def get_sdg_alignment(role_id: str, db) -> list[dict]:
    """JOIN role_sdg -> sdg_goals. Returns [] until Person C seeds role_sdg table."""
    resp = (
        db.schema("telos_sdc")
        .table("role_sdg")
        .select("sdg_goal, sdg_goals(title, color_hex), sdg_target, impact_reasoning, source")
        .eq("role_id", role_id)
        .execute()
    )
    results = []
    for row in (resp.data or []):
        results.append({
            "sdg_goal":        row["sdg_goal"],
            "sdg_name":        row.get("sdg_goals", {}).get("title", "") if row.get("sdg_goals") else "",
            "target":          row.get("sdg_target"),
            "impact_reasoning": row.get("impact_reasoning", ""),
            "source":          row.get("source", "UNSD SDG API"),
            "color_hex":       row.get("sdg_goals", {}).get("color_hex") if row.get("sdg_goals") else None,
        })
    return results


def apply_disruption_penalty(score: float, role_onet_code: str, db) -> float:
    """
    Phase 3 — Person E populates occupation_disruption_matrix.
    Until then, returns score unchanged (scenario=fast has no effect).
    """
    resp = (
        db.schema("telos_sdc")
        .table("occupation_disruption_matrix")
        .select("disruption_penalty_fast")
        .eq("onet_soc_code", role_onet_code)
        .maybe_single()
        .execute()
    )
    if resp.data:
        penalty = resp.data.get("disruption_penalty_fast", 0.0)
        score = score * (1.0 - penalty)
    return round(score, 4)


# ── Main Endpoint ─────────────────────────────────────────────────────────────

@router.get("/match", response_model=MatchResponse)
def get_match(
    user_id:  str = Query(..., description="UUID of the user profile"),
    scenario: Literal["moderate", "fast"] = Query("moderate"),
    top_k:    int = Query(5, ge=1, le=20),
):
    """
    GET /api/match?user_id=<uuid>&scenario=moderate&top_k=5

    Returns ranked role recommendations with match score, skill gap,
    and SDG alignment for the given user profile.

    Substep 3.5 — Owner: Person A
    """
    db = get_supabase()

    # ── 1. Load user profile ─────────────────────────────────────────────
    profile_resp = (
        db.schema("telos_sdc")
        .table("user_profiles")
        .select("id, hard_skills, soft_skills, experience_years, user_dense_vector, user_sparse_vector")
        .eq("id", user_id)
        .maybe_single()
        .execute()
    )
    if not profile_resp.data:
        raise HTTPException(status_code=404, detail=f"User profile {user_id!r} not found")

    profile      = profile_resp.data
    experience   = profile.get("experience_years", 0)
    hard_skills  = profile.get("hard_skills") or []
    user_skill_ids = {s["esco_id"] for s in hard_skills if s.get("esco_id")}

    dense_vec  = profile.get("user_dense_vector")
    sparse_vec = profile.get("user_sparse_vector")

    # ── 2. Hybrid Search (RRF) ───────────────────────────────────────────
    # ⏳ Waits for: Person B RunPod BGE-M3 vectors + role_vectors populated
    if dense_vec and sparse_vec:
        rrf_resp = db.rpc(
            "telos_sdc.hybrid_search",
            {"query_dense": dense_vec, "query_sparse": sparse_vec, "k": top_k * 3},
        ).execute()
        rrf_rows = rrf_resp.data or []
    else:
        # Fallback Candidate Selection:
        # Match candidate roles that require the user's hard skills
        rrf_rows = []
        if user_skill_ids:
            from collections import Counter
            rrs_resp = (
                db.schema("telos_sdc")
                .table("role_required_skills")
                .select("role_id")
                .in_("skill_id", list(user_skill_ids))
                .execute()
            )
            if rrs_resp.data:
                counts = Counter(r["role_id"] for r in rrs_resp.data)
                top_matched = counts.most_common(top_k * 3)
                max_matches = max(c for _, c in top_matched) if top_matched else 1
                rrf_rows = [
                    {"role_id": r_id, "rrf_score": round(0.4 + 0.6 * (count / max_matches), 4)}
                    for r_id, count in top_matched
                ]

        # If no skill match found or profile has no skills, fall back to sample
        if not rrf_rows:
            occ_resp = (
                db.schema("telos_sdc")
                .table("occupations")
                .select("esco_id, preferred_label, onet_soc_code")
                .limit(top_k * 3)
                .execute()
            )
            rrf_rows = [
                {"role_id": r["esco_id"], "rrf_score": 0.5}
                for r in (occ_resp.data or [])
            ]

    if not rrf_rows:
        return MatchResponse(user_id=user_id, scenario=scenario, results=[])

    # ── 3-4. Score + Skill Gap per role ──────────────────────────────────
    results: list[MatchResult] = []

    # Fetch occupation labels in one query
    role_ids = [r["role_id"] for r in rrf_rows]
    occ_resp = (
        db.schema("telos_sdc")
        .table("occupations")
        .select("esco_id, preferred_label, onet_soc_code")
        .in_("esco_id", role_ids)
        .execute()
    )
    occ_map = {o["esco_id"]: o for o in (occ_resp.data or [])}

    for rrf_row in rrf_rows:
        role_id   = rrf_row["role_id"]
        rrf_score = float(rrf_row["rrf_score"])
        occ       = occ_map.get(role_id, {})

        hard_skill_cov, skill_gap = compute_hard_skill_coverage(
            user_skill_ids, role_id, db
        )
        sen_score = seniority_match(experience, role_id)

        # Weighted composite score (Substep 3.3)
        # Final Score = 0.5*RRF + 0.3*HardSkillCoverage + 0.2*SeniorityMatch
        composite = (0.5 * rrf_score) + (0.3 * hard_skill_cov) + (0.2 * sen_score)

        # Phase 3: apply disruption penalty for scenario=fast
        if scenario == "fast":
            composite = apply_disruption_penalty(
                composite, occ.get("onet_soc_code", ""), db
            )

        # SDG alignment JOIN (Substep 5.3) — empty until Person C seeds role_sdg
        sdg = get_sdg_alignment(role_id, db)

        results.append(MatchResult(
            target_role=occ.get("preferred_label", role_id),
            esco_id=role_id,
            match_score=round(composite, 4),
            score_breakdown=ScoreBreakdown(
                rrf_score=round(rrf_score, 4),
                hard_skill_coverage=round(hard_skill_cov, 4),
                seniority_match=round(sen_score, 4),
            ),
            skills_gap=[SkillGapItem(**g) for g in skill_gap],
            sdg_alignment=[SdgAlignment(**s) for s in sdg],
        ))

    # Sort by composite score descending, return top_k
    results.sort(key=lambda x: x.match_score, reverse=True)
    return MatchResponse(
        user_id=user_id,
        scenario=scenario,
        results=results[:top_k],
    )
