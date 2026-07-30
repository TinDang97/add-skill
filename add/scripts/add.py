#!/usr/bin/env python3
"""add — the ADD engine for ABF-1 bundles. Python stdlib only, one file.

e1 slice: node I/O. Everything else in the engine calls through here.

Two rules shape this module, and both come from the format:

* **Reads are tiered** (FORMAT law 2). `read(path, tier)` returns exactly its tier and
  no more: T0 is frontmatter, T1 adds `## CARD`, T2 adds the whole body. A tier that
  leaks is a context cost the format exists to remove.
* **Writes are surgical, never regenerative** (task `port-okf-parse`, R:REGEN). A node
  is held as BOTH a parsed dict (to read) and its original raw frontmatter text (to
  write). Changing a key rewrites one line region and leaves every other byte — comments,
  key order, blank lines, block scalars — exactly as the human left it. Serialising a
  parsed dict back to YAML would silently strip the rationale comments this bundle
  carries, which is why no such function exists here.

The parser covers the ABF-1 subset and nothing more: top-level scalars, block lists,
inline lists, inline flow maps, block scalars, nested maps, and lists of flow maps.
Anything outside it survives in `raw` and is simply absent from the dict — never
half-parsed into a plausible wrong value.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path, PurePosixPath

FENCE = re.compile(r"\A---\n(.*?)\n---\n?(.*)\Z", re.DOTALL)
BLOCK_SCALARS = {">", ">-", ">+", "|", "|-", "|+"}


# --------------------------------------------------------------------- scanning


def _strip_comment(line: str) -> str:
    """Drop a trailing `#` comment, honouring quotes. A `#` inside a value is data."""
    quote = None
    for i, ch in enumerate(line):
        if quote:
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
        elif ch == "#" and (i == 0 or line[i - 1].isspace()):
            return line[:i]
    return line


def _scalar(value: str):
    value = value.strip()
    if value in ("[]", "{}"):
        return [] if value == "[]" else {}
    if value.startswith("[") and value.endswith("]"):
        return [_scalar(v) for v in _split_commas(value[1:-1]) if v.strip()]
    if value.startswith("{") and value.endswith("}"):
        return _flow_map(value)
    if len(value) > 1 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def _split_commas(text: str) -> list[str]:
    """Split on commas that sit outside quotes and outside nested braces."""
    out, depth, quote, start = [], 0, None, 0
    for i, ch in enumerate(text):
        if quote:
            quote = None if ch == quote else quote
        elif ch in "\"'":
            quote = ch
        elif ch in "{[":
            depth += 1
        elif ch in "}]":
            depth -= 1
        elif ch == "," and depth == 0:
            out.append(text[start:i])
            start = i + 1
    out.append(text[start:])
    return out


def _flow_map(text: str) -> dict:
    """`{ by: x, at: 2026-07-29T08:00Z }` — split pairs on the FIRST colon only, so a
    timestamp or a `human:actor` value keeps its own colons."""
    data = {}
    for pair in _split_commas(text.strip().lstrip("{").rstrip("}")):
        key, sep, value = pair.partition(":")
        if sep:
            data[key.strip()] = _scalar(value)
    return data


def _open_quote(text: str) -> bool:
    """True when `text` ends inside an unterminated quoted string.

    Scanned, never counted. An apostrophe in `the node's own body` makes the single-quote count
    odd while opening nothing, because the value is already inside double quotes. Counting
    instead of tracking state made a continuation run to the end of the frontmatter and swallow
    `budget`, `generated` and `verified` across 25 nodes of this bundle — with the full suite
    green and the M0 validator reporting CONFORMS.
    """
    quote = None
    for ch in text:
        if quote:
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
    return quote is not None


def _tokens(raw: str) -> list[tuple[int, str]]:
    lines = []
    for line in raw.splitlines():
        stripped = _strip_comment(line)
        if stripped.strip():
            lines.append((len(stripped) - len(stripped.lstrip()), stripped.strip()))
    return lines


def _block(toks: list[tuple[int, str]], i: int, indent: int):
    """Parse one block at `indent`; return (value, index after it)."""
    if toks[i][1].startswith("- "):
        items = []
        while i < len(toks) and toks[i][0] >= indent and toks[i][1].startswith("- "):
            text, i = toks[i][1][2:], i + 1
            # A list item may wrap: an unclosed flow map, or an unclosed quote. Both are
            # continued until they balance. Without the quote arm a wrapped `"…"` was cut at
            # the first newline and KEPT its opening quote, so the value parsed to something
            # plausible and wrong — found by e5 rendering a `gives:` into a brief, after this
            # had survived 132 checks, the M0 validator and five human gates.
            while i < len(toks) and (text.count("{") > text.count("}") or _open_quote(text)):
                text, i = text + " " + toks[i][1], i + 1
            items.append(_scalar(text))
        return items, i

    data = {}
    while i < len(toks) and toks[i][0] >= indent:
        if toks[i][0] > indent:  # deeper than this block: not ours to claim
            i += 1
            continue
        key, sep, value = toks[i][1].partition(":")
        if not sep:
            i += 1
            continue
        key, value, i = key.strip(), value.strip(), i + 1
        if value in BLOCK_SCALARS:
            folded = []
            while i < len(toks) and toks[i][0] > indent:
                folded.append(toks[i][1])
                i += 1
            data[key] = " ".join(folded) if value.startswith(">") else "\n".join(folded)
        elif value == "" and i < len(toks) and toks[i][0] > indent:
            data[key], i = _block(toks, i, toks[i][0])
        elif value == "":
            data[key] = []
        else:
            data[key] = _scalar(value)
    return data, i


# ------------------------------------------------------------------ public read


def split(text: str):
    """(raw_frontmatter, body). `(None, text)` when there is no parseable fence."""
    match = FENCE.match(text)
    return (match.group(1), match.group(2)) if match else (None, text)


def parse(text: str):
    """(frontmatter_dict, body). Never raises — a malformed node is the caller's finding
    to record, not this function's exception to throw (FORMAT law 3)."""
    raw, body = split(text)
    if raw is None:
        return None, body
    try:
        toks = _tokens(raw)
        return (_block(toks, 0, 0)[0] if toks else {}), body
    except Exception:  # a notary reports; it does not crash the caller
        return None, text


def card_of(body: str) -> str:
    """The `## CARD` section only — T1 stops where the next `## ` heading starts."""
    out, inside = [], False
    for line in body.splitlines(keepends=True):
        if line.startswith("## "):
            if inside:
                break
            inside = line.strip() == "## CARD"
            continue
        if inside:
            out.append(line)
    return "".join(out).strip()


def read(path: Path, tier: str = "T0") -> dict:
    """Read one node at exactly `tier` (FORMAT §4). Nothing past the tier is returned."""
    if tier not in ("T0", "T1", "T2"):
        raise ValueError(f"unknown tier {tier!r} — expected T0, T1 or T2")
    text = Path(path).read_text(encoding="utf-8")
    raw, body = split(text)
    fm, _ = parse(text)
    return {
        "path": Path(path),
        "fm": fm,
        "raw": raw,
        "card": card_of(body) if tier in ("T1", "T2") else "",
        "body": body if tier == "T2" else "",
    }


# ---------------------------------------------------------------- public write


def _key_line(raw: str, key: str) -> int:
    for n, line in enumerate(raw.splitlines()):
        if line.startswith(f"{key}:"):
            return n
    return -1


def set_key(raw: str, key: str, value: str) -> str:
    """Replace one top-level key's scalar value. Every other byte survives, including a
    trailing comment on the same line."""
    lines = raw.splitlines()
    n = _key_line(raw, key)
    if n < 0:
        return raw + f"\n{key}: {value}"
    stripped = _strip_comment(lines[n])
    comment = lines[n][len(stripped):]
    lines[n] = f"{key}: {value}" + comment
    return "\n".join(lines)


def append_item(raw: str, key: str, item: str) -> str:
    """Append one item to a top-level block list, matching the block's own indentation."""
    lines = raw.splitlines()
    n = _key_line(raw, key)
    if n < 0:
        return raw + f"\n{key}:\n  - {item}"
    # An inline empty list (`verified: []`) becomes a block list on first append. Without
    # this the item lands under a surviving `[]` and parses back as empty — found by e4,
    # because e1's suite only ever appended to a list that already had items.
    head = _strip_comment(lines[n])
    if head.partition(":")[2].strip() == "[]":
        lines[n] = f"{key}:" + lines[n][len(head):]
    last, indent = n, "  "
    for i in range(n + 1, len(lines)):
        body = _strip_comment(lines[i])
        if body.strip().startswith("- "):
            last, indent = i, body[: len(body) - len(body.lstrip())]
        elif body.strip():
            break
    lines.insert(last + 1, f"{indent}- {item}")
    return "\n".join(lines)


def write(path: Path, text: str) -> None:
    """Atomic single-file replace. The temp file shares the target's directory, because
    `os.replace` is only atomic within one filesystem. On failure the original is
    untouched and no debris is left behind."""
    path = Path(path)
    tmp = path.with_name(f".{path.name}.tmp")
    try:
        with open(tmp, "w", encoding="utf-8") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink()


