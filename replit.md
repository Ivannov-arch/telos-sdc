# Running on Replit

This project is a Python FastAPI backend (`src/backend`) plus a Next.js 16 +
Tailwind v4 frontend (`src/frontend`). Keep the existing source layout under
`src/` and the existing Supabase/Runpod services.

## Workflows

- **Start application** (Run button, preview on port 5000):
  `cd src/frontend && npx next dev --hostname 0.0.0.0 --port 5000`
- **Backend API** (console, port 8000):
  `uv run uvicorn backend.main:app --app-dir src --host 0.0.0.0 --port 8000`

Both must be running. Python dependencies live in the root `pyproject.toml` /
`uv.lock` (mirroring `src/backend/requirements.txt`); frontend dependencies in
`src/frontend/package.json` (`npm install` inside `src/frontend`).

The backend root `/` redirects to its interactive docs at `/docs`; `/health`
checks only that the API process is alive.

## Frontend architecture

- App Router under `src/frontend/src/app`. Pages: `/`, `/profiles`,
  `/profile/new`, `/profile/[id]`, `/match/[id]`, `/simulate`,
  `/simulate/[taskId]`. The "active profile" is remembered in localStorage.
- All browser data access goes through the typed client
  `src/frontend/src/lib/api.ts`, which calls the server-side proxy
  `src/frontend/src/app/api/backend/[...path]/route.ts`. The proxy forwards to
  `BACKEND_URL` (default `http://127.0.0.1:8000`) and attaches the
  `API_ACCESS_TOKEN` bearer token. **Never expose that token to the browser.**
- `next.config.ts` sets `allowedDevOrigins` for the Replit preview domains (and
  `127.0.0.1` for local checks). Next's dev runtime does not hydrate until its
  HMR socket connects, so a blocked origin shows a page stuck in loading state.
- Styling: Tailwind v4 is wired through a Turbopack `*.css` loader rule in
  `next.config.ts`; that rule also captures `*.module.css`, so CSS Modules do
  not work here. Use global classes in `src/app/globals.css` instead. If
  stylesheet edits do not appear after a restart, delete `src/frontend/.next`
  (Turbopack's persistent cache) and restart.
- Checks: `cd src/frontend && npx tsc --noEmit && npx eslint .`

## External services (Replit Secrets; never commit)

- `API_ACCESS_TOKEN`: long random token for the trusted-operator API. All
  backend `/api/*` routes require `Authorization: Bearer <token>`; the frontend
  proxy supplies it server-side. Missing server config → 503; bad token → 401.
  This is a private shared-operator boundary, not multi-user auth. Individual
  sign-in and per-profile ownership checks are required before ordinary users
  may access profile or simulation data.
- `SUPABASE_URL`: the existing Supabase project URL.
- `SUPABASE_SECRET_KEY`: must be the project's **secret** key
  (`sb_secret_…` or legacy `service_role` JWT). A publishable key
  (`sb_publishable_…`) allows reads only; writes then fail with a row-level
  security error (the backend reports this as HTTP 502 with an explanation).
- `RUNPOD_API_KEY`, `RUNPOD_BGE_M3_URL`: existing Runpod BGE-M3 endpoint.
- `RUNPOD_LLM_ENDPOINT_URL` (optional; `RUNPOD_LLM_URL` also accepted): LLM
  evaluator. Without it the deterministic rubric evaluator is used.

## Data state (as of setup)

Supabase `telos_sdc` has skills, occupations, simulation tasks and role data
seeded; matching returns real roles with skill gaps and SDG alignment. One
smoke-test profile ("Smoke-test profile created during frontend setup") was
created during setup and can be deleted. Backend tests: `uv run python -m unittest discover -s src -p "test_api_access.py"`.
