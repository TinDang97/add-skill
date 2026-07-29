---
type: Task
title: Define authority and evidence rules
goal: a headless run has a legal freeze path and no gate can pass on a stale or absent receipt
status: done
depth: standard
kind: docs
sensitivity: security
milestone: /milestones/format-standard.md
depends_on:
  - /tasks/define-task-schema.md
needs:
  - /tasks/define-task-schema.md#gives
gives:
  - "a receipt is fresh iff the git blob digest of its scope: set still matches (A22)"
  - "mtime survives only as a declared fallback outside a git tree; a receipt states which predicate it used"
  - "authority ladder: human > plan > ai-verify > process; sensitivity pins the minimum"
  - "receipt freshness: a receipt is stale if any file in scope: is newer than it"
  - "the engine records receipts; add run -- <cmd> executes, a bare gate never does"
scope:
  - FORMAT.md
generated: { by: claude/opus-5, at: 2026-07-29 }
verified:
  - { by: "human:tindang", at: 2026-07-29, act: freeze, authority: human }
  - { by: "human:tindang", at: 2026-07-29, act: gate, authority: human, outcome: PASS,
      receipt: /tasks/build-worked-example.d/runs/3.md }
    # A17 pinned this to `human`: `scope:` includes FORMAT.md, a sensitive_path. The
    # declared `sensitivity:` was never the binding constraint.
---
## CARD
goal: amendments A1–A3 — who may freeze, and what makes a receipt count
gives: the authority ladder, the freshness rule, the record-never-execute rule
scope: FORMAT.md §3 · FORMAT.md §8
beat: done · gate PASS by human:tindang on receipt 3

## RULES
<must>
- M1 every freeze and gate stamp carries an `authority:` value from the closed ladder
- M2 `sensitivity: security | data | architecture` pins the minimum authority to `human`, unstrikeably
- M3 a milestone `ratified:` stamp pre-approves its member tasks at `plan` authority
- M4 a gate refuses unless a receipt exists AND is newer than every file in the task's `scope:`
- M5 the engine never executes a command string read from a file; `add run -- <cmd>` executes what the caller passes
- M9 freshness is content-addressed: a receipt records the git blob digest of its `scope:` set,
     and a gate refuses on any difference. mtime is a declared fallback, never a silent one (A22)
</must>
<reject>
- R:FORGE a headless run that stamps `human` authority without a human -> "FORGE"
- R:STALE a gate that passes on a receipt older than an in-scope edit -> "STALE"
- R:EXEC a verb that executes a `computation:` string from a node -> "EXEC"
</reject>
<after>
- an agent can run the full loop headless without either blocking or faking a human stamp
- a green receipt from before the last edit cannot earn a gate
</after>
⚠ that mtime is a sound freshness signal across checkouts and worktrees — if wrong:
  freshness needs a content hash of the scope set, which costs a read of every scoped file

## PLAN
contract: the ladder as a closed enum, the freshness predicate, and the execution boundary
strategy: specify in FORMAT §8 beside the Run receipt shape. Design against the two
  failure modes that matter: a forged human stamp (authority is recorded, not asserted)
  and a stale green (freshness is computed, not trusted). Rollback: none needed — these
  are additive keys; a bundle without them reads as `process` authority and no freshness claim.
scope: FORMAT.md §3 (verified stamps) · FORMAT.md §8 (receipts)
floor: none — greenfield format
least-sure: contract — mtime vs content hash for the freshness predicate

## CHECKS
- test_authority_enum · covers: M1 · a stamp without an authority value is an `error` finding
- test_sensitivity_floor · covers: M2, R:FORGE · a `security` task refuses any authority below `human`
- test_ratified_pre_approves · covers: M3 · a member task of a ratified milestone freezes at `plan`
- test_stale_receipt_refused · covers: M4, R:STALE · touching an in-scope file after the receipt makes the gate refuse
- test_no_exec_from_node · covers: M5, R:EXEC · a node carrying a `computation:` string is never executed by `gate`
- test_freshness_is_content · covers: M9 · a receipt records a scope digest and the gate compares digests
- test_fresh_after_checkout · covers: M9 · a receipt survives a fresh worktree checkout that resets every mtime
- test_predicate_is_declared · covers: M9 · a receipt states `freshness: content | mtime`; a gate never guesses
red-first: every check above MUST fail for the right reason before BUILD.

## EVIDENCE
receipt: /tasks/build-worked-example.d/runs/3.md — 18/18, the shared M0 evidence run
gate: PASS — human:tindang, 2026-07-29, authority `human` (A17 floor)
scope-check: FORMAT.md only — inside the declared scope

## LESSONS
- 2.5 carried `gate_mode: ai-plan-verify` in a PLAN header; without a first-class ladder a headless run must either block or forge -> add learn method
