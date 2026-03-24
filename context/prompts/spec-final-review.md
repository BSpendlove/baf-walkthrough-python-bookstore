# spec-final-review

Post-implementation code review against the spec.

**Recommended agent:** Any (each agent brings different review strengths)

## Instructions

You are reviewing implemented code against its spec.

### Input
- **Spec path** — provided by the human (e.g., `context/specs/42-bookstore-api/`)

### Steps

1. **Read the workflow process**
   - Read `context/PROCESS.md` for review guidelines and severity scale

2. **Read the spec and implementation**
   - Read `<spec-path>/IMPLEMENTATION_SPEC.md` — what should have been built
   - Read `<spec-path>/DECISIONS.md` — what was decided
   - Read all files listed in the spec's File Plan
   - Run `git log --oneline main..HEAD` to see implementation commits
   - Run `git diff main...HEAD` to see the full diff

3. **Read the issue conversation history**
   - Run: `gh issue view <number> --json comments`
   - Understand the full context — including mid-implementation clarifications

4. **Review from three angles:**

   **Bug Hunting:**
   - Line-level bugs, race conditions, resource leaks
   - Security vulnerabilities (injection, XSS, OWASP top 10)
   - Error handling gaps

   **Spec Compliance:**
   - Did we build what the spec says?
   - What's missing from acceptance criteria?
   - What drifted from the spec?

   **Best Practices:**
   - Language/framework idioms
   - Performance concerns
   - Test coverage and quality

5. **Produce severity-rated findings**
   - Each finding references specific code (file:line)

6. **Write the review**
   - Output to: `<spec-path>/code-reviews/REVIEW.md` (or agent-named)

7. **Commit and push**
   - Commit: `docs(code-review): add code review for <slug> (#<issue-number>)`
   - Push to the current branch

8. **Post conversation summary to the GitHub issue (MANDATORY)**
   - You MUST post a comment using `gh issue comment <issue-number> --body "..."`. This is not optional.
   - Follow the conversation tracking rules and comment format in `context/PROCESS.md`
   - Include finding counts by severity, spec compliance status, and key findings

## Constraints

- Review what was actually built, not hypothetical scenarios
- Every finding must reference specific code
- Do NOT fix code — only review. Fixes come from the implementer.
