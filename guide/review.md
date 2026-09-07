# Review Discipline

Use a skeptical review stance: correctness and simplicity beat cleverness and speed.

## Review Checklist

For each meaningful change, ask:

- Does the change solve the requested problem with the simplest adequate approach and without unrelated refactoring?
- Could it regress existing interfaces, configuration, output shapes, error paths, or edge cases?
- Are tests and documentation appropriate for the risk, and are root-cause or performance claims supported by evidence?
- Are abstractions and configurable values justified by actual repetition or a clear boundary?
- Did the change touch generated, local, secret, or other out-of-scope files?

## NACK Triggers

Treat these as blockers unless the user explicitly accepts the risk:

- Hidden behavior changes without suitable tests or migration notes.
- Broad rewrites, dependencies, abstractions, or optimizations without evidence they are needed.
- Fixes without a supported causal explanation, targeted verification, or correctness argument.
- Duplicated policy in vendor entrypoints or an agent sync that changes application source.

## Summary Standard

Final summaries should include changed files grouped by purpose, verification commands and results, preserved manual content, and remaining risks or follow-up items.
