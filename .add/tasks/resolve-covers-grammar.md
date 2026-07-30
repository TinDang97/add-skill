---
type: Task
title: reconcile the covers: grammar — FORMAT §6.1 vs the validator
goal: one grammar for rule IDs, decided deliberately rather than widened to make the author pass
status: done
depth: standard
kind: feature
sensitivity: security
milestone: /milestones/engine-core.md
depends_on:
  - /tasks/build-evidence-binding.md
needs:
  - /tasks/build-evidence-binding.md#gives
generated: { by: add/3.0.0, at: 2026-07-30 }
verified:
  - { by: "claude/opus-5", at: 2026-07-30, act: freeze, authority: human }
  - { by: "process:run", at: 2026-07-30, act: run, authority: process, outcome: PASS, receipt: /tasks/resolve-covers-grammar.d/runs/1.md }
  - { by: "human:tindang", at: 2026-07-30, act: gate, authority: human, outcome: PASS, receipt: /tasks/resolve-covers-grammar.d/runs/1.md, brief: "sha256:a9a74072782f76f9" }
scope:
  - FORMAT.md
  - scripts/validate_bundle.py
  - tests/test_covers_grammar.py
---
## CARD
goal: one grammar for rule IDs, decided deliberately rather than widened to make the author pass
gives: a single stated grammar · both oracles enforcing it · the decision and its reason recorded
scope: FORMAT.md · scripts/validate_bundle.py · tests/test_covers_grammar.py
beat: done · next: e14 `checks --sync` — and it now has e15's evidence to design against

## RULES
<must>
- M1 FORMAT §6.1 and `scripts/validate_bundle.py` state and enforce the SAME grammar, asserted by a
     check that reads both rather than by a human comparing them (F1 has been open since M0)
- M2 the decision is recorded WITH its reason. Widening to admit digits (`R:T2SCAN`, `R:T2FANOUT`,
     `R:MTIME2`) and narrowing while renaming those three are both defensible; choosing without a
     recorded reason is not, because the author of the offending IDs is the one choosing (A17)
- M3 no gated node's rule IDs are silently rewritten. If narrowing wins, the renames are recorded as
     a correction on each node, not applied as a sweep (§3.6)
</must>
<reject>
- R:SELFSERVE widening a grammar so the author's own nodes stop reporting, with no other reason -> "SELFSERVE"
- R:DRIFT two oracles carrying two grammars for one format -> "DRIFT"
</reject>
<after>
- the 7 `covers_referent` info lines this bundle reports are either gone or justified
- the next person to add a rule ID learns the grammar from one place
</after>
⚠ that this is worth a task at all — it reports `info`, not `error`, and nothing is blocked. The
  argument for doing it is that F1 is the ONLY finding in this project where two documents disagree
  about the format itself, and every later oracle inherits the ambiguity.

## PLAN
contract: <published at freeze>
strategy: <published at freeze>
scope: FORMAT.md · scripts/validate_bundle.py · tests/test_covers_grammar.py
floor: validator CONFORMS on `.add/`; the M0 suite stays green
least-sure: rules — M2. This is a judgement about a naming convention, and the honest risk is
  spending a human gate on something that reports `info` and blocks nothing.

## DECISION
chosen: widen
by: human:tindang
at: 2026-07-30
reason: A digit inside an identifier is unremarkable, and no rule of this format depends on rule
  IDs being alphabetic — the exclusion of digits was never a decision anyone took, it was a regex
  written narrowly and never revisited. The alternative, narrowing, would rename rule IDs inside
  three human-gated nodes to satisfy a constraint with no purpose behind it, and every such rename
  is a §3.6 correction that a future reader has to reconcile against what was actually accepted at
  the gate. Widening costs one character class and touches no gated node; narrowing costs three
  recorded corrections and buys nothing. The self-serve objection is real and is answered on the
  merits rather than dismissed: the three IDs this admits happen to be mine, so the test suite was
  written decision-NEUTRAL before the choice was made — every check asserts that the oracles agree,
  not which grammar they agree on, so narrowing would have turned them green too.
what-was-actually-wrong: F1 was misdiagnosed as two documents disagreeing. §6.1 stated only the
  metavariable `R:<CODE>` and expanded `<CODE>` nowhere, so there was no grammar to disagree with —
  the validator and the engine had each invented one, and drifted. §6.1 now carries a fenced
  `covers-grammar` block as the single statement, and a check holds all three to it. Found by the
  subagent that executed this task, and it is a better diagnosis than the one the node opened with
also-fixed-here: the validator's `COVERS` regex was unanchored and scanned the whole body, reading
  `· covers: …` out of PLAN prose and inventing referents. **Four of this bundle's seven
  `covers_referent` info lines were that bug, not a grammar problem.** 7 info → 3 → 0

