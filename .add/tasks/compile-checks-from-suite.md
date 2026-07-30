---
type: Task
title: CHECKS compiled from the suite, not authored beside it
goal: a check citation cannot name a test that does not exist, because it is extracted from the tests
status: done
depth: standard
kind: feature
sensitivity: architecture
milestone: /milestones/engine-core.md
depends_on:
  - /tasks/build-evidence-binding.md
needs:
  - /tasks/build-evidence-binding.md#gives
generated: { by: add/3.0.0, at: 2026-07-30 }
verified:
  - { by: "claude/opus-5", at: 2026-07-30, act: freeze, authority: human }
  - { by: "process:run", at: 2026-07-30, act: run, authority: process, outcome: FAIL, receipt: /tasks/compile-checks-from-suite.d/runs/1.md }
  - { by: "process:run", at: 2026-07-30, act: run, authority: process, outcome: FAIL, receipt: /tasks/compile-checks-from-suite.d/runs/2.md }
  - { by: "process:run", at: 2026-07-30, act: run, authority: process, outcome: FAIL, receipt: /tasks/compile-checks-from-suite.d/runs/3.md }
  - { by: "process:run", at: 2026-07-30, act: run, authority: process, outcome: PASS, receipt: /tasks/compile-checks-from-suite.d/runs/4.md }
  - { by: "human:tindang", at: 2026-07-30, act: gate, authority: human, outcome: PASS, receipt: /tasks/compile-checks-from-suite.d/runs/4.md, brief: "sha256:7b2e21c5b54b9909" }
scope:
  - add/scripts/add.py
  - tests/engine/test_checks_compiler.py
---
## CARD
goal: a check citation cannot name a test that does not exist, because it is extracted from the tests
gives: checks_of(suite) · checks --sync · checks --verify (F2 in both directions)
scope: add/scripts/add.py · tests/engine/test_checks_compiler.py
beat: done · next: add status --milestone engine-core

## RULES
<must>
- M1 the CHECKS section is **compiled from the suite**, never authored beside it (L7 — compiled
     beats authored). The citation is read from wherever the test carries it: a docstring (118 of
     this repo's tests) or a `# --- <name> · covers: … ---` header above the function (e15's 5).
     Both carriers, because both already exist in this repo — not because two are elegant
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
> **ANSWERED before BUILD, 2026-07-30, and the answer is no.** e15 was executed by a subagent which
> carried `covers:` in `# --- name · covers: … ---` comment headers instead of docstrings, and left
> two machinery tests deliberately unlabelled. One author, one task, and the convention already
> diverged. M1 is corrected above to read both carriers rather than to mandate one — a rule written
> against a habit that a second author does not share is a rule that will be broken by accident.
> The ⚠ stands as written (§3.6); the correction is above it, not inside it.

## PLAN
contract: `checks_of(paths) -> {test_id: ([rule_ids], description)}` reading BOTH carriers ·
  `unlabelled(paths)` · `checks_verify(root, cid, paths) -> [{severity, message, rule, test}]`
  graded `pending` vs `error` on whether a gate has been taken · `checks_sync(root, cid, paths)`
  rewriting only `## CHECKS`, refusing a gated node
strategy: the extractor is the whole task and everything else is a thin shell over e1's line editor.
  Discovery goes through `ast` rather than a regex — decided during BUILD, after a regex read three
  `def test_` out of fixture STRING CONSTANTS on this task's own node. Grading came second and was
  also discovered during BUILD: the first live run flagged 13 nodes as if they were 13 defects, when
  4 were ungated M1 tasks whose tests are not written yet. A citation that cannot resolve is a
  finding only once someone has gated against it
scope: add/scripts/add.py · tests/engine/test_checks_compiler.py
floor: validator CONFORMS on `.add/`; every earlier task's checks stay green
least-sure: rules — M4 vs R:SILENTFIX. `--sync` must be able to fix an ungated node and must refuse
  a gated one, and the boundary between those is exactly the §3.6 asymmetry F2 turned on.

