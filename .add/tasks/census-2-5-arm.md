---
type: Task
title: v8 — the 2.5-arm census, gate-0
goal: run ADD 2.5 on the pre-registered task set and count engine calls, turns, tokens and approvals with the FIXED counter (B1, B4)
status: direction
depth: standard
kind: test
sensitivity: data
milestone: /milestones/prove-it.md
scope:
  - benchmark/**
depends_on:
  - /tasks/prove-first-light.md
generated: { by: add/3.0.0, at: 2026-08-05 }
verified: []
---
## CARD
goal: gate-0 — measure ADD 2.5 with the fixed counter, so every later claim has a real baseline (B1, B4)
beat: direction · next: add freeze census-2-5-arm

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
