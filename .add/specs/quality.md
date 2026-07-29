---
type: Spec
title: Quality
lens: tdd
project: ADD-SKILL
generated: { by: claude/opus-5, at: 2026-07-29 }
---
## Now
Two evaluation tracks, deliberately separated because they have different epistemics.

**Conformance (deterministic, n=1, in CI):** things that are *counted*, not sampled —
engine calls per lane, files created by `init`, brief bytes per depth, receipt
presence and freshness, cold-resume correctness, `doctor` findings. This is where a
ceremony budget becomes a tested number.

**Behavioral (stochastic, n≥3, rubric):** things an agent *chooses* — the right lane,
the quick lane when eligible, refusing to weaken a check, escalating a security
sensitivity to a human.

Token cost is reported directionally with spread, never as a headline. The pilot
documents run-to-run variance up to 8× on tokens and a complete fidelity flip
(0.0 vs 0.98) on a rerun at n=1; a single-run token delta is noise wearing a number.

## Decisions that bind
- Every engine verb is built red/green: a failing test that fails for the right reason first. (define-authority-rules)
- A gate is earned by a receipt, never by a claim. No receipt, no PASS. (A2/A3)
- A Must or Reject encoded in no check means the rules are not understood — stop. (2.5, kept)
- Never weaken, skip, or delete a check to reach green; that is a change request. (2.5, kept)
- Cost claims require n≥3 or are not made. (PROPOSAL §6)
- Conformance assertions are counted, never sampled. (PROPOSAL §6)
- Trigger precision is measured before anything downstream: a number produced by a skill that never
  loaded is not a number. (D-9, v7)
- An eval carries a stated budget and a task set pre-registered before the first run; an overrun degrades
  n *visibly* ("directional, n<3") and never silently. (D-10)

## Deltas (newest first)
<!-- `add learn quality "<lesson>"` prepends here -->
- [open · 2026-07-29] Our own trust chain had a forgeable link: `covers:` named a check, the receipt reported `passed: n`, and nothing tied the two. A gate could pass on checks that were never written. Evidence is only evidence when the *specific* claim is bound to the *specific* observation — counting green is not the same as confirming the named check ran. (define-evidence-binding)
- [open · 2026-07-29] The 2.5 benchmark's own fairness checklist flags that ADD ran under a loop-enforcing prompt wrapper tuned across 3 iterations while the comparison arm ran raw. A plain skill has no wrapper — adoption must be measured, not inherited. (build-worked-example)
