---
type: Task
title: the gate contract — <=15 lines, decidable in 30 s
goal: the human-gate contract, the follow-along contract and the report form, split out of loop
status: direction
depth: standard
kind: feature
sensitivity: architecture
milestone: /milestones/skill-surface.md
scope:
  - add/references/gate.md
depends_on:
  - /tasks/write-skill-core.md
needs:
  - /tasks/write-skill-core.md#gives
gives:
  - "the <=15-line gate card — ARC, flags, approve"
  - "the report form, rendered from receipts never prose"
  - "the follow-along contract"
budget: a reference file, not engine lines
generated: { by: add/3.0.0, at: 2026-08-05 }
verified: []
---
## CARD
goal: the human-gate contract, the follow-along contract and the report form, split out of loop
gives: the <=15-line gate card — ARC, flags, approve · the report form, rendered from receipts never prose · the follow-along contract
beat: direction · next: add freeze write-gate-ref

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
