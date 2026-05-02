---
name: format-markdown
enabled: true
event: edit
pattern: \.md$
action: warn
---

**Markdown edited — check formatting.**

After editing a Markdown file, verify:
1. Tables are aligned and render correctly
2. Code fences are closed with matching language tags
3. No trailing whitespace on heading lines
4. Lists use consistent markers (all `-` or all `*`, not mixed)
