---
type: Task
title: doctor — conformance and repair over the compiled graph
goal: every FORMAT rule the M0 validator enforces still holds after the engine has written
status: done
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
verified:
  - { by: "claude/opus-5", at: 2026-07-30, act: freeze, authority: human }
  - { by: "process:run", at: 2026-07-30, act: run, authority: process, outcome: PASS, receipt: /tasks/build-doctor.d/runs/1.md }
  - { by: "process:run", at: 2026-07-30, act: run, authority: process, outcome: PASS, receipt: /tasks/build-doctor.d/runs/2.md }
  - { by: "human:tindang", at: 2026-07-30, act: gate, authority: human, outcome: PASS, receipt: /tasks/build-doctor.d/runs/2.md, brief: "sha256:59846163a8e48971" }
---
## CARD
goal: every FORMAT rule the M0 validator enforces still holds after the engine has written
gives: doctor · doctor --sync · parity with the M0 oracle, asserted by a test that runs both
scope: add/scripts/add.py · its red suite
beat: done · next: add freeze build-doctor

## RULES
<must>
- M1 `doctor` runs over **e2's compiled graph**, never its own scan — the 150-line saving amendment A1 pre-booked, and the reason it cannot import repo tooling the skill does not ship
- M2 `doctor` and `scripts/validate_bundle.py` agree on every finding for this bundle. Where they differ, one is wrong about the format and the test says which
- M3 `--sync` is the A23 merge resolution: it regenerates every compiled artifact from node stamps, so a conflicted `index.md` or `log.md` is resolved by recomputation rather than by hand
- M4 `doctor` reports; only `--sync` writes, and it writes only files declared compiled
- M5 `doctor` reports an **orphaned receipt** — a Run node under `<slug>.d/runs/` that no `verified[]`
     stamp points at. This is F3's assigned check. e13's `orphans()` already computes the set; what
     has never existed is the report that makes it visible. 8 of this bundle's receipts are orphaned
     and predate the fix, so the count must be REPORTED and must not go to zero by repair
- M6 `doctor` surfaces e14's `checks_verify` errors as findings, so F2's shape is caught by the
     conformance oracle and not only by a verb someone remembers to run. `pending` is not a finding
     here — an ungated node's CHECKS are a plan (e14's grading), and promoting it would make
     `doctor` scream about every task not yet built
</must>
<reject>
- R:SECONDSCAN doctor building its own node scan -> "SECONDSCAN"
- R:DIVERGE a finding the M0 oracle would not also produce -> "DIVERGE"
- R:SYNCAUTHORED --sync overwriting a file humans author -> "SYNCAUTHORED"
- R:REPAIRAWAY `--sync` making an orphaned receipt or a gated F2 claim disappear instead of
  reporting it -> "REPAIRAWAY"
</reject>
⚠ that M2's parity is achievable at all. `scripts/validate_bundle.py` is 400+ lines of repo tooling
  and `doctor` gets ~200 total while being forbidden from importing it (the skill ships without this
  repo). Parity may turn out to mean "no finding the validator would not also produce" — a subset,
  not an equality — and if so the rule is what changes, with the reason recorded, not the test.
> **ANSWERED before BUILD, 2026-07-30, by reading the oracle rather than guessing at it.** The
> validator emits exactly **seven** codes — `missing_frontmatter`, `type_empty`,
> `edge_out_of_bundle` (error) and `unknown_type`, `edge_unresolved`, `broken_md_link`,
> `compiled_undeclared` (info) — plus `covers_referent`. `doctor` cannot equal it and should not:
> `doctor` also knows things the validator cannot, because it reads STAMPS (orphaned receipts, F2
> claims behind a gate, CARD drift). So M2 is **asymmetric parity, and this is the reading the rule
> carries from here**: on the validator's own seven codes the two must agree finding-for-finding;
> beyond them `doctor` may report more. R:DIVERGE means "no CONFORMANCE finding the M0 oracle would
> not also produce", not "no finding at all". The ⚠ stands as written (§3.6); this is the answer to
> it, not an edit of it.
> Also corrected here: the `contract:` line below said each finding carries a `message`. The
> validator's key is **`detail`**, and two oracles whose findings cannot be diffed by key are not
> comparable — which is the whole point of M2. `doctor` emits `{severity, code, detail}` plus an
> optional `node`, so a parity test can compare dicts rather than prose.

## PLAN
contract: `doctor(root) -> [{severity, code, node, message}]` over e2's compiled graph, using the
  M0 oracle's finding codes · `doctor_sync(root) -> (changed, note)` recomputing only the artifacts
  FORMAT declares compiled (`index.md` TOC, `log.md` groups, CARD lines) · both reachable as one
  verb with a flag
strategy: `doctor` is a REPORTER composed from oracles that already exist — `cycles`, `card_drift`,
  `orphans`, `checks_verify`, `resolve` — plus the frontmatter rules the validator enforces that no
  verb yet reads. Almost none of it is new logic; the work is choosing the finding set and proving
  parity. `--sync` is A23 merge resolution: a conflicted compiled file is resolved by recomputation,
  which is only sound because L1 says the nodes are the database and the compiled bodies are views.