# ===================================================================== the graph (e2)
#
# One compiled graph, built from T0 reads. Every other verb reads this instead of walking
# the tree itself. Three rules from the format shape it:
#
# * **Edges come from an allowlist, never a heuristic** (§3.3). `scope:` holds repo paths and
#   `persona_corpus:` a config path; a scanner that guessed would read `templates/task.md.tmpl`
#   as a link to `/task.md` — observed 2026-07-29.
# * **Fragments resolve in a fixed order** (§3.3): frontmatter key first, heading slug second,
#   `edge_unresolved` third. Ordered, so one reference can never resolve two ways.
# * **Activity is derived, never stored** (§3.4). There is no pointer to corrupt.

EDGE_KEYS = ("depends_on", "needs", "tasks", "milestone", "relates_to", "task", "supersedes")
ACTIVE_STATES = ("direction", "build", "verify")
CACHE_NAME = "graph.json"


def cid_of(root: Path, path: Path) -> str:
    """A bundle-absolute concept ID (OKF §2): `/tasks/x.md`, never a filesystem path."""
    return "/" + Path(path).relative_to(root).as_posix()


def scan(root) -> dict:
    """Every node in the bundle at T0. Bodies are not read here (law 2)."""
    root = Path(root)
    graph = {}
    for path in sorted(root.rglob("*.md")):
        node = read(path, "T0")
        if node["fm"] is None:
            continue  # not a node — log.md and prose files are data, not graph
        node["cid"] = cid_of(root, path)
        node["root"] = root
        graph[node["cid"]] = node
    return graph


def _norm(src_cid: str, ref: str) -> str:
    """Resolve a reference to a cid. Bundle-absolute wins; relative resolves against `src`."""
    target = ref.partition("#")[0].strip()
    if not target:
        return src_cid
    if target.startswith("/"):
        return target
    base = PurePosixPath(src_cid).parent
    return "/" + str(PurePosixPath(os.path.normpath(str(base / target)))).lstrip("/")


def edges(graph: dict) -> list:
    """`[(src_cid, key, ref, target_cid|None)]` — typed, and only from EDGE_KEYS."""
    out = []
    for cid, node in graph.items():
        for key in EDGE_KEYS:
            value = (node["fm"] or {}).get(key)
            if value is None:
                continue
            for ref in value if isinstance(value, list) else [value]:
                ref = str(ref).strip()
                if ".md" not in ref:
                    continue
                target = _norm(cid, ref)
                out.append((cid, key, ref, target if target in graph else None))
    return out


def _section(body: str, slug: str) -> str:
    """The body section under the heading whose kebab-cased text is `slug`."""
    out, inside = [], False
    for line in body.splitlines(keepends=True):
        if line.startswith("#"):
            if inside:
                break
            text = line.lstrip("#").strip().lower()
            inside = "-".join(re.findall(r"[a-z0-9]+", text)) == slug
            continue
        if inside:
            out.append(line)
    return "".join(out).strip()


def resolve(graph: dict, ref: str, src: str = "") -> tuple:
    """`(cid, value, why)` under §3.3's ordered grammar.

    `why` is one of `node` · `frontmatter` · `heading` · `edge_unresolved`. Frontmatter wins
    even when a same-named heading exists, so a reference can never resolve two ways.
    """
    cid = _norm(src or ref, ref)
    fragment = ref.partition("#")[2].strip()
    node = graph.get(cid)
    if node is None:
        return cid, None, "edge_unresolved"
    if not fragment:
        return cid, node, "node"
    fm = node["fm"] or {}
    for key in (fragment, fragment.replace("-", "_")):
        if key in fm:
            return cid, fm[key], "frontmatter"
    # Only now is a body read, and only this one (law 2 — never a bulk scan).
    section = _section(read(node["path"], "T2")["body"], fragment)
    return (cid, section, "heading") if section else (cid, None, "edge_unresolved")


def active(graph: dict) -> list:
    """Active iff `status` is direction|build|verify (§3.4). Nothing is stored."""
    return sorted(c for c, n in graph.items()
                  if (n["fm"] or {}).get("status") in ACTIVE_STATES)


def ready(graph: dict) -> list:
    """Active tasks whose every `depends_on` target is `done` — the frontier."""
    out = []
    for cid in active(graph):
        node = graph[cid]
        if (node["fm"] or {}).get("type") != "Task":
            continue
        deps = (node["fm"] or {}).get("depends_on") or []
        if all((graph.get(_norm(cid, d), {}).get("fm") or {}).get("status") == "done"
               for d in (deps if isinstance(deps, list) else [deps])):
            out.append(cid)
    return out


def cycles(graph: dict) -> list:
    """Every dependency cycle, as lists of cids. Iterative, so a bad bundle reports (law 3).

    Tarjan's SCC with an explicit stack — a recursive walk would raise RecursionError on a
    deep or cyclic graph, which is the crash R:CYCLECRASH forbids.
    """
    adj = {c: [] for c in graph}
    for src, key, ref, target in edges(graph):
        if target and key in ("depends_on", "needs", "supersedes"):
            adj[src].append(target)

    index, low, on, stack, counter, found = {}, {}, set(), [], [0], []
    for start in graph:
        if start in index:
            continue
        work = [(start, iter(adj[start]))]
        index[start] = low[start] = counter[0]; counter[0] += 1
        stack.append(start); on.add(start)
        while work:
            node, children = work[-1]
            nxt = next(children, None)
            if nxt is None:
                work.pop()
                if work:
                    low[work[-1][0]] = min(low[work[-1][0]], low[node])
                if low[node] == index[node]:
                    comp = []
                    while True:
                        w = stack.pop(); on.discard(w); comp.append(w)
                        if w == node:
                            break
                    if len(comp) > 1 or node in adj[node]:
                        found.append(sorted(comp))
            elif nxt not in index:
                index[nxt] = low[nxt] = counter[0]; counter[0] += 1
                stack.append(nxt); on.add(nxt)
                work.append((nxt, iter(adj[nxt])))
            elif nxt in on:
                low[node] = min(low[node], index[nxt])
    return found


def load(root, cache: bool = True) -> dict:
    """The graph, always from the files.

    `graph.json` is an **export**, not an optimisation: FORMAT §4 lets a consumer read the
    graph at T0 without this engine. It is written, never read back, which is what makes
    R:CACHEAUTH structurally impossible rather than merely tested — a cache that is never
    consulted cannot outrank the files.
    """
    graph = scan(root)
    if cache:
        try:
            payload = {
                "nodes": {c: (n["fm"] or {}) for c, n in graph.items()},
                "edges": [[s, k, r, t] for s, k, r, t in edges(graph)],
            }
            write(Path(root) / CACHE_NAME, json.dumps(payload, indent=1, sort_keys=True) + "\n")
        except OSError:
            pass  # a read-only bundle is legal; the export is a convenience, never a dependency
    return graph


# ======================================================================= init (e3)
#
# A profile selects which SPEC LENSES a bundle gets — never which rules apply. It is a
# dict, so adding one is data, not an engine branch (goal 2's closed-lens claim, tested by
# adding a profile at runtime). `code` and `doc` ship as engine data; the remaining three
# ship as template files (amendment A1).

PROFILES = {
    "code": {
        "domain": "what the product must be true about",
        "system": "how it is built, and what that forecloses",
        "experience": "who uses it and what they feel",
        "quality": "what counts as proof",
        "method": "how work proceeds, and what a gate costs",
    },
    "doc": {
        "domain": "what the document must get right",
        "experience": "who reads it and what they need",
        "quality": "what counts as proof, when there is no test runner",
        "method": "how drafts proceed to a gate",
    },
}

RESERVED_FILES = ("index.md", "log.md", "PROJECT.md")


def _stamp(by: str = "add/3.0.0") -> str:
    return f"generated: {{ by: {by}, at: {_today()} }}"


def _today() -> str:
    import datetime
    return datetime.date.today().isoformat()


