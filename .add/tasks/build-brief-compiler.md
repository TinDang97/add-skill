---
type: Task
title: brief — compile a task's context, and nothing else
goal: an agent receives exactly the context a task needs, assembled by the engine rather than by judgement
status: done
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
verified:
  - { by: "claude/opus-5", at: 2026-07-30, act: freeze, authority: human }
  - { by: "process:run", at: 2026-07-30, act: run, authority: process, outcome: PASS, receipt: /tasks/build-brief-compiler.d/runs/2.md }
  - { by: "human:tindang", at: 2026-07-30, act: gate, authority: human, outcome: PASS }
  - { by: "process:run", at: 2026-07-30, act: run, authority: process, outcome: PASS, receipt: /tasks/build-brief-compiler.d/runs/3.md }
---
## CARD
goal: an agent receives exactly the context a task needs, assembled by the engine rather than by judgement
gives: brief · the XML prompt skeleton filled mechanically from the graph  · a byte count, so the cost of a brief is measured rather than assumed
scope: add/scripts/add.py · its red suite
beat: done · next: add freeze build-brief-compiler

## RULES
<must>
- M1 **T2 is single-node.** A brief carries the task's own body, T1 CARDS of its `depends_on`, the `#gives` fragments it `needs:`, and the bind sections of relevant specs. Nothing else, ever, by default (FORMAT §4)
- M2 the brief is COMPILED from the graph, never authored — no hand-written context blocks, so it cannot drift from the nodes it describes (law L7)
- M3 the brief reports its own size in bytes and node count, so §3e's token method is measured against real numbers rather than estimated
- M4 a persona's frontmatter is included; its body is not (D-4 — the corpus is referenced, never vendored)
- M5 a brief compiles **byte-identically** from the same bundle state, and prints a content hash
     (A16). No timestamp, no path outside the bundle, no set iteration order may enter the text
- M6 on overflow the brief degrades to T1 refs in a DECLARED order and reports every degradation
     (A5). It never silently truncates the subject's own body — dropping instructions quietly is
     worse than reporting an overflow
</must>
<reject>
- R:T2FANOUT pulling a second node's full body into one brief -> "T2FANOUT"
- R:HANDBRIEF any context assembled by hand rather than compiled -> "HANDBRIEF"
- R:UNMEASURED a brief that does not report its own cost -> "UNMEASURED"
- R:INLINE inlining a file from outside the bundle as instruction rather than quoted `<evidence>` -> "INLINE"
- R:SILENTCUT truncating the subject body to fit a budget -> "SILENTCUT"
</reject>
⚠ that a closed five-spec model makes "relevant specs" a compiled fact rather than a judgement —
  all five bind sections total 6,522 bytes on this bundle, 27% of a standard brief. If that ratio
  holds on real projects the rule is affordable; if a domain's specs grow, relevance has to become
  a declared edge and this becomes a per-milestone `honors:` lookup.

## PLAN
contract:
  `brief(root, cid, phase=None, for_subagent=False, evidence=None) -> dict` returning
  `{text, bytes, hash, nodes, budget, degraded: [str], phase, depth}` ·
  `bind_sections(graph) -> {spec_cid: text}` · `brief_budget(depth) -> int`
strategy:
  Everything is resolved through e2's compiled graph and e1's tiered `read`; the compiler never
  walks the tree. Composition, in a fixed order so A16's determinism is structural rather than
  asserted: subject body (T2, the ONE node) → T1 CARDs of `depends_on` sorted by cid → `#gives`
  fragments for each `needs:` ref via e2's `resolve` → all five specs' `Decisions that bind`,
  sorted → persona frontmatter if a `persona:` ref exists. Nothing else can enter, because
  nothing else is read.
  **Units.** FORMAT §7.2 states the ceiling in BYTES; PROPOSAL §3d states the lane budgets in
  TOKENS (2k/6k/10k). The engine has no tokenizer and may not acquire one (D-1, stdlib only), so
  bytes are the enforced unit at a DECLARED 4 bytes/token — 8,000 / 24,000 / 40,000 — and the
  brief prints both numbers with the ratio labelled as declared, never measured. This is A1's
  units error caught before it could ship rather than after.
  **Degradation ladder** (M6), applied in order and each step reported: (1) spec bind sections
  become unresolved `<ref/>` elements · (2) dep CARDs become `<card omitted="budget"/>` ·
  (3) still over → the brief reports `OVER BUDGET` and emits the subject whole anyway.
  Failure handling: a missing ref resolves to `<ref unresolved="true"/>`, never an exception —
  a brief that refuses to compile blocks the work it exists to enable. Rollback: git.
