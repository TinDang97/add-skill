---
type: Milestone
title: Format standard
goal: >-
  ABF-1 plus amendments A1–A24 are ratified, every profiled standard claim is checked
  against its source text, and a worked example bundle validates every rule by
  existing — a validator exits 0 on it
status: done
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
verified:
  - { by: "human:tindang", at: 2026-07-29, act: close, authority: human, outcome: PASS }
---
## CARD
goal: ABF-1 + A1–A24 ratified, proven by a bundle that validates
shape: nine rule tasks land in FORMAT.md, one task proves them by building the example
state: done — 10/10 gated at `human` authority on one shared receipt
next: M1 `e1 port-okf-parse` — the frontmatter parser in validate_bundle.py was written to be that port

## SCOPE
In:  FORMAT.md §0–§13 · amendments A1–A24 · the template corpus · this bundle as the
     worked example · a validator script that exits 0 on a conforming bundle
Out: the engine (M1) · SKILL.md (M2) · personas beyond the schema (M3) · evals (M4)
     · packaging (M5) · any migration path from 2.5 (cut in v1)

## GROUND
touches: `FORMAT.md` · `templates/*.tmpl` · `templates/prompts/*.xml.tmpl` · `.add/**`
anchors: OKF v0.2 frontmatter (`type`, `generated`, `verified`) · ATG §3's node `(i, f, o)`,
  raised one altitude to `needs`/work/`gives` (A19) · the closed `type:` vocabulary · T0/T1/T2
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
- [x] FORMAT.md carries A1–A24, each with its rationale                   (← define-authority-rules, define-read-protocol, define-log-rotation, align-standards-citations, define-scale-rules, define-compat-contract, define-evidence-binding)
- [x] the `type:` vocabulary and slug rules are closed and unambiguous     (← define-entity-model)
- [x] a task node's frozen interface is machine-readable and its repair rule stated (← define-task-schema)
- [x] every read tier and the brief budget are specified, not implied     (← define-read-protocol)
- [x] every OKF **and ATG** claim matches its source text, and every extension is declared (← align-standards-citations)
- [x] no bundle file has two concurrent writers: everything derivable is compiled (← define-log-rotation)
- [x] a milestone's scope can change without a silent edit and without erasing a dropped goal (← define-compat-contract)
- [x] a gate cannot pass on a check that was never written, at any depth   (← define-evidence-binding)
- [x] the format can add a key without breaking a live bundle             (← define-compat-contract)
- [x] orientation cost is bounded on a bundle of hundreds of nodes        (← define-scale-rules)
- [x] `.add/` in this repo conforms: validator exits 0, zero `error` findings (← build-worked-example)
- [~] the example exercises `#gives`, `#goal`, a heading-slug fragment, and one deliberate `edge_unresolved` (← build-worked-example)
      MET IN FIXTURE, NOT IN THE LIVE BUNDLE. `test_all_fragment_forms` exercises all four forms in a temp
      bundle; `.add/` carries no defect on purpose. Recorded rather than ticked: a reference example should
      be exemplary, and a criterion half-met is not a criterion met.

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
evidence: one shared receipt earned this milestone — `/tasks/build-worked-example.d/runs/3.md`
  (18/18, `kind: test-ids`, `ids: parsed`, `red_first: proven`, `freshness: content`), because
  nine of the ten tasks deliver rules in one artifact and the tenth is the check on that artifact.
  - build-worked-example ....... gate=PASS · checks 12 green · residue: two coverage rules
      (a deliberate `edge_unresolved`, and ≥3 concurrent `status:` values) live in the test
      fixture rather than the live bundle — declared, not manufactured
  - define-entity-model ........ gate=PASS · 5 checks · residue: none
  - define-task-schema ......... gate=PASS · 5 checks · residue: none
  - define-authority-rules ..... gate=PASS · 8 checks · residue: A22's predicate is specified, not implemented (e7)
  - define-read-protocol ....... gate=PASS · 7 checks · residue: none
  - define-log-rotation ........ gate=PASS · 8 checks · residue: compile-cost assumption open (⚠ recorded)
  - align-standards-citations .. gate=PASS · 6 checks · residue: none — both sources fetched and checked
  - define-scale-rules ......... gate=PASS · 3 checks · residue: none
  - define-compat-contract ..... gate=PASS · 11 checks · residue: none
  - define-evidence-binding .... gate=PASS · 10 checks · residue: `ids: unknown` frequency unknown until e12

census (A18):
  engine calls ............ 0 — the engine does not exist yet. **M0 ran entirely in hand-mode**,
                            which is the only honest test of G7 and of "files are the database"
  briefs compiled ......... 0 (0 bytes) — no compiler yet; every prompt was authored
  receipts ................ 3 — runs/1 (13/13 red, validator absent) · runs/2 (14/14) · runs/3 (18/18)
  human decisions ......... 3, producing 10 gate stamps
  gates by outcome ........ PASS 10 · RISK-ACCEPTED 0 · HARD-STOP 0
  amendments landed ....... A1–A24, across three format revisions (1.0 → 1.1 → 1.2 → 1.3)
  defects found by check .. 9 — D1–D5 (OKF citations) · R1 (ATG citation) · R10 (three stale
                            authored facts) · P2 (mtime freshness, killed by test) · P3 (compiled
                            files still merge-conflict)

log: the `## 2026-07-29` group rotates here from `log.md` (A4). Every line traces to a stamp:
  - 10 × gate PASS by human:tindang on receipt 3 — the M0 close
  - process:pytest · receipts 1–3 on build-worked-example
  - claude/opus-5 · FORMAT.md 1.1 → 1.2 → 1.3; PROPOSAL v2 → v3 → v4
  - human:tindang · four ratification decisions (D-7 … D-10, then the proactive layer and Stage 1)

goal met: ABF-1 plus A1–A24 are ratified and every external standard claim is checked against its
  source text. The proof is that this bundle exists and validates: `python3 scripts/validate_bundle.py
  .add` → 21 nodes · 51 edges · 0 info · 0 error · exit 0. The rule that bound hardest was our own —
  A17 pinned all ten tasks to `human` because their scope is `FORMAT.md`, a declared sensitive path,
  and no batching path exists below `human`. That cost is recorded as finding P8 and left unfixed,
  because amending a trust rule that binds its author is the failure this method exists to prevent.
