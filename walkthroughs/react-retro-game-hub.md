# Walkthrough: React Retro Game Hub

This walkthrough demonstrates the **full three-agent pipeline** — spec-create, spec-review, spec-critique, spec-finalize, spec-implement, and spec-final-review — building a React dashboard for browsing retro games. It shows how multiple agents collaborate through issue comments, each building on the last.

> **Agents used:** Claude (spec-create, spec-finalize, spec-implement), Gemini (spec-review), Codex (spec-critique, spec-final-review)

---

## Step 0: Set up the repo

1. **Create a repo from the template.** Go to the baf template repo on GitHub, click **"Use this template" → "Create a new repository"**. Name it something like `retro-game-hub`.
2. **Clone it locally:**
   ```bash
   git clone https://github.com/<your-username>/retro-game-hub.git
   cd retro-game-hub
   ```
3. **Run the bootstrap script:**
   ```bash
   ./scripts/bootstrap.sh "Retro Game Hub"
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

**Title:** Build Retro Game Hub — browse, search, and favorite classic games

| Field | Value |
|-------|-------|
| **What** | A React SPA that lets users browse retro games from the [RAWG API](https://rawg.io/apidocs). Grid layout with game cards (cover art, title, platform, rating). Search by name. Favorite games stored in localStorage. Filter by platform (NES, SNES, Genesis, PS1, N64, Arcade). |
| **Why** | Fun portfolio project that demonstrates React patterns, API integration, and state management. Also: retro games are cool. |
| **Acceptance criteria** | Homepage shows paginated game grid · Search filters results in real-time · Clicking a heart adds to favorites (persisted in localStorage) · `/favorites` page shows saved games · Platform filter chips narrow results · Responsive: works on mobile · Loading/error states handled |
| **Not in scope** | User accounts, backend server, game details page, reviews/comments, purchasing, ROM downloads |
| **Priority** | P2 (nice to have) |
| **Agents** | Three agents (add spec-review + spec-critique) |

Or from the CLI: `gh issue create --title "Build Retro Game Hub — browse, search, and favorite classic games" --body "..."`

**Add the `approved` label.**

---

## Step 2: spec-create (Claude)

```
/spec-create 1
```

### What to expect

Claude will ask about API keys, state management, styling, and search behavior. Suggested responses:

- **API key handling:** "Env var, never commit keys."
- **State management:** "Zustand — it's simple."
- **Search debouncing:** "Debounce at 300ms."
- **Styling:** "Tailwind."

### Try this: Amend the requirements mid-conversation

This is a real-world scenario — requirements evolve during discussion. When Claude asks about styling or theme, **add a requirement that wasn't in the issue:**

> "Can we add a dark mode toggle? Retro games deserve a dark theme."

Claude should flag that this isn't in the original acceptance criteria. Tell it to include it anyway — "Consider it an amendment."

This gets captured in the conversation log as an AMENDMENT — clearly marked so reviewers know it's a scope addition that came from the human during spec-create, not something the agent invented.

### Check the result

Go to issue #1. The spec-create comment should include:
- All the design decisions
- Your dark mode amendment, clearly marked
- **Next Steps** with ready-to-paste prompts for both Gemini (review) and Codex (critique)

---

## Step 3: spec-review (Gemini)

Switch to **Gemini CLI** in the same repo. Use the prompt from the issue comment, or:

```
Read CLAUDE.md and context/PROCESS.md. Execute spec-review for context/specs/1-retro-game-hub/
```

### What to expect

Gemini reads the spec files in the repo, the issue, and the issue comments — including the spec-create comment where Claude documented your dark mode amendment. It will likely find things like:

- API rate limiting concerns (RAWG has limits)
- Pagination UX left undefined (infinite scroll? page numbers?)
- localStorage bloat if you store full game objects
- Missing error handling for API failures

### Check the result

Issue #1 gets a second comment — Gemini's review with a severity-ranked findings table.

---

## Step 4: spec-critique (Codex)

Switch to **Codex CLI** (or any third agent). Use the prompt from the issue, or:

```
Read CLAUDE.md and context/PROCESS.md. Execute spec-critique for context/specs/1-retro-game-hub/
```

### What to expect

Codex reads the spec files, the issue, and all the issue comments — including Claude's spec-create summary and Gemini's review findings. It looks for things the other two missed. For example:

- Cross-tab localStorage sync (if you have two tabs open, favorites don't sync)
- Implementation phases that are too coarse
- Agreeing with Gemini's findings but adding specificity (e.g., "use TanStack Query with stale-while-revalidate, not just 'add caching'")

### Check the result

Issue #1 now has a **third comment** — Codex's critique. Notice how it references and builds on Gemini's findings rather than repeating them. This is the multi-agent flywheel working.

---

## Step 5: spec-finalize (Claude)

Back in Claude Code:

```
/spec-finalize context/specs/1-retro-game-hub/
```

Claude reads ALL review findings from both agents and presents them to you.

### Try this: Make deliberate accept/reject decisions

You'll have findings from two different agents to evaluate. This is where your judgment shapes the spec. **Don't just accept everything.** For example:

- Gemini flagged responsive breakpoints? "Reject — Tailwind's defaults are fine."
- Codex found the cross-tab sync issue? "Accept — but use the storage event listener approach, it's simpler."
- Gemini wants query caching? "Accept — add TanStack Query."
- Codex says implementation Phase 2 is too coarse? "Accept — split it into sub-phases."

Each decision gets written to `DECISIONS.md` with your rationale. The accept/reject pattern with reasoning is what makes the spec-finalize comment on the issue so valuable — it's a clear record of how review feedback was handled.

### Check the result

Issue #1 gets a fourth comment showing:
- Total findings from both agents
- How many you accepted vs rejected
- The specific rationale for each decision

---

## Step 6: spec-implement (Claude)

```
/spec-implement context/specs/1-retro-game-hub/
```

Claude implements the code following the finalized spec.

### Try this: Watch for discoveries during implementation

Larger implementations often surface surprises. Claude might discover:
- API response formats differ from what the spec assumed
- Platform IDs in the RAWG API don't match what was expected
- Edge cases the spec didn't cover (games without cover art, etc.)

If Claude asks you a question mid-implementation, answer it and then **go check the issue** — you should see a mid-implementation update comment capturing the clarification.

### Check the result

When complete, issue #1 gets the implementation comment with a PR link.

---

## Step 7: spec-final-review (Codex) — optional

For the full pipeline, run a final code review with Codex:

```
Read CLAUDE.md and context/PROCESS.md. Execute spec-final-review for context/specs/1-retro-game-hub/
```

Codex reviews the actual code diff against the finalized spec. It checks:
- Were all accepted review findings actually implemented?
- Does the code match the spec?
- Any implementation-level issues (performance, UX polish)?

### Check the result

Issue #1 gets a final comment — the code review. If Codex found that the cross-tab sync (which it originally flagged as CRITICAL) is correctly implemented, it'll note that. The loop closes.

---

## The result

Issue #1 has **6 comments** telling the complete story:

| # | Phase | Agent | What happened |
|---|-------|-------|---------------|
| 1 | spec-create | Claude | Requirements refined, dark mode added as amendment, key design decisions |
| 2 | spec-review | Gemini | Findings — caching, pagination UX, localStorage bloat, error handling |
| 3 | spec-critique | Codex | More findings — cross-tab sync bug, implementation order too coarse |
| 4 | spec-finalize | Claude | You accepted some findings, rejected others, with rationale for each |
| 5 | spec-implement | Claude | Code written per spec, PR opened |
| 6 | spec-final-review | Codex | Code review confirms spec compliance, minor improvements noted |

**Three different agents** worked on this issue. They never talked to each other directly — the GitHub issue is the shared context. Each agent read the spec files and the issue comments from previous phases. No context was lost because everything was posted to the issue as it happened.

### The exercise that matters

Read issue #1 end-to-end. Then ask yourself: if a new contributor (human or AI) picked this up in 6 months, would they understand:
- Why dark mode was added? (Yes — it's marked as an amendment from the human)
- Why shunting-yard/Zustand/Tailwind? (Yes — design conversation is there)
- Why some review findings were rejected? (Yes — DECISIONS.md + the finalize comment)
- Whether the cross-tab sync was actually implemented? (Yes — the final review confirms it)

That's the point of baf.

---

## Try it yourself with your own feature

1. File issue #2 — something different for this project (e.g., "Add game details page with screenshots and ratings")
2. Run the full pipeline across all three agents
3. Compare the two issues side by side — that's your project's decision history building up
4. Try having a different agent do the review this time — see how the findings differ