## CHECKS
- test_grammar_stated_once · covers: M1, R:DRIFT · the regex in the validator matches the grammar FORMAT states
- test_both_oracles_agree_on_rule_ids · covers: M1 · the engine's RULE_ID and the validator accept the same set
- test_decision_is_recorded · covers: M2, R:SELFSERVE · the node carries the reason, not just the outcome
- test_no_gated_node_rewritten · covers: M3 · a gated node's rule IDs are unchanged, or the change is recorded
- test_covers_read_only_from_checks · covers: M1 · a `covers:` in PLAN prose is not a referent
red-first: every check above MUST fail for the right reason before BUILD.
unlabelled by design: `test_grammar_extractor_is_functional` and
  `test_engine_pattern_is_extractable` carry no `covers:`. They prove the suite's own machinery on
  a fixture before it is trusted against FORMAT.md — a check on the checker, which enforces no rule
  of this node. Recorded here rather than given a label it does not deserve (e14's M3).

## EVIDENCE
receipt: /tasks/resolve-covers-grammar.d/runs/1.md — 7/7 green · kind test-ids · freshness content
red-first: the subagent's own red run, captured on its branch: 4 failed / 3 passed. The four are
  the option-dependent checks and each named its own fix — the first said "§6.1 states the grammar
  only as prose metavariables … §6.1 must carry ONE fenced `covers-grammar` block", which is the
  root cause this task turned out to be about
floor: validator on `.add/` — **54 nodes · 158 edges · 0 info · 0 error.** The bundle is fully
  clean for the first time in the project's history. Full suite 168 green
outcome: **F1 CLOSED, and it was smaller and different than recorded.** 7 info → 0. Four of the
  seven were a validator bug (an unanchored `COVERS` scanning PLAN prose and inventing referents),
  and the remaining three were not a disagreement between two grammars but the absence of one:
  §6.1 stated `R:<CODE>` and expanded `<CODE>` nowhere, so the validator and the engine had each
  invented a grammar and drifted. §6.1 now states it once, in a fenced block, and
  `test_grammar_stated_once` holds all three to it by string equality
budget: 0 lines of engine growth — this task's scope is FORMAT.md, the validator and a test file.
  Engine unchanged at 1,448/2,400 · A3 invariant: 1,448 + 530 = **1,978 / 2,400 — slack 422**
scope-check: match — FORMAT.md, scripts/validate_bundle.py, tests/test_covers_grammar.py. The
  node's CARD originally named `tests/test_validate_bundle.py`; the suite landed as a new file
  instead, and both CARD and frontmatter were corrected to the file that actually exists
executed-by: the first subagent this project has used, in an isolated worktree, from a compiled
  `brief --for-subagent` of 11,458 B (~2.9k tok) as its complete context contract. It respected
  every constraint — `add/scripts/add.py` untouched, no `verified[]` stamp appended, no gated node
  rewritten, and the `human`-authority decision explicitly NOT taken. Cost: 123,069 tokens over 53
  tool calls in 12.5 minutes. Merged after review at `human` authority (A17: `validate_bundle.py`
  is a sensitive path)
gate: PASS — human:tindang, 2026-07-30, recorded by `add gate`

## LESSONS
- **A finding recorded for a day and a half was misdiagnosed the whole time.** F1 read "two
  documents disagree about the grammar". The truth was that one document never stated a grammar —
  it stated a metavariable and never expanded it — so both implementations invented one privately
  and drifted, and four of the seven symptoms were an unrelated regex bug. Writing a finding down
  preserves it; it does not verify it. A finding needs a check before it needs a task.
  -> add learn quality
- **The check that closed F1 was written to be neutral about the answer, on purpose.** Every test
  asserts the oracles AGREE, never which grammar they agree on, so narrowing would have turned them
  green exactly as widening did. That is what let a `human` decision be taken on the merits instead
  of being pre-empted by whichever behaviour the suite happened to encode — and it is the concrete
  defence against R:SELFSERVE, given the three IDs at stake were the author's own.
  -> add learn method
- **`covers:` placement is already not uniform, at the second author.** I put it in test docstrings
  (118 of 131 tests); the subagent put it in `# --- name · covers: … ---` comment headers above each
  function, and deliberately left two machinery tests unlabelled. e14's ⚠ asked whether docstrings
  are a durable carrier — the answer arrived before e14 was built, and it is no. e14 must accept
  both forms or declare one and migrate, and it must keep e15's honest "unlabelled by design" case.
  -> add learn system
- **A grammar with no machine-readable address will not stay in step with a second oracle.** Not
  "might not" — this project ran two oracles against one prose metavariable and they diverged
  without anyone noticing, then a third (the engine) diverged again in the other direction.
  -> add learn domain
