#!/usr/bin/env python3
"""One-off codemod used for the Deal Intelligence rebrand (branch di/self-host).

Rewrites user-visible "Comp AI" / "CompAI" copy in TS/TSX source to the
brand-driven value `brand.name` from '@trycompai/utils/brand', and swaps
hard-coded `https://app.trycomp.ai` / `https://portal.trycomp.ai` fallbacks
for `brand.appUrl` / `brand.portalUrl`.

Rules:
- Comments are left untouched.
- Single/double-quoted string literals that contain the brand text are
  converted to template literals; JSX attribute values are wrapped in {}.
- Template literals get `${brand.name}` inline.
- Bare JSX text gets `{brand.name}`.
- The import is appended after the last top-level import (or after the
  'use client' / 'use server' directive when the file has no imports).

Usage: python3 scripts/rebrand-codemod.py <file> [<file> ...]
"""
from __future__ import annotations

import re
import sys

BRAND_IMPORT = "import { brand } from '@trycompai/utils/brand';"
BRAND_RE = re.compile(r"Comp AI|CompAI")

TOKEN_RE = re.compile(
    r"""
    (?P<line_comment>//[^\n]*)
  | (?P<block_comment>/\*.*?\*/)
  | (?P<template>`(?:[^`\\]|\\.)*`)
  | (?P<single>'(?:[^'\\\n]|\\.)*')
  | (?P<double>"(?:[^"\\\n]|\\.)*")
    """,
    re.DOTALL | re.VERBOSE,
)

URL_FALLBACKS = [
    (
        re.compile(
            r"process\.env\.(?:NEXT_PUBLIC_APP_URL|NEXT_PUBLIC_BETTER_AUTH_URL)\s*(?:\?\?|\|\|)\s*'https://app\.trycomp\.ai'"
        ),
        "brand.appUrl",
    ),
    (
        re.compile(
            r"process\.env\.NEXT_PUBLIC_PORTAL_URL\s*(?:\?\?|\|\|)\s*'https://portal\.trycomp\.ai'"
        ),
        "brand.portalUrl",
    ),
    (re.compile(r"'https://app\.trycomp\.ai'"), "brand.appUrl"),
    (re.compile(r"'https://portal\.trycomp\.ai'"), "brand.portalUrl"),
]


def to_template(inner: str) -> str:
    inner = inner.replace("`", "\\`").replace("${", "\\${")
    return "`" + BRAND_RE.sub("${brand.name}", inner) + "`"


def is_jsx_attr(src: str, start: int) -> bool:
    """True when the literal at `start` is the value of a JSX attribute."""
    i = start - 1
    if i < 0 or src[i] != "=":
        return False
    j = i - 1
    return j >= 0 and (src[j].isalnum() or src[j] in "_-$")


def rewrite(src: str) -> tuple[str, bool]:
    out: list[str] = []
    pos = 0
    changed = False
    for m in TOKEN_RE.finditer(src):
        gap = src[pos : m.start()]
        if BRAND_RE.search(gap):
            gap = BRAND_RE.sub("{brand.name}", gap)
            changed = True
        out.append(gap)
        tok = m.group(0)
        kind = m.lastgroup
        if kind in ("line_comment", "block_comment"):
            out.append(tok)
        elif kind == "template":
            if BRAND_RE.search(tok):
                tok = BRAND_RE.sub("${brand.name}", tok)
                changed = True
            out.append(tok)
        else:
            if BRAND_RE.search(tok):
                tmpl = to_template(tok[1:-1])
                if is_jsx_attr(src, m.start()):
                    tmpl = "{" + tmpl + "}"
                out.append(tmpl)
                changed = True
            else:
                out.append(tok)
        pos = m.end()
    tail = src[pos:]
    if BRAND_RE.search(tail):
        tail = BRAND_RE.sub("{brand.name}", tail)
        changed = True
    out.append(tail)
    result = "".join(out)

    for pattern, replacement in URL_FALLBACKS:
        result, n = pattern.subn(replacement, result)
        if n:
            changed = True
    return result, changed


IMPORT_LINE_RE = re.compile(r"^import\b[^;]*;[ \t]*$", re.MULTILINE)
DIRECTIVE_RE = re.compile(r"^(['\"])use (client|server)\1;?[ \t]*$", re.MULTILINE)


def add_import(src: str) -> str:
    if "@trycompai/utils/brand" in src:
        return src
    imports = list(IMPORT_LINE_RE.finditer(src))
    if imports:
        last = imports[-1]
        return src[: last.end()] + "\n" + BRAND_IMPORT + src[last.end() :]
    directive = DIRECTIVE_RE.search(src)
    if directive:
        return src[: directive.end()] + "\n\n" + BRAND_IMPORT + src[directive.end() :]
    return BRAND_IMPORT + "\n\n" + src


def main(paths: list[str]) -> None:
    for path in paths:
        with open(path, encoding="utf-8") as fh:
            src = fh.read()
        result, changed = rewrite(src)
        if not changed:
            print(f"unchanged: {path}")
            continue
        if "brand." in result:
            result = add_import(result)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(result)
        print(f"rewrote:   {path}")


if __name__ == "__main__":
    main(sys.argv[1:])
