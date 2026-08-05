---
type: Task
title: status is the product, not a node listing
goal: status delivers the specified orientation surface and its next: names the READY node
status: direction
depth: standard
kind: fix
sensitivity: architecture
milestone: /milestones/engine-core.md
scope:
  - add/scripts/add.py
  - tests/engine/test_status_surface.py
depends_on:
  - /tasks/build-orient.md
  - /tasks/build-hints-layer.md
needs:
  - /tasks/build-orient.md#gives
budget: 60 lines wc -l of growth (A5)
generated: { by: add/3.0.0, at: 2026-07-30 }
verified: []
---
## CARD
goal: status delivers the specified orientation surface and its next: names the READY node
gives: beat · git progress · cheapest legal lane · fold nudge · stuck rule · lane advisory · node aging · a next: derived from readiness, not from sort order
scope: add/scripts/add.py · its red suite
beat: direction · next: add freeze repair-status-surface
why: N7 — `status` emitted `next: add brief build-durability` while the milestone CARD said
  `next: e16`, and e16 is the one that must land first. Specs and index burn the 20-line
  orientation budget. This is the surface that answers weakness 5 and goals 6 and 13

## RULES
<must>
- M1 <the rule that must hold>
</must>
<reject>
- R:<NAME> <what must never happen> -> "<NAME>"
</reject>

## PLAN
contract: <the shape this publishes>
scope: <files>

## CHECKS
- <test_name> · covers: M1 · <what it proves>
red-first: every check MUST fail first.

## EVIDENCE
receipt: <runs/<n>.md>
gate: <PASS | RISK-ACCEPTED | HARD-STOP>

## LESSONS
- <lesson> -> add learn <lens>
