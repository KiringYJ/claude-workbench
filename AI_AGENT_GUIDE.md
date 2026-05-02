<!--
agent-workbench: managed
source: KiringYJ/agent-workbench
profile: base
updated: 0.1.0
manual-edits: preserve-marked-sections-only
-->

# AI Agent Guide

This file is generated from `agent-workbench` modules. Re-run the sync prompt to update it. Keep project-specific details in `AI_AGENT_PROJECT.md`.

# Base Agent Guide

## Purpose

This guide is the vendor-neutral baseline for AI agents working in a project. It applies to Claude Code, Codex, Gemini, OpenCode, and any other agent that can read repository files.

The canonical generated file in a consumer project is `AI_AGENT_GUIDE.md`. Vendor files such as `CLAUDE.md`, `AGENTS.md`, and `GEMINI.md` should only load or point to that guide and to `AI_AGENT_PROJECT.md`.

## Language Policy

All artifacts committed to a repository must be written in English: code, comments, documentation, commit messages, configuration, and generated examples. Conversation with a user may use any language, but repository content should stay in English unless the project explicitly documents a different policy in `AI_AGENT_PROJECT.md`.

## Operating Principles

- Prefer evidence over assumption; inspect files and run verification before claiming completion.
- Use the smallest reversible change that solves the real problem.
- Preserve existing user behavior, public APIs, CLI flags, configuration formats, and machine-readable output unless the user explicitly requests a breaking change.
- Keep diffs focused and bisectable.
- Reuse existing project patterns before adding new abstractions.
- Do not add dependencies, services, code generators, plugins, marketplace entries, or global configuration without an explicit project decision.
- Treat project-local instructions as authoritative over generic guidance when they conflict.

## Standard Work Loop

1. Read the relevant instructions: `AI_AGENT_GUIDE.md` and `AI_AGENT_PROJECT.md` if present.
2. Understand the task and inspect the current implementation before editing.
3. For non-trivial work, state or internally maintain a short plan: files to change, verification to run, and risks.
4. Make the minimal change.
5. Run the documented verification commands from `AI_AGENT_PROJECT.md` when available.
6. Review the diff for accidental edits, secrets, generated noise, and stale documentation.
7. Report changed files, verification evidence, and any remaining risks.

## Naming and Structure

- Use domain-specific names. Avoid vague containers such as `utils`, `helpers`, `common`, or `shared` unless the project already uses them intentionally.
- Spell names out. Avoid abbreviations unless they are standard in the language or domain.
- Source modules represent concepts and should usually use singular names.
- Data or collection directories that hold many peer files may use plural names.
- Prefer simple, explicit control flow and early returns over deeply nested conditions.

## Output and Logging

Keep machine output and human diagnostics separate.

- Standard output is for command results or generated data.
- Standard error or the language logging framework is for progress, diagnostics, warnings, and errors.
- Library or domain code should not use raw print statements for status messages.
- Performance claims require measurements or profiling evidence.

## Dependency and External API Discipline

Before adopting or changing a dependency or SDK:

- Consult version-specific official documentation when possible.
- Confirm return values, error behavior, and edge cases with a minimal reproduction or test.
- Pin versions according to the project language ecosystem.
- Add or update integration tests when behavior crosses a boundary.
- Document the reason for the dependency if it is not obvious.

## Documentation Discipline

Update documentation when behavior, commands, configuration, public APIs, file layout, or onboarding instructions change. Stale documentation is a defect.

---

# Git and Change Management

## Safe Staging

- Stage only the files intentionally changed for the current task.
- Do not use broad staging commands such as `git add .` or `git add -A` unless the user explicitly asks and the diff has been reviewed.
- Inspect `git status` and relevant diffs before committing or summarizing work.

## History Safety

- Do not run destructive history or working-tree commands (`git reset --hard`, `git clean`, force push, branch deletion, interactive rebase) unless explicitly authorized for the current task.
- Do not bypass hooks or checks with `--no-verify`. If a hook fails, fix or document the underlying cause.
- Keep commits focused and reversible.

## Commit Messages

All commits should use a Conventional Commit subject line and explain why the change exists, not just what files changed.

Subject format:

```text
<type>[optional scope]: <intent-oriented summary>
```

Use standard types such as `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, and `ci`. Choose the type that best describes the user-visible intent of the change.

For non-trivial commits, include useful Lore trailers when they clarify constraints, rejected alternatives, risk, or verification.

Example shape:

```text
refactor: make agent instructions portable across vendors

