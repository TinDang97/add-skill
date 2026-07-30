---
type: Task
title: test IDs carry their file — a failing check cannot be recorded as passed
goal: every check ID in a receipt names exactly one test, so evidence cannot be masked
status: direction
depth: standard
kind: fix
sensitivity: security
milestone: /milestones/engine-core.md
scope:
  - add/scripts/add.py
  - tests/engine/test_evidence_ids.py
depends_on:
  - /tasks/build-evidence-binding.md
  - /tasks/compile-checks-from-suite.md
needs:
  - /tasks/build-evidence-binding.md#gives
  - /tasks/compile-checks-from-suite.md#gives
budget: 60 lines wc -l of growth (A3 — from e8's 5-line underrun and the 344-line slack)
generated: { by: add/3.0.0, at: 2026-07-30 }
verified:
  - { by: "claude/opus-5", at: 2026-07-30, act: freeze, authority: human }
---
## CARD
goal: every check ID in a receipt names exactly one test, so evidence cannot be masked
gives: `classname::name` IDs in extract_ids and checks_of · a decision on existing receipts · a check that a collision cannot pass
scope: add/scripts/add.py · tests/engine/test_evidence_ids.py
beat: direction · next: add freeze repair-evidence-ids

## RULES
<must>
- M1 a check ID is `classname::name`, taken from junit's `classname` attribute — which was in the
     data all along and thrown away. Two tests sharing a bare name in different files must produce
     two IDs, and `extract_ids` must never let one overwrite the other
- M2 a junit report containing one FAILING and one PASSING test of the same bare name records the
     failure. This is F7's exact demonstration and it is the check the whole task exists for
- M3 `checks_of` (e14) carries the same defect and is fixed in the same shape, because `doctor`'s F2
     check and `gate`'s binding both read it. One fix, two call sites, one ID grammar — a second
     grammar here would be R:DRIFT again (F1's lesson, one level down)
- M4 the migration is DECIDED and recorded, not performed silently. Every existing receipt holds
     bare-name IDs; changing the shape means a stored ID no longer matches what a re-run reports.
     Whether old receipts are left as-is, re-taken, or read through a compatibility rule is a human
     decision with a reason (A17 — `add/scripts/add.py` is a sensitive path)
- M5 no gated node's `covers:` citations are rewritten to the new shape. A citation names a TEST, and
     `M1 · covers: test_foo` stays legible; if the binding needs the file, the resolution is in the
     reader, not in 133 rewritten claims across nine human-gated nodes (§3.6)
</must>
<reject>
- R:MASK a receipt in which a failing check is recorded as passing -> "MASK"
- R:DRIFT two ID grammars for one format -> "DRIFT"
- R:SWEEP rewriting citations inside gated nodes to satisfy a new ID shape -> "SWEEP"
</reject>
<after>
- `gate` can no longer be entitled by a check that failed, which is what A24's ladder assumed all along
- the 211/212 discrepancy that revealed F7 becomes impossible to reproduce
</after>
⚠ that `classname::name` is the right ID shape for a format that does not know pytest exists. junit's
  `classname` is emitted by every runner the format supports at v1.0, but "supported at v1.0" is one
  runner. If a second runner spells it differently, the ID becomes runner-specific and A24's kind
  ladder has a portability hole one rung from the top — if wrong, the ID needs a normalising rule and
  this task grows one.

## PLAN
contract: <published at freeze>
strategy: <published at freeze>
scope: add/scripts/add.py · tests/engine/test_evidence_ids.py
floor: validator CONFORMS on `.add/`; the 212-check suite stays green; no gated node edited
least-sure: rules — M4. The engineering is small and the migration question is not: this bundle holds
  20 receipts and 11 gates whose evidence was recorded in the old shape, and no answer makes all of
  them retroactively unambiguous.

## CHECKS
- test_two_tests_one_name_are_two_ids · covers: M1 · junit's classname distinguishes them
- test_a_masked_failure_is_recorded · covers: M2, R:MASK · F7's demonstration, as a check
- test_checks_of_keys_by_file_too · covers: M3 · e14's extractor carries the same defect
- test_one_id_grammar · covers: M3, R:DRIFT · both call sites state the shape once
- test_migration_decision_is_recorded · covers: M4 · the node carries the reason, not just the outcome
- test_no_gated_citation_rewritten · covers: M5, R:SWEEP · nine gated M0 nodes are byte-identical
red-first: every check above MUST fail for the right reason before BUILD.
authored-not-compiled: these six are a PLAN — the tests do not exist yet, so e14's grading calls
  this `pending` and `doctor` must not report it as a defect. `checks --sync` replaces the section
  after BUILD, and that replacement is the check on this note (e8 proved it: 10 authored, 20 real).

## EVIDENCE
receipt: <runs/<n>.md>
gate: <PASS | RISK-ACCEPTED | HARD-STOP>
budget: <growth vs allocation · A3 invariant>
scope-check: <files touched vs `scope:`>

## LESSONS
- <lesson> -> add learn <domain|system|experience|quality|method>
