---
type: Task
title: CHECKS compiled from the suite, not authored beside it
goal: a check citation cannot name a test that does not exist, because it is extracted from the tests
status: direction
depth: standard
kind: feature
sensitivity: architecture
milestone: /milestones/engine-core.md
depends_on:
  - /tasks/build-evidence-binding.md
needs:
  - /tasks/build-evidence-binding.md#gives
generated: { by: add/3.0.0, at: 2026-07-30 }
verified: []
---
## CARD
goal: a check citation cannot name a test that does not exist, because it is extracted from the tests
gives: checks_of(suite) · checks --sync · checks --verify (F2 in both directions)
scope: add/scripts/add.py · tests/engine/test_checks_compiler.py
beat: direction · next: add freeze compile-checks-from-suite

## RULES
<must>
- M1 the CHECKS section is **compiled from the suite's docstrings**, never authored beside it (L7 —
     compiled beats authored). This is already possible: 118 of this repo's 131 tests carry an
     explicit `covers:` in their docstring
- M2 `--verify` reports F2 in BOTH directions — a citation naming a test that exists nowhere, and a
     `covers:` referent naming a rule the node never declares. `define-scale-rules` is the second
     shape and the M0 validator accepted it
- M3 a test carrying no `covers:` is REPORTED, never guessed at from its name. An unlabelled test is
     a visible gap; an inferred label is F2 with extra steps
- M4 `--sync` is surgical: it rewrites the CHECKS section and nothing else, using e1's line editor,
     and it never touches a node whose CHECKS already verify
</must>
<reject>
- R:AUTHOREDCHECK a CHECKS line surviving `--sync` with no test behind it -> "AUTHOREDCHECK"
- R:GUESS inferring which rule a test covers from its name -> "GUESS"
- R:WIDEEDIT a sync that changes any byte outside the CHECKS section -> "WIDEEDIT"
- R:SILENTFIX rewriting a GATED node's CHECKS to make it verify -> "SILENTFIX"
</reject>
<after>
- F2's defect class becomes structurally impossible for every task authored after this ships:
  a citation is extracted, so it cannot be aspirational
- the CHECKS section stops being the one part of a node where a claim costs nothing to make
</after>
⚠ that docstrings are a durable place to carry `covers:` — if wrong: the citation belongs in a
  decorator or a sidecar map, and this becomes a parser over that instead. The 118/131 measurement
  is what makes the docstring the cheapest option today, and it is a measurement of THIS project's
  habits, not of anyone else's.

## PLAN
contract: <published at freeze>
strategy: <published at freeze>
scope: add/scripts/add.py · tests/engine/test_checks_compiler.py
floor: validator CONFORMS on `.add/`; every earlier task's checks stay green
least-sure: rules — M4 vs R:SILENTFIX. `--sync` must be able to fix an ungated node and must refuse
  a gated one, and the boundary between those is exactly the §3.6 asymmetry F2 turned on.

## CHECKS
- test_checks_extracted_from_docstrings · covers: M1 · covers: is read from the test, not the node
- test_sync_writes_the_checks_section · covers: M1 · a node with no CHECKS gains the real ones
- test_sync_rewrites_only_checks · covers: M4, R:WIDEEDIT · a byte-diff outside CHECKS is zero
- test_sync_is_idempotent · covers: M4 · a second sync writes nothing
- test_sync_refuses_a_gated_node · covers: M4, R:SILENTFIX · §3.6 — a gated claim is recorded, not repaired
- test_verify_catches_fictional_citation · covers: M2 · a named test that does not exist is reported
- test_verify_catches_unresolvable_referent · covers: M2 · a covers: naming no declared rule is reported
- test_unlabelled_test_is_reported · covers: M3, R:GUESS · no rule is inferred from a test name
- test_no_authored_check_survives_sync · covers: M1, R:AUTHOREDCHECK · invented lines do not persist
- test_live_bundle_verify_reports_f2 · covers: M2 · the 65 labelled-not-proven rules are REPORTED, not fixed
red-first: every check above MUST fail for the right reason before BUILD.

## EVIDENCE
receipt: <runs/<n>.md>
gate: <PASS | RISK-ACCEPTED | HARD-STOP>
budget: <growth vs allocation · A3 invariant>
scope-check: <files touched vs `scope:`>

## LESSONS
- <lesson> -> add learn <domain|system|experience|quality|method>
