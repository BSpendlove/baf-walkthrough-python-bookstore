---
name: spec-final-review
description: Post-implementation code review. Reviews the implemented code against the spec for bugs, spec compliance, and best practices. Any agent can run this.
argument-hint: <spec-path>
disable-model-invocation: true
---

# Post-Implementation Code Review

Read and follow the instructions in `context/prompts/spec-final-review.md` for the spec at `$ARGUMENTS`.

The full instructions are in that file. Key points:

1. Read the spec and all implemented files
2. Read the full diff: `git diff main...HEAD`
3. Review for bugs, spec compliance, and best practices
4. Write review to `$ARGUMENTS/code-reviews/REVIEW.md`
5. Commit and push
6. **MANDATORY: Post conversation summary to the issue using `gh issue comment <issue-number> --body "..."`** — follow `context/PROCESS.md` for the comment format
