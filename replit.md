# Running on Replit

This import is a Python FastAPI backend, not a frontend application. Keep the
existing source layout under `src/` and the existing Supabase/Runpod services.

## Start

Use the **Start application** workflow (the Run button):

```sh
uv run uvicorn backend.main:app --app-dir src --host 0.0.0.0 --port 5000
```

Dependencies are installed through the root `pyproject.toml` and `uv.lock`,
matching the packages in `src/backend/requirements.txt`. `uv run` restores them
if needed. Python 3.12 is configured in `.replit`.

The preview opens the interactive API documentation at `/docs` via a root
redirect. `/health` checks that the API process is alive; it does not check
database connectivity. The OpenAPI schema is at `/openapi.json`.

## External services

Configure the existing service values in Replit Secrets; never commit them:

- `SUPABASE_URL`: the existing Supabase project URL.
- `SUPABASE_SECRET_KEY`: the existing server-side Supabase secret/service key.
- `RUNPOD_API_KEY`: the key for the existing Runpod endpoints.
- `RUNPOD_BGE_M3_URL`: the existing BGE-M3 inference endpoint URL.
- `RUNPOD_LLM_ENDPOINT_URL` (optional; `RUNPOD_LLM_URL` is also supported):
  the existing LLM evaluator endpoint URL.

Startup, docs, and health work without these values. Profile persistence,
matching, and simulation data require Supabase, with the `telos_sdc` schema and
seed data described in `src/supabase/` and `src/docs/DATASETS.md`. No database
schema or seed changes are applied automatically by the workflow.

Without the Runpod embedding settings the imported code skips vector generation.
Without the optional LLM evaluator it uses its existing deterministic rubric
evaluator. Full service-backed behavior cannot be verified until real service
settings are supplied.
