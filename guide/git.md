# Git and Change Management

## Safe Staging

- Inspect `git status` and the relevant diff, then stage only reviewed files for the current task. Avoid broad staging commands unless the user explicitly requests them and the entire candidate diff has been reviewed.

## Atomic Commit Discipline

- Make each commit one reviewable, reversible logical change. Split unrelated fixes, refactors, dependency updates, formatting, and documentation; exclude speculative cleanup.

## History Safety

- Treat existing working-tree changes as user-owned. Do not discard, overwrite, or hide them, and use destructive history or working-tree commands only with explicit authorization for their exact target.
- Never bypass hooks with `--no-verify`. Investigate and fix a hook failure, or report the underlying cause when it cannot be resolved in scope.

## Pre-commit Enforcement

Prefer deterministic, documented project hooks for routine format, lint, type, and test checks; keep slow checks in CI. Hook policy does not change the prohibition on bypassing hooks.

## Commit Messages

Every commit must use a Conventional Commit subject that explains the intent:

Subject format:

```text
<type>[optional scope]: <intent-oriented summary>
```

Use the standard type that best describes the change. For non-trivial commits, add only useful Lore trailers such as `Constraint:`, `Rejected:`, `Confidence:`, `Scope-risk:`, and `Tested:`.

## Review Before Final Response

Before reporting completion, confirm the diff contains only intended work, generated markers and project-specific content were preserved, and verification commands and outcomes are recorded.
