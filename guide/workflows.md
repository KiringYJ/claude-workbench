# Portable Agent Workflows

Every synchronized project should carry the same core workflows regardless of which coding agent is active. Use the Agent Skills standard directly instead of describing each workflow again through a capability registry or per-vendor adapter files.

## Canonical Project-Local Locations

- `.agents/prompts/` stores supporting prompt workflows that any capable coding agent can read and execute.
- `.agents/skills/` stores the canonical project copies of portable Agent Skills, including optional `scripts/`, `references/`, and `assets/` resources.
- `.agents/guardrails/` stores vendor-neutral guardrail documents.
- `.agent-workbench.lock.json` records sync provenance, scoped baselines, installed artifacts, and retained removals. Keep `.agent-workbench.yaml` as human-owned desired configuration.

`manifest.yaml` registers prompts and skills directly. Do not introduce a second registry that repeats their paths, portability labels, vendor targets, or fallback behavior.

## Vendor Discovery Boundary

Codex, Gemini CLI, OpenCode, and other compatible agents should discover the shared `.agents/skills/` tree directly.

Claude Code uses `.claude/skills/` for project skill discovery. When the Claude target is enabled, sync should copy the registered managed source/resource set for each canonical skill from `.agents/skills/<name>/` to `.claude/skills/<name>/` without appending adapter prose or changing its resources. Corresponding managed files must be byte-identical; unregistered local files remain preserved only in `.agents/skills/`. The Claude copy is a generated discovery mirror, not another source of truth. Use real copied files rather than symlinks so synchronized repositories behave consistently on Windows and other environments.

Do not generate `.codex/skills/`, `.gemini/skills/`, or `.opencode/skills/` mirrors by default. Create a vendor-specific file only when it encodes actual runtime behavior that the shared standard cannot express, such as loader configuration, permissions, hooks, invocation controls, or vendor metadata.

## Required Portable Workflows

| Workflow | Canonical artifacts |
| --- | --- |
| Workbench sync and audit | `.agents/prompts/sync-agent-workbench.md`, `.agents/prompts/audit-agent-workbench.md`, `.agents/prompts/repair-agent-workbench.md`, `.agents/skills/sync-agent-workbench/SKILL.md` |
| Loop until done | `.agents/prompts/loop-until-done.md`, `.agents/skills/loop-until-done/SKILL.md` |
| Guardrail authoring | `.agents/prompts/create-guardrail.md`, `.agents/skills/guardrail-authoring/SKILL.md` |
| Skill authoring | `.agents/prompts/create-agent-skill.md`, `.agents/skills/skill-authoring/SKILL.md` |
| Commit workflow | `.agents/prompts/commit-workflow.md`, `.agents/skills/commit-workflow/SKILL.md` |
| Linus-style review | `.agents/prompts/linus-review.md`, `.agents/skills/linus-review/SKILL.md` |
| Read a linked ChatGPT conversation | `.agents/skills/read-chatgpt-conversation/SKILL.md` |

## Portability Rules

- Treat install as the first sync. The same workflow should detect new, legacy/no-lockfile, and already-managed repositories.
- Use `.agent-workbench.lock.json` as a provenance/baseline ledger, not a package-manager lockfile.
- Classify sync drift as confirmed upstream removal, confirmed removal with local edits, suspected legacy removal, deselected by local config, source changed / migration required, or local unmanaged.
- Never delete downstream artifacts without explicit user confirmation. Record a decision to retain an obsolete managed artifact in `retainedRemovals`.
- Keep skills within the standard `SKILL.md` format unless an explicit target requires an extension.
- Prefer a compatible built-in or installed implementation when the active environment provides one, but keep the portable skill available as the project-owned fallback.
- Store any vendor preference or fallback rule once in the canonical skill or supporting prompt, not in four parallel adapter notes.
- Do not make a consumer project depend on a marketplace, plugin, extension, global configuration, submodule, or machine-local path.
- Keep generated workflows in English and project-local.

If a native feature is missing, unstable, or disabled, execute the canonical `.agents/skills/` or `.agents/prompts/` workflow directly.

## Skill Model and Reasoning Routing

This is the canonical dispatch table for installed skills. It chooses a default
combination for the *skill's first eligible stage*, not a new fixed agent role
or a promise that a runtime will honour an override. An explicit user-selected
model or effort wins. Before invoking a skill, look up its exact full name,
then its explicit aliases in this table. If it is not listed, use `gpt-5.6-terra`
with `medium` effort and report that the skill was unmapped. Load that skill's
original `SKILL.md` before work. For independent work, pass the path and a
bounded scope to an eligible child; do not auto-create a new task or launch a
CLI workflow.

When the native generic child surface supports overrides, dispatch its explicit
`model` and `reasoning_effort` fields separately, with `fork_turns` set to
`none` or a bounded recent history as the task needs. Keep model and effort
independent; do not create an agent definition for each pair. For a skill whose named
specialist is fixed at an incompatible pair, use that generic child only when
the runtime permits it; otherwise keep the current parent settings and report
the recommended pair and actual settings separately.

