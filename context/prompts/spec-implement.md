# spec-implement

Implement code from a finalized spec.

**Recommended agent:** Claude (needs codebase access to write and commit code)

## Instructions

You are implementing the code described in a finalized spec.

### Input
- **Spec path** — provided by the human (e.g., `context/specs/42-bookstore-api/`)

### Steps

1. **Read the workflow process**
   - Read `context/PROCESS.md` for implementation rules
   - Read `context/SUMMARY.md` for project state

2. **Read the spec**
   - Read `<spec-path>/IMPLEMENTATION_SPEC.md` — this is your blueprint
   - Read `<spec-path>/DECISIONS.md` if it exists — respect all decisions made
   - Read `<spec-path>/README.md` for status

3. **Read the issue conversation history**
   - Run: `gh issue view <number> --json comments`
   - Read ALL comments for full context — requirements clarifications, design decisions

4. **Verify gate**
   - Check the source issue has `spec:approved` label
   - If not approved, stop and tell the human

5. **Check out the feature branch**
   - The branch was created during spec-create. Check it out.
   - `git pull` to get latest
   - Do NOT create a new branch

6. **Implement following the spec's Implementation Order**
   - Follow the numbered steps exactly
   - One commit per logical unit
   - Each commit: `<type>(<scope>): <description>`
   - Follow existing codebase patterns and conventions
   - Write tests as specified

7. **Create a PR**
   - PR title: `<type>(<scope>): <description>`
   - PR body: summary, `Closes #<issue-number>`, spec link, file list, testing checklist

8. **Update context/SUMMARY.md**
   - Add the completed spec to Completed Specs table
   - Record any key decisions that affect future work

9. **Post conversation summary to the GitHub issue (MANDATORY)**
   - You MUST post a comment using `gh issue comment <issue-number> --body "..."`. This is not optional.
   - Follow the conversation tracking rules and comment format in `context/PROCESS.md`
   - Include PR link, file list
   - Add label: `gh issue edit <issue-number> --add-label "phase:implementation"`
   - Generate handoff prompt for spec-final-review if desired

## Constraints

- Implement ONLY what the spec describes
- If you discover something out of scope, note it but do NOT implement it
- Follow the implementation order from the spec
- Creating the PR is mandatory
