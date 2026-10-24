"""
routers/profile.py — Feature 1: Skills Profile Intake & CV Parser
Owner: Person B (AI/ML Engineer) — Substeps 1.2, 1.3, 1.4

Flow:
  1. Intake CV via PDF upload (pdfplumber) or manual JSON form.
  2. Extract structured fields: hard_skills, soft_skills, experience_years.
  3. Resolve skills against ESCO skills taxonomy in Supabase (telos_sdc.skills).
  4. Generate user_dense_vector (1024-dim) via RunPod BGE-M3 serverless endpoint.
  5. Persist profile to telos_sdc.user_profiles and return structured JSON with profile UUID.
"""

from __future__ import annotations

import io
import os
import re
import logging
from typing import Literal, Optional
from functools import lru_cache

import requests
import pdfplumber
from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile, status
from pydantic import BaseModel, Field

from backend.db import get_supabase

logger = logging.getLogger("profile_router")
router = APIRouter()

MAX_PDF_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB cap per WORKSTEPS.md / TASKS.md

RUNPOD_API_KEY = os.getenv("RUNPOD_API_KEY", "")
RUNPOD_BGE_M3_URL = os.getenv("RUNPOD_BGE_M3_URL", "")


# ── Pydantic Schemas (Substep 1.3) ──────────────────────────────────────────

class SkillEntry(BaseModel):
    skill_name: str = ""
    label: str | None = None
    esco_id: Optional[str] = None          # None if confidence is below threshold
    confidence_score: float = 0.0          # 0.0 – 1.0

    def model_post_init(self, __context):
        if not self.label and self.skill_name:
            self.label = self.skill_name
        elif not self.skill_name and self.label:
            self.skill_name = self.label
        elif not self.skill_name and not self.label:
            self.skill_name = "Skill"
            self.label = "Skill"


class ProfileFormRequest(BaseModel):
    hard_skills: list[str] = Field(default_factory=list, description="List of technical/hard skill names")
    soft_skills: list[str] = Field(default_factory=list, description="List of soft skill names")
    experience_years: int = Field(default=0, ge=0, le=70, description="Years of professional experience")
    raw_text: Optional[str] = Field(default=None, description="Optional raw text or resume summary")


class UserProfileResponse(BaseModel):
    id: str = Field(..., description="UUID in telos_sdc.user_profiles")
    hard_skills: list[SkillEntry]
    soft_skills: list[SkillEntry]
    experience_years: int
    source_type: Literal["pdf", "form"]
    has_dense_vector: bool = False
    message: str = "Profile processed and saved successfully"


# ── Common Soft Skills Taxonomy ─────────────────────────────────────────────

COMMON_SOFT_SKILLS = {
    "communication", "verbal communication", "written communication",
    "leadership", "team leadership", "management", "stakeholder management",
    "teamwork", "collaboration", "cross-functional collaboration",
    "problem solving", "critical thinking", "analytical thinking",
    "adaptability", "flexibility", "resilience",
    "time management", "organization", "multitasking",
    "presentation", "public speaking", "active listening",
    "negotiation", "conflict resolution", "mentoring", "coaching",
    "emotional intelligence", "interpersonal skills", "attention to detail",
    "creativity", "work ethic", "decision making"
}


# ── ESCO Skill Resolver with In-Memory Caching ──────────────────────────────

