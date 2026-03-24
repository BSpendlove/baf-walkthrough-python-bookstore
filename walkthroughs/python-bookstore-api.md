# Walkthrough: Python Bookstore REST API

This walkthrough shows the **standard workflow path** with spec-review — from filing a GitHub issue to a merged PR, building a FastAPI bookstore API. It demonstrates how two agents (Claude + Gemini) collaborate through issue comments.

> **Agents used:** Claude (spec-create, spec-finalize, spec-implement), Gemini (spec-review)

---

## Step 0: Set up the repo

1. **Create a repo from the template.** Go to the baf template repo on GitHub, click **"Use this template" → "Create a new repository"**. Name it something like `bookstore-api`.
2. **Clone it locally:**
   ```bash
   git clone https://github.com/<your-username>/bookstore-api.git
   cd bookstore-api
   ```
3. **Run the bootstrap script:**
   ```bash
   ./scripts/bootstrap.sh "Bookstore API"
   ```
4. **Commit the bootstrap:**
   ```bash
   git add -A && git commit -m "chore: bootstrap baf project"
   git push
   ```
5. **Open Claude Code** in the repo root:
   ```bash
   claude
   ```

---

## Step 1: File the issue

Go to your repo's **Issues** tab, click **New issue**, select the **Feature** template:

**Title:** Add Bookstore REST API with CRUD, search, and ISBN validation

| Field | Value |
|-------|-------|
| **What** | Build a REST API for managing a bookstore. Endpoints for books (CRUD), authors, and search. ISBN-13 validation on create/update. SQLite for storage, Pydantic for validation. |
| **Why** | We need a backend API so the frontend team can start building the catalog UI. No API exists yet. |
| **Acceptance criteria** | `POST /books` creates a book with valid ISBN-13 · `GET /books` lists with pagination ·  `GET /books/{id}` returns a single book · `PUT /books/{id}` updates · `DELETE /books/{id}` deletes · `GET /books/search?q=` searches by title/author · Invalid ISBN-13 returns 422 · Tests pass with pytest |
| **Not in scope** | Authentication, user accounts, frontend, deployment, book cover images |
| **Priority** | P1 (important) |
| **Agents** | Two agents (add spec-review) |

Or from the CLI: `gh issue create --title "Add Bookstore REST API with CRUD, search, and ISBN validation" --body "..."`

**Add the `approved` label.**

---

## Step 2: spec-create (Claude)

```
/spec-create 1
```

Claude reads the issue and starts the design conversation.

### What to expect

Claude will likely ask about:
- Search matching strategy (fuzzy vs substring)
- Pagination style (offset vs cursor)
- Whether authors should be a separate resource or just a string field

Answer however you like. For this walkthrough, here are some suggested responses:
- "Substring match is fine for now"
- "Offset pagination"
- "Authors as a separate resource — books reference authors by ID"

### Try this: Build on Claude's suggestions

When Claude asks good questions, **add requirements** that weren't in the original issue. For example, if Claude asks about the author model, say:

> "Yes, and add an `authors/{id}/books` endpoint to get all books by an author."

This is a common real-world pattern — the conversation surfaces requirements you hadn't thought of. When Claude posts the completion comment to the issue, your addition will be documented as something that came out of the spec-create conversation.

### Check the result

Go to issue #1 on GitHub. The comment should include:
- The key design decisions (search strategy, pagination, author model)
- Your addition (the books-by-author endpoint)
- **Next Steps** with the exact commands to run for the review phase, including a ready-to-paste prompt for Gemini

---

## Step 3: spec-review (Gemini)

Now switch agents. Open **Gemini CLI** (or whatever review agent you want to use) in the same repo directory.

The spec-create comment on the issue includes a ready-to-paste prompt. Copy it into Gemini, or use something like:

```
Read CLAUDE.md and context/PROCESS.md. Execute spec-review for context/specs/1-bookstore-rest-api/
```

Gemini reads the spec, the issue, and the issue comments (where Claude posted the spec-create conversation summary). It then produces its review.

### What to expect

Gemini will find things Claude missed. These might include:
- Undefined behavior (e.g., "what happens when you delete an author who has books?")
- Missing error handling
- Scope concerns (e.g., rate limiting)

### Check the result

Go to issue #1. There should now be a **second comment** — from Gemini — with a findings table (CRITICAL/HIGH/MEDIUM/LOW) and specific recommendations.

**This is the multi-agent handoff in action.** Gemini has no direct access to Claude's session — it got all that context by reading the issue comments on GitHub, just like a human would.

---

## Step 4: spec-finalize (Claude)

Back in Claude Code:

```
/spec-finalize context/specs/1-bookstore-rest-api/
```

Claude reads the review artifact that Gemini wrote to the spec directory and the review comment on the issue, then presents the findings to you for decisions.

### Try this: Accept some, reject others

This is where you exercise judgment. For each finding, Claude will ask you what to do. **Don't just accept everything** — reject at least one finding and explain why. For example:

- If Gemini flags rate limiting: "Reject — that's out of scope, we said no auth."
- If Gemini flags author deletion behavior: "Accept — return 409 Conflict when author has books."

The point: your accept/reject decisions with rationale get written to `DECISIONS.md` and posted to the issue. Future contributors can see exactly which review findings were accepted and which were rejected, and *why*.

### Check the result

Issue #1 now has a **third comment** — the finalize summary. It shows:
- How many findings were accepted vs rejected
- Your rationale for each decision
- What changed in the spec

---

## Step 5: spec-implement (Claude)

```
/spec-implement context/specs/1-bookstore-rest-api/
```

Claude follows the finalized spec and implements the code.

### Try this: Watch for mid-implementation updates

If the spec left anything ambiguous, Claude will ask you during implementation. Answer the question, and then **go check the issue** — Claude posts a mid-implementation update comment capturing the clarification in real time, not just at the end.

If Claude doesn't ask anything, the spec was thorough enough (which means the review process worked).

### Check the result

When complete, issue #1 gets a final comment with the PR link. Open the PR to see the code.

---

## The result

Issue #1 now has a **complete, readable history**:

1. **spec-create** (Claude) — requirements refined, design decisions made, new endpoint added mid-conversation
2. **spec-review** (Gemini) — findings that Claude missed, informed by the issue comments from spec-create
3. **spec-finalize** (Claude) — you accepted some findings, rejected others, with rationale
4. **spec-implement** (Claude) — code written per spec, PR opened

**Two different agents** worked on this issue. They never talked to each other directly — the GitHub issue is the shared context. Each agent read the issue comments from previous phases and built on them. The issue reads like a decision journal.

### The exercise that matters

Go read issue #1 end-to-end. Every comment tells part of the story. Now imagine you're a new contributor picking up this project six months later — you can understand not just *what* was built, but *why*, what was considered and rejected, and what came out of the human-agent conversations.

---

## Try it yourself with your own feature

1. File issue #2 with a different feature for this bookstore (e.g., "Add book categories and filtering")
2. Run the same workflow, but this time **deliberately push back more** during spec-create
3. Have Gemini review it — see if it catches different things than before
4. Read both issues side by side — that's your project's decision history
