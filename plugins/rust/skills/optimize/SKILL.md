---
name: optimize
description: Profile and optimize a slow operation using cargo bench and release builds
---

# Performance Optimization Workflow

Profile and optimize a slow Rust operation.

**Core constraint**: never let a single profiling run exceed 2 minutes.

## Steps

1. **Baseline profiling run** — build in release mode and measure:
   ```bash
   cargo build --release 2>&1
   cargo bench 2>&1 | head -50
   ```
   If no benchmarks exist, time the target binary directly:
   ```bash
   time cargo run --release -- <args>
   ```

2. **Analyze profile** — identify:
   - Which functions dominate cumulative time?
   - Unnecessary allocations or clones?
   - Repeated parsing or serialization?
   - Missing iterator chains (collecting then iterating again)?

3. **Identify all optimization opportunities** — list everything before implementing:
   - **Allocation**: reduce clones, use `&str` over `String`, reuse buffers
   - **Algorithmic**: reduce complexity, use appropriate data structures (`HashMap` vs `BTreeMap`)
   - **I/O**: batch operations, use buffered readers/writers
   - **Iterator chains**: replace `collect()` + loop with chained iterators
   - **Parallelism**: use `rayon` for CPU-bound work where applicable
   - **Early exit**: short-circuit with `find`, `any`, `take_while`

4. **Implement all optimizations in one pass**. Follow existing code conventions.

5. **Verify tests pass**:
   ```bash
   cargo fmt --all
   cargo clippy --tests -- -D warnings
   cargo test
   ```

6. **Measure improvement** — re-run profiling, compare to baseline.

7. **Iterate** — repeat steps 2-6 until no new opportunities are visible.

## Rules

- 2-minute cap per profiling run.
- Always profile release builds (`--release`), never debug builds.
- Batch all optimizations — identify everything, then implement in one pass.
- Tests must pass after every implementation pass — no exceptions.
- Never sacrifice correctness for speed.
