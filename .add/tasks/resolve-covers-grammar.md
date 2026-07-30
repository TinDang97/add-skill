---
type: Task
title: reconcile the covers: grammar — FORMAT §6.1 vs the validator
goal: one grammar for rule IDs, decided deliberately rather than widened to make the author pass
status: direction
depth: standard
kind: feature
sensitivity: security
milestone: /milestones/engine-core.md
depends_on:
  - /tasks/build-evidence-binding.md
needs:
  - /tasks/build-evidence-binding.md#gives
generated: { by: add/3.0.0, at: 2026-07-30 }
verified: []
---
## CARD
goal: one grammar for rule IDs, decided deliberately rather than widened to make the author pass
gives: a single stated grammar · both oracles enforcing it · the decision and its reason recorded
scope: FORMAT.md · scripts/validate_bundle.py · tests/test_validate_bundle.py
beat: direction · next: add freeze resolve-covers-grammar

## RULES
<must>
- M1 FORMAT §6.1 and `scripts/validate_bundle.py` state and enforce the SAME grammar, asserted by a
     check that reads both rather than by a human comparing them (F1 has been open since M0)
- M2 the decision is recorded WITH its reason. Widening to admit digits (`R:T2SCAN`, `R:T2FANOUT`,
     `R:MTIME2`) and narrowing while renaming those three are both defensible; choosing without a
     recorded reason is not, because the author of the offending IDs is the one choosing (A17)
- M3 no gated node's rule IDs are silently rewritten. If narrowing wins, the renames are recorded as
     a correction on each node, not applied as a sweep (§3.6)
</must>
<reject>
- R:SELFSERVE widening a grammar so the author's own nodes stop reporting, with no other reason -> "SELFSERVE"
- R:DRIFT two oracles carrying two grammars for one format -> "DRIFT"
</reject>
<after>
- the 7 `covers_referent` info lines this bundle reports are either gone or justified
- the next person to add a rule ID learns the grammar from one place
</after>
⚠ that this is worth a task at all — it reports `info`, not `error`, and nothing is blocked. The
  argument for doing it is that F1 is the ONLY finding in this project where two documents disagree
  about the format itself, and every later oracle inherits the ambiguity.

## PLAN
contract: <published at freeze>
strategy: <published at freeze>
scope: FORMAT.md · scripts/validate_bundle.py · tests/test_validate_bundle.py
floor: validator CONFORMS on `.add/`; the M0 suite stays green
least-sure: rules — M2. This is a judgement about a naming convention, and the honest risk is
  spending a human gate on something that reports `info` and blocks nothing.

## CHECKS
- test_grammar_stated_once · covers: M1, R:DRIFT · the regex in the validator matches the grammar FORMAT states
- test_both_oracles_agree_on_rule_ids · covers: M1 · the engine's RULE_ID and the validator accept the same set
- test_decision_is_recorded · covers: M2, R:SELFSERVE · the node carries the reason, not just the outcome
- test_no_gated_node_rewritten · covers: M3 · a gated node's rule IDs are unchanged, or the change is recorded
red-first: every check above MUST fail for the right reason before BUILD.

## EVIDENCE
receipt: <runs/<n>.md>
gate: <PASS | RISK-ACCEPTED | HARD-STOP>
budget: <growth vs allocation · A3 invariant>
scope-check: <files touched vs `scope:`>

## LESSONS
- <lesson> -> add learn <domain|system|experience|quality|method>
