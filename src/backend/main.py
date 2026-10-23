"""
FastAPI Backend — Aiversecity SDC XMUM
Owner: Person A (Backend Lead)
Run: uvicorn backend.main:app --reload --port 8000
"""

import sys
from pathlib import Path

# Ensure src/ directory is on sys.path for both local development and Render deployment
SRC_DIR = Path(__file__).resolve().parent.parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from postgrest.exceptions import APIError as PostgrestAPIError
from backend.routers import match, profile, simulate
from backend.access import require_api_access

app = FastAPI(
    title="Aiversecity API",
    description="Future-Ready Workforce Matching Engine — SDC XMUM Hackathon",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Person C: tighten this to Next.js origin in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(profile.router, prefix="/api", tags=["profile"],
                   dependencies=[Depends(require_api_access)])
app.include_router(match.router, prefix="/api", tags=["matching"],
                   dependencies=[Depends(require_api_access)])
app.include_router(simulate.router, prefix="/api", tags=["simulation"],
                   dependencies=[Depends(require_api_access)])


@app.exception_handler(PostgrestAPIError)
async def supabase_error_handler(_: Request, exc: PostgrestAPIError):
    """Surface Supabase/PostgREST failures as a readable `detail` instead of a bare 500."""
    message = exc.message or "Database request failed."
    hint = ""
    if exc.code == "42501":
        hint = (
            " The database rejected the write under row-level security. "
            "This usually means SUPABASE_SECRET_KEY is a publishable key rather than "
            "the project's secret (service) key."
        )
    return JSONResponse(status_code=502, content={"detail": f"Supabase error: {message}.{hint}"})


@app.get("/", include_in_schema=False)
def index():
    return RedirectResponse(url="/docs")


@app.get("/health")
def health():
    return {"status": "ok", "service": "telos-sdc-api"}
