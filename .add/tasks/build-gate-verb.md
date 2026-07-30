---
type: Task
title: gate — the verdict, its three refusals, and the quick lane
goal: a gate is recorded only when the evidence entitles it, and a quick task costs one engine call
status: done
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
verified:
  - { by: "claude/opus-5", at: 2026-07-30, act: freeze, authority: human }
  - { by: "process:run", at: 2026-07-30, act: run, authority: process, outcome: PASS, receipt: /tasks/build-gate-verb.d/runs/1.md }
  - { by: "human:tindang", at: 2026-07-30, act: gate, authority: human, outcome: PASS, receipt: /tasks/build-gate-verb.d/runs/1.md, brief: "sha256:849f741108fe4a87" }
  - { by: "process:run", at: 2026-07-30, act: run, authority: process, outcome: PASS, receipt: /tasks/build-gate-verb.d/runs/2.md }
  - { by: "human:tindang", at: 2026-07-30, act: gate, authority: human, outcome: PASS, receipt: /tasks/build-gate-verb.d/runs/2.md, brief: "sha256:7e7013b05039d206" }
scope:
  - add/scripts/add.py
  - tests/engine/test_gate_verb.py
---
## CARD
goal: a gate is recorded only when the evidence entitles it, and a quick task costs one engine call
gives: gate · its three refusals · run's own stamp (F3) · done --cmd as the quick lane
scope: add/scripts/add.py · tests/engine/test_gate_verb.py
beat: done · next: e14 `checks --sync`, or e8 `doctor`

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
contract:
  `gate(root, cid, verdict, by, authority=None, reason=None) -> (ok, note)` ·
  `orphans(root) -> [cid]` · `latest_receipt(root, cid) -> (receipt, cid)` ·
  `placeholders_in(node) -> [line]` · `quick(root, slug, title, cmd, by, cwd, depth) -> (ok, note)`
strategy:
  `gate` composes what earlier waves already built and adds no new machinery: e7's `fresh` for
  refusal 1, e12's `unbound` for refusal 2, e5's `brief` for the A16 hash, e6's `render_card` and
  e4's `done` for the transition. Every refusal returns `(False, note)` where the note's last line
  is a runnable command — refusing is not raising, and it never stops a human writing the stamp
  themselves with their own authority (law 3).
  `run` changes in two ways for F3: it records the ID NAMES the node cites (a count cannot be
  bound to anything) plus every failure, and it appends its own run stamp so the receipt is
  reachable from the task.
  Failure handling: a missing receipt, an unknown verdict and an unauthored node are all refusals
  with named fixes, never exceptions. Rollback: git.
  **The ⚠ resolved before BUILD, with a measurement.** `test_gate_on_live_bundle_history` ran M2
  against this project's own eleven gates: it would have refused **8 — exactly the 8 tasks F2
  found labelled-but-not-proven — and zero of the 7 well-bound M1 tasks.** The refusal fires on
  the defect and nothing else, so no `--covers-unverified` flag is needed: `RISK-ACCEPTED` with a
  recorded reason is a better degradation because the reason lands in the stamp.
scope: add/scripts/add.py · tests/engine/test_gate_verb.py
floor: validator CONFORMS on `.add/`; every earlier task's checks stay green
least-sure: rules — M2's strictness. RESOLVED by the measurement above, before building against it.

