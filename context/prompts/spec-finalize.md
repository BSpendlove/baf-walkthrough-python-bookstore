# spec-finalize

Finalize an implementation spec by incorporating accepted review/critique findings.

**Recommended agent:** Claude (needs codebase access to update spec accurately)

## Instructions

You are finalizing a spec by incorporating feedback from reviews and critiques.

### Input
- **Spec path** — provided by the human (e.g., `context/specs/42-bookstore-api/`)

### Steps

1. **Read the workflow process**
   - Read `context/PROCESS.md` for finalization guidelines

2. **Read everything in the spec directory**
   - `<spec-path>/IMPLEMENTATION_SPEC.md` — the current spec
   - `<spec-path>/README.md` — status tracker
   - `<spec-path>/spec-reviews/*.md` — all review and critique documents

3. **Read the issue conversation history**
   - Run: `gh issue view <number> --json comments`
   - Read ALL comments for full context

4. **Present findings to the human**
   - List every finding from all review documents
   - Group by severity (CRITICAL first)
   - For each: source agent, severity, title, description
   - Ask the human to accept or reject each finding
   - If no reviews exist, confirm the spec is final as-is

5. **Update the spec**
   - Integrate all accepted findings into `IMPLEMENTATION_SPEC.md`
   - Maintain internal consistency after changes
   - Do NOT change anything based on rejected findings

6. **Write DECISIONS.md**
   - Document every finding: accepted with resolution, or rejected with rationale
   - See `context/PROCESS.md` for the DECISIONS.md format

7. **Update README.md**
   - Mark review/critique as Complete (or Skipped)
   - Mark spec-finalize as Complete
   - Add links to DECISIONS.md and review artifacts

8. **Commit and push**
   - Commit: `docs(spec): finalize spec for <slug> (#<issue-number>)`
   - Push to the current branch

9. **Post conversation summary to the GitHub issue (MANDATORY)**
   - You MUST post a comment using `gh issue comment <issue-number> --body "..."`. This is not optional.
   - Follow the conversation tracking rules and comment format in `context/PROCESS.md`
   - Include accept/reject counts and key decisions
   - Add label: `gh issue edit <issue-number> --add-label "spec:approved"`
   - Generate handoff prompts for spec-implement

## Constraints

- The human has final say on accept/reject decisions
- Do NOT silently accept or reject — present everything for decision
- If no reviews exist, skip to confirmation and mark as final