`Bounded child` means a separately reviewable read, implementation, or review
slice. `Leader workflow` remains in the parent, which owns its state,
orchestration, and final decision. `Parent-bound tool` remains in the parent
because it needs the current browser, UI, authenticated connector, live Excel,
or artifact session. Typed roles or a runtime may fix a model and reject an
override; choose an unconfigured eligible child only when the active runtime
supports the requested pair, otherwise keep the stage with the parent and
state that limitation. Image-generation models are selected by their tool, not
by this reasoning table.

Keep every required specialist lane and its evidence contract. For a dynamic
generic child, include the original specialist instructions as well as the skill
and bounded assignment. A missing required independent review is a blocker,
not permission for the author to self-review. A workflow that requires an
unavailable runtime remains unavailable; this table does not substitute a
different execution engine. Source-order rules apply to the skill handler's
own work; unrelated parent work may continue independently.

| Exact skill or explicit alias group | Model | Effort | Delivery | Stage or escalation |
| --- | --- | --- | --- | --- |
| `imagegen` | `gpt-5.6-terra` | `medium` | Parent-bound tool | Use this pair only for prompt and edit planning; the image tool controls its own model. |
| `openai-docs` | `gpt-5.6-luna` | `medium` | Bounded child | Escalate compatibility, migration, or policy interpretation to Sol high. |
| `plugin-creator` | `gpt-5.6-terra` | `high` | Bounded child | Keep manifest and local validation in scope. |
| `skill-creator`, `skill-creator:skill-creator` | `gpt-5.6-terra` | `high` | Bounded child | Use original skill instructions; escalate cross-runtime design to Sol high. |
| `skill-installer`, `plugin-management:plugin-management` | `gpt-5.6-terra` | `low` | Parent-bound tool | Installation, connection, and account changes remain parent-owned. |
| `ai-slop-cleaner`, `oh-my-codex:ai-slop-cleaner` | `gpt-5.6-sol` | `high` | Leader workflow | First lock behaviour; escalate a public-contract or architecture decision to Astra high. |
| `analyze`, `oh-my-codex:analyze` | `gpt-5.6-sol` | `high` | Bounded child | Investigation only; escalate security or architecture findings to Astra high. |
| `autopilot`, `oh-my-codex:autopilot` | `gpt-5.6-sol` | `high` | Leader workflow | Its exploration, implementation, and review stages use Luna low, Terra medium, and Sol high respectively; difficult architecture or critic stages may use Astra high. |
| `claude-code-setup:claude-automation-recommender` | `gpt-5.6-sol` | `high` | Bounded child | Recommendations only; installation follows the installer route. |
| `claude-md-management:claude-md-improver`, `claude-md-management:source-command-revise-claude-md` | `gpt-5.6-terra` | `medium` | Bounded child | Escalate conflicting project policy to Sol high. |
| `code-review`, `oh-my-codex:code-review` | `gpt-5.6-sol` | `xhigh` | Leader workflow | Code-reviewer lane: Sol xhigh. Independent architect lane: Astra high. Parent synthesizes both required results; preserve the skill's unavailable-review gate. |
| `computer-use:computer-use` | `gpt-5.6-terra` | `medium` | Parent-bound tool | Preserve the active computer session. |
| `deep-interview`, `oh-my-codex:deep-interview` | `gpt-5.6-sol` | `high` | Leader workflow | Parent asks and integrates answers; no child runs the interview. |
| `deep-research-work:deep-research` | `gpt-6-astra` | `high` | Bounded child | Preserve citations; difficult mathematical or high-stakes synthesis may use Astra xhigh. |
| `doctor`, `oh-my-codex:doctor` | `gpt-5.6-terra` | `high` | Parent-bound tool | Escalate repeated or cross-runtime diagnosis to Sol high. |
| `documents:documents`, `pdf:pdf`, `presentations:Presentations`, `spreadsheets:Spreadsheets` | `gpt-5.6-terra` | `high` | Parent-bound tool | Keep render, visual QA, and artifact session with parent. |
| `help`, `oh-my-codex:hud`, `oh-my-codex:cancel`, `ralph-loop:source-command-help`, `ralph-loop:source-command-cancel-ralph` | `gpt-5.6-luna` | `low` | Parent-bound tool | Status or control only. |
| `hookify:source-command-configure`, `hookify:writing-hookify-rules` | `gpt-5.6-terra` | `medium` | Parent-bound tool | Escalate security-enforcement semantics to Sol xhigh. |
| `hookify:source-command-list` | `gpt-5.6-luna` | `low` | Parent-bound tool | Read-only listing. |
| `oh-my-codex:ask` | `gpt-5.6-sol` | `high` | Parent-bound tool | External-advisor question stays parent-owned; verify returned claims locally. |
| `oh-my-codex:autoresearch`, `oh-my-codex:autoresearch-goal` | `gpt-5.6-sol` | `high` | Leader workflow | Keep state and evaluator gates in the parent; difficult critic stages may use Astra high. |
| `oh-my-codex:best-practice-research` | `gpt-5.6-sol` | `high` | Bounded child | Use official evidence; escalate a dependency choice to the dependency route. |
| `oh-my-codex:configure-notifications` | `gpt-5.6-luna` | `medium` | Parent-bound tool | User-facing notification configuration remains parent-owned. |
| `oh-my-codex:design` | `gpt-5.6-sol` | `high` | Leader workflow | Escalate difficult product or architectural decisions to Astra high. |
| `oh-my-codex:omx-setup`, `omx-setup` | `gpt-5.6-terra` | `medium` | Parent-bound tool | Escalate repair diagnosis to Sol high. |
| `oh-my-codex:performance-goal` | `gpt-5.6-sol` | `high` | Leader workflow | Use measurement before implementation; difficult architecture tradeoffs may use Astra high. |
| `oh-my-codex:pipeline`, `oh-my-codex:ralph`, `ralph`, `oh-my-codex:ultragoal`, `oh-my-codex:ultrawork`, `ultrawork`, `oh-my-codex:ultraqa`, `ultraqa` | `gpt-5.6-sol` | `high` | Leader workflow | Keep loop/pipeline state in parent; use Luna low for lookup, Terra medium for routine implementation, Sol high for verification. |
| `oh-my-codex:plan`, `plan`, `oh-my-codex:ralplan`, `ralplan` | `gpt-5.6-sol` | `high` | Leader workflow | Escalate contested architecture or high-impact strategy to Astra xhigh. |
| `oh-my-codex:prometheus-strict` | `gpt-5.6-sol` | `high` | Leader workflow | Keep interview, criticism, and synthesis parent-led; difficult synthesis may use Astra xhigh. |
| `oh-my-codex:skill` | `gpt-5.6-terra` | `medium` | Parent-bound tool | Installing/removing skills follows the installer route. |
| `oh-my-codex:team`, `team` | `gpt-5.6-sol` | `high` | Leader workflow | Parent owns coordination; difficult architecture or critic stages may use Astra high. |
| `oh-my-codex:visual-ralph` | `gpt-5.6-sol` | `xhigh` | Leader workflow | Preserve visual evidence and iterative state in parent. |
| `oh-my-codex:wiki` | `gpt-5.6-terra` | `medium` | Parent-bound tool | Escalate a cross-project taxonomy decision to Sol high. |
| `oh-my-codex:worker` | `gpt-5.6-terra` | `medium` | Bounded child | Team runtime assigns its actual model; this row does not override it. |
| `security-review` | `gpt-5.6-sol` | `xhigh` | Bounded child | Independent security review; send high-impact remediation decisions to Astra xhigh. |
| `sites:sites-building` | `gpt-5.6-terra` | `high` | Parent-bound tool | Preserve Sites project/session; deployment uses hosting route. |
| `sites:sites-hosting` | `gpt-5.6-sol` | `high` | Parent-bound tool | External publish remains parent-owned. |
| `spreadsheets:excel-live-control` | `gpt-5.6-terra` | `high` | Parent-bound tool | Preserve the live Excel session. |
| `template-creator:template-creator` | `gpt-5.6-terra` | `high` | Bounded child | Render and verify the produced reusable artifact. |
| `visualize:visualize` | `gpt-5.6-terra` | `medium` | Parent-bound tool | Preserve interactive visualization state. |
| `web-clone` | `gpt-5.6-sol` | `high` | Leader workflow | Use parent-held browser evidence; escalate major design decisions to Astra xhigh. |
| `commit-workflow` | `gpt-5.6-sol` | `high` | Parent-bound tool | Parent owns staging, commit, push, and external PR actions. |
| `guardrail-authoring` | `gpt-5.6-sol` | `xhigh` | Leader workflow | Escalate enforcement or security-contract decisions to Astra xhigh. |
| `linus-review` | `gpt-5.6-sol` | `xhigh` | Bounded child | Independent reviewer only; edits remain parent-directed. |
| `loop-until-done` | `gpt-5.6-terra` | `high` | Leader workflow | Escalate repeated verification failure or ambiguous root cause to Sol high. |
| `read-chatgpt-conversation` | `gpt-5.6-terra` | `medium` | Parent-bound tool | Preserve authenticated reader/browser session and transcript completeness evidence; escalate difficult synthesis to Sol high. |
| `skill-authoring` | `gpt-5.6-terra` | `high` | Bounded child | Escalate cross-runtime or safety policy design to Sol high. |
| `sync-agent-workbench` | `gpt-5.6-sol` | `high` | Leader workflow | Preserve sync state; external/global installation is out of scope unless separately requested. |
