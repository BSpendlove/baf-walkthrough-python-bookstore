---
name: spec-critique
description: Critique an implementation spec for architectural gaps, missing edge cases, failure modes, and scope issues. Recommended for OpenAI/Codex but works with any agent.
argument-hint: <spec-path>
disable-model-invocation: true
---

# Critique Implementation Spec

Read and follow the instructions in `context/prompts/spec-critique.md` for the spec at `$ARGUMENTS`.

The full instructions are in that file. Key points:

1. Read `context/PROCESS.md` for critique guidelines
2. Read the spec at `$ARGUMENTS/IMPLEMENTATION_SPEC.md`
3. Read ALL comments on the source issue for conversation history
4. Focus on what's NOT there — missing failure paths, edge cases, architectural gaps
5. Write critique to `$ARGUMENTS/spec-reviews/CRITIQUE.md`
6. Commit and push
7. **MANDATORY: Post conversation summary to the issue using `gh issue comment <issue-number> --body "..."`** — follow `context/PROCESS.md` for the comment format
8. **Update labels:** `gh issue edit <issue-number> --add-label "phase:review"`
