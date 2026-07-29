---
type: Task
title: Define the journal, its rotation, and the conformance codes
goal: the journal is compiled from stamps, cannot grow into a context hazard, and conformance never rejects a bundle for style
status: verify
depth: standard
kind: docs
sensitivity: mechanical
milestone: /milestones/format-standard.md
depends_on:
  - /tasks/define-entity-model.md
needs:
  - /tasks/define-entity-model.md#gives
gives:
  - "log.md is COMPILED from node verified[] stamps and generated.at — never appended (A20)"
  - "a trailing `## Notes` section is human-owned and preserved verbatim across recompiles"
  - "log.md rotates at milestone close: whole date groups fold into that milestone's CLOSE"
  - "conformance codes: error = missing_frontmatter|type_empty|edge_out_of_bundle; all else info"
scope:
  - FORMAT.md
generated: { by: claude/opus-5, at: 2026-07-29 }
verified: []
---
## CARD
goal: A4 + A20 — a journal nobody writes by hand, plus the conformance severity table
gives: the compile rule, the rotation rule, the three error codes
scope: FORMAT.md law 5 · §1 (log.md) · §4.1 · §9
beat: verify · next: blocked on the validator (build-worked-example) for its receipt

## RULES
<must>
- M1 every journal line is derived from a stamp on a node — `verified[]` entries and `generated.at` — so a
     line that cannot be traced to a node cannot exist
- M2 a `## Notes` section, if present, is preserved verbatim across every recompile; it is the only place a
     human writes in the journal
- M3 entries are grouped newest-first under ISO `## YYYY-MM-DD` headings (OKF §9), and rotation moves whole
     date groups into the closing milestone's CLOSE
- M4 exactly three codes carry `error`; every other finding is `info` and never rejects a bundle
</must>
<reject>
- R:APPEND a design in which two agents can append to the journal concurrently -> "APPEND"
- R:ORPHAN a journal line with no stamp behind it -> "ORPHAN"
- R:FAILINFO conformance that exits non-zero on an `info` finding -> "FAILINFO"
</reject>
<after>
- N agents working N nodes in N worktrees produce zero conflicts on shared bundle files
- a human reading `log.md` can follow any line back to the node and stamp that produced it
</after>
⚠ that compiling the journal on every write stays cheap — if wrong: the T0 scan dominates
  short verbs, and the fallback is to compile on `doctor --sync` and at milestone close only,
  accepting a journal that lags by minutes. The predicate is isolated so it can move.

## PLAN
contract: FORMAT.md law 5 (compiled beats authored), §1 (`log.md`'s description), §4.1 (rotation), §9 (codes)
strategy: make the journal a *projection* rather than a record. Every event ADD cares about —
  open, freeze, gate, close — already lands as a stamp on the node it happened to, so the
  journal has no fact of its own to lose. Rendering it removes the last shared mutable file,
  which is what makes the L-E parallel-wave design safe. Failure handling: an unparseable node
  contributes no lines and one `info` finding; it never aborts the render.
scope: FORMAT.md
floor: none — greenfield format
least-sure: contract — whether `## Notes` should sit at the top (read first) or the bottom
  (never displaces the compiled body). Chosen: bottom, because the compiled body is what a
  cold agent reads first.

## CHECKS
- test_log_is_compiled · covers: M1, R:ORPHAN · every rendered line resolves to a stamp on an existing node
- test_notes_preserved · covers: M2 · a `## Notes` block survives a recompile byte-identically
- test_no_concurrent_append · covers: R:APPEND · the format specifies no verb that appends to `log.md`
- test_log_rotates_at_close · covers: M3 · closing a milestone moves whole date groups into CLOSE and truncates
- test_only_three_errors · covers: M4 · exactly three codes carry `error`; every other finding is `info`
- test_unknown_type_is_info · covers: M4 · a node with an unrecognized `type:` yields `info` and still compiles
- test_escape_is_error · covers: M4 · an edge pointing outside the bundle yields `error`
- test_info_exits_zero · covers: R:FAILINFO · a bundle whose only findings are `info` exits 0
red-first: every check above MUST fail for the right reason before BUILD.

## EVIDENCE
receipt: <tasks/define-log-rotation.d/runs/1.md — pending the M0 validator>
gate: <pending>
scope-check: <pending>

## LESSONS
- The journal was the last file in the bundle that two agents could write at once, and it was also the only
  one holding facts already stamped elsewhere. Those two properties are the same property: a file worth
  compiling is a file nobody needs to lock -> add learn system
- Rotation stopped needing a rule the moment the journal became a projection. A rendered artifact is
  truncated by changing what it renders, not by editing it -> add learn method
