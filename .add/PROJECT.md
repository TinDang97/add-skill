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
shape: FORMAT (M0) → engine (M1) → skill ∥ personas (M2/M3) → proof (M4) → ship (M5)
state: M0 active (10/10 rules written, validator green, nothing gated) · M1–M5 queued
next: human gate on build-worked-example — A17 pins it, and it is M0's only evidence path

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
- Python stdlib only, single package, engine ≤ 2,400 lines, shipped inside the skill directory
- clean break from 2.5 — no migration verb ships in v1
- red/green TDD on every engine verb
- the bundle holds knowledge; the engine lives in the installed package