def init(root, profile: str = "code", title: str = None) -> tuple:
    """Create a conforming bundle. Never overwrites; an existing file is left alone.

    Returns `(graph, created_cids, note)`. The note ends in a `next:` line, because a verb
    that does not say what comes next teaches nothing (law 4).
    """
    root, created = Path(root), []
    lenses = PROFILES.get(profile) or PROFILES["code"]
    title = title or root.resolve().name

    def put(rel: str, text: str):
        path = root / rel
        if path.exists():
            return  # M2 — a human's file always outranks a template
        path.parent.mkdir(parents=True, exist_ok=True)
        write(path, text)
        created.append("/" + rel)

    put("index.md", f'---\nokf_version: "0.2"\nabf_version: "1.3"\nname: {root.resolve().name}\n'
                    f"profile: {profile}\nengine: add/3.0.0\ncreated: {_today()}\n"
                    f"sensitive_paths: []\n{_stamp()}\n---\n\n"
                    "<!-- COMPILED BODY (A11) — regenerated by the engine; do not hand-maintain. -->\n")
    put("log.md", "# log\n\n<!-- COMPILED BODY (A20) — rendered from node `verified[]` stamps.\n"
                  "     Humans write in `## Notes` only. -->\n\n## Notes\n")
    put("PROJECT.md", f"---\ntype: Project\ntitle: {title}\ngoal: <one sentence — what is true when this ships>\n"
                      f"stage: mvp\nprofile: {profile}\n{_stamp()}\n---\n"
                      f"## CARD\ngoal: <the one line a cold reader needs>\nstate: initialised\n"
                      f"next: add new milestone <slug>\n")
    for slug, goal in lenses.items():
        put(f"specs/{slug}.md",
            f"---\ntype: Spec\ntitle: {slug.title()}\nlens: {slug}\nproject: {title}\n{_stamp()}\n---\n"
            f"## Now\n{goal}\n\n## Decisions that bind\n- <the first decision that constrains the rest>\n\n"
            f"## Deltas\n- <what changed, and the evidence that changed it>\n")

    note = (f"created {len(created)} files ({profile} profile)" if created
            else "bundle already exists — nothing written")
    return load(root), created, f"{note}\nnext: add new milestone <slug>"


# ============================================== new · freeze · done — transitions (e4)
#
# One shared write path (`_transition`) serves all three verbs, per amendment A1. Two rules
# decide the shape:
#
# * **A notary refuses to forge, never to record.** `done` will not CREATE a `status: done`
#   that no gate stamp entitles — signing an unsigned document is not notarising it. But it
#   never prevents a human from writing their own stamp with their own authority. That is
#   the line between law 3's notary and the guard it forbids.
# * **Authority is computed, never passed.** A caller cannot argue its way below the floor,
#   because the floor is derived from the node and the index, not from an argument.

AUTHORITY_ORDER = ("process", "ai-verify", "plan", "human")
SENSITIVITY_FLOOR = {
    "mechanical": "process",
    "data": "plan",
    "architecture": "plan",
    "security": "human",
}
TYPE_DIR = {"Task": "tasks", "Milestone": "milestones", "Spec": "specs",
            "Persona": "personas", "Prompt": "prompts", "Run": "runs"}
BODIES = {
    "Task": "## CARD\ngoal: <one line>\nbeat: direction · next: add freeze {slug}\n\n"
            "## RULES\n<must>\n- M1 <the rule that must hold>\n</must>\n<reject>\n"
            "- R:<NAME> <what must never happen> -> \"<NAME>\"\n</reject>\n\n"
            "## PLAN\ncontract: <the shape this publishes>\nscope: <files>\n\n"
            "## CHECKS\n- <test_name> · covers: M1 · <what it proves>\nred-first: every check MUST fail first.\n\n"
            "## EVIDENCE\nreceipt: <runs/<n>.md>\ngate: <PASS | RISK-ACCEPTED | HARD-STOP>\n\n"
            "## LESSONS\n- <lesson> -> add learn <lens>\n",
    "Milestone": "## CARD\ngoal: <one line>\nnext: add new task <slug>\n\n## SCOPE\nIn:  <what>\nOut: <what not>\n\n"
                 "## GROUND\ntouches: <paths>\nrisks:\n  - <the one that would hurt>\n\n"
                 "## EXIT\n- [ ] <criterion>   (← <task>)\n\n## CLOSE\nevidence: <one row per task>\n",
}


def authority_for(graph: dict, cid: str) -> str:
    """`max(sensitivity floor, A17 sensitive-path floor)` — FORMAT §3.1.

    A17 is a path match against `index.md`'s `sensitive_paths:`, so a notary may perform it:
    it is mechanical, and it outranks the declared `sensitivity:` in one direction only.
    """
    import fnmatch
    node = graph.get(cid) or {}
    fm = node.get("fm") or {}
    floor = SENSITIVITY_FLOOR.get(fm.get("sensitivity"), "process")

    patterns = ((graph.get("/index.md", {}).get("fm") or {}).get("sensitive_paths")) or []
    scope = fm.get("scope") or []
    for entry in (scope if isinstance(scope, list) else [scope]):
        for pattern in (patterns if isinstance(patterns, list) else [patterns]):
            if fnmatch.fnmatch(str(entry), str(pattern)) or str(entry).startswith(
                    str(pattern).replace("**", "").replace("*", "").rstrip("/")):
                return "human"  # A17 — unstrikeable, and never lowered
    return floor


def _transition(root, cid: str, sets: dict = None, appends: list = None) -> tuple:
    """The one write path. Surgical edits on RAW text, then an atomic replace."""
    path = Path(root) / cid.lstrip("/")
    if not path.is_file():
        return None, f"no such node: {cid}"
    node = read(path, "T2")
    raw = node["raw"]
    for key, value in (sets or {}).items():
        raw = set_key(raw, key, value)
    for key, item in (appends or []):
        raw = append_item(raw, key, item)
    write(path, f"---\n{raw}\n---\n{node['body']}")
    return read(path, "T0"), ""


def new(root, node_type: str, slug: str, **fields) -> tuple:
    """Create a typed node. A colliding slug reports and writes nothing (R:DUPSLUG)."""
    root = Path(root)
    rel = f"{TYPE_DIR.get(node_type, 'tasks')}/{slug}.md"
    path = root / rel
    if path.exists():
        return None, f"slug already taken: {slug} ({rel})\nnext: pick another slug, or `add status` to see it"

    order = ["type", "title", "goal", "status", "depth", "kind", "sensitivity", "milestone", "scope"]
    fm = {"type": node_type, "title": fields.pop("title", slug), "status": "direction"}
    fm.update({k: v for k, v in fields.items() if v is not None})
    lines = []
    for key in order + [k for k in fm if k not in order]:
        if key not in fm:
            continue
        value = fm[key]
        if isinstance(value, list):
            lines.append(f"{key}:\n" + "\n".join(f"  - {v}" for v in value))
        else:
            lines.append(f"{key}: {value}")
    lines += [_stamp(), "verified: []"]

    path.parent.mkdir(parents=True, exist_ok=True)
    write(path, "---\n" + "\n".join(lines) + "\n---\n" + BODIES.get(node_type, "## CARD\ngoal: <one line>\n"))
    return "/" + rel, f"created {rel}\nnext: add freeze {slug}"


def freeze(root, cid: str, by: str, authority: str = None) -> tuple:
    """Append a freeze stamp. A second freeze REFREEZES — §3.5, history is append-only."""
    graph = scan(root)
    authority = authority or authority_for(graph, cid)
    stamps = ((graph.get(cid) or {}).get("fm") or {}).get("verified") or []
    act = "refreeze" if any(s.get("act") in ("freeze", "refreeze") for s in stamps
                            if isinstance(s, dict)) else "freeze"
    node, err = _transition(root, cid, appends=[
        ("verified", f'{{ by: "{by}", at: {_today()}, act: {act}, authority: {authority} }}')])
    if err:
        return None, err + "\nnext: add status"
    return node, f"{act} recorded at authority `{authority}`\nnext: build, then `add run -- <cmd>`"


def done(root, cid: str) -> tuple:
    """Transition to `done` only when a gate stamp entitles it.

    Refusing to create an unsupported record is the notary's duty, not guarding: this never
    prevents a human from writing the stamp themselves with their own authority.
    """
    graph = scan(root)
    node = graph.get(cid)
    if node is None:
        return False, ["node"], f"no such node: {cid}\nnext: add status"

    required = authority_for(graph, cid)
    stamps = [s for s in ((node["fm"] or {}).get("verified") or []) if isinstance(s, dict)]
    gates = [s for s in stamps if s.get("act") == "gate"]
    entitled = [s for s in gates
                if AUTHORITY_ORDER.index(str(s.get("authority", "process"))) >=
                AUTHORITY_ORDER.index(required)]

    missing = []
    if not gates:
        missing.append(f"a gate stamp (none recorded; `{required}` or above is required)")
    elif not entitled:
        missing.append(f"a gate at authority `{required}` — highest recorded is "
                       f"`{max(gates, key=lambda s: AUTHORITY_ORDER.index(str(s.get('authority', 'process')))).get('authority')}`")
    if missing:
        return False, missing, ("cannot record `done` — " + "; ".join(missing) +
                                f"\nnext: add gate {cid.rsplit('/', 1)[-1][:-3]}")

    _transition(root, cid, sets={"status": "done"})
    return True, [], f"{cid} is done\nnext: add status"


# ================================================ status — orientation and its flags (e6)
#
# Everything here reads e2's compiled graph; no verb walks the tree. Three rules bind:
#
# * **Bounded, always** (A12). Output must not grow with the bundle: 20 node lines and a
#   count. A report that becomes a context hazard defeats the format it reports on.
# * **Stamps, never mtime** (A22). The M0 kill-test proved mtime worthless across a
#   checkout, so `--since` reads recorded acts.
# * **Report, never block** (law 3). The one write here is `render_card`, and it repairs
#   the contradiction e4's transition created rather than displaying it as current.

