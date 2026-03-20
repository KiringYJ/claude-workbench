@rules/core.md
@rules/python.md
<!-- rust.md not imported: this repo contains no Rust code. Consumer projects import it independently. -->

## Workbench-Specific Rules

### Auto-release after plugin changes

After committing a `feat:` or `fix:` change that touches `plugins/*/`, run `/release <plugin-name>` to bump the version before reporting completion. Do not wait for the user to ask.
