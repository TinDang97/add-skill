---
type: Task
title: a gate cannot pass over a receipt whose command failed
goal: a receipt that records a failed run cannot entitle a PASS, in any lane
status: direction
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
verified: []
---
## CARD
goal: a receipt that records a failed run cannot entitle a PASS, in any lane
gives: a sixth refusal in `gate`, keyed on the receipt's own `exit` field
scope: add/scripts/add.py · tests/engine/test_red_command.py
beat: direction · next: add freeze refuse-red-command

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
- <compiled at BUILD — see F11 before running `checks --sync` against the whole suite>
red-first: every check MUST fail first.

## EVIDENCE
receipt: <runs/<n>.md>
gate: <PASS | RISK-ACCEPTED | HARD-STOP>

## LESSONS
- <lesson> -> add learn <lens>