scope: add/scripts/add.py · tests/engine/test_doctor.py
floor: validator exits 0 on `.add/`; every earlier task's checks stay green
least-sure: rules — M2. Parity with a 400-line oracle inside a 200-line allocation is the claim most
  likely to be wrong, and the ⚠ above says what changes if it is.
budget-risk: **the last three tasks overran +37%, +89% and +92%.** At +92% e8 is 384 lines, which
  keeps A3 (consumed 2,005 + remaining 240 = 2,245/2,400) but cuts slack from 339 to 155 with three
  tasks left. A1 pre-booked doctor's 150-line saving as "runs over e2's compiled graph" — that is M1,
  and it is the reason this fits at all. If parity forces a second scan, the budget goes with it.

## CHECKS
- test_a_broken_edge_is_found_by_both · covers: M2, R:DIVERGE · the same injected defect produces the same code in both tools. Parity on a clean bundle is cheap: both report…
- test_doctor_on_the_live_bundle_is_clean · covers: M2 · the project's own bundle carries no conformance error under its own oracle. The floor every task in this…
- test_doctor_reports_nothing_on_a_fresh_bundle · covers: M1 · a bundle the engine just created has no conformance findings. The floor for every other assertion here: if…
- test_doctor_reports_only_and_sync_writes · covers: M4 · `doctor` is a reporter; not one byte moves unless `--sync` was asked for. Law 3, stated as a test: the notary…
- test_doctor_uses_the_graph · covers: M1, R:SECONDSCAN · doctor reads e2's compiled graph and never rglobs its own. Asserted by making a second scan impossible:…
- test_f2_claims_surface_as_findings · covers: M6 · a gated node citing a test that exists nowhere is a doctor finding. F2's 65 rules were labelled, not proven…
- test_live_orphans_are_all_reported · covers: M5 · the eight orphans this bundle carries are reported, every one. They predate F3's fix and cannot be stamped…
- test_missing_frontmatter_is_reported_by_doctor · covers: M2, R:DIVERGE · the code F6 proved doctor was blind to. `.pytest_cache/README.md` was written into this bundle by a command…
- test_orphaned_receipt_is_reported · covers: M5 · a receipt no `verified[]` stamp points at is a finding, not a silence. F3's assigned check. The receipt…
- test_orphans_are_not_repaired_away · covers: M5, R:REPAIRAWAY · `--sync` cannot make an orphaned receipt disappear. The tempting repair is to append the missing stamp. That…
- test_orphans_from_the_graph_match_orphans_from_the_disk · covers: M1, R:SECONDSCAN · `orphans` reads Run nodes from the graph, same answer as before. e13 computed this by rglobbing `runs/*.md`…
- test_parity_with_m0_oracle · covers: M2, R:DIVERGE · on the validator's own seven codes, both oracles agree exactly. Run on the LIVE bundle, which is the only…
- test_pending_checks_are_not_findings · covers: M6 · an unbuilt node's planned CHECKS are a plan, not a defect. e14 learned this by flagging thirteen nodes when…
- test_reserved_files_are_not_missing_frontmatter · covers: M2, R:DIVERGE · `index.md` and `log.md` carry no frontmatter BY DESIGN. They are compiled bodies (A11/A20). The validator…
- test_scan_collects_strays_without_polluting_the_graph · covers: M1 · `scan` reports non-node files through a caller-owned list, not the graph. e2's contract, extended after its…
- test_sync_is_idempotent · covers: M3 · a second sync writes nothing, because the views already match the nodes. An oracle that always reports work…
- test_sync_never_touches_authored · covers: M4, R:SYNCAUTHORED · a file humans author is not rewritten, ever. `log.md`'s `## Notes` is human-owned by A20 and every node body…
- test_sync_regenerates_index · covers: M3 · a corrupted TOC is rebuilt from the nodes, because the nodes are the database. This is A23 merge resolution:…
- test_sync_repairs_card_drift · covers: M3 · e6's `render_card` runs across the bundle, not one node at a time. `card_drift` has reported this since e6…
- test_the_suite_is_parsed_once_per_doctor_run · covers: M6 · extracting the suite 59 times to answer one question is a defect, not a cost. `checks_verify` extracts every…
red-first: every check above MUST fail for the right reason before BUILD.
<!-- COMPILED from the suite (e14). Do not author here: a citation edited by hand
     cannot be distinguished from one that was never true (F2). -->

## EVIDENCE
receipt: /tasks/build-doctor.d/runs/2.md — 211/211 reported · kind test-ids · freshness content ·
  20 of this node's cited IDs passed · 0 failed. Receipt 1 was superseded: A22 declared it STALE
  because F8's fix touched `add/scripts/add.py` after the run, and `gate` refused on that basis —
  the freshness check earning its keep on the task that added the conformance oracle
