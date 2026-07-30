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
  - /tasks/build-gate-verb.md
  - /tasks/compile-checks-from-suite.md
  - /tasks/resolve-covers-grammar.md
depends_on:
  - /milestones/format-standard.md
generated: { by: claude/opus-5, at: 2026-07-29 }
ratified: []
amended:
  - { by: "human:tindang", at: 2026-07-29, authority: human, reason: "A1 line-budget rebase — the twelve per-task allocations were written in code lines while the 2,400 ceiling is wc -l. Re-derived in the ceiling's unit; 660 code lines of surface pre-booked as cuts. See ## AMENDMENTS" }
  - { by: "human:tindang", at: 2026-07-29, authority: human, reason: "A2 — A1's falsifier was a ratio between two estimates, so it fired at e2 while its conclusion was false. Restated as one measurable: cumulative consumed vs cumulative allocated, checked at every gate. A1 left unedited per §3.6" }
  - { by: "human:tindang", at: 2026-07-29, authority: human, reason: "A3 — restored --locate, --graph and status --since (~247 lines) into e6 after three consecutive under-runs left +301 margin; restated the invariant as consumed + remaining allocations <= 2400, because A2's was one-directional and generated no signal while winning" }
  - { by: "human:tindang", at: 2026-07-30, authority: human, reason: "A4 — three tasks added from an audit of hand-work across waves 2 and 3: gate (never existed, though D-2 counts it in the ten and all 11 gates were hand-appended through a private function), CHECKS compiled from the suite (F2s defect class made structurally impossible), and F1s covers grammar. 260 lines allocated; invariant 1956/2400, slack 444. See ## AMENDMENTS" }