The repository now generates one canonical guide and keeps vendor
entrypoints thin so projects can use Claude Code, Codex, Gemini, or
OpenCode without duplicating policy.

Constraint: Sync must not require global configuration or marketplaces
Rejected: Git submodule distribution | too intrusive for consumer projects
Confidence: high
Scope-risk: moderate
Tested: Inspected generated files and sync prompt invariants
```

## Review Before Final Response

Before reporting completion:

- Confirm no unrelated files were modified.
- Confirm generated or managed files contain expected markers.
- Confirm project-specific files were preserved.
- Include verification commands and outcomes.

---

# Security and Safety

## Secrets and Sensitive Data

- Never commit secrets, tokens, private keys, credentials, `.env` files, local database dumps, or personal data.
- If sensitive material appears in the working tree, stop and report it without copying the secret into logs or summaries.
- Do not print secret values. Redact them when context is necessary.

## Scope Boundaries

- Modify only files relevant to the requested task.
- Do not modify application source code during an agent-workbench sync unless the user separately requests application changes.
- Do not install dependencies, plugins, marketplaces, extensions, or global/user-scope configuration as part of instruction sync.
- Prefer project-scoped configuration over user-scoped configuration.
- Do not rely on machine-local absolute paths in committed files.

## Generated Instruction Files

Managed instruction files may be regenerated by the sync prompt. Project-specific manual content belongs in `AI_AGENT_PROJECT.md` or inside explicit manual preservation blocks in `AI_AGENT_GUIDE.md`.

The sync process may update only:

- `AI_AGENT_GUIDE.md`
- `AI_AGENT_PROJECT.md` when it is missing
- `CLAUDE.md`
- `AGENTS.md`
- `GEMINI.md`
- `opencode.json`
- `.codex/config.toml`
- `.agent-workbench.yaml`

Any broader edit requires explicit user authorization.

## High-Risk Operations

Ask for explicit confirmation before destructive, irreversible, production-affecting, or credential-dependent operations. If a safe read-only inspection can answer the question, do that first.

---

# Testing and Verification

## Test-First Bias

For feature work and bug fixes, prefer this loop:

1. Add or extend a test that proves the expected behavior.
2. Run it and confirm it fails for the expected reason when practical.
3. Implement the minimal fix.
4. Run the targeted test and the broader project checks documented in `AI_AGENT_PROJECT.md`.
5. Refactor only while tests stay green.

If the project lacks tests, use the lightest reliable verification available and state the gap.

## Verification Selection

Choose verification proportional to risk:

- Documentation-only change: render or inspect relevant Markdown/configuration and check links or examples when practical.
- Small code change: targeted tests plus formatter/linter if available.
- Multi-file or behavior change: targeted tests, broader suite, type checks, lint, and documentation review.
- Security or data-mutation change: add negative tests, boundary tests, and explicit rollback or recovery notes.

## Clean Output

A successful verification run should have no unexplained warnings, formatter diffs, or stale generated output. If checks fail for pre-existing reasons, document the exact command and failure summary.

## Project Commands

Use `AI_AGENT_PROJECT.md` as the source of truth for build and test commands. If commands are missing, infer conservatively from standard manifests and report the assumption.

---

# Review Discipline

Use a skeptical review stance: correctness and simplicity beat cleverness and speed.

## Review Checklist

For each meaningful change, ask:

- Does this solve a real requested problem?
- Is there a simpler approach that removes a special case instead of adding branches?
- Could this regress existing CLI flags, configuration formats, public APIs, or output shapes?
- Are feature changes tangled with unrelated refactors?
- Are tests or verification appropriate for the risk?
- Are documentation and examples still accurate?
- Are new abstractions justified by current duplication, performance evidence, or clear boundary needs?
- Are error paths and edge cases explicit?
- Are performance claims backed by measurements?
- Did any generated, local, or secret file get touched accidentally?

## NACK Triggers

Treat these as blockers unless the user explicitly accepts the risk:

- Hidden behavior changes without tests or migration notes.
- Broad rewrite when a small fix would work.
- New dependency without a clear reason and version pinning.
- Optimization without measurements.
- Large duplicated guide content in vendor-specific entrypoints.
- Agent sync changing application source code.

## Summary Standard

Final summaries should include:

- Changed files grouped by purpose.
- Verification commands and results.
- Manual content preserved or created.
- Remaining risks or follow-up items.