MAX_LINES = 20
BEAT_KEYS = ("beat", "state")
# What a cold reader needs, in order. `Run` is absent on purpose — see `status`.
ORIENT_RANK = {"Project": 0, "Milestone": 1, "Task": 2, "Spec": 5, "Persona": 6, "Prompt": 7}


def locate(graph: dict, term: str) -> list:
    """Cids whose slug or title contains `term`. A human should never need a path."""
    term = term.lower()
    return sorted(cid for cid, n in graph.items()
                  if term in cid.rsplit("/", 1)[-1][:-3].lower()
                  or term in str((n["fm"] or {}).get("title", "")).lower())


def graph_lines(graph: dict, milestone_cid: str) -> list:
    """The DAG for ONE milestone. Never whole-bundle — that is the A12 hazard."""
    node = graph.get(milestone_cid)
    if node is None:
        return [f"no such milestone: {milestone_cid}"]
    members = list((node["fm"] or {}).get("tasks") or [])
    # A task may be listed by the milestone, or may name the milestone itself. Honour both:
    # `new` writes the back-reference, so a graph that read only `tasks:` would show nothing.
    members += [c for c, n in graph.items()
                if (n["fm"] or {}).get("milestone") == milestone_cid and c not in members]
    out = [f"{milestone_cid}  {(node['fm'] or {}).get('title', '')}"]
    for ref in sorted(set(str(m) for m in members)):
        cid = _norm(milestone_cid, str(ref))
        task = graph.get(cid)
        if task is None:
            out.append(f"  ? {ref}  (unresolved)")
            continue
        fm = task["fm"] or {}
        deps = [str(d).rsplit("/", 1)[-1][:-3] for d in (fm.get("depends_on") or [])]
        out.append(f"  {'x' if fm.get('status') == 'done' else 'o'} {cid.rsplit('/', 1)[-1][:-3]}"
                   f"  [{fm.get('status', '?')}]" + (f"  <- {', '.join(deps)}" if deps else ""))
    return out


def since(graph: dict, date: str) -> list:
    """`[(at, cid, act, by)]` from `verified[]` — recorded acts, never file mtimes (A22)."""
    rows = []
    for cid, node in graph.items():
        for stamp in ((node["fm"] or {}).get("verified") or []):
            if isinstance(stamp, dict) and str(stamp.get("at", "")) >= date:
                rows.append((str(stamp.get("at")), cid, stamp.get("act"), stamp.get("by")))
    return sorted(rows, reverse=True)


def card_drift(graph: dict) -> list:
    """Nodes whose `## CARD` contradicts frontmatter — the defect e4's transition created.

    `[(cid, key, card_says, fm_says)]`. Reporting it is the notary's job; `render_card`
    repairs it.
    """
    out = []
    for cid, node in graph.items():
        status = (node["fm"] or {}).get("status")
        if not status:
            continue
        card = card_of(read(node["path"], "T2")["body"])
        for line in card.splitlines():
            key, sep, value = line.partition(":")
            if sep and key.strip() in BEAT_KEYS:
                said = value.split("·")[0].strip()
                if said and said != status and said in ("direction", "build", "verify", "done"):
                    out.append((cid, key.strip(), said, status))
    return out


def render_card(root, cid: str) -> tuple:
    """Repair a stale CARD beat line. Surgical: exactly one line changes, or none."""
    graph = scan(root)
    drift = [d for d in card_drift(graph) if d[0] == cid]
    if not drift:
        return False, "card is current"
    _, key, said, status = drift[0]
    path = Path(root) / cid.lstrip("/")
    node = read(path, "T2")
    lines = node["body"].splitlines(keepends=True)
    for i, line in enumerate(lines):
        if line.startswith(f"{key}:") and said in line:
            lines[i] = line.replace(said, status, 1)
            break
    write(path, f"---\n{node['raw']}\n---\n{''.join(lines)}")
    return True, f"{cid}: {key} {said} -> {status}\nnext: add status"


def status(root, locate_term: str = None, milestone: str = None,
           since_date: str = None, all: bool = False, check: bool = False) -> str:
    """One bounded orientation report, ending in a runnable `next:` line.

    `check=True` adds the CARD-drift scan. It is OPT-IN because detecting drift requires
    reading every node's CARD, and M1 holds this verb to T0. Orientation must stay cheap;
    the deeper pass belongs to `doctor --sync`.
    """
    graph = scan(root)
    out = []

    if locate_term:
        found = locate(graph, locate_term)
        out += [f"· {c}" for c in found[:MAX_LINES]] or ["no match"]
        return "\n".join(out + [f"next: add status --graph <milestone>"])
    if milestone:
        return "\n".join(graph_lines(graph, milestone) + ["next: add status"])
    if since_date:
        rows = since(graph, since_date)
        out += [f"· {at}  {cid}  {act} by {by}" for at, cid, act, by in rows[:MAX_LINES]]
        return "\n".join((out or [f"nothing recorded since {since_date}"]) + ["next: add status"])

    project = next((n for n in graph.values() if (n["fm"] or {}).get("type") == "Project"), None)
    out.append(f"{((project or {}).get('fm') or {}).get('title', Path(root).name)}"
               f"  ·  {len(graph)} nodes")

    # Orientation is about WORK. Receipts are evidence — reachable from the task that owns
    # them, and never the thing a cold reader needs first. Ordering by ORIENT_RANK keeps the
    # 20-line budget spent on milestones and tasks rather than on files named `1.md`.
    def keep(cid):
        fm = graph[cid]["fm"] or {}
        if fm.get("type") == "Run":
            return False
        return all or fm.get("status") not in ("done", "dropped")

    shown = sorted((c for c in graph if keep(c)),
                   key=lambda c: (ORIENT_RANK.get((graph[c]["fm"] or {}).get("type"), 9), c))
    for cid in shown[:MAX_LINES]:
        fm = graph[cid]["fm"] or {}
        out.append(f"  · {cid.rsplit('/', 1)[-1][:-3]:<28} [{fm.get('status', '—')}] {fm.get('type', '')}")
    if len(shown) > MAX_LINES:
        out.append(f"  … {len(shown) - MAX_LINES} more of {len(shown)} (`--all` for done nodes)")

    drift = card_drift(graph) if check else []
    if drift:
        out.append(f"  ! {len(drift)} node(s) whose CARD contradicts frontmatter — `add doctor --sync`")

    frontier = ready(graph)
    waiting = [c for c in active(graph) if (graph[c]["fm"] or {}).get("status") == "verify"]
    if waiting:
        nxt = f"next: add gate {waiting[0].rsplit('/', 1)[-1][:-3]}"
    elif frontier:
        nxt = f"next: add brief {frontier[0].rsplit('/', 1)[-1][:-3]}"
    elif any((n["fm"] or {}).get("type") == "Milestone" for n in graph.values()):
        nxt = "next: add new task <slug>"
    else:
        nxt = "next: add new milestone <slug>"
    return "\n".join(out + [nxt])


# ============================ run · freshness · learn — the receipt layer (e7)
#
# This module pays the A22 debt. A receipt is fresh when the code it observed is the code
# that exists now, and "now" is decided by CONTENT, not by timestamps:
#
#   `git worktree add` sets every checked-out file's mtime to checkout time. Under the
#   mtime predicate every committed receipt reads stale in a fresh clone, worktree or CI
#   job — deterministically, and hardest on the two designs this format promotes. Blob
#   hashes do not move when a file is checked out, so they answer the question actually
#   being asked: is this the same code?
#
# `run` executes the command the AGENT supplied and notarises the result. It never runs
# anything on its own initiative, and it is always bounded by a timeout — a hang is a
# recorded outcome, not a lost session.

RUN_TIMEOUT = 900


def _git(root, *args, timeout: int = 30):
    """Run one git command. Returns None when git is absent or the tree is not a repo."""
    try:
        done = subprocess.run(["git", *args], cwd=str(root), capture_output=True,
                              text=True, timeout=timeout)
    except (OSError, subprocess.SubprocessError):
        return None
    return done.stdout.strip() if done.returncode == 0 else None


def scope_digest(root, scope: list) -> list:
    """`[{path, blob}]` — git blob hashes over the freshness set (FORMAT §8.1, A22).

    Outside a git working tree this returns `[]`, and the caller must declare
    `freshness: mtime` rather than pretend to a content digest it cannot compute.
    """
    root = Path(root)
    if _git(root, "rev-parse", "--git-dir") is None:
        return []
    out = []
    for entry in sorted(str(s) for s in (scope or [])):
        for path in sorted(root.glob(entry)) if any(c in entry for c in "*?[") else [root / entry]:
            if not path.is_file():
                continue
            blob = _git(root, "hash-object", str(path.relative_to(root)))
            if blob:
                out.append({"path": path.relative_to(root).as_posix(), "blob": f"sha1:{blob}"})
    return out


