---
type: Milestone
title: Engine core
goal: >-
  all ten verbs are green under red/green TDD, in ≤2,400 lines of Python stdlib shipped
  inside the skill directory, and this repo's own `.add/` runs on them
status: active
stage: mvp
depth: deep
tasks:
  - /tasks/port-okf-parse.md
  - /tasks/compile-graph.md
  - /tasks/build-init-profiles.md
  - /tasks/build-node-verbs.md
  - /tasks/build-brief-compiler.md
  - /tasks/build-orient.md
  - /tasks/build-receipts-learn.md
  - /tasks/build-evidence-binding.md
  - /tasks/build-doctor.md
  - /tasks/build-hints-layer.md
  - /tasks/build-durability.md
  - /tasks/package-in-skill.md
depends_on:
  - /milestones/format-standard.md
generated: { by: claude/opus-5, at: 2026-07-29 }
ratified: []
amended:
  - { by: "human:tindang", at: 2026-07-29, authority: human, reason: "A1 line-budget rebase — the twelve per-task allocations were written in code lines while the 2,400 ceiling is wc -l. Re-derived in the ceiling's unit; 660 code lines of surface pre-booked as cuts. See ## AMENDMENTS" }
  - { by: "human:tindang", at: 2026-07-29, authority: human, reason: "A2 — A1's falsifier was a ratio between two estimates, so it fired at e2 while its conclusion was false. Restated as one measurable: cumulative consumed vs cumulative allocated, checked at every gate. A1 left unedited per §3.6" }
verified: []
---
## CARD
goal: ten verbs, ≤2,400 lines, stdlib only, shipped inside the skill — and dogfooded here
shape: five waves; each wave's line budget is asserted in CI so overflow shows at wave one
state: wave 1 CLOSED — e1 and e2 gated PASS (31 checks) · engine 430/2400 · +162 lines ahead of plan
next: wave 2 — e3 `init+profiles` ∥ e4 `node verbs` ∥ e6 `status`, budgets 213 · 320 · 160

## SCOPE
In:  `add/scripts/add.py` (the engine) · its templates, profiles and method personas ·
     the ten verbs and their flags · red/green tests for every verb · the in-skill
     packaging that makes `python3 <skill>/scripts/add.py` work with zero install
Out: `SKILL.md` and its references (M2) · persona authoring beyond schema validation (M3)
     · the evals (M4) · `plugin.json` and the identity contract (M5) · any 2.5 migration

## GROUND
touches: `add/scripts/add.py` · `tests/engine/**` · `.add/**` (as the dogfood bundle)
anchors: FORMAT.md is frozen at v1.3-draft and the engine compiles against it, not around
  it · `scripts/validate_bundle.py` is the proven T0 parser and the conformance oracle —
  every rule it already enforces must still hold when the engine writes the bundle
honors: specs/system#decisions-that-bind (notary not guard · atomic single-file replace ·
  records but never executes · no undo, git is the log · every verb ends with `next:`) ·
  specs/method#decisions-that-bind (depth dial, authority ladder, T2 is single-node)
risks:
  - **A22 is specified, not implemented.** `e7` owes the content digest. Until then no
    receipt this engine writes can be trusted fresh across a checkout — the exact defect
    the M0 kill-test exposed
  - **A24 rests on test-ID extraction working in tools we do not control.** If
    `ids: unknown` is the common case in real runners, `e12` reopens A15
  - **P8 bites hardest here.** Every engine task's scope is the engine, and the engine is a
    sensitive path — so A17 pins all twelve to `human`. M1 either costs twelve human gates
    or P8 gets decided. Decide it with one gate's evidence in hand, not zero
  - a frontmatter writer that round-trips through a YAML serializer will silently strip the
    comments this bundle uses to carry rationale. Writes must be surgical, not regenerative

## EXIT
- [ ] ten verbs green, each built red-first, each ending in a `next:` line   (← every e-task)
- [ ] engine ≤ 2,400 lines **`wc -l`**, asserted in CI from wave one          (← build-durability)
- [ ] every per-task line budget is asserted in the SAME unit as the ceiling  (← amendment A1)
- [ ] cumulative consumed ≤ cumulative allocated at every gate                (← amendment A2)
- [ ] `.add/` in this repo is driven by the engine, not by hand              (← package-in-skill)
- [ ] `python3 add/scripts/add.py` runs from a clean checkout with zero install (← package-in-skill)
- [ ] every FORMAT rule the validator enforces still holds after the engine writes (← build-doctor)
- [ ] a receipt survives a fresh worktree checkout (A22 implemented, not just specified) (← build-receipts-learn)

## AMENDMENTS
### A1 · 2026-07-29 · line-budget rebase (human:tindang)
**What e1 found.** Not an overrun — a units error. e1 came in at **159 code lines against a
180-line allocation (88%)** and **245 total lines (136%)**. The allocation was a good estimate; it
was simply denominated in code lines, while the 2,400 ceiling is `wc -l` — the unit of the
8,948-line 2.5 anchor (`add.py` 6,600 + `add_engine/` 2,348). Nobody converted. Measured across all
twelve tasks the gap is **1,337 lines**, not the 65 the first reading suggested.

