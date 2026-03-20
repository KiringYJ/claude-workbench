# claude-workbench

Centralized Claude Code plugin marketplace and shared rules for cross-project reuse.

## Architecture

This repo serves two purposes:

1. **Shared rules** (`rules/`) — persistent context loaded via `@import` in consumer projects
2. **Plugins** (`plugins/`) — functional extensions (skills, hooks, hookify rules, MCP servers)

Rules are **not** inside plugins. Plugins provide functionality (hooks enforce checks, skills encode workflows); rules provide persistent context (conventions, philosophy, naming). Consumer projects import both independently.

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

Consumer projects do two things:

### 1. Import shared rules (via git submodule + `@import`)

```bash
# Add claude-workbench as a submodule
git submodule add https://github.com/KiringYJ/claude-workbench.git vendor/claude-workbench
```

Then in your project's `CLAUDE.md`:

```markdown
# Project Rules

@vendor/claude-workbench/rules/core.md
@vendor/claude-workbench/rules/rust.md
```

Import only the rules you need. `core.md` is recommended for all projects.

### 2. Enable plugins (via settings.json)

Add to your project's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "workbench": {
      "source": {
        "source": "github",
        "repo": "KiringYJ/claude-workbench"
      }
    }
  },
  "enabledPlugins": {
    "core@workbench": true,
    "rust@workbench": true
  }
}
```

Enable only the plugins you need.

## Structure

```
rules/
  core.md                          # shared rules (imported by consumer projects)
  python.md
  rust.md
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
```

## License

MIT
