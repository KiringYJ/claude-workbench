# Project-Specific Agent Context

## Architecture

This repository is the source workbench for vendor-neutral AI-agent instructions. Shared guidance lives in `guide/`, profile composition lives in `profiles/`, consumer-facing templates live in `templates/`, and prompt-driven workflows live in `prompts/`.

Legacy Claude Marketplace/plugin assets from the previous design are preserved under `archive/claude-workbench-legacy/` for reference only.

## Build Commands

No build step is required for the prompt/template repository.

## Test Commands

No automated test suite is currently required. For changes, verify by inspecting:

```bash
git status --short
git diff --stat
```

For prompt/template edits, also verify that `manifest.yaml` references existing files and that generated entrypoints remain thin.

## Important Files and Directories

- `manifest.yaml` — module, profile, and template registry.
- `guide/` — source modules for generated guides.
- `profiles/` — module selection profiles.
- `templates/` — files created in consumer projects.
- `prompts/` — LLM-executed sync, audit, and repair workflows.
- `archive/claude-workbench-legacy/` — deprecated Claude-centric implementation retained for reference.

## Domain Terms

- **Canonical guide**: `AI_AGENT_GUIDE.md`, generated from selected modules.
- **Project guide**: `AI_AGENT_PROJECT.md`, manually maintained by each project.
- **Thin entrypoint**: vendor-specific file that points to the canonical guides without duplicating them.
- **Profile**: YAML selection of modules for a language or project type.

## Project-Specific Constraints

- Keep the architecture vendor-neutral.
- Do not make Claude Marketplace or plugins the primary distribution mechanism.
- Do not require global/user-scope configuration, git submodules, or machine-local paths.
- Preserve project-specific manual content during sync.
- Do not create `AGENT.md`; use `AGENTS.md`.
