# spec-critique

Critique an implementation spec for architectural gaps, missing edge cases, failure modes, and scope issues.

**Recommended agent:** OpenAI / Codex (strong at finding what's NOT there)

## Instructions

You are critiquing an implementation spec. You focus on what's missing or broken, not what's good. You do NOT edit the spec directly.

### Input
- **Spec path** — provided by the human (e.g., `context/specs/42-bookstore-api/`)

### Steps

1. **Read the workflow process**
   - Read `context/PROCESS.md` for critique guidelines and severity scale

2. **Read the spec**
   - Read `<spec-path>/IMPLEMENTATION_SPEC.md`
   - Read `<spec-path>/README.md` for context

3. **Read the source issue and conversation history**
   - Extract the issue number from the spec's "Source Issue" section
   - Run: `gh issue view <number> --json title,body,labels,comments`
   - Read ALL existing comments — previous conversation history gives you the reasoning behind decisions

4. **Analyze the codebase**
   - Read files referenced in the spec's File Plan
   - Look at the broader architecture around the changes

5. **Focus your critique on what's NOT there:**
   - Missing failure paths and error handling
   - Unaddressed edge cases
   - Architectural gaps or inconsistencies
   - Scope creep or scope gaps
   - Missing rollback / undo considerations
   - Security implications not addressed
   - Dependencies or ordering issues in the implementation plan

6. **Produce findings** using the severity scale:
   - **CRITICAL** — will cause failures, security vulnerabilities, or broken builds
   - **HIGH** — significant bugs or missing functionality the spec promised
   - **MEDIUM** — edge cases, performance issues, non-ideal error handling
   - **LOW** — cosmetic issues, future-proofing concerns

   Each finding: **title**, **severity**, **description**, **suggested resolution**

7. **Write the critique**
   - Output to: `<spec-path>/spec-reviews/CRITIQUE.md` (or use your agent name: `CODEX.md`, `OPENAI.md`, etc.)
   - Do NOT edit the spec directly

8. **Commit and push**
   - Commit: `docs(review): add spec critique for <slug> (#<issue-number>)`
   - Push to the current branch

9. **Post conversation summary to the GitHub issue (MANDATORY)**
   - You MUST post a comment using `gh issue comment <issue-number> --body "..."`. This is not optional.
   - Follow the conversation tracking rules and comment format in `context/PROCESS.md`
   - Include finding counts by severity and key findings
   - Add label: `gh issue edit <issue-number> --add-label "phase:review"`

## Constraints

- Focus on what's missing or broken, not what's good
- Every finding must be specific and actionable
- Do NOT modify the spec — only produce the critique document
- If there are no real issues, say so honestly
