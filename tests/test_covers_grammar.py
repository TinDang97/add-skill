"""Red suite for e15 `resolve-covers-grammar` — ONE grammar for rule IDs.

F1 (open since M0, recorded on `.add/milestones/engine-core.md`): FORMAT §6.1 and
`scripts/validate_bundle.py` do not state the same grammar for a `covers:` referent.
§6.1 states the metavariable `R:<CODE>` and never expands `<CODE>`; the validator
enforces `R:[A-Z_]+`; the engine enforces `R:[A-Z0-9_]+`. Three oracles, two of them
in code and disagreeing with each other, and the prose pins neither.

This suite replaces "a human compares two documents" with an assertion (M1).

**It is deliberately decision-neutral.** Every test asserts that the oracles AGREE; not
one asserts WHICH grammar they agree on. Widening to admit digits and narrowing while
recording the renames both turn these tests green. That choice is a `human` authority
call (A17 — the task is `sensitivity: security`, and the author of the three offending
IDs is the one who would be choosing), and nothing here presumes it. A suite that
encoded the outcome would BE R:SELFSERVE, not a check against it.
"""

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FORMAT = REPO / "FORMAT.md"
BUNDLE = REPO / ".add"

sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / "add" / "scripts"))

import add  # noqa: E402  — READ ONLY. e15 may not edit the engine; it may only compare to it.
import validate_bundle  # noqa: E402


# --------------------------------------------------------------- the three oracles

# The depth keys the grammar is stated for. FORMAT §6.1 splits on depth because `quick`
# has no RULES section, so its referents are `goal`/`G<n>` rather than `M<n>`/`R:<CODE>`.
DEPTH_KEYS = ("quick", "standard|deep")

FENCE = re.compile(r"```[^\n]*\n(.*?)```", re.DOTALL)


def format_section(number: str) -> str:
    """The body of one numbered FORMAT section, heading exclusive."""
    text = FORMAT.read_text(encoding="utf-8")
    start = re.search(rf"^#+ {re.escape(number)} · .*$", text, re.MULTILINE)
    if not start:
        return ""
    rest = text[start.end() :]
    nxt = re.search(r"^#+ \d", rest, re.MULTILINE)
    return rest[: nxt.start()] if nxt else rest


def format_stated_grammar() -> dict[str, str]:
    """The grammar FORMAT §6.1 states, as {depth_key: pattern}.

    The contract this test imposes on FORMAT: §6.1 carries exactly ONE fenced block
    whose info line names `covers-grammar`, holding `<depth key> = <regex>` lines. A
    prose metavariable is not a statement of a grammar — nothing can be checked against
    `R:<CODE>` — so a §6.1 that only says `R:<CODE>` states nothing and returns {}.
    """
    for fence in FENCE.finditer(format_section("6.1")):
        info = format_section("6.1")[: fence.start()].rsplit("```", 1)
        block = fence.group(1)
        if "covers-grammar" not in (fence.group(0).splitlines()[0] + block):
            continue
        stated = {}
        for line in block.splitlines():
            if "=" not in line or line.lstrip().startswith("#"):
                continue
            key, _, pattern = line.partition("=")
            stated[key.strip().strip("`").replace(" ", "")] = pattern.strip().strip("`")
        return stated
    return {}


def validator_grammar() -> dict[str, str]:
    """The grammar `scripts/validate_bundle.py` enforces, as {depth_key: pattern}.

    Read from module constants on purpose. A grammar compiled inline inside
    `Scan.bodies()` is not *stated* anywhere a second oracle can cite, which is the
    structural half of R:DRIFT: you cannot keep two statements in step if one of them
    has no address.
    """
    quick = getattr(validate_bundle, "COVERS_QUICK", None)
    rule = getattr(validate_bundle, "COVERS_RULE", None)
    if quick is None or rule is None:
        return {}
    return {"quick": quick.pattern, "standard|deep": rule.pattern}


def engine_rule_pattern() -> re.Pattern:
    """The engine's RULE_ID, stripped of its list-item scaffolding.

    `add.RULE_ID` matches a RULES *line* (`- M1 …`); the validator matches a bare
    referent. Comparing them means comparing the ID alternation inside, not the anchors.
    """
    inner = re.search(r"\((M\\d\+\|R:\[[^\]]+\]\+)\)", add.RULE_ID.pattern)
    assert inner, f"cannot locate the ID alternation in add.RULE_ID: {add.RULE_ID.pattern!r}"
    return re.compile(rf"\A({inner.group(1)})\Z")


# --------------------------------------------------------------- the live bundle


def live_rule_ids() -> dict[str, list[str]]:
    """Every rule ID DECLARED in a RULES section anywhere in the bundle -> its nodes.

    Uses the engine's own RULE_ID so the corpus is not a third opinion.
    """
    ids: dict[str, list[str]] = {}
    for path in sorted(BUNDLE.rglob("*.md")):
        for line in path.read_text(encoding="utf-8").splitlines():
            m = add.RULE_ID.match(line)
            if m:
                ids.setdefault(m.group(1), []).append(path.relative_to(REPO).as_posix())
    return ids


