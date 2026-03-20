---
name: sync-workbench
description: Sync claude-workbench rules and plugin settings to this project
argument-hint: "<profile> [--rules-only | --settings-only | --check]"
user-invocable: true
---

# Sync Workbench

Synchronize rules and plugin settings from claude-workbench to this project.
Idempotent — safe to run repeatedly. Only overwrites managed files.

## Step 1: Determine Profile

1. If a profile argument was provided, use it.
2. Else ask the user to choose: `base`, `rust`, `python`, or `full`.

| Profile  | Rules              | Plugins                                    |
|----------|--------------------|--------------------------------------------|
| base     | core               | core@workbench                             |
| rust     | core, rust         | core@workbench, rust@workbench             |
| python   | core, python       | core@workbench, python@workbench           |
| full     | core, rust, python | core@workbench, rust@workbench, python@workbench |

## Step 2: Fetch Profile Config

Fetch `workbench.json` from the workbench source to confirm profile definitions.

Use WebFetch:
```
https://raw.githubusercontent.com/KiringYJ/claude-workbench/main/workbench.json
```

Parse the JSON. Verify the selected profile exists in `profiles`.

## Step 3: Sync Rules (skip if `--settings-only`)

For each rule name in the profile's `rules` array:

1. Fetch the rule file via WebFetch:
   ```
   https://raw.githubusercontent.com/KiringYJ/claude-workbench/main/rules/{name}.md
   ```
2. Prepend this header line:
   ```
   <!-- managed by sync-workbench — do not edit manually -->
   ```
   followed by a blank line, then the fetched content.
3. Write to `.claude/rules/{name}.md`.
4. If the file already exists with identical content, skip and report "up to date".

Create `.claude/rules/` directory if it does not exist.

**Do not touch** any `.claude/rules/*.md` file that is NOT in the profile's rules list.

## Step 4: Sync Settings (skip if `--rules-only`)

Read `.claude/settings.json` (create `{}` if it does not exist).

**Only** merge these two keys — preserve everything else unchanged:

### extraKnownMarketplaces

Add or update from workbench config:
```json
{
  "workbench": {
    "source": {
      "source": "github",
      "repo": "KiringYJ/claude-workbench"
    }
  }
}
```

### enabledPlugins

Set each plugin in the profile's `plugins` array to `true`.
**Do not remove** existing plugin entries that are not part of this profile.

Write back with `indent=2`.

## Step 5: Report

Print a summary:
- Which rules were synced vs already up to date
- Whether settings.json was updated vs already up to date

## Check Mode (`--check`)

If `--check` flag is present, **do not write any files**. Instead:
1. Fetch each rule and compare against the local `.claude/rules/{name}.md`.
2. Compare current `.claude/settings.json` plugin keys against what the profile defines.
3. Report "in sync" or list what is out of date.
