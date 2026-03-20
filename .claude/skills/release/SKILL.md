---
name: release
description: Create versioned releases for workbench plugins using conventional commit prefixes
disable-model-invocation: true
---

# Release

Create versioned releases for workbench plugins. Version bumps are derived from conventional commit prefixes since the last release tag.

## Arguments

- `$ARGUMENTS` — either `seed` (first-time baseline tagging) or an optional plugin name (e.g., `core`, `rust`). If omitted, release all plugins with pending changes.

## Tag format

Tags follow the pattern `<plugin-name>@<version>` (e.g., `core@1.0.8`, `python@1.0.1`).

## Subcommand: `seed`

If `$ARGUMENTS` is `seed`, create baseline tags for all plugins at their current versions. This is a one-time setup step.

### Steps (seed)

1. **Read each plugin's version.** For every `plugins/*/.claude-plugin/plugin.json`, extract `name` and `version`.

2. **Check for existing tags.** For each plugin, run `git tag -l "<name>@*"`. If any tags already exist for that plugin, skip it and warn.

3. **Create annotated tags.** For each plugin without existing tags:
   ```
   git tag -a "<name>@<version>" -m "release: <name>@<version> (seed)"
   ```

4. **Report.** Print a table of created tags:
   ```
   Plugin   Version   Tag
   core     1.0.8     core@1.0.8
   python   1.0.1     python@1.0.1
   rust     1.0.1     rust@1.0.1
   ```

5. **Remind** the user to push tags when ready: `git push origin --tags`

## Main flow: release

### Steps

1. **Resolve target plugins.** If a plugin name is given, validate it exists under `plugins/<name>/`. Otherwise, discover all plugins from `plugins/*/.claude-plugin/plugin.json`.

2. **For each plugin, find the latest release tag:**
   ```bash
   git tag -l "<name>@*" --sort=-v:refname | head -1
   ```
   If no tag exists, error and tell the user to run `/release seed` first.

3. **List commits since the last tag that touch this plugin's directory:**
   ```bash
   git log <tag>..HEAD --oneline -- "plugins/<name>/"
   ```
   If no commits found, skip this plugin (no changes to release).

4. **Determine bump level from commit prefixes.** Parse each commit's subject line:

   | Prefix pattern | Bump |
   |----------------|------|
   | Subject contains `BREAKING CHANGE` or `!:` (e.g., `feat!:`, `fix!:`) | **major** |
   | `feat:` or `feat(<scope>):` | **minor** |
   | `fix:` or `fix(<scope>):` | **patch** |
   | Everything else (`chore:`, `docs:`, `refactor:`, `test:`, `ci:`, `style:`, `perf:`) | **none** |

   Take the **highest** bump level across all commits for that plugin. If the highest is "none", skip this plugin.

5. **Compute new version.** Given current version `X.Y.Z`:
   - **major** → `(X+1).0.0`
   - **minor** → `X.(Y+1).0`
   - **patch** → `X.Y.(Z+1)`

6. **Show summary table and ask for confirmation:**
   ```
   Plugin   Current   Bump    New       Commits
   core     1.0.8     minor   1.1.0     3
   python   1.0.1     patch   1.0.2     1
   rust     —         —       —         (no changes)
   ```
   Ask: "Proceed with these releases? (yes/no)"

   **Do NOT proceed without explicit user confirmation.**

7. **For each plugin with a bump, apply the release:**

   a. **Update `plugins/<name>/.claude-plugin/plugin.json`** — set `"version"` to the new version.

   b. **Update `.claude-plugin/marketplace.json`** — find the entry where `"name"` matches and set its `"version"` to the new version.

   c. **Commit the version files:**
      ```
      git add "plugins/<name>/.claude-plugin/plugin.json" ".claude-plugin/marketplace.json"
      git commit -m "release: <name>@<new_version>"
      ```

   d. **Create an annotated tag:**
      ```
      git tag -a "<name>@<new_version>" -m "release: <name>@<new_version>"
      ```

8. **Report results.** Print a summary of what was released:
   ```
   Released:
     core@1.1.0   (minor: 3 commits)
     python@1.0.2 (patch: 1 commit)
   ```

9. **Remind** the user to push commits and tags when ready:
   ```
   git push origin main --follow-tags
   ```
