---
type: Task
title: Port OKF node I/O — read tiers and surgical writes
goal: the engine can read a node at any tier and change one key without disturbing anything else in the file
status: done
depth: standard
kind: feature
sensitivity: architecture
milestone: /milestones/engine-core.md
depends_on:
  - /tasks/build-worked-example.md
  - /tasks/define-read-protocol.md
  - /tasks/define-entity-model.md
needs:
  - /tasks/build-worked-example.md#gives
  - /tasks/define-read-protocol.md#gives
  - /tasks/define-entity-model.md#gives
gives:
  - "parse(text) -> (frontmatter dict, body) — the OKF subset this format actually uses, or (None, text)"
  - "read(path, tier) -> T0 frontmatter | T1 frontmatter+CARD | T2 whole node (FORMAT §4)"
  - "set_key / append_item — SURGICAL line edits on the raw text; untouched lines, comments and key order survive byte-identically"
  - "write(path, text) — atomic single-file replace via tmp + os.replace, same directory"
scope:
  - add/scripts/add.py
  - tests/engine/test_node_io.py
generated: { by: claude/opus-5, at: 2026-07-29 }
verified:
  - { by: "process:pytest", at: 2026-07-29, act: run, authority: process, outcome: PASS, receipt: /tasks/port-okf-parse.d/runs/2.md }
  - { by: "human:tindang", at: 2026-07-29, act: gate, authority: human, outcome: PASS }
---
## CARD
goal: read a node at a declared tier; change one key without touching any other byte
gives: parse · read(tier) · set_key/append_item · atomic write
scope: add/scripts/add.py · tests/engine/test_node_io.py
beat: done · next: make the red suite green, then `add run -- pytest`

## RULES
<must>
- M1 `read` honours the tier it is given: T0 never returns body text, T1 returns frontmatter plus the
     `## CARD` section and nothing after it, T2 returns the whole node (FORMAT §4, law 2)
- M2 a write is a single-file atomic replace — write a temp file in the SAME directory, then
     `os.replace`. A reader either sees the old file whole or the new file whole, never a partial one
- M3 changing a key preserves every byte the change does not concern: comments, blank lines, key
     order, block scalars, and the body all survive unchanged
- M4 `parse` is a notary: a file with no parseable frontmatter returns `(None, text)` and never raises.
     The caller decides whether that is a finding (law 3)
- M5 the parser covers exactly what ABF-1 uses and says so: top-level scalars, block lists, inline
     lists, inline flow maps (`generated: { by: x, at: y }`), block scalars (`>-`, `|`), and lists of
     inline maps (`verified:` entries). Anything outside that subset is preserved as raw text, never
     silently dropped
</must>
<reject>
- R:REGEN a writer that serialises the whole frontmatter from a parsed dict -> "REGEN"
- R:PARTIAL a write path where a crash can leave a truncated node on disk -> "PARTIAL"
- R:TIERLEAK a T0 or T1 read that returns body text past its tier -> "TIERLEAK"
- R:RAISE a parse that raises on a malformed node instead of reporting it -> "RAISE"
</reject>
<after>
- every other verb has one way to read a node and one way to change it
- `.add/index.md`'s rationale comments survive an engine write, so the bundle stays human-authored
  where humans authored it
</after>
⚠ that a surgical line editor is sufficient for every write the ten verbs need — if wrong:
  some verb needs a structural rewrite (re-ordering a list, nesting a new block), and that
  verb gets an explicit regenerate path with its own test, rather than the editor quietly
  growing into the YAML serialiser R:REGEN exists to forbid

## PLAN
contract:
  `parse(text) -> (dict | None, body)` · `read(path, tier) -> dict` with keys `fm`, `card`, `body`
  populated per tier · `set_key(raw_fm, key, value) -> raw_fm` · `append_item(raw_fm, key, item) -> raw_fm`
  · `write(path, text) -> None`
strategy:
  Frontmatter is held as BOTH a parsed dict (for reading) and the original raw text (for writing).
  Reads use the dict; writes rewrite one line region of the raw text and leave the rest alone. This
  is the only design that satisfies M3 without a comment-preserving YAML library we are not allowed
  to depend on. `os.replace` is atomic on POSIX and Windows when source and destination share a
  filesystem — hence the same-directory temp file.
  Failure handling: parse never raises; write fails loudly and leaves the original intact (the temp
  file is removed in a `finally`). Rollback: git, per specs/system.
