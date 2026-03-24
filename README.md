# Bookstore API

This project uses the [baf](https://github.com/BSpendlove/baf) workflow — an LLM-driven development process where every conversation is tracked on GitHub issues.

## Getting started

1. File a GitHub issue using one of the issue templates
2. Add the `approved` label
3. Open your AI agent in the repo root and run a skill:
   - **Claude Code:** `/spec-create 1`
   - **Other agents:** Read `CLAUDE.md` and `context/PROCESS.md`, then follow the workflow

## Workflow

```
Issue → spec-create → spec-review (optional) → spec-finalize → spec-implement
```

See [context/PROCESS.md](context/PROCESS.md) for the full workflow definition.

## Skills

| Skill | Purpose |
|-------|---------|
| `/spec-create <issue>` | Draft implementation spec from a GitHub issue |
| `/spec-review <path>` | Review spec for completeness |
| `/spec-critique <path>` | Critique spec for gaps and edge cases |
| `/spec-finalize <path>` | Finalize spec, incorporate feedback |
| `/spec-implement <path>` | Implement code from finalized spec |
| `/spec-final-review <path>` | Post-implementation code review |
| `/spec-status [issue]` | Show workflow status |
