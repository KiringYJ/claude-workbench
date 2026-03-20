# Core Engineering Rules

## Code Review & Engineering Philosophy

**Core stance**: skeptical until proven necessary. Correctness > speed.

**Process**: Research -> Plan -> Implement -> Validate. All code must be explicit, small, reversible, test-anchored.

### Engineering Taste

- Clarity over cleverness. Don't be clever — be clear.
- Simplicity beats flexibility. Ship working simplicity now.
- Invariants > conditionals (collapse branches where model corrections suffice).
- Prefer early returns over nested conditions for readability.
- Use domain-specific names — avoid generic modules like `utils`, `helpers`, `common`, `shared`.
- "Good taste": rewrite so the special case disappears and becomes the normal case.
- Never break userspace (existing CLI flags, config formats, JSON output shapes).
- Data safety is not optional — financial data and database mutations require care.

### Review Rules (applied to every patch)

0. First questions (before reading code):
   - Is this fixing a real production problem, or adding speculative complexity?
   - Is there a simpler approach that removes a special case by changing the model/data shape?
   - Will this introduce any regression (CLI, config, JSON shapes, outputs, semantics)?

1. Small diffs only; bisectable always.
2. Performance requires receipts (benchmark/profile).
3. Abstractions must earn rent (duplication pressure, perf evidence, divergence risk).
4. Kill ambiguity early; unclear problem => NACK.

**Tripwires:**
- >3 indentation levels => redesign (reduce nesting / change data flow).
- Any behavior change without tests (or snapshot update + migration note) => NACK.
- "Optimization" without numbers => NACK.

**Automatic NACK triggers**
- Hidden behavior change / missing tests
- Refactor + feature tangled in one patch
- "Optimization" without numbers
- Large patch not decomposed
- Added abstraction "for future extensibility"

**Accept criteria**
- Failing test before / passing after (or new visible capability)
- Net clarity / reduced complexity
- Single-revert rollback possible

## Claude Interaction Rules

### Plan-First Rule (mandatory)

Every non-trivial task **must** go through plan mode before implementation begins. No exceptions.

1. **Clarify first** — If the user's request is ambiguous or underspecified, ask clarifying questions until the desired behavior is fully understood. Do not guess or assume intent.
2. **Enter plan mode** — Research the codebase, then present a concrete plan (approach, files to change, trade-offs).
3. **Get user approval** — Wait for the user to confirm or adjust the plan before writing any code.
4. **Then implement** — Only after alignment, proceed to implementation.

Skipping straight to code without a plan is a **hard blocker** — treat it the same as skipping tests.

### Do
- Utilize subagents (Agent tool) as early as possible — parallelize independent research, exploration, and validation tasks to maximize throughput.
- Propose at least one *simpler* alternative if the plan seems complex.
- Batch related edits; keep functions short; explain data shapes.
- When uncertain, ask: *A (simple) vs B (flexible) -- which do you prefer?*
- Flag missing tests as hard blockers.

### Don't
- Don't break existing CLI flags or JSON output shapes.
- Don't add complexity without a concrete payoff.
- Don't hedge; don't accept TODO placeholders in hot paths.
- Don't proceed without reproducing a reported issue.

### Bash tool usage (mandatory)
- Run `cd <project>` **once** as a standalone Bash call at the start of the session.
- All subsequent Bash calls must use bare commands (e.g., `cargo test`, `git status`) — **never** compound with `cd <project> && ...`.
- The working directory persists between Bash calls, so repeating `cd` is unnecessary and noisy.

## File & Directory Naming Convention

**0. No abbreviations — spell names out in full.**

Use `database`, not `db`. Use `foreign_exchange`, not `fx`. Use `deduplicate`, not `dedup`.

Two rules govern singular vs plural:

**1. Source files and module directories use singular.**

These name a *concept*, not a collection.

**2. Data/collection directories use plural.**

These *hold multiple items* of the same kind.

**Quick test:** "Is this a module/concept?" → singular. "Does this hold N files of the same type?" → plural.

## Feature & Change Workflow

1. Write/extend tests first (happy path, edge case, failure mode).
2. **Verify RED** — run the test and confirm it fails for the expected reason (missing feature, not a typo). A test that passes immediately proves nothing.
3. Minimal implementation to make the test pass — nothing more.
4. **Verify GREEN** — all tests pass, output clean.
5. Refactor while staying green.
6. Review diff size and justification.
7. Verify docs are still accurate — if CLI flags, config formats, or parameters changed, update the relevant documentation.
8. Non-compliance (skipped tests, stale docs) => rejection.

**Bug fixes** — always write a failing test that reproduces the bug *before* fixing it. The test proves the fix and prevents regression.

**External dependency adoption checklist**
- Docs consulted (version-specific)
- Minimal reproduction confirming behavior
- Return/error semantics verified
- Integration test exists
- Version pinned in manifest
