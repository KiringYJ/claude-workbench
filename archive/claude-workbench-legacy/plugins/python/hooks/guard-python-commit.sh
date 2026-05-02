#!/usr/bin/env bash
set -euo pipefail

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""')

needs_guard=0
if [[ "$COMMAND" =~ ^git[[:space:]]+commit([[:space:]]|$) ]]; then
  needs_guard=1
elif [[ "$COMMAND" =~ ^git[[:space:]]+push([[:space:]]|$) ]]; then
  needs_guard=1
elif [[ "$COMMAND" =~ ^gh[[:space:]]+pr[[:space:]]+create([[:space:]]|$) ]]; then
  needs_guard=1
fi

if [[ "$needs_guard" -eq 0 ]]; then
  exit 0
fi

# Verification gate — check only, never modify files
uv run ruff check . >/dev/null 2>&1 || {
  echo "Blocked: ruff check failed. Run uv run ruff check . --fix first." >&2
  exit 2
}

uv run ruff format --check . >/dev/null 2>&1 || {
  echo "Blocked: ruff format check failed. Run uv run ruff format . first." >&2
  exit 2
}

uv run ty >/dev/null 2>&1 || {
  echo "Blocked: ty type check failed." >&2
  exit 2
}

exit 0
