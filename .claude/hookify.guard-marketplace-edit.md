---
name: guard-marketplace-edit
enabled: true
event: edit
pattern: marketplace\.json$
action: warn
---

**Marketplace manifest edited — verify plugin structure.**

When modifying `marketplace.json`, ensure:
1. Every listed plugin has a matching `plugins/<name>/` directory
2. Each plugin directory contains `.claude-plugin/plugin.json`
3. A corresponding `rules/<name>.md` exists (if the plugin provides rules)
4. The `name` field in `marketplace.json` matches the `name` in `plugin.json`
5. The `source` path points to an existing directory
6. The `version` in `marketplace.json` matches the `version` in `plugin.json`