def fresh(receipt: dict, root) -> tuple:
    """`(ok, why)` — recompute the digest and compare. Any difference is stale."""
    root = Path(root)
    recorded = receipt.get("scope_digest") or []
    if receipt.get("freshness") != "content" or not recorded:
        return False, "receipt carries no content digest — freshness cannot be established"
    for entry in recorded:
        path = root / str(entry.get("path"))
        if not path.is_file():
            return False, f"{entry.get('path')} has vanished since the run"
        blob = _git(root, "hash-object", str(path.relative_to(root)))
        if blob is None or f"sha1:{blob}" != entry.get("blob"):
            return False, f"{entry.get('path')} changed since the run"
    return True, "every file in scope is byte-identical to the run"


def run(root, cid: str, command: list, cwd=None, timeout: int = RUN_TIMEOUT, junit=None) -> dict:
    """Execute the agent's own command, notarise the result as a Run node.

    Never executes anything the caller did not supply. A non-zero exit and a timeout are
    both recorded outcomes — this function does not raise on a failing command (law 3).
    """
    root, cwd = Path(root), Path(cwd or root)
    node = (scan(root).get(cid) or {})
    scope = ((node.get("fm") or {}).get("scope")) or []
    digest = scope_digest(cwd, scope)

    try:
        done = subprocess.run([str(c) for c in command], cwd=str(cwd),
                              capture_output=True, text=True, timeout=timeout)
        exit_code, stdout, note = done.returncode, done.stdout[-2000:], ""
    except subprocess.TimeoutExpired:
        exit_code, stdout, note = 124, "", f"timeout after {timeout}s — recorded, not raised"
    except OSError as err:
        exit_code, stdout, note = 127, "", f"could not start the command: {err}"

    slug = cid.rsplit("/", 1)[-1][:-3]
    runs = root / f"tasks/{slug}.d/runs"
    runs.mkdir(parents=True, exist_ok=True)
    n = len(list(runs.glob("*.md"))) + 1
    # A24: the evidence kind is EARNED, never assumed. `test-ids` requires IDs a runner
    # actually reported — e12 owes that extraction. Until then the honest kind for a bare
    # command is `command-exit`. Freshness is a separate question from evidence, and wiring
    # both to the presence of a digest (as this first did) claims proof that does not exist.
    # A24's ladder is climbed only with real IDs (e12). No report, no promotion.
    ids = extract_ids(junit) if junit else {}
    # A24 needs the ID NAMES, not a count: `gate` binds the node's `covers:` against what the
    # runner reported, and "2/2 reported" cannot be bound to anything. Recording every ID of a
    # 113-test suite would bloat the receipt, so this records exactly the evidence the node's
    # own claims need — the IDs it cites that passed — plus EVERY failure, which is always
    # relevant whether the node cites it or not.
    cited = {c for ids_ in covers(read(node["path"], "T2") if node else {}).values() for c in ids_} \
        if node else set()
    passed = sorted(i for i, v in ids.items() if v == "pass" and i in cited)
    failed = sorted(i for i, v in ids.items() if v != "pass")
    receipt = {"kind": "test-ids" if ids else "command-exit",
               "ids": f"{sum(v == 'pass' for v in ids.values())}/{len(ids)} reported" if ids else "unknown",
               "exit": exit_code,
               "freshness": "content" if digest else "mtime", "at": _today(),
               "stdout": stdout.strip().splitlines()[-1] if stdout.strip() else "",
               "note": note}
    body = (f"---\ntype: Run\nruntime: process\ntask: {cid}\n"
            f'computation: "{" ".join(str(c) for c in command)}"\n'
            f"receipt:\n" + "".join(f"  {k}: {v!r}\n" if k in ("stdout", "note") else f"  {k}: {v}\n"
                                    for k, v in receipt.items()) +
            ("  passed:\n" + "".join(f"    - {i}\n" for i in passed) if passed else "") +
            ("  failed:\n" + "".join(f"    - {i}\n" for i in failed) if failed else "") +
            ("  scope_digest:\n" + "".join(
                f'    - {{ path: {d["path"]}, blob: "{d["blob"]}" }}\n' for d in digest) if digest else "") +
            f"{_stamp('process:run')}\n---\n")
    write(runs / f"{n}.md", body)
    receipt = dict(receipt, passed=passed, failed=failed, scope_digest=digest)  # F3: the returned
    # copy is the receipt, digest included — a caller passing it to `fresh()` must get the truth.
    cid_run = "/" + str((runs / f"{n}.md").relative_to(root))
    # F3: bind the receipt to the task. A receipt no stamp points at is unreachable evidence.
    _transition(root, cid, appends=[("verified",
        f'{{ by: "process:run", at: {_today()}, act: run, authority: process, '
        f'outcome: {"PASS" if exit_code == 0 else "FAIL"}, receipt: {cid_run} }}')])
    return {"path": runs / f"{n}.md", "receipt": receipt, "computation": " ".join(str(c) for c in command),
            "note": f"receipt {n} recorded (exit {exit_code})\nnext: add gate {slug}"}


def learn(root, lens: str, lesson: str, evidence: str = None) -> tuple:
    """Append a lesson to a spec's `## Deltas`. Evidence is required, not decorative.

    A lesson with no evidence is an opinion, and a spec full of opinions is the thing this
    method exists to replace.
    """
    if not evidence:
        return False, "refused: a lesson needs evidence — cite the receipt or decision that caused it"
    path = Path(root) / "specs" / f"{lens}.md"
    if not path.is_file():
        return False, f"no such spec lens: {lens}\nnext: add status"
    node = read(path, "T2")
    lines = node["body"].splitlines(keepends=True)
    entry = f"- {lesson} — evidence: {evidence} ({_today()})\n"
    for i, line in enumerate(lines):
        if line.startswith("## Deltas"):
            lines.insert(i + 2 if i + 1 < len(lines) else i + 1, entry)
            break
    else:
        lines += ["\n## Deltas\n\n", entry]
    write(path, f"---\n{node['raw']}\n---\n{''.join(lines)}")
    return True, f"recorded on specs/{lens}\nnext: add status"


# ================================== the covers: binding — evidence that earns its name (e12)
#
# A15's finding: `covers:` was a LABEL. A task could claim a Must was proven by a check that
# never ran, and nothing noticed. Here a Must is proven only by a check ID the RUNNER
# reported passing — not by a string in a markdown table.
#
# This also closes the gap e7 left: `test-ids` was unreachable, so every receipt degraded to
# `command-exit`. An evidence kind that can never be earned is not a ladder, it is a label —
# the same defect A15 found, one level up.

# FORMAT §6.1's `covers-grammar`, stated ONCE here and reused. e15 closed F1 by holding
# FORMAT, the validator and this engine to one grammar; a second copy in this file would
# reopen R:DRIFT inside the engine itself.
RULE_ALT = r"M\d+|R:[A-Z0-9_]+"
RULE_ID = re.compile(rf"^-\s+({RULE_ALT})\b")
REFERENT = re.compile(rf"\A({RULE_ALT}|goal|G\d+)\Z")
COVERS_IN_CHECK = re.compile(r"^-\s+(\S+)\s+·\s*covers:\s*([^·]+?)\s*·")


def _section_of(body: str, heading: str) -> str:
    out, inside = [], False
    for line in body.splitlines(keepends=True):
        if line.startswith("## "):
            if inside:
                break
            inside = line.strip().lower() == f"## {heading}".lower()
            continue
        if inside:
            out.append(line)
    return "".join(out)


PLACEHOLDER = re.compile(r"<[a-z_][^>]*>")


def placeholders_in(node: dict) -> list:
    """Template tokens still standing in a node's RULES or CHECKS.

    `new` ships `- M1 <the rule that must hold>` and `- <test_name> · covers: M1`. Those parse as
    a real rule and a real check, so an unauthored node refuses at the gate with "M1 has no
    reported passing check" — true, and it points at RISK-ACCEPTED when the fix is to author the
    node. Naming the placeholder turns a confusing refusal into an actionable one (M4).
    """
    found = []
    for heading in ("RULES", "CHECKS"):
        for line in _section_of(node.get("body") or "", heading).splitlines():
            if line.startswith("- ") and PLACEHOLDER.search(line):
                found.append(line.strip())
    return found


def rules_of(node: dict) -> list:
    """Every Must and Reject id declared in the node's RULES section."""
    body = read(node["path"], "T2")["body"]
    return [m.group(1) for m in (RULE_ID.match(l) for l in _section_of(body, "RULES").splitlines()) if m]


def covers(node: dict) -> dict:
    """`{rule_id: [check_id, ...]}` — parsed from the CHECKS section, keyed by rule."""
    body = read(node["path"], "T2")["body"]
    out = {}
    for line in _section_of(body, "CHECKS").splitlines():
        match = COVERS_IN_CHECK.match(line.strip())
        if not match:
            continue
        check = match.group(1)
        for rule in (r.strip() for r in match.group(2).split(",")):
            if rule:
                out.setdefault(rule, []).append(check)
    return out


