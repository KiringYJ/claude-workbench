# Testing and Verification

## Test-First Bias

For feature work and bug fixes, add or extend a test that proves expected behavior, confirm the failure when practical, implement the minimal fix, and run targeted plus documented project checks. Refactor only while tests stay green.

If the project lacks tests, use the lightest reliable verification available and state the gap.

For reversible, low-impact changes, avoid adding tests that merely repeat implementation details or match documentation wording. Add tests when they establish meaningful behavior or protect a real boundary.

## Root Cause and Proof Discipline

For a bug or incident, reproduce or precisely characterize the failure and support the causal mechanism before presenting a root-cause fix. Test observations and rule out plausible alternatives. If the evidence remains incomplete, state the uncertainty and keep any experimental change narrow and reversible.

## Verification Selection

Choose verification proportional to risk:

- Documentation-only change: render or inspect relevant Markdown/configuration and check links or examples when practical.
- Small code change: targeted tests plus formatter/linter if available.
- Multi-file or behavior change: targeted tests, broader suite, type checks, lint, and documentation review.
- Security or data-mutation change: add negative tests, boundary tests, and explicit rollback or recovery notes.

Complete required checks. Broaden or repeat them only after further changes, failures, or unresolved concerns; stop when fresh evidence supports the completion criteria.

## Project Commands and Output

Use `AI_AGENT_PROJECT.md` as the source of truth for build and test commands. If commands are missing, infer conservatively from standard manifests and report the assumption. A successful run has no unexplained warnings, formatter diffs, or stale generated output; report exact commands and summaries for pre-existing failures.
