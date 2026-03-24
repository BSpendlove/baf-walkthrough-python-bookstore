# baf — BYOA Framework

LLM-driven GitHub issue workflow template. Contributors bring their own AI agents (BYOA) to work through issues using structured skills.

## How This Works

All work starts from a **GitHub issue**. Contributors use AI agent skills to move issues through a spec-driven workflow. **Claude is the recommended orchestrator** — it drives the core phases (spec-create, spec-finalize, spec-implement) and generates handoff prompts for other agents. Gemini and Codex are brought in for review and critique where their strengths shine. Any agent can run any skill, but Claude as the backbone produces the most coherent results. See `context/PROCESS.md` for details.

## Available Skills

| Skill | Purpose | Recommended Agent |
|-------|---------|-------------------|
| `/spec-create <issue>` | Draft implementation spec from a GitHub issue | Claude |
| `/spec-review <spec-path>` | Review spec for completeness and correctness | Gemini |
| `/spec-critique <spec-path>` | Critique spec for gaps and edge cases | OpenAI / Codex |
| `/spec-finalize <spec-path>` | Finalize spec, incorporate review feedback | Claude |
| `/spec-implement <spec-path>` | Implement code from finalized spec | Claude |
| `/spec-final-review <spec-path>` | Post-implementation code review | Any agent |
| `/spec-status [issue or path]` | Show workflow status | Any agent |

## Workflow Summary

```
Issue → spec-create → spec-review → spec-finalize → spec-implement → spec-final-review
                    → spec-critique ↗       (optional)                   (optional)
```

Contributors can skip optional steps. Minimum viable path: `spec-create → spec-finalize → spec-implement`.

## Repository Layout

```
.claude/skills/          # Workflow skills (the core of this template)
context/
├── PROCESS.md           # Full workflow definition, rules, formats
├── SUMMARY.md           # Project state tracker
└── specs/               # Implementation specs (one per issue)
    └── <N>-<slug>/
        ├── IMPLEMENTATION_SPEC.md
        ├── README.md              # Status tracker
        ├── DECISIONS.md           # Accept/reject rationale
        ├── spec-reviews/          # Review + critique artifacts
        └── code-reviews/          # Post-implementation reviews
.github/ISSUE_TEMPLATE/  # Structured issue templates
```

## Starting Work

1. Read the issue: `gh issue view <number>`
2. Read `context/PROCESS.md` for the full workflow
3. Read `context/SUMMARY.md` for project state and key decisions
4. Run the appropriate skill

## Conversation Tracking

**Every skill, every phase, always.** The GitHub issue is the single source of truth for the full conversation history around that issue. This means:

1. **Read issue comments before starting** — previous phases leave full conversation logs (human-agent dialogue, decisions, rejected approaches, context). Always read them.
2. **Capture the dialogue as it happens** — when a human and agent go back-and-forth (debating approaches, refining requirements, changing direction), that conversation gets posted to the issue. Not just the final output — the reasoning, the rejections, the pivots. Post summaries mid-conversation at major decision points, not just when the skill finishes.
3. **Post a structured completion comment** — when a skill finishes, post the full conversation log (see `context/PROCESS.md` for format).
4. **Sanitize everything posted** — the following must NEVER appear in GitHub comments:
   - API keys, tokens, passwords, or secrets of any kind
   - Email addresses or personally identifiable information (PII)
   - Absolute local file paths (use repo-relative paths)
   - Credentials from command outputs
   - Any environment variable values that could be sensitive

The issue should read like a decision journal. Anyone picking it up — human or agent — can understand not just what was decided, but *why*, what was rejected, and what the human's intent was.

## Labels

Labels track workflow state on issues. Agents should read and update them:

| Label | Meaning |
|-------|---------|
| `approved` | Issue approved for work |
| `phase:spec` | Spec is being drafted |
| `phase:review` | Spec is under review/critique |
| `spec:approved` | Spec finalized, ready for implementation |
| `phase:implementation` | Code is being written |
| `phase:done` | All work complete, PR merged |
| `priority:p0` | Critical path |
| `priority:p1` | Important |
| `priority:p2` | Nice to have |

## Conventions

- **Commits:** Conventional Commits format — `<type>(<scope>): <description>`
- **Branches:** `<type>/<scope>-<description>` — e.g., `feat/add-auth`, `fix/login-redirect`
- **Scope:** One feature per PR. One PR per issue. No bundling.
- **Specs:** `context/specs/<issue-number>-<slug>/` — deterministic from issue number + title
