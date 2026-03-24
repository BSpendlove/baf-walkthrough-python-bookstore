# Workflow Process

This project uses a structured, skill-driven workflow for spec writing, review, and implementation. All participating agents read this file as their entry point.

## Overview

All work starts from a **GitHub issue**. Issues are the single source of truth for requirements. Contributors use AI agent skills to move issues through a spec-driven pipeline. Each skill is agent-agnostic but some agents are better suited to certain tasks.

## Recommended Agents

**Claude as the orchestrator.** During testing, Claude consistently produced the best results as the primary agent driving the workflow end-to-end. It handles the phases that require deep codebase understanding (spec-create, spec-finalize, spec-implement) and generates the handoff prompts that coordinate other agents. We recommend using Claude Code as the backbone of the workflow, bringing in Gemini and Codex for the phases where their specific strengths shine.

Any agent *can* run any skill — these are suggestions, not requirements.

| Skill | Best Agent | Why |
|-------|-----------|-----|
| `spec-create` | **Claude** | Direct codebase access, grounds spec in real file paths and patterns |
| `spec-review` | **Gemini** | Large context window excels at cross-referencing spec against best practices |
| `spec-critique` | **OpenAI / Codex** | Strong at finding what's NOT there — missing failure paths, edge cases |
| `spec-finalize` | **Claude** | Needs codebase access to update spec with accepted changes |
| `spec-implement` | **Claude** | Needs codebase access to write and commit code |
| `spec-final-review` | **Any** | Each agent brings different review strengths |

## Workflow Paths

### Full workflow (recommended for complex features)
```
spec-create → spec-review → spec-critique → spec-finalize → spec-implement → spec-final-review
```

### Standard workflow (most issues)
```
spec-create → spec-review → spec-finalize → spec-implement
```

### Minimal workflow (small changes, bug fixes)
```
spec-create → spec-finalize → spec-implement
```

### Skip the spec (trivial fixes)
For typos, one-line fixes, or documentation corrections — just fix it, commit, and open a PR. Not everything needs a spec.

## Issue Requirements

Issue templates enforce a consistent format. Each issue that triggers the spec workflow must capture:

- **What** — the specific deliverable
- **Why** — the motivation or problem being solved
- **Acceptance criteria** — how to know it's done
- **Not in scope** — what is explicitly NOT part of this issue
- **Workflow agents** — which agents should participate (suggestion, not requirement)

## Scope Rules

**One feature per PR. One PR per issue. No exceptions.**

- A PR implements exactly one issue
- Do not bundle unrelated changes
- If implementation reveals a needed change outside scope, file a new issue
- Bug fixes and trivial changes can skip the spec workflow

## Spec Directory Convention

Every issue going through the spec workflow gets a directory:

```
context/specs/<issue-number>-<slug>/
```

Where `<slug>` is a short lowercase-hyphenated description from the issue title. This is deterministic — any agent can derive the path.

### Directory structure
```
<issue-number>-<slug>/
├── IMPLEMENTATION_SPEC.md     # The spec (created by spec-create)
├── README.md                  # Status tracker
├── DECISIONS.md               # Accept/reject rationale (created by spec-finalize)
├── spec-reviews/              # Review and critique artifacts
│   ├── REVIEW.md              # From spec-review (or agent-named: GEMINI.md, etc.)
│   └── CRITIQUE.md            # From spec-critique (or agent-named: CODEX.md, etc.)
└── code-reviews/              # Post-implementation reviews
    └── REVIEW.md              # From spec-final-review
```

## Spec Format

### IMPLEMENTATION_SPEC.md sections (in order)

1. **Overview** — what and why, 2-3 sentences
2. **Source Issue** — link to the GitHub issue
3. **Current State** — what exists today
4. **Design** — architecture, data flow, key decisions
5. **Configuration** — env vars, config files, examples (if applicable)
6. **File Plan** — every file to create/modify with purpose
7. **Implementation Order** — numbered steps, each independently testable
8. **Testing** — what to test and how
9. **Not In Scope** — explicit exclusions

### DECISIONS.md format

