# claude-workbench

Centralized Claude Code plugin marketplace and shared rules for cross-project reuse.

## Architecture

This repo serves two purposes:

1. **Shared rules** (`rules/`) — synced to consumer projects as `.claude/rules/*.md`
2. **Plugins** (`plugins/`) — functional extensions (skills, hooks, hookify rules, MCP servers)

Rules are **not** inside plugins. Plugins provide functionality (hooks enforce checks, skills encode workflows); rules provide persistent context (conventions, philosophy, naming). Consumer projects sync both via a single skill.

## Rules

| File | Scope |
|------|-------|
| `rules/core.md` | Language-agnostic engineering rules, review philosophy, naming conventions |
| `rules/rust.md` | Rust naming, cargo workflow, pre-commit checks |
| `rules/python.md` | Python naming, uv/ruff/ty workflow, logging conventions |

## Plugins

| Plugin | Description |
|--------|-------------|
| **core** | Safety guards (hookify), doc review hook, code review skill, MCP servers |
| **rust** | Pre-commit guard (fmt/clippy/check), optimize skill |
| **python** | Pre-commit guard (ruff/ty), optimize skill, ty LSP server |

## Usage

### Quick start

1. Install the core plugin (adds the workbench marketplace and the `sync-workbench` skill):

```bash
claude plugin install core --marketplace workbench --source github:KiringYJ/claude-workbench
```

2. Run the sync skill to set up rules and plugin settings:

```
/sync-workbench rust
```

This generates `.claude/rules/*.md` and merges plugin settings into `.claude/settings.json`.

### Profiles

| Profile  | Rules              | Plugins                                    |
|----------|--------------------|--------------------------------------------|
| `base`   | core               | core@workbench                             |
| `rust`   | core, rust         | core@workbench, rust@workbench             |
| `python` | core, python       | core@workbench, python@workbench           |
| `full`   | core, rust, python | core@workbench, rust@workbench, python@workbench |

### Updating

Re-run `/sync-workbench` at any time. It is idempotent — unchanged files are skipped, and existing settings (permissions, env, custom plugins) are preserved.

Flags:
- `--rules-only` — only sync `.claude/rules/*.md`
- `--settings-only` — only sync `.claude/settings.json`
- `--check` — report whether anything is out of date without writing

### Standalone script (CI / no-Claude usage)

```bash
python scripts/sync_workbench.py rust --source /path/to/claude-workbench --target /path/to/project
python scripts/sync_workbench.py --check --source /path/to/claude-workbench --target /path/to/project
```

## Structure

```
workbench.json                     # profile definitions (rules + plugins per profile)
rules/
  core.md                          # shared rules (synced to consumer projects)
  python.md
  rust.md
scripts/
  sync_workbench.py                # standalone sync script for CI / non-Claude usage
plugins/
  core/
    .claude-plugin/
      plugin.json
    hooks/
      document_sync.py
      enforce_rules.py
      hooks.json
      test_document_sync.py
      test_enforce_rules.py
    skills/
      review/
        SKILL.md
      sync-workbench/
        SKILL.md                   # sync rules + settings to consumer projects
      update-document/
        SKILL.md
      update-todo/
        SKILL.md
    .mcp.json
    hookify.block-bad-git-add.md
    hookify.block-compound-cd.md
    hookify.block-no-verify.md
    hookify.ultrathink-mode.md
  python/
    .claude-plugin/
      plugin.json
    hooks/
      guard-python-commit.sh
      hooks.json
    skills/
      optimize/
        SKILL.md
  rust/
    .claude-plugin/
      plugin.json
    hooks/
      guard-rust-commit.sh
      hooks.json
    skills/
      optimize/
        SKILL.md
.claude/
  skills/
    new-plugin/
      SKILL.md
    plugin-test/
      SKILL.md
    release/
      SKILL.md
```

## License

MIT
