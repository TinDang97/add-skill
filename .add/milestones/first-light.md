---
type: Milestone
title: First light
goal: a cold agent, given the skill directory alone, drives init -> quick -> standard -> gate end to end
status: direction
depth: deep
stage: mvp
tasks:
  - /tasks/prove-first-light.md
depends_on:
  - /milestones/engine-core.md
generated: { by: add/3.0.0, at: 2026-07-30 }
verified: []
---
## CARD
goal: the walking skeleton — the first moment the product exists end to end
shape: one task, one demonstration; the artifact the decision gate is run against
state: `direction` — blocked on M1's tail (e16 · e9 · e11) and on `s1`/`s2` from M2
next: add freeze prove-first-light

## SCOPE
In:  a cold agent, given ONLY the shipped `add/` directory, completing `init` → the quick lane →
     one standard task → a gate, with no wrapper, no loop-driving prompt and no proxy authority
Out: measuring it (that is `v7` and `v0`, in M4) · the remaining five references (M2) · personas
     and the prompt library (M3) · CI, packaging polish and the plugin manifest (M5)

## GROUND
touches: `add/**` — the shipped artifact, whole · a scratch repository outside this one
anchors: PROPOSAL v5 §6b and §12 — this milestone is one task because its value is the
  DEMONSTRATION, not the machinery. Everything it needs is owed by M1's tail and by `s1`/`s2`
honors: specs/system#decisions-that-bind (one artifact, one version · zero install · the engine
  ships inside the skill) · specs/experience#decisions-that-bind (`add status` is the resume verb ·
  every verb ends with `next:`) · specs/method#decisions-that-bind (the depth dial, the authority
  ladder)
risks:
  - **this milestone is where the N family is either closed or repeated.** Its EXIT criteria are
    phrased as things a user can DO, precisely because M1's were not — and eight promises went
    unkept underneath ten gated verbs (A28, `define-product-exit`)
  - a demonstration driven by the agent that built the thing proves less than it appears to. The
    honest reading is that it establishes the product EXISTS end to end; whether a COLD agent can
    drive it is `v0`'s question, not this one, and conflating the two is how `v0` gets pre-passed
  - it depends on `e11`, the task most likely to break the line ceiling (D-12)

## EXIT
- [ ] a cold agent, given only `add/`, runs `init` and gets a conforming 8-file bundle    (← prove-first-light)
- [ ] the same agent completes one quick-lane task whose receipt BINDS a check             (← prove-first-light · bind-quick-lane)
- [ ] the same agent completes one standard task through direction → build → verify        (← prove-first-light)
- [ ] every command it ran came from a `next:` line it was given, not from reading source  (← build-hints-layer)
- [ ] the transcript is kept as the artifact `v8`, `v7` and `v0` are run against           (← prove-first-light)

## CLOSE
evidence: <one row per task — <t-slug>: gate=<outcome> · checks=<n green> · residue=<none|note>>
census: <engine calls · briefs compiled and their bytes · receipts · human approvals · gates by outcome>
log: <the rotated `## YYYY-MM-DD` groups from log.md fold in here>
goal met: <restate the goal, and the one evidence line that proves the ship meets it>
