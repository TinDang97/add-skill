---
type: Task
title: D-12 fires — three status flags are withdrawn, not erased
goal: the pre-booked cut is paid in full before the ceiling's unit is questioned
status: done
depth: standard
kind: fix
sensitivity: security
milestone: /milestones/engine-core.md
scope:
  - add/scripts/add.py
  - tests/engine/test_status.py
  - tests/engine/test_cut_flags.py
depends_on:
  - /tasks/build-orient.md
  - /tasks/refuse-red-command.md
needs:
  - /tasks/build-evidence-binding.md#gives
gives:
  - "`--locate`, `--graph` and `status --since` are gone from the engine, with the saving measured"
  - "a retirement record: e6's gated node is untouched and the withdrawal is written elsewhere"
  - "the calibration number D-12's cut order was missing — predicted vs actual"
budget: 0 lines wc -l of growth — this task REMOVES lines; the measurement is the deliverable
generated: { by: add/3.0.0, at: 2026-08-05 }
verified:
  - { by: "claude/opus-5", at: 2026-08-05, act: freeze, authority: human }
  - { by: "process:run", at: 2026-08-05, act: run, authority: process, outcome: FAIL, receipt: /tasks/cut-status-flags.d/runs/1.md }
  - { by: "process:run", at: 2026-08-05, act: run, authority: process, outcome: PASS, receipt: /tasks/cut-status-flags.d/runs/2.md }
  - { by: "process:run", at: 2026-08-05, act: run, authority: process, outcome: PASS, receipt: /tasks/cut-status-flags.d/runs/3.md }
  - { by: "human:tindang", at: 2026-08-05, act: gate, authority: human, outcome: PASS, receipt: /tasks/cut-status-flags.d/runs/3.md, brief: "sha256:37af3ab04e38f376" }
---
## CARD
goal: the pre-booked cut is paid in full before the ceiling's unit is questioned
gives: three flags withdrawn · a retirement record · predicted-vs-actual for D-12
scope: add/scripts/add.py · tests/engine/test_status.py · tests/engine/test_cut_flags.py
beat: done · next: add gate cut-status-flags

## RULES
<must>
- M1 `locate`, `graph_lines` and `since` are removed from the engine, along with `status()`'s
     `locate_term`, `milestone` and `since_date` parameters and the three branches that read
     them. D-12 named this cut order before the overflow arrived; firing it now is the decision
     being honoured, not a new one
- M2 **`build-orient.md` is not edited.** Those three flags are its M1, M3 and M4, and it carries
     a human gate. The rules were TRUE when the gate was taken, and a gate records what was
     accepted rather than what still ships. Editing them to match the cut is R:ERASE, which §3.6
     exists to forbid and which this project has refused four times already
- M3 the checks that proved e6's M1/M3/M4 are removed WITH their reason recorded in this node.
     A check deleted silently is indistinguishable from a check that never existed — F2's whole
     finding — and a cut that shrinks the suite without saying so shrinks the evidence too
- M4 nothing else about `status` changes. The orientation surface, the 20-line budget (A12), the
     CARD-drift check and the frontier hint all behave exactly as before. A cut that quietly
     takes collateral is worse than one that takes too little, because the collateral is
     discovered later and attributed to something else
- M5 the saving is MEASURED and written down against what D-12 predicted. F21 showed A3's
     estimate for these same three flags was wrong by 5–7×; a cut fired on the strength of an
     estimate must leave behind the number that estimate should have been
</must>
<reject>
- R:ERASE editing a gated node so the record matches what shipped later -> "ERASE"
- R:SILENTCUT a feature or a check removed with no record of why -> "SILENTCUT"
- R:COLLATERAL any change to `status`'s remaining behaviour -> "COLLATERAL"
</reject>
<after>
- D-12's first three steps are spent, and what they bought is a measured number rather than a
  pre-booked promise — which is what the residual decision needs in order to be honest
- `doctor --locate` (§4b) loses the function it would have called; it is unbuilt, so this is a
  reduction in planned surface, not a regression
</after>
⚠ that this cut is worth making. If D-15 restates the ceiling in code lines, the crisis these
  lines were cut to relieve disappears, and three working, tested, human-gated UX surfaces will
  have been deleted for nothing — and UX is weakness #5, the one this project exists to fix.
  The counter-argument is the reason the order was chosen: paying the pre-booked price BEFORE
  changing the measuring stick is what keeps the stick change from being R:SELFSERVE. Recorded
  as the known cost of that ordering, decided with both figures visible.

## PLAN
contract: `status(root, all=False, check=False)` — three parameters and three branches lighter.
  `locate`, `graph_lines` and `since` cease to exist. Their four checks in `test_status.py` are
  removed; `test_cut_flags.py` asserts the absence and the survival of everything else.
strategy: delete, measure, record. No refactor rides along — M4 makes collateral a Reject, so
  the diff is expected to be subtractions plus one new test file.
scope: add/scripts/add.py · tests/engine/test_status.py · tests/engine/test_cut_flags.py
floor: validator CONFORMS on `.add/`; the suite stays green minus the four withdrawn checks;
  `build-orient.md` byte-identical
