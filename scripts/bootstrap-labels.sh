#!/usr/bin/env bash
set -euo pipefail

# Bootstrap GitHub labels for the baf workflow.
# Run once after creating your repo from the template.
#
# Usage: ./scripts/bootstrap-labels.sh

echo "Creating baf workflow labels..."

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

echo "Done. All baf labels created."
