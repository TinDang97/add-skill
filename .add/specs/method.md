---
type: Spec
title: Method
lens: add
project: ADD-SKILL
generated: { by: claude/opus-5, at: 2026-07-29 }
---
## Now
Three beats per task: **direction** (rules + plan + red checks, then ONE freeze) →
**build** (green, inside scope) → **verify** (receipt, then a recorded gate).

Ceremony is proportional to risk, set by `depth:` and floored by `sensitivity:`.
`quick` renders three body sections and closes in one engine call. `standard` renders
six and crosses three. `deep` adds milestone strategy and a human freeze.

Cost = turns × context-per-turn. Four levers, in evidence order: fewer turns
(compound verbs, one-draft composition) · smaller context per turn (T0/T1/T2 tiers,
briefs that inject refs not prose) · less ceremony where risk is low (the depth dial)
· and adoption, which decides whether the first three ever happen.

Learning is a loop: a lesson lands as a delta the moment it is learned, and folds
into `Now` at close — so the next loop reads a smaller, truer picture.

## Decisions that bind
- Direction ends with exactly ONE approval; a ratified milestone pre-approves its member tasks. (A1)
- `sensitivity: security` requires a per-task human freeze — never batched, never derived. (A1)
- `sensitivity: data | architecture` requires at least `plan` authority: a human ratified the milestone
  that contains the task, and ratification covers only the membership frozen at the stamp. (A1, FORMAT §3.1)
- A task whose `scope:` matches `index.md`'s `sensitive_paths:` is pinned to `human` regardless of its
  declared sensitivity — a path match, not a judgement. (A17)
- Authority ladder: human > plan > ai-verify > process; sensitivity pins the minimum. (A1, define-authority-rules)
- T2 is single-node: a task's context is its own body + T1 CARDs of its deps + `Decisions that bind`. (define-read-protocol)
- The milestone gathers GROUND once; tasks project from it and never re-ground the repo. (A8)
- Specs are never re-scanned; they are updated by delta. (define-log-rotation)
- A milestone scope change is an `amended:` stamp at no less authority than its ratification; dropped
  tasks keep their nodes with a reason, and EXIT criteria are struck, never deleted. (A21, define-compat-contract)
- After ANY context loss — a new session, a subagent handoff, or a compaction — re-orient with `add status`
  before acting. The repo is never re-read. (PROPOSAL v4 R5)
- Personas: select → fold → author. A roster of near-duplicates is worse than one sharp lens. (2.5, kept)
- The generic fallback is a 15-year specialist in the task's `kind:` — it never blocks and never lowers a gate. (2.5, kept)

## Deltas (newest first)
<!-- `add learn method "<lesson>"` prepends here -->
- [open · 2026-07-29] A17 pinned all ten M0 tasks to `human` because every one of them has `FORMAT.md` in scope and `FORMAT.md` is a declared sensitive path — including the two marked `mechanical`. The only batching mechanism in the format is milestone ratification at `plan` authority, which A17 outranks, so a milestone whose whole scope IS a sensitive path costs one human gate per task. Recorded and left unfixed: amending a trust rule because it binds its author is the failure this method exists to prevent. Decide in M1, on evidence about how often it bites. (define-authority-rules)
- [open · 2026-07-29] The adoption chain had no root: `next:` is the mechanism that makes every other lever fire, and `next:` only exists AFTER an engine call, and nothing caused the first call. In the 2.5 pilot a loop-enforcing wrapper hid this. Designing an affordance without asking what triggers the first one is how a measured 0% adoption gets re-earned. (define-read-protocol)
- [open · 2026-07-29] The 1.0-draft rule "data | architecture | security all need a per-task human freeze" made `plan` and `ai-verify` unreachable and blocked every headless run on routine data work. Batching approval through milestone ratification restores the lane — but only because ratification is bounded to the membership frozen at the stamp. An authority ladder without a bound on batching is a blank cheque. (define-authority-rules)
- [open · 2026-07-29] Phase decomposition of the 2.5 pilot: specify+scenarios+contract = 3% of tokens; tests 34% + verify 30% = 64%. Writing specs is nearly free — executing trust is the cost. Cutting spec volume buys nothing and costs the floor. (define-read-protocol)
