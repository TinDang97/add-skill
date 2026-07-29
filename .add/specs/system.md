---
type: Spec
title: System
lens: sdd
project: ADD-SKILL
generated: { by: claude/opus-5, at: 2026-07-29 }
---
## Now
Three shipped parts, in ONE artifact: the **format** (ABF-1, `FORMAT.md`), the
**engine** (`add`, Python stdlib, **10 verbs** plus flags, living in the skill's
`scripts/`), and the **skill** (`SKILL.md` + 6 references). The engine is a notary
and a compiler — it records, validates, and compiles the graph and briefs. It never
judges, and it never executes a command on its own initiative. Judgment lives in
the skill and the personas.

Everything derivable is compiled, never authored: `graph.json`, `index.md`'s body,
**`log.md`**, seams, the census, the review packet. A compiled artifact cannot rot
and has no concurrent writers. `graph.json` is additionally gitignored, and is never
authoritative and never trusted for a gate decision.

## Decisions that bind
- Files are the database. No `state.json`; activity is derived from `status:`. (define-entity-model)
- Compiled beats authored: anything derivable from frontmatter is rendered, never hand-maintained —
  `graph.json`, `index.md`'s body, `log.md`, seams, the census, the review packet. (A20, FORMAT law 5)
- There is no shared mutable file in a bundle, which is what makes N agents in N worktrees safe. (A20)
- The journal is a projection of `verified[]` stamps; a `## Notes` block is the only human-written part
  and is preserved verbatim across recompiles. (A20, define-log-rotation)
- The skill keeps the name `add`; a 2.5 install is moved aside to `add-legacy`, and routing is a
  mechanical check for `abf_version:` in `index.md` — never a judgement. (D-7)
- ABF's frozen `gives:` interface is an ABF extension: ATG §4.3 defines minimal-subgraph repair and
  does not constrain a node's interface. Every profiled source is audited, not just the first. (A19)
- Python stdlib only, single package, engine ≤ 2,400 lines (raised once, 2026-07-29, to carry the §11 evidence-binding work); overflow drops a verb — `--locate` then `--graph` — never a law, and never the budget again. (PROPOSAL §10, D-6)
- The engine ships INSIDE the skill directory (`add/scripts/add.py`); a `pipx` shim is optional and may never become required. One artifact, one version. (PROPOSAL §4c, D-1)
- A gate refuses when a `covers:` key names a check absent from the receipt's passed set; unparseable runner output degrades to a `covers_unverified` finding, never a silent pass. (A15, define-evidence-binding)
- `brief` is deterministic and prints a content hash; the gate stamps the hash of the brief that drove the work. (A16, define-evidence-binding)
- Every write is a single-file atomic replace (tmp + rename). No multi-file transactions exist. (define-authority-rules)
- Git is the transaction log and the rollback. The engine ships no `undo`. (define-authority-rules)
- The engine RECORDS receipts; `add run -- <cmd>` executes the agent's own command. A bare `gate` never executes anything. (A3, define-authority-rules)
- A receipt is stale if any file in the task's `scope:` is newer than it; a stale receipt cannot earn a gate. (A2, define-authority-rules)
- Every verb's stdout ends with a `next:` line naming the exact next command and the cheapest legal lane. (A6, L4)
- Every write verb supports `--dry-run`; slugs validate against a path-safe charset. (define-authority-rules)
- Receipts pin the engine version; `doctor` warns on skew against `index.md`'s `abf_version`. (define-authority-rules)
- The CLI lives in the installed package, never vendored into a bundle. (PROPOSAL §7)
- Clean break from 2.5: no migration verb in v1. (PROPOSAL §7)

## Deltas (newest first)
<!-- `add learn system "<lesson>"` prepends here -->
- [open · 2026-07-29] Compiling `log.md` and `index.md` removed concurrent WRITERS and did not remove MERGE conflicts: a committed compiled file still collides between branches. Two failure modes wear the same word "conflict", and closing one reads like closing both. A compiled artifact needs a declared regeneration path, not just a compiler. (define-compat-contract)
- [open · 2026-07-29] This spec's own `Now` said "15 verbs" for a full day after 10 were ratified, while `index.md`'s compiled TOC and a task's EVIDENCE line carried two more contradictions — three stale authored facts in a 20-node bundle, in one day, written by the same agent that ratified the change. Discipline does not scale; compilation does. (define-log-rotation)
- [open · 2026-07-29] 2.5's engine is 9,058 lines across 17 modules — the ≤2,000 target is a 4.5× cut, not 3×. Budget, not promise. (define-entity-model)
