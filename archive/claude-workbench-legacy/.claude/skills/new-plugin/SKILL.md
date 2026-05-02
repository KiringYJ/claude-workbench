---
name: new-plugin
description: Scaffold a new workbench plugin with standard structure
disable-model-invocation: true
---

# New Plugin

Scaffold a new plugin in the workbench with the standard directory structure.

## Arguments

- `$ARGUMENTS` — plugin name (required, e.g., `go`, `typescript`, `docker`)

## Steps

1. **Validate the name.** Reject if:
   - Name is empty
   - `plugins/<name>/` already exists
   - Name contains uppercase or special characters (must be lowercase alphanumeric + hyphens)

2. **Create the plugin directory structure:**

```
plugins/<name>/
  .claude-plugin/
    plugin.json
```

3. **Generate `plugin.json`** with this template:

```json
{
  "name": "<name>",
  "description": "<Name> development rules",
  "version": "1.0.0"
}
```

4. **Create `rules/<name>.md`** with this template:

```markdown
# <Name> Development Rules

## Naming (<Name>-specific additions)

<!-- Add language/domain-specific naming conventions here -->

## Workflow (<Name>-specific additions)

<!-- Add language/domain-specific workflow steps here -->
<!-- e.g., formatter, linter, type checker commands -->

**Pre-commit checklist (mandatory)**
- <!-- List required checks before committing -->
- Fix all warnings, even if not caused by your change.
- Do not commit until all commands pass cleanly.

**External package adoption**
- Version pinned in the manifest (explicit version constraint).
```

5. **Register in marketplace.** Add an entry to `.claude-plugin/marketplace.json`:

```json
{
  "name": "<name>",
  "source": "./plugins/<name>",
  "description": "<Name> development rules",
  "version": "1.0.0",
  "keywords": ["<name>"],
  "category": "language"
}
```

6. **Report what was created** and remind the user to:
   - Fill in the `rules/<name>.md` template
   - Add skills in `plugins/<name>/skills/` if needed
   - Add hooks in `plugins/<name>/hooks/` if needed
   - Add hookify rules as `plugins/<name>/hookify.*.md` if needed
