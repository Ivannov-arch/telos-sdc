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

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from backend.routers import match, profile, simulate
from backend.routers import game  # FutureProof crisis simulation — F01/F02/F03
from backend.access import require_api_access

app = FastAPI(
    title="FutureProof API — Aiversecity SDC XMUM",
    description=(
        "FutureProof: Human–AI Decision Lab. "
        "Crisis simulation game → behavioral skill report → career intelligence."
    ),
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Tighten to Next.js origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# FutureProof Game Engine (F01 Quick Skill Profile + F02 Crisis Simulation + F03 Report)
app.include_router(game.router, prefix="/api", tags=["game"],
                   dependencies=[Depends(require_api_access)])

# Legacy pipeline (kept — CV upload, ESCO match, micro-task simulate)
app.include_router(profile.router, prefix="/api", tags=["profile"],
                   dependencies=[Depends(require_api_access)])
app.include_router(match.router, prefix="/api", tags=["matching"],
                   dependencies=[Depends(require_api_access)])
app.include_router(simulate.router, prefix="/api", tags=["simulation"],
                   dependencies=[Depends(require_api_access)])


@app.get("/", include_in_schema=False)
def index():
    return RedirectResponse(url="/docs")


@app.get("/health")
def health():
    return {"status": "ok", "service": "telos-sdc-api"}
