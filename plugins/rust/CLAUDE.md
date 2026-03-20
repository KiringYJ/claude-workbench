# Rust Development Rules

## Naming (Rust-specific additions)

The only acceptable abbreviation is `cli` (universally understood in the Rust ecosystem).

Use `snake_case` (underscores) in file names to stay consistent with Rust conventions. Hyphens are reserved for date components (e.g., `2026-01`) and the crate name in `Cargo.toml`.

## Workflow (Rust-specific additions)

Refactor step: iterate with `cargo clippy` + `cargo fmt` while staying green.

**Pre-commit enforcement**
- Run `cargo fmt --all` and `cargo clippy --tests -- -D warnings` before committing.
- The PreToolUse guard hook (`guard-rust-commit.sh`) automatically blocks `git commit`, `git push`, and `gh pr create` if fmt/clippy/check fail.

**External crate adoption**
- Version pinned in `Cargo.toml` (not just manifest — explicit version constraint).
