---
type: Spec
title: Experience
lens: udd
project: ADD-SKILL
generated: { by: claude/opus-5, at: 2026-07-29 }
---
## Now
The surface is a CLI read by two audiences at once: a human skimming a terminal and
an agent parsing stdout. Both are served by the same shape — a short human line, then
a `next:` line that is literally the command to run.

The felt experience we are designing for: *you come back cold after two weeks, type
one command, and know exactly what to do next.* `add status` is that command.

For a `cli-tool` profile, this lens covers the verb surface, the output contract, and
the error voice. (For a `ui-app` it would cover IA, tokens, and component states; for
a `library`, the public API surface. The lens is fixed; the skeleton is profiled.)

## Decisions that bind
- `add status` is *the* resume verb — no separate `next` verb exists. (PROPOSAL §3f)
- Every verb ends with `next:` — this is the adoption mechanism, not a nicety. (A6, define-read-protocol)
- Guidance lives in engine output, never in template blockquotes that are re-read forever. (define-read-protocol)
- Errors name the fix, not the rule: say the command that resolves it. (define-read-protocol)
- A refusal is never silent: a refused gate prints why and what would make it pass. (define-authority-rules)
- ADD orients once per session, unasked, in a repo that has a bundle — a `SessionStart` hook running
  `add status --brief`. It is the only moment ADD speaks first, and it is gated on `.add/` existing so a
  session with no ADD work pays nothing. (E12, PROPOSAL §12)
- The proactivity ladder stops at *propose*: orient, notice, propose — never act. An engine that acts
  unasked owns outcomes it has no authority for. (E12)

## Deltas (newest first)
<!-- `add learn experience "<lesson>"` prepends here -->
- [open · 2026-07-29] Measured in the 2.5 pilot: features documented only in guides got 0% adoption; the same feature named in engine output went 0 → 12 uses and −29% tokens at identical fidelity. Output is the only surface that gets read. (define-read-protocol)
