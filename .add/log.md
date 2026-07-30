# log

<!-- COMPILED BODY (A20) — rendered from node `verified[]` stamps and `generated.at`.
     Do not append here; a line with no stamp behind it cannot exist (define-log-rotation M1).
     Newest first, grouped under ISO date headings (OKF §9, A10). Humans write in `## Notes` only. -->

<!-- ROTATED (A4): M0's entries folded into milestones/format-standard.md#close at the M0 close
     and are no longer rendered here. Nothing was deleted — a rendered journal is truncated by
     changing what it renders, not by editing it. What follows is M1 only. -->

## 2026-07-30

- human:tindang · tasks/resolve-covers-grammar · gate PASS by `add gate` — F1 CLOSED. Bundle at **0 info, 0 error** for the first time
- human:tindang · FORMAT.md §6.1 · DECISION widen — the grammar is now stated ONCE in a fenced `covers-grammar` block; three oracles held to it by string equality
- claude/opus-5 · milestones/engine-core · F1 was MISDIAGNOSED: 4 of its 7 symptoms were an unanchored validator regex reading PLAN prose; the other 3 were §6.1 stating no grammar at all
- human:tindang · scripts/validate_bundle.py · merged the subagent's fix at `human` authority (A17, sensitive path) — `covers:` now anchored to the CHECKS section
- claude/opus-5 · tasks/resolve-covers-grammar · L-E FIRST TRIAL — executed by a subagent in an isolated worktree from an 11,458 B compiled brief; 123,069 tokens, 53 tool calls, 12.5 min. Every constraint held; the human decision correctly refused
- human:tindang · tasks/build-gate-verb · gate PASS — recorded BY `add gate`: freshness fresh, brief sha256:7e7013b0, receipt 2. The first gate in this project not hand-appended
- claude/opus-5 · tasks/build-gate-verb · CORRECTION — the first gate stamp was taken with freshness silently skipped: `new` ran without `scope=`, so frontmatter had no `scope:` while the CARD claimed one. Both stamps kept (§3.6)
- process:run · tasks/build-gate-verb · receipt 2 — 25/25 pass, kind test-ids, freshness content, 25/25 cited IDs bound
- claude/opus-5 · tasks/build-gate-verb · CHECKS recompiled from the suite — 12 authored lines against a suite that reached 25; every addition was found during the build
- claude/opus-5 · add/scripts/add.py · F3 FIXED — `run` now records the cited ID names plus every failure, returns its digest, and appends its own stamp
- claude/opus-5 · tasks/build-gate-verb · ⚠ resolved BEFORE build by measurement — a strict M2 would have refused 8 of this project's gates, all of them F2's, and none of the 7 well-bound M1 tasks
- process:run · tasks/build-gate-verb · receipt 1 — 19/20 fail on absent `gate`/`orphans`/`quick`; the red-first record
- claude/opus-5 · tasks/build-gate-verb · opened and frozen — wave 3b, budget 140 lines wc -l
- claude/opus-5 · milestones/engine-core · amended A4 — three tasks added from a hand-work audit: e13 gate (140) · e14 checks --sync (90) · e15 covers grammar (30). Invariant 1956/2400, slack 444
- claude/opus-5 · tasks/build-gate-verb, compile-checks-from-suite, resolve-covers-grammar · opened BY THE ENGINE — 15 M1 tasks, DAG resolves, 52 nodes / 156 edges / 0 cycles
- claude/opus-5 · milestones/engine-core · F5 recorded — `new` never substituted `{slug}`; every node it created carries an unrunnable `next:` hint. Assigned to e9, which already declares R:FAKEHINT
- claude/opus-5 · milestones/engine-core · measured: 8 of 18 receipts unreachable from any stamp (44% of evidence) · 118 of 131 tests already carry covers: · all 11 gates so far hand-appended through a private function
- claude/opus-5 · milestones/engine-core · wave 3 CLOSED — e5, e7, e12 gated PASS · 136 checks · engine 1256/2400, slack 704
- human:tindang · tasks/build-brief-compiler · gate PASS — first measured brief costs: mean 13,658 B (~3.4k tok), max 19,221 B, 0 over budget
- process:run · tasks/build-brief-compiler · receipt 3 — 23/23 pass, kind test-ids, freshness content. Receipt 2 went STALE by digest when the parser was fixed (A22 working)
- claude/opus-5 · add/scripts/add.py · `_open_quote` — the quote-COUNT fix had swallowed budget/generated/verified across 25 nodes with 134 green and CONFORMS; caught by `done` refusing a transition it could not entitle
- claude/opus-5 · milestones/engine-core · F4 recorded — three silent e1 parser defects; the missing oracle was read fidelity, now closed by `test_live_bundle_keys_all_parse`
- claude/opus-5 · add/scripts/add.py · fixed a silent e1 defect live since e2: a wrapped quoted list item was truncated and kept its opening quote — found by RENDERING a `gives:` into a brief
- claude/opus-5 · add/scripts/add.py · fixed mangled ref ids — `#gives` compiled to `#gi`; no agent could resolve a brief's refs back
- process:run · tasks/build-brief-compiler · receipt 1 — 19/19 fail on absent `brief`, `0/19 reported`: the red-first record
- claude/opus-5 · tasks/build-brief-compiler · units resolved before BUILD — FORMAT §7.2 says bytes, PROPOSAL §3d says tokens; bytes enforced, tokens printed at a DECLARED 4 B/tok
- claude/opus-5 · tasks/build-brief-compiler · CHECKS extended before freeze — M5/M6 had no check at all; 7 → 21
- claude/opus-5 · tasks/build-brief-compiler · opened and frozen — wave 3, budget 267 lines wc -l
- claude/opus-5 · milestones/engine-core · F3 recorded — `run` writes a receipt but never appends the stamp; all six earlier run stamps were hand-written. Assigned to e8
- claude/opus-5 · tasks/build-evidence-binding · run stamp appended BY HAND (F3); CARD `next:` corrected by hand — `render_card` repairs only `beat:`
- human:tindang · tasks/build-evidence-binding · gate PASS — stamped by the engine at authority `human` (A17: sensitivity security)
- claude/opus-5 · milestones/engine-core · F2 recorded — 67/133 rules proven; 65 claimed by 61 check IDs that do not exist, across 9 M0 tasks. Recorded, nothing reopened
- claude/opus-5 · tasks/build-evidence-binding · CHECKS corrected BEFORE the gate — one fictional ID in five, replaced by the 10 real ones
- process:run · tasks/build-evidence-binding · receipt 1 — 10/10 pass, **kind test-ids, ids 10/10 reported** — the first receipt to earn A24's top rung
- claude/opus-5 · milestones/engine-core · A24 risk ANSWERED at e12; A22 risk RETIRED at e7
- human:tindang · tasks/build-receipts-learn · gate PASS — the M0 kill-test run in reverse: worktree rewrote every mtime, receipt still FRESH
- process:pytest · tasks/build-receipts-learn · receipt 1 — 14/14 pass, A22 implemented, not merely specified
- claude/opus-5 · add/scripts/add.py · fixed a dishonest receipt: `kind` was derived from the scope digest, so a bare command claimed `test-ids` with no IDs
- claude/opus-5 · tasks/build-receipts-learn · M3 corrected before BUILD — "run never executes" contradicted specs/system; the prohibition is on the engine's own initiative
- claude/opus-5 · tasks/build-receipts-learn · opened — wave 3, budget 240 lines wc -l

