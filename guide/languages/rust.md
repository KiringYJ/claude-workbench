# Rust Agent Guide

## Naming

Use Rust-standard `snake_case` for modules and file names. The abbreviation `cli` is acceptable because it is common in the Rust ecosystem; otherwise prefer full words.

## Workflow

Typical verification, adjusted by `AI_AGENT_PROJECT.md`, is:

```bash
cargo fmt --all --check
cargo clippy --tests -- -D warnings
cargo check
cargo test
```

Run `cargo fmt --all` only when intentionally formatting. Fix all warnings before committing.

## Dependencies

Pin external crates in `Cargo.toml` with explicit version constraints. Before adding a crate, verify that the standard library or existing dependencies do not already solve the problem.

## Output

Use the project logging stack (`log`, `tracing`, or documented equivalent) for diagnostics. Reserve `println!` for intentional command output.