red-first: 20 checks, all 20 red before any code, each failing on the ABSENCE of `doctor` /
  `doctor_sync` / `scan(strays=)` rather than on a fixture mistake. Three initially failed with
  `FileNotFoundError` because this file unpacked `add.new`'s `(cid, note)` backwards — fixed before
  BUILD, because a test that is red for the wrong reason proves nothing when it turns green
compiled-checks: the section above was written by `add checks --sync` (e14), not by hand. The
  authored plan listed 10 checks; the suite finished at **20**, and the ten it did not predict are
  the ones discovered while building. This is the first node in the project whose CHECKS section no
  human typed, which is the milestone's EXIT criterion holding for real on one file
outcome: **the last of the ten verbs.** `doctor` reports 93 findings on this bundle — 85
  `checks_citation` and 8 `orphan_receipt` — and **zero conformance findings, matching the M0
  validator exactly on all seven of its codes.** Both halves matter: the agreement is M2, and the 93
  are the things the validator structurally cannot see because it does not read stamps
f2-restated-precisely: 85 breaks down as **82 citations naming a test that exists nowhere and 3
  referents naming a rule the node never declares**, across **exactly F2's nine gated M0 tasks** and
  no others. F2's own number was 65 *rules* unproven / 61 distinct test names; 85 counts
  (rule, test) PAIRS plus the three `G1`/`G2`/`G3` referents. Different unit, same nine nodes —
  stated here because quoting "65" against a report that prints 85 would look like a discrepancy
budget: engine 1,621 → **1,816 = 195 lines against 200 allocated (98%)** — under, and the first
  task in four to be. A1's pre-booked 150-line saving is what did it: `doctor` composes `cycles`,
  `card_drift`, `orphans` and `checks_verify` instead of re-deriving them. A3 invariant:
  1,816 + 240 (e9 80 · e10 80 · e11 80) = **2,056 / 2,400 — slack 344.** D-6 untouched
scope-check: `add/scripts/add.py` and `tests/engine/test_doctor.py` as declared. Two gated nodes
  were also touched and both changes are recorded corrections, not edits: `/tasks/compile-graph.md`
  (e2's `scan` contract extended, decided at human authority) and this node's own compiled CHECKS
gate: PASS — human:tindang, 2026-07-30, at authority `human` (A17). Brief `sha256:59846163a8e48971`.
  Refused TWICE before recording, both times correctly: once on F8 (a backticked path pattern read
  as a template placeholder) and once on A22 freshness after F8's fix. The verb that exists to
  refuse refused its own author's node twice in ten minutes
found-here: **F7** (a failing check can be recorded as PASSED — test IDs keyed by bare name; this
  receipt reads 211/211 for a 212-test suite because `test_sync_is_idempotent` exists in two files)
  and **F8** (fixed here). F7 is assigned to a new task by human decision: fix the ID shape before
  any further gate is taken

## LESSONS
- **The compiled graph was lossy for exactly the defect that had already bitten this project.**
  `scan` drops any file with no frontmatter — correct for a graph, and it made `doctor` structurally
  blind to `missing_frontmatter`, the M0 oracle's most consequential error. Not theoretical: F6's
  `.pytest_cache/README.md` was that file shape, and a shipped `add doctor` without this extension
  would have certified a bundle the validator called broken. Two rules on one node contradicted each
  other (M1 use the graph, M2 reach parity) and the contradiction was invisible until something was
  built against both. A conflict between two Musts is a design question the node cannot answer by
  itself; it took a measurement and a human decision.
  -> add learn system
- **An oracle's basis is part of its contract, not an implementation detail.** `orphans` counted
  files under `runs/`; it now counts nodes of `type: Run`. Same eight receipts on this bundle — but
  the old basis was silently wrong in two directions: a receipt outside `runs/` was invisible, and a
  malformed one with no frontmatter counted as evidence. The equivalence was asserted against a
  hand-recomputed directory walk, because the obvious test — comparing the function to itself with
  and without a `graph=` argument — cannot fail. I wrote that vacuous version first.
  -> add learn quality
- **45x, from a signature that looked harmless.** `checks_verify(root, cid, paths)` re-extracts the
  suite for every node, so `doctor(paths=…)` parsed twelve files fifty-nine times: 1,650 ms against
  37 ms, on the verb whose entire purpose is to run in CI. Found by timing the dogfood run rather
  than by reading the code, and fixed with one shared `extracted` map in five lines. The test counts
  `ast.parse` calls instead of measuring a clock, because a timing assertion is a flaky test and a
  count is a true one.
  -> add learn method
- **`--sync` had to be talked out of eating authored prose.** `index.md` is a COMPILED body by A11,
  so recomputing it wholesale looks obviously right — and it would have destroyed every hand-written
  description in the TOC ("ten verbs, ≤2,400 lines, dogfooded here" exists nowhere else in the
  bundle). A file being compiled does not make every byte in it derivable. The resolution is
  surgical: recompute the mechanical tokens, carry the authored tail across keyed by path, and never
  touch frontmatter, because `sensitive_paths` IS the A17 floor.
  -> add learn domain
