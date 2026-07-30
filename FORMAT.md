---
type: Spec
title: ABF-1 — the ADD Bundle Format, version 1.3-draft
description: >-
  The format standard for ADD-SKILL: an OKF v0.2 profile with declared extensions, where
  files are the database, everything derivable is compiled (never hand-maintained), every
  read has a declared token tier, and a gate is bound to the specific checks a receipt
  observed. Successor to AIDD-Book's state.json-centric .add/ layout.
status: draft
version: 1.3-draft
supersedes: FORMAT.md@1.2-draft (2026-07-29 — amendments A22–A24 landed; the mtime freshness assumption was tested and replaced)
generated: { by: claude/opus-5, at: 2026-07-29 }
relates_to: [ /PROPOSAL.md ]
---

# ABF-1 — ADD Bundle Format v1.3 (draft)

ABF-1 is a **profile of Open Knowledge Format v0.2**
(`github.com/GoogleCloudPlatform/knowledge-catalog/okf/SPEC.md`) plus **five declared
extensions**: a typed atomic task graph, a fragment grammar, an evidence-binding rule, a
frozen node interface, and a content-addressed freshness predicate.

The task graph is **informed by** the Atomic Task Graph model (arxiv 2607.01942). Two
claims, each cited and each bounded (A19):

- **Node shape.** ATG §3 defines a node as `v_j = (i_j, f_j, o_j)`, where *"f_j ∈ 𝒯 is the
  selected tool, i_j is its input, and o_j is its output"* — an ATG node is **one concrete
  tool call**. ABF's `needs` / work / `gives` is the same triple raised one altitude: the
  unit is a work item a human or agent completes, not a single call.
- **Repair.** ATG §4.3 (*Minimal Necessary Subgraph Repair*) locates *"the smallest ancestor
  node from which the failed region was derived"* and repairs *"only this subgraph … by
  replacing incorrect tools, inserting missing nodes, or adjusting local dependencies."*
  ABF adopts the localisation rule and adds a constraint ATG does not state: **a node's
  `gives:` is frozen, so repair may replace internals but never the external interface**
  (§3.5). That constraint is an ABF extension, listed in §12.

> **Honesty about the OKF relationship (A9).** ABF-1 is *OKF plus declared extensions*,
> not pure OKF. Section 12 lists every extension and where OKF is silent. A generic OKF
> consumer reading an ABF bundle sees conformant documents with unknown optional keys and
> some links it cannot resolve — which OKF §11 requires it to tolerate. Nothing here asks
> OKF to mean something it does not say.

## 0 · The governing laws

1. **Files are the database.** Every entity is exactly one markdown file with OKF
   frontmatter. There is no authoritative `state.json`. The graph index (`graph.json`) is
   a *compiled cache* — regenerable from frontmatter at any time, gitignored, never
   hand-edited, never trusted over the files.
   *Evidence:* AIDD 2.5's `state.json`-as-truth required merge-conflict detection,
   forward-migration code, and doc↔state reconciliation — a whole failure class that
   disappears when the files ARE the state.
2. **Every read has a tier.** Frontmatter (T0) → CARD section (T1) → full body (T2). An
   agent never reads T2 of a node it is not actively working. This is the context-rot
   protection and the token method, enforced by format rather than by discipline.
3. **Notary, not guard** (OKF §11). Unknown keys, unknown types, and broken links are
   recorded findings, never rejections. Only a containment escape (`edge_out_of_bundle`)
   is fatal. *Verbatim from the source:* "Consumers MUST NOT reject a bundle because of:
   Missing optional frontmatter fields. Unknown `type` values… Broken cross-links."
4. **The bundle is authored content; everything else is data (A14).** A compiled brief may
   present bundle nodes as instructions. Repo source, command output, and fetched
   documents enter a brief **only** inside `<evidence>`, quoted, and are never presented
   as instructions.
5. **Compiled beats authored (A20).** Any fact derivable from node frontmatter is
   *rendered*, never hand-maintained: `graph.json`, `index.md`'s body, `log.md`, seams, the
   milestone census, the review packet. Two consequences, and both are the point: a
   compiled artifact cannot go stale, and it has no concurrent writers — which is what lets
   N agents work N nodes in N worktrees without a shared file to conflict on.
   *Evidence:* within one day of hand-authoring, this bundle at 20 nodes carried three
   contradictions between an authored summary and the nodes it summarised. Authored
   duplicates rot at a rate that does not depend on discipline.

Two engine-level laws bind this format at one point each: every verb's output ends with a
`next:` line (§7.4, A6), and the engine records evidence but never executes a command of
its own initiative (§8.2, A3).

## 1 · Bundle layout

