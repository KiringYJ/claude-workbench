---
name: block-bad-git-add
enabled: true
event: bash
pattern: git\s+add\s+(-A|\.)(\s|$)
action: block
---

**BLOCKED: Unsafe `git add` detected.**

Do not use `git add -A` or `git add .`.
Stage only the minimal relevant files by explicit name.

This prevents accidentally committing sensitive files (.env, credentials) or large binaries.
