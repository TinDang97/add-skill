---
type: Task
title: the covers: binding — a check that proves a rule, or says it cannot
goal: every Must is bound to a check that actually ran, or the gap is visible
status: done
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
verified:
  - { by: "process:run", at: 2026-07-30, act: run, authority: process, outcome: PASS, receipt: /tasks/build-evidence-binding.d/runs/1.md }
  - { by: "human:tindang", at: 2026-07-30, act: gate, authority: human, outcome: PASS }
---
## CARD
goal: every Must is bound to a check that actually ran, or the gap is visible
gives: covers · bind · unbound
scope: add/scripts/add.py · its red suite
beat: done · next: e5 `brief`, the last of wave 3

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
contract:
  `covers(node) -> {rule_id: [check_id]}` · `rules_of(node) -> [rule_id]` ·
  `bind(node, reported) -> (proven: {rule: [id]}, unproven: {rule: [id]})` ·
  `unbound(node, reported) -> [rule_id]` · `extract_ids(path) -> {test_id: pass|fail}`
strategy:
  Two independent parses of one node, both T2 and both regex-anchored: `rules_of` reads the
  `<must>`/`<reject>` blocks for rule IDs, `covers` reads the CHECKS section for `· covers: …`.
  `bind` is then pure set arithmetic against a dict of IDs the RUNNER reported — the binding
  never inspects a test file, only what a report says ran. `extract_ids` reads junit-xml via
  `xml.etree` (A1's v1.0 cut) and returns `{}` on any OSError or ParseError, so an absent or
  corrupt report degrades the kind rather than raising.
  Failure handling: every function is a notary — a node with no CHECKS yields empty maps, not an
  error. Rollback: git.
scope: add/scripts/add.py · tests/engine/test_evidence_binding.py
floor: validator exits 0 on `.add/`; every earlier task's checks stay green
least-sure: rules — M2. The kind ladder is only honest if `test-ids` is genuinely reachable; if
  real runners rarely emit parseable IDs, A24's top rung is decoration and A15 reopens.

## CHECKS
- test_covers_parsed_from_checks · covers: M1 · the map is built from the CHECKS section, keyed by rule
- test_bind_requires_reported_id · covers: M1, R:LABEL · a covers: naming a test that did not run proves nothing
- test_failing_check_does_not_prove · covers: M1, R:LABEL · a check that RAN and FAILED proves nothing either
- test_unbound_musts_reported · covers: M3, R:SILENTGAP · a Must with no check at all is visible
- test_extract_ids_from_junit · covers: M2 · junit-xml is the v1.0 format A1 scoped this to
- test_extract_ids_missing_file_is_unknown · covers: M2 · no report means unknown, never an invented pass
- test_extract_ids_corrupt_is_unknown · covers: M2 · unparseable output reports; it does not raise
- test_run_earns_test_ids_with_junit · covers: M2 · with real IDs the receipt may finally claim test-ids
- test_run_without_junit_stays_command_exit · covers: M2 · no report, no promotion — e7's degradation holds
- test_live_bundle_binding · covers: M1, M3 · this repo's own gated tasks are checked for unbound Musts
red-first: every check above MUST fail for the right reason before BUILD.
<!-- Corrected 2026-07-30, BEFORE the gate: the authored list named
     `test_ids_unknown_degrades_kind`, which was never written — one fictional ID in five. The
     suite splits M2 across four real checks instead. This node was one gate away from being the
     tenth instance of the defect F2 records. The correction is legitimate here precisely because
     nothing had been stamped yet; the same edit on a gated node would be R:ERASE. -->

## EVIDENCE
receipt: /tasks/build-evidence-binding.d/runs/1.md — 10/10 green · **kind: test-ids · ids: 10/10
  reported** · the first receipt in this project to EARN the top rung of A24 rather than assert it
red-first: 9/10 failed on absent `covers`. One passed —
  `test_run_without_junit_stays_command_exit` — because it guards behaviour e7 already
  established. Recorded as a regression check, not counted as a red
floor: validator CONFORMS on `.add/`; full suite 113 green (15+16+8+15+17+14+10 + validator)
found-on-live-bundle: **F2** — 67 of 133 rules across 15 gated tasks are PROVEN; 65 are claimed by
  check IDs that do not exist in any suite, across 9 M0 tasks (61 distinct fictional IDs). See
  /milestones/engine-core.md#findings. The verb's first act was to convict the milestone that
  specified it
budget: 97 lines against 160 allocated. Engine 1,038/2,400 · A3 invariant: 1,038 + 707 (e5 267 +
  e8 200 + e9 80 + e10 80 + e11 80) = **1,745 / 2,400 — slack 655**
scope-check: match — `add/scripts/add.py` and `tests/engine/test_evidence_binding.py` only
gate: PASS — human:tindang, 2026-07-30, stamped by the engine
⚠ open: `rules_of` did not parse `/tasks/define-scale-rules.md`'s rule block at all, so that node
  reports zero rules rather than unproven ones. A parser gap that reads as a clean bill of health
  is worse than one that raises — `e8 doctor` owes a check that a Task with a RULES section yields
  at least one rule ID
> **Corrected 2026-07-30, minutes after the gate — the diagnosis above is wrong, and it is left
> standing because the gate was taken with it.** `rules_of` parsed nothing because
> `define-scale-rules` **has no RULES section**: its body is CARD · CHECKS · EVIDENCE. Its three
> checks cite `G1`, `G2`, `G3` — a rule-ID namespace FORMAT does not define — and all three test
> names are fictional. So it is not a parser gap but a node that declares checks over rules it
> never states, and the M0 validator accepted it. `e8 doctor` still owes the check; it must assert
> that every `covers:` referent RESOLVES to a rule the node declares, which is strictly stronger
> than what was written above. Found by reading the node instead of trusting my own summary of it.

## LESSONS
- **A `covers:` label costs nothing to write and reads exactly like proof.** Nine gated M0 tasks
  named 61 tests that were never written, and no reader — including four human gates — noticed,
  because a plausible test name is indistinguishable from a real one at review speed. Only
  binding against what a runner REPORTED could tell them apart. That asymmetry is the whole
  argument for A15/A16: the label is free, the binding is not. -> add learn quality
- **The tool that detects a defect must be pointed at its own author's work first.** e12's own
  CHECKS carried one fictional ID. It was found by running the verb on the node one minute before
  gating it. A method that only audits other people's artifacts is a rhetorical device.
  -> add learn method
- **Fixing a fictional binding is only honest before the stamp.** e12's CHECKS were corrected
  freely; M0's nine cannot be, because a gate was taken against them and rewriting the claim
  would erase what was actually accepted. The remedy for a gated false claim is a recorded
  finding, not a quiet edit — which is exactly the asymmetry §3.6 encodes. -> add learn method
