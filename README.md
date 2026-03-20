# claude-workbench

Centralized Claude Code plugin marketplace for cross-project reuse.

## Plugins

| Plugin | Description |
|--------|-------------|
| **core** | Language-agnostic engineering rules, review philosophy, safety guards, and doc review hook |
| **rust** | Rust naming conventions, cargo TDD workflow, pre-commit guard (fmt/clippy/check), optimize skill |
| **python** | uv/ruff/ty workflow, logging conventions, ty LSP server, pre-commit guard (ruff/ty), optimize skill |

## Usage

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

Enable only the plugins you need. `core` is recommended for all projects.

## Structure

```
.claude-plugin/
  marketplace.json
plugins/
  core/
    .claude-plugin/
      plugin.json
    hooks/
      doc_sync.py
      enforce_rules.py
      hooks.json
    skills/
      review/
        SKILL.md
      update-doc/
        SKILL.md
      update-todo/
        SKILL.md
    .mcp.json
    CLAUDE.md
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
    CLAUDE.md
  rust/
    .claude-plugin/
      plugin.json
    hooks/
      guard-rust-commit.sh
      hooks.json
    skills/
      optimize/
        SKILL.md
    CLAUDE.md
```

## License

MIT
