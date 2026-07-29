---
type: Task
title: the next: line — one affordance, every verb
goal: no verb ever leaves the user without a runnable next step
status: direction
depth: standard
kind: feature
sensitivity: mechanical
milestone: /milestones/engine-core.md
scope:
  - add/scripts/add.py
  - tests/engine/test_hints_layer.py
depends_on:
  - /tasks/build-orient.md
  - /tasks/build-doctor.md
needs:
  - /tasks/build-orient.md#gives
  - /tasks/build-doctor.md#gives
gives:
  - "hint(graph, after_verb) -> the next: line, derived from graph state"
  - "a test asserting EVERY verb's output ends in one (law 4, mechanically)"
budget: 80 lines wc -l of growth (amendment A1/A3)
generated: { by: add/3.0.0, at: 2026-07-29 }
verified: []
---
## CARD
goal: no verb ever leaves the user without a runnable next step
gives: hint · a test asserting EVERY verb's output ends in one 
scope: add/scripts/add.py · its red suite
beat: direction · next: add freeze build-hints-layer

## RULES
<must>
- M1 every verb's output ends in a `next:` line naming a runnable command (law 4)
- M2 the hint is derived from graph state, not from a static per-verb string, so it stays true as the project moves
- M3 when no next step is defensible, the verb says so plainly rather than inventing one
</must>
<reject>
- R:NOHINT a verb whose output lacks a next: line -> "NOHINT"
- R:FAKEHINT a hint naming a command that would fail if run -> "FAKEHINT"
</reject>

## PLAN
contract: <published at freeze>
strategy: <published at freeze>
scope: add/scripts/add.py · tests/engine/
floor: validator exits 0 on `.add/`; every earlier task's checks stay green

## CHECKS
- test_every_verb_ends_with_next · covers: M1, R:NOHINT · enumerated over all ten verbs, not sampled
- test_hint_is_derived · covers: M2 · changing graph state changes the hint
- test_hint_is_runnable · covers: M3, R:FAKEHINT · every hint parses as a real command
red-first: every check above MUST fail for the right reason before BUILD.

## EVIDENCE
receipt: <runs/<n>.md>
gate: <PASS | RISK-ACCEPTED | HARD-STOP>
budget: <growth vs allocation · A3 invariant>
scope-check: <files touched vs `scope:`>

## LESSONS
- <lesson> -> add learn <domain|system|experience|quality|method>