verified: []
---
## CARD
goal: ten verbs, ≤2,400 lines, stdlib only, shipped inside the skill — and dogfooded here
shape: five waves; each wave's line budget is asserted in CI so overflow shows at wave one
state: e13 `gate` gated PASS by the GATE VERB — 8 of 10 verbs done · 161 checks · engine 1448/2400 · projected 2008/2400, slack 392
next: e14 `checks --sync` (90) — e13's CHECKS drifted 12→25 inside one build, which is e14's whole case

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
findings:
  - **F1 · spec/implementation mismatch, unresolved by design.** FORMAT §6.1 states the
    `covers:` grammar as `R:<CODE>`; `scripts/validate_bundle.py` encodes `R:[A-Z_]+`, which
    excludes digits. So `R:T2SCAN`, `R:T2FANOUT` and `R:MTIME2` raise `covers_referent` info
    while conforming to what the format actually says. One of the two is wrong. Left OPEN
    rather than fixed inline: both files are sensitive paths, and widening a grammar so the
    author's own nodes pass is the move A17 exists to prevent. Needs its own gated task
  - **F2 · 65 rules are LABELLED, not proven — measured by e12 on this bundle, 2026-07-30.**
    Binding every gated task's `covers:` labels against the set of check IDs that exist in the
    suites: **67 of 133 rules proven.** Of the 66 that are not, **65 are claimed by check IDs that
    do not exist anywhere**, across nine M0 tasks — `align-standards-citations` (6 fictional IDs),
    `define-authority-rules` (8), `define-compat-contract` (11), `define-entity-model` (5),
    `define-evidence-binding` (10), `define-log-rotation` (7), `define-read-protocol` (7),
    `define-scale-rules` (3), `define-task-schema` (5) — 61 distinct names in total. The remaining
    1 is an honest gap: a Must in `build-worked-example` with no `covers:` at all.
    Worked example: `define-entity-model` cites `test_minimum_bundle`; the suite contains
    `test_minimal_bundle_conforms`. The others cite tests never written.
    A second, worse shape sits inside the same finding: `define-scale-rules` has **no RULES
    section at all**, and its three checks cite `G1`/`G2`/`G3` — a rule-ID namespace FORMAT does
    not define. It declares proof over rules it never states, and the validator accepted it. So
    `covers:` is unchecked in both directions: neither the check nor the rule had to exist.
    **What is and is not wrong.** The M0 *rules* are sound and `validate_bundle.py` does enforce
    many of them — 18 real checks passed and M0's CLOSE openly declared that one shared receipt
    (`build-worked-example.d/runs/3.md`) earned the milestone, so the gate decision was defensible
    in intent. What was false is the narrower claim each node made in its CHECKS section: that
    *these named checks* proved *these numbered Musts*. The honest A24 kind for those nine tasks
    was `artifact-hash`, not `test-ids`.
    **Disposition (human:tindang, 2026-07-30): recorded, nothing reopened.** No gated node is
    rewritten — a gate was taken against those claims, and editing the claim afterwards erases
    what was accepted (R:ERASE, §3.6). M0 stays closed. This is A15's own finding, measured on the
    project that raised it, and it stands as the evidence for A15/A16 rather than as debt
  - **F3 · `run` writes a receipt and never binds it to the task — found 2026-07-30, at e12's
    gate.** `add.run` creates the Run node correctly and returns `next: add gate <slug>`, but
    appends nothing to the task's `verified[]`. That list is the ONLY thing `done()` and `since()`
    read, so the receipt exists on disk while the record of it existing does not. Every
    `process:pytest` / `process:run` stamp in this bundle — six of them, e1–e4, e6, e7 — was
    written by hand; e12's is the first that was not, which is how the gap became visible.
    Two consequences worth stating plainly: `status --since` under-reports every machine act, and
    this milestone's EXIT criterion "`.add/` is driven by the engine, not by hand" is **not yet
    met** on the receipt→stamp link, though it reads as though it were. The fix is a few lines
    inside `run`, and it is deliberately NOT being made here: `run` is e7's contract and e7 is
    gated. Assigned to `e8 build-doctor`, which must also carry the check that catches it —
    a task whose `verified[]` cites no receipt while `<slug>.d/runs/` is non-empty.
    Same function, same class, found at e5: the receipt dict `run` RETURNS omits `scope_digest`
    while declaring `freshness: content`, so a caller passing it to `fresh()` gets `False` with
    "no content digest". The receipt on disk is complete; the in-memory copy is not the receipt
  - **F4 · e1's parser has produced two silent value defects, and the fix for one caused a
    third — recorded 2026-07-30, decided: keep building.** In order: (a) `append_item` could not
    append to an inline `verified: []`, dropping every stamp on a fresh node (found by e4, after
    e1's 15 checks and a human gate); (b) a wrapped double-quoted list item was truncated at the
    first newline and kept its opening quote, silently losing the tail of a frozen `gives:` — live
    in `compile-graph` since e2, through 132 checks, the validator and five gates (found by e5
    RENDERING the value); (c) the first fix counted quote characters instead of scanning them, so
    one apostrophe swallowed `budget`/`generated`/`verified` across **25 nodes**, with 134 green
    and CONFORMS (found because `done` refused a transition it could not entitle).
    **The pattern, not the instances, is the finding.** All three were silent — no exception, no
    failing check, a plausible wrong value. Two oracles existed and neither could see them: the
    suite tests constructs it thought of, and the validator has an independent parser, so
    agreement between them proves nothing about either. What each defect had in common is that
    nothing asserted READ fidelity: `test_roundtrip_bundle_byte_identical` proves writes are
    lossless and is silent when a key vanishes from `fm` while the bytes stay perfect.
    That gap is now closed by `test_live_bundle_keys_all_parse` — every key present in a node's
    raw text must reach its parsed dict — which is the cheapest strong oracle this project has
    added, and would have caught all three. A deliberate parser audit was considered and NOT
    taken: the missing oracle was the actual defect, and it is now in place
  - **F5 · `new` has never substituted its template placeholder — found 2026-07-30.** `add.py`
    writes `BODIES` without `.format(slug=slug)`, so every node `new` has ever created carries a
    literal `{slug}` in its CARD `next:` line — a hint that would fail if run, which is R:FAKEHINT
    and a law-4 violation in the verb whose whole job is to teach the next command. It survived
    e4's 15 checks and a human gate because those asserted the node was created and parseable,
    never that its hint was runnable. I hand-wrote the real slug into all twelve M1 nodes while
    filling their CARDs and never noticed the cause. **Assigned to `e9 build-hints-layer`**, which
    already declares `R:FAKEHINT` and `test_hint_is_runnable` — the check was planned before the
    defect was found, which is the one encouraging thing about it
risks:
  - ~~**A22 is specified, not implemented.**~~ **RETIRED at e7, 2026-07-30.** `scope_digest`
    hashes git blobs over `scope:`; the M0 kill-test was run in reverse — `git worktree add`
    rewrote every mtime and the receipt still read FRESH, while a one-byte edit read STALE
  - ~~**A24 rests on test-ID extraction working in tools we do not control.**~~ **ANSWERED at
    e12, 2026-07-30.** `test-ids` is reachable: e12's own receipt earned it with 10/10 IDs from
    junit-xml. The residual risk is narrower than stated — junit-xml is the only supported format
    at v1.0 (A1's cut), so a runner that emits nothing parseable leaves every receipt at
    `command-exit`. That degradation is now honest and labelled, which is what A24 required
  - **P8 bites hardest here.** Every engine task's scope is the engine, and the engine is a
    sensitive path — so A17 pins all twelve to `human`. M1 either costs twelve human gates
    or P8 gets decided. Decide it with one gate's evidence in hand, not zero
  - a frontmatter writer that round-trips through a YAML serializer will silently strip the
    comments this bundle uses to carry rationale. Writes must be surgical, not regenerative

## EXIT
- [ ] ten verbs green, each built red-first, each ending in a `next:` line   (← every e-task)
      ↳ 8 of 10 gated: parse · graph · init · new/freeze/done · status · run/learn · brief · bind · gate
      ↳ remaining: `doctor` (e8) · the CLI surface (e11)
- [ ] engine ≤ 2,400 lines **`wc -l`**, asserted in CI from wave one          (← build-durability)
- [ ] every per-task line budget is asserted in the SAME unit as the ceiling  (← amendment A1)
- [ ] consumed + Σ(remaining allocations) ≤ 2,400 at every gate               (← amendment A3)
- [ ] `.add/` in this repo is driven by the engine, not by hand              (← package-in-skill)
- [ ] `python3 add/scripts/add.py` runs from a clean checkout with zero install (← package-in-skill)
- [ ] every FORMAT rule the validator enforces still holds after the engine writes (← build-doctor)
- [x] a receipt survives a fresh worktree checkout (A22 implemented, not just specified) (← build-receipts-learn)
      ↳ `test_receipt_survives_worktree`, gated 2026-07-30. mtime rewritten, digest unchanged, FRESH

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

### A3 · 2026-07-29 · restore the UX cuts; fix the invariant that kept them dead (human:tindang)
**Three under-runs in a row.** e1 245/245 · e2 185/347 · e3 74/213 — cumulative **504 consumed
against 805 allocated, +301**. A1 pre-booked 660 code lines of cuts to survive a units error that
turned out not to bind. Three of those cuts were user-facing, and they are precisely the surface
that answers 2.5's weakness #5, *user experience on gates and following AI work*.

**Restored** (~247 lines at the observed 0.65 density), folded into `e6`:

| restored | code | why it should not have died |
|---|---:|---|
| `--locate` | 50 | jump to a node by slug — goal 11, "slugs easy to look up" |
| `--graph` | 70 | render the milestone DAG — the only view of what the AI is doing |
| `status --since` | 40 | what changed since a point in time — R8, following AI work |

`e6 build-orient`'s budget: **160 → 407**.

**The invariant A2 stated was one-directional and therefore useless here.** "Consumed > allocated"
fires only when losing; three consecutive wins produced no signal at all, so the cuts stayed dead
by default rather than by decision. It is also gameable in the wrong direction — inflating an
allocation makes the trigger recede. Restated:

> **consumed + Σ(remaining allocations) ≤ 2,400**, checked at every gate.
> One number, symmetric, and it is the ceiling itself rather than a proxy for it. Slack that
> appears when a task lands under budget is *visible and spendable*, not silently banked.

| | value |
|---|---:|
| consumed (e1–e3) | 504 |
| remaining allocations (9 tasks, e6 now 407) | 1,834 |
| **projected total** | **2,338 / 2,400 — slack 62** |

D-6 untouched: the ceiling still has not moved. What moved is which side of it we can see.

### A4 · 2026-07-30 · three tasks added from a hand-work audit (human:tindang)
**What was audited.** Every action taken by hand across waves 2 and 3, against what the format says
is compiled and what D-2 says the engine does. Most of it was already planned: the CLI is `e11`'s
M2, and `index.md`/`log.md`/CARD compilation is `e8`'s `--sync`. Three things had **no owner**:

| gap | measured | new task | code |
|---|---|---|---:|
| `gate` does not exist as a verb, though D-2 counts it in the ten | all 11 gates so far were hand-appended through the private `_transition`; none of its 3 specified refusals ran | `build-gate-verb` | 140 |
| `run` writes a receipt no stamp points at (F3) | **8 of 18 receipts unreachable from the graph — 44% of all evidence** | (same task, M5) | — |
| `done` is not §3d's one-call quick lane | the lane the ceremony budget is measured against does not exist | (same task, M6) | — |
| CHECKS is authored, and F2 proved it fiction-prone | **118 of 131 tests already carry `covers:` in their docstring** | `compile-checks-from-suite` | 90 |
| F1 open since M0 — two documents, two grammars | 7 `covers_referent` info lines | `resolve-covers-grammar` | 30 |

**The invariant, recomputed** (A3): consumed 1,256 + remaining 700 (e8 200 · e9 80 · e10 80 ·
e11 80 · e13 140 · e14 90 · e15 30) = **1,956 / 2,400 — slack 444.** D-6 untouched: the ceiling has
still never moved.

**Why `build-gate-verb` matters more than its line count suggests.** e12's M3 says "`unbound` is
part of every gate's report". That rule was gated PASS while no gate report existed — it could not
have been true. The rule was not wrong; it had nowhere to land. This task is where it lands, and
until then every PASS in this project was recorded without the refusal that was supposed to guard it.

**What was NOT added, deliberately.** A `status --bind` census flag (e12's primitives plus e6's
report already compose it — a flag, not a task) and an `add commit-msg` compiler (it would author
prose from a node, which is the R:HANDBRIEF mistake pointed the other way).

## STRATEGY
approach: dependency-first — nothing can be built before the thing that reads and writes a
  node, and nothing can be reasoned about before the graph compiles
freeze-first: `port-okf-parse` publishes the node I/O contract every other verb calls; it
  freezes before any verb is written
waves: (1) e1 parse → e2 graph · (2) e3 init ∥ e4 node-verbs ∥ e6 status · (3) e5 brief ∥
  e7 receipts → e12 evidence · (4) e8 doctor · (5) e9 hints ∥ e10 durability ∥ e11 packaging.
  A4 adds: (3b) e13 gate · (4b) e14 checks ∥ e15 grammar
  <!-- Corrected 2026-07-30. This line read "Waves 2 and 3 are worktree-parallel — the first real
       use of L-E". They were not: both were built sequentially in one context, so L-E has never
       been exercised and the milestone asserted a practice the record does not support. The trial
       is now scheduled explicitly at 4b (e15 as a worktree subagent, decided with the human at
       wave 3's close) rather than described as already happening. -->
  <!-- Renumbered 2026-07-29: this line first read six waves (e1 and e2 separately) while
       amendment A1's table read five. Two numbering schemes for one plan is a defect, not a
       viewpoint. A1's numbering wins because it is the one CI asserts the line budget against. -->

## CLOSE
evidence: <one row per task — <t-slug>: gate=<outcome> · checks=<n green> · residue=<none|note>>
census: <engine calls · briefs compiled and their bytes · receipts · human approvals · gates by outcome>
log: <the rotated `## YYYY-MM-DD` groups from log.md fold in here>
goal met: <restate the goal, and the one evidence line that proves the ship meets it>
