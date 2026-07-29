---
type: Spec
title: Domain
lens: ddd
project: ADD-SKILL
generated: { by: claude/opus-5, at: 2026-07-29 }
---
## Now
The domain is *a method for driving software work with an AI*, expressed as files.

**Bundle** — one `.add/` directory; an OKF bundle and the whole state of a project.
**Node** — one markdown file with OKF frontmatter; the unit of the graph.
**Project** — the bundle's standing direction (1 per bundle).
**Milestone** — one user-request scope; a wave of tasks with an exit condition.
**Task** — one atomic node: *(needs, work, gives)*. Its `gives:` is its external
interface; rebuilding may change anything inside, never the frozen `gives:`.
**Spec** — one of five fixed lenses (domain · system · experience · quality · method).
**Persona** — a reasoning lens applied at a decision point.
**Prompt** — a parametric XML skeleton compiled into a brief.
**Run** — an evidence receipt from a command that actually executed.

**Beat** — one of the three: direction, build, verify.
**Depth** — the ceremony dial: quick · standard · deep.
**Lane** — the path a request takes, chosen by depth and sensitivity.
**Tier** — how much of a node is read: T0 frontmatter · T1 CARD · T2 body.
**Freeze** — the act that makes `gives:` an interface others may depend on.
**Gate** — the recorded verdict on a task, earned by a receipt.
**Delta** — a lesson landed on a spec; **fold** — a delta absorbed into `Now`.
**Seam** — a `gives:` consumed by a task in a different milestone; compiled, never authored.

## Decisions that bind
- A task's identity is its file; its interface is `gives:`; everything else may change. (define-task-schema)
- The five lenses are closed. Domains vary the *skeleton*, never the lens set. (define-entity-model)
- `type:` vocabulary is closed: Project · Milestone · Task · Spec · Persona · Prompt · Run. (define-entity-model)
- Slug = filename stem; verb-first for tasks, noun-first for milestones, ≤4 words, kebab-case. (define-entity-model)

## Deltas (newest first)
<!-- `add learn domain "<lesson>"` prepends here -->
- [open · 2026-07-29] "Seam" is derivable from cross-milestone `gives:`/`needs:` edges — 2.5 maintained SEAMS.md by hand; 3.0 compiles it. (define-entity-model)
