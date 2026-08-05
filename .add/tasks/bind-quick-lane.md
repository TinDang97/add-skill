---
type: Task
title: no gate is entitled by an empty covers: set
goal: an auto-authority gate refuses an empty binding and names the cheapest way to earn one
status: direction
depth: standard
kind: fix
sensitivity: security
milestone: /milestones/engine-core.md
scope:
  - add/scripts/add.py
  - tests/engine/test_quick_binding.py
depends_on:
  - /tasks/build-gate-verb.md
  - /tasks/build-evidence-binding.md
needs:
  - /tasks/build-evidence-binding.md#gives
budget: 24 CODE lines of growth (D-15 — converted from 40 wc -l at the engine's measured 60% code ratio; the unit changed, this allocation did not)
generated: { by: add/3.0.0, at: 2026-07-30 }
verified: []
---
## CARD
goal: an auto-authority gate refuses an empty binding and names the cheapest way to earn one
gives: L8 enforced — an empty `covers:` refuses at process authority and records `covers_absent` at human · a quick-lane node whose EVIDENCE is filled · no done node hinting at its own re-run
scope: add/scripts/add.py · its red suite
beat: direction · next: add freeze bind-quick-lane
why: N8 — one call on a fresh bundle returned `gate PASS` over a node with no scope, no CHECKS and
  a `command-exit` receipt. Every existing refusal assumes a node that declared something, so the
  cheapest lane is the least guarded — and it is the lane the short-scope claim rests on

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
