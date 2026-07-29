---
type: Task
title: Define scale rules for a long-running bundle
goal: a six-month bundle stays cheap to orient in, by rule rather than by tidiness
status: done
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
verified:
  - { by: "human:tindang", at: 2026-07-29, act: freeze, authority: human }
  - { by: "human:tindang", at: 2026-07-29, act: gate, authority: human, outcome: PASS,
      receipt: /tasks/build-worked-example.d/runs/3.md }
    # A17 pinned this to `human`: `scope:` includes FORMAT.md, a sensitive_path. The
    # declared `sensitivity:` was never the binding constraint.
---
## CARD
goal: T0 is cheap per node and not free in aggregate — bound the aggregate
gives: A12 — scan exclusion, output ceiling, per-milestone graph
scope: FORMAT.md §4.1
beat: done · gate PASS by human:tindang on receipt 3

## CHECKS
- test_done_excluded_by_default · covers: G1 · a scan of a bundle with 300 done nodes reads only the active set
- test_output_ceiling · covers: G2 · orientation output never exceeds 20 node lines
- test_graph_scoped · covers: G3 · graph rendering defaults to one milestone
red-first: every check above MUST fail for the right reason before BUILD.

## EVIDENCE
receipt: /tasks/build-worked-example.d/runs/3.md — 18/18, the shared M0 evidence run
gate: PASS — human:tindang, 2026-07-29, authority `human` (A17 floor)
scope-check: FORMAT.md only — inside the declared scope
