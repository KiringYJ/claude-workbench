---
name: plugin-test
description: Validate a workbench plugin's structure, rules, hooks, and skills
disable-model-invocation: true
---

# Plugin Test

Validate that a workbench plugin is structurally correct and ready to ship.

## Arguments

- `$ARGUMENTS` — plugin name (e.g., `rust`, `python`, `core`). If omitted, test all plugins.

## Steps

1. **Resolve target plugins.** If a plugin name is given, validate only that one. Otherwise, read `marketplace.json` and validate every listed plugin.

2. **For each plugin, run these checks:**

### Structure checks
- `plugins/<name>/.claude-plugin/plugin.json` exists and is valid JSON
- `plugin.json` has required fields: `name`, `description`, `version`
- Plugin is listed in `.claude-plugin/marketplace.json`

### Rules checks (if `rules/<name>.md` exists)
- File parses as valid Markdown (no broken tables, unclosed fences)
- No TODO/FIXME/HACK markers left in the file
- If the plugin has language-specific rules, they don't contradict core rules

### Hooks checks (if `hooks/` directory exists)
- `hooks.json` exists and is valid JSON
- Every script referenced in `hooks.json` exists on disk
- Hook scripts are executable (have `+x` or appropriate shebang)

### Skills checks (if `skills/` directory exists)
- Each skill subdirectory has a `SKILL.md`
- Each `SKILL.md` has valid YAML frontmatter with `name` and `description`

### Hookify checks (if `hookify.*.md` files exist)
- Each hookify rule has valid YAML frontmatter with `name`, `enabled`, `event`, `pattern`, `action`
- Regex in `pattern` field compiles without error

3. **Output a structured report:**

```
Plugin: <name>
  [PASS] plugin.json valid
  [PASS] rules/<name>.md present (or [SKIP] no rules file)
  [FAIL] hooks/guard.sh missing execute permission
  ...
Result: X/Y checks passed
```

4. If all plugins pass, output `All plugins valid.` If any fail, list failures and exit with a clear summary.
