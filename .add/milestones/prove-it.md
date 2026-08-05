---
type: Milestone
title: Prove it
goal: the skill fires, a cold agent drives it unwrapped, and ADD 3.0 is measured against a measured ADD 2.5
status: direction
depth: deep
stage: mvp
tasks:
  - /tasks/census-2-5-arm.md
  - /tasks/eval-trigger-precision.md
  - /tasks/eval-unwrapped-drive.md
depends_on:
  - /milestones/first-light.md
generated: { by: add/3.0.0, at: 2026-08-05 }
verified: []
---
## CARD
goal: M4 `prove-it` — the scoreboard gets numbers; the D-13 decision gate fires on them
shape: gate-0 measures 2.5 first (v8) → trigger precision (v7) → unwrapped drive (v0) → Stage D
state: `direction` — 3 of 10 nodes opened (the D-13 critical path); the rest open after v8
next: add freeze census-2-5-arm

## SCOPE
In:  the pre-registered task set · the 2.5-arm census with the FIXED counter (B1) · the trigger
     query-set eval, two arms (S5) · the unwrapped-drive eval, two arms (S3) · the scoreboard
     compiled from receipts by `scripts/`, never by the engine
Out: any fix the numbers motivate (a new milestone, after Stage D) · the remaining seven M4
     evals until v8 gates · publishing ANY cost/efficiency claim before v8 lands (D-14) ·
     conversation-carry arms (2.5 proved the mode, not the method, is the rot hazard)

## GROUND
touches: `benchmark/**` (new, outside the D-15 ceiling) · `scripts/**` (scoreboard compiler) ·
  the `w1` transcript from /milestones/first-light.md — the artifact every eval runs against
anchors: PROPOSAL v5 §3d (cost = turns × context-per-turn) · the B family (B1 14× counting bug ·
  B2 harness variance · B3 time-to-first-edit is the real loss · B4 nothing ever measured 2.5) ·
  legacy pinned meter `claude-sonnet-5 --effort medium`, so numbers compose with the 2026-07
  campaign data
honors: specs/quality#decisions-that-bind (a gate is earned by a receipt, never a claim) ·
  specs/method#decisions-that-bind (D-13 order fixed: v8 → v7 → v0 · D-14 no cost claim
  until v8 · Stage D pre-committed: PASS / NARROW / STOP)
risks:
  - **v8 is the first time 2.5 is measured. If its corrected baseline is better than assumed
    (B1 already showed ~18 real calls, not 251), the beat-targets below tighten — they are
    re-derived from v8's numbers, never relaxed to fit**
  - the evals are run by agents of the same family that built the thing; two-arm designs
    (S3, S5) and the fixed counter are the only defense — a single-arm "win" is not evidence
  - Stage D's STOP is a real outcome. Pre-passing it by softening an EXIT line here is the
    exact failure this milestone exists to prevent

## EXIT
scoreboard — each row measured, never projected; baselines come from v8, targets from PROPOSAL §3d:
- [ ] v8 census recorded: 2.5's calls · turns · tokens · approvals on the task set, FIXED counter  (← census-2-5-arm)
- [ ] time-to-first-edit ≤2× vanilla on the quick lane (2.5 measured 4–5×, B3)                     (← eval-unwrapped-drive)
- [ ] engine calls p50 within lane budget: quick 1 · standard ≤4 · deep ≤4, counted from receipts  (← eval-unwrapped-drive)
- [ ] cost ≤1.5× spec-kit on short scope, ≤2× standard lane (2.5 measured 3.3×)                    (← eval-unwrapped-drive)
- [ ] fidelity 1.00 and 0 regressions — 2.5's floor, held, not traded for speed                    (← eval-unwrapped-drive)
- [ ] trigger precision AND recall ≥0.9 on the query set, both S5 arms reported                    (← eval-trigger-precision)
- [ ] unwrapped drive: cold agent freezes before building, runs red first, gates on a receipt,
      in ≥2 of 3 reps, both S3 arms reported                                                       (← eval-unwrapped-drive)
- [ ] every number above traces to a receipt or transcript kept in the bundle — a number
      without an artifact is a defect                                                              (← census-2-5-arm)
- [ ] Stage D recorded as PASS / NARROW / STOP by a human, citing the scoreboard rows              (← eval-unwrapped-drive)

## STRATEGY
approach: risk-first — v8 first because every downstream claim keys off it (B4); a wrong baseline
  poisons the whole gate
freeze-first: the task set and counter are pre-registered at v8's freeze; changing either after
  a single rep is an amendment, not an edit
waves: sequential on the critical path (v8 → v7 → v0); the seven remaining evals open only
  after v8 gates, scoped by what its numbers say is worth measuring
tradeoffs: measuring 2.5 first costs a wave before any 3.0 number exists — accepted, because
  the alternative is v4's mistake (a headline built on an uncounted baseline, B1)

## CLOSE
evidence: <one row per task — <t-slug>: gate=<outcome> · checks=<n green> · residue=<none|note>>
census: <engine calls · briefs compiled and their bytes · receipts · human approvals · gates by outcome>
log: <the rotated `## YYYY-MM-DD` groups from log.md fold in here>
goal met: <restate the goal, and the one evidence line that proves the ship meets it>
