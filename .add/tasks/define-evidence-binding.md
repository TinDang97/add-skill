---
type: Task
title: Bind a gate to the checks its receipt actually observed
goal: a gate cannot pass on a check that was never written, and red-first stops being a self-report
status: done
depth: deep
kind: security
sensitivity: security
milestone: /milestones/format-standard.md
depends_on:
  - /tasks/define-task-schema.md
  - /tasks/define-authority-rules.md
needs:
  - /tasks/define-task-schema.md#gives
  - /tasks/define-authority-rules.md#gives
gives:
  - "a receipt declares its kind: test-ids | command-exit | artifact-hash | human-observed (A24)"
  - "each kind states what it proves AND what it does not; a weaker kind is a visible weakening"
  - "a Run receipt records observed test IDs and their outcome, plus ids: parsed|unknown"
  - "freeze refuses unless every Must and Reject appears in at least one check's covers:"
  - "gate refuses unless every CHECKS id appears in the receipt with outcome: pass"
  - "unparseable runner output degrades to a covers_unverified finding, never a silent pass"
  - "red_first: proven requires a prior receipt on the same task where those ids failed"
  - "brief is deterministic and prints a content hash; the gate stamps the hash that drove the work"
  - "covers: referents by depth — goal|G<n> at quick, M<n>|R:<CODE> at standard and deep"
scope:
  - FORMAT.md
generated: { by: claude/opus-5, at: 2026-07-29 }
verified:
  - { by: "human:tindang", at: 2026-07-29, act: freeze, authority: human }
  - { by: "human:tindang", at: 2026-07-29, act: gate, authority: human, outcome: PASS,
      receipt: /tasks/build-worked-example.d/runs/3.md }
    # A17 pinned this to `human`: `scope:` includes FORMAT.md, a sensitive_path. The
    # declared `sensitivity:` was never the binding constraint.
---
## CARD
goal: close the forgeable link in our own trust chain
gives: A15 evidence binding · A16 brief determinism and hash
scope: FORMAT.md §6.1 · §7.3 · §8.3
beat: done · gate PASS by human:tindang on receipt 3

## RULES
<must>
- M1 a receipt records the test IDs it observed and each one's outcome, not only a pass count
- M2 a gate refuses when a check named in CHECKS is absent from the receipt's passed set
- M3 when IDs cannot be extracted, the receipt records `ids: unknown` and the gate carries `covers_unverified` — visible, never silent
- M4 `red_first: proven` requires a prior receipt on the same task in which those same IDs failed
- M5 a brief compiles byte-identically from the same inputs and prints a content hash; the gate stamps it
- M6 `covers:` has a defined referent at every depth, including `quick`, which has no RULES section
- M7 a receipt declares its evidence `kind:`, and each kind states what it proves AND what it does not;
     a gate records the kind it accepted, so a weaker kind is a visible weakening rather than a silent one (A24)
</must>
<reject>
- R:LABEL a design where `covers:` names a rule but binds to no observation -> "LABEL"
- R:COUNT a gate that accepts a pass COUNT as evidence for a NAMED check -> "COUNT"
- R:CLAIMED a `red_first` value the agent asserts rather than a prior receipt demonstrates -> "CLAIMED"
- R:HOSTAGE a refusal triggered purely by a runner's output formatting -> "HOSTAGE"
</reject>
<after>
- naming a check that was never written is refused at the gate, mechanically
- a reviewer can trace: this brief -> this code -> this receipt -> this gate, by hash and by ID
</after>
⚠ that test IDs are extractable from the runners real projects use — if wrong: `ids:
  unknown` becomes the common case and the binding degrades to a finding nobody reads,
  which would make M2 decorative. First evidence: whichever runner the M1 engine meets first

## PLAN
contract: FORMAT.md §8.3 (the two bindings and the degradation), §7.3 (determinism and
  hash), §6.1 (the `covers:` referent table)
strategy: split the binding across the two moments that already exist — freeze checks
  rule→check coverage (authored), gate checks check→receipt (observed). Neither moment
  gains a step; both gain a refusal. Extraction reads `--junitxml` via stdlib XML where a
  runner offers it and falls back to parsing verbose node lines. Failure handling: the
  fallback's failure is a recorded finding, never a crash and never a refusal, because a
  format hostage to one runner's formatting would be worse than the gap it closes.
scope: FORMAT.md
floor: none — greenfield format; the rule it replaces was an unchecked correspondence
least-sure: contract — the degradation. `covers_unverified` as `info` is the permissive
  choice; the strict alternative (refuse unless IDs parse) buys a harder guarantee at the
  cost of blocking any project whose runner we cannot read

## CHECKS
- test_receipt_records_ids · covers: M1, R:COUNT · a receipt with only a pass count is incomplete
- test_gate_refuses_unmet_covers · covers: M2, R:LABEL · a CHECKS id absent from the receipt refuses the gate
- test_unknown_ids_degrade · covers: M3, R:HOSTAGE · unparseable output yields `covers_unverified` and does not refuse
- test_red_first_needs_prior · covers: M4, R:CLAIMED · `red_first: proven` without a prior failing receipt is rejected
- test_brief_deterministic · covers: M5 · the same inputs compile to the same bytes and the same hash
- test_gate_stamps_brief · covers: M5 · a gate stamp carries the hash of the brief that drove the work
- test_covers_referent_quick · covers: M6 · a quick-depth check may cite `goal` or `G<n>` and nothing else
- test_kind_is_declared · covers: M7 · a receipt with no `kind:` cannot earn a gate
- test_weaker_kind_is_recorded · covers: M7 · a `command-exit` gate carries `covers_coarse`, never a silent pass
- test_doc_profile_has_a_path · covers: M7 · a `doc`-profile task reaches a gate without `ids: unknown`
red-first: every check above MUST fail for the right reason before BUILD.

## EVIDENCE
receipt: /tasks/build-worked-example.d/runs/3.md — 18/18, the shared M0 evidence run
gate: PASS — human:tindang, 2026-07-29, authority `human` (A17 floor)
scope-check: FORMAT.md only — inside the declared scope

## LESSONS
- Our own trust chain had a forgeable link: `covers:` named a check, the receipt reported a pass count, and nothing tied the two. Evidence is only evidence when the specific claim binds to the specific observation -> add learn quality
- The reviewer's habit that found it: follow the chain to its last link and ask what is checking THAT one. The gap was at the end, where confidence was highest -> add learn method
