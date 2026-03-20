---
name: optimize
description: Profile and optimize a slow operation using cProfile
---

# Performance Optimization Workflow

Profile and optimize a slow Python operation.

**Core constraint**: never let a single profiling run exceed 2 minutes.

## Steps

1. **Baseline profiling run** — run the target with cProfile:
   ```bash
   uv run python -m cProfile -s cumulative <module_or_script> 2>&1 | head -50
   ```

2. **Analyze profile** — identify:
   - Which functions dominate cumulative time?
   - Redundant I/O operations?
   - Repeated parsing or serialization?
   - Unnecessary object creation?

3. **Identify all optimization opportunities** — list everything before implementing:
   - **Caching**: memoize repeated reads or computations
   - **Algorithmic**: reduce complexity, avoid re-sorting
   - **I/O**: batch operations, avoid re-reading files
   - **Early exit**: skip items that cannot affect the result

4. **Implement all optimizations in one pass**. Follow existing code conventions.

5. **Verify tests pass**:
   ```bash
   uv run ruff check . --fix
   uv run ruff format .
   uv run ty
   uv run python -m pytest -q
   ```

6. **Measure improvement** — re-run profiling, compare to baseline.

7. **Iterate** — repeat steps 2-6 until no new opportunities are visible.

## Rules

- 2-minute cap per profiling run.
- Batch all optimizations — identify everything, then implement in one pass.
- Tests must pass after every implementation pass — no exceptions.
- Never sacrifice correctness for speed.
