"""Red suite for scripts/validate_bundle.py — the ABF-1 conformance validator.

One test per Must / Reject of tasks/build-worked-example, carrying the same `covers:`
keys as the task's CHECKS section. Every test must fail for the right reason before the
validator exists (red-first, FORMAT §8.3).
"""

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
VALIDATOR = REPO / "scripts" / "validate_bundle.py"


def run(bundle, *args):
    """Run the validator; return (exit_code, parsed_json)."""
    proc = subprocess.run(
        [sys.executable, str(VALIDATOR), str(bundle), "--json", *args],
        capture_output=True,
        text=True,
    )
    payload = json.loads(proc.stdout) if proc.stdout.strip() else {}
    return proc.returncode, payload


def codes(payload, severity=None):
    return [
        f["code"]
        for f in payload.get("findings", [])
        if severity is None or f["severity"] == severity
    ]


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    return path


def minimal_bundle(root: Path) -> Path:
    """The three-file minimum conforming bundle of FORMAT §11."""
    write(root / "index.md", '---\nokf_version: "0.2"\nabf_version: "1.1"\n---\n')
    write(
        root / "PROJECT.md",
        "---\ntype: Project\ntitle: Fixture\ngoal: a fixture bundle exists\n---\n",
    )
    write(
        root / "tasks" / "fix-typo.md",
        "---\ntype: Task\ntitle: Fix typo\ngoal: the typo is gone\nstatus: todo\n"
        "depth: quick\n---\n## CARD\ngoal: the typo is gone\n",
    )
    return root


# --- test_conforming_exits_zero · covers: M1, M2 -----------------------------


def test_conforming_exits_zero():
    """This repo's own .add/ bundle conforms: exit 0, zero error findings."""
    code, payload = run(REPO / ".add")
    assert code == 0, f"expected exit 0, got {code}: {codes(payload, 'error')}"
    assert codes(payload, "error") == []


def test_minimal_bundle_conforms(tmp_path):
    """FORMAT §11: three files, no engine, still conforming."""
    code, payload = run(minimal_bundle(tmp_path / "b"))
    assert code == 0
    assert codes(payload, "error") == []


# --- test_missing_frontmatter_errors · covers: M2 ----------------------------


def test_missing_frontmatter_errors(tmp_path):
    root = minimal_bundle(tmp_path / "b")
    write(root / "tasks" / "bare.md", "# no frontmatter here\n")
    code, payload = run(root)
    assert code != 0
    assert "missing_frontmatter" in codes(payload, "error")


def test_type_empty_errors(tmp_path):
    root = minimal_bundle(tmp_path / "b")
    write(root / "tasks" / "untyped.md", "---\ntitle: Untyped\n---\nbody\n")
    code, payload = run(root)
    assert code != 0
    assert "type_empty" in codes(payload, "error")


# --- test_escape_errors · covers: M2 -----------------------------------------


def test_escape_errors(tmp_path):
    """Containment is decided by the RESOLVED path, never by the spelling."""
    root = minimal_bundle(tmp_path / "b")
    write(
        root / "tasks" / "escapee.md",
        "---\ntype: Task\ntitle: Escapee\ngoal: escape\nstatus: todo\ndepth: quick\n"
        "depends_on:\n  - ../../outside.md\n---\n",
    )
    code, payload = run(root)
    assert code != 0
    assert "edge_out_of_bundle" in codes(payload, "error")


def test_dotdot_inside_the_bundle_is_not_an_escape(tmp_path):
    """`../PROJECT.md` from tasks/ lands INSIDE the bundle — it resolves, it does not escape.

    The authored check for this task assumed `../outside.md` escapes; from a node in
    `tasks/` it does not. Recorded as a lesson: a `..` is not an escape.
    """
    root = minimal_bundle(tmp_path / "b")
    write(
        root / "tasks" / "neighbour.md",
        "---\ntype: Task\ntitle: Neighbour\ngoal: g\nstatus: todo\ndepth: quick\n"
        "depends_on:\n  - ../PROJECT.md\n---\n",
    )
    code, payload = run(root)
    assert code == 0
    assert "edge_out_of_bundle" not in codes(payload)
    assert "edge_unresolved" not in codes(payload)


# --- test_unresolved_is_info_only · covers: M2, R:FAILINFO -------------------


def test_unresolved_is_info_only(tmp_path):
    """A milestone may declare its wave before the task files exist."""
    root = minimal_bundle(tmp_path / "b")
    write(
        root / "milestones" / "wave.md",
        "---\ntype: Milestone\ntitle: Wave\ngoal: the wave ships\nstatus: queued\n"
        "tasks:\n  - /tasks/not-yet-written.md\n---\n",
    )
    code, payload = run(root)
    assert code == 0, "an unresolved edge must never fail the verdict"
    assert "edge_unresolved" in codes(payload, "info")
    assert codes(payload, "error") == []


