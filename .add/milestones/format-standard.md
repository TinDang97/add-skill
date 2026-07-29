---
type: Milestone
title: Format standard
goal: >-
  ABF-1 plus amendments A1–A21 are ratified, every profiled standard claim is checked
  against its source text, and a worked example bundle validates every rule by
  existing — a validator exits 0 on it
status: active
stage: mvp
depth: deep
tasks:
  - /tasks/define-entity-model.md
  - /tasks/define-task-schema.md
  - /tasks/define-authority-rules.md
  - /tasks/define-read-protocol.md
  - /tasks/define-log-rotation.md
  - /tasks/align-standards-citations.md
  - /tasks/define-scale-rules.md
  - /tasks/define-compat-contract.md
  - /tasks/define-evidence-binding.md
  - /tasks/build-worked-example.md
depends_on: []
generated: { by: claude/opus-5, at: 2026-07-29 }
ratified: []
verified: []
---
## CARD
goal: ABF-1 + A1–A21 ratified, proven by a bundle that validates
shape: nine rule tasks land in FORMAT.md, one task proves them by building the example
state: 10 verify — all rules written, validator green, nothing gated yet
next: human gate on build-worked-example — `scope:` matches `sensitive_paths:`, so A17
      pins the floor to human and the task cannot self-gate

## SCOPE
In:  FORMAT.md §0–§13 · amendments A1–A21 · the template corpus · this bundle as the
     worked example · a validator script that exits 0 on a conforming bundle
Out: the engine (M1) · SKILL.md (M2) · personas beyond the schema (M3) · evals (M4)
     · packaging (M5) · any migration path from 2.5 (cut in v1)

## GROUND
touches: `FORMAT.md` · `templates/*.tmpl` · `templates/prompts/*.xml.tmpl` · `.add/**`
anchors: OKF v0.2 frontmatter (`type`, `generated`, `verified`) · ATG node
  *(needs, work, gives)* · the closed `type:` vocabulary · the T0/T1/T2 tiers
honors: specs/domain#decisions-that-bind (closed vocabulary, slug rules) ·
  specs/system#decisions-that-bind (files are the database, engine records only)
risks: fragment resolution (`#gives` vs heading slugs) is the one rule with no
  precedent in 2.5 — it must be proven by example before M1 builds a resolver on it ·
  a format change after M1 starts is a change request with real cost ·
  test-ID extraction (A15) is the one rule whose viability depends on tools we do not
  control; if `ids: unknown` becomes the common case, the binding degrades to a finding
  nobody reads · every OKF claim is a citation that can be wrong in a way that reads
  correct — check the source, never the memory

## EXIT
- [ ] FORMAT.md carries A1–A21, each with its rationale                   (← define-authority-rules, define-read-protocol, define-log-rotation, align-standards-citations, define-scale-rules, define-compat-contract, define-evidence-binding)
- [ ] the `type:` vocabulary and slug rules are closed and unambiguous     (← define-entity-model)
- [ ] a task node's frozen interface is machine-readable and its repair rule stated (← define-task-schema)
- [ ] every read tier and the brief budget are specified, not implied     (← define-read-protocol)
- [ ] every OKF **and ATG** claim matches its source text, and every extension is declared (← align-standards-citations)
- [ ] no bundle file has two concurrent writers: everything derivable is compiled (← define-log-rotation)
- [ ] a milestone's scope can change without a silent edit and without erasing a dropped goal (← define-compat-contract)
- [ ] a gate cannot pass on a check that was never written, at any depth   (← define-evidence-binding)
- [ ] the format can add a key without breaking a live bundle             (← define-compat-contract)
- [ ] orientation cost is bounded on a bundle of hundreds of nodes        (← define-scale-rules)
- [ ] `.add/` in this repo conforms: validator exits 0, zero `error` findings (← build-worked-example)
- [ ] the example exercises `#gives`, `#goal`, a heading-slug fragment, and one deliberate `edge_unresolved` (← build-worked-example)

## STRATEGY
approach: risk-first — the three unprecedented rules (authority, fragments, freshness)
  land before the four that merely restate proven 2.5 behavior
freeze-first: `define-task-schema` publishes the node shape every other task cites;
  it freezes before the rest fill in
waves: define-authority-rules ∥ define-read-protocol ∥ define-log-rotation ∥
  align-standards-citations ∥ define-scale-rules can run concurrently once the schema is
  frozen; define-compat-contract and define-evidence-binding follow the authority rules
  they build on; build-worked-example is strictly last — it is M0's only evidence path
tradeoffs: considered ratifying FORMAT.md as-is and amending during M1 — rejected,
  because the engine compiles against the format and a mid-M1 format change
  invalidates written code. One session of format work buys a stable M1.

## CLOSE
evidence: <one row per task — <t-slug>: gate=<outcome> · checks=<n green> · residue=<none|note>>
census: <engine calls · briefs compiled and their bytes · receipts · human approvals · gates by outcome>   (A18)
log: <the rotated `## YYYY-MM-DD` groups from log.md fold in here>                                          (A4)
goal met: <restate the goal, and the one evidence line that proves the ship meets it>
