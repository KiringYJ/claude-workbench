# Base Agent Guide

## Purpose

This vendor-neutral baseline is generated as `AI_AGENT_GUIDE.md`. Vendor entrypoints should only load or point to it and to the manually maintained `AI_AGENT_PROJECT.md`.

## Language Policy

All artifacts committed to a repository must be written in English: code, comments, documentation, commit messages, configuration, and generated examples. Conversation with a user may use any language, but repository content should stay in English unless the project explicitly documents a different policy in `AI_AGENT_PROJECT.md`.

## Operating Principles

- Inspect before editing, make the smallest reversible change that solves the real problem, and verify before claiming completion.
- Prefer current stable stacks, toolchains, runtimes, language standards, and project scaffolding for new work or upgrades unless project constraints require an older version.
- Preserve existing user behavior, public APIs, CLI flags, configuration formats, and machine-readable output unless the user explicitly requests a breaking change.
- Reuse existing project patterns before adding new abstractions.
- Do not add dependencies, services, code generators, plugins, marketplace entries, or global configuration without an explicit project decision.
- Treat project-local instructions as authoritative over generic guidance when they conflict.

## Standard Work Loop

1. Read the relevant instructions: `AI_AGENT_GUIDE.md` and `AI_AGENT_PROJECT.md` if present.
2. Inspect the current implementation and relevant working-tree state.
3. For non-trivial work, state or internally maintain a short plan covering scope, verification, and risk.
4. Make the minimal change and run the checks documented in `AI_AGENT_PROJECT.md`.
5. Review the diff for accidental edits, secrets, generated noise, and stale documentation.
6. Report changed files, verification evidence, and any remaining risks.

## Naming and Structure

- Use domain-specific, spelled-out names; retain established or standard abbreviations and existing intentional container names.
- Name source modules for singular concepts and peer-file collections with plurals when that distinction helps.
- Prefer simple, explicit control flow and early returns over deeply nested conditions.
- Promote repeated, environment-specific, arbitrary, or change-prone values to a named constant, configuration value, or documented project boundary.

## Output and Logging

Keep machine output and human diagnostics separate.

- Standard output is for command results or generated data.
- Standard error or the language logging framework is for progress, diagnostics, warnings, and errors.
- Library or domain code should not use raw print statements for status messages.
- Performance claims require measurements or profiling evidence.

## Dependency and External API Discipline

Before adopting or changing a dependency or SDK, consult version-specific official documentation, select a stable project-compatible version, and pin it according to the ecosystem. Confirm boundary behavior with a minimal reproduction or integration test, and document non-obvious reasons for the dependency.

## Documentation Discipline

Update documentation when behavior, commands, configuration, public APIs, layout, or onboarding changes. Keep `README.md` user-facing; place maintainer architecture, internal sync mechanics, and implementation notes in dedicated maintainer docs unless users need them.
