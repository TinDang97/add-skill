---
type: Task
title: package the engine inside the skill directory
goal: the skill ships the engine, and this repo's own bundle is driven by it
status: direction
depth: standard
kind: feature
sensitivity: architecture
milestone: /milestones/engine-core.md
scope:
  - add/scripts/add.py
  - tests/engine/test_package_in_skill.py
depends_on:
  - /tasks/build-durability.md
  - /tasks/build-hints-layer.md
needs:
  - /tasks/build-durability.md#gives
  - /tasks/build-hints-layer.md#gives
gives:
  - "the skill directory layout with the engine at scripts/add.py"
  - "the CLI entry point: argument parsing over the ten verbs"
  - "this repo's `.add/` driven by the engine — the M1 EXIT criterion"
budget: 138 CODE lines of growth (D-15) — MEASURED, not estimated. A working CLI spike covering all ten verbs, --dry-run, --json and exit codes came to 208 wc -l / 138 code. Supersedes both the 80 in this frontmatter and the 200 in A5, which disagreed by 120 lines and never met (F20)
generated: { by: add/3.0.0, at: 2026-07-29 }
verified: []
---
## CARD
goal: the skill ships the engine, and this repo's own bundle is driven by it
gives: the skill directory layout with the engine at scripts/add.py · the CLI entry point: argument parsing over the ten verbs · this repo's `.add/` driven by the engine — the M1 EXIT criterion
scope: add/scripts/add.py · its red suite
beat: direction · next: add freeze package-in-skill

## RULES
<must>
- M1 `python3 <skill>/scripts/add.py <verb>` works from a clean checkout with zero install (D-1)
- M2 the ten verbs are reachable from the CLI with the flags their tasks defined
- M3 this repo's `.add/` is driven by the engine, not by hand — the M1 EXIT criterion, demonstrated not asserted
</must>
<reject>
- R:HANDDRIVEN a bundle state reachable only by hand editing -> "HANDDRIVEN"
- R:DEP a runtime dependency outside the standard library -> "DEP"
</reject>

## PLAN
contract: <published at freeze>
strategy: <published at freeze>
scope: add/scripts/add.py · tests/engine/
floor: validator exits 0 on `.add/`; every earlier task's checks stay green

## CHECKS
- test_cli_zero_install · covers: M1, R:DEP · a subprocess run from a clean checkout succeeds
- test_all_ten_verbs_reachable · covers: M2 · each verb responds to the CLI
- test_stdlib_only · covers: M1, R:DEP · no third-party import anywhere in the engine
- test_bundle_driven_by_engine · covers: M3, R:HANDDRIVEN · a full task lifecycle runs through the CLI
red-first: every check above MUST fail for the right reason before BUILD.

## EVIDENCE
receipt: <runs/<n>.md>
gate: <PASS | RISK-ACCEPTED | HARD-STOP>
budget: <growth vs allocation · A3 invariant>
scope-check: <files touched vs `scope:`>

## LESSONS
- <lesson> -> add learn <domain|system|experience|quality|method>