# --- test_all_fragment_forms · covers: M3 ------------------------------------


def fragment_bundle(root: Path) -> Path:
    minimal_bundle(root)
    write(
        root / "tasks" / "publisher.md",
        "---\ntype: Task\ntitle: Publisher\ngoal: the interface is published\n"
        "status: verify\ndepth: standard\n"
        'gives:\n  - "GET /thing -> 200"\n---\n'
        "## CARD\ngoal: publish\n\n## Decisions that bind\n- one line\n",
    )
    write(
        root / "tasks" / "consumer.md",
        "---\ntype: Task\ntitle: Consumer\ngoal: the interface is consumed\n"
        "status: build\ndepth: deep\n"
        "needs:\n"
        "  - /tasks/publisher.md#gives\n"
        "  - /tasks/publisher.md#goal\n"
        "  - /tasks/publisher.md#decisions-that-bind\n"
        "  - /tasks/publisher.md#no-such-thing\n---\n## CARD\ngoal: consume\n",
    )
    return root


def test_all_fragment_forms(tmp_path):
    """#frontmatter-key, #goal, a heading slug, and one deliberate miss."""
    code, payload = run(fragment_bundle(tmp_path / "b"))
    assert code == 0
    forms = payload["report"]["fragment_forms"]
    assert forms["frontmatter_key"] >= 2, forms  # #gives and #goal
    assert forms["heading_slug"] == 1, forms
    assert forms["unresolved"] == 1, forms
    assert codes(payload, "error") == []


def test_frontmatter_wins_over_heading(tmp_path):
    """FORMAT §3.3: the resolver is ordered — one ref can never resolve two ways."""
    root = minimal_bundle(tmp_path / "b")
    write(
        root / "tasks" / "both.md",
        "---\ntype: Task\ntitle: Both\ngoal: g\nstatus: todo\ndepth: quick\n"
        'gives:\n  - "the frontmatter value"\n---\n## Gives\nthe heading section\n',
    )
    write(
        root / "tasks" / "reader.md",
        "---\ntype: Task\ntitle: Reader\ngoal: g\nstatus: todo\ndepth: quick\n"
        "needs:\n  - /tasks/both.md#gives\n---\n",
    )
    code, payload = run(root)
    assert code == 0
    resolved = payload["report"]["resolved_fragments"]
    assert resolved["/tasks/both.md#gives"] == "frontmatter_key"


# --- test_depth_and_status_coverage · covers: M4 -----------------------------


def test_depth_and_status_coverage(tmp_path):
    root = fragment_bundle(tmp_path / "b")  # quick + standard + deep, 3 statuses
    _, payload = run(root)
    report = payload["report"]
    assert set(report["depths"]) == {"quick", "standard", "deep"}
    assert len(set(report["statuses"])) >= 3, report["statuses"]


# --- test_reserved_files_exempt · covers: M5 ---------------------------------


def test_reserved_files_exempt(tmp_path):
    root = minimal_bundle(tmp_path / "b")
    write(root / "log.md", "# log\n\n## 2026-07-29\n\n- actor · node · opened\n")
    code, payload = run(root)
    assert code == 0
    assert "type_empty" not in codes(payload)


# --- test_no_body_parse · covers: R:BODY -------------------------------------


def test_no_body_parse(tmp_path):
    """The verdict is frontmatter-only: replacing every body changes no error finding."""
    intact = fragment_bundle(tmp_path / "intact")
    noised = fragment_bundle(tmp_path / "noised")
    for md in noised.rglob("*.md"):
        text = md.read_text()
        head, _, _ = text.partition("---\n")[2].partition("\n---\n")
        md.write_text(f"---\n{head}\n---\n!!! noise !!!\n")

    code_a, payload_a = run(intact)
    code_b, payload_b = run(noised)
    assert code_a == code_b == 0
    assert sorted(codes(payload_a, "error")) == sorted(codes(payload_b, "error"))


# --- the covers referent rule (FORMAT §6.1) is an info finding, never a gate --


def test_covers_referent_is_info_not_error(tmp_path):
    """A quick-depth check citing M1 is reported, but law 3 forbids rejecting for it."""
    root = minimal_bundle(tmp_path / "b")
    write(
        root / "tasks" / "wrong-covers.md",
        "---\ntype: Task\ntitle: Wrong\ngoal: g\nstatus: todo\ndepth: quick\n---\n"
        "## CHECKS\n- test_thing · covers: M1 · does a thing\n",
    )
    code, payload = run(root)
    assert code == 0, "a covers-referent mistake must not fail the verdict (law 3)"
    assert "covers_referent" in codes(payload, "info")


def test_unknown_type_is_info(tmp_path):
    root = minimal_bundle(tmp_path / "b")
    write(root / "tasks" / "odd.md", "---\ntype: Sandwich\ntitle: Odd\n---\n")
    code, payload = run(root)
    assert code == 0
    assert "unknown_type" in codes(payload, "info")
