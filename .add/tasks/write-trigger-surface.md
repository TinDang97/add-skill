---
type: Task
title: the description — what fires it, and what must not
goal: a description that fires in-regime and stays silent out-of-regime, proven by the query set
status: direction
depth: standard
kind: feature
sensitivity: architecture
milestone: /milestones/skill-surface.md
scope:
  - add/SKILL.md
depends_on:
  - /tasks/write-trigger-eval-set.md
  - /tasks/write-skill-core.md
needs:
  - /tasks/write-trigger-eval-set.md#gives
budget: frontmatter, not engine lines
generated: { by: add/3.0.0, at: 2026-07-30 }
verified: []
---
## CARD
goal: a description that fires in-regime and stays silent out-of-regime, proven by the query set
gives: name · description with explicit trigger phrases and the `.add/` presence condition · when-NOT-to-use · the 2.5 routing predicate · user-invocable and argument-hint
scope: add/SKILL.md
beat: direction · next: add freeze write-trigger-surface
why: S4 — v4's plan kept the negative surface and dropped the positive one that is doing the work
  in the artifact that demonstrably fires today. S5 — the regime statement's economics belong in
  the body, not in the ~100 always-loaded words whose only job is recall

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
