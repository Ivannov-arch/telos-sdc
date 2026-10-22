"""
FastAPI Backend — Aiversecity SDC XMUM
Owner: Person A (Backend Lead)
Run: uvicorn backend.main:app --reload --port 8000
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import match

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

app.include_router(match.router, prefix="/api", tags=["matching"])


@app.get("/health")
def health():
    return {"status": "ok", "service": "aiversecity-api"}