```
.add/                          # the OKF bundle root
  index.md                     # RESERVED — bundle config in frontmatter + a COMPILED body
                               #   (A11). Frontmatter: okf_version "0.2" · abf_version
                               #   "1.3" (the skill's branch key — absent ⇒ a pre-ABF
                               #   bundle) · optional sensitive_paths (A17) ·
                               #   optional persona_corpus. Body: a grouped concept TOC,
                               #   regenerated by the engine, never hand-maintained.
  log.md                       # RESERVED — journal, newest first, entries grouped under
                               #   ISO `## YYYY-MM-DD` headings (A10, OKF §9). COMPILED
                               #   from node `verified[]` stamps and `generated.at` (A20)
                               #   — one line per freeze / gate / close / open, each
                               #   traceable to the stamp that produced it. A trailing
                               #   `## Notes` section is human-owned and preserved
                               #   verbatim. Rotates by whole date groups at close (A4).
  PROJECT.md                   # type: Project    (1 per bundle)
  specs/
    domain.md                  # type: Spec  lens: ddd — what the system IS
    system.md                  # type: Spec  lens: sdd — how it is built
    experience.md              # type: Spec  lens: udd — how it feels to use
    quality.md                 # type: Spec  lens: tdd — how we know it works
    method.md                  # type: Spec  lens: add — how we work
  milestones/<m-slug>.md       # type: Milestone  (single file per milestone)
  tasks/<t-slug>.md            # type: Task       (single file = one atomic node)
  tasks/<t-slug>.d/            # OPTIONAL sidecar dir, created only when a task
    runs/<n>.md                #   accrues assets: runs (type: Run), design files
  personas/<p-slug>.md         # type: Persona — PROJECT-authored lenses only; starts
                               #   empty (method personas ship in the installed package)
  prompts/<name>.md            # type: Prompt — project OVERRIDES only; starts empty
                               #   (default templates ship in the installed package)
  graph.json                   # DERIVED cache — gitignored, rebuilt on demand
  .gitattributes               # A23 — declares the compiled files to git so a merge
                               #   resolves without a hand-edit. Written by `init`.
```

### 1.1 · Compiled files and merge (A23)

Law 5 removes concurrent *writers*. It does not remove *merge* conflicts: `index.md`'s body
and `log.md` change on both sides of any parallel wave that is later merged, and both are
committed. The resolution is stated in the bundle rather than left to whoever hits it:

```gitattributes
index.md merge=ours linguist-generated=true
log.md   merge=ours linguist-generated=true
```

`merge=ours` is a **built-in** git driver — no configuration, no install step, which is what
keeps it compatible with "drop the directory in place". On conflict git keeps the local side
and the truth is restored by `add doctor --sync`, because both files are derived: whichever
side survives the merge is equally wrong and equally repairable.

**The rule generalises:** every compiled file declares itself. Its body opens with a
`<!-- COMPILED BODY` marker naming the amendment that owns it, and `.gitattributes` lists
it. A compiled file that declares neither is a `compiled_undeclared` finding — a human who
hand-edits it will lose the edit at the next `--sync`, and the format's job is to say so
before that happens rather than after.

Flat `tasks/` plus a `milestone:` key (rather than nesting tasks under milestone
directories) keeps concept IDs stable when a task is re-homed, and keeps a short-scope
project to **three files total**: `index.md`, `PROJECT.md`, one task.

**Concept ID** = the bundle-relative path with `.md` removed (OKF **§2, Terminology**):
`tasks/add-auth-token`.

**Slug** = the filename stem: kebab-case, ≤ 4 words, unique per type, verb-first for tasks
(`add-auth-token`), noun-first for milestones (`auth-layer`). Lookup is therefore
mechanical — a slug resolves from the filename before any frontmatter is parsed.

**Reserved files.** `index.md` and `log.md` carry no `type:` and are exempt from the
`type_empty` finding.

## 2 · The closed `type:` vocabulary

| type | one per | required keys | purpose |
|---|---|---|---|
| `Project` | bundle | `type, title, goal` | direction of the whole bundle |
| `Milestone` | file | `type, title, goal, status` | one user-request scope (a wave) |
| `Task` | file | `type, title, goal, status` | one atomic graph node |
| `Spec` | 5 fixed files | `type, title, lens` | a living 5-DD lens document |
| `Persona` | file | `type, name, vibe` | a reasoning lens for a decision point |
| `Prompt` | file | `type, title, fills` | a parametric XML prompt template |
| `Run` | file | `type, runtime, receipt` | evidence record from a command that executed |

The set is closed **for authoring**, not for reading: an unknown `type:` is an `info`
finding and still compiles into the graph (law 3).

**`Run` is a result record, not an OKF Attested Computation (A9).** OKF §10 defines
`type: Attested Computation` as the *definition* of a sanctioned computation (`runtime`
REQUIRED, plus `parameters` / `computation` / `executor` / `attester`), and explicitly
leaves the result record producer-defined: *"`receipt` declares the fields a run must
return."* ABF's `Run` is exactly that producer-defined result. A bundle MAY additionally
publish `Attested Computation` concepts for reproducible gates; ABF does not require it.

`Prompt` and `Run` are new relative to AIDD 2.5's five types. Everything else carries over
unchanged — proven vocabulary is not renamed.

## 3 · The task node — ATG-aligned schema

```yaml
---
type: Task
title: Reject overlapping bookings per user
goal: a second booking overlapping an existing one returns 409 OVERLAP
status: todo | direction | build | verify | done | dropped
depth: quick | standard | deep          # the ceremony dial — §6
kind: feature | fix | refactor | test | docs | ui | security | data | infra | integration
sensitivity: mechanical | data | architecture | security     # pins the authority floor
milestone: /milestones/auth-layer.md    # optional — quick tasks may be milestone-less
depends_on:                             # ATG edges: their `gives` may feed my `needs`
  - /tasks/add-auth-token.md
