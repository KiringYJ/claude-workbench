# claude-workbench

Centralized Claude Code plugin marketplace for cross-project reuse.

## Plugins

| Plugin | Description |
|--------|-------------|
| **core** | Language-agnostic engineering rules, review philosophy, safety guards, code review skill |
| **rust** | Rust naming conventions, cargo TDD workflow, pre-commit guard (fmt/clippy/check) |
| **python** | uv/ruff/ty workflow, logging conventions, ty LSP, commit/optimize/pre-push skills |

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
  marketplace.json          # marketplace manifest
plugins/
  core/
    CLAUDE.md               # review philosophy, interaction rules, naming, TDD workflow
    skills/review/          # /review — Linus Mode code review
    hookify.block-*         # safety guards (git add, --no-verify, compound cd)
    hookify.ultrathink-*    # extended reasoning mode
  rust/
    CLAUDE.md               # Rust-specific naming, cargo workflow
    hooks/                  # pre-commit guard (cargo fmt/clippy/check)
  python/
    CLAUDE.md               # Python-specific naming, ruff/ty workflow, logging
    skills/commit/          # /commit — lint, format, type-check, test, commit
    skills/optimize/        # /optimize — cProfile-based profiling workflow
    skills/pre-push/        # /pre-push — ruff + ty + pytest
```

## License

MIT
