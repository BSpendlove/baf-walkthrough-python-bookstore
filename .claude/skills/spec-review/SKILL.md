---
name: spec-review
description: Review an implementation spec for completeness, correctness, and best practices. Produces a review document with severity-rated findings. Recommended for Gemini but works with any agent.
argument-hint: <spec-path>
disable-model-invocation: true
---

# Review Implementation Spec

Read and follow the instructions in `context/prompts/spec-review.md` for the spec at `$ARGUMENTS`.

The full instructions are in that file. Key points:

1. Read `context/PROCESS.md` for review guidelines
2. Read the spec at `$ARGUMENTS/IMPLEMENTATION_SPEC.md`
3. Read ALL comments on the source issue for conversation history
4. Produce severity-rated findings (CRITICAL/HIGH/MEDIUM/LOW)
5. Write review to `$ARGUMENTS/spec-reviews/REVIEW.md`
6. Commit and push
7. **MANDATORY: Post conversation summary to the issue using `gh issue comment <issue-number> --body "..."`** — follow `context/PROCESS.md` for the comment format
8. **Update labels:** `gh issue edit <issue-number> --add-label "phase:review"`