def gated_nodes() -> dict[str, str]:
    """Nodes carrying a `gate` stamp in `verified[]` -> their full text.

    §3.6 / R:ERASE: a gated claim is recorded, never repaired. These are exactly the
    nodes whose rule IDs may not be rewritten in place.
    """
    out = {}
    for path in sorted(BUNDLE.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        fm = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
        if fm and re.search(r"act:\s*gate", fm.group(1)):
            out[path.relative_to(REPO).as_posix()] = text
    return out


def declared_ids(text: str) -> set[str]:
    return {m.group(1) for m in (add.RULE_ID.match(l) for l in text.splitlines()) if m}


# The three IDs F1 is about, pinned to the gated node that declares each. Pinned as data
# so that if a later sweep removes one, `test_no_gated_node_rewritten` notices (M3).
DISPUTED = {
    "R:T2SCAN": ".add/tasks/build-orient.md",
    "R:T2FANOUT": ".add/tasks/build-brief-compiler.md",
    "R:MTIME2": ".add/tasks/build-receipts-learn.md",
}


# --- test_grammar_stated_once · covers: M1, R:DRIFT ---------------------------


def test_grammar_stated_once():
    """The regex the validator enforces IS the grammar FORMAT states — same string.

    Neutral by construction: asserts equality, never a value.
    """
    stated = format_stated_grammar()
    assert stated, (
        "FORMAT §6.1 states the grammar only as prose metavariables — `M<n>` and "
        "`R:<CODE>` — and `<CODE>` is expanded nowhere in FORMAT.md. A metavariable "
        "cannot be compared to a regex, so no oracle can be held to §6.1 as written. "
        "§6.1 must carry ONE fenced `covers-grammar` block. (R:DRIFT, root cause)"
    )
    enforced = validator_grammar()
    assert enforced, (
        "scripts/validate_bundle.py compiles its grammar inline inside Scan.bodies(); "
        "it must expose COVERS_QUICK and COVERS_RULE so the stated grammar has one "
        "citable address. (R:DRIFT, structural half)"
    )
    assert set(stated) == set(DEPTH_KEYS), (
        f"§6.1 must state a grammar for each depth class {DEPTH_KEYS}, got {sorted(stated)}"
    )
    for key in DEPTH_KEYS:
        assert stated[key] == enforced[key], (
            f"R:DRIFT at depth `{key}`: FORMAT §6.1 states {stated[key]!r} but "
            f"scripts/validate_bundle.py enforces {enforced[key]!r}. One format, one grammar."
        )


# --- test_both_oracles_agree_on_rule_ids · covers: M1 ------------------------


def test_both_oracles_agree_on_rule_ids():
    """The engine's RULE_ID and the validator accept the SAME set of rule IDs.

    Not "the right set" — the same set. Counted over the live bundle, never sampled
    (specs/quality: conformance assertions are counted, never sampled), plus synthetic
    probes so the check keeps its teeth in an empty bundle.
    """
    enforced = validator_grammar()
    assert enforced, (
        "scripts/validate_bundle.py must expose COVERS_RULE before its grammar can be "
        "compared to the engine's RULE_ID. (R:DRIFT, structural half)"
    )
    validator = re.compile(enforced["standard|deep"])
    engine = engine_rule_pattern()

    probes = sorted(live_rule_ids()) + [
        "M1",
        "M12",
        "R:DRIFT",
        "R:SELF_SERVE",
        "R:T2SCAN",
        "R:MTIME2",
        "R:lower",
        "R:",
        "X1",
    ]
    split = {
        p: (bool(engine.match(p)), bool(validator.match(p)))
        for p in probes
        if bool(engine.match(p)) != bool(validator.match(p))
    }
    assert not split, (
        "R:DRIFT — two oracles, two grammars for one format. "
        f"{len(split)} referent(s) are accepted by one and rejected by the other: "
        + "; ".join(
            f"{p!r} engine={'accept' if e else 'reject'} validator={'accept' if v else 'reject'}"
            for p, (e, v) in sorted(split.items())
        )
    )


# --- test_decision_is_recorded · covers: M2, R:SELFSERVE ---------------------


def test_decision_is_recorded():
    """The node carries the REASON, not just the outcome.

    M2 is the whole point of the task: either resolution is defensible, and choosing
    without a recorded reason is not — because the author of the three offending IDs is
    the one choosing (A17). This test cannot go green until a human records the
    decision, and that is correct: it is the check standing in for the authority.
    """
    node = (BUNDLE / "tasks" / "resolve-covers-grammar.md").read_text(encoding="utf-8")
    m = re.search(r"^## DECISION\n(.*?)(?=^## |\Z)", node, re.DOTALL | re.MULTILINE)
    assert m, (
        "tasks/resolve-covers-grammar.md carries no `## DECISION` section. M2 requires "
        "the decision recorded WITH its reason; an outcome visible only as a diff to "
        "FORMAT.md is an unrecorded decision."
    )
    body = m.group(1)

    chosen = re.search(r"^chosen:\s*(widen|narrow)\s*$", body, re.MULTILINE)
    assert chosen, "`## DECISION` must name `chosen: widen` or `chosen: narrow`."

    reason = re.search(r"^reason:\s*(.+?)(?=^\w+:|\Z)", body, re.DOTALL | re.MULTILINE)
    assert reason and len(reason.group(1).split()) >= 12, (
        "`## DECISION` must carry a `reason:` of substance. M2: the outcome without the "
        "reason is exactly what this task exists to prevent."
    )
    by = re.search(r"^by:\s*human:\S+", body, re.MULTILINE)
    assert by, (
        "`## DECISION` must record `by: human:<who>`. A17 pins a `sensitivity: security` "
        "task to `human` authority; a decision stamped by an agent is not the decision."
    )

    # R:SELFSERVE — "widening a grammar so the author's own nodes stop reporting, with no
    # other reason". The reason may cite the three IDs; it may not consist ONLY of them.
    prose = reason.group(1)
    stripped = prose
    for rid in DISPUTED:
        stripped = stripped.replace(rid, "")
    assert len(stripped.split()) >= 10, (
        "R:SELFSERVE — the recorded reason reduces to the author's own three offending "
        "IDs. A reason must hold some ground beyond 'my nodes stop reporting'."
    )


# --- test_no_gated_node_rewritten · covers: M3 -------------------------------


def test_no_gated_node_rewritten():
    """A gated node's rule IDs are unchanged, or the change is recorded (§3.6).

    Two halves. The first is red today: gated nodes declare IDs the live oracle rejects,
    and no correction is recorded — so the bundle is in a state where SOME resolution is
    owed. The second is a ratchet: it goes red the moment a disputed ID disappears from
    a gated node without a §3.6 correction, which is the sweep M3 forbids.
    """
    gated = gated_nodes()
    assert gated, "expected the live bundle to contain gated nodes"

    enforced = validator_grammar()
    assert enforced, (
        "scripts/validate_bundle.py must expose COVERS_RULE before a gated node's IDs "
        "can be tested against the one stated grammar."
    )
    validator = re.compile(enforced["standard|deep"])

    # half 1 — every rule ID in a gated node is admitted by the ONE grammar, or the node
    # records a §3.6 correction for it.
    owed = {
        f"{rel}:{rid}"
        for rel, text in gated.items()
        for rid in declared_ids(text)
        if not validator.match(rid) and f"corrected: {rid}" not in text
    }
    assert not owed, (
        f"{len(owed)} rule ID(s) in human-gated nodes are rejected by the grammar the "
        "validator enforces, and no §3.6 correction is recorded for them: "
        f"{sorted(owed)}. Either the grammar admits them or each rename is recorded on "
        "its node — never a silent sweep."
    )

    # half 2 — the ratchet. A disputed ID may leave its gated node only via a record.
    for rid, rel in DISPUTED.items():
        text = gated.get(rel)
        assert text is not None, f"{rel} was expected to be a gated node"
        assert rid in declared_ids(text) or f"corrected: {rid}" in text, (
            f"R:ERASE / §3.6 — {rid} is gone from {rel}, which carries a `gate` stamp, "
            "and the node records no `corrected: <old-id>` line. A gated claim is "
            "recorded, never repaired."
        )


# --- test_covers_read_only_from_checks · covers: M1 --------------------------
# NOT one of the four checks e15's CHECKS section names. Added because measuring the
# `after` criterion ("the 7 covers_referent info lines are either gone or justified")
# turned up a second, independent defect: only 3 of those 7 lines are about the grammar
# at all. The other 4 are the validator's COVERS regex reading PROSE — it is unanchored
# and scans the whole body, so `· covers: …` inside a PLAN paragraph is parsed as a
# referent and the `[^·]+?` run swallows text across newlines. The engine's
# COVERS_IN_CHECK is line-anchored and does not have this defect. Reported to the
# orchestrator as a finding in its own right; the fix is grammar-independent.


def test_covers_read_only_from_checks(tmp_path):
    """`covers:` is read from CHECKS list items only — never from prose."""
    node = tmp_path / "prose.md"
    node.write_text(
        "---\ntype: Task\ntitle: Prose\ngoal: g\nstatus: build\ndepth: standard\n---\n"
        "## PLAN\n"
        "strategy: `rules` reads the `<must>` block · `covers` reads CHECKS for "
        "`· covers: …`. That sentence is prose, not a check.\n"
        "\n## CHECKS\n- test_real · covers: M1 · a genuine referent\n",
        encoding="utf-8",
    )
    scan = validate_bundle.Scan(tmp_path).run()
    bogus = [f for f in scan.findings if f["code"] == "covers_referent"]
    assert not bogus, (
        "the validator parsed a `covers:` referent out of PLAN prose. `covers:` is "
        f"defined for CHECKS list items (FORMAT §8.3); got: {bogus}"
    )
