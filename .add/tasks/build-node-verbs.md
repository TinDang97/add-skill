---
type: Task
title: new · freeze · done — the node transitions
goal: the engine writes node state, and refuses to write a record no evidence entitles
status: done
depth: standard
kind: feature
sensitivity: security
milestone: /milestones/engine-core.md
depends_on:
  - /tasks/port-okf-parse.md
  - /tasks/compile-graph.md
  - /tasks/build-init-profiles.md
needs:
  - /tasks/port-okf-parse.md#gives
  - /tasks/compile-graph.md#gives
gives:
  - "new(root, type, slug, **fields) -> a node from a template, attributed, slug-unique"
  - "freeze(root, cid, by, authority) -> appends a freeze stamp; a changed frozen `gives:` refreezes, never edits in place (§3.5)"
  - "done(root, cid, ...) -> transitions only when a gate stamp at the required authority exists; otherwise reports what is missing"
  - "authority_for(graph, cid) -> the floor from `sensitivity:` raised by A17's sensitive-path match"
scope:
  - add/scripts/add.py
  - tests/engine/test_node_verbs.py
budget: 320 lines wc -l of growth (amendment A1)
generated: { by: claude/opus-5, at: 2026-07-29 }
verified:
  - { by: "process:pytest", at: 2026-07-29, act: run, authority: process, outcome: PASS, receipt: /tasks/build-node-verbs.d/runs/2.md }
  - { by: "human:tindang", at: 2026-07-29, act: gate, authority: human, outcome: PASS }
---
## CARD
goal: the engine writes transitions — and will not forge one
gives: new · freeze · done · authority_for
scope: add/scripts/add.py · tests/engine/test_node_verbs.py
beat: done · gated PASS by the ENGINE · 150/320 lines · next: e6 status

## RULES
<must>
- M1 `new` creates a node from a template: correct `type`, unique slug, `generated: { by, at }`,
     and a body carrying the sections its type requires. A colliding slug is reported, not
     silently suffixed
- M2 `freeze` appends `verified: { act: freeze, by, at, authority }`. A frozen `gives:` is
     **never edited in place** — a change lands as a NEW `refreeze` stamp with the old stamp intact
     (§3.5), because history is append-only
- M3 `done` transitions `status` only when `verified[]` already carries a gate stamp at or above
     the required authority. Without one it changes nothing and reports exactly what is missing.
     **This is not guarding: a notary that signs an unsigned document is not a notary** (law 3)
- M4 `authority_for` returns `max(sensitivity floor, A17 sensitive-path floor)` — the §3.1 table
     raised to `human` when any `scope:` entry matches `index.md`'s `sensitive_paths:`. A path
     match is mechanical, so a notary may perform it
- M5 every transition is a surgical write through e1 — comments, key order and body survive
     byte-identically except for the keys the transition names
- M6 every verb returns a `next:` line naming the command that follows (law 4)
</must>
<reject>
- R:FORGE writing `status: done` without a gate stamp that entitles it -> "FORGE"
- R:INPLACE editing a frozen `gives:` instead of appending a refreeze stamp -> "INPLACE"
- R:AUTHDROP computing an authority below A17's sensitive-path floor -> "AUTHDROP"
- R:DUPSLUG creating a node whose slug already exists, or silently renaming it -> "DUPSLUG"
- R:REGEN a transition that rewrites frontmatter from a parsed dict -> "REGEN"
</reject>
<after>
- `.add/` in this repo can be driven by the engine instead of by hand — the EXIT criterion
  `package-in-skill` inherits
- the authority ladder stops being prose and becomes a function with a test
</after>
⚠ that refusing to stamp `done` without evidence is consistent with law 3 — if wrong: the engine
  is guarding after all, and either law 3 or this verb is misstated. The distinction this task
  asserts: a notary refuses to CREATE an unsupported record, but never blocks a human who records
  one themselves with their own authority. Tested both ways.

## PLAN
contract:
  `new(root, type, slug, **fields) -> (cid, note)` · `freeze(root, cid, by, authority=None) -> (node, note)`
  · `done(root, cid) -> (ok: bool, missing: list, note)` · `authority_for(graph, cid) -> str`
strategy:
  All three verbs funnel through one `_transition(root, cid, changes, stamp)` that reads T0, applies
  surgical `set_key`/`append_item` edits to the RAW text, and writes atomically — the shared path
  amendment A1 pre-booked. Authority is computed, never passed in by the caller, so a caller cannot
  talk its way below the floor.
  Failure handling: every verb returns `(result, note)` and reports rather than raises; a missing
  node, a duplicate slug and insufficient evidence are all return values. Rollback: git.
