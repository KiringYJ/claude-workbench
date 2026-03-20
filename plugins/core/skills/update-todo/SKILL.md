---
name: update-todo
description: Review and update project TODO.md to reflect current implementation state
---

# Update TODO

Review the project's `TODO.md` and update it to reflect the current state of the codebase. If no `TODO.md` exists, create one from scratch based on known planned work.

## Record Format

The TODO.md file follows a strict two-layer format:

### 1. Header

```markdown
# TODO

> **Done** = implementation merged, **Verified** = manually tested / snapshot-covered.

## Record Format

Each category section contains:

1. **Summary table** with three columns:
   - **Done** (`[x]`/`[ ]`) — implementation merged into codebase
   - **Verified** (`[x]`/`[ ]`) — manually tested or snapshot-covered
   - **Item** — short task description
2. **Detail subsection** (`### Item Name`) per task, containing:
   - **File(s):** relevant source path(s)
   - Bullet list: CLI interface, behavior, key implementation notes
```

### 2. Summary table

A single markdown table listing all items with their status:

```markdown
| Done | Verified | Item |
|:----:|:--------:|------|
| [x]  | [x]      | Feature A |
| [x]  | [ ]      | Feature B |
| [ ]  | [ ]      | Feature C |
```

- Items with `Done [x]` have their implementation merged into the codebase.
- Items with `Verified [x]` have been manually tested or have snapshot/test coverage.
- Table rows are separated by a `---` horizontal rule from the detail subsections.

### 3. Detail subsections

One `### Item Name` subsection per table row, containing:

- **File(s):** — relevant source path(s) (`**File:**` for one, `**Files:**` for many)
- Bullet list describing: CLI interface, behavior, key implementation notes
- For unimplemented items: problem statement, proposed solution, design decisions, implementation plan

## Steps

1. **Read** the existing `TODO.md` at the project root. If it does not exist, note that a new one will be created.
2. **Scan the codebase** — use git log, grep, and file reads to determine which items are implemented, which have tests, and whether any new planned work should be added.
3. **Update status** — flip `[ ]` to `[x]` for Done when implementation is merged; flip `[ ]` to `[x]` for Verified when tests or manual verification exist.
4. **Add new items** — if the user mentions new planned work or you discover undocumented TODOs in the code, add them to both the summary table and the detail subsections.
5. **Remove completed items** — only if the user explicitly requests cleanup. By default, keep completed items visible for traceability.
6. **Update detail subsections** — ensure `File(s):` paths are accurate and descriptions match current implementation.
7. **Write** the updated `TODO.md`.
8. **Stage** the file with `git add TODO.md`.
