---
type: Task
title: test IDs carry their file — a failing check cannot be recorded as passed
goal: every check ID in a receipt names exactly one test, so evidence cannot be masked
status: done
depth: standard
kind: fix
sensitivity: security
milestone: /milestones/engine-core.md
scope:
  - add/scripts/add.py
  - tests/engine/test_evidence_ids.py
depends_on:
  - /tasks/build-evidence-binding.md
  - /tasks/compile-checks-from-suite.md
needs:
  - /tasks/build-evidence-binding.md#gives
  - /tasks/compile-checks-from-suite.md#gives
gives:
  - "extract_ids keys by `classname::name`, so two same-named tests are two IDs"
  - "resolve_check(cite, reported) -> pass | fail | ambiguous | absent — the reader-side rule that lets a bare citation bind without rewriting it"
  - "checks_of keys by the same grammar, stated once and shared"
  - "a skipped test is recorded as skipped, never as passed"
budget: 60 lines wc -l of growth (A3 — from e8's 5-line underrun and the 344-line slack)
generated: { by: add/3.0.0, at: 2026-07-30 }
verified:
  - { by: "claude/opus-5", at: 2026-07-30, act: freeze, authority: human }
  - { by: "human:tindang", at: 2026-07-30, act: freeze, authority: human, note: "REFREEZE — M6/R:SKIP folded in (F12), M4 decided, gives: published" }
  - { by: "process:run", at: 2026-07-30, act: run, authority: process, outcome: FAIL, receipt: /tasks/repair-evidence-ids.d/runs/1.md }
  - { by: "process:run", at: 2026-07-30, act: run, authority: process, outcome: PASS, receipt: /tasks/repair-evidence-ids.d/runs/2.md }
  - { by: "process:run", at: 2026-07-30, act: run, authority: process, outcome: PASS, receipt: /tasks/repair-evidence-ids.d/runs/3.md }
  - { by: "human:tindang", at: 2026-08-05, act: gate, authority: human, outcome: PASS, receipt: /tasks/repair-evidence-ids.d/runs/3.md, brief: "sha256:0ddb4080d5deea29" }
---
## CARD
goal: every check ID in a receipt names exactly one test, so evidence cannot be masked
gives: `classname::name` IDs in extract_ids and checks_of · a decision on existing receipts · a check that a collision cannot pass
scope: add/scripts/add.py · tests/engine/test_evidence_ids.py
beat: done · next: add freeze repair-evidence-ids

## RULES
<must>
- M1 a check ID is `classname::name`, taken from junit's `classname` attribute — which was in the
     data all along and thrown away. Two tests sharing a bare name in different files must produce
     two IDs, and `extract_ids` must never let one overwrite the other
- M2 a junit report containing one FAILING and one PASSING test of the same bare name records the
     failure. This is F7's exact demonstration and it is the check the whole task exists for
- M3 `checks_of` (e14) carries the same defect and is fixed in the same shape, because `doctor`'s F2
     check and `gate`'s binding both read it. One fix, two call sites, one ID grammar — a second
     grammar here would be R:DRIFT again (F1's lesson, one level down)
- M4 the migration is DECIDED and recorded, not performed silently. Every existing receipt holds
     bare-name IDs; changing the shape means a stored ID no longer matches what a re-run reports.
     Whether old receipts are left as-is, re-taken, or read through a compatibility rule is a human
     decision with a reason (A17 — `add/scripts/add.py` is a sensitive path)
- M5 no gated node's `covers:` citations are rewritten to the new shape. A citation names a TEST, and
     `M1 · covers: test_foo` stays legible; if the binding needs the file, the resolution is in the
     reader, not in 133 rewritten claims across nine human-gated nodes (§3.6)
- M6 a SKIPPED test is recorded as `skip`, never as `pass`, and a skip proves nothing. Folded in at
     the refreeze (F12): `extract_ids` tested only for `failure`/`error`, so `<skipped/>` fell through
     to the pass branch — F7's sentence with one word changed, in the same six lines this task
     rewrites. Folding it here is not scope creep but its opposite: fixing it later would be a
     second migration of the same ID semantics, behind a gate this task is about to earn
</must>
<reject>
- R:MASK a receipt in which a failing check is recorded as passing -> "MASK"
- R:DRIFT two ID grammars for one format -> "DRIFT"
- R:SWEEP rewriting citations inside gated nodes to satisfy a new ID shape -> "SWEEP"
- R:PHANTOM a rule proven by a check that did not run -> "PHANTOM"
</reject>
<after>
- `gate` can no longer be entitled by a check that failed, which is what A24's ladder assumed all along
- the 211/212 discrepancy that revealed F7 becomes impossible to reproduce
</after>
⚠ that `classname::name` is the right ID shape for a format that does not know pytest exists. junit's
  `classname` is emitted by every runner the format supports at v1.0, but "supported at v1.0" is one
  runner. If a second runner spells it differently, the ID becomes runner-specific and A24's kind
  ladder has a portability hole one rung from the top — if wrong, the ID needs a normalising rule and
  this task grows one.

## PLAN
contract: `extract_ids` and `checks_of` both key by `qualify(classname_or_path, name)` -> `a.b.c::name`,
  one grammar stated once. `resolve_check(cite, reported)` is the reader: an exact hit wins; else a
  suffix match on `::<cite>`; exactly one hit resolves to its outcome; two or more resolve to
  `ambiguous`; none resolves to `absent`. `bind` proves a rule only on `pass`.
strategy: reader-side resolution, not a sweep — M5 forbids rewriting citations, and the measurement
  below says a sweep would be enormous effort to fix two lines. Old bare-name receipts keep binding
  through the exact-hit arm; new qualified receipts bind through the suffix arm.
scope: add/scripts/add.py · tests/engine/test_evidence_ids.py
floor: validator CONFORMS on `.add/`; the 212-check suite stays green; no gated node edited
least-sure: ~~rules — M4~~ **RESOLVED at the refreeze by measurement, before BUILD.** The migration
  question was sized rather than argued: the suite holds **211 distinct bare names across 212 tests**,
  the bundle holds **394 citations**, and **exactly one** bare name is ambiguous
  (`test_sync_is_idempotent`, in `test_checks_compiler.py` and `test_doctor.py` — the collision F7
  named). **2 of 394 citations** are affected. The fear in the original note — that "no answer makes
  all of them retroactively unambiguous" — was right in principle and wrong in magnitude by two
  orders of magnitude. Now least-sure: the ⚠ below, which measurement cannot settle.

## DECISION
**M4 · the migration (human:tindang, 2026-07-30) — LEAVE, and resolve in the reader.**

Decided with the numbers in hand, not from the shape of the problem:

| measured before deciding | value |
|---|---:|
| receipts holding `kind: test-ids` | 23 of 27 |
| distinct bare test names / tests in the suite | 211 / 212 |
| bare names that collide | **1** |
| `covers:` citations in the bundle | 394 |
| citations that become ambiguous | **2** |

Existing receipts are **not re-taken and not invalidated**. They keep their bare-name IDs and keep
binding through `resolve_check`'s exact-hit arm; receipts written from now on carry
`classname::name` and bind through the suffix arm. A citation matching two IDs resolves to
`ambiguous` and **proves nothing** — which is the correct outcome for the two affected citations,
because those are exactly the claims F7 showed were never sound.

**Why not the alternatives.** Re-taking the 23 receipts would manufacture fresh evidence for gates
already recorded, so the receipt on disk would stop being the one the gate was taken against —
R:REPAIRAWAY's shape. Refusing to bind old-shape receipts would invalidate 23 receipts and 11
gates to fix 2 citations, reopening closed work at a ratio of eleven to one.

**What this decision costs, stated:** the bundle holds two ID grammars for the rest of its life.
That is a real cost and it is bounded — the reader states the rule once, and no node has to know.

## CHECKS
- test_a_masked_failure_is_recorded · covers: M2, R:MASK · F7's exact demonstration — the failure must survive extraction
- test_a_skip_proves_no_rule · covers: M6, R:PHANTOM · bind refuses to prove a rule from a skipped check
- test_a_skipped_test_is_not_a_pass · covers: M6, R:PHANTOM · F12's demonstration — `<skipped/>` must not read as pass
- test_ambiguous_citation_proves_nothing · covers: M1, R:MASK · a bare citation matching two IDs resolves to ambiguous, never pass
- test_bare_citation_still_binds · covers: M4, M5 · an old bare-name receipt keeps binding through the exact-hit arm
- test_checks_of_keys_by_file_too · covers: M3 · e14's extractor carries the same defect, and loses a real test to it
- test_migration_decision_is_recorded · covers: M4 · the node carries the reason, not just the outcome
- test_no_gated_citation_rewritten · covers: M5, R:SWEEP · gated M0 nodes keep their citations byte-identical
- test_one_id_grammar · covers: M3, R:DRIFT · both call sites form an ID through the same function
- test_two_tests_one_name_are_two_ids · covers: M1 · junit's classname distinguishes two same-named tests in different files
red-first: every check above MUST fail for the right reason before BUILD.
<!-- COMPILED from the suite (e14). Do not author here: a citation edited by hand
     cannot be distinguished from one that was never true (F2). -->

## EVIDENCE
receipt: runs/2.md — 222/222 test-ids, exit 0, freshness content. Red record is runs/1.md
  (7 failed, 3 passed, `3/10 reported`). Three of the ten could not go red and are labelled below.
gate: PASS — human:tindang, 2026-07-30, recorded by `add gate` at authority `human` (A17).
  Receipt `runs/3.md`, brief `sha256:0ddb4080d5deea29` — and that hash is F16's own defect
  demonstrating itself: `gate` recomputes the brief with default arguments, so the stamp names
  an artifact no agent was ever given. Recorded here rather than quietly, because the first
  gate taken after finding a defect is the cheapest place to show it is real.
budget: **1822 → 1896 = 74 lines against 60 allocated — 14 OVER.** The overrun is `resolve_check`
  and `cite_hits`, which the frozen PLAN did not name: the contract was written as "fix the key
  shape" and the reader-side resolution M5 forces is a second function, not a wider dict. Recorded
  against the A5 invariant, which was already 72 over before this task: **2472 → 2486 / 2400.**
scope-check: two files edited OUTSIDE `scope:` — `tests/engine/test_checks_compiler.py` and
  `tests/engine/test_evidence_binding.py`. Both assert `checks_of`/`extract_ids` key SHAPE, which
  this task changes by contract, so they fail the moment the fix lands. Declared rather than
  quietly absorbed: no assertion was weakened or deleted — six bare-key lookups now resolve through
  the production grammar (`cite_hits`), which makes them stronger, not laxer, because they would
  now also catch a collision. The alternative was a refreeze to widen `scope:`, and a scope whose
  only purpose is to legalise a mechanical consequence of the contract teaches nothing.
red-first: 7 of 10 failed for the right reason (missing `qualify`/`resolve_check`, and a skipped
  test extracted as `pass`). **3 could not fail and are not claimed as red**:
  `test_migration_decision_is_recorded` and `test_no_gated_citation_rewritten` are documentation
  and non-regression guards, and `test_a_skip_proves_no_rule` was already satisfied — `bind`
  proves only on `== "pass"`, so the skip defect was purely extraction-side. Recording them as red
  would have been the easiest lie available in this task.

## LESSONS
- <lesson> -> add learn <domain|system|experience|quality|method>