## CHECKS
- test_a_long_description_is_cut_at_a_word · covers: M1 · a compiled line that ends mid-word is a line a reader stops trusting. The first compiled section of this…
- test_a_test_inside_a_string_literal_is_not_a_test · covers: M1, R:GUESS · a regex over source text reads code out of quoted strings. Found by running `checks_sync` on THIS task's own…
- test_checks_extracted_from_comment_headers · covers: M1 · e15's carrier, discovered before this was built rather than after. A subagent wrote `# --- test_gamma ·…
- test_checks_extracted_from_docstrings · covers: M1 · the citation is read from the test, not from the node
- test_description_survives_compilation · covers: M1 · compile the citation, keep the human's reason for the check. The first compiled section rendered every line…
- test_gated_citation_is_a_defect · covers: M2 · once a gate is taken against the claim, the same gap is an error
- test_live_bundle_verify_reports_f2 · covers: M2 · F2's 65 rules, REPORTED by the verb rather than by an ad-hoc script. Reports rather than asserting zero: the…
- test_no_authored_check_survives_sync · covers: M1, R:AUTHOREDCHECK · a citation with no test behind it does not persist
- test_no_rule_inferred_from_a_name · covers: M3, R:GUESS · `test_m1_something` must not be read as covering M1
- test_pending_citation_is_not_a_defect · covers: M2 · a test not yet written on a node not yet gated is not a finding. Run on the live bundle, `checks_verify`…
- test_sync_is_idempotent · covers: M4 · a second sync writes nothing at all
- test_sync_on_a_gated_node_still_reports · covers: M2, M4 · refusing to fix is not refusing to say. The finding survives the refusal
- test_sync_preserves_unlabelled_note · covers: M3 · the honest gap is carried into the section, not dropped from it. e15 recorded two machinery tests as…
- test_sync_refuses_a_gated_node · covers: M4, R:SILENTFIX · §3.6: a gated claim is recorded, never repaired. This is the asymmetry F2 turned on. e12's own CHECKS were…
- test_sync_rewrites_only_checks · covers: M4, R:WIDEEDIT · every byte outside the CHECKS section survives
- test_sync_writes_the_checks_section · covers: M1 · the invented line goes; the real ones arrive
- test_unlabelled_test_is_reported · covers: M3, R:GUESS · an unlabelled test is a visible gap, never an inferred label
- test_unresolvable_referent_is_always_an_error · covers: M2 · a rule the node never declares is wrong whatever its status. Unlike a missing test, this cannot become true…
- test_verify_catches_fictional_citation · covers: M2 · F2's first shape: a CHECKS line naming a test that exists nowhere
- test_verify_catches_unresolvable_referent · covers: M2 · F2's second shape, which the M0 validator accepted. `define-scale-rules` cites `G1`/`G2`/`G3` and declares no…
- test_verify_is_clean_after_sync · covers: M2, M4 · the two halves agree: what sync writes, verify accepts
red-first: every check above MUST fail for the right reason before BUILD.
<!-- COMPILED from the suite (e14). Do not author here: a citation edited by hand
     cannot be distinguished from one that was never true (F2). -->

## EVIDENCE
receipt: /tasks/compile-checks-from-suite.d/runs/4.md — 189/189 reported · kind test-ids ·
  freshness content · 21 of this node's own cited IDs passed · 0 failed
red-first: 21 checks, each red before its code. Three were written red DURING the build from
  reading output rather than from the RULES: the string-literal defect, the grading gap, and the
  mid-word truncation. `--sync` on this node then compiled 21 lines from 21 real tests, and a second
  sync refused as a no-op
floor: validator on `.add/` — **58 nodes · 162 edges · 0 info · 0 error, CONFORMS.** Full suite 189
  green
outcome: **F2's defect class is now structurally impossible for anything authored after this.** The
  section this node carries was not written by me: `checks_of` read it out of the suite, citations
  and all. Both directions of `--verify` are live, and the M0 shape the old validator accepted (a
  `covers:` naming a rule the node never declares) is now an `error` at any status
