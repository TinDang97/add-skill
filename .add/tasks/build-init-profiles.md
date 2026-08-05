---
type: Task
title: init — create a bundle from a profile
goal: one command turns an empty directory into a conforming ABF-1 bundle the validator accepts
status: done
depth: standard
kind: feature
sensitivity: architecture
milestone: /milestones/engine-core.md
depends_on:
  - /tasks/port-okf-parse.md
  - /tasks/compile-graph.md
needs:
  - /tasks/port-okf-parse.md#gives
  - /tasks/compile-graph.md#gives
gives:
  - "init(root, profile, title) -> the three-file minimum bundle (index.md, log.md, PROJECT.md) plus specs"
  - "PROFILES — `code` and `doc` as engine data; the other three ship as template files (A1 cut)"
  - "a bundle that `scripts/validate_bundle.py` accepts at 0 errors on first run, with no hand editing"
scope:
  - add/scripts/add.py
  - tests/engine/test_init.py
budget: 213 lines wc -l of growth (amendment A1)
generated: { by: claude/opus-5, at: 2026-07-29 }
verified:
  - { by: "process:pytest", at: 2026-07-29, act: run, authority: process, outcome: PASS, receipt: /tasks/build-init-profiles.d/runs/2.md }
  - { by: "human:tindang", at: 2026-07-29, act: gate, authority: human, outcome: PASS }
---
## CARD
goal: `add init` produces a bundle that validates, from a profile, with zero hand editing
gives: init() · the `code` and `doc` profiles · a conforming three-file minimum
scope: add/scripts/add.py · tests/engine/test_init.py
beat: done · gated PASS · 74/213 lines · next: e4 node verbs ∥ e6 status

## RULES
<must>
- M1 a fresh `init` produces a bundle that `scripts/validate_bundle.py` accepts at **0 errors**,
     with no hand editing. The M0 oracle is the acceptance test, not a bespoke assertion
- M2 `init` **never overwrites**. An existing `index.md` makes it a no-op that reports, and the
     existing bundle is returned untouched (law 3 — a notary does not clobber)
- M3 the profile selects which specs exist, not which rules apply. Profiles are data: adding one
     must not require an engine change (goal 2's closed-lens claim)
- M4 every file `init` writes carries `generated: { by, at }`, so nothing in a new bundle is
     unattributed (OKF §10)
- M5 `init` ends by printing a `next:` line naming the exact command to run (law 4)
</must>
<reject>
- R:CLOBBER an init path that can overwrite an existing node -> "CLOBBER"
- R:HANDFIX a produced bundle that needs manual editing before it validates -> "HANDFIX"
- R:PROFILECODE a profile whose addition requires new engine branches -> "PROFILECODE"
</reject>
<after>
- a user with an empty directory can reach a first gated task without reading FORMAT.md
</after>
⚠ that the three-file minimum plus specs is enough to validate — if wrong: `init` grows a fourth
  required file and FORMAT §1's "minimum bundle" claim is wrong, which is a format defect, not an
  engine one. Tested directly by running the M0 validator on init's output.

## PLAN
contract: `init(root, profile="code", title=None) -> (graph, created: list[cid], note)`
strategy:
  Profiles are dicts of `{spec_slug: one-line goal}` — data, not branches. `init` writes the three
  reserved files plus one spec node per lens, then returns the compiled graph so the caller can
  print `next:` without a second scan.
  Failure handling: existing bundle → no-op with a note, never an exception; partial write is
  impossible because every file goes through e1's atomic `write`. Rollback: git, per specs/system.
scope: add/scripts/add.py · tests/engine/test_init.py
floor: `scripts/validate_bundle.py` exits 0 on `.add/` AND on every bundle `init` produces
least-sure: rules — M3. "Profiles are data" is easy to claim and easy to break with one `if
  profile == "doc"`. The suite therefore adds a profile at runtime and asserts it works with no
  engine change.

## CHECKS
- test_init_output_validates · covers: M1, R:HANDFIX · the M0 validator exits 0 on a freshly created bundle
- test_init_creates_minimum · covers: M1 · index.md, log.md and PROJECT.md all exist
- test_init_is_idempotent · covers: M2, R:CLOBBER · a second init reports and changes no byte
- test_init_never_overwrites_edited_node · covers: M2, R:CLOBBER · a hand-edited index.md survives a re-init
- test_profile_selects_specs · covers: M3 · the `code` and `doc` profiles produce different spec sets
- test_new_profile_needs_no_engine_change · covers: M3, R:PROFILECODE · a profile added at runtime works
- test_every_file_is_attributed · covers: M4 · every created node carries `generated.by` and `generated.at`
- test_init_prints_next · covers: M5 · the returned note names a runnable command
red-first: every check above MUST fail for the right reason before BUILD.

## EVIDENCE
receipt: /tasks/build-init-profiles.d/runs/2.md — 8/8 green · kind test-ids · freshness content ·
  red-first proven by runs/1.md
cross-oracle: `add init`'s output was accepted by `scripts/validate_bundle.py` at **0 errors, with
  no hand editing** (7 nodes · 2 info). The oracle predates the engine, so M1 is met by a test the
  engine's author did not choose
closed-lens: a `research` profile added **at runtime** produced a valid bundle with no engine
  change — goal 2's claim survives its first real test (M3, R:PROFILECODE)
⚠ open: only 2 of 5 profiles exist as engine data; the other 3 are unwritten template files. The
  closed-lens claim is proven for three profiles, not five
budget: 74 lines against 213 allocated — UNDER by 139. Engine 504/2400
gate: PASS — human:tindang, 2026-07-29
scope-check: match — `add/scripts/add.py` and `tests/engine/test_init.py` only

## LESSONS
- **The acceptance test should be one the author did not choose.** `init` is checked by M0's
  conformance oracle rather than by an assertion written alongside it. Every other verb that
  produces a bundle artifact should be judged the same way — by the validator, not by its own
  expectations. -> add learn quality
- **A one-directional falsifier generates no signal when you are winning.** A2 fires only when
  consumed exceeds allocated, so three consecutive under-runs produced no trigger and the 660
  pre-booked cuts stayed dead by default. Under-run is information too. Fixed in A3.
  -> add learn method
