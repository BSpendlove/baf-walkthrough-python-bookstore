---
name: spec-create
description: Create an implementation spec from a GitHub issue. Reads the issue, analyzes the codebase, and drafts a structured spec with implementation plan. Best run with Claude.
argument-hint: <issue-number>
disable-model-invocation: true
---

# Create Implementation Spec

Read and follow the instructions in `context/prompts/spec-create.md` for issue #$ARGUMENTS.

The full instructions are in that file. Key points:

1. Read `context/PROCESS.md` and `context/SUMMARY.md` first
2. Read the issue via `gh issue view $ARGUMENTS --json title,body,labels,state,number,comments`
3. Analyze the codebase
4. Draft `IMPLEMENTATION_SPEC.md` and `README.md` in `context/specs/$ARGUMENTS-<slug>/`
5. Create a feature branch, commit, and push
6. **MANDATORY: Post the conversation summary to the issue using `gh issue comment $ARGUMENTS --body "..."`** — this is the most important step. Follow `context/PROCESS.md` for the comment format. Without this, the entire workflow breaks.
7. **Generate ready-to-paste prompts** for the next agents in the issue comment — so the human can copy them into Gemini, Codex, or another agent for spec-review and spec-critique
8. **Update labels:** `gh issue edit $ARGUMENTS --add-label "phase:spec"`