@lru_cache(maxsize=1024)
def _resolve_single_skill_cached(skill_name: str) -> tuple[Optional[str], float, Optional[str]]:
    """
    Look up skill in Supabase telos_sdc.skills.
    Returns (esco_id, confidence_score, canonical_label).
    """
    clean_name = skill_name.strip()
    if not clean_name:
        return None, 0.0, None

    db = get_supabase()

    # 1. Exact match on preferred_label (case-insensitive)
    try:
        r1 = (
            db.schema("telos_sdc")
            .table("skills")
            .select("esco_id, preferred_label, skill_type")
            .ilike("preferred_label", clean_name)
            .limit(1)
            .execute()
        )
        if r1.data:
            return r1.data[0]["esco_id"], 0.98, r1.data[0]["preferred_label"]
    except Exception as e:
        logger.warning(f"Error in exact skill lookup for {clean_name}: {e}")

    # 2. Contains match on preferred_label
    try:
        r2 = (
            db.schema("telos_sdc")
            .table("skills")
            .select("esco_id, preferred_label, skill_type")
            .ilike("preferred_label", f"%{clean_name}%")
            .limit(1)
            .execute()
        )
        if r2.data:
            return r2.data[0]["esco_id"], 0.85, r2.data[0]["preferred_label"]
    except Exception as e:
        logger.warning(f"Error in contains skill lookup for {clean_name}: {e}")

    # 3. Low confidence / not matched in ESCO -> do NOT force hallucinated ID
    return None, 0.0, clean_name


def resolve_skills(skill_names: list[str]) -> list[SkillEntry]:
    """Resolve a list of skill strings into SkillEntry models with ESCO IDs and confidence."""
    entries: list[SkillEntry] = []
    seen = set()

    for name in skill_names:
        clean = name.strip()
        if not clean or clean.lower() in seen:
            continue
        seen.add(clean.lower())

        esco_id, confidence, canonical_label = _resolve_single_skill_cached(clean)
        entries.append(
            SkillEntry(
                skill_name=clean,
                label=canonical_label or clean,
                esco_id=esco_id,
                confidence_score=confidence,
            )
        )
    return entries


