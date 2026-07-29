---
type: Task
title: brief — compile a task's context, and nothing else
goal: an agent receives exactly the context a task needs, assembled by the engine rather than by judgement
status: direction
depth: standard
kind: feature
sensitivity: architecture
milestone: /milestones/engine-core.md
scope:
  - add/scripts/add.py
  - tests/engine/test_brief_compiler.py
depends_on:
  - /tasks/compile-graph.md
  - /tasks/build-orient.md
needs:
  - /tasks/compile-graph.md#gives
  - /tasks/build-orient.md#gives
gives:
  - "brief(root, cid) -> the compiled T2 context: the node's own body + T1 cards of depends_on + #gives fragments + the `Decisions that bind` of relevant specs"
  - "the XML prompt skeleton filled mechanically from the graph (FORMAT §4, A6)"
  - "a byte count, so the cost of a brief is measured rather than assumed"
budget: 267 lines wc -l of growth (amendment A1/A3)
generated: { by: add/3.0.0, at: 2026-07-29 }
verified: []
---
## CARD
goal: an agent receives exactly the context a task needs, assembled by the engine rather than by judgement
gives: brief · the XML prompt skeleton filled mechanically from the graph  · a byte count, so the cost of a brief is measured rather than assumed
scope: add/scripts/add.py · its red suite
beat: direction · next: add freeze build-brief-compiler

## RULES
<must>
- M1 **T2 is single-node.** A brief carries the task's own body, T1 CARDS of its `depends_on`, the `#gives` fragments it `needs:`, and the bind sections of relevant specs. Nothing else, ever, by default (FORMAT §4)
- M2 the brief is COMPILED from the graph, never authored — no hand-written context blocks, so it cannot drift from the nodes it describes (law L7)
- M3 the brief reports its own size in bytes and node count, so §3e's token method is measured against real numbers rather than estimated
- M4 a persona's frontmatter is included; its body is not (D-4 — the corpus is referenced, never vendored)
</must>
<reject>
- R:T2FANOUT pulling a second node's full body into one brief -> "T2FANOUT"
- R:HANDBRIEF any context assembled by hand rather than compiled -> "HANDBRIEF"
- R:UNMEASURED a brief that does not report its own cost -> "UNMEASURED"
</reject>

## PLAN
contract: <published at freeze>
strategy: <published at freeze>
scope: add/scripts/add.py · tests/engine/
floor: validator exits 0 on `.add/`; every earlier task's checks stay green

## CHECKS
- test_brief_is_single_node_t2 · covers: M1, R:T2FANOUT · only the subject's body appears in full
- test_brief_includes_dep_cards · covers: M1 · each depends_on contributes its CARD, not its body
- test_brief_resolves_gives_fragments · covers: M1 · a `needs: x#gives` is injected verbatim
- test_brief_includes_bind_sections · covers: M1 · specs contribute `Decisions that bind` only
- test_brief_is_compiled_not_authored · covers: M2, R:HANDBRIEF · changing a node changes the brief with no other edit
- test_brief_reports_bytes · covers: M3, R:UNMEASURED · the output states its size and node count
- test_persona_body_excluded · covers: M4 · a persona contributes frontmatter only
red-first: every check above MUST fail for the right reason before BUILD.

## EVIDENCE
receipt: <runs/<n>.md>
gate: <PASS | RISK-ACCEPTED | HARD-STOP>
budget: <growth vs allocation · A3 invariant>
scope-check: <files touched vs `scope:`>

## LESSONS
- <lesson> -> add learn <domain|system|experience|quality|method>