least-sure: the ⚠ above, which no measurement settles because it is a question about ordering
  rather than about size.

## CHECKS
- test_card_drift_survives · covers: M4, R:COLLATERAL · e6's M5 is NOT part of the cut and must still work
- test_gated_node_untouched · covers: M2, R:ERASE · e6 keeps its M1/M3/M4 exactly as the human gate accepted them. The rules were true when gated. A gate records…
- test_status_no_longer_takes_the_three_parameters · covers: M1 · the branches go with the functions, not just the functions
- test_status_stays_within_its_line_budget · covers: M4, R:COLLATERAL · the 20-line orientation budget is unchanged
- test_status_still_orients · covers: M4, R:COLLATERAL · the surface the cut was NOT supposed to touch
- test_the_saving_is_measured_not_estimated · covers: M5 · a cut fired on an estimate must leave behind the number it should have been. F21 found A3's estimate for…
- test_the_withdrawal_is_recorded_somewhere · covers: M3, R:SILENTCUT · a removed feature that leaves no trace is a feature that lied
- test_the_withdrawn_functions_are_gone · covers: M1, R:SILENTCUT · D-12's first three steps, spent
red-first: every check above MUST fail for the right reason before BUILD.
<!-- COMPILED from the suite (e14). Do not author here: a citation edited by hand
     cannot be distinguished from one that was never true (F2). -->

## RETIRED
**Withdrawn 2026-08-05 by D-12, with the reason recorded (M3, R:SILENTCUT).**

Three flags and the four checks that proved them. The features were not defective and the
checks were not wrong — both were spent to buy line budget, which is a different thing and
has to read differently in the record.

| withdrawn | proved | in `build-orient` |
|---|---|---|
| `status --graph <milestone>` | `test_graph_is_per_milestone` | M1, R:UNBOUNDED |
| `status --find <term>` (`locate`) | `test_locate_by_slug_fragment`, `test_locate_by_title_fragment` | M3 |
| `status --since <date>` | `test_since_uses_stamps_not_mtime` | M4, R:MTIME |

**`build-orient.md` is byte-identical and stays that way.** Its M1, M3 and M4 were true when
its human gate was taken, and they still describe what was accepted on that day. A gate is a
record of an acceptance, not a claim about what ships forever; editing those rules so the
record matches today's engine would erase the acceptance rather than supersede it (R:ERASE,
§3.6). Anyone reading e6 in future sees rules with no implementation and should be sent here —
which is what the trace left in `test_status.py` does.

**What was actually lost.** `--since` was the only affordance answering "what has happened
recently", and following AI work is weakness #5 — the weakness this project exists to fix.
`--graph` was the only per-milestone DAG view. `--find` was goal 11 ("slugs easy to look up").
Three UX surfaces, in a project whose named UX weakness is now less covered than before.

**Measured against what D-12 predicted.** The cut order was booked without a number:

| | lines |
|---|---:|
| my estimate before cutting | ~46 |
| **actual, `wc -l` before and after** | **56** |
| A3's estimate for the same three flags (F21) | ~247 |

56, not 46 and not 247. Recorded because D-12's remaining step (folding `learn` into
`doctor --learn`) is still an estimate, and this is the calibration for it.

## EVIDENCE
receipt: runs/3.md — 236/236 test-ids, exit 0, freshness content. Red record is runs/1.md
  (`4/9 reported`, exit 1, 5 failed); runs/2.md was green but left M5 unbound.
gate: <PASS | RISK-ACCEPTED | HARD-STOP>
budget: allocated 0 growth; **actual −56 lines (1921 → 1865)**. The first negative entry in this
  milestone's ledger. The A3 invariant moves with it — see the milestone's A7.
scope-check: no file edited outside `scope:`. `build-orient.md` verified byte-identical against
  HEAD by `test_gated_node_untouched`, which is the check M2 exists for.
red-first: 5 of 9 failed for the right reason — the three functions still existed, `status` still
  took their parameters, and the retirement record was unwritten. **4 could not fail and are not
  claimed as red**: `test_gated_node_untouched` and the three R:COLLATERAL guards assert that
  things stay as they are, and a deletion's guards are green before the deletion by definition.
  For a cut, the non-regression half IS most of the suite.
m5-was-unbound: the FIRST green receipt (runs/2.md) was refused by `gate` — M5 said the saving
  must be measured against D-12's prediction, and I had written the measurement into `## RETIRED`
  while binding no check to it. A rule proven by prose is A15's finding verbatim, committed in
  the task that exists to keep a cut honest. `test_the_saving_is_measured_not_estimated` now
  binds it, and is declared NON-RED: the numbers were already on the page when it was written.
suite-size: 239 → 236 checks. Four fewer, deliberately, with the trace in `test_status.py` and
  the reason under `## RETIRED`. A shrinking suite is normally a smell; this is the case where it
  is the deliverable, which is exactly why it needed saying out loud.

## LESSONS
- <lesson> -> add learn <lens>
