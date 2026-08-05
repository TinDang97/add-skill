---
type: Task
title: v7 — trigger precision, two arms
goal: the description fires in-regime and stays silent out-of-regime, with and without the regime statement (S5)
status: direction
depth: standard
kind: test
milestone: /milestones/prove-it.md
scope:
  - benchmark/**
depends_on:
  - /tasks/census-2-5-arm.md
  - /tasks/write-trigger-eval-set.md
generated: { by: add/3.0.0, at: 2026-08-05 }
verified: []
---
## CARD
goal: precision AND recall >=0.9 on the query set, both S5 arms — the skill fires in-regime, stays silent off it
beat: direction · next: add freeze eval-trigger-precision

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
