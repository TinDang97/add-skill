---
type: Milestone
title: Skill surface
goal: the judgment layer inside a stated budget: a cold agent drives the loop from the skill text alone
status: direction
depth: deep
stage: mvp
tasks:
  - /tasks/write-trigger-eval-set.md
  - /tasks/write-skill-core.md
  - /tasks/write-trigger-surface.md
  - /tasks/write-first-contact-block.md
  - /tasks/write-team-ref.md
depends_on:
  - /milestones/engine-core.md
generated: { by: add/3.0.0, at: 2026-07-30 }
verified: []
---
## CARD
goal: the judgment layer inside a stated budget — the loop driven from the skill text alone
shape: wave 1 the critical path (s0 → s1 → s2 ∥ s7); wave 2 the nine remaining references
state: `direction` — 5 of 14 nodes opened; wave 2 opens when wave 1 gates
next: add freeze write-trigger-eval-set

## SCOPE
In:  `add/SKILL.md` and `add/references/**` · the `CLAUDE.md` first-contact block `init` injects ·
     the trigger query set and its fixture repo · the CI that asserts the skill's own budget
Out: the engine and its verbs (M1) · personas and the prompt library (M3) · the evals that
     MEASURE this (M4) · `plugin.json` and the identity contract (M5)

## GROUND
touches: `add/SKILL.md` · `add/references/**` · `add/scripts/add.py` (only for `s7`'s injector)
anchors: 2.5's shipped skill is the only empirical evidence of this method working — source head
  **178 lines + 1,829 across 10 references + a 690-line `persona-author/` sub-skill**. Every
  budget here is derived from it rather than guessed
honors: specs/experience#decisions-that-bind (guidance lives in engine output, never in template
  blockquotes · every verb ends with `next:` · errors name the fix) · specs/method#decisions-that-bind
  (the depth dial · the authority ladder · re-orient after any context loss)
risks:
  - **the artifact this milestone is modelled on has never run unwrapped.** `arms/add.toml:5` sets
    `prompt_wrapper = "add-loop"`, and that wrapper restates the three beats in the prompt — orient
    first, no code before freeze, record the gate, with proxy authority. So "2.5 works" means
    "2.5 works with the loop re-injected every run", and **no version of this method has been shown
    to drive from SKILL.md alone.** This milestone writes the thing that has to; `v0` finds out
  - `loop.md` is the plan's dumping ground. 2.5 needed 396 lines across three files for what v4
    routes into one, which is why `write-gate-ref` splits the gate contract back out
  - the quick lane may be structurally unreachable: skill-creator documents that simple one-step
    queries may not fire a skill at all. `write-trigger-eval-set` carries that class so the
    question is answered by a number rather than by hope

## EXIT
- [ ] `SKILL.md` ≤200 lines AND ≤180 chars/line, asserted in CI          (← write-skill-core · assert-skill-conformance)
- [ ] the whole artifact ≤1,500 lines, asserted in CI                     (← assert-skill-conformance)
- [ ] every reference is cited from `SKILL.md` with a when-to-read cue    (← assert-skill-conformance)
- [ ] every cookbook command and every `next:` template resolves to a real verb+flag (← assert-skill-conformance)
- [ ] a cold agent in a repo with `.add/` and NO plugin still orients     (← write-first-contact-block)
- [ ] the description fires on the query set and stays silent off it      (← write-trigger-surface · write-trigger-eval-set)

## CLOSE
evidence: <one row per task — <t-slug>: gate=<outcome> · checks=<n green> · residue=<none|note>>
census: <engine calls · briefs compiled and their bytes · receipts · human approvals · gates by outcome>
log: <the rotated `## YYYY-MM-DD` groups from log.md fold in here>
goal met: <restate the goal, and the one evidence line that proves the ship meets it>
