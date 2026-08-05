---
type: Task
title: the query set that makes a description falsifiable
goal: 25-40 queries across five classes plus a .add/ fixture repo, wired to run_eval.py
status: direction
depth: standard
kind: feature
sensitivity: mechanical
milestone: /milestones/skill-surface.md
scope:
  - evals/trigger
gives:
  - "a query set of 25-40 prompts across five classes, each labelled with its expected verdict"
  - "a fixture repository containing .add/ so the presence trigger is observable"
budget: a query set, not engine lines
generated: { by: add/3.0.0, at: 2026-07-30 }
verified: []
---
## CARD
goal: 25-40 queries across five classes plus a `.add/` fixture repo, wired to run_eval.py
gives: the query set (in-regime · out-of-regime · small-change · resume · 2.5-bundle) · a fixture repo that makes the `.add/`-exists trigger observable
scope: evals/trigger
beat: direction · next: add freeze write-trigger-eval-set
why: without it `write-trigger-surface` is authored with no red test, and D-9's three-revision cap
  is spent guessing. It also carries the small-change class, because skill-creator documents that
  simple one-step queries may not fire a skill at all — which is the class the quick lane serves

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
