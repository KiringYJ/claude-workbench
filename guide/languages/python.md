# Python Agent Guide

## Naming

Use Python-standard `snake_case` for modules, packages, functions, and test files.

```text
src/example_project/add_entries.py
tests/test_normalize.py
```

## Workflow

Typical verification, adjusted by `AI_AGENT_PROJECT.md`, is:

```bash
uv run ruff check .
uv run ruff format --check .
uv run ty
uv run pytest
```

When intentionally fixing style, use `uv run ruff check . --fix` and `uv run ruff format .`, then rerun checks.

## Logging and Output

- Use `logging.getLogger(__name__)` for diagnostics.
- Do not use `print()` for status messages in library code.
- Reserve `print()` for intentional CLI output.

## Dependencies

Pin external packages in `pyproject.toml` or the project-approved lock/manifest with explicit version constraints. Prefer existing dependencies and standard library modules when sufficient.