**Cuts pre-booked** (660 code lines; the overflow rule's order — surface first, never a law):

| cut | code | owner |
|---|---:|---|
| `--locate` dropped | 50 | e6 |
| `--graph` dropped | 70 | e6 |
| `status --since` dropped — R8's window is served by `log.md`'s date groups | 40 | e6 |
| `doctor` runs its checks over **e2's compiled graph** instead of building its own scan | 150 | e8 |
| `init` ships 2 profiles as code; the other 3 become template data | 80 | e3 |
| `new`/`freeze`/`done` share one node-transition path | 60 | e4 |
| `brief` renders from e2's compiled graph rather than its own traversal | 60 | e5 |
| evidence binding extracts test IDs from junit-xml only at v1.0 | 80 | e12 |
| `learn` appends to spec deltas without its own dedupe pass | 40 | e7 |
| durability tests reuse e1's atomic-write harness | 30 | e10 |

**Rebased budgets, in the ceiling's unit.** Verb modules are budgeted at **0.75 code/total**; e1
keeps 0.65 because its docstrings are the R:REGEN guard, not decoration.

| | e2 | e3 | e4 | e6 | e5 | e7 | e12 | e8 | e9 | e10 | e11 | sum |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| code | 260 | 160 | 240 | 120 | 200 | 180 | 120 | 150 | 60 | 60 | 60 | 1610 |
| **total** | **347** | **213** | **320** | **160** | **267** | **240** | **160** | **200** | **80** | **80** | **80** | **2147** |

e1 spent 245 + 2,147 = **2,392 against 2,400. The reserve is 8 lines.** That is not comfort; it is
a plan with no slack, and it should be read that way.

⚠ that verb modules can be written at 0.75 code/total — e1 ran 0.65. **If wave 2 lands at 0.65 the
plan is 322 lines over and a verb must go**, which is a D-2 change and needs its own decision.
`e2` tests this at the next gate.

**No task left scope, so no `status: dropped` node and no `needs:` propagation.** D-6 is untouched:
the ceiling did not move.

> **Corrected within the hour of writing.** The `e8` row first read "*reuses `validate_bundle.py`'s
> checks*". It cannot: the validator lives in `scripts/` as repo tooling, while the engine ships
> **inside the skill directory with zero install** and therefore may not import out of this repo.
> The real 150 lines come from `doctor` running over e2's compiled graph rather than building a
> second scan — same saving, sound mechanism. Caught by asking what `e8` would actually import.

### A2 · 2026-07-29 · the A1 falsifier was malformed; restated (human:tindang)
A1 predicted: *if wave 2 lands at 0.65 code/total the plan is 322 lines over and a verb must go.*
**e2 landed at exactly 0.65 — and the plan is 162 lines ahead.** The prediction fired while its
conclusion was false, because it silently assumed A1's code-line estimates were right. e2 needed
**120 code lines against 260 allocated**: it is thin glue over e1, not new machinery. Two wrong
parameters cancelled.

A1 is left **unedited** (§3.6 — amendments are recorded, never rewritten). It is superseded here.

**The restated falsifier — one measurable, checked at every gate:**

> cumulative lines consumed vs cumulative lines allocated for all gated tasks.
> **Trigger: consumed > allocated. Response: the next cut is a verb** (`--locate`, `--graph` and
> `status --since` are already spent by A1).

| after | allocated (cum.) | consumed (cum.) | margin |
|---|---:|---:|---:|
| e1 | 245 | 245 | 0 |
| e2 | 592 | 430 | **+162** |

Density is demoted to an observation. It is a ratio between two estimates and can never be a
trigger — that is the defect A2 exists to remove.

## STRATEGY
approach: dependency-first — nothing can be built before the thing that reads and writes a
  node, and nothing can be reasoned about before the graph compiles
freeze-first: `port-okf-parse` publishes the node I/O contract every other verb calls; it
  freezes before any verb is written
waves: (1) e1 parse ∥ — · (2) e2 graph · (3) e3 init ∥ e4 node-verbs ∥ e6 status ·
  (4) e5 brief ∥ e7 receipts → e12 evidence · (5) e8 doctor · (6) e9 hints ∥ e10 durability
  ∥ e11 packaging. Waves 3 and 4 are worktree-parallel — the first real use of L-E
tradeoffs: considered porting 2.5's `okf.py` (206 lines, proven) wholesale — rejected: it
  is coupled to `state.json` as truth, which is the exact thing L1 removes. Port its shape.
  Considered a third-party YAML parser — rejected: stdlib-only is a shipping constraint, and
  a full parser would round-trip away the comments this bundle depends on.

## CLOSE
evidence: <one row per task — <t-slug>: gate=<outcome> · checks=<n green> · residue=<none|note>>
census: <engine calls · briefs compiled and their bytes · receipts · human approvals · gates by outcome>
log: <the rotated `## YYYY-MM-DD` groups from log.md fold in here>
goal met: <restate the goal, and the one evidence line that proves the ship meets it>