needs:                                  # interfaces consumed (i in ATG's (i, f, o))
  - /tasks/add-auth-token.md#gives      # a frozen fragment of a neighbour
gives:                                  # interface produced (o) — FROZEN at freeze
  - "POST /bookings -> 409 OVERLAP on user-overlap"
scope:                                  # paths this task may touch; the freshness set (§8.1)
  - src/bookings/**
generated: { by: claude/fable-5, at: 2026-07-29T08:00:00Z }
verified:                               # OKF §5.2 trust family; ABF adds `act` and `authority`
  - { by: "human:tindang", at: 2026-07-29T09:00:00Z, act: freeze, authority: human }
  - { by: "process:pytest", at: 2026-07-29T10:00:00Z, act: gate, authority: process,
      outcome: PASS, receipt: /tasks/overlap-reject.d/runs/2.md,
      brief: "sha256:9f2c…" }          # A16 — the brief that drove the work
---
## CARD                                  # T1 — ≤ 10 lines, the ONLY cross-node read
<goal restated · the contract shape · scope tokens · current beat + next action>

## RULES                                 # Must / Reject / After, plus the ONE ⚠ assumption
## PLAN                                  # contract detail · strategy · scope · floor
## CHECKS                                # red suite: one check per Must/Reject, `covers:` keys
## EVIDENCE                              # receipt links · gate outcome · scope check
## LESSONS                               # deltas emitted -> `add learn <lens>`
```

**Atomicity guarantee (ATG).** Rebuilding a task may change anything in its body, but its
frontmatter `gives:` is its external interface — frozen at the freeze stamp. Any change to
it is a *change request* that reopens direction. A failing check resolves to its owning
node and the minimal repair subgraph (the node, plus dependents whose `needs:` cite its
`gives`).

### 3.1 · Authority (A1)

Every `freeze` and `gate` stamp carries an `authority:` value from a closed ladder:

| authority | means | who may stamp it |
|---|---|---|
| `human` | a person approved this node, now | a human, per task |
| `plan` | a human ratified the milestone that contains this node | derived from the milestone's `ratified:` stamp |
| `ai-verify` | a second model reviewed and found no objection | a headless verify pass |
| `process` | evidence alone: a green, fresh, covers-bound receipt | the engine |

Ordering: `human` > `plan` > `ai-verify` > `process`.

**`sensitivity:` pins the minimum, unstrikeably:**

| sensitivity | minimum authority |
|---|---|
| `mechanical` | `process` |
| `data` | `plan` |
| `architecture` | `plan` |
| `security` | `human` — never batched, never derived |

**Sensitive-path floor (A17).** If any entry in a task's `scope:` matches a pattern in
`index.md`'s `sensitive_paths:`, the floor is raised to `human` regardless of the declared
`sensitivity:`. This is a path match, not a judgement, so a notary may perform it.

**Ratification is bounded.** A milestone's `ratified:` stamp pre-approves exactly the
tasks listed in its `tasks:` key **at the moment of the stamp**. A task added afterwards is
not pre-approved and needs its own authority. Without this bound, "ratify the milestone"
would be a blank cheque against work nobody has seen.

> **Change of record (2026-07-29).** v1.0-draft and the bundle's `specs/method` held that
> `data | architecture | security` each require a per-task **human** freeze. Landing A1
> showed that rule makes `plan` and `ai-verify` unreachable in practice and blocks every
> headless run on routine data work. The refined table above keeps human approval for all
> three — batched through ratification for `data`/`architecture`, per-task for `security` —
> and the ratification bound above is what makes the batching safe. Recorded here rather
> than changed silently.

### 3.2 · The milestone node

```yaml
---
type: Milestone
title: Auth layer
goal: every booking endpoint refuses an unauthenticated caller with 401   # required
status: queued | active | done | dropped
stage: prototype | poc | mvp | production
depth: quick | standard | deep
tasks:                        # MEMBERSHIP — refs, unresolved allowed pre-creation
  - /tasks/add-auth-token.md
  - /tasks/overlap-reject.md
depends_on: []                # cross-milestone edges only
ratified: []                  # { by, at, authority, tasks: <count at stamp> }  (A1)
amended: []                   # { by, at, authority, reason } — a scope change (A21, §3.6)
---
## CARD                        # T1 — goal restated · wave shape · current state
## SCOPE                       # In: … / Out: … (the anti-scope-creep list)
## GROUND                      # A8 — gathered ONCE: shared touches · anchors · honored
                               #   decisions · shared risks. Tasks PROJECT from this and
                               #   never re-ground the repository.
## EXIT                        # observable criteria, each mapped to the task that delivers it
## STRATEGY                    # depth: deep only — approach · freeze-first · waves · tradeoffs
## CLOSE                       # at done: per-task evidence rollup · the census (A18) ·
                               #   rotated log groups (A4) · goal-met verdict
```

One source per fact: the milestone owns *membership, ground, and exit criteria*; each task
owns *its own edges*. The graph compiles from both; a `tasks:` ref whose file never appears
stays an `edge_unresolved` info finding.

**The census (A18).** At close, `CLOSE` carries the engine's own rollup: engine calls,
briefs compiled and their byte sizes, receipts recorded, human approvals requested, and
gates by outcome. This is what makes a ceremony budget a measured number on real projects
rather than only inside an eval harness.

**Todo capture.** A todo writes a stub task node — auto-slug, `status: todo`, the text as
`goal:`, no body beyond CARD. Graph-visible from birth, T0-cheap (~10 lines), promoted in
place by filling sections; never a second format.

### 3.3 · Edges and the fragment grammar (declared extension, A9)

`depends_on` / `needs` / `gives`-refs are ABF extension keys, legal under OKF §11. Values
follow OKF §6: bundle-absolute (`/tasks/x.md`) or relative — optionally with a `#fragment`.

> **OKF §6 does not define fragments.** The grammar below is an **ABF extension owned by
> the ABF resolver**. A generic OKF consumer is entitled to treat `/tasks/x.md#gives` as a
> link it cannot resolve, and OKF requires it to tolerate that. No conformance claim is
> made on OKF's behalf.

**The grammar is closed, two namespaces, no ambiguity.** A fragment resolves against:

1. the target's **frontmatter key** (`#gives`, `#goal`) — the value is injected verbatim;
2. and only if no such key exists, the **body heading slug** (`#decisions-that-bind` → the
   `## Decisions that bind` section), where a heading slug is the kebab-cased heading;
3. matching neither → `edge_unresolved` (severity `info`).

Frontmatter wins even when a same-named heading exists — the rule is ordered, so one
reference can never resolve two ways. An edge escaping the bundle is `edge_out_of_bundle`
(severity `error`) — the only fatal finding class.

### 3.4 · Activity is derived, never pointed at

ABF-1 has no `active_task` / `active_milestone` pointer. A node is *active* iff its
`status` is `direction | build | verify`. Resume is a T0 scan for active nodes; several may
be active at once (parallel agents in worktrees), and closing one can never corrupt a
shared pointer.

**Build progress is read from git, not stored.** For a node in `status: build`, progress is
`git status --porcelain` intersected with the node's `scope:`. Read-only, always current,
and it invents no state that could disagree with the tree.

### 3.5 · Frozen-interface evolution

A change request against a frozen `gives:` is recorded, never edited in place: the new
shape lands with a `verified: { act: refreeze, by, at, authority }` entry — the old entry
stays, because history is append-only. Every node whose `needs:` cite the changed fragment
is flagged **stale** and must re-verify before its next gate. This is ATG's repair rule
made mechanical: internals may change freely; an interface change propagates as explicit,
bounded re-verification of the dependents.

### 3.6 · Milestone amendment — when the human changes their mind (A21)

§3.5 governs a frozen *task* interface. A milestone's **scope** is the other thing that
changes mid-flight, and it changes for the most legitimate reason there is: the person who
asked for the work now wants something different. That is a recorded event, never a silent
edit.

| step | rule |
|---|---|
| **record** | append `amended: { by, at, authority, reason }`. The authority floor is the milestone's own `ratified:` authority — re-scoping cannot be cheaper than approving |
| **remove** | a task leaving scope moves to `status: dropped` and keeps its node and its reason. Nodes are never deleted; the graph's history is the audit trail |
| **exit** | `EXIT` criteria are **append-only**. A criterion that no longer applies is struck through with its amendment date, never removed — otherwise a milestone can be made to have met a goal it never met |
| **propagate** | any node whose `needs:` cite a dropped task's `gives:` is flagged **stale** and must re-verify before its next gate — the §3.5 rule, applied to a removal instead of a change |
| **ratification** | a prior `ratified:` stamp does **not** extend to tasks added by an amendment (§3.1's bound). New membership needs new authority |

An amendment that drops every remaining task is a milestone `status: dropped`, with its
`CLOSE` recording what was learned. A cancelled milestone with a written reason is a
result; a silently abandoned one is a leak.

## 4 · Read protocol — the token method as format

| tier | what is read | cost/node | when |
|---|---|---:|---|
| **T0** | frontmatter only (or `graph.json`) | ~50 tok | orientation, status, DAG walks |
| **T1** | + `## CARD` | ~150 tok | planning a milestone, picking the next task |
| **T2** | full body | ~1–3k tok | ONLY the active node + `#gives` fragments of direct deps |

The rule an agent and every compiled brief must honour: **T2 is single-node.** Context for
a task = its own body + T1 cards of `depends_on` + the `Decisions that bind` section of
relevant specs + the persona's frontmatter. Nothing else, ever, by default.

### 4.1 · Scale rules (A12)

T0 is cheap per node and not free in aggregate. A bundle that runs for six months must not
become the context hazard this format exists to prevent:

- default scans **exclude** `status: done | dropped`; an explicit flag includes them;
- orientation output prints at most **20 node lines** plus a count;
- graph rendering is **per milestone**, never whole-bundle by default;
- `log.md` rotates by whole date groups at milestone close (A4), its lines folding into
  that milestone's `CLOSE`.

## 5 · Specs — five lenses, wide domains

The five files are fixed (a closed competency model: DDD · SDD · UDD · TDD · ADD); their
*contents* are domain-profiled. Every spec has the same three sections:

```
## Now                    # the standing picture — state, not history
## Decisions that bind    # one line each — the ONLY spec section a brief may cite
## Deltas                 # inbox, newest first; a lesson prepends here
```

A domain profile seeds domain-fitted `Now` skeletons (e.g. `experience.md` for a library is
its public API surface; for a pipeline, its operator's runbook view). The lens set never
changes; the skeleton does. This is what makes the five specs flexible across domains
without an open-ended taxonomy.

**The specs absorb 2.5's foundation files** — one home per fact: GLOSSARY → `domain.md`;
CONVENTIONS, dependency allowlists, model registries → `system.md` under *Decisions that
bind*; DESIGN → `experience.md` (heavy assets in a sidecar dir); voice → a human-owned
section of `PROJECT.md`. Init scaffolds **8 files**: `index.md` · `log.md` · `PROJECT.md` ·
the five specs.

**Learning loop.** Deltas land the moment a lesson is learned; at task or milestone close,
open deltas fold up into `Now` / `Decisions that bind` and are retagged `[folded]`. The
specs stay current, and the *next* loop reads a smaller, truer picture. Evidence for the
fold is the delta's task backlink.

## 6 · Depth — one template, three ceremonies

| depth | body sections | engine calls (task lifetime) | gate |
|---|---|---:|---|
| `quick` | CARD · CHECKS · EVIDENCE | **1** (compound create+freeze+gate with receipt) | auto on a green, covers-bound receipt; sensitivity floor still applies |
| `standard` | all six | ≤ 3 + one `run` | auto on evidence at `process` authority, unless the floor is higher |
| `deep` | all six + milestone STRATEGY | ≤ 3 + one `run` + milestone verbs | human freeze; lowest-confidence-first ordering |

*Why:* the 2.5 benchmark showed the fidelity premium is real (0.97 floor) but WM1 cost 251
engine calls / 12.85M tokens against spec-kit's 1.11M. Ceremony becomes proportional to the
request **by format**, not by agent judgement alone.

### 6.1 · What `covers:` refers to, by depth

A `covers:` key names the rule a check exists to enforce. At `quick` depth there is no
RULES section, so the referent is defined explicitly:

| depth | legal `covers:` referents |
|---|---|
| `quick` | `goal`, or `G<n>` — the nth entry of `gives:` |
| `standard` · `deep` | `M<n>` (a Must) or `R:<CODE>` (a Reject) |

The table above is prose for a reader. **This block is the grammar**, and it is the only
statement of it — every oracle enforces these exact patterns, and a check holds them equal:

```covers-grammar
quick           = \A(goal|G\d+)\Z
standard | deep = \A(M\d+|R:[A-Z0-9_]+)\Z
```

*Why a fenced block and not prose (F1, resolved 2026-07-30).* §6.1 previously stated only the
metavariable `R:<CODE>` and expanded `<CODE>` nowhere in this document. A metavariable cannot be
compared to a regex, so no implementation could be held to §6.1 as written — and two did drift,
the validator to `R:[A-Z_]+` and the engine to `R:[A-Z0-9_]+`. The disagreement was never between
two grammars; one side had never stated one. A grammar with no machine-readable address cannot be
kept in step with a second oracle, so it will not be.

**Red-first is not claimed at `quick` depth.** One engine call cannot produce a
pre-build receipt, so a quick-lane receipt records `red_first: unproven` rather than
implying evidence it does not have.

## 7 · Prompts and briefs — parametric XML, refs not prose

`prompts/<name>.md` bodies are XML skeletons; a brief compiles the fill mechanically from
the graph:

```xml
<task id="tasks/overlap-reject" phase="build" depth="standard">
  <objective>{{goal}}</objective>
  <persona ref="personas/task-planner" inject="frontmatter"/>  <!-- body on demand -->
  <context>   <!-- refs resolved at BRIEF time — spec changes never break prompts -->
    <ref id="tasks/add-auth-token#gives" frozen="true"/>
    <ref id="specs/system#decisions-that-bind"/>
    <card id="tasks/session-store"/>                            <!-- T1 only -->
  </context>
  <constraints>never weaken a check · never edit a frozen gives · scope: {{scope}}</constraints>
  <evidence require="run-receipt"/>
</task>
```

### 7.1 · Injection is by reference, not inclusion

A brief resolves refs against the *current* bundle, so changing a spec re-scopes every
future prompt with zero prompt edits. A brief that copies spec prose into its body is a
defect, not a style choice — it is what makes scope changes expensive.

### 7.2 · Budget (A5)

A brief declares a byte ceiling per depth and cannot silently exceed it. On overflow it
degrades to T1 refs **and reports the degradation** in its own output. A silent overflow
reinstates the context cost the tier system exists to remove.

### 7.3 · Determinism and hash (A16)

Given the same bundle state, node, and phase, a brief compiles **byte-identically**: refs
resolve in sorted, stable order. Every brief prints a content hash, and the gate stamps the
hash of the brief that drove the work (§3, `verified[].brief`). This closes the provenance
chain — *these instructions produced this code, which earned this gate* — and it is what
makes parallel subagent work auditable rather than merely fast.

### 7.4 · The affordance contract (A6)

Every verb's output ends with a `next:` line naming the exact next command and the cheapest
legal lane. This is a format-level requirement because it is the measured difference
between 0% and immediate adoption of every other mechanism here: in the 2.5 pilot,
features documented only in guides got zero uptake, while the same feature named in the
engine's own output went 0 → 12 uses and cut milestone tokens 29% at identical fidelity.

### 7.5 · The trust boundary (A14, law 4)

Bundle nodes compose as instructions. Repo source, command output, and fetched documents
enter a brief **only** inside `<evidence>`, quoted and labelled with their origin. A brief
never inlines a file from outside the bundle as instruction.

## 8 · Evidence — Run receipts

A gate is earned by a receipt, never by a claim:

```yaml
---
type: Run
runtime: pytest
task: /tasks/overlap-reject.md
computation: "python -m pytest tests/test_overlap.py -q --junitxml=…"
receipt:
  kind: test-ids                       # A24 — what kind of observation this is
  exit: 0
  passed: 14
  failed: 0
  checks:                              # A15 — the observed test IDs and their outcome
    - { id: test_overlap_rejects, outcome: pass }
    - { id: test_overlap_allows_adjacent, outcome: pass }
  ids: parsed                          # parsed | unknown
  red_first: proven                    # proven | unproven
  freshness: content                   # A22 — content | mtime
  scope_digest:                        # A22 — the freshness set, sorted by path
    - { path: src/bookings/service.py, blob: "sha1:4f2a…" }
  at: 2026-07-29T10:00:00Z
generated: { by: process:pytest, at: 2026-07-29T10:00:00Z }
---
```

### 8.0 · Evidence kinds (A24)

`covers:` binds a rule to an **observation**. A parsed test ID is the strongest kind of
observation and it is not the only one: two of the six shipped domain profiles (`doc`,
`ui-app`) routinely have no test runner, and a format in which those degrade to
`ids: unknown` by default has made its central check decorative exactly where it is hardest
to satisfy.

Every receipt declares its `kind:`, and each kind states what it proves and what it does not:

| kind | the observation | `covers:` binds to | red-first provable? | what it does NOT prove |
|---|---|---|---|---|
| `test-ids` | named tests ran and passed | a check ID present in `checks:` with `outcome: pass` | **yes** | that the test asserts the right thing |
| `command-exit` | a command exited 0 | the command as a whole; the receipt records `ids: n/a` and the gate carries `covers_coarse` | yes | *which* rule the command exercised — one exit code cannot distinguish two Musts |
| `artifact-hash` | a named artifact exists and hashes to a recorded value | the artifact path + digest (a rendered page, a generated schema, a built binary) | no | that the artifact is *correct* — only that it is the one that was reviewed |
| `human-observed` | a person states they saw the behaviour | the observer, the rule, and the date | no | anything reproducible. It requires `authority: human`, is never derived, never batched, and never applied to `sensitivity: security` in place of a test |

**The ordering is `test-ids` > `artifact-hash` > `command-exit` > `human-observed`**, and a
gate records the kind it accepted. A weaker kind is a *visible* weakening — which is the
whole point, and the same principle as `covers_unverified`: the format never chooses between
lying and refusing.

`init --profile` seeds a default kind: `test-ids` for `api-service` · `library` · `cli-tool`
· `data-pipeline`; `artifact-hash` for `doc`; `artifact-hash` with `human-observed` allowed
for `ui-app`. A task may declare a stronger kind at any time and never a weaker one than its
`sensitivity:` floor permits.

### 8.1 · Freshness (A2, A22)

A receipt is **fresh** when the code it observed is the code that exists now. A stale
receipt cannot earn a gate. This kills the stale-green failure — tests that passed before
the last edit — and it makes "same-session receipt" mechanical instead of honour-system.

**The predicate is content-addressed (A22).** A receipt records, per file matching the
task's `scope:`, the git blob hash of that file at run time:

```yaml
receipt:
  freshness: content            # content | mtime
  scope_digest:                 # sorted by path; the freshness set
    - { path: src/bookings/service.py, blob: "sha1:4f2a…" }
    - { path: src/bookings/models.py,  blob: "sha1:9c01…" }
```

A gate recomputes the digest and refuses on any difference. A file that has appeared in
`scope:` since the run is a difference; so is one that has vanished.

**Fallback, declared rather than silent.** Outside a git working tree the receipt records
`freshness: mtime` and the old rule applies — any in-`scope:` mtime later than the
receipt's `at` makes it stale. A receipt always states which predicate it used, because a
gate that cannot tell which one it trusted is a gate that trusts neither.

> **Why the change (recorded, not applied silently).** 1.1-draft used mtime alone and
> carried a ⚠ saying so. The assumption was tested and it failed: `git worktree add` sets
> *every* checked-out file's mtime to checkout time, so in any fresh clone, worktree, or CI
> job, a committed receipt reads stale against files it genuinely observed. The failure is
> deterministic, and it lands hardest on exactly the two designs this format promotes —
> parallel worktree fan-out, and conformance checks running in CI on a clean checkout.
> mtime measures *when a file was written to this disk*; freshness is a question about
> *content*. The predicate was isolated for this, and this is the replacement.

⚠ **The new recorded assumption:** hashing the `scope:` set stays cheap. A `scope:` glob
matching hundreds of files costs a read of each. If that dominates, the digest moves to
the git index entries (`git ls-files -s`), which git already maintains — the predicate
stays isolated for the same reason it was isolated before.

### 8.2 · The engine records; it never executes (A3)

The engine executes only the command its caller passes on the command line, and captures
the result. **No `computation:` string read from a node is ever executed.** A notary that
executes arbitrary strings from files is an execution surface, and it would let a gate pass
without anyone having run anything.

### 8.3 · Evidence binding — `covers:` is a binding, not a label (A15)

Two distinct checks, at two distinct moments:

| moment | check | failure |
|---|---|---|
| **freeze** | every `M<n>` and `R:<CODE>` in RULES appears in at least one check's `covers:` | refuse to freeze: a rule encoded in no check means the rules are not understood |
| **gate** | every check ID listed in CHECKS appears in the receipt's `checks:` with `outcome: pass` | refuse the gate: `covers:` names a check that did not demonstrably pass |

**Degradation is explicit.** When test IDs cannot be extracted from the runner's output,
the receipt records `ids: unknown`, and the gate proceeds carrying a `covers_unverified`
finding rather than refusing. A visible weakening beats a silent one; a refusal on
un-parseable output would make the format hostage to one test runner's formatting.

**Red-first is earned (A15).** `red_first: proven` requires a *prior* receipt on the same
task in which at least one of the same check IDs failed. Absent that, the receipt records
`red_first: unproven`. Red-first stops being a self-report.

### 8.4 · Trust tiers

Derived from OKF §5: no `verified` entry → unverified · a `process:` actor → machine-
confirmed · a `human:` actor → human-reviewed. The `authority:` value (§3.1) records *who
was entitled to approve*; the receipt records *what was observed*. Both are needed: an
authority without evidence is an opinion, evidence without an authority is an orphan.

## 9 · Conformance

Two severities only. A bundle **conforms** iff it has zero `error` findings.

| code | severity | meaning |
|---|---|---|
| `missing_frontmatter` | error | a `.md` node with no parseable YAML frontmatter |
| `type_empty` | error | frontmatter with no non-empty `type:` (reserved files exempt) |
| `edge_out_of_bundle` | error | a link escaping the bundle root — the containment escape |
| `edge_unresolved` | info | a link or fragment with no target (a wave may be sketched first) |
| `unknown_type` · `unknown_key` | info | law 3 — recorded, never rejected |
| `broken_md_link` | info | OKF §6 requires tolerance |
| `covers_unverified` | info | a gate passed with `ids: unknown` (§8.3) |
| `covers_coarse` | info | a gate passed on a `command-exit` receipt — the rule is bound to a command, not to a named check (§8.0) |
| `compiled_undeclared` | info | a compiled file missing its `COMPILED BODY` marker or its `.gitattributes` entry (§1.1) |
| `receipt_stale` | info | a receipt whose scope digest no longer matches (the *gate* refuses; the scan reports) |
| `placeholder_survived` | info | an unfilled `<placeholder>` past freeze |

**A gate refusal is not a conformance finding.** Refusals (stale receipt, unmet `covers:`,
authority below the floor) are decisions made at the moment of gating. The conformance scan
*reports* the same conditions so they are visible in a sweep, but a scan never gates and a
gate never depends on a scan.

## 10 · Compatibility contract (A13)

Within a major `abf_version`, changes are **additive only**: new optional keys, new body
sections, new finding codes. Removing a key, narrowing an enum, or changing a rule's
meaning requires a major bump, and the bump ships a mechanical `--fix` migration.

Law 3 makes forward compatibility free — an old engine reading a newer bundle sees unknown
keys and records `info`. This contract is what makes backward compatibility a promise
rather than a hope. Receipts pin the engine version; a scan warns on skew between the
engine and `index.md`'s `abf_version`.

**Back-compat with AIDD 2.5: clean break.** ABF bundles only. Existing 2.5 projects stay on
the 2.5 engine until manually re-initialised; no migration verb ships in v1.

## 11 · The minimum conforming bundle

Three files, no engine required:

```
.add/index.md        # okf_version: "0.2" · abf_version: "1.1"
.add/PROJECT.md      # type: Project · title · goal
.add/tasks/fix-typo.md   # type: Task · title · goal · status
```

**Hand-mode is a first-class path.** Every rule in this format is honourable by editing
files in a text editor. The engine makes the method cheap and discoverable; it is not what
makes it valid. A bundle authored entirely by hand is a conforming bundle — which is the
only honest test of "files are the database".

## 12 · Extension ledger — where ABF goes beyond OKF (A9)

| ABF construct | OKF status | ABF's claim |
|---|---|---|
| `type:` values other than `Attested Computation` | OKF leaves `type` open | extension; unknown types are `info` for any consumer |
| `depends_on` / `needs` / `gives` | not in OKF | extension keys, legal under §11 |
| `#fragment` resolution (§3.3) | **§6 defines paths; fragments are unspecified** | ABF-owned grammar; generic consumers may leave them unresolved |
| `act` / `authority` / `outcome` / `receipt` / `brief` inside `verified[]` | §5.2 defines `by` / `at`; extra keys unspecified | additive extension inside an OKF-shaped list |
| `type: Run` result records | §10 leaves results producer-defined | ABF's producer-defined receipt shape |
| `covers:` binding rules (§8.3) | not in OKF | ABF evidence extension |
| `index.md` config frontmatter | §8 permits `okf_version` at the bundle root | additive keys (`abf_version`, `sensitive_paths`, `persona_corpus`) |
| Tiered reads T0/T1/T2 | not in OKF | a consumer discipline, not a document requirement |
| **Frozen `gives:` interface** (§3.5) | **ATG §4.3 defines minimal-subgraph repair; it does NOT constrain a node's interface** | ABF extension. ATG repairs by replacing tools and adjusting local dependencies; ABF adds that the external interface may not move without an explicit `refreeze` |
| **ATG node = a work item** (§3) | **ATG §3's node is one concrete tool call** `(i, f, o)` | ABF raises the same triple one altitude. The shape is borrowed; the granularity is ABF's |
| **`amended:` on a milestone** (§3.6) | not in OKF | additive extension inside an OKF-shaped list, same family as `ratified:` |
| **Compiled reserved files** (`log.md`, `index.md` body) | §8/§9 define the *shape* of these files, not who writes them | ABF requires them to be rendered from node stamps. A hand-authored `log.md` is still conforming to OKF — this is an ABF production rule, not a document requirement |

## 13 · Amendments landed in 1.3

| # | amendment | landed in |
|---|---|---|
| A22 | content-addressed receipt freshness; mtime demoted to a declared fallback | §8.1 |
| A23 | compiled files declare themselves to git; `merge=ours` + `doctor --sync` is the resolution | §1, §1.1, §9 |
| A24 | evidence kinds — `test-ids` · `command-exit` · `artifact-hash` · `human-observed`, each with what it does not prove | §8.0, §8, §9 |

**Changes from 1.2-draft:** the mtime freshness assumption recorded in 1.1 was **tested and
failed** — a `git worktree` checkout resets every mtime, so a committed receipt reads stale
in any fresh clone, worktree, or CI job. Freshness is now a content digest of the `scope:`
set, with mtime surviving only where git is absent and only when the receipt says so. Law
5's compiled files gain a merge story, because compiling removed concurrent writers and not
merge conflicts. And `covers:` binds to an observation rather than specifically to a test
ID, so the two profiles with no test runner have an honest evidence path instead of a
`covers_unverified` finding nobody reads.

## 13.1 · Amendments landed in 1.2

| # | amendment | landed in |
|---|---|---|
| A19 | ATG citation repair — node `(i, f, o)` is one tool call (§3); minimal-subgraph repair (§4.3); the frozen interface declared an ABF extension | §0 preamble, §12 |
| A20 | `log.md` is compiled from `verified[]` stamps, with a human-owned `## Notes` block | law 5, §1 |
| A21 | milestone amendment protocol — `amended:` stamp, dropped tasks keep their nodes, EXIT append-only, dependents flagged stale | §3.2, §3.6 |

**Changes from 1.1-draft:** the ATG relationship is stated with its section numbers and its
boundary, the way A9 did for OKF — the same defect class was present in the second standard
and went unchecked for one revision. `log.md` moves from append-only to compiled, which
removes the last file two concurrent agents could write and makes every journal line
traceable to a stamp. Milestones gain a scope-change protocol, so a human changing their
mind mid-wave is a recorded event rather than a silent edit. Law 5 generalises all of it.

## 13.2 · Amendments landed in 1.1

| # | amendment | landed in |
|---|---|---|
| A1 | authority ladder; sensitivity floor; bounded ratification | §3.1 |
| A2 | receipt freshness vs in-scope mtimes | §8.1 |
| A3 | the engine records, never executes | §8.2 |
| A4 | `log.md` rotation at milestone close | §1, §4.1 |
| A5 | brief context budget with loud degradation | §7.2 |
| A6 | `next:` affordance contract | §7.4 |
| A7 | fragment-resolver proof in the worked example | §3.3 (exercised by the M0 example) |
| A8 | milestone `## GROUND`, gathered once | §3.2 |
| A9 | OKF citation repair · `Run` vs Attested Computation · fragments declared an extension | §0, §2, §3.3, §12 |
| A10 | `log.md` date-grouped per OKF §9 | §1 |
| A11 | `index.md` compiled TOC body | §1 |
| A12 | scale rules | §4.1 |
| A13 | compatibility contract | §10 |
| A14 | injection trust boundary | law 4, §7.5 |
| A15 | evidence binding: `covers:` → receipt; red-first earned | §8.3 |
| A16 | brief determinism and hash stamped at the gate | §7.3 |
| A17 | sensitive-path authority floor | §3.1 |
| A18 | census in milestone `CLOSE` | §3.2 |

**Changes from 1.0-draft:** the four OKF defects above (D1–D5 of the v3 review) are
repaired; `scope:` is promoted to a frontmatter key (it was body prose, but the freshness
predicate needs it at T0); the `covers:` referent is defined for `quick` depth, which
1.0-draft left undefined; and the `data`/`architecture` authority floor moved from
per-task `human` to `plan`, bounded by §3.1's ratification rule.