scope: add/scripts/add.py · tests/engine/test_brief_compiler.py
floor: validator exits 0 on `.add/`; every earlier task's checks stay green
least-sure: rules — M5. Determinism is easy to claim and easy to break by accident: a dict
  iteration order, a `set`, an `os.listdir`, a stamp. The suite compiles the same brief twice and
  compares bytes, which catches all four.

## CHECKS
- test_brief_is_single_node_t2 · covers: M1, R:T2FANOUT · only the subject's body appears in full
- test_brief_includes_dep_cards · covers: M1 · each depends_on contributes its CARD, not its body
- test_brief_resolves_gives_fragments · covers: M1 · a `needs: x#gives` is injected verbatim
- test_brief_includes_bind_sections · covers: M1 · specs contribute `Decisions that bind` only
- test_brief_is_compiled_not_authored · covers: M2, R:HANDBRIEF · editing a node changes the brief with no other edit
- test_brief_reports_bytes · covers: M3, R:UNMEASURED · the output states bytes, node count and budget
- test_brief_reports_both_units · covers: M3 · the token figure is printed AND labelled as a declared ratio
- test_persona_body_excluded · covers: M4 · a persona contributes frontmatter only
- test_brief_hash_is_deterministic · covers: M5 · the same bundle state compiles byte-identically twice
- test_brief_hash_changes_with_bundle · covers: M5 · a one-byte spec edit changes the hash
- test_brief_carries_no_timestamp · covers: M5 · today's date appears nowhere in the text
- test_budget_overflow_degrades_loudly · covers: M6 · an oversized bundle drops specs to refs and SAYS so
- test_degradation_never_truncates_subject · covers: M6, R:SILENTCUT · the subject body survives whole
- test_outside_file_enters_only_as_evidence · covers: M1, R:INLINE · a repo file appears quoted in `<evidence>`, never in `<context>`
- test_for_subagent_is_self_contained · covers: M2 · the subagent contract carries objective, constraints, required evidence and a close command
- test_phase_sets_required_evidence · covers: M3 · direction requires none, build a receipt, verify a covers-bound receipt
- test_brief_ends_with_next · covers: M2 · law 4 holds for this verb too
- test_missing_ref_does_not_raise · covers: M1 · an unresolved ref is reported in the text, not raised
- test_live_bundle_brief · covers: M1, M3 · every Task in this repo compiles within its own budget
- test_ref_ids_survive_compilation · covers: M1, M2 · a ref id survives compilation intact, so an agent can resolve it back
- test_wrapped_quoted_gives_is_not_truncated · covers: M1 · a wrapped quoted list item keeps its whole value (e1 regression)
- test_quoted_item_with_apostrophe_does_not_swallow_frontmatter · covers: M1 · quote balance is scanned, not counted
- test_live_bundle_keys_all_parse · covers: M1, M2 · every key on disk reaches the parsed node — the read-side oracle
red-first: every check above MUST fail for the right reason before BUILD.
<!-- Authored 2026-07-30, before freeze. The seven checks this node opened with named the shape
     correctly but left M5/M6 — determinism and degradation, the two rules with real failure modes —
     with no check at all. F2's lesson applied to the node being written rather than to M0's. -->

## EVIDENCE
receipt: /tasks/build-brief-compiler.d/runs/2.md — 21/21 green · kind test-ids · freshness content ·
  red-first proven by runs/1.md (19/19 fail on absent `brief`, `0/19 reported`)
floor: validator CONFORMS on `.add/`; full suite 134 green
measured-not-estimated: the first real numbers for PROPOSAL §3d's lane budgets, over this repo's
  16 Task nodes — **mean 13,658 B (~3.4k tok) · max 19,221 B (~4.8k tok) · 0 over budget, 0
  degraded** — against a standard lane of 24,000 B / 6k tok. The five bind sections are 6,522 B of
  that, so "relevant specs = all five" costs ~27% of a standard brief and is affordable at this
  scale. §3d's ≤6k tok target holds on real nodes rather than on an estimate
