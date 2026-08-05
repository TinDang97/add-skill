---
type: Task
title: a gate cannot pass over a receipt whose command failed
goal: a receipt that records a failed run cannot entitle a PASS, in any lane
status: done
depth: standard
kind: fix
sensitivity: security
milestone: /milestones/engine-core.md
scope:
  - add/scripts/add.py
  - tests/engine/test_red_command.py
depends_on:
  - /tasks/build-gate-verb.md
  - /tasks/repair-evidence-ids.md
needs:
  - /tasks/build-evidence-binding.md#gives
gives:
  - "gate refuses PASS while the latest receipt records a non-zero exit"
  - "the refusal names the exit code and the command, so the fix is the run, not the verdict"
  - "a non-PASS verdict may still be recorded over a red receipt — refusing that would trap the node"
budget: 25 lines wc -l of growth (A3)
generated: { by: add/3.0.0, at: 2026-07-30 }
verified:
  - { by: "claude/opus-5", at: 2026-08-05, act: freeze, authority: human }
  - { by: "process:run", at: 2026-08-05, act: run, authority: process, outcome: FAIL, receipt: /tasks/refuse-red-command.d/runs/1.md }
  - { by: "process:run", at: 2026-08-05, act: run, authority: process, outcome: PASS, receipt: /tasks/refuse-red-command.d/runs/2.md }
  - { by: "human:tindang", at: 2026-08-05, act: gate, authority: human, outcome: PASS, receipt: /tasks/refuse-red-command.d/runs/2.md, brief: "sha256:7d12ec34bc67f6a9" }
---
## CARD
goal: a receipt that records a failed run cannot entitle a PASS, in any lane
gives: a sixth refusal in `gate`, keyed on the receipt's own `exit` field
scope: add/scripts/add.py · tests/engine/test_red_command.py
beat: done · next: add gate refuse-red-command

## RULES
<must>
- M1 `gate` refuses `PASS` when the latest receipt records a non-zero `exit`. This is F17: the
     verb's five refusals cover the verdict, the node, the reason, the receipt's existence, its
     freshness, its placeholders and its unbound rules — and never the one field that says
     whether the command succeeded
- M2 the refusal names the exit code and the recorded command, because `gate`'s contract is that
     every refusal says what would make it pass. "re-run it" is not that; "`pytest` exited 1"
     followed by `add run <slug> -- <cmd>` is
- M3 `RISK-ACCEPTED` and `HARD-STOP` stay recordable over a red receipt. A verdict is how a node
     leaves a bad state, so refusing every verdict over a red run would trap the node with no
     legal move — the same trap A13 avoided for freshness. Only `PASS` is refused
- M4 a receipt whose `kind` is not `command-exit` is refused on the same rule. The exit code is
     recorded for every kind (`run` writes it unconditionally), and a `test-ids` receipt with ten
     green IDs and `exit: 1` is the exact shape that made F17 survive — the suite reported pass
     while the process that ran it did not
</must>
<reject>
- R:GREENLIE a PASS recorded while the receipt on disk says the run failed -> "GREENLIE"
- R:TRAP a node with a red receipt and no legal verdict -> "TRAP"
- R:MUTE a refusal that does not name the exit code -> "MUTE"
</reject>
<after>
- L8 holds in the one place it did not: a gate is entitled by what a receipt CONTAINS, and a
  contained refusal stops being readable-past
- `command-exit`, A24's floor kind, becomes load-bearing at the gate instead of decorative
</after>
⚠ that non-zero always means failure. A suite that exits 1 because coverage fell below a
  threshold has still reported its tests truthfully, and a caller who wants that gate has no way
  to say so — this refusal has no escape hatch by design (M3 leaves `RISK-ACCEPTED`, which forces
  a written reason). If that proves too blunt in practice the answer is a recorded reason, never
  a flag that mutes the check; the flag is how R:GREENLIE comes back wearing a permission.

## PLAN
contract: `gate` gains one refusal between the receipt-exists check and the freshness check —
  ordered there because a stale red receipt should report red, which is the more actionable of
  the two facts. Reads `receipt.get("exit")`; refuses only `PASS`; the note carries the exit code
  and `receipt["computation"]`.
strategy: the smallest possible change to one function, no new helper. F17's cost is not
  complexity, it is that nobody looked at the field.
