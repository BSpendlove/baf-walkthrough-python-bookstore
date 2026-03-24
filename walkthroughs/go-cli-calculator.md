# Walkthrough: Go CLI Calculator

This walkthrough demonstrates the **minimal workflow path** — spec-create → spec-finalize → spec-implement — building a Go command-line calculator. It shows how baf works for smaller features where a full review cycle isn't needed.

> **Agent used:** Claude only (single agent path)

---

## Step 0: Set up the repo

1. **Create a repo from the template.** Go to the baf template repo on GitHub, click **"Use this template" → "Create a new repository"**. Name it something like `cli-calculator`.
2. **Clone it locally:**
   ```bash
   git clone https://github.com/<your-username>/cli-calculator.git
   cd cli-calculator
   ```
3. **Run the bootstrap script.** This removes template files (walkthroughs, media, template README), creates a clean project README, resets `context/SUMMARY.md`, and creates all the GitHub labels:
   ```bash
   ./scripts/bootstrap.sh "CLI Calculator"
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

Go to your repo's **Issues** tab on GitHub. Click **New issue**, select the **Feature** template, and fill it in:

**Title:** Build CLI calculator with expression parsing and history

| Field | Value |
|-------|-------|
| **What** | A Go CLI calculator that evaluates mathematical expressions from stdin. Supports `+`, `-`, `*`, `/`, parentheses, and operator precedence. Maintains a session history accessible via `history` command. |
| **Why** | Need a standalone utility for quick calculations without leaving the terminal. Existing tools are either too complex (bc) or don't support history. |
| **Acceptance criteria** | `calc "2 + 3 * 4"` returns `14` · Parentheses work: `calc "(2 + 3) * 4"` returns `20` · Division by zero returns a clear error · `calc history` shows last 50 expressions and results · `calc clear` clears history · `go test ./...` passes |
| **Not in scope** | Variables, functions (sin/cos), graphing, GUI, floating point precision beyond float64 |
| **Priority** | P2 (nice to have) |
| **Agents** | Single agent |

Or file it from the CLI:

```bash
gh issue create --title "Build CLI calculator with expression parsing and history" \
  --body "See the Feature template fields above"
```

**Add the `approved` label** to the issue (you can do this in the GitHub UI sidebar, or `gh issue edit 1 --add-label approved`).

---

## Step 2: spec-create (Claude)

In Claude Code, run:

```
/spec-create 1
```

Claude reads the issue and starts asking you questions. This is the back-and-forth — answer its questions directly in the Claude Code prompt.

### What to expect

Claude will ask clarifying questions about the design. For this walkthrough, here's a suggested conversation — but feel free to answer however you like:

- **If Claude asks about REPL mode:** "Yes, if you run `calc` with no args, drop into interactive mode."
- **If Claude asks about history storage:** "`~/.local/share/calc/history.json` following XDG."
- **If Claude suggests a parsing approach:** Push back if it picks recursive descent — tell it "Shunting-yard, we're explicitly NOT adding functions per the scope boundary, so extensibility isn't a concern."

### Try this: Override a decision

This is the important part. When Claude proposes something you disagree with, **say no and explain why**. This is what baf is designed to capture — the debate, not just the outcome.

After Claude finishes, it will:
1. Create a branch and write the spec files
2. **Post a comment to issue #1** with the full conversation summary

### Check the result

Go to your issue on GitHub. You should see a comment from Claude with:
- A summary of what was decided
- A **Conversation Log** section showing the back-and-forth, including any places where you overrode the agent
- Next steps telling you what command to run next

**This is the core of baf** — that comment is now permanent context. Anyone (human or AI) who picks up this issue later can read exactly what was discussed and why.

---

## Step 3: spec-finalize (Claude)

Since this is the minimal path (no reviews), go straight to finalize:

```
/spec-finalize context/specs/1-cli-calculator/
```

Claude will tell you there are no review artifacts and ask if you want to approve the spec as-is.

### Try this: Request a change before approving

Instead of just saying "yes, ship it", **ask Claude to make a small change** to the spec. For example:

- "Before we finalize — add a `--version` flag that prints the version number."
- "Actually, cap history at 100 entries instead of 50."

Claude will update the spec and note the change. Then confirm to finalize.

### Check the result

Go back to issue #1. You should now see a **second comment** — the spec-finalize summary. If you requested a change, it will be documented there. The issue now has two comments building up the decision trail.

---

## Step 4: spec-implement (Claude)

```
/spec-implement context/specs/1-cli-calculator/
```

Claude reads the finalized spec and starts writing code. This phase can take a few minutes.

### Try this: Intervene mid-implementation

While Claude is working, it may ask you clarifying questions — things the spec didn't fully cover. For example, exit codes, error message formatting, or edge cases.

If Claude *doesn't* ask you anything, that's fine — it means the spec was detailed enough. But you can also **proactively interrupt** with something like:

- "For error messages, prefix them with `error:` so they're easy to grep."
- "Make sure the REPL prompt is `> ` not `calc> `."

When you do this, Claude will:
1. Incorporate your feedback into the implementation
2. **Post a mid-implementation update** to the issue capturing the clarification

### Check the result

When implementation is complete, go to issue #1 one more time. You should see:
- A **mid-implementation update** comment (if any clarifications happened)
- A **spec-implement complete** comment with the PR link

Open the PR. The code is there, tests pass, and the issue has the full story.

---

## The result

Issue #1 tells the full story in 3-4 comments:

1. **spec-create** — the design conversation, including any decisions you overrode
2. **spec-finalize** — approved (with any last-minute changes you requested)
3. **spec-implement** — code written, PR opened (with any mid-implementation clarifications)

The most interesting part: if you pushed back on a decision in step 2, that's captured. A future contributor wondering "why was it done this way?" can read the issue and see the exact reasoning — not just the outcome, but the debate.

---

## Try it yourself with your own feature

Now that you've seen the flow, try it with something different:

1. File a new issue (#2) with a feature *you* actually want to build
2. Run `/spec-create 2`
3. During the conversation, **deliberately disagree** with at least one thing Claude suggests — this is how you see the conversation tracking in action
4. Run `/spec-finalize` → `/spec-implement`
5. Read the issue comments end-to-end — that's the decision journal
