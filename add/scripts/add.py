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

import json
import os
import re
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
            while text.count("{") > text.count("}") and i < len(toks):  # a wrapped flow map
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
