---
type: Task
title: Define the evolution contract, the amendment protocol, and the trust boundary
goal: the format and a milestone can both change without breaking a live bundle, and a brief cannot be used as an injection path
status: done
depth: standard
kind: docs
sensitivity: architecture
milestone: /milestones/format-standard.md
depends_on:
  - /tasks/define-task-schema.md
needs:
  - /tasks/define-task-schema.md#gives
gives:
  - "every compiled file declares itself: a COMPILED BODY marker and a .gitattributes entry (A23)"
  - "merge=ours (a built-in driver, no install step) plus `doctor --sync` is the documented resolution"
  - "within a major abf_version, changes are additive only: new optional keys, sections, finding codes"
  - "a removal or semantic change requires a major bump shipping a mechanical --fix migration"
  - "bundle content composes as instruction; all other content enters a brief only as quoted <evidence>"
  - "a milestone scope change is an `amended:` stamp, never a silent edit (A21)"
  - "a task leaving scope becomes status: dropped with a reason and keeps its node; EXIT is append-only"
  - "a node whose needs: cite a dropped task's gives: is flagged stale and must re-verify before its next gate"
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
goal: durable under evolution — of the format AND of the human's mind — and safe under composition
gives: A13 the compatibility contract · A14 the injection trust boundary · A21 the amendment protocol
scope: FORMAT.md §3.6 · §7.5 · §10 · law 4
beat: done · gate PASS by human:tindang on receipt 3

## RULES
<must>
- M1 within a major version, only additive changes are legal — new optional keys, sections, codes
- M2 a removal, a narrowed enum, or a changed rule meaning requires a major bump AND a `--fix` path
- M3 a brief presents bundle nodes as instruction and everything else as quoted evidence, labelled with its origin
- M4 forward compatibility needs no rule: the notary law already makes an unknown key an `info` finding
- M5 a milestone scope change records `amended: { by, at, authority, reason }` at no less authority than its
     own ratification, and a prior `ratified:` stamp never extends to tasks the amendment adds
- M6 a task removed from scope becomes `status: dropped` with a reason and keeps its node; `EXIT` criteria are
     struck, never deleted; dependents citing a dropped `gives:` are flagged stale
- M7 a compiled file declares itself twice — a `COMPILED BODY` marker for the human, a `.gitattributes`
     entry for git — and the documented merge resolution (`merge=ours` then `doctor --sync`) needs no
     git configuration, because an install step would break "drop the directory in place" (A23)
</must>
<reject>
- R:BREAK a minor-version change that removes a key a live bundle depends on -> "BREAK"
- R:INJECT a brief that inlines a file from outside the bundle as instruction -> "INJECT"
- R:QUIET a scope change applied by editing the milestone without a stamp -> "QUIET"
- R:ERASE an EXIT criterion deleted rather than struck, so the milestone appears to have met a goal it dropped -> "ERASE"
</reject>
<after>
- a bundle written under 1.1 still reads under 1.3 without an edit
- a hostile string in a source file cannot become an instruction in a future brief
- a reader of a closed milestone can see what it was asked to do, what it stopped doing, and who decided
</after>
⚠ that additive-only is sustainable for a full major version — if wrong: a needed
  correction is either deferred or forces a major bump nobody wanted, and the pressure
  lands on whichever key was designed worst

## PLAN
contract: FORMAT.md §10 (the contract) and §7.5 (the boundary), plus law 4 in §0
strategy: state both as rules with named failure modes rather than as advice. The
  compatibility rule is worth more than its cost only if it is checkable, so it is phrased
  as a property of a diff between two format versions. Rollback: none — both are additive.
scope: FORMAT.md
floor: none — greenfield format
least-sure: rules — whether `sensitive_paths:` and `persona_corpus:` should have been in
  1.0, since adding them under an additive-only contract is legal but sets a precedent for
  growing `index.md` one key at a time

## CHECKS
- test_additive_only · covers: M1, R:BREAK · a minor bump that removes a key is rejected by the diff rule
- test_major_ships_fix · covers: M2 · a major bump without a `--fix` path is incomplete
- test_evidence_is_quoted · covers: M3, R:INJECT · non-bundle content appears only inside `<evidence>`
- test_unknown_key_is_info · covers: M4 · an unknown key from a newer version yields `info`, never `error`
- test_amend_is_stamped · covers: M5, R:QUIET · a milestone whose `tasks:` changed without an `amended:` stamp is a finding
- test_amend_authority_floor · covers: M5 · an amendment stamped below the milestone's ratification authority is refused
- test_dropped_keeps_node · covers: M6 · a removed task's file still exists at `status: dropped` with a reason
- test_exit_append_only · covers: M6, R:ERASE · an EXIT criterion present at ratification is still present after an amendment
- test_dependents_stale · covers: M6 · a node citing a dropped task's `gives:` is flagged stale
- test_compiled_declared_rule · covers: M7 · FORMAT §1.1 names both declarations and only built-in git drivers
- test_merge_needs_no_config · covers: M7 · the resolution works on a clone with an empty git config
red-first: every check above MUST fail for the right reason before BUILD.

## EVIDENCE
receipt: /tasks/build-worked-example.d/runs/3.md — 18/18, the shared M0 evidence run
gate: PASS — human:tindang, 2026-07-29, authority `human` (A17 floor)
scope-check: FORMAT.md only — inside the declared scope

## LESSONS
- The notary law paid a second dividend nobody designed it for: tolerating unknown keys makes forward compatibility free, so the contract only has to promise the backward direction -> add learn system
- Evolution was specified for the format and for a frozen task interface, and nowhere for a milestone — which is the one that changes most, because it is the only one a human changes on purpose. A durability contract that covers the machine's changes and not the person's is half a contract -> add learn method

