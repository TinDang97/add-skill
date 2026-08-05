---
type: Project
title: ADD-SKILL
goal: >-
  a repo owner drives any project — a 30-minute fix or a 6-month product — through
  one skill plus one CLI, resumes it cold from the bundle alone, and trusts every
  shipped change through a recorded receipt, at a token cost proportional to risk
stage: mvp
profile: cli-tool
generated: { by: claude/opus-5, at: 2026-07-29 }
---
## CARD
goal: lean, trustworthy AI-driven development — ADD 3.0 on the ABF-1 file graph
shape: honest evidence → a reachable engine → the walking skeleton → **a decision gate** → the
  method → proof → ship. PROPOSAL v5 reordered this: the two results that could kill the project
  now arrive in nine tasks instead of twenty-eight
state: M0 done · M1 15 of 23 · the CLI is **measured** (208 wc -l / 138 code) but still unbuilt ·
  M1.5 `first-light` and M2 `skill-surface` opened · e16/e17/e18 gated PASS · **D-12 fired** —
  `--find`/`--graph`/`--since` withdrawn, −56 lines — and it still did not fit, so **D-15 restates
  the ceiling in CODE lines and raises it to 1,550, breaking D-6 knowingly (A7)** ·
  projected **1485/1550 code, slack 65** · 21 findings recorded, 8 unowned
next: M1 `build-durability` — its CI job is the only thing that stops this invariant being
  maintained by hand in three places, which is how F20 hid a 120-line disagreement

## Direction
Distil AIDD-Book 2.5 — which scored a best-in-class 0.97 fidelity floor across six
benchmark milestones — into a method that keeps the floor and sheds the ceremony.
The core (3 beats, 5 specs, freeze/gate trust, personas, learning loop) is kept
unchanged. What changes: files become the database, ceremony becomes proportional
to risk, and every read declares a tier.

ADD is not a correctness upgrade — six milestones say a good spec-first alternative
reaches the same answers. ADD buys a floor with no catastrophic milestone, auditable
trust artifacts, and a price advantage in one measured regime: small increments
against an established codebase, where it ran at half the alternative's cost. On
large milestones it ran 3–4× steeper. The skill states that regime out loud rather
than selling a "worth it at scale" story the benchmark retracted.

## Voice
*(human-owned — the AI never rewrites this section)*

Plain, exact, unhedged. Numbers over adjectives. Name the weakest link in the
delivery, never in private. A claim without evidence is written as a claim.
No ceremony that does not earn its tokens.

## Constraints
- Python stdlib only, single package, engine ≤ **1,550 CODE lines** (D-15, was 2,400 wc -l;
  the unit changed AND the number rose — see engine-core A7), shipped inside the skill directory
- clean break from 2.5 — no migration verb ships in v1
- red/green TDD on every engine verb
- the bundle holds knowledge; the engine lives in the installed package
