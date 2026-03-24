---
name: spec-finalize
description: Finalize an implementation spec by incorporating accepted review/critique findings. Produces updated spec and DECISIONS.md. Best run with Claude.
argument-hint: <spec-path>
disable-model-invocation: true
---

# Finalize Implementation Spec

Read and follow the instructions in `context/prompts/spec-finalize.md` for the spec at `$ARGUMENTS`.

The full instructions are in that file. Key points:

1. Read all review/critique artifacts in `$ARGUMENTS/spec-reviews/`
2. Present each finding to the human for accept/reject decision
3. Update `IMPLEMENTATION_SPEC.md` with accepted changes
4. Write `DECISIONS.md` documenting every finding's resolution
5. Commit and push
6. **MANDATORY: Post conversation summary to the issue using `gh issue comment <issue-number> --body "..."`** — follow `context/PROCESS.md` for the comment format
7. **Update labels:** `gh issue edit <issue-number> --add-label "spec:approved"`
8. **Generate ready-to-paste prompt** for spec-implement in the issue comment
