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

import os
import re
from pathlib import Path

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
