---
type: Task
title: run · learn — receipts, and the content-addressed freshness A22 owes
goal: a receipt proves a specific computation over a specific scope, and survives a fresh checkout
status: done
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
verified:
  - { by: "process:run", at: 2026-07-30, act: run, authority: process, outcome: PASS, receipt: /tasks/build-receipts-learn.d/runs/1.md }
  - { by: "human:tindang", at: 2026-07-30, act: gate, authority: human, outcome: PASS }
---
## CARD
goal: a receipt proves a specific computation over a specific scope, and survives a fresh checkout
gives: run · scope_digest · fresh · learn
scope: add/scripts/add.py · its red suite
beat: done · next: add freeze build-receipts-learn

## RULES
<must>
- M1 freshness is **content-addressed**: a receipt records `scope_digest` as git blob hashes over the task's `scope:`. A receipt is fresh iff those hashes still match. **This is the A22 debt M1 has carried since M0** — the kill-test proved mtime worthless across a checkout
- M2 a receipt survives `git worktree add` — the exact scenario that killed the mtime predicate. This is the acceptance test, run against a real worktree, not a simulation
- M3 `run` executes **the command the agent explicitly supplied** and notarises the result. It
     never runs anything on its own initiative, and a bare `gate` executes nothing
     (specs/system#decisions-that-bind: `add run -- <cmd>` executes the agent's own command).
     The command is bounded by a timeout, and a timeout is a recorded outcome, not a crash
- M4 `learn` appends to a spec's `## Deltas` with the evidence that caused it. A lesson with no evidence is an opinion and is refused
</must>
<reject>
- R:MTIME2 any freshness predicate that consults a file timestamp -> "MTIME2"
- R:INITIATIVE the engine running any command the caller did not supply -> "INITIATIVE"
- R:HANG an unbounded subprocess with no timeout -> "HANG"
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
- test_run_executes_only_what_was_given · covers: M3, R:INITIATIVE · the recorded command is exactly the one supplied
- test_run_times_out_as_an_outcome · covers: M3, R:HANG · a hanging command is recorded as a timeout, not raised
- test_learn_appends_to_deltas · covers: M4 · the lesson lands in the named spec
- test_learn_without_evidence_refused · covers: M4, R:OPINION · an unevidenced lesson is rejected with a reason
red-first: every check above MUST fail for the right reason before BUILD.

## EVIDENCE
receipt: /tasks/build-receipts-learn.d/runs/1.md — written BY `add run`, the verb this task
  built. 14/14 green, exit 0, `freshness: content`, scope digest over both scoped files
gate: PASS — human:tindang, 2026-07-30, stamped by the engine
a22-discharged: **the M0 kill-test, inverted.** `git worktree add` rewrote the checked-out
  file's mtime (…587.011 → …587.055), which is exactly what made every committed receipt read
  stale under the old predicate. The content digest was unchanged, so the receipt stayed FRESH —
  and a real one-byte edit immediately made it STALE. The debt M1 carried since M0 is paid
defect-found: the first receipt `add run` wrote for its own task declared `kind: test-ids`
  while carrying no IDs. The kind had been derived from whether a scope DIGEST existed — but a
  digest answers "is this the same code?" and the kind answers "what does this prove?". Two
  unrelated questions wired to one answer, which is the silent over-claim A24 forbids. Caught by
  reading the artifact, not by the suite. Fixed red-first
spec-correction: this node's M3 originally read "`run` never executes; the caller runs the
  command". `specs/system#decisions-that-bind` says the opposite — `add run -- <cmd>` executes
  the agent's own command; the prohibition is on acting on the engine's OWN initiative. Corrected
  before building, not after
budget: 129 lines against 240 allocated. Engine 941/2400; A3 invariant 1808/2400, slack 592
scope-check: match — `add/scripts/add.py` and `tests/engine/test_receipts_learn.py`
⚠ open: `test-ids` remains unreachable — every receipt this verb writes is `command-exit` with
  `ids: unknown` until `e12` extracts real IDs. The strongest evidence kind A24 defines is
  currently unearnable by the engine

## LESSONS
- **Freshness and evidence are different questions and must never share a variable.** One
  expression decided both, so a scope digest silently promoted a bare command to `test-ids`.
  The bug was invisible in tests because both questions had the same answer in every fixture.
  -> add learn quality
- **Reading the artifact found what the suite could not.** Three defects this session came from
  USING the output — a bounded-but-useless report, a silently dropped stamp, an over-claimed
  receipt. Tests verify that code does what was specified; they are silent when the
  specification itself was wrong. Every verb needs one pass where its real output is read by a
  human before it is gated. -> add learn experience
- **A specification outranks the plan written against it.** M3 was authored contradicting
  `specs/system#decisions-that-bind`. Checking the spec BEFORE building cost one grep; finding
  it after would have cost a gated task built on a false rule. -> add learn method
