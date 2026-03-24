---
name: spec-implement
description: Implement code from a finalized spec. Follows the spec's file plan and implementation order. Best run with Claude.
argument-hint: <spec-path>
disable-model-invocation: true
---

# Implement From Spec

Read and follow the instructions in `context/prompts/spec-implement.md` for the spec at `$ARGUMENTS`.

The full instructions are in that file. Key points:

1. Read `$ARGUMENTS/IMPLEMENTATION_SPEC.md` — this is your blueprint
2. Verify the issue has `spec:approved` label
3. Check out the existing feature branch
4. Implement following the spec's Implementation Order
5. One commit per logical unit
6. Create a PR with summary, file list, and testing checklist
7. Update `context/SUMMARY.md`
8. **MANDATORY: Post conversation summary to the issue using `gh issue comment <issue-number> --body "..."`** — follow `context/PROCESS.md` for the comment format
9. **Update labels:** `gh issue edit <issue-number> --add-label "phase:implementation"`
10. **Generate ready-to-paste prompt** for spec-final-review if desired
