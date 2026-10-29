#!/usr/bin/env python3
"""Convert Humadroid-exported policy/procedure PDFs to clean Markdown.

Usage:
    python3 -I scripts/di-migration/pdf_to_md.py data/Compliance/evidence/policies-procedures data/markdown

For each PDF: extract Markdown with pymupdf4llm, strip the Humadroid
"Document Information" cover block (kept as YAML front matter), drop page
headers/footers, fix known placeholders, and replace "Humadroid" references
with the replacement system (Comp). Emits <slug>.md with front matter:
title, doc_type, version, acknowledgment, effective_date, review_date, source.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pymupdf4llm

REPLACEMENTS = [
    # Humadroid is being replaced by the self-hosted Comp instance.
    (re.compile(r"the organization's risk assessment module in Humadroid", re.I), "the risk register in the compliance platform"),
    (re.compile(r"in Humadroid's (Incident Reporting system|risk assessment module)", re.I), r"in the compliance platform's \1"),
    (re.compile(r"Humadroid's", re.I), "the compliance platform's"),
    (re.compile(r"\bHumadroid\b", re.I), "the compliance platform"),
    # Template placeholders left in the body.
    (re.compile(r"\\?\[Current Date\]"), "{{EFFECTIVE_DATE}}"),
    (re.compile(r"\\?\[Current Date \+ 1 Year\]"), "{{REVIEW_DATE}}"),
    (re.compile(r"\\?\[Annual Review( Date)?\]"), "{{REVIEW_DATE}}"),
    (re.compile(r"\\?\[Authorized Signatory\]"), "Mo Messidi, CEO"),
    (re.compile(r"privacy@dealintelligence\.com"), "privacy@dealintelligence.io"),
]

COVER_FIELDS = [
    "Document Type", "Version", "Status", "Acknowledgment Type", "Author",
    "Finalized At", "Effective Date", "Review Date",
]


def parse_cover(md: str) -> tuple[dict, str]:
    """Humadroid cover is a 2-column table of label/value rows; body starts at
    the first '## **Title**' heading after it."""
    meta: dict[str, str] = {}
    cover_end = md.find("\n## ")
    cover = md[:cover_end] if cover_end > 0 else ""
    rows = [r for r in cover.splitlines() if r.startswith("|") and not r.startswith("|---")]
    cells = [[c.strip().strip("*").strip() for c in r.strip("|").split("|")] for r in rows]
    for labels, values in zip(cells[0::2], cells[1::2]):
        for label, value in zip(labels, values):
            if label in COVER_FIELDS:
                meta[label] = value
    body = md[cover_end + 1:] if cover_end > 0 else md
    return meta, body


def normalize_heading(line: str) -> str:
    m = re.match(r"^(#+)\s+(.*?)\s*$", line)
    if not m:
        return line
    level, text = len(m.group(1)), m.group(2).strip().strip("*").strip()
    # pymupdf4llm sizes: ### = section, #### = subsection. Shift up one level.
    level = max(2, min(level - 1, 4))
    return f"{'#' * level} {text}"


def clean_body(body: str, title: str) -> str:
    lines = []
    for line in body.splitlines():
        s = line.strip()
        # page footer/header noise
        if re.fullmatch(r"(Page )?\d+( of \d+)?", s):
            continue
        if s.startswith("-----"):
            continue
        if s.startswith("#"):
            line = normalize_heading(s)
        lines.append(line.rstrip())
    out = "\n".join(lines).strip()
    # Humadroid renders the title twice (## then #); collapse to one H1.
    out = re.sub(rf"^(#+ {re.escape(title)}\s*\n+)+", f"# {title}\n\n", out)
    for pattern, repl in REPLACEMENTS:
        out = pattern.sub(repl, out)
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out.strip() + "\n"


def slugify(name: str) -> str:
    return re.sub(r"-v\d+\.\d+$", "", name.lower())


def convert(pdf: Path, out_dir: Path) -> dict:
    md = pymupdf4llm.to_markdown(str(pdf), show_progress=False)
    meta, body = parse_cover(md)
    title_match = re.search(r"\n#+ \**(.+?)\**\s*\n", "\n" + body)
    title = title_match.group(1).strip() if title_match else pdf.stem
    body = clean_body(body, title)
    front = {
        "title": title,
        "doc_type": meta.get("Document Type", "Policy"),
        "version": meta.get("Version", "1.0"),
        "acknowledgment": meta.get("Acknowledgment Type", "None"),
        "effective_date": meta.get("Effective Date", "N/A"),
        "review_date": meta.get("Review Date", "N/A"),
        "finalized_at": meta.get("Finalized At", ""),
        "author": meta.get("Author", ""),
        "source": pdf.name,
    }
    slug = slugify(pdf.stem)
    fm = "---\n" + "\n".join(f"{k}: {json.dumps(v)}" for k, v in front.items()) + "\n---\n\n"
    (out_dir / f"{slug}.md").write_text(fm + body, encoding="utf-8")
    return {"slug": slug, **front, "chars": len(body)}


def main() -> None:
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    dst.mkdir(parents=True, exist_ok=True)
    results = [convert(p, dst) for p in sorted(src.glob("*.pdf"))]
    (dst / "_index.json").write_text(json.dumps(results, indent=2))
    for r in results:
        print(f"{r['slug']:60s} {r['doc_type']:10s} ack={r['acknowledgment']:8s} {r['chars']:>6d} chars")


if __name__ == "__main__":
    main()