scope: add/scripts/add.py · tests/engine/test_node_io.py
floor: `scripts/validate_bundle.py` must still exit 0 on `.add/` after any engine write — the M0
  conformance oracle is the regression floor for all of M1
least-sure: rules — M5's subset boundary. The honest failure is a construct that parses to something
  plausible but wrong; the test suite therefore asserts the exact parsed value for every construct
  the live bundle actually contains, not a hand-written sample.

## CHECKS
- test_parse_scalars_and_lists · covers: M5 · scalars, block lists and inline `[]` parse to exact values
- test_parse_inline_map · covers: M5 · `generated: { by: x, at: y }` parses to a dict, not a string
- test_parse_block_scalar · covers: M5 · a `>-` goal folds to one line with no trailing newline
- test_parse_list_of_maps · covers: M5 · `verified:` entries parse to dicts carrying `act` and `authority`
- test_parse_no_frontmatter_returns_none · covers: M4, R:RAISE · a bare markdown file returns `(None, text)`
- test_parse_malformed_does_not_raise · covers: M4, R:RAISE · an unterminated block raises nothing
- test_read_t0_has_no_body · covers: M1, R:TIERLEAK · T0 returns frontmatter and empty body/card
- test_read_t1_is_card_only · covers: M1, R:TIERLEAK · T1 returns the CARD section and nothing past it
- test_read_t2_is_whole_node · covers: M1 · T2 returns the full body
- test_set_key_preserves_comments · covers: M3, R:REGEN · a key change leaves every comment and neighbouring line byte-identical
- test_set_key_preserves_order · covers: M3 · key order is unchanged after a set
- test_append_item_keeps_indent · covers: M3 · an appended list item matches the block's existing indentation
- test_write_is_atomic · covers: M2, R:PARTIAL · the temp file lands in the same directory and no partial file survives a failure
- test_roundtrip_bundle_byte_identical · covers: M3, R:REGEN · reading and rewriting every node in `.add/` with no change produces zero diff
red-first: every check above MUST fail for the right reason before BUILD.

## EVIDENCE
receipt: /tasks/port-okf-parse.d/runs/2.md — 15/15 green · kind test-ids · freshness content ·
  red-first proven by runs/1.md (collection failed: no module named `add` — every check failed for
  the one right reason)
proof: the round-trip is not vacuous — 23 live nodes rewritten byte-identically, including a
  wrapped multi-line flow map, nested `receipt` maps, a `verified:` list-of-maps, a folded `>-`
  scalar, and the rationale comments in `index.md`. `log.md` is correctly skipped: no frontmatter
floor: `scripts/validate_bundle.py .add` still exits 0 — 23 nodes · 71 edges · 11 info · 0 error.
  The 11 info are `edge_unresolved` refs to M1 tasks not yet created (§7 permits sketching a wave)
budget: OVER — 245 lines against an allocation of 180 (+65, +36%). Code is 159; the overhang is
  42 blank · 37 docstring · 7 comment. See LESSONS
gate: PASS — human:tindang, 2026-07-29. The budget overrun was excluded from the gate and
  decided separately as a milestone amendment (see /milestones/engine-core.md#amended)
scope-check: match — `add/scripts/add.py` and `tests/engine/test_node_io.py` only. One node outside
  scope was edited before BUILD, not during it: `index.md`'s `sensitive_paths` gained
  `add/scripts/**` when this task created that directory

## LESSONS
- **A budget and its allocations must be stated in the same unit, and the unit must be named.**
  The 2,400 ceiling is `wc -l` — the unit of the 8,948-line 2.5 anchor. The twelve per-task
  allocations were written in code lines. e1 hit 88% of its allocation in code and 136% in total,
  which is not an overrun but a units error surfacing. Measured across the whole plan the gap is
  1,337 lines, not the 65 the first reading suggested.
  -> add learn method
- **Summing a column is a compiled fact, not an authored one (L7, third instance).** §13c asserted
  "~15% held in reserve" one paragraph above a table whose own total row read 2,450 against a
  2,400 ceiling. Both were hand-written; neither was computed. -> add learn quality
- **P7 worked.** A per-task line budget asserted from wave one turned a wave-nine catastrophe into a
  wave-one arithmetic problem. The signal was worth more than the number it reported.
  -> add learn method
