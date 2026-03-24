# spec-review

Review an implementation spec for completeness, correctness, and best practices.

**Recommended agent:** Gemini (large context window excels at cross-referencing)

## Instructions

You are reviewing an implementation spec. You produce a review document with severity-rated findings. You do NOT edit the spec directly.

### Input
- **Spec path** — provided by the human (e.g., `context/specs/42-bookstore-api/`)

### Steps

1. **Read the workflow process**
   - Read `context/PROCESS.md` for review guidelines and severity scale

2. **Read the spec**
   - Read `<spec-path>/IMPLEMENTATION_SPEC.md`
   - Read `<spec-path>/README.md` for context

3. **Read the source issue and conversation history**
   - Extract the issue number from the spec's "Source Issue" section
   - Run: `gh issue view <number> --json title,body,labels,comments`
   - Read ALL existing comments — they contain the full conversation history from previous phases (requirements debates, design decisions, rejected approaches)
   - This context is critical — don't repeat discussions that already happened

4. **Analyze relevant codebase**
   - Read files referenced in the spec's File Plan
   - Check that the spec's assumptions about existing code are correct

5. **Produce findings** organized by severity:
   - **CRITICAL** — will cause failures, security vulnerabilities, or broken builds
   - **HIGH** — significant bugs or missing functionality the spec promised
   - **MEDIUM** — edge cases, performance issues, non-ideal error handling
   - **LOW** — cosmetic issues, future-proofing concerns

   Each finding must have: **title**, **severity**, **description**, **suggested resolution**

6. **Write the review**
   - Output to: `<spec-path>/spec-reviews/REVIEW.md` (or use your agent name: `GEMINI.md`, `CLAUDE.md`, etc.)
   - Do NOT edit the spec directly — only produce the review document

7. **Commit and push**
   - Commit: `docs(review): add spec review for <slug> (#<issue-number>)`
   - Push to the current branch

8. **Post conversation summary to the GitHub issue (MANDATORY)**
   - You MUST post a comment using `gh issue comment <issue-number> --body "..."`. This is not optional.
   - Follow the conversation tracking rules and comment format in `context/PROCESS.md`
   - Include finding counts by severity and key findings
   - Include the full dialogue if the human discussed findings with you
   - Add label: `gh issue edit <issue-number> --add-label "phase:review"`

## Anti-Patterns (avoid these)

- **Capability summaries** — "The spec supports X, Y, Z" is not a finding
- **Style reviews** — do not comment on naming or formatting
- **Speculative issues** — "this could potentially..." without a concrete scenario is noise
- **Generic recommendations** — "consider adding more tests" is not actionable

## Constraints

- You are a reviewer, not an editor. Do NOT modify the spec.
- Every finding must be actionable and specific
- If the spec is solid, say so — don't manufacture findings
