---
type: Task
title: doctor — conformance and repair over the compiled graph
goal: every FORMAT rule the M0 validator enforces still holds after the engine has written
status: direction
depth: standard
kind: feature
sensitivity: architecture
milestone: /milestones/engine-core.md
scope:
  - add/scripts/add.py
  - tests/engine/test_doctor.py
depends_on:
  - /tasks/compile-graph.md
  - /tasks/build-orient.md
  - /tasks/build-evidence-binding.md
needs:
  - /tasks/compile-graph.md#gives
  - /tasks/build-orient.md#gives
  - /tasks/build-evidence-binding.md#gives
gives:
  - "doctor(root) -> findings over e2's graph, using the same codes as scripts/validate_bundle.py"
  - "doctor --sync -> repairs compiled artifacts: index TOC, log rotation, CARD drift, A23 merge resolution"
  - "parity with the M0 oracle, asserted by a test that runs both"
budget: 200 lines wc -l of growth (amendment A1/A3)
generated: { by: add/3.0.0, at: 2026-07-29 }
verified: []
---
## CARD
goal: every FORMAT rule the M0 validator enforces still holds after the engine has written
gives: doctor · doctor --sync · parity with the M0 oracle, asserted by a test that runs both
scope: add/scripts/add.py · its red suite
beat: direction · next: add freeze build-doctor

## RULES
<must>
- M1 `doctor` runs over **e2's compiled graph**, never its own scan — the 150-line saving amendment A1 pre-booked, and the reason it cannot import repo tooling the skill does not ship
- M2 `doctor` and `scripts/validate_bundle.py` agree on every finding for this bundle. Where they differ, one is wrong about the format and the test says which
- M3 `--sync` is the A23 merge resolution: it regenerates every compiled artifact from node stamps, so a conflicted `index.md` or `log.md` is resolved by recomputation rather than by hand
- M4 `doctor` reports; only `--sync` writes, and it writes only files declared compiled
</must>
<reject>
- R:SECONDSCAN doctor building its own node scan -> "SECONDSCAN"
- R:DIVERGE a finding the M0 oracle would not also produce -> "DIVERGE"
- R:SYNCAUTHORED --sync overwriting a file humans author -> "SYNCAUTHORED"
</reject>

## PLAN
contract: <published at freeze>
strategy: <published at freeze>
scope: add/scripts/add.py · tests/engine/
floor: validator exits 0 on `.add/`; every earlier task's checks stay green

## CHECKS
- test_doctor_uses_the_graph · covers: M1, R:SECONDSCAN · no independent rglob
- test_parity_with_m0_oracle · covers: M2, R:DIVERGE · both tools report the same findings on .add/
- test_sync_regenerates_index · covers: M3 · a corrupted TOC is rebuilt from nodes
- test_sync_rotates_log · covers: M3 · closed milestones' groups fold into CLOSE
- test_sync_repairs_card_drift · covers: M3 · e6's render_card runs across the bundle
- test_sync_never_touches_authored · covers: M4, R:SYNCAUTHORED · a hand-authored node is not rewritten
red-first: every check above MUST fail for the right reason before BUILD.

## EVIDENCE
receipt: <runs/<n>.md>
gate: <PASS | RISK-ACCEPTED | HARD-STOP>
budget: <growth vs allocation · A3 invariant>
scope-check: <files touched vs `scope:`>

## LESSONS
- <lesson> -> add learn <domain|system|experience|quality|method>
