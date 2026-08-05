---
type: Task
title: six profiles as data, and a lens set that is really closed
goal: every profile creates all five lenses, six profiles exist as data, and an unknown profile is refused
status: direction
depth: standard
kind: fix
sensitivity: architecture
milestone: /milestones/engine-core.md
scope:
  - add/scripts/add.py
  - tests/engine/test_profiles.py
depends_on:
  - /tasks/build-init-profiles.md
needs:
  - /tasks/build-init-profiles.md#gives
budget: 36 CODE lines of growth (D-15 — converted from 60 wc -l at the engine's measured 60% code ratio; the unit changed, this allocation did not)
generated: { by: add/3.0.0, at: 2026-07-30 }
verified: []
---
## CARD
goal: every profile creates all five lenses, six profiles exist as data, and an unknown profile is refused
gives: 6 profile packs as data · all five lenses always created · an unknown profile refused, never downgraded · a doctor check that `persona_corpus:` resolves
scope: add/scripts/add.py · its red suite
beat: direction · next: add freeze ship-domain-profiles
why: N2 — `doc` ships four lenses against a law that says the set is closed. N3 — four of the six
  named profiles resolve to `code` while `index.md` records the name you asked for. N6 — this
  bundle's own `persona_corpus:` points at a path that does not exist. Goals 2 and 4 rest here

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
