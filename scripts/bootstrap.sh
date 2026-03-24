#!/usr/bin/env bash
set -euo pipefail

# Bootstrap a new project from the baf template.
# Run once after creating your repo from the template.
#
# What it does:
#   1. Removes template-specific files (walkthroughs, media, template README)
#   2. Creates a minimal project README
#   3. Resets context/SUMMARY.md to a clean slate
#   4. Creates all GitHub labels for the baf workflow
#
# Usage: ./scripts/bootstrap.sh [project-name]
#
# Example:
#   ./scripts/bootstrap.sh "My Bookstore API"

PROJECT_NAME="${1:-$(basename "$(pwd)")}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "Bootstrapping baf project: $PROJECT_NAME"
echo ""

# ─── Step 1: Remove template-specific files ──────────────────────────────────

echo "Cleaning up template files..."

# Walkthroughs are examples for the template repo, not for your project
rm -rf "$REPO_ROOT/walkthroughs"

# Template branding
rm -rf "$REPO_ROOT/media"

# Template README — we'll replace it below
rm -f "$REPO_ROOT/README.md"

# This bootstrap script itself — you only run it once
# (We delete it at the very end so it can finish running first)

echo "  Removed: walkthroughs/, media/, README.md"

# ─── Step 2: Create a minimal project README ─────────────────────────────────

cat > "$REPO_ROOT/README.md" << EOF
# $PROJECT_NAME

This project uses the [baf](https://github.com/BSpendlove/baf) workflow — an LLM-driven development process where every conversation is tracked on GitHub issues.

## Getting started

1. File a GitHub issue using one of the issue templates
2. Add the \`approved\` label
3. Open your AI agent in the repo root and run a skill:
   - **Claude Code:** \`/spec-create 1\`
   - **Other agents:** Read \`CLAUDE.md\` and \`context/PROCESS.md\`, then follow the workflow

## Workflow

\`\`\`
Issue → spec-create → spec-review (optional) → spec-finalize → spec-implement
\`\`\`

See [context/PROCESS.md](context/PROCESS.md) for the full workflow definition.

## Skills

| Skill | Purpose |
|-------|---------|
| \`/spec-create <issue>\` | Draft implementation spec from a GitHub issue |
| \`/spec-review <path>\` | Review spec for completeness |
| \`/spec-critique <path>\` | Critique spec for gaps and edge cases |
| \`/spec-finalize <path>\` | Finalize spec, incorporate feedback |
| \`/spec-implement <path>\` | Implement code from finalized spec |
| \`/spec-final-review <path>\` | Post-implementation code review |
| \`/spec-status [issue]\` | Show workflow status |
EOF

echo "  Created: README.md (project-specific)"

# ─── Step 3: Reset context/SUMMARY.md ────────────────────────────────────────

cat > "$REPO_ROOT/context/SUMMARY.md" << EOF
# Project Summary

This file tracks project state. Every agent session should read this before starting new work.

**Updated after every spec is implemented.**

## Current State

$PROJECT_NAME — no work completed yet. File an issue to get started.

## Completed Specs

| Spec | Issue | Status | Summary |
|------|-------|--------|---------|
| *(none yet)* | | | |

## Key Decisions

*(Decisions that affect future specs will be recorded here as work progresses.)*
EOF

echo "  Reset: context/SUMMARY.md"

# ─── Step 4: Create GitHub labels ────────────────────────────────────────────

echo ""
echo "Creating GitHub labels..."

# Workflow state
gh label create "approved"              --color 0E8A16 --description "Issue approved for work"                2>/dev/null || gh label edit "approved"              --color 0E8A16 --description "Issue approved for work"
gh label create "phase:spec"            --color 1D76DB --description "Spec is being drafted"                  2>/dev/null || gh label edit "phase:spec"            --color 1D76DB --description "Spec is being drafted"
gh label create "phase:review"          --color 1D76DB --description "Spec is under review"                   2>/dev/null || gh label edit "phase:review"          --color 1D76DB --description "Spec is under review"
gh label create "spec:approved"         --color 0E8A16 --description "Spec approved for implementation"       2>/dev/null || gh label edit "spec:approved"         --color 0E8A16 --description "Spec approved for implementation"
gh label create "phase:implementation"  --color 1D76DB --description "Code is being written"                  2>/dev/null || gh label edit "phase:implementation"  --color 1D76DB --description "Code is being written"
gh label create "phase:done"            --color 0E8A16 --description "Complete — PR merged"                   2>/dev/null || gh label edit "phase:done"            --color 0E8A16 --description "Complete — PR merged"

# Priority
gh label create "priority:p0"           --color B60205 --description "Critical path — blocks other work"      2>/dev/null || gh label edit "priority:p0"           --color B60205 --description "Critical path — blocks other work"
gh label create "priority:p1"           --color D93F0B --description "Important — do soon"                    2>/dev/null || gh label edit "priority:p1"           --color D93F0B --description "Important — do soon"
gh label create "priority:p2"           --color FBCA04 --description "Nice to have"                           2>/dev/null || gh label edit "priority:p2"           --color FBCA04 --description "Nice to have"

# Agent selection
gh label create "agents:single"         --color C5DEF5 --description "Single agent workflow"                  2>/dev/null || gh label edit "agents:single"         --color C5DEF5 --description "Single agent workflow"
gh label create "agents:two"            --color C5DEF5 --description "Two agent workflow (+ review)"          2>/dev/null || gh label edit "agents:two"            --color C5DEF5 --description "Two agent workflow (+ review)"
gh label create "agents:three"          --color C5DEF5 --description "Three agent workflow (+ review + critique)" 2>/dev/null || gh label edit "agents:three"      --color C5DEF5 --description "Three agent workflow (+ review + critique)"
gh label create "agents:full"           --color C5DEF5 --description "Full pipeline including final review"   2>/dev/null || gh label edit "agents:full"           --color C5DEF5 --description "Full pipeline including final review"

# Issue types
gh label create "feature"               --color A2EEEF --description "New capability"                         2>/dev/null || gh label edit "feature"               --color A2EEEF --description "New capability"
gh label create "enhancement"           --color A2EEEF --description "Improvement to existing feature"        2>/dev/null || gh label edit "enhancement"           --color A2EEEF --description "Improvement to existing feature"

echo "  Created all 15 labels"

# ─── Step 5: Clean up this script ────────────────────────────────────────────

echo ""
echo "Removing bootstrap scripts (no longer needed)..."
rm -f "$REPO_ROOT/scripts/bootstrap-labels.sh"
rm -f "$REPO_ROOT/scripts/bootstrap.sh"
rmdir "$REPO_ROOT/scripts" 2>/dev/null || true

echo ""
echo "Done! Your project is ready."
echo ""
echo "Next steps:"
echo "  1. git add -A && git commit -m 'chore: bootstrap baf project'"
echo "  2. File your first issue using the Feature template"
echo "  3. Add the 'approved' label"
echo "  4. Open Claude Code and run: /spec-create 1"
