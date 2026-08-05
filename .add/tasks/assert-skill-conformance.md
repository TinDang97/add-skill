---
type: Task
title: CI asserts the skill keeps its own promises
goal: L7 applied to the skill: budgets, reference citations, and every cookbook command resolving to a real verb+flag
status: direction
depth: standard
kind: test
sensitivity: architecture
milestone: /milestones/skill-surface.md
scope:
  - tests/skill/test_skill_conformance.py
depends_on:
  - /tasks/write-skill-core.md
  - /tasks/write-gate-ref.md
needs:
  - /tasks/write-skill-core.md#gives
gives:
  - "a CI oracle asserting SKILL.md <=200 lines and <=180 chars/line"
  - "every reference cited from SKILL.md with a when-to-read cue"
  - "every cookbook command and next: template resolving to a real verb+flag"
budget: a CI oracle, not engine lines
generated: { by: add/3.0.0, at: 2026-08-05 }
verified: []
---
## CARD
goal: L7 applied to the skill — the budgets and citations asserted, not claimed
gives: a CI oracle asserting SKILL.md <=200 lines and <=180 chars/line · every reference cited from SKILL.md with a when-to-read cue · every cookbook command and next: template resolving to a real verb+flag
beat: direction · next: add freeze assert-skill-conformance

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
