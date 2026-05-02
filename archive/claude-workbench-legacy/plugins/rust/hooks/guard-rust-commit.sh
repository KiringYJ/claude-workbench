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
cargo fmt --all --check >/dev/null 2>&1 || {
  echo "Blocked: cargo fmt --all --check failed. Run cargo fmt --all first." >&2
  exit 2
}

cargo clippy --tests -- -D warnings >/dev/null 2>&1 || {
  echo "Blocked: cargo clippy --tests -- -D warnings failed." >&2
  exit 2
}

cargo check >/dev/null 2>&1 || {
  echo "Blocked: cargo check failed." >&2
  exit 2
}

exit 0
