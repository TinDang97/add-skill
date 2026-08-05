---
type: Task
title: v0 — unwrapped drive, two arms
goal: with no wrapper, a cold agent invokes the engine, picks a lane, freezes before building, runs checks red first, and gates on a receipt — with and without the orient sentence (S3)
status: direction
depth: deep
kind: test
sensitivity: architecture
milestone: /milestones/prove-it.md
scope:
  - benchmark/**
depends_on:
  - /tasks/eval-trigger-precision.md
generated: { by: add/3.0.0, at: 2026-08-05 }
verified: []
---
## CARD
goal: a cold agent, no wrapper, drives freeze -> red -> receipt -> gate, both S3 arms — the thing S6 says was never shown
beat: direction · next: add freeze eval-unwrapped-drive

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
