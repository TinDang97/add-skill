---
type: Task
title: durability — CI, the budget assertion, and the failure modes
goal: the engine's own invariants are asserted by machine, on every change
status: direction
depth: standard
kind: feature
sensitivity: architecture
milestone: /milestones/engine-core.md
scope:
  - add/scripts/add.py
  - tests/engine/test_durability.py
depends_on:
  - /tasks/build-doctor.md
needs:
  - /tasks/build-doctor.md#gives
gives:
  - "the CI job asserting the A3 invariant: consumed + remaining allocations <= 2,400"
  - "concurrency and crash tests over the atomic write path"
  - "the fresh-checkout test: `python3 add/scripts/add.py` with zero install"
budget: 80 lines wc -l of growth (amendment A1/A3)
generated: { by: add/3.0.0, at: 2026-07-29 }
verified: []
---
## CARD
goal: the engine's own invariants are asserted by machine, on every change
gives: the CI job asserting the A3 invariant: consumed + remaining allocations <= 2,400 · concurrency and crash tests over the atomic write path · the fresh-checkout test: `python3 add/scripts/add.py` with zero install
scope: add/scripts/add.py · its red suite
beat: direction · next: add freeze build-durability

## RULES
<must>
- M1 CI asserts the A3 invariant on every change — a budget nobody counts is a wish
- M2 the atomic write path is tested under concurrent writers and simulated crash, reusing e1's harness (A1 cut)
- M3 a fresh clone runs the engine with zero install, no PYTHONPATH, stdlib only
</must>
<reject>
- R:UNASSERTED an invariant stated in a node but not checked by machine -> "UNASSERTED"
- R:INSTALL a step required before the engine runs -> "INSTALL"
</reject>

## PLAN
contract: <published at freeze>
strategy: <published at freeze>
scope: add/scripts/add.py · tests/engine/
floor: validator exits 0 on `.add/`; every earlier task's checks stay green

## CHECKS
- test_budget_asserted_in_ci · covers: M1, R:UNASSERTED · the invariant fails CI when exceeded
- test_concurrent_writers · covers: M2 · two writers to one bundle cannot interleave a node
- test_fresh_checkout_zero_install · covers: M3, R:INSTALL · a clean clone runs the engine
red-first: every check above MUST fail for the right reason before BUILD.

## EVIDENCE
receipt: <runs/<n>.md>
gate: <PASS | RISK-ACCEPTED | HARD-STOP>
budget: <growth vs allocation · A3 invariant>
scope-check: <files touched vs `scope:`>

## LESSONS
- <lesson> -> add learn <domain|system|experience|quality|method>
