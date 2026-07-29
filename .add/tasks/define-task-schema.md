---
type: Task
title: Define the task node schema
goal: a task node's external interface is machine-readable and its repair rule is mechanical
status: verify
depth: standard
kind: docs
sensitivity: architecture
milestone: /milestones/format-standard.md
depends_on:
  - /tasks/define-entity-model.md
needs:
  - /tasks/define-entity-model.md#gives
gives:
  - "Task frontmatter: type·title·goal·status·depth·kind·sensitivity·milestone·depends_on·needs·gives·generated·verified"
  - "body sections: CARD·RULES·PLAN·CHECKS·EVIDENCE·LESSONS, section set conditioned by depth"
scope:
  - FORMAT.md
  - templates/task.md.tmpl
generated: { by: claude/opus-5, at: 2026-07-29 }
verified: []
---
## CARD
goal: the task node shape every other M0 task cites
gives: Task frontmatter keys + the six body sections, depth-conditioned
scope: FORMAT.md §3 · templates/task.md.tmpl
beat: verify · next: blocked on the validator (build-worked-example) for its receipt

## RULES
<must>
- M1 the frozen interface lives in frontmatter (`gives:`), not in body prose, so dependents can be found mechanically
- M2 `status:` alone determines activity — no pointer key exists anywhere in the bundle
- M3 the section set is a function of `depth:`; `quick` renders CARD · CHECKS · EVIDENCE only
- M4 a change to a frozen `gives:` appends a `refreeze` stamp; the prior stamp is never edited
</must>
<reject>
- R:POINTER a schema that reintroduces an `active_task` field -> "POINTER"
- R:PROSE_IFACE a schema where the interface is only readable as body prose -> "PROSE_IFACE"
</reject>
<after>
- every other M0 task can cite `#gives` on this node and get the shape verbatim
- `doctor` can list the dependents of a changed interface without reading any body
</after>
⚠ that `gives:` as a list of strings is expressive enough for non-API tasks (docs, infra, data)
  — if wrong: the key needs a typed shape and every consumer changes

## PLAN
contract: the frontmatter key set above, plus the six named body sections
strategy: state the schema in FORMAT.md §3 with one worked instance; the template
  file is the executable copy. Failure mode to design against: a key that only makes
  sense for API tasks, which would push other kinds back into prose.
scope: FORMAT.md §3 · templates/task.md.tmpl
floor: none — greenfield format
least-sure: contract — the `gives:` value shape for non-API work

## CHECKS
- test_gives_is_frontmatter · covers: M1 · a task file's interface is parseable from frontmatter alone, body unread
- test_no_pointer_key · covers: M2, R:POINTER · scanning the schema for `active_*` finds nothing
- test_depth_sections · covers: M3 · rendering at `quick` yields exactly CARD, CHECKS, EVIDENCE
- test_refreeze_appends · covers: M4 · a second freeze leaves the first stamp byte-identical
- test_non_api_gives · covers: R:PROSE_IFACE · a `kind: docs` task expresses its interface in `gives:`
red-first: every check above MUST fail for the right reason before BUILD.

## EVIDENCE
receipt: <tasks/define-task-schema.d/runs/1.md — pending the M0 validator>
gate: <pending>
scope-check: <pending>

## LESSONS
- 2.5's frozen §3 was prose a human read; making it frontmatter is what lets `doctor` compute staleness -> add learn domain
