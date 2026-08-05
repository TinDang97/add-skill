---
type: Task
title: a cold agent drives the loop from the skill directory alone
goal: init -> quick -> standard -> gate, by an agent given nothing but the skill directory
status: direction
depth: deep
kind: feature
sensitivity: architecture
milestone: /milestones/first-light.md
scope:
  - add
  - tests/engine/test_first_light.py
depends_on:
  - /tasks/package-in-skill.md
needs:
  - /tasks/package-in-skill.md#gives
budget: a demonstration, not engine lines
generated: { by: add/3.0.0, at: 2026-07-30 }
verified: []
---
## CARD
goal: init -> quick -> standard -> gate, by an agent given nothing but the skill directory
gives: the walking skeleton — the artifact v8, v7 and v0 are run against
scope: add · its red suite
beat: direction · next: add freeze prove-first-light
why: D-13. Everything before this is substrate; this is the first moment the product exists end to
  end, and it is the input to the decision gate. Not an eval — a demonstration

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
