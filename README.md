# agent-workbench

`agent-workbench` is a vendor-neutral instruction workbench for AI coding agents. It turns shared engineering guidance into one canonical project guide plus thin entrypoints for Claude Code, Codex, Gemini, OpenCode, and other agents.

This repository may still be hosted or checked out under the historical name `claude-workbench` until it is renamed. The internal architecture and generated files now use `agent-workbench`.

## Why vendor-neutral?

The workbench does not make Claude, Claude plugins, Claude Marketplace, or Claude-specific settings the center of the system. Consumer projects should be usable by multiple agents without duplicating rules across vendor files.

The model is:

- `AI_AGENT_GUIDE.md` — canonical generated/shared guide.
- `AI_AGENT_PROJECT.md` — manually maintained project-specific guide.
- `CLAUDE.md` — thin Claude Code entrypoint.
- `AGENTS.md` — thin Codex/OpenCode/general agent entrypoint.
- `GEMINI.md` — thin Gemini entrypoint.
- `opencode.json` — optional OpenCode config that explicitly loads the guide files.
- `.codex/config.toml` — optional project-scoped Codex config.
- `.agent-workbench.yaml` — project sync profile.

No marketplace, plugin installation, git submodule, global CLI, user-scope config, or machine-local path is required.

## Repository layout

```text
agent-workbench/
├─ README.md
├─ manifest.yaml
├─ guide/
│  ├─ base.md
│  ├─ git.md
│  ├─ security.md
│  ├─ testing.md
│  ├─ review.md
│  ├─ languages/
│  │  ├─ rust.md
│  │  ├─ python.md
│  │  └─ typescript.md
│  └─ tools/
│     ├─ claude.md
│     ├─ codex.md
│     ├─ gemini.md
│     └─ opencode.md
├─ profiles/
│  ├─ base.yaml
│  ├─ rust.yaml
│  ├─ python.yaml
│  └─ typescript.yaml
├─ templates/
│  ├─ AI_AGENT_GUIDE.md.tpl
│  ├─ AI_AGENT_PROJECT.md.tpl
│  ├─ CLAUDE.md.tpl
│  ├─ AGENTS.md.tpl
│  ├─ GEMINI.md.tpl
│  ├─ opencode.json.tpl
│  ├─ codex.config.toml.tpl
│  └─ agent-workbench.yaml.tpl
└─ prompts/
   ├─ sync-agent-workbench.md
   ├─ audit-agent-workbench.md
   └─ repair-agent-workbench.md
```

Legacy Claude Marketplace/plugin assets from the previous design are preserved under `archive/claude-workbench-legacy/` for reference. They are not the primary distribution mechanism.

## Consumer project layout

A synchronized project should look like this:

```text
my-project/
├─ AI_AGENT_GUIDE.md
├─ AI_AGENT_PROJECT.md
├─ CLAUDE.md
├─ AGENTS.md
├─ GEMINI.md
├─ opencode.json
├─ .codex/
│  └─ config.toml
└─ .agent-workbench.yaml
```

`AGENTS.md` is the correct file name. Do not create `AGENT.md`.

## Canonical guide and thin entrypoints

`AI_AGENT_GUIDE.md` is generated from modules in `guide/` according to `.agent-workbench.yaml` and the selected profile. It carries a metadata marker:

```html
<!--
agent-workbench: managed
source: <repo-or-url>
profile: <profile-name>
updated: <date-or-version>
manual-edits: preserve-marked-sections-only
-->
```

Vendor entrypoints stay thin:

- `CLAUDE.md` uses Claude Code `@AI_AGENT_GUIDE.md` and `@AI_AGENT_PROJECT.md` references.
- `AGENTS.md` tells Codex, OpenCode, and general agents to read the canonical files directly.
- `GEMINI.md` uses Gemini-compatible guide references.

Do not copy the full guide into vendor-specific files.

## Project-specific content

`AI_AGENT_PROJECT.md` is manually maintained by each consumer project. It should contain details that do not belong in the shared guide:

- Architecture
- Build commands
- Test commands
- Important files and directories
- Domain terms
- Project-specific constraints

The sync workflow creates this file if it is missing, but never overwrites it after creation.

If a project must keep manual notes inside `AI_AGENT_GUIDE.md`, wrap them in explicit preservation blocks:

```html
<!-- agent-workbench:manual-begin -->
Manual note to preserve.
<!-- agent-workbench:manual-end -->
```

Only marked blocks are preserved during guide regeneration.

## Syncing a consumer project with an LLM

The update mechanism is prompt-driven. Give an agent the sync prompt and ask it to apply a profile.

Example invocation:

```text
Follow prompts/sync-agent-workbench.md from KiringYJ/agent-workbench.
Sync this project with the rust profile. Do not modify source code.
```

Or, if this repository is checked out locally:

```text
Use the agent-workbench sync prompt at ../agent-workbench/prompts/sync-agent-workbench.md.
Run a full sync with the python profile.
```

The prompt instructs the agent to:

1. Inspect the consumer repository.
2. Read or create `.agent-workbench.yaml`.
3. Resolve the selected profile and modules.
4. Compose `AI_AGENT_GUIDE.md` from `guide/` modules.
5. Preserve marked manual blocks.
6. Create `AI_AGENT_PROJECT.md` only if missing.
7. Create or update thin entrypoints and explicit agent config files.
8. Merge JSON/TOML config conservatively.
9. Report a concise diff summary.

## Sync modes

The sync prompt supports natural-language modes:

- `full sync` — guide, project file if missing, entrypoints, and agent configs.
- `guide-only sync` — only `AI_AGENT_GUIDE.md` and missing `.agent-workbench.yaml`.
- `entrypoints-only sync` — only vendor entrypoints and agent config files.
- `audit-only mode` — inspect consistency without modifying files.
- `repair missing files` — recreate missing or malformed instruction files while preserving manual content.

## Profiles

Profiles are YAML files under `profiles/`.

| Profile | Modules |
| --- | --- |
| `base` | `base`, `git`, `security`, `testing`, `review` |
| `rust` | `base` plus `languages/rust` |
| `python` | `base` plus `languages/python` |
| `typescript` | `base` plus `languages/typescript` |

Consumer projects can add explicit modules in `.agent-workbench.yaml`.

## Adding a language module

1. Create `guide/languages/<language>.md`.
2. Add it to `manifest.yaml` under `modules`.
3. Create `profiles/<language>.yaml` that extends `base` and lists `languages/<language>`.
4. Document expected build, lint, typecheck, and test commands in the module.
5. Keep project-specific commands in each consumer project's `AI_AGENT_PROJECT.md`.

## Safe overwrite policy

Sync may overwrite or update:

- `AI_AGENT_GUIDE.md` except marked manual blocks.
- `CLAUDE.md`.
- `AGENTS.md`.
- `GEMINI.md`.
- `.agent-workbench.yaml` when creating or changing the requested profile/modules.
- `opencode.json` only by conservative merge.
- `.codex/config.toml` only by conservative merge.

Sync must not overwrite after creation:

- `AI_AGENT_PROJECT.md`.

Sync must not modify:

- Application source code.
- Dependency manifests except explicitly listed agent config files.
- Global/user-scope configuration.
- Marketplace/plugin installation state.
- Git submodules.

## Auditing and repairing

Use `prompts/audit-agent-workbench.md` to check a project without modifying files.

Use `prompts/repair-agent-workbench.md` to repair missing or malformed instruction files while preserving manual content.

## License

MIT
