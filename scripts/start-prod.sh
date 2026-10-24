#!/usr/bin/env bash
set -Eeuo pipefail

PORT="${PORT:-5000}"
BACKEND_PORT="${BACKEND_PORT:-8000}"
BACKEND_HOST="${BACKEND_HOST:-127.0.0.1}"
FRONTEND_DIR="${FRONTEND_DIR:-src/frontend}"
export BACKEND_URL="${BACKEND_URL:-http://${BACKEND_HOST}:${BACKEND_PORT}}"

uv run uvicorn backend.main:app \
  --app-dir src \
  --host "${BACKEND_HOST}" \
  --port "${BACKEND_PORT}" &
backend_pid=$!

(
  cd "${FRONTEND_DIR}"
  exec ./node_modules/.bin/next start \
    --hostname 0.0.0.0 \
    --port "${PORT}"
) &
frontend_pid=$!

cleanup() {
  local exit_code=$?
  trap - EXIT INT TERM
  kill "${backend_pid}" "${frontend_pid}" 2>/dev/null || true
  wait "${backend_pid}" "${frontend_pid}" 2>/dev/null || true
  exit "${exit_code}"
}
trap cleanup EXIT INT TERM

wait -n "${backend_pid}" "${frontend_pid}"
