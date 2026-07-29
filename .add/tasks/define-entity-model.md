---
type: Task
title: Define the entity model and slug rules
goal: the type vocabulary, bundle layout, and slug rules are closed and unambiguous
status: done
depth: standard
kind: docs
sensitivity: architecture
milestone: /milestones/format-standard.md
depends_on: []
needs: []
gives:
  - "closed type: vocabulary — Project·Milestone·Task·Spec·Persona·Prompt·Run"
  - "bundle layout: index·log·PROJECT·specs/5·milestones/·tasks/·personas/·prompts/·graph.json"
  - "slug rule: filename stem, kebab-case, <=4 words, verb-first tasks, noun-first milestones"
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
goal: closed vocabulary, flat layout, mechanical slug lookup
gives: the type set, the bundle layout, the slug rule
scope: FORMAT.md §1–§2
beat: done · gate PASS by human:tindang on receipt 3

## RULES
<must>
- M1 `type:` is a closed set of seven; an unknown type is an `info` finding, never a rejection
- M2 tasks live flat in `tasks/`, keyed to a milestone by a frontmatter ref, never by nesting
- M3 a slug resolves by filename before any frontmatter is parsed
- M4 a short-scope project is three files total: `index.md`, `PROJECT.md`, one task
</must>
<reject>
- R:NEST a layout that nests tasks under milestone directories -> "NEST"
- R:GUARD a conformance rule that rejects a bundle for an unknown key -> "GUARD"
</reject>
<after>
- re-homing a task to another milestone changes one frontmatter line and no concept ID
- `add find <slug>` needs no index to answer
</after>
⚠ that seven types cover every artifact a wide-domain project needs — if wrong: an
  eighth type is added later and every consumer's exhaustive match changes

## PLAN
contract: FORMAT.md §1 (layout, concept ID, slug) and §2 (the type table)
strategy: state the vocabulary as a closed table with required keys per type; state
  the notary rule (L3) beside it so the closure never becomes a rejection rule.
scope: FORMAT.md §1 · FORMAT.md §2
floor: none — greenfield format
least-sure: rules — whether `Run` deserves to be a type or a receipt sub-shape

## CHECKS
- test_type_table_closed · covers: M1 · exactly seven types, each with required keys
- test_flat_tasks · covers: M2, R:NEST · a task's concept ID is stable across a milestone change
- test_slug_lookup_no_parse · covers: M3 · a slug resolves from the filename alone
- test_minimum_bundle · covers: M4 · a three-file bundle conforms
- test_unknown_key_is_info · covers: R:GUARD · an unknown frontmatter key yields `info`, not `error`
red-first: every check above MUST fail for the right reason before BUILD.

## EVIDENCE
receipt: /tasks/build-worked-example.d/runs/3.md — 18/18, the shared M0 evidence run
gate: PASS — human:tindang, 2026-07-29, authority `human` (A17 floor)
scope-check: FORMAT.md only — inside the declared scope

## LESSONS
- A hand-maintained SEAMS.md is a compiled view in disguise; cross-milestone `gives:`/`needs:` edges already carry it -> add learn domain