scope: add/scripts/add.py · tests/engine/test_red_command.py
floor: validator CONFORMS on `.add/`; the suite stays green; no gated node edited
least-sure: the ⚠ above — whether a blanket refusal on non-zero is right, or whether the exit
  code needs the same kind-ladder treatment A24 gave evidence. Sized before BUILD: every receipt
  in this bundle records `exit: 0`, so there is no case in-hand where the blunt rule costs
  anything. Deciding it on zero counter-examples is what the ⚠ exists to flag.

## CHECKS
- test_green_ids_cannot_mask_a_red_command · covers: M4, R:GREENLIE · F17's exact shape — every cited ID passes, the command does not. This is why the defect survived: `bind` is…
- test_green_receipt_still_passes · covers: M1 · the refusal must not fire on a healthy run — the non-regression half. A refusal that fires wrongly is more…
- test_hard_stop_survives_a_red_receipt · covers: M3, R:TRAP · HARD-STOP is the honest verdict over a failed run and must be recordable
- test_pass_refused_over_a_red_receipt · covers: M1, R:GREENLIE · a PASS cannot be recorded while the receipt says the run failed
- test_risk_accepted_survives_a_red_receipt · covers: M3, R:TRAP · a verdict is how a node LEAVES a bad state; refusing all of them traps it
- test_the_refusal_names_the_command · covers: M2, R:MUTE · naming the command is what makes the fix the run, not the verdict
- test_the_refusal_names_the_exit_code · covers: M2, R:MUTE · `gate`'s contract is that a refusal says what would make it pass. Asserts the refusal FIRST and the digit in…
- test_the_refusal_precedes_freshness · covers: M1 · a receipt that is BOTH red and stale reports red, the more actionable fact
red-first: every check above MUST fail for the right reason before BUILD.
<!-- COMPILED from the suite (e14). Do not author here: a citation edited by hand
     cannot be distinguished from one that was never true (F2). -->

## EVIDENCE
receipt: runs/2.md — 230/230 test-ids, exit 0, freshness content. Red record is runs/1.md
  (`3/8 reported`, exit 1, 5 failed).
gate: PASS — human:tindang, 2026-08-05, recorded by `add gate` at authority `human` (A17).
  Receipt `runs/2.md`, brief `sha256:7d12ec34bc67f6a9` — which is F16 again: `gate` recomputes
  the brief with default arguments, so this hash names an artifact no agent was handed. Noted
  a second time because a defect that is recorded but keeps happening is not yet fixed.
budget: **1896 → 1921 = 25 lines against 25 allocated — exactly on budget**, the first task in
  this milestone that did not overrun. Cheap because the PLAN was right about the shape: F17's
  cost was never complexity, it was that nobody read the field. The A3 invariant is unchanged
  by this task at **2511/2400** — the 25 were already booked by A6.
scope-check: no file edited outside `scope:`. e16's excursion is not repeated.
red-first: 5 of 8 failed for the right reason — `gate` RECORDED a PASS where it had to refuse,
  which is F17 itself rather than a missing name. **3 could not fail and are not claimed as red**:
  `test_green_receipt_still_passes` and the two R:TRAP guards assert behaviour that was already
  correct and must STAY correct after a new refusal lands. A refusal's non-regression half cannot
  be red without the refusal being wrong.
found-while-building: two defects in the first draft of this fix, both caught by the suite before
  any receipt was taken. (1) `exit` round-trips through the T0 parser as the STRING `'0'`, so
  `code not in (0, None)` refused all 222 existing gates — caught by the one check that exists to
  catch exactly that, `test_green_receipt_still_passes`. This is the case for writing the
  non-regression half of a refusal before the refusal. (2) `computation:` is a top-level key of
  the Run node, not a field inside `receipt:`, so the first draft's refusal named
  `command not recorded` every time — R:MUTE, committed by the very task that forbids it, and
  caught by `test_the_refusal_names_the_command`.
also-found: a weak assertion in my own red suite. `assert "3" in note` PASSED against the
  un-fixed engine, because a brief hash contains digits — the check would have been satisfied by
  a hex digest. Strengthened to assert the refusal fires first, then the digit in a phrase. Same
  class as F18, found the same way: reading the diff rather than the result.

## LESSONS
- <lesson> -> add learn <lens>