def bind(node: dict, reported: dict) -> tuple:
    """`(proven, unproven)` — a rule is proven only by a check the runner reported PASSING.

    `reported` is `{check_id: "pass" | "fail"}` from `extract_ids`. A check that is absent
    did not run; a check that failed did not prove. Neither counts.
    """
    proven, unproven = {}, {}
    for rule, checks in covers(node).items():
        passing = [c for c in checks if reported.get(c) == "pass"]
        (proven if passing else unproven)[rule] = passing or checks
    return proven, unproven


def unbound(node: dict, reported: dict) -> list:
    """Rules with no passing check — declared but unproven. The honest gap."""
    mapped = covers(node)
    proven, _ = bind(node, reported)
    return sorted(r for r in rules_of(node) if r not in proven or not mapped.get(r))


def extract_ids(path) -> dict:
    """`{check_id: "pass"|"fail"}` from junit-xml. Unreadable output yields `{}`, never a guess.

    junit-xml only at v1.0 (amendment A1). A runner that emits nothing usable leaves the
    receipt at a weaker kind, which A24 requires it to say out loud.
    """
    import xml.etree.ElementTree as ET
    try:
        root = ET.parse(str(path)).getroot()
    except (OSError, ET.ParseError):
        return {}
    out = {}
    for case in root.iter("testcase"):
        name = case.get("name")
        if not name:
            continue
        bad = any(case.find(tag) is not None for tag in ("failure", "error"))
        out[name] = "fail" if bad else "pass"
    return out


# ================================================== brief — refs, not prose (e5)
#
# One rule decides this whole verb: **T2 is single-node** (FORMAT §4). A brief carries the
# subject's own body, T1 CARDs of its `depends_on`, the `#gives` fragments it `needs:`, and
# the five specs' bind lines. Nothing else can leak in, because nothing else is READ.
#
# Two units live here and they are not the same. FORMAT §7.2 states the ceiling in BYTES;
# PROPOSAL §3d states the lane budgets in TOKENS. The engine has no tokenizer and may not
# acquire one (D-1, stdlib only), so bytes are enforced and tokens are printed at a DECLARED
# ratio. A1 cost this project an amendment for exactly this class of mistake; naming the unit
# in the output is the whole fix.

BRIEF_BUDGET = {"quick": 8_000, "standard": 24_000, "deep": 40_000}
BYTES_PER_TOKEN = 4
PHASE_EVIDENCE = {"direction": "none", "build": "run-receipt",
                  "verify": "run-receipt,covers-bound"}
PHASE_OF = {"direction": "direction", "build": "build", "verify": "verify",
            "done": "verify", "dropped": "verify"}


def brief_budget(depth: str) -> int:
    return BRIEF_BUDGET.get(str(depth or "standard"), BRIEF_BUDGET["standard"])


def bind_sections(root) -> list:
    """The five specs' `Decisions that bind`, sorted — the ONLY spec section a brief may cite.

    Sorted by filename, so A16's determinism is structural: there is no dict order, no
    `set`, and no `glob` order to depend on.
    """
    out = []
    for path in sorted((Path(root) / "specs").glob("*.md")):
        text = _section(read(path, "T2")["body"], "decisions-that-bind")
        if text:
            out.append((f"specs/{path.stem}", text))
    return out


def _flat(value) -> str:
    """A resolved ref's value as text. A `gives:` list renders as a list, not as a repr."""
    if isinstance(value, list):
        return "\n".join(f"- {v}" for v in value)
    if isinstance(value, dict):
        return "\n".join(f"{k}: {v}" for k, v in value.items())
    return str(value)


def brief(root, cid: str, phase: str = None, for_subagent: bool = False,
          evidence: list = None) -> dict:
    """Compile the XML brief for one node. Deterministic, budgeted, and self-measuring."""
    root = Path(root)
    graph = scan(root)
    node = graph.get(cid)
    if node is None:
        return {"text": f'<task unresolved="true" id="{cid}"/>\nnext: add status\n',
                "bytes": 0, "hash": "", "nodes": 0, "budget": 0, "degraded": [],
                "phase": phase or "build", "depth": "standard"}

    fm = node["fm"] or {}
    slug = cid.rsplit("/", 1)[-1][:-3]
    ident = cid.strip("/")[:-3]
    phase = phase or PHASE_OF.get(str(fm.get("status", "")), "build")
    depth = str(fm.get("depth") or "standard")
    budget = brief_budget(depth)
    body = read(node["path"], "T2")["body"]

    cards = []
    for dep in sorted(str(d) for d in (fm.get("depends_on") or [])):
        dcid, dnode, _ = resolve(graph, dep, cid)
        cards.append((dcid.strip("/")[:-3], read(dnode["path"], "T1")["card"] if dnode else None))
    refs = []
    for need in sorted(str(n) for n in (fm.get("needs") or [])):
        _, value, why = resolve(graph, need, cid)
        # Strip `.md` from the PATH only. Applying it to the whole ref ate the fragment's last
        # two characters — `#gives` became `#gi` — and a ref an agent cannot resolve back is
        # not a reference. The suite checked the resolved value and never the id.
        path, _, frag = need.partition("#")
        ident_ref = path.strip("/")[:-3] if path.endswith(".md") else path.strip("/")
        refs.append((f"{ident_ref}#{frag}" if frag else ident_ref,
                     None if why == "edge_unresolved" else _flat(value)))
    binds = bind_sections(root)

    persona = None
    if fm.get("persona"):
        pcid, pnode, _ = resolve(graph, str(fm["persona"]), cid)
        # T0 only — `raw` is the frontmatter text `scan` already holds. The body is never
        # opened, so D-4 ("the corpus is referenced, never vendored") holds structurally
        # rather than by a filter that could be forgotten.
        if pnode:
            persona = (pcid.strip("/")[:-3], pnode["raw"])

    quoted = []
    for src in (evidence or []):
        src = Path(src)
        try:
            origin = str(src.relative_to(root.parent))
        except ValueError:
            origin = src.name          # never an absolute path: it would break A16 per machine
        try:
            quoted.append((origin, src.read_text()))
        except OSError as err:
            quoted.append((origin, f"unreadable: {err}"))

    nodes = 1 + len(cards) + len(binds) + (1 if persona else 0)
    constraints = ("never weaken a check · never edit a frozen `gives` · T2 is single-node · "
                   f"scope: {' · '.join(str(s) for s in (fm.get('scope') or ['—']))}")

    def assemble(drop_specs: bool, drop_cards: bool) -> str:
        out = [f'<task id="{ident}" phase="{phase}" depth="{depth}"'
               + (' standalone="true">' if for_subagent else ">"),
               f"  <objective>{fm.get('goal') or fm.get('title') or ''}</objective>"]
        if persona:
            out.append(f'  <persona ref="{persona[0]}" inject="frontmatter">')
            out += ["    " + l for l in persona[1].splitlines()]
            out.append("  </persona>")
        out.append("  <context>")
        for dcid, card in cards:
            if card is None:
                out.append(f'    <card id="{dcid}" unresolved="true"/>')
            elif drop_cards:
                out.append(f'    <card id="{dcid}" omitted="budget"/>')
            else:
                out.append(f'    <card id="{dcid}">')
                out += ["      " + l for l in card.splitlines()]
                out.append("    </card>")
        for ref, value in refs:
            if value is None:
                out.append(f'    <ref id="{ref}" unresolved="true"/>')
            else:
                out.append(f'    <ref id="{ref}" frozen="true">')
                out += ["      " + l for l in value.splitlines()]
                out.append("    </ref>")
        for scid, text in binds:
            rid = f"{scid}#decisions-that-bind"
            if drop_specs:
                out.append(f'    <ref id="{rid}" omitted="budget"/>')
            else:
                out.append(f'    <ref id="{rid}">')
                out += ["      " + l for l in text.splitlines()]
                out.append("    </ref>")
        out.append("  </context>")
        # The subject is emitted VERBATIM and unindented. R:SILENTCUT forbids trimming it, and
        # reformatting it would be a quieter version of the same thing.
        out.append(f'  <subject id="{ident}">')
        out.append(body.rstrip("\n"))
        out.append("  </subject>")
        out.append(f"  <constraints>{constraints}</constraints>")
        out.append(f'  <evidence require="{PHASE_EVIDENCE[phase]}"/>')
        for origin, text in quoted:
            # §7.5 · law L6 — outside content is DATA. It sits outside `<context>`, quoted and
            # labelled, so it can never be read as instruction.
            out.append(f'  <evidence origin="{origin}" trust="data">')
            out += ["  > " + l for l in text.splitlines()]
            out.append("  </evidence>")
        if for_subagent:
            out.append(f"  <close>add run {slug} -- &lt;cmd&gt; · then add gate {slug}</close>")
        out.append("</task>")
        return "\n".join(out) + "\n"

    def finish(payload: str, degraded: list, over: bool) -> tuple:
        # The hash covers the payload only: the cost line quotes the hash, and a hash of a
        # string containing itself does not exist.
        digest = "sha256:" + hashlib.sha256(payload.encode()).hexdigest()[:16]
        tail = (f"cost: ###### B / {budget} B budget · ~##### tok / "
                f"~{budget // BYTES_PER_TOKEN} tok (declared {BYTES_PER_TOKEN} B/tok) · "
                f"{nodes} nodes · {digest}"
                + ("\n  DEGRADED (A5): " + " → ".join(degraded) if degraded else "")
                + ("\n  OVER BUDGET — reported, not truncated (R:SILENTCUT)" if over else "")
                + f"\nnext: add run {slug} -- <cmd>   # then add gate {slug}\n")
        # Fixed-width placeholders: the printed size includes the line printing it, so the
        # substitution must not change the length. One pass, no fixed-point iteration.
        size = len(payload.encode()) + len(tail.encode())
        tail = tail.replace("######", f"{size:>6}", 1).replace("#####", f"{size // BYTES_PER_TOKEN:>5}", 1)
        return payload + tail, size, digest

    ladder = [((False, False), None),
              ((True, False), "specs → refs"),
              ((True, True), "dep cards → refs")]
    degraded, text, size, digest = [], "", 0, ""
    for flags, label in ladder:
        if label:
            degraded.append(label)
        payload = assemble(*flags)
        text, size, digest = finish(payload, degraded, False)
        if size <= budget:
            break
    else:
        text, size, digest = finish(payload, degraded, True)

    return {"text": text, "bytes": size, "hash": digest, "nodes": nodes,
            "budget": budget, "degraded": degraded, "phase": phase, "depth": depth}