units-resolved: FORMAT §7.2 (bytes) and PROPOSAL §3d (tokens) disagreed. Bytes are enforced,
  tokens are printed at a DECLARED 4 B/tok, and the word "declared" is itself asserted by a check
  (`test_brief_reports_both_units`) so the ratio can never be read as measured. A1's units error
  caught before shipping instead of after
budget: 200 lines against 267 allocated. Engine 1,238/2,400 · A3 invariant: 1,238 + 440
  (e8 200 + e9 80 + e10 80 + e11 80) = **1,678 / 2,400 — slack 722**
scope-check: match — `add/scripts/add.py` and `tests/engine/test_brief_compiler.py` only
found-by-reading-the-output: **two defects, with 19/19 already green.** (1) every `#gives` ref id
  rendered as `tasks/x.md#gi` — `[:-3]` applied to the whole ref instead of to the path — so no
  agent could resolve a ref back; the suite asserted resolved VALUES and never once the id.
  (2) an **e1 parser defect**: a double-quoted list item wrapped across lines was truncated at the
  first newline and kept its opening quote, silently losing the rest of a frozen `gives:`. It was
  live in this repo's own `compile-graph` node since e2 and survived 132 checks, the M0 validator
  and five human gates. Both fixed red-first; `test_wrapped_quoted_gives_is_not_truncated` is the
  regression
gate: PASS — human:tindang, 2026-07-30, stamped by the engine
> **Post-gate correction, recorded not rewritten (§3.6).** The parser fix above was WRONG and did
> more damage than the defect it repaired. It continued a wrapped list item while the quote COUNT
> was odd; `the node's own body` makes a single-quote count odd while opening nothing, so the
> continuation ran to the end of the frontmatter and swallowed `budget`, `generated` and
> `verified` into one string — **across 25 nodes of this bundle**, with the full suite at 134 green
> and the M0 validator reporting CONFORMS. Both oracles were blind: the suite has no node with an
> apostrophe inside a quoted item, and the validator has its own independent parser.
> **What caught it was `done` refusing to transition** — the gate stamp had become unparseable, so
> the notary correctly declined to record a `done` it could not entitle. A refusal designed to stop
> a false record stopped a parser defect instead.
> Fixed properly with `_open_quote`, which SCANS quote state rather than counting characters.
> Two checks added red-first: the apostrophe regression, and `test_live_bundle_keys_all_parse` —
> the oracle this project was missing, asserting that every key present in a node's raw text
> reaches its parsed dict. `test_roundtrip_bundle_byte_identical` proved writes lossless and was
> silent on reads; a key can vanish from `fm` while the bytes on disk are perfect.
> Receipt 2 went STALE by content digest the moment `add.py` changed (A22 working as designed), so
> the gate rests on **receipt 3 — 23/23, kind test-ids, freshness content, verified fresh**.
> Final: 136 green · engine 1,256 lines · 218 against 267 allocated.

## LESSONS
- **Three defects now, every one found by reading output a green suite had already approved.**
  e6's bounded-but-useless report, e7's over-claimed receipt, e5's mangled ref ids. The pattern is
  exact: tests assert what the code was specified to do and go silent wherever the specification
  never mentioned the thing a reader notices first. A check that asserts a resolved VALUE will
  never notice a corrupted KEY. Every user-facing verb needs one check whose subject is the
  artifact as a reader receives it. -> add learn quality
- **A brief is the cheapest defect detector this project has.** It renders authored values where a
  human reads them, so an e1 parser bug that five gates, a conformance validator and 132 checks all
  missed became visible at a glance. Rendering is a stronger oracle than validating: validation
  asks "is this well-formed?", rendering asks "is this what you meant?" -> add learn quality
- **A flag that changes nothing is not a feature, and a check that cannot see the difference is not
  a check.** `test_for_subagent_is_self_contained` as first authored passed for the default brief
  too. Caught before green by asking what would make it fail. -> add learn method
- **Two specs stating one budget in two units is A1 repeating.** FORMAT said bytes, PROPOSAL said
  tokens, and nothing reconciled them until a verb had to enforce one. The fix is not picking a
  unit — it is printing both with the derived one LABELLED as declared, so the next reader cannot
  make the same mistake silently. -> add learn method