```markdown
# Decisions: <issue-number>-<slug>

## Accepted

### <finding title>
- **Source:** <agent name>
- **Severity:** CRITICAL | HIGH | MEDIUM | LOW
- **Resolution:** <what was changed in the spec>

## Rejected

### <finding title>
- **Source:** <agent name>
- **Severity:** CRITICAL | HIGH | MEDIUM | LOW
- **Rationale:** <why this was rejected>
```

## Severity Scale

All agents use these definitions when producing findings:

| Severity | Definition |
|----------|------------|
| **CRITICAL** | Will cause failures, security vulnerabilities, or broken builds |
| **HIGH** | Significant bugs or missing functionality the spec promised |
| **MEDIUM** | Edge cases, performance issues, non-ideal error handling |
| **LOW** | Cosmetic issues, future-proofing concerns |

## Branching and Commits

### Branch naming
```
<type>/<scope>-<description>
```
Type matches the commit type: `feat/`, `fix/`, `test/`, `docs/`, `refactor/`, `ci/`, `chore/`

### Commit messages
Conventional Commits format:
```
<type>(<scope>): <description>
```
Types: `feat`, `fix`, `docs`, `refactor`, `test`, `ci`, `chore`, `build`

### Branch lifecycle
- Created during `spec-create` — all work for the issue lives on this branch
- Review agents commit their artifacts to the same branch
- Implementation happens on the same branch
- PR is created from this branch at the end of `spec-implement`

## Amendments

Requirements evolve. When they change:

1. **Before spec exists:** Edit the issue body directly
2. **After spec exists:** Comment on the issue describing the amendment. The agent running the next skill reads the comment and updates the spec. An AMENDMENT entry is added to DECISIONS.md.
3. **During implementation:** Comment on the issue or PR. The implementing agent adjusts.

Amendments must stay within the original issue's scope. If the amendment is a new feature, file a new issue.

## Anti-Patterns (All Agents)

1. **Capability summaries** — "The implementation supports X, Y, and Z" is not a review finding
2. **Style reviews** — do not comment on naming, formatting, or code style
3. **Speculative issues** — "this could potentially..." without a concrete scenario is noise
4. **Generic recommendations** — "consider adding more tests" is not actionable
5. **Scope creep** — do not add requirements beyond what the issue states

## Conversation Tracking & Issue History

The GitHub issue is the **living record** of every conversation that happens around it. This is not a post-hoc step — it happens continuously, in every skill, at any point.

### How to post to the issue

Use the `gh` CLI. This is not optional — every skill MUST post at least one comment before finishing.

```bash
# Post a comment to the issue
gh issue comment <issue-number> --body "your comment body here"

# For long comments, use a heredoc
gh issue comment <issue-number> --body "$(cat <<'COMMENT'
## 📋 spec-create — Complete

**Agent:** Claude
...rest of comment...
COMMENT
)"

# Update labels
gh issue edit <issue-number> --add-label "phase:spec"
```

### Rules (all agents, all phases, always)

1. **Read before you act.** Before starting any skill, read ALL comments on the issue. They contain conversation summaries, decisions, context, and amendments from every previous interaction — human or agent. This is your primary context source.

2. **Capture the dialogue, not just the result.** The issue must record the *conversation* — the back-and-forth between human and agent. When a human says "what about approach X?", the agent responds, the human pushes back, they iterate — all of that reasoning gets captured. The issue should read like a decision journal, not a changelog.

3. **Post throughout the conversation, not just at the end.** Conversations are messy. The human might change direction three times, reject two approaches, and settle on a third. Capture this as it happens:

   - **After significant decisions** — "Human asked about caching, we discussed Redis vs in-memory, decided on Redis because of X"
   - **After direction changes** — "Human initially wanted approach A, but after discussing trade-offs, pivoted to B because Y"
   - **After requirements refinement** — "Human clarified that the API also needs to support Z, which wasn't in the original issue"
   - **When the skill completes** — final structured summary of everything that happened

   Don't wait until you're "done" to post. If a conversation has 15 messages of back-and-forth, post a summary after major turning points so the context is captured even if the session crashes or gets interrupted.

