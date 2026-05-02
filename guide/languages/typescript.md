# TypeScript Agent Guide

## Naming

Follow the project’s existing TypeScript conventions first. If no convention is documented:

- Use `camelCase` for variables and functions.
- Use `PascalCase` for classes, types, interfaces, React components, and exported constructors.
- Use descriptive file names aligned with the local framework convention.

## Workflow

Typical verification, adjusted by `AI_AGENT_PROJECT.md`, is:

```bash
npm run typecheck
npm run lint
npm test
```

Use the package manager already present in the project (`npm`, `pnpm`, `yarn`, `bun`) and do not switch package managers without explicit approval.

## Logging and Output

Use the project’s structured logger when available. Avoid `console.log` for diagnostics in library or server code unless the project explicitly uses it.

## Dependencies

Do not add packages casually. Prefer platform APIs, framework utilities, or existing dependencies. If a package is necessary, update the correct manifest and lockfile together.
