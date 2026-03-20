---
name: update-doc
description: Review and update project documentation to match current state
---

# Update Documentation

Review all project documentation and update anything that is stale or inaccurate.

## Checklist

1. **Read each documentation file** (README.md, CLAUDE.md, etc.)
2. **Verify plugin table** — do plugin names and descriptions match `plugins/*/.claude-plugin/plugin.json`?
3. **Verify file structure** — does the documented tree match the actual filesystem?
4. **Verify usage instructions** — are setup steps, config examples, and commands still accurate?
5. **Verify descriptions** — does the project summary reflect what the project actually does?
6. **Fix any inaccuracies** — edit the documentation files directly.
7. **Stage changes** — `git add` any updated documentation files.