# ============================================ gate — the verdict, and its refusals (e13)
#
# This verb should have existed since e4. Every gate in this project's history was recorded by
# hand-appending a stamp through the private `_transition`, so none of the three refusals
# PROPOSAL specifies for `gate` had ever run against anything.
#
# It is also where e12's M3 lands. That rule reads "`unbound` is part of every gate's report" —
# and it was gated PASS while no gate report existed. The rule was never wrong; it had nowhere
# to be true.
#
# Refusing is not guarding (law 3). A refusal never stops a human from writing the stamp
# themselves with their own authority; it stops the ENGINE from manufacturing a record that its
# own evidence does not support. The measured case for the strict form: run against this
# project's own history, M2 would have refused 8 gates — exactly the 8 tasks F2 found
# labelled-but-not-proven, and zero of the 7 well-bound M1 tasks. It fires on the defect and
# nothing else, so `RISK-ACCEPTED` with a recorded reason is the only degradation needed.

VERDICTS = ("PASS", "RISK-ACCEPTED", "HARD-STOP")


def orphans(root) -> list:
    """Receipt nodes that no `verified[]` stamp points at — unreachable evidence (R:ORPHAN)."""
    root = Path(root)
    cited = set()
    for node in scan(root).values():
        for stamp in ((node["fm"] or {}).get("verified") or []):
            if isinstance(stamp, dict) and stamp.get("receipt"):
                cited.add(str(stamp["receipt"]).lstrip("/"))
    return ["/" + str(p.relative_to(root)) for p in sorted(root.rglob("runs/*.md"))
            if str(p.relative_to(root)) not in cited]


def latest_receipt(root, cid: str) -> tuple:
    """`(receipt_dict, cid)` for the newest receipt of a task, or `(None, None)`."""
    root = Path(root)
    slug = cid.rsplit("/", 1)[-1][:-3]
    runs = sorted((root / f"tasks/{slug}.d/runs").glob("*.md"),
                  key=lambda p: int(p.stem) if p.stem.isdigit() else 0)
    if not runs:
        return None, None
    fm = read(runs[-1], "T0")["fm"] or {}
    return fm.get("receipt"), "/" + str(runs[-1].relative_to(root))


def gate(root, cid: str, verdict: str, by: str, authority: str = None,
         reason: str = None) -> tuple:
    """Record a verdict, or refuse and say what would make it pass. `(ok, note)`."""
    root = Path(root)
    slug = cid.rsplit("/", 1)[-1][:-3]

    def refuse(why: str, fix: str) -> tuple:
        return False, f"cannot record `{verdict}` — {why}\nnext: {fix}"

    if verdict not in VERDICTS:
        return refuse(f"unknown verdict {verdict!r}",
                      f"add gate {slug} <{' | '.join(VERDICTS)}>")
    graph = scan(root)
    if cid not in graph:
        return refuse(f"no such node: {cid}", "add status")
    if verdict != "PASS" and not reason:
        return refuse(f"a {verdict} with no reason is a PASS in disguise",
                      f'add gate {slug} {verdict} --reason "<why>"')

    node_body = lambda n: read(n["path"], "T2")["body"]
    receipt, receipt_cid = latest_receipt(root, cid)
    if receipt is None:
        return refuse("no receipt has been recorded", f"add run {slug} -- <cmd>")

    # Refusal 1 (M1) — a verdict over changed code is evidence of nothing.
    #
    # A node declaring no `scope:` has nothing to be stale ABOUT, and §3d's quick and doc lanes
    # both allow one. That is not-applicable, not failed — but it must be SAID, and it must not
    # become a way to dodge freshness: scope declared with no digest recorded stays a refusal.
    declared_scope = (graph[cid]["fm"] or {}).get("scope") or []
    if not declared_scope:
        # A CARD claiming a scope the frontmatter lacks is worse than an honestly unscoped node:
        # the CARD is what a human reads, while `scope_digest` and A17's path floor both match
        # against frontmatter. This gated e13 itself with freshness silently skipped.
        card_scope = [l for l in card_of(node_body(graph[cid])).splitlines()
                      if l.startswith("scope:") and l.partition(":")[2].strip()]
        if card_scope and verdict == "PASS":
            return refuse(f"the CARD claims a scope the frontmatter does not declare "
                          f"({card_scope[0].strip()}) — freshness and A17's path floor both read "
                          f"frontmatter, so both were silently skipped",
                          f"add scope: to {slug}'s frontmatter, then add run {slug} -- <cmd>")
        freshness = "freshness: n/a — the node declares no `scope:`"
    else:
        ok, why = fresh(receipt, root.parent)
        if not ok and verdict == "PASS":
            return refuse(f"the receipt is stale — {why}", f"add run {slug} -- <cmd>")
        freshness = f"freshness: {'fresh' if ok else 'STALE'} — {why}"

    node = read(graph[cid]["path"], "T2")
    stubs = placeholders_in(node)
    if stubs and verdict == "PASS":
        return refuse("the node still carries template placeholders: " + " · ".join(stubs),
                      f"author {slug}'s RULES and CHECKS, then add gate {slug} PASS")

    # Refusal 2 (M2) — a Must proven by nothing is a label (A15). e12's M3, landing.
    reported = {i: "pass" for i in (receipt.get("passed") or [])}
    reported.update({i: "fail" for i in (receipt.get("failed") or [])})
    gaps = unbound(node, reported)
    if gaps and verdict == "PASS":
        return refuse("these rules have no reported passing check: " + ", ".join(gaps),
                      f'add gate {slug} RISK-ACCEPTED --reason "<why the gap is acceptable>"')

    authority = authority_for(graph, cid)          # computed, never the caller's claim (M3)
    digest = brief(root, cid)["hash"]              # A16 — the instructions that drove the work
    stamp = (f'{{ by: "{by}", at: {_today()}, act: gate, authority: {authority}, '
             f'outcome: {verdict}, receipt: {receipt_cid}, brief: "{digest}"'
             + (f', reason: "{reason}"' if reason else "") + " }")
    _transition(root, cid, appends=[("verified", stamp)])

    if verdict == "PASS":
        done(root, cid)
        render_card(root, cid)
        tail = f"{cid} is done"
    else:
        tail = f"{verdict} recorded; {slug} stays in `{(graph[cid]['fm'] or {}).get('status')}`"
    note = (f"gate {verdict} recorded at authority `{authority}`"
            + f"\n  {freshness}"
            + (f"\n  unbound (reported, not blocking): {', '.join(gaps)}" if gaps else "")
            + f"\n  brief {digest} · receipt {receipt_cid}\n{tail}\nnext: add status")
    return True, note


def quick(root, slug: str, title: str, cmd: list, by: str, cwd=None,
          depth: str = "quick", **fields) -> tuple:
    """§3d's quick lane: new + freeze + run + gate in ONE engine call.

    Refused above `quick` depth. A one-call lane that works at `deep` is not a lane, it is a
    bypass of every control this engine has.
    """
    if depth != "quick":
        return False, (f"the one-call lane is `quick` depth only; this is `{depth}`"
                       f"\nnext: add new task {slug} --depth {depth}")
    root = Path(root)
    cid, _ = new(root, "Task", slug, title=title, depth="quick", **fields)
    # A quick task's evidence is its exit code, not a covers-bound suite (§3d: "rename a flag;
    # add a log line"). The standard template's placeholder Musts would make the one-call lane
    # unclosable by construction, so the quick body declares none.
    path = root / cid.lstrip("/")
    stub = read(path, "T2")
    write(path, f"---\n{stub['raw']}\n---\n## CARD\ngoal: {title}\n"
                f"beat: build · next: add run {slug} -- <cmd>\n\n"
                f"## EVIDENCE\nreceipt: <runs/<n>.md>\ngate: <PASS>\n")
    freeze(root, cid, by=by)
    node = run(root, cid, cmd, cwd=cwd or root.parent)
    if node["receipt"]["exit"] != 0:
        return False, (f"the command exited {node['receipt']['exit']} — a red command earns no gate"
                       f"\nnext: fix, then add run {slug} -- <cmd>")
    ok, note = gate(root, cid, "PASS", by=by)
    return ok, f"quick lane: {slug} opened, run and gated in one call\n{note}"


