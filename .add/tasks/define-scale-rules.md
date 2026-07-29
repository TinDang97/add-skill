---
type: Task
title: Define scale rules for a long-running bundle
goal: a six-month bundle stays cheap to orient in, by rule rather than by tidiness
status: verify
depth: quick
kind: docs
sensitivity: mechanical
milestone: /milestones/format-standard.md
depends_on:
  - /tasks/define-entity-model.md
needs:
  - /tasks/define-entity-model.md#gives
gives:
  - "default scans exclude status: done|dropped; an explicit flag includes them"
  - "orientation output prints at most 20 node lines plus a count"
  - "graph rendering is per milestone, never whole-bundle by default"
scope:
  - FORMAT.md
generated: { by: claude/opus-5, at: 2026-07-29 }
verified: []
---
## CARD
goal: T0 is cheap per node and not free in aggregate — bound the aggregate
gives: A12 — scan exclusion, output ceiling, per-milestone graph
scope: FORMAT.md §4.1
beat: verify · next: blocked on the validator for its receipt

## CHECKS
- test_done_excluded_by_default · covers: G1 · a scan of a bundle with 300 done nodes reads only the active set
- test_output_ceiling · covers: G2 · orientation output never exceeds 20 node lines
- test_graph_scoped · covers: G3 · graph rendering defaults to one milestone
red-first: every check above MUST fail for the right reason before BUILD.

## EVIDENCE
receipt: <tasks/define-scale-rules.d/runs/1.md — pending the M0 validator>
gate: <pending — quick lane auto-PASS on a green receipt; sensitivity mechanical, no escalation>
scope-check: <pending>
