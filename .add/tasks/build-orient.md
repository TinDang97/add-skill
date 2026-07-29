---
type: Task
title: status — orientation, and the three flags A3 restored
goal: a cold reader learns where the project is, and what to do next, from one bounded T0 report
status: done
depth: standard
kind: feature
sensitivity: architecture
milestone: /milestones/engine-core.md
depends_on:
  - /tasks/compile-graph.md
  - /tasks/build-node-verbs.md
needs:
  - /tasks/compile-graph.md#gives
  - /tasks/build-node-verbs.md#gives
gives:
  - "status(root, ...) -> a bounded orientation report ending in a `next:` line"
  - "locate(graph, term) -> nodes matching a slug or title fragment (A3, goal 11)"
  - "graph_lines(graph, milestone) -> the DAG for ONE milestone, never the whole bundle (A12)"
  - "since(graph, date) -> what changed on or after a date, from `verified[]` stamps (A3, R8)"
  - "card_drift(graph) / render_card(...) -> detect and repair the CARD/frontmatter contradiction e4 created"
scope:
  - add/scripts/add.py
  - tests/engine/test_status.py
budget: 407 lines wc -l of growth (amendment A1 as revised by A3)
generated: { by: claude/opus-5, at: 2026-07-29 }
verified:
  - { by: "process:pytest", at: 2026-07-29, act: run, authority: process, outcome: PASS, receipt: /tasks/build-orient.d/runs/2.md }
  - { by: "human:tindang", at: 2026-07-29, act: gate, authority: human, outcome: PASS }
---
## CARD
goal: one bounded T0 report that orients a cold reader and names the next command
gives: status · locate · graph_lines · since · card_drift/render_card
scope: add/scripts/add.py · tests/engine/test_status.py
beat: done · next: red suite, then green, then gate

## RULES
<must>
- M1 `status` reads **T0 only** and stays bounded: at most 20 node lines plus a count, `done` and
     `dropped` excluded by default, graph rendering per milestone and never whole-bundle (A12)
- M2 `status` ends in a `next:` line naming a runnable command, derived from the graph — the
     frontier from `ready()`, or the gate a task is waiting on (law 4)
- M3 `locate` matches a slug or title fragment and returns cids, so a human never has to know a
     path to find a node (goal 11)
- M4 `since(date)` reports from `verified[]` stamps — the recorded acts, never file mtimes, which
     the M0 kill-test proved worthless across a checkout (A22)
- M5 `card_drift` reports every node whose `## CARD` contradicts its frontmatter, and
     `render_card` repairs it. **This closes the defect e4 created**: a transition that changes
     `status:` must not leave `beat:` asserting the old one
- M6 every function here is a **notary**: it reports and never blocks, never raises on a malformed
     node, and never writes except through `render_card`, which writes surgically (law 3)
</must>
<reject>
- R:UNBOUNDED output that grows with bundle size — the context hazard A12 exists to stop -> "UNBOUNDED"
- R:T2SCAN reading bodies of every node to build a report -> "T2SCAN"
- R:MTIME using file mtime for `--since` instead of recorded stamps -> "MTIME"
- R:SILENTDRIFT a report that shows a stale CARD as though it were current -> "SILENTDRIFT"
</reject>
<after>
- a cold agent can resume this project from `add status` alone, without reading FORMAT.md
- the engine stops producing the contradiction it was built to prevent
</after>
⚠ that `next:` can always be derived from the graph — if wrong: some state has no defensible next
  step and `status` must say so honestly rather than invent one. The suite asserts a `next:` line
  on an empty bundle, a blocked bundle, and a finished one.

## PLAN
contract:
  `status(root, locate=None, graph=None, since=None, all=False) -> str` ·
  `locate(graph, term) -> [cid]` · `graph_lines(graph, milestone_cid) -> [str]` ·
  `since(graph, date) -> [(date, cid, act, by)]` · `card_drift(graph) -> [(cid, field, card, fm)]` ·
  `render_card(root, cid) -> (changed: bool, note)`
