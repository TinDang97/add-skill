---
type: Task
title: Align ABF-1 with the OKF and ATG source texts
goal: every external standard claim in FORMAT.md is either verified against the source or declared an extension
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
  - "concept ID cites OKF §2 (Terminology), not §4"
  - "type: Run is a producer-defined RESULT record; OKF §10 Attested Computation is the DEFINITION"
  - "the #fragment grammar is an ABF extension owned by the ABF resolver — OKF §6 is silent on fragments"
  - "log.md groups entries under ISO YYYY-MM-DD headings per OKF §9"
  - "index.md carries a compiled grouped-concept TOC body per OKF §8"
  - "ATG §3 defines a node as (i, f, o) where f is ONE CONCRETE TOOL CALL — ABF raises the same triple one altitude"
  - "ATG §4.3 is Minimal Necessary Subgraph Repair — the frozen gives: interface is an ABF constraint ATG does not state"
  - "§12 extension ledger — every construct where ABF exceeds OKF or ATG, listed"
scope:
  - FORMAT.md
generated: { by: claude/opus-5, at: 2026-07-29 }
verified: []
---
## CARD
goal: every standard we profile says what we claim it says — all of them, not one of them
gives: A9–A11 + A19 — repaired OKF and ATG citations, the Run/Attested split, the ledger
scope: FORMAT.md §0 · §1 · §2 · §3.3 · §12
beat: verify · next: blocked on the validator (build-worked-example) for its receipt

## RULES
<must>
- M1 every § reference to OKF in FORMAT.md matches the section that actually carries that rule
- M2 any construct OKF or ATG does not define is listed in the extension ledger, with the source's status beside it
- M3 `type: Run` is described as a producer-defined result record, never as an OKF Attested Computation
- M4 reserved files conform to their OKF shapes: `log.md` date-grouped (§9), `index.md` with a body (§8)
- M5 every ATG claim carries its section number, and the boundary between what ATG defines and what ABF
     adds is stated where the claim is made — not only in the ledger
</must>
<reject>
- R:BORROW a claim that a source sanctions a construct it never mentions -> "BORROW"
- R:SILENT_EXT an extension used in the format but absent from the ledger -> "SILENT_EXT"
- R:PARTIAL auditing one profiled standard and not the others -> "PARTIAL"
</reject>
<after>
- a reader can check every external claim against its source in one pass, and none of them fails
- a generic OKF consumer reading this bundle records only `info` findings
</after>
⚠ that OKF v0.2 and the ATG preprint are stable while ABF-1 is drafted against them — if wrong:
  a revision changes a section number or a rule, and the ledger is the one place that must be
  re-checked

## PLAN
contract: FORMAT.md §0 (the preamble and its two ATG claims), §2 (Run), §3.3 (fragments), §12 (the ledger)
strategy: fetch each source text and check each claim rather than citing from memory —
  the defect class here is a citation that sounds right. State extensions as extensions;
  the format loses nothing by admitting where it exceeds its base, and loses its
  credibility by claiming sanction it does not have. Do this for EVERY profiled source in
  one pass: auditing one and trusting the other is the same defect wearing a different name.
scope: FORMAT.md
floor: none — the 1.0-draft claims were unverified, so there is nothing to regress
least-sure: rules — whether `Run` should instead BE an Attested Computation, which would
  make gates reproducible by a third party at the cost of a heavier receipt

## CHECKS
- test_okf_section_refs · covers: M1 · every `OKF §n` in FORMAT.md matches the source's section n
- test_extension_ledger_complete · covers: M2, R:SILENT_EXT · every non-OKF key used in the format appears in §12
- test_run_not_attested · covers: M3, R:BORROW · FORMAT.md never calls a Run receipt an Attested Computation
- test_log_date_grouped · covers: M4 · `.add/log.md` entries sit under `## YYYY-MM-DD` headings
- test_index_has_body · covers: M4 · `.add/index.md` carries a grouped concept TOC
- test_atg_claims_cited · covers: M5, R:PARTIAL · every ATG claim in FORMAT.md carries a section number, and
  the frozen-interface rule is marked an ABF extension where it is stated
red-first: every check above MUST fail for the right reason before BUILD.

## EVIDENCE
receipt: <tasks/align-standards-citations.d/runs/1.md — pending the M0 validator>
gate: <pending>
scope-check: <pending>

## LESSONS
- A citation that sounds right is the cheapest thing in a spec to get wrong and the most expensive to inherit: a validator built on a mis-cited section certifies nothing -> add learn quality
- Declaring an extension costs one table row; claiming a standard sanctions it costs the reader's trust in every other claim -> add learn system
- The rule "verify the standards you profile" was written after auditing OKF, and then applied to OKF only. ATG went unchecked for a full revision, and it carried the same defect class: `node = (needs, work, gives)` reads like a citation but ATG's node is one concrete tool call, and the frozen-interface rule is ours. A discipline applied to the artifact that taught it, and not to its siblings, is a habit rather than a rule -> add learn method