# ── PDF Parser via pdfplumber (Substep 1.2) ─────────────────────────────────

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Extract text using pdfplumber with pure-Python layout preservation
    handling multi-column resume formats without AGPL licensing issues.
    """
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            pages_text = []
            for page in pdf.pages:
                text = page.extract_text() or ""
                if text.strip():
                    pages_text.append(text.strip())
            return "\n\n".join(pages_text)
    except Exception as e:
        logger.error(f"pdfplumber extraction error: {e}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Failed to extract text from PDF: {str(e)}",
        )


def parse_cv_text_to_profile(text: str) -> tuple[list[str], list[str], int]:
    """
    NER / Rule-based extraction from CV text:
    - Extracts experience years
    - Identifies hard skills and soft skills
    """
    # 1. Experience Years Detection
    years = 0
    # Pattern a: "X years of experience" or "over X years"
    exp_match = re.search(
        r"(?:over\s+|more\s+than\s+)?(\d{1,2})\+?\s*(?:years?|yrs?)(?:\s+of)?\s+(?:experience|exp|in\b)",
        text,
        re.IGNORECASE,
    )
    if exp_match:
        try:
            years = int(exp_match.group(1))
        except ValueError:
            pass

    # Pattern b: Date ranges e.g. 2018 - 2024
    if years == 0:
        year_spans = re.findall(r"\b(20\d{2}|19\d{2})\s*[-–—to]+\s*(20\d{2}|present|current)\b", text, re.IGNORECASE)
        total_span = 0
        current_year = 2026
        for start_str, end_str in year_spans:
            try:
                start = int(start_str)
                end = current_year if end_str.lower() in ("present", "current") else int(end_str)
                diff = end - start
                if 0 <= diff <= 40:
                    total_span += diff
            except ValueError:
                continue
        if total_span > 0:
            years = min(total_span, 40)

    # 2. Extract Skills Section and Keywords
    raw_hard_skills: list[str] = []
    raw_soft_skills: list[str] = []

    # Look for common skills header section
    skills_section_match = re.search(
        r"(?:SKILLS|TECHNICAL SKILLS|CORE COMPETENCIES|EXPERTISE|TECHNOLOGIES|TOOLS|PROFICIENCIES)[:\n](.*?)(?=(?:EXPERIENCE|WORK EXPERIENCE|EDUCATION|PROJECTS|CERTIFICATIONS|\Z))",
        text,
        re.IGNORECASE | re.DOTALL,
    )
    section_text = skills_section_match.group(1) if skills_section_match else text

    # Split lines and tokens by delimiters (, • | ; / \n)
    tokens = re.split(r"[,•|\n;/\t]+", section_text)
    for tok in tokens:
        clean = tok.strip()
        # Clean leading header names if prefixed on the same line
        clean = re.sub(
            r"^(?:soft\s+skills?|technical\s+skills?|hard\s+skills?|core\s+skills?|skills?|proficiencies|technologies|tools|competencies)[:\s-]*",
            "",
            clean,
            flags=re.IGNORECASE,
        ).strip()
        # Clean leading dashes or bullets
        clean = re.sub(r"^[-*•–—\d\.]+\s*", "", clean).strip()
        if not clean or len(clean) < 2 or len(clean) > 40:
            continue
        # Avoid common section headers or sentences
        if any(h in clean.lower() for h in ["experience", "education", "project", "university", "responsible for"]):
            continue

        lower = clean.lower()
        if lower in COMMON_SOFT_SKILLS or any(s in lower for s in ["communication", "leadership", "management", "teamwork"]):
            raw_soft_skills.append(clean)
        else:
            raw_hard_skills.append(clean)

    # Also scan full text for ubiquitous high-impact technical keywords
    known_tech = [
        "Python", "SQL", "Machine Learning", "Deep Learning", "Data Analysis",
        "Data Engineering", "Apache Spark", "Docker", "Kubernetes", "AWS",
        "PostgreSQL", "React", "TypeScript", "JavaScript", "FastAPI",
        "Git", "Linux", "PyTorch", "TensorFlow", "Tableau", "Power BI",
        "CI/CD", "ETL", "NoSQL", "Java", "C++", "Go", "NLP"
    ]
    for tech in known_tech:
        pattern = r"\b" + re.escape(tech) + r"\b"
        if re.search(pattern, text, re.IGNORECASE) and not any(tech.lower() == h.lower() for h in raw_hard_skills):
            raw_hard_skills.append(tech)

    return raw_hard_skills, raw_soft_skills, years


# ── RunPod BGE-M3 Vector Generation ─────────────────────────────────────────

def build_profile_text(hard_skills: list[SkillEntry], soft_skills: list[SkillEntry], years: int, raw_text: str | None = None) -> str:
    """Format skills and experience into natural text for BGE-M3 embedding."""
    if raw_text and len(raw_text.strip()) > 50:
        return raw_text.strip()[:2000]

    hard_labels = [s.label or s.skill_name for s in hard_skills]
    soft_labels = [s.label or s.skill_name for s in soft_skills]

    parts = []
    if hard_labels:
        parts.append(f"Hard skills: {', '.join(hard_labels)}")
    if soft_labels:
        parts.append(f"Soft skills: {', '.join(soft_labels)}")
    if years:
        parts.append(f"Experience: {years} years")

    return ". ".join(parts) if parts else "Professional skilled worker"


# In-memory vector cache to prevent duplicate RunPod serverless calls (Budget Guard)
_EMBEDDING_CACHE: dict[str, list[float]] = {}


def generate_user_embeddings_batch(texts: list[str], batch_size: int = 32) -> list[Optional[list[float]]]:
    """
    Batched and cached vector generation for multiple texts via RunPod BGE-M3.
    Checks memory cache first, batches uncached texts up to batch_size per request,
    and caches results to prevent duplicate serverless billing.
    """
    if not texts:
        return []

    results: list[Optional[list[float]]] = [None] * len(texts)
    uncached_indices: list[int] = []
    uncached_texts: list[str] = []

    for i, t in enumerate(texts):
        cleaned = t.strip()
        if cleaned in _EMBEDDING_CACHE:
            results[i] = _EMBEDDING_CACHE[cleaned]
        else:
            uncached_indices.append(i)
            uncached_texts.append(cleaned)

    if not uncached_texts:
        return results

    if not RUNPOD_BGE_M3_URL or not RUNPOD_API_KEY:
        logger.warning("RUNPOD_BGE_M3_URL or RUNPOD_API_KEY not set; skipping vector generation")
        return results

    headers = {
        "Authorization": f"Bearer {RUNPOD_API_KEY}",
        "Content-Type": "application/json",
    }

    for chunk_start in range(0, len(uncached_texts), batch_size):
        chunk_texts = uncached_texts[chunk_start : chunk_start + batch_size]
        chunk_indices = uncached_indices[chunk_start : chunk_start + batch_size]
        payload = {
            "input": {
                "model": "BAAI/bge-m3",
                "input": chunk_texts,
            }
        }

        try:
            resp = requests.post(RUNPOD_BGE_M3_URL, headers=headers, json=payload, timeout=60)
            resp.raise_for_status()
            res_json = resp.json()
            output = res_json.get("output", res_json)

            vectors: list[Optional[list[float]]] = []
            if isinstance(output, dict) and "data" in output:
                items = output["data"]
                items.sort(key=lambda x: x.get("index", 0))
                vectors = [item.get("embedding") for item in items]
            elif isinstance(output, list):
                vectors = output

            for idx, text_val, vec in zip(chunk_indices, chunk_texts, vectors):
                if vec:
                    _EMBEDDING_CACHE[text_val] = vec
                    results[idx] = vec

        except Exception as e:
            logger.error(f"RunPod BGE-M3 batch vector generation failed for chunk {chunk_start}: {e}")

    return results


def generate_user_embedding(text: str) -> Optional[list[float]]:
    """Call RunPod BGE-M3 serverless endpoint to produce 1024-dim dense vector (cached & batched)."""
    res = generate_user_embeddings_batch([text])
    return res[0] if res else None


# ── DB Persistence Helper ───────────────────────────────────────────────────

def save_user_profile(
    hard_skills: list[SkillEntry],
    soft_skills: list[SkillEntry],
    experience_years: int,
    source_type: Literal["pdf", "form"],
    raw_text: Optional[str] = None,
    dense_vector: Optional[list[float]] = None,
) -> str:
    """Insert profile into telos_sdc.user_profiles and return generated UUID."""
    db = get_supabase()

    row = {
        "hard_skills": [s.model_dump() for s in hard_skills],
        "soft_skills": [s.model_dump() for s in soft_skills],
        "experience_years": experience_years,
        "raw_cv_text": raw_text[:5000] if raw_text else None,
        "source_type": source_type,
        "is_synthetic": False,
        "user_dense_vector": dense_vector,
    }

    resp = db.schema("telos_sdc").table("user_profiles").insert(row).execute()
    if not resp.data:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to persist user profile into database",
        )
    return resp.data[0]["id"]


# ── Endpoints ────────────────────────────────────────────────────────────────

@router.post("/profile/upload", response_model=UserProfileResponse)
async def upload_profile_pdf(file: UploadFile = File(...)):
    """
    POST /api/profile/upload
    Accepts a PDF resume (<=5MB), parses via pdfplumber, resolves ESCO skills,
    computes BGE-M3 dense vector, and persists profile to database.
    """
    if file.content_type and "pdf" not in file.content_type.lower() and not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file format. Only PDF files are accepted.",
        )

    pdf_bytes = await file.read()
    if len(pdf_bytes) > MAX_PDF_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds maximum allowed size of 5MB (got {len(pdf_bytes)} bytes).",
        )

    # 1. Extract raw text with pdfplumber
    raw_text = extract_text_from_pdf(pdf_bytes)
    if not raw_text.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No readable text found in PDF. Scanned images without OCR are not supported.",
        )

    # 2. Extract skills and experience years
    raw_hard, raw_soft, years = parse_cv_text_to_profile(raw_text)

    # 3. Resolve ESCO IDs and confidence scores
    resolved_hard = resolve_skills(raw_hard)
    resolved_soft = resolve_skills(raw_soft)

    # 4. Generate BGE-M3 dense vector
    profile_text = build_profile_text(resolved_hard, resolved_soft, years, raw_text)
    dense_vec = generate_user_embedding(profile_text)

    # 5. Persist profile
    profile_id = save_user_profile(
        hard_skills=resolved_hard,
        soft_skills=resolved_soft,
        experience_years=years,
        source_type="pdf",
        raw_text=raw_text,
        dense_vector=dense_vec,
    )

    return UserProfileResponse(
        id=profile_id,
        hard_skills=resolved_hard,
        soft_skills=resolved_soft,
        experience_years=years,
        source_type="pdf",
        has_dense_vector=dense_vec is not None,
        message="PDF resume successfully parsed, embedded, and saved",
    )


@router.post("/profile", response_model=UserProfileResponse)
async def create_profile_or_upload(request: Request):
    """
    POST /api/profile
    Dual-mode endpoint (per TASKS.md Substep 1.3):
    - Accepts multipart/form-data with PDF file
    - OR application/json with manual skills form data
    """
    content_type = request.headers.get("content-type", "")

    # Mode A: Multipart / File Upload
    if "multipart/form-data" in content_type:
        form = await request.form()
        uploaded_file = form.get("file")
        if not uploaded_file or not hasattr(uploaded_file, "read"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Form-data must include a 'file' field containing the PDF.",
            )
        return await upload_profile_pdf(uploaded_file)

    # Mode B: JSON Payload (Manual form entry)
    try:
        body_dict = await request.json()
        form_req = ProfileFormRequest(**body_dict)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid JSON request body: {str(e)}",
        )

    # Resolve skills against ESCO
    resolved_hard = resolve_skills(form_req.hard_skills)
    resolved_soft = resolve_skills(form_req.soft_skills)

    # Generate vector
    profile_text = build_profile_text(resolved_hard, resolved_soft, form_req.experience_years, form_req.raw_text)
    dense_vec = generate_user_embedding(profile_text)

    # Persist
    profile_id = save_user_profile(
        hard_skills=resolved_hard,
        soft_skills=resolved_soft,
        experience_years=form_req.experience_years,
        source_type="form",
        raw_text=form_req.raw_text,
        dense_vector=dense_vec,
    )

    return UserProfileResponse(
        id=profile_id,
        hard_skills=resolved_hard,
        soft_skills=resolved_soft,
        experience_years=form_req.experience_years,
        source_type="form",
        has_dense_vector=dense_vec is not None,
        message="Manual profile successfully processed, embedded, and saved",
    )


@router.get("/profile/{user_id}", response_model=UserProfileResponse)
def get_user_profile(user_id: str):
    """
    GET /api/profile/{user_id}
    Retrieve a saved profile by UUID.
    """
    db = get_supabase()
    resp = (
        db.schema("telos_sdc")
        .table("user_profiles")
        .select("id, hard_skills, soft_skills, experience_years, source_type, user_dense_vector")
        .eq("id", user_id)
        .maybe_single()
        .execute()
    )
    if not resp or not getattr(resp, "data", None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User profile {user_id!r} not found")

    data = resp.data

    def _parse_skill(s) -> SkillEntry:
        if isinstance(s, str):
            return SkillEntry(skill_name=s, label=s, confidence_score=1.0)
        if isinstance(s, dict):
            name = s.get("skill_name") or s.get("label") or "Skill"
            lbl = s.get("label") or name
            return SkillEntry(
                skill_name=name,
                label=lbl,
                esco_id=s.get("esco_id"),
                confidence_score=float(s.get("confidence_score") or 0.0),
            )
        return SkillEntry(skill_name=str(s), label=str(s))

    hard_skills = [_parse_skill(s) for s in (data.get("hard_skills") or [])]
    soft_skills = [_parse_skill(s) for s in (data.get("soft_skills") or [])]

    return UserProfileResponse(
        id=data["id"],
        hard_skills=hard_skills,
        soft_skills=soft_skills,
        experience_years=data.get("experience_years", 0) or 0,
        source_type=data.get("source_type", "form") or "form",
        has_dense_vector=data.get("user_dense_vector") is not None,
        message="Profile retrieved",
    )