strategy:
  Everything reads the compiled graph from e2 — no verb walks the tree itself. `status` composes
  the same primitives the flags expose, so the flags are views on one report rather than three
  code paths. `render_card` uses e1's surgical line edit on the CARD's `beat:`/`state:` line only.
  Failure handling: a malformed node is reported as a line in the output, never an exception.
  Rollback: git.
scope: add/scripts/add.py · tests/engine/test_status.py
floor: validator exits 0 on `.add/`; e1's round-trip and e4's transitions stay green
least-sure: rules — M5. Repairing a CARD is a write, and every other function here is read-only.
  The risk is a repair that rewrites more than the one stale line, so the suite asserts a
  byte-diff of exactly one line.

## CHECKS
- test_status_is_t0_only · covers: M1, R:T2SCAN · no body is read to build the report
- test_status_is_bounded · covers: M1, R:UNBOUNDED · a 100-node bundle still prints ≤20 node lines plus a count
- test_status_excludes_done_by_default · covers: M1 · done nodes appear only with all=True
- test_status_ends_with_next · covers: M2 · the report's last line names a runnable command
- test_next_on_empty_bundle · covers: M2 · a bundle with no tasks still names a defensible next step
- test_next_names_the_blocking_gate · covers: M2 · a task awaiting a gate produces `add gate <slug>`
- test_locate_by_slug_fragment · covers: M3 · a partial slug finds the node
- test_locate_by_title_fragment · covers: M3 · a title word finds the node
- test_graph_is_per_milestone · covers: M1, R:UNBOUNDED · rendering one milestone excludes another's tasks
- test_since_uses_stamps_not_mtime · covers: M4, R:MTIME · touching a file changes nothing; a stamp does
- test_card_drift_detected · covers: M5, R:SILENTDRIFT · a CARD contradicting frontmatter is reported
- test_render_card_repairs_one_line · covers: M5 · the repair changes exactly one line
- test_render_card_is_idempotent · covers: M5 · a second render writes nothing
- test_notary_never_raises · covers: M6 · a malformed node yields a report line, not an exception
- test_live_bundle_status · covers: M1, M2 · this repo's own bundle produces a bounded report with a next:
red-first: every check above MUST fail for the right reason before BUILD.

## EVIDENCE
receipt: /tasks/build-orient.d/runs/2.md — 17/17 green · red-first proven by runs/1.md
gate: PASS — human:tindang, 2026-07-29, stamped by the engine
found-on-live-bundle: the drift scan reported a REAL contradiction in this repo —
  `/tasks/port-okf-parse.md` carried `status: done` with `beat: build`, introduced at e1 and
  missed through four later gates and five human approvals. `render_card` repaired it, one line
conflict-resolved: `card_drift` reads each CARD, contradicting M1's T0 bound. The scan became
  OPT-IN (`--check`) rather than M1 being weakened to fit the code. The deep pass is `doctor --sync`
budget: 158 lines against 407 allocated. Engine 812/2400; A3 invariant 1919/2400, slack 481
scope-check: match — `add/scripts/add.py` and `tests/engine/test_status.py`
⚠ open: `render_card` repairs only the `beat:` token. The rest of a CARD line — a stale `next:`
  hint, for instance — is left as authored. Drift is reduced, not eliminated

## LESSONS
- **A green suite proved the code correct and said nothing about whether it was good.** `status`
  passed 15 checks while spending 10 of its 20 orientation lines on receipt nodes named `1`, `2`,
  `3` — bounded, conformant, and useless. The defect was invisible until the verb was RUN against
  a real bundle. Every user-facing verb needs one check that asserts what the output is FOR, not
  merely what it contains. -> add learn experience
- **When an implementation contradicts a rule, narrow the feature before touching the rule.**
  `card_drift` needed body reads; M1 says T0. Weakening M1 would have been one line and would
  have quietly deleted the bound that stops orientation becoming a context hazard.
  -> add learn method
- **The drift detector's first act was to convict its own project.** Four gated tasks and five
  human approvals had passed over a contradiction that a nine-line function found immediately.
  Cheap mechanical checks outperform expensive human attention on mechanical facts — which is
  the argument for compiling them, not for gating harder. -> add learn quality