## CHECKS
- test_gate_refuses_stale_receipt · covers: M1, R:STALEGATE · a verdict over changed code is evidence of nothing
- test_no_scope_makes_freshness_not_applicable · covers: M1 · a node declaring no `scope:` has nothing to be stale about
- test_card_scope_without_frontmatter_scope_is_refused · covers: M1, R:STALEGATE · the hole that gated e13 itself without a freshness check
- test_declared_scope_without_a_digest_is_still_refused · covers: M1, R:STALEGATE · the hole the fix above could have opened
- test_template_placeholders_are_refused_by_name · covers: M2, M4 · an unauthored node refuses with the reason, not with a confusing one
- test_quick_task_declares_no_musts · covers: M6 · a quick task's evidence is its exit code, not a covers-bound suite
- test_gate_accepts_a_fresh_receipt · covers: M1, M3 · the happy path still works, or the refusal is just a wall
- test_gate_refuses_unproven_must · covers: M2, R:UNPROVEN · this is e12's M3, finally landing somewhere
- test_gate_refusal_names_the_unproven_rules · covers: M2 · naming WHICH rules is the difference between a report and a complaint
- test_gate_counts_a_failing_check_as_unproven · covers: M2 · a check that RAN and FAILED proves nothing (e12's rule, at the gate)
- test_gate_records_at_computed_authority · covers: M3 · A17's floor is computed, never taken from the caller's claim
- test_gate_stamps_the_brief_hash · covers: M3 · A16: these instructions produced this code, which earned this gate
- test_gate_pass_transitions_to_done · covers: M3 · a PASS that leaves the node in `build` is a stamp nobody acted on
- test_risk_accepted_records_the_risk · covers: M3 · RISK-ACCEPTED is a verdict with a reason, not a softer PASS
- test_risk_accepted_requires_a_reason · covers: M3, R:SILENTREFUSE · an unexplained RISK-ACCEPTED is a PASS in disguise
- test_hard_stop_does_not_transition · covers: M3 · a HARD-STOP is recorded and the node stays where it is
- test_gate_refusal_names_the_fix · covers: M4, R:SILENTREFUSE · every refusal ends in a command that would resolve it
- test_unknown_verdict_is_refused · covers: M4 · the verdict vocabulary is closed, and the refusal lists it
- test_run_appends_its_own_stamp · covers: M5 · F3's fix. A receipt nothing points at is unreachable evidence
- test_orphan_receipts_are_reported · covers: M5, R:ORPHAN · an unreachable receipt is a finding, not a silent file
- test_no_orphan_receipts_on_live_bundle · covers: M5, R:ORPHAN · this repo's own 8 orphans, reported rather than asserted away
- test_quick_lane_is_one_engine_call · covers: M6 · §3d's quick lane: new + freeze + run + gate in ONE call
- test_quick_lane_refuses_above_quick · covers: M6, R:BYPASS · a one-call lane that works at `deep` bypasses every control
- test_quick_lane_refuses_a_failing_command · covers: M6 · one call still means real evidence: a red command earns no gate
- test_gate_on_live_bundle_history · covers: M2 · would a strict M2 have refused this project's own gates?
red-first: every check above MUST fail for the right reason before BUILD.
<!-- Compiled from tests/engine/test_gate_verb.py on 2026-07-30, not authored beside it. The
     node opened with 12 hand-written lines while the suite grew to 25; the 13 additions were
     all found DURING the build, which is exactly why an authored CHECKS section drifts. This
     is e14's mechanism applied by hand once, and it is the argument for e14. -->

> **CORRECTED AFTER THIS GATE — 2026-07-30 (F8).** `placeholders_in` refused e8's fully authored
> node because its M5 named the path shape `<slug>.d/runs/` inside backticks. The oracle could not
> tell a template token from prose about a path. Fixed by excluding backticked spans, verified safe
> against both `BODIES` templates first (no placeholder in either is backticked). Two checks were
> added to `tests/engine/test_gate_verb.py` after this node was gated —
> `test_a_backticked_path_pattern_is_not_a_placeholder` and `test_a_real_placeholder_is_still_caught`
> — so the CHECKS section below lists fewer than the suite now contains. `checks --sync` REFUSES to
> reconcile that, correctly: this node carries a gate stamp (§3.6, R:SILENTFIX). Nothing above is
> edited; this is the record.

## EVIDENCE
receipt: /tasks/build-gate-verb.d/runs/2.md — 25/25 green · kind test-ids · freshness content ·
  red-first proven by runs/1.md (19/20 fail on absent `gate`/`orphans`/`quick`; `test_run_appends_
  its_own_stamp` failed on an AssertionError, which is F3 failing for exactly the right reason)
not-a-red: `test_gate_on_live_bundle_history` passed in the red run. It composes only existing
  functions because it is a MEASUREMENT, not a behaviour check — recorded as such rather than
  counted as a red. Its number is what resolved this task's ⚠
floor: validator CONFORMS on `.add/`; full suite 161 green
first-of-its-kind: the first gate in this project's history recorded BY THE GATE VERB rather than
  by hand-appending a stamp through the private `_transition`. All eleven before it were hand-made
budget: **OVER — 192 lines against 140 allocated (+52, +37%).** The overrun is the three refusals
  the build discovered were needed and the node did not anticipate: CARD/frontmatter scope drift,
  template placeholders, and the no-scope not-applicable case. Engine 1,448/2,400 · A3 invariant:
  1,448 + 560 (e8 200 + e9 80 + e10 80 + e11 80 + e14 90 + e15 30) = **2,008 / 2,400 — slack 392**
scope-check: match — `add/scripts/add.py` and `tests/engine/test_gate_verb.py` only
gate: PASS — human:tindang, 2026-07-30, recorded by `add gate`
> **Recorded, not rewritten (§3.6): the FIRST gate stamp on this node was taken with freshness
> silently skipped.** `new` was called without `scope=`, so the frontmatter had no `scope:` key
> while the CARD read `scope: add/scripts/add.py · tests/engine/test_gate_verb.py`. Both
> `scope_digest` and A17's sensitive-path floor read frontmatter, so the receipt degraded to
> `mtime` and the gate printed `freshness: n/a`. The verb built to refuse an unverified gate
> recorded its own that way, and only reading its output caught it — the suite could not, because
> no test had a node whose CARD and frontmatter disagreed about scope.
> `sensitivity: security` still floored it at `human`, so the authority was right by luck, not by
> mechanism. Fixed with `test_card_scope_without_frontmatter_scope_is_refused`; the frontmatter now
> declares the scope; a second receipt and a second gate stamp follow, and the first stamp stays.
> The CHECKS section was also 12 authored lines against a suite that had grown to 25 — corrected by
> COMPILING it from the suite, which is e14's mechanism applied by hand once, and the argument for e14.

## LESSONS
- **The verb that refuses unverified gates recorded its own gate unverified.** Not through a logic
  error — through a missing frontmatter key that made every check vacuously pass. `scope:` absent
  meant nothing to hash, nothing to match A17 against, and a cheerful `freshness: n/a`. The lesson
  is not "add the key": it is that **a control which degrades to not-applicable when its input is
  absent will eventually be absent.** Every such degradation needs a check that the input was
  there at all. -> add learn quality
- **A measurement resolved a design question that argument could not.** The ⚠ asked whether a hard
  refusal on unproven Musts was affordable. Running it against this project's own history answered
  in one number: 8 refusals, all of them F2's, none of them a false positive. The rule got stricter
  because the evidence permitted it, not because strictness sounds rigorous. -> add learn method
- **An authored CHECKS section drifted by 13 lines inside a single build.** The node opened with 12
  checks; the suite ended at 25, and every addition came from something the build discovered. No
  amount of care at authoring time closes that gap, because the knowledge does not exist yet.
  Compilation is the only fix, which is what e14 is for. -> add learn quality
- **`run` writing a receipt nothing pointed at hid for six tasks because I supplied the missing
  stamp by hand every time.** A workaround applied consistently is indistinguishable from a working
  feature, right up to the moment someone stops applying it. -> add learn system
