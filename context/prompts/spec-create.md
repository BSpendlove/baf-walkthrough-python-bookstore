# spec-create

Create an implementation spec from a GitHub issue.

**Recommended agent:** Claude (needs codebase access to ground the spec in real file paths)

## Instructions

You are drafting an implementation spec for a GitHub issue.

### Input
- **Issue number** — provided by the human

### Steps

1. **Read the workflow process**
   - Read `context/PROCESS.md` for the full workflow definition
   - Read `context/SUMMARY.md` for current project state and key decisions

2. **Read the issue**
   - Run: `gh issue view <issue-number> --json title,body,labels,state,number,comments`
   - Extract: what, why, acceptance criteria, scope boundary, agent preferences
   - Read all existing comments — previous phases may have left context
   - Do NOT ask the human to re-explain what is already in the issue

3. **Analyze the codebase**
   - Read files relevant to the issue
   - Understand existing patterns, conventions, and architecture
   - Identify files that will need to be created or modified

4. **Derive the spec directory**
   - Slug: lowercase-hyphenated short description from the issue title
   - Path: `context/specs/<issue-number>-<slug>/`
   - Create the directory and subdirectories: `spec-reviews/`, `code-reviews/`

5. **Create a feature branch** (if one doesn't already exist for this issue)
   - `git checkout main && git pull && git checkout -b <type>/<scope>-<description>`
   - Branch prefix matches commit type: `feat/`, `fix/`, `test/`, `docs/`, etc.

6. **Write IMPLEMENTATION_SPEC.md** with these sections (in order):
   1. **Overview** — what and why, 2-3 sentences
   2. **Source Issue** — issue number with link
   3. **Current State** — what exists today relevant to this work
   4. **Design** — architecture, data flow, key decisions
   5. **Configuration** — env vars, config files, examples (if applicable)
   6. **File Plan** — every file to create/modify with purpose
   7. **Implementation Order** — numbered steps, each independently testable
   8. **Testing** — what to test and how
   9. **Not In Scope** — explicit exclusions from the issue

7. **Write README.md** (status tracker) with:
   - One-line description
   - Source issue link
   - Status table (spec-create: Complete, all others: Not Started)
   - Key files list
   - Dependencies (upstream/downstream)

8. **Commit and push**
   - Commit: `docs(spec): draft implementation spec for <slug> (#<issue-number>)`
   - Push the branch

9. **Post conversation summary to the GitHub issue (MANDATORY)**
   - You MUST post a comment to the issue using `gh issue comment <issue-number> --body "..."`. This is not optional.
   - Follow the conversation tracking rules and comment format in `context/PROCESS.md`
   - Include the full dialogue — questions, debates, pivots, decisions
   - Generate ready-to-paste prompts for the next phase agents (see below)
   - Add label: `gh issue edit <issue-number> --add-label "phase:spec"`

10. **Generate handoff prompts** for the next agents. Include these in the issue comment so the human can copy-paste them into Gemini, Codex, or another agent:

    **For spec-review (paste into Gemini or another agent):**
    ```
    Read the following files in this repo:
    - context/PROCESS.md (workflow rules)
    - context/prompts/spec-review.md (your instructions)
    - context/specs/<N>-<slug>/IMPLEMENTATION_SPEC.md (the spec to review)
    - context/specs/<N>-<slug>/README.md (status)

    Also read all comments on GitHub issue #<N> for conversation history:
    gh issue view <N> --json comments

    Then execute the spec-review instructions.
    ```

    **For spec-critique (paste into Codex or another agent):**
    ```
    Read the following files in this repo:
    - context/PROCESS.md (workflow rules)
    - context/prompts/spec-critique.md (your instructions)
    - context/specs/<N>-<slug>/IMPLEMENTATION_SPEC.md (the spec to critique)

    Also read all comments on GitHub issue #<N> for conversation history:
    gh issue view <N> --json comments

    Then execute the spec-critique instructions.
    ```

## Constraints

- Do NOT invent requirements beyond what the issue states
- Do NOT propose changes outside the issue's scope boundary
- Reference real file paths from the codebase
- Follow existing codebase conventions
- The spec must be concrete enough that a different agent could implement from it

## Re-running

If run again for the same issue (e.g., after feedback):
- Check out the existing branch
- Read existing spec artifacts and issue comments for context
- Update the spec rather than starting from scratch
- Note in the GitHub comment that this is a re-run and what changed