4. **Structured completion comment.** When a skill finishes, post:

   ```markdown
   ## <emoji> <skill-name> — <status>

   **Agent:** <agent name/model>
   **Branch:** `<branch-name>` (if applicable)

   ### Summary
   <what was done, key decisions made, 2-5 sentences>

   ### Artifacts
   - `path/to/artifact` — description

   ### Next Steps
   <what to do next, which skill, suggested agent>

   <details>
   <summary>Conversation Log</summary>

   **Full dialogue summary** — not just outcomes, but the reasoning path:

   1. Human asked about <topic>. Agent proposed <approach A>.
   2. Human raised concern about <X>. Agent agreed and suggested <approach B> instead.
   3. Human asked "what about <edge case>?" Agent added handling for it in the spec.
   4. Human rejected <design choice> because <reason>. Went with <alternative>.
   5. Final agreement: <what was decided and why>

   **Key decisions:**
   - Chose X over Y because <rationale>
   - Explicitly excluded Z per human's direction

   **Open questions (if any):**
   - <anything unresolved that the next phase should address>

   </details>
   ```

   Skill emojis: spec-create `📋`, spec-review `🔍`, spec-critique `🔬`, spec-finalize `✅`, spec-implement `🔨`, spec-final-review `🔎`

5. **Update labels.** When transitioning between phases, update the issue labels to reflect current state (see Labels section).

### What gets captured

Every interaction that shapes the work:

- **Requirements discussions** — human and agent refining what to build
- **Design debates** — approaches considered, trade-offs discussed, choices made
- **Rejections and pivots** — "we tried X, human said no because Y, went with Z"
- **Clarifications** — "human clarified that 'users' means only authenticated users"
- **Scope negotiations** — "human wanted to add feature X, agent flagged it as out of scope, human agreed to file a separate issue"
- **Feedback and corrections** — "human said the spec missed edge case X, agent added it"

### What does NOT get captured

- Raw tool output (file contents, grep results, etc.)
- Internal agent reasoning/chain-of-thought
- Anything covered by sanitization rules (see below)

### Sanitization Rules (mandatory, no exceptions)

Before posting ANY content to a GitHub issue comment, strip:

- **API keys, tokens, secrets** — any string that looks like a credential (`sk-...`, `ghp_...`, `AIza...`, Bearer tokens, etc.)
- **Passwords** — never post passwords, even hashed
- **Email addresses and PII** — names tied to accounts, phone numbers, addresses
- **Absolute local paths** — replace with repo-relative paths (e.g., `/home/user/project/src/foo.py` → `src/foo.py`)
- **Environment variable values** — reference the variable name, not its value
- **Command outputs containing credentials** — sanitize before posting
- **Private repository URLs or internal hostnames** — unless the issue is in that same repo

If in doubt, don't post it. The conversation summary should capture decisions and rationale, not raw terminal output.

### Why This Matters

- **Any contributor** (human or agent) can pick up where the last one left off by reading the issue
- **Maintainers** get full visibility into what agents did and why
- **Audit trail** — every decision is recorded, traceable, and reversible
- **Cross-agent handoff** — agent A (Claude) does spec-create, agent B (Gemini) does spec-review, and B has full context from A's summary

## Labels

Labels track workflow state and metadata. Agents should read and update them.

### Workflow State

| Label | Applied When | Removed When |
|-------|-------------|--------------|
| `approved` | Human approves the issue for work | Never (audit trail) |
| `phase:spec` | spec-create starts | spec-finalize completes |
| `phase:review` | spec-review or spec-critique starts | spec-finalize completes |
| `spec:approved` | Spec finalized and approved | Never (audit trail) |
| `phase:implementation` | spec-implement starts | spec-implement completes |
| `phase:done` | All phases complete, PR merged | Never (audit trail) |

### Priority

| Label | Meaning |
|-------|---------|
| `priority:p0` | Critical path — blocks other work |
| `priority:p1` | Important — do soon |
| `priority:p2` | Nice to have |

### Agent Selection (informational)

| Label | Meaning |
|-------|---------|
| `agents:single` | One agent handles everything |
| `agents:two` | Add spec-review |
| `agents:three` | Add spec-review + spec-critique |
| `agents:full` | All skills including spec-final-review |

### Issue Type

Auto-applied by templates: `feature`, `bug`, `enhancement`
