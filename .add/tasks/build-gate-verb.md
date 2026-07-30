---
type: Task
title: gate — the verdict, its three refusals, and the quick lane
goal: a gate is recorded only when the evidence entitles it, and a quick task costs one engine call
status: direction
depth: standard
kind: feature
sensitivity: security
milestone: /milestones/engine-core.md
depends_on:
  - /tasks/build-evidence-binding.md
  - /tasks/build-receipts-learn.md
needs:
  - /tasks/build-evidence-binding.md#gives
  - /tasks/build-receipts-learn.md#gives
generated: { by: add/3.0.0, at: 2026-07-30 }
verified: []
---
## CARD
goal: a gate is recorded only when the evidence entitles it, and a quick task costs one engine call
gives: gate · its three refusals · run's own stamp (F3) · done --cmd as the quick lane
scope: add/scripts/add.py · tests/engine/test_gate_verb.py
beat: direction · next: add freeze build-gate-verb

## RULES
<must>
- M1 `gate` REFUSES when the entitling receipt is not fresh by A22's content predicate. A verdict
     recorded over changed code is not evidence of anything
- M2 `gate` REFUSES a PASS while any Must or Reject in the node's CHECKS is unproven by an ID the
     receipt actually reported (e12's `bind`), and the refusal names the unproven rules.
     **This is e12's M3.** That rule says "`unbound` is part of every gate's report" — and it
     cannot be true while no gate report exists, which it did not when e12 was gated
- M3 `gate` records the verdict as a `verified[]` stamp at the authority `authority_for` computes,
     and stamps the hash of the brief that drove the work (A16, `verified[].brief`)
- M4 a refusal is never silent: it prints why, and the exact command that would make it pass
     (specs/experience#decisions-that-bind)
- M5 `run` appends its own run stamp to the task's `verified[]` — **F3's fix**. A receipt no stamp
     points at is unreachable evidence: 8 of this bundle's 18 receipts are in that state today
- M6 `done --cmd` is §3d's quick lane — new + freeze + run + gate in ONE engine call — and it
     REFUSES for any depth above `quick`. A one-call lane that works at `deep` is not a lane, it is
     a bypass of every control this engine has
</must>
<reject>
- R:STALEGATE a verdict recorded against a receipt that is no longer fresh -> "STALEGATE"
- R:UNPROVEN a PASS recorded while a Must has no reported passing check -> "UNPROVEN"
- R:SILENTREFUSE a refusal that does not name the command that would fix it -> "SILENTREFUSE"
- R:ORPHAN a receipt written with no stamp pointing at it -> "ORPHAN"
- R:BYPASS the one-call lane reachable above `quick` depth -> "BYPASS"
</reject>
<after>
- no gate in this project can be taken by hand-appending a stamp through a private function,
  which is how all eleven gates so far were recorded
- `status --since` stops under-reporting machine acts, because every run leaves a stamp
</after>
⚠ that refusing an unproven PASS is affordable — if wrong: F2's 65 labelled-not-proven rules mean
  a strict M2 would have refused nine M0 gates, so the refusal may need a `--covers-unverified`
  degradation (PROPOSAL §e12 names one) rather than a hard stop. The suite must decide which by
  running M2 against this bundle's real history before the rule is fixed.

## PLAN
contract: <published at freeze>
strategy: <published at freeze>
scope: add/scripts/add.py · tests/engine/test_gate_verb.py
floor: validator CONFORMS on `.add/`; every earlier task's checks stay green
least-sure: rules — M2's strictness. See the ⚠.

## CHECKS
- test_gate_refuses_stale_receipt · covers: M1, R:STALEGATE · a one-byte scope edit invalidates the verdict
- test_gate_refuses_unproven_must · covers: M2, R:UNPROVEN · a Must with no reported check blocks a PASS
- test_gate_refusal_names_the_unproven_rules · covers: M2 · the refusal lists which rules, not just that some failed
- test_gate_refusal_names_the_fix · covers: M4, R:SILENTREFUSE · every refusal ends in a runnable command
- test_gate_records_at_computed_authority · covers: M3 · A17's floor is applied, not the caller's claim
- test_gate_stamps_the_brief_hash · covers: M3 · the stamp carries the brief that drove the work
- test_risk_accepted_records_the_risk · covers: M3 · RISK-ACCEPTED is a verdict with a reason, not a softer PASS
- test_run_appends_its_own_stamp · covers: M5 · a run is reachable from the task afterwards
- test_no_orphan_receipts_on_live_bundle · covers: M5, R:ORPHAN · this repo's 8 orphans are reported
- test_quick_lane_is_one_engine_call · covers: M6 · a quick task closes in a single invocation
- test_quick_lane_refuses_above_quick · covers: M6, R:BYPASS · standard and deep cannot use it
- test_gate_on_live_bundle_history · covers: M2 · M2 run against this project's own gated tasks, to size the ⚠
red-first: every check above MUST fail for the right reason before BUILD.

## EVIDENCE
receipt: <runs/<n>.md>
gate: <PASS | RISK-ACCEPTED | HARD-STOP>
budget: <growth vs allocation · A3 invariant>
scope-check: <files touched vs `scope:`>

## LESSONS
- <lesson> -> add learn <domain|system|experience|quality|method>
