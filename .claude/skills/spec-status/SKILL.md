---
name: spec-status
description: Show the current workflow status for a spec or issue. Displays phase progress, pending reviews, and next steps.
argument-hint: [issue-number or spec-path]
disable-model-invocation: true
---

# Spec Workflow Status

Show the current workflow status for `$ARGUMENTS`.

## Steps

1. **Determine what was passed**
   - If `$ARGUMENTS` is a number: it's an issue number, derive the spec path from `context/specs/`
   - If `$ARGUMENTS` is a path: use it directly
   - If blank: list all specs in `context/specs/` with their status

2. **If listing all specs:**
   - Scan `context/specs/*/README.md`
   - For each, extract: issue number, one-line description, current phase status
   - Print a summary table
   - Stop here

3. **If showing a specific spec:**
   - Read `$ARGUMENTS/README.md` for phase status
   - Read `$ARGUMENTS/IMPLEMENTATION_SPEC.md` for overview
   - Check `$ARGUMENTS/spec-reviews/` for review documents
   - Check `$ARGUMENTS/code-reviews/` for code review documents
   - Check git branch status: `git branch -a | grep <slug>`
   - Check for open PRs: `gh pr list --search "<slug>"`
   - Check issue labels: `gh issue view <number> --json labels`

4. **Print status report:**
   - Issue number and title
   - Current branch (if any)
   - Phase progress table
   - Files produced so far
   - Pending actions / next steps
   - Recommended next skill to run and suggested agent
