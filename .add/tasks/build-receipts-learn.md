---
type: Task
title: run · learn — receipts, and the content-addressed freshness A22 owes
goal: a receipt proves a specific computation over a specific scope, and survives a fresh checkout
status: direction
depth: standard
kind: feature
sensitivity: security
milestone: /milestones/engine-core.md
scope:
  - add/scripts/add.py
  - tests/engine/test_receipts_learn.py
depends_on:
  - /tasks/build-node-verbs.md
  - /tasks/compile-graph.md
needs:
  - /tasks/build-node-verbs.md#gives
  - /tasks/compile-graph.md#gives
gives:
  - "run(root, cid, command) -> a Run node recording exit code, test IDs and the scope digest"
  - "scope_digest(root, scope) -> git blob hashes over the task's `scope:` — A22's content-addressed predicate"
  - "fresh(receipt, root) -> whether a receipt still describes the current tree"
  - "learn(root, lens, lesson) -> a lesson appended to a spec's Deltas"
budget: 240 lines wc -l of growth (amendment A1/A3)
generated: { by: add/3.0.0, at: 2026-07-29 }
verified: []
---
## CARD
goal: a receipt proves a specific computation over a specific scope, and survives a fresh checkout
gives: run · scope_digest · fresh · learn
scope: add/scripts/add.py · its red suite
beat: direction · next: add freeze build-receipts-learn

## RULES
<must>
- M1 freshness is **content-addressed**: a receipt records `scope_digest` as git blob hashes over the task's `scope:`. A receipt is fresh iff those hashes still match. **This is the A22 debt M1 has carried since M0** — the kill-test proved mtime worthless across a checkout
- M2 a receipt survives `git worktree add` — the exact scenario that killed the mtime predicate. This is the acceptance test, run against a real worktree, not a simulation
- M3 `run` RECORDS a computation; it never executes one on the engine's authority. The caller runs the command; the engine notarises the result (specs/system — records but never executes)
- M4 `learn` appends to a spec's `## Deltas` with the evidence that caused it. A lesson with no evidence is an opinion and is refused
</must>
<reject>
- R:MTIME2 any freshness predicate that consults a file timestamp -> "MTIME2"
- R:EXECUTE the engine running a build or test command itself -> "EXECUTE"
- R:OPINION a learn entry with no evidence reference -> "OPINION"
</reject>

## PLAN
contract: <published at freeze>
strategy: <published at freeze>
scope: add/scripts/add.py · tests/engine/
floor: validator exits 0 on `.add/`; every earlier task's checks stay green

## CHECKS
- test_scope_digest_is_git_blobs · covers: M1 · the digest matches `git hash-object` exactly
- test_receipt_survives_worktree · covers: M1, M2, R:MTIME2 · a receipt stays fresh across `git worktree add` — the M0 kill-test, inverted
- test_edited_scope_makes_receipt_stale · covers: M1 · changing a scoped file invalidates the receipt
- test_unrelated_edit_keeps_receipt_fresh · covers: M1 · a file outside `scope:` does not invalidate it
- test_run_does_not_execute · covers: M3, R:EXECUTE · the engine never spawns the command
- test_learn_appends_to_deltas · covers: M4 · the lesson lands in the named spec
- test_learn_without_evidence_refused · covers: M4, R:OPINION · an unevidenced lesson is rejected with a reason
red-first: every check above MUST fail for the right reason before BUILD.

## EVIDENCE
receipt: <runs/<n>.md>
gate: <PASS | RISK-ACCEPTED | HARD-STOP>
budget: <growth vs allocation · A3 invariant>
scope-check: <files touched vs `scope:`>

## LESSONS
- <lesson> -> add learn <domain|system|experience|quality|method>