## 2026-07-29

- claude/opus-5 · milestones/engine-core · seven remaining M1 task nodes created BY THE ENGINE; the DAG resolves with no unresolved edges
- claude/opus-5 · milestones/engine-core · F1 recorded — FORMAT §6.1 says `R:<CODE>`, the validator encodes `R:[A-Z_]+`; left open, not fixed inline
- claude/opus-5 · tasks/port-okf-parse, tasks/build-orient · CARD drift repaired by `render_card` — one line each
- human:tindang · tasks/build-orient · gate PASS — stamped by the engine; all three A3-restored flags working on the live bundle
- process:pytest · tasks/build-orient · receipt 2 — 17/17 pass, kind test-ids, freshness content, red_first proven
- process:pytest · tasks/build-orient · receipt 1 — 15/15 fail on absent `status`, the red-first record
- claude/opus-5 · tasks/build-orient · opened — wave 2, budget 407 lines wc -l
- human:tindang · tasks/build-node-verbs · gate PASS — stamped BY THE ENGINE; first transition ADD 3.0 wrote against its own bundle
- process:pytest · tasks/build-node-verbs · receipt 2 — 15/15 pass, kind test-ids, freshness content, red_first proven
- process:pytest · tasks/build-node-verbs · receipt 1 — 14/14 fail on absent `new`, the red-first record
- claude/opus-5 · add/scripts/add.py · fixed a silent e1 defect: append_item lost every stamp appended to an inline empty list
- claude/opus-5 · tasks/build-node-verbs · opened — wave 2, budget 320 lines wc -l
- human:tindang · milestones/engine-core · amended A3 — restored --locate/--graph/--since into e6; invariant restated as consumed + remaining ≤ 2400
- human:tindang · tasks/build-init-profiles · gate PASS — init's output accepted by the M0 oracle at 0 errors, unedited
- process:pytest · tasks/build-init-profiles · receipt 2 — 8/8 pass, kind test-ids, freshness content, red_first proven
- process:pytest · tasks/build-init-profiles · receipt 1 — 8/8 fail on absent `init`, the red-first record
- claude/opus-5 · tasks/build-init-profiles · opened — wave 2, budget 213 lines wc -l
- human:tindang · milestones/engine-core · amended A2 — A1's falsifier was a ratio between two estimates; restated as one measurable
- human:tindang · tasks/compile-graph · gate PASS — engine and validator independently agree: 81 edges over 27 nodes
- process:pytest · tasks/compile-graph · receipt 2 — 16/16 pass, kind test-ids, freshness content, red_first proven
- process:pytest · tasks/compile-graph · receipt 1 — 16/16 fail on absent `scan`, the red-first record
- claude/opus-5 · tasks/compile-graph · opened — wave 1 task 2, budget 347 lines wc -l
- human:tindang · milestones/engine-core · amended A1 — line budget rebased into `wc -l`; 660 code lines of surface pre-booked as cuts; reserve 8 lines
- human:tindang · tasks/port-okf-parse · gate PASS — 23 live nodes round-trip byte-identically
- process:pytest · tasks/port-okf-parse · receipt 2 — 15/15 pass, kind test-ids, freshness content, red_first proven
- process:pytest · tasks/port-okf-parse · receipt 1 — collection failed, module absent: the red-first record
- claude/opus-5 · milestones/engine-core · opened — M1 seeded: 12 tasks, 5 waves, per-task line budgets

## Notes

<!-- HUMAN-OWNED (A20) — preserved verbatim across every recompile. The engine never
     rewrites, reorders, or summarises anything below this heading. -->
