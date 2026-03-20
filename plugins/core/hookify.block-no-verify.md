---
name: block-no-verify
enabled: true
event: bash
pattern: git\s+(commit|push)\b.*--no-verify
action: block
---

**BLOCKED: `--no-verify` flag detected.**

Do not bypass hooks with `--no-verify`.
If a hook fails, investigate and fix the underlying issue instead of skipping it.
