#!/usr/bin/env bash
set -Eeuo pipefail

PORT="${PORT:-5000}"
FRONTEND_DIR="${FRONTEND_DIR:-src/frontend}"
export BACKEND_URL="${BACKEND_URL:-https://telos-sdc.onrender.com}"

cd "${FRONTEND_DIR}"
exec ./node_modules/.bin/next start \
  --hostname 0.0.0.0 \
  --port "${PORT}"