budget: engine 1,448 → **1,618 = 170 lines against 90 allocated (+89%)** — the largest overrun of
  this milestone, and it bought two things the allocation did not price: `ast`-based discovery
  instead of a regex, and severity grading. A3 invariant: 1,618 + 440 (e8 200 · e9 80 · e10 80 ·
  e11 80) = **2,058 / 2,400 — slack 342.** D-6 untouched
scope-check: match — `add/scripts/add.py`, `tests/engine/test_checks_compiler.py`. Two files outside
  `scope:` changed and both are recorded, not smuggled: this node's own body (the compiled section,
  which is what the verb is FOR) and the milestone's findings block (F6)
found-here: **F6** — `run`'s default `cwd` is `.add/`, which contradicts the format's repo-relative
  `scope:` paths and made a test runner write `.pytest_cache/` into the bundle. Recorded on the
  milestone, assigned to e10, deliberately not fixed here. `runs/2.md` and `runs/3.md` are kept as
  the recorded outcomes of that mistake
post-gate: **a 22nd check was written AFTER this gate, and `--sync` refused to fold it in.**
  Reviewing the diff surfaced one more defect: `checks_sync` walks `paths` twice, so a generator
  made the second walk empty and the note read "22 checks compiled from 0 suite files" — the
  section correct, the count false. `test_a_generator_of_paths_reports_the_true_file_count` is red-
  first proof of it; the fix is one `list(paths)`. Engine 1,618 → **1,621 = 173 lines against 90
  (+92%)**; A3 invariant 1,621 + 440 = **2,061 / 2,400, slack 339.** The numbers in `budget:` above
  were true when the gate was taken and are left as written (§3.6).
  The section above still lists 21 checks and MUST: R:SILENTFIX refused the repair on this node,
  its own author's node, which is the first time that rule has fired against me. The suite is 22
  and the record says 21 — that gap is the rule working, not a bookkeeping error. It closes when a
  later task re-gates this node, or never, and either is honest.
gate: PASS — human:tindang, 2026-07-30, recorded by `add gate` at authority `human`
  (A17: `add/scripts/add.py` is a sensitive path). Freshness fresh, brief
  `sha256:7b2e21c5b54b9909`. The +89% overrun was put to the human at the gate with
  its reason and PASSED on the merits, not waived

## LESSONS
- **A regex that reads code is an oracle that cannot tell code from a quotation.** `DEF_TEST` found
  `def test_alpha` inside a fixture's string constant and compiled three tests that do not exist —
  into the CHECKS section of the very task whose goal is that a citation cannot name a test that
  does not exist. e15 had fixed the same class in the validator two hours earlier (an unanchored
  `COVERS` reading PLAN prose), and I reintroduced it in the engine while holding the lesson in
  hand. `ast` is stdlib, it is shorter than the regex it replaced, and it cannot make this mistake.
  -> add learn domain
- **Compile what a human cannot keep honest; carry what only a human knows.** The first version
  compiled every line as `· covers: M1 · proves M1` — perfectly accurate, perfectly empty. It had
  extracted the citation and thrown away the sentence explaining why the check exists, which is the
  part no tool can reconstruct. Extraction is not a licence to replace the author everywhere it
  can; it is a tool for the places where the author's claim was unverifiable.
  -> add learn quality
- **Every defect this wave was found by READING the output, and none by running the tests.** Four
  times now: e5's mangled ref ids, e1's parser, e13's silently-skipped freshness, and this task's
  phantom tests plus its conflated severities. The suite tests what the code was specified to do,
  so it is silent exactly where the specification never mentioned what a reader notices first. The
  loop that works is: build it, RUN IT ON THIS BUNDLE, read the output, write the red test for what
  looks wrong. Dogfooding is not validation of the feature — it is the oracle the suite is not.
  -> add learn method
- **Grading a finding is part of reporting it.** 13 nodes flagged, 9 real and 4 merely unbuilt. An
  ungraded report of the true set is worse than a graded report of the same set, because the reader
  who cannot separate them stops reading all of them. `pending` vs `error` turns on one fact the
  bundle already records: whether a gate has been taken against the claim (§3.6).
  -> add learn system
