---
type: Task
title: the CLAUDE.md block — the first link, and the agent-agnostic one
goal: init injects a marker-delimited orient block into CLAUDE.md, AGENTS.md and .clinerules
status: direction
depth: standard
kind: feature
sensitivity: architecture
milestone: /milestones/skill-surface.md
scope:
  - add/scripts/add.py
  - tests/engine/test_first_contact.py
depends_on:
  - /tasks/build-init-profiles.md
needs:
  - /tasks/build-init-profiles.md#gives
budget: 50 lines wc -l of growth — NOT yet in the A5 invariant; see its RULES
generated: { by: add/3.0.0, at: 2026-07-30 }
verified: []
---
## CARD
goal: init injects a marker-delimited orient block into CLAUDE.md, AGENTS.md and .clinerules
gives: the block and its markers · an idempotent update rule · the agent-agnostic routing steps
scope: add/scripts/add.py · its red suite
beat: direction · next: add freeze write-first-contact-block
why: S7 — this is 2.5's PROVEN first link (add_engine/guidelines.py:27-40, "agent-agnostic by
  design"), and v4 replaced it with a Claude-Code-only SessionStart hook. Without it G7 is false
  and the description's primary trigger — "a repo has .add/" — is not observable, because a cold
  agent does not `ls` the repo before answering
⚠ its 50 lines are NOT in A5's invariant, which is already 72 over. Either e11's CLI lands under
  budget or this task waits behind the D-12 cut — decided at e11's freeze, not here

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