scope: add/scripts/add.py · tests/engine/test_node_verbs.py
floor: `scripts/validate_bundle.py` exits 0 on `.add/` after any engine transition, and e1's
  round-trip check stays green
least-sure: rules — M3's boundary. "Refuses to forge" and "guards" are one line apart. The suite
  pins the line: the engine will not create a `done` stamp without evidence, AND will not stop a
  human from writing one with `authority: human`.

## CHECKS
- test_new_creates_typed_node · covers: M1 · the node has the right `type` and required sections
- test_new_is_attributed · covers: M1 · `generated.by` and `generated.at` are present
- test_new_rejects_duplicate_slug · covers: M1, R:DUPSLUG · a colliding slug reports and writes nothing
- test_freeze_appends_stamp · covers: M2 · `verified[]` gains an entry with `act: freeze`
- test_freeze_preserves_comments · covers: M2, M5, R:REGEN · every other byte survives a freeze
- test_refreeze_keeps_old_stamp · covers: M2, R:INPLACE · a second freeze appends; the first remains
- test_done_refuses_without_gate · covers: M3, R:FORGE · status is unchanged and the note names what is missing
- test_done_transitions_with_gate · covers: M3 · with a human gate stamp present, status becomes done
- test_done_does_not_block_human_record · covers: M3 · a human writing their own stamp is never prevented
- test_authority_floor_from_sensitivity · covers: M4 · `security` floors at `human`, `mechanical` at `process`
- test_authority_raised_by_sensitive_path · covers: M4, R:AUTHDROP · a scope match raises `mechanical` to `human`
- test_transition_is_surgical · covers: M5, R:REGEN · a transition changes only the named keys
- test_every_verb_returns_next · covers: M6 · new, freeze and done each return a `next:` line
- test_live_bundle_still_validates · covers: M5 · the M0 oracle exits 0 after an engine transition
red-first: every check above MUST fail for the right reason before BUILD.

## EVIDENCE
receipt: /tasks/build-node-verbs.d/runs/2.md — 15/15 green · kind test-ids · freshness content ·
  red-first proven by runs/1.md
gate: PASS — human:tindang, 2026-07-29. **Stamped BY THE ENGINE, not by hand** — the first
  transition ADD 3.0 has written against its own bundle
dogfood: `authority_for` computed `human` from `sensitivity: security`; `done` REFUSED the
  transition while no gate stamp existed and named what was missing; after the stamp it
  transitioned. The refusal path ran against the live bundle, not a fixture
surgical-proof: the engine's diff on a 114-line node dense with nested maps, block scalars, XML
  tags and rationale comments was exactly two hunks — `status:` and `verified:`. Nothing else
  moved. Validator 0 errors; e1's byte-identical round-trip still green
defect-found: e4 surfaced a **silent** e1 defect — `append_item` could not append to an inline
  empty list (`verified: []`); the item landed under a surviving `[]` and parsed back as empty.
  No error, no exception, a lost stamp. e1 had 15 green checks and a human gate and shipped it
budget: 150 lines against 320 allocated — UNDER by 170. Engine 654/2400; A3 invariant 2168/2400,
  slack 232
scope-check: match — `add/scripts/add.py` and `tests/engine/test_node_verbs.py`

## LESSONS
- **The engine now creates the drift L7 warns about.** `done` set `status: done` and left the
  CARD reading `beat: build` — one file, two contradicting facts, written by the tool that
  exists to prevent exactly that. A transition must render every derived field it invalidates,
  or the CARD must be compiled. Owed by `e5`/`e6`; fixed by hand here and recorded rather than
  silently patched. -> add learn system
- **A gate is not a defect filter, and should not be sold as one.** e1 passed 15 checks and a
  human gate, then shipped a bug that silently dropped the freeze and gate stamps this entire
  method rests on. It was caught by the NEXT task using the function differently — not by
  review, not by the gate. Gates buy an auditable record of who accepted what; they do not buy
  correctness. Any claim otherwise is unsupported by our own evidence. -> add learn quality
- **Test the empty case of every container you write to.** The defect existed because e1 only
  ever appended to a list that already had items. The first-write path is the one that runs on
  every freshly created node — i.e. the most common path in production. -> add learn quality
