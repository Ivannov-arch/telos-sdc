#!/usr/bin/env bash
set -euo pipefail

uv sync --frozen
npm --prefix src/frontend ci