# ================================= checks — the CHECKS section, compiled (e14)
#
# F2 measured this project's own version of the defect: 61 cited test names that were never
# written, across nine gated M0 tasks. Nobody noticed because a plausible test name reads
# exactly like a real one at review speed.
#
# More care at authoring time does not fix it. e13 opened with 12 authored checks and its suite
# finished at 25 — every addition was discovered DURING the build, so the knowledge did not exist
# when the section was written. Extraction is the only fix (L7: compiled beats authored).
#
# Two carriers, because this repo already contains two: a docstring `covers:` (118 tests) and a
# `# --- name · covers: … ---` header above the function (e15's subagent, 5 tests). One author was
# enough for the convention to diverge, so the reader accepts both.

COVERS_IN_TEST = re.compile(r"covers:\s*([^—\n·]+)(?:[—·]\s*(.*))?", re.DOTALL)
HEADER_COVERS = re.compile(r"^#.*?\b(test_\w+)\s*·\s*covers:\s*([^-\n]+?)\s*-*$", re.MULTILINE)


def checks_of(paths) -> dict:
    """`{test_id: (rule_ids, description)}` for every test in `paths`.

    Which names are functions is the PARSER's answer, not a regex's. A regex over source text
    reads `def test_…` out of quoted strings: this verb compiled its own task's node and listed
    three tests that exist only inside fixture string constants. Same defect class as the
    unanchored validator regex e15 fixed, found the same way — by reading the output.

    An unlabelled test maps to `([], doc)` and is REPORTED as unlabelled, never given a rule
    inferred from its name (R:GUESS): `test_m1_something` proves whatever its body proves, which
    may be nothing to do with M1.
    """
    found = {}
    for path in paths:
        try:
            tree = ast.parse(src := Path(path).read_text(encoding="utf-8"))
        except (OSError, SyntaxError):
            continue
        real = {n.name: (ast.get_docstring(n) or "") for n in ast.walk(tree)
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                and n.name.startswith("test_")}
        # A header citation is honoured only for a name the parser confirms, so a comment inside a
        # string literal cannot smuggle one in either.
        from_header = {m.group(1): m.group(2) for m in HEADER_COVERS.finditer(src)
                       if m.group(1) in real}
        for name, doc in real.items():
            raw, desc = None, ""
            match = COVERS_IN_TEST.search(doc)
            if match:
                raw, desc = match.group(1), match.group(2) or ""
            elif name in from_header:
                raw, desc = from_header[name], doc
            # Every referent is validated against FORMAT §6.1's grammar. A docstring reading
            # "No covers: anywhere" otherwise yields rules named `anywhere. A gap` — found by a
            # fixture that said exactly that, by accident. Prose mentioning the word is not a
            # citation, and the grammar is what tells the two apart.
            rules = [r.strip() for r in (raw or "").split(",") if REFERENT.match(r.strip())]
            found[name] = (rules, _summarise(desc))
    return found


def _summarise(text: str, width: int = 110) -> str:
    """One line, cut at a word and marked as cut. A CHECKS description is a summary of a test,
    never the test — but a cut that does not say so reads as a typo, not as an omission."""
    flat = " ".join(text.split()).strip(' ."')
    if len(flat) <= width:
        return flat
    head = flat[:width].rsplit(" ", 1)[0]
    return f"{head.rstrip(' ,;.')}…"


def unlabelled(paths) -> list:
    """Tests carrying no `covers:` — a visible gap (M3)."""
    return sorted(name for name, (rules, _) in checks_of(paths).items() if not rules)


def _checks_lines(node: dict, paths) -> tuple:
    """`(lines, gaps)` — the compiled CHECKS body for one node, and its unlabelled tests.

    The citation is compiled because a human cannot be trusted to keep it in step with the suite.
    The DESCRIPTION is the opposite: knowledge only the author has. Restating the citation as
    `· proves M1` compiles a line that says nothing twice, so the author's sentence is carried
    through and only its absence is filled in.
    """
    rules, extracted = rules_of(node), checks_of(paths)
    relevant = {t: v for t, v in extracted.items() if any(r in rules for r in v[0])}
    lines = [f"- {t} · covers: {', '.join(rs)} · {desc or 'no description in the test'}"
             for t, (rs, desc) in sorted(relevant.items())]
    return lines, sorted(t for t, (rs, _) in extracted.items() if not rs)


def checks_verify(root, cid: str, paths) -> list:
    """F2 in BOTH directions, graded. `[{severity, message, rule, test}]` (M2).

    Two findings that look identical mean different things, and grading them the same makes the
    report useless:

    * a cited test that does not exist on a node **still in `direction`** is `pending` — the task
      has not been built, and its CHECKS are a plan. Thirteen live nodes reported at first run and
      four were exactly this;
    * the same gap on a node carrying a **gate stamp** is an `error`: a claim was accepted against
      evidence that was not there. That is F2.

    A referent naming no declared rule is always an `error`. Unlike a missing test it cannot come
    true later — it is a claim about the node's own contents, and the node is right there.
    """
    node = scan(Path(root)).get(cid)
    if node is None:
        return []
    full = read(node["path"], "T2")
    stamps = [s for s in ((node["fm"] or {}).get("verified") or []) if isinstance(s, dict)]
    gated = any(s.get("act") == "gate" for s in stamps)
    known, rules = set(checks_of(paths)), set(rules_of(full))
    findings = []
    for rule, cited in sorted(covers(full).items()):
        if rule not in rules:
            findings.append({"severity": "error", "rule": rule, "test": None,
                             "message": f"{cid}: `covers: {rule}` names no rule this node declares"})
        for test in cited:
            if test not in known:
                findings.append({
                    "severity": "error" if gated else "pending", "rule": rule, "test": test,
                    "message": f"{cid}: `{test}` exists in no suite"
                               + ("" if gated else " (node is not gated — its checks are a plan)")})
    return findings


def checks_sync(root, cid: str, paths) -> tuple:
    """Rewrite one node's CHECKS from the suite. `(changed, note)`.

    Refuses a node carrying a gate stamp (R:SILENTFIX). That is the §3.6 asymmetry F2 turned on:
    e12's own CHECKS were corrected freely because nothing had been stamped, and M0's nine cannot
    be, because a gate was taken against them. Refusing to repair is not refusing to REPORT —
    `checks_verify` still speaks.
    """
    # Materialised once: this function walks `paths` to compile and again to report how many files
    # it read, and a generator makes the second walk empty. The section came out correct and the
    # note said "from 0 suite files" — a true report is not optional in a notary.
    root, paths = Path(root), list(paths)
    node = scan(root).get(cid)
    if node is None:
        return False, f"no such node: {cid}\nnext: add status"
    if any(s.get("act") == "gate" for s in ((node["fm"] or {}).get("verified") or [])
           if isinstance(s, dict)):
        return False, (f"{cid} carries a gate stamp — a gated claim is recorded, not repaired "
                       f"(§3.6, R:SILENTFIX)\nnext: add checks {cid.rsplit('/', 1)[-1][:-3]} --verify")

    full = read(node["path"], "T2")
    lines, gaps = _checks_lines(full, paths)
    body = full["body"]
    start = body.find("## CHECKS")
    if start < 0:
        return False, f"{cid} has no `## CHECKS` section to compile into\nnext: add status"
    rest = body[start:]
    end = start + (rest.find("\n## ", 1) if "\n## " in rest[1:] else len(rest))
    section = ("## CHECKS\n" + "\n".join(lines) +
               "\nred-first: every check above MUST fail for the right reason before BUILD.\n" +
               (f"unlabelled: {', '.join(gaps)} — carry no `covers:`; reported, never inferred (M3)\n"
                if gaps else "") +
               "<!-- COMPILED from the suite (e14). Do not author here: a citation edited by hand\n"
               "     cannot be distinguished from one that was never true (F2). -->\n")
    new_body = body[:start] + section + body[end:]
    if new_body == body:
        return False, f"{cid}'s CHECKS already match the suite\nnext: add status"
    write(node["path"], f"---\n{full['raw']}\n---\n{new_body}")
    return True, (f"{cid}: {len(lines)} checks compiled from {len(list(paths))} suite files"
                  + (f" · {len(gaps)} unlabelled" if gaps else "") + "\nnext: add status")
