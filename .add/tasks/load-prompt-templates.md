---
type: Task
title: brief compiles from a template file, not from code
goal: a prompt template is a bundle node that brief loads, so the prompt library has a consumer
status: direction
depth: standard
kind: fix
sensitivity: architecture
milestone: /milestones/engine-core.md
scope:
  - add/scripts/add.py
  - templates/prompts
  - tests/engine/test_prompt_templates.py
depends_on:
  - /tasks/build-brief-compiler.md
needs:
  - /tasks/build-brief-compiler.md#gives
budget: 24 CODE lines of growth (D-15 — converted from 40 wc -l at the engine's measured 60% code ratio; the unit changed, this allocation did not)
generated: { by: add/3.0.0, at: 2026-07-30 }
verified: []
---
## CARD
goal: a prompt template is a bundle node that brief loads, so the prompt library has a consumer
gives: `brief` compiles from templates/prompts/*.xml.tmpl · Prompt templates resolve through the fragment grammar · the dead `add locate` corrected
scope: add/scripts/add.py · templates/prompts · its red suite
beat: direction · next: add freeze load-prompt-templates
why: N4 — no template loading exists anywhere in the engine; the three M0-gated skeletons are read
  by no code, and M3's p3 is scheduled to write more of them. FORMAT §7 already states this
  contract. N5 — the build skeleton cites a verb D-2 folded away

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
