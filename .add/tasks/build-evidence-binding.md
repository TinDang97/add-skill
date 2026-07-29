---
type: Task
title: the covers: binding — a check that proves a rule, or says it cannot
goal: every Must is bound to a check that actually ran, or the gap is visible
status: direction
depth: standard
kind: feature
sensitivity: security
milestone: /milestones/engine-core.md
scope:
  - add/scripts/add.py
  - tests/engine/test_evidence_binding.py
depends_on:
  - /tasks/build-receipts-learn.md
needs:
  - /tasks/build-receipts-learn.md#gives
gives:
  - "covers(node) -> {must_id: [check_ids]} parsed from the CHECKS section"
  - "bind(receipt, node) -> which Musts are proven by IDs the runner actually reported (A15/A16)"
  - "unbound(node) -> Musts with no passing check — the honest gap"
budget: 160 lines wc -l of growth (amendment A1/A3)
generated: { by: add/3.0.0, at: 2026-07-29 }
verified: []
---
## CARD
goal: every Must is bound to a check that actually ran, or the gap is visible
gives: covers · bind · unbound
scope: add/scripts/add.py · its red suite
beat: direction · next: add freeze build-evidence-binding

## RULES
<must>
- M1 a Must is proven only by a check ID the RUNNER reported passing. A `covers:` label with no matching test ID is an unbound claim and is reported as such (A15 — `covers:` was a label, not a binding)
- M2 when a runner reports no usable IDs, the receipt degrades to a weaker evidence kind (A24) and SAYS SO. It never silently claims test-ids
- M3 `unbound` is part of every gate's report, so a gate is taken with the gap visible rather than assumed absent
</must>
<reject>
- R:LABEL treating a `covers:` string as proof without a matching reported ID -> "LABEL"
- R:SILENTGAP a gate report that omits unbound Musts -> "SILENTGAP"
</reject>

## PLAN
contract: <published at freeze>
strategy: <published at freeze>
scope: add/scripts/add.py · tests/engine/
floor: validator exits 0 on `.add/`; every earlier task's checks stay green

## CHECKS
- test_covers_parsed_from_checks · covers: M1 · the map is built from the CHECKS section
- test_bind_requires_reported_id · covers: M1, R:LABEL · a covers: naming a test that did not run proves nothing
- test_ids_unknown_degrades_kind · covers: M2 · with no IDs the receipt kind drops and is labelled
- test_unbound_musts_reported · covers: M3, R:SILENTGAP · a Must with no check appears in the report
- test_live_bundle_binding · covers: M1 · this repo's own gated tasks are checked for unbound Musts
red-first: every check above MUST fail for the right reason before BUILD.

## EVIDENCE
receipt: <runs/<n>.md>
gate: <PASS | RISK-ACCEPTED | HARD-STOP>
budget: <growth vs allocation · A3 invariant>
scope-check: <files touched vs `scope:`>

## LESSONS
- <lesson> -> add learn <domain|system|experience|quality|method>
