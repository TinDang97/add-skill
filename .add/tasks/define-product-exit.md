---
type: Task
title: an EXIT criterion names a promise, never a function
goal: every EXIT criterion names a user-visible promise and carries the check that observes it
status: direction
depth: standard
kind: feature
sensitivity: architecture
milestone: /milestones/engine-core.md
scope:
  - FORMAT.md
  - add/scripts/add.py
  - tests/engine/test_promises.py
depends_on:
  - /tasks/build-doctor.md
needs:
  - /tasks/build-doctor.md#gives
budget: 18 CODE lines of growth (D-15 — converted from 30 wc -l at the engine's measured 60% code ratio; the unit changed, this allocation did not)
generated: { by: add/3.0.0, at: 2026-07-30 }
verified: []
---
## CARD
goal: every EXIT criterion names a user-visible promise and carries the check that observes it
gives: the EXIT phrasing rule (A28) · `doctor --promises` reporting criteria phrased as functions and promises with no check
scope: FORMAT.md · add/scripts/add.py · its red suite
beat: direction · next: add freeze define-product-exit
why: G9 and the whole N family — ten verbs gated, eight promises unkept, because the checks
  asserted that the machinery ran and never that the promise held. This is the meta-fix, and
  without it the same class recurs at M2 where nothing is testable by a validator

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
