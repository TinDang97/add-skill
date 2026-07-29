---
type: Task
title: Define the read protocol and brief grammar
goal: every read declares a tier and every brief declares a budget it cannot silently exceed
status: done
depth: standard
kind: docs
sensitivity: architecture
milestone: /milestones/format-standard.md
depends_on:
  - /tasks/define-task-schema.md
needs:
  - /tasks/define-task-schema.md#gives
gives:
  - "read tiers: T0 frontmatter ~50tok · T1 CARD ~150tok · T2 body 1-3k; T2 is single-node"
  - "fragment resolver: frontmatter key first, then heading slug, else edge_unresolved (info)"
  - "brief budget: a per-depth ceiling; overflow degrades to T1 refs and says so"
scope:
  - FORMAT.md
  - templates/prompts/*.tmpl
generated: { by: claude/opus-5, at: 2026-07-29 }
verified:
  - { by: "human:tindang", at: 2026-07-29, act: freeze, authority: human }
  - { by: "human:tindang", at: 2026-07-29, act: gate, authority: human, outcome: PASS,
      receipt: /tasks/build-worked-example.d/runs/3.md }
    # A17 pinned this to `human`: `scope:` includes FORMAT.md, a sensitive_path. The
    # declared `sensitivity:` was never the binding constraint.
---
## CARD
goal: the token method expressed as format, not discipline
gives: the three tiers, the fragment resolver, the brief budget
scope: FORMAT.md §4 · FORMAT.md §7 · templates/prompts/*.xml.tmpl
beat: done · gate PASS by human:tindang on receipt 3

## RULES
<must>
- M1 a node's cross-node read is its CARD; T2 is read for the active node only
- M2 a fragment resolves against the frontmatter key first, then a heading slug, and nothing else
- M3 a brief injects references, never copied prose, so a spec edit re-scopes every future brief
- M4 a brief declares a byte ceiling per depth; on overflow it degrades to T1 refs and reports the degradation
- M5 every verb's output ends with a `next:` line naming the exact next command and the cheapest legal lane
</must>
<reject>
- R:INLINE a brief that copies spec text into the prompt body -> "INLINE"
- R:SILENT a brief that exceeds its budget without saying so -> "SILENT"
- R:AMBIG a fragment grammar where one reference could resolve two ways -> "AMBIG"
</reject>
<after>
- a task's context is its own body plus T1 cards of its dependencies, and nothing else by default
- changing a spec version re-scopes every future prompt with zero prompt edits
</after>
⚠ that CARD stays under ten lines in practice once real projects fill it — if wrong:
  T1 inflates toward T2 and the tier distinction stops buying anything

## PLAN
contract: the tier table, the two-namespace fragment resolver, the budget rule, the `next:` contract
strategy: specify in FORMAT §4 (tiers) and §7 (briefs). The resolver is the one rule
  with no 2.5 precedent, so it is stated as a closed grammar with an explicit
  else-branch (`edge_unresolved`, severity info) rather than as a lookup heuristic.
scope: FORMAT.md §4 · FORMAT.md §7 · templates/prompts/*.xml.tmpl
floor: none — greenfield format
least-sure: rules — the CARD line ceiling, and whether the budget is bytes or tokens

## CHECKS
- test_card_is_t1 · covers: M1 · resolving a neighbor's shape reads CARD only, never the body
- test_fragment_frontmatter_first · covers: M2 · `#gives` resolves to the key even when a `## Gives` heading exists
- test_fragment_heading_fallback · covers: M2 · `#decisions-that-bind` resolves to the section when no such key exists
- test_fragment_unresolved_is_info · covers: M2, R:AMBIG · a fragment matching neither yields `info`, not `error`
- test_brief_is_refs · covers: M3, R:INLINE · a compiled brief contains reference ids, not copied spec prose
- test_budget_degrades_loudly · covers: M4, R:SILENT · an over-budget brief drops to T1 and reports it
- test_next_line_present · covers: M5 · every verb's output ends with a `next:` line
red-first: every check above MUST fail for the right reason before BUILD.

## EVIDENCE
receipt: /tasks/build-worked-example.d/runs/3.md — 18/18, the shared M0 evidence run
gate: PASS — human:tindang, 2026-07-29, authority `human` (A17 floor)
scope-check: FORMAT.md only — inside the declared scope

## LESSONS
- Measured: cost = turns x context-per-turn; the tier rule is the only lever that touches every one of ~600 turns -> add learn method
- Measured: guide-only features got 0% adoption; the `next:` line is the adoption mechanism, not a courtesy -> add learn experience
