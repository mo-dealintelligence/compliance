#!/usr/bin/env python3
"""Convert Humadroid-exported policy/procedure/record PDFs to clean Markdown.

Usage:
    python3 -I scripts/di-migration/pdf_to_md.py <pdf dir> <out dir>

Per PDF: extract Markdown with pymupdf4llm, read the Humadroid cover block
into front matter, drop page noise, revision-history tables and inline
"Document ID / Version / Next Review" control lines (Comp tracks versions and
review dates itself), merge table rows that wrapped across lines, fix
template placeholders, and replace "Humadroid" references since Comp is now
the system of record.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pymupdf4llm

COVER_FIELDS = {
    "Document Type": "doc_type",
    "Record Version": "version",
    "Version": "version",
    "Status": "status",
    "Acknowledgment Type": "acknowledgment",
    "Author": "author",
    "Finalized At": "finalized_at",
    "Effective Date": "effective_date",
    "Review Date": "review_date",
}
INLINE_PAIRS = [  # Humadroid inline cover: "**Document Type Version** Policy 1.0 ..."
    ("Document Type", "Version"),
    ("Status", "Acknowledgment Type"),
    ("Author", "Finalized At"),
    ("Effective Date", "Review Date"),
]
DATE = r"(?:N/A|[A-Z][a-z]+ \d{1,2}, \d{4}(?: at \d{1,2}:\d{2} [AP]M)?)"

REPLACEMENTS = [
    (re.compile(r"the organization's risk assessment module in Humadroid", re.I), "the risk register in the compliance platform"),
    (re.compile(r"in Humadroid's (Incident Reporting system|risk assessment module)", re.I), r"in the compliance platform's \1"),
    (re.compile(r"Humadroid's", re.I), "the compliance platform's"),
    (re.compile(r"\bHumadroid\b", re.I), "the compliance platform"),
    (re.compile(r"\\?\[Current\s*(?:<br>)?\s*Date\]"), "{{EFFECTIVE_DATE}}"),
    (re.compile(r"\\?\[Original\s*(?:<br>)?\s*Date\]"), "{{ORIGINAL_DATE}}"),
    (re.compile(r"\\?\[Current Date \+ 1 Year\]"), "{{REVIEW_DATE}}"),
    (re.compile(r"\\?\[Annual Review( Date)?\]"), "{{REVIEW_DATE}}"),
    (re.compile(r"\\?\[Authorized Signatory\]"), "Mo Messidi, CEO"),
    (re.compile(r"privacy@dealintelligence\.com"), "privacy@dealintelligence.io"),
    (re.compile(r"<br>"), " "),
]
DROP_SECTIONS = re.compile(r"^(document control|revision history|document history|version history|document information)$", re.I)
CONTROL_LINE = re.compile(r"^\*\*Document ID:\*\*.*", re.M)


def strip_bold(s: str) -> str:
    return s.replace("**", "").strip()


def parse_cover(cover: str) -> dict:
    meta: dict[str, str] = {}
    # Table form: cells alternate label/value, or a label row then a value row.
    rows = [r for r in cover.splitlines() if r.startswith("|") and not r.startswith("|---")]
    if rows:
        pending: list[str] = []
        for row in rows:
            for cell in [c.strip() for c in row.strip("|").split("|")]:
                label = strip_bold(cell)
                if cell.startswith("**") and label in COVER_FIELDS:
                    pending.append(COVER_FIELDS[label])
                elif pending:
                    meta[pending.pop(0)] = label
        return meta
    # Inline form.
    text = " ".join(cover.split())
    for a, b in INLINE_PAIRS:
        m = re.search(rf"\*\*{a} {b}\*\*\s*(.*?)(?=\s*\*\*|$)", text)
        if not m:
            continue
        values = m.group(1).strip()
        if a == "Effective Date":
            d = re.findall(DATE, values)
            if len(d) >= 2:
                meta["effective_date"], meta["review_date"] = d[0], d[1]
        elif a == "Author":
            mm = re.match(rf"(.+?)\s+({DATE})$", values)
            if mm:
                meta["author"], meta["finalized_at"] = mm.group(1), mm.group(2)
        else:
            parts = values.split(" ", 1)
            if len(parts) == 2:
                meta[COVER_FIELDS[a]], meta[COVER_FIELDS[b]] = parts[0], parts[1]
    return meta


def merge_wrapped_rows(lines: list[str]) -> list[str]:
    out: list[str] = []
    for line in lines:
        if line.startswith("|") and out and out[-1].startswith("|") and not line.startswith("|---"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            prev = [c.strip() for c in out[-1].strip("|").split("|")]
            if len(cells) == len(prev) and cells[0] in {".", ""} and not out[-1].startswith("|---"):
                merged = [f"{p} {c}".strip() for p, c in zip(prev, cells)]
                out[-1] = "|" + "|".join(merged) + "|"
                continue
        out.append(line)
    return out


def drop_sections(lines: list[str]) -> list[str]:
    out: list[str] = []
    skipping_level = 0
    for line in lines:
        m = re.match(r"^(#+)\s+(.*)$", line)
        if m:
            level, text = len(m.group(1)), m.group(2).strip()
            if skipping_level and level <= skipping_level:
                skipping_level = 0
            if DROP_SECTIONS.match(text):
                skipping_level = level
                continue
        if skipping_level:
            continue
        out.append(line)
    return out


def normalize_heading(line: str) -> str:
    m = re.match(r"^(#+)\s+(.*?)\s*$", line)
    if not m:
        return line
    level, text = len(m.group(1)), strip_bold(m.group(2))
    return f"{'#' * max(2, min(level - 1, 4))} {text}"


def clean_body(body: str, title: str) -> str:
    lines = []
    for raw in body.splitlines():
        s = raw.strip()
        if re.fullmatch(r"(Page )?\d+( of \d+)?", s) or s.startswith("-----"):
            continue
        if s.startswith("<mark>") and "Docusign" in s:
            continue
        lines.append(normalize_heading(s) if s.startswith("#") else raw.rstrip())
    lines = drop_sections(merge_wrapped_rows(lines))
    out = "\n".join(lines).strip()
    out = re.sub(rf"^(#+ \**{re.escape(title)}\**\s*\n+)+", f"# {title}\n\n", out)
    out = CONTROL_LINE.sub("", out)
    for pattern, repl in REPLACEMENTS:
        out = pattern.sub(repl, out)
    return re.sub(r"\n{3,}", "\n\n", out).strip() + "\n"


def convert(pdf: Path, out_dir: Path) -> dict:
    md = pymupdf4llm.to_markdown(str(pdf), show_progress=False)
    cut = md.find("\n## ")
    if cut < 0:
        cut = md.find("\n# ")
    cover, body = (md[:cut], md[cut + 1:]) if cut > 0 else ("", md)
    meta = parse_cover(cover)
    tm = re.search(r"^#+ \**(.+?)\**\s*$", body, re.M)
    title = tm.group(1).strip() if tm else pdf.stem
    front = {
        "title": title,
        "doc_type": meta.get("doc_type", "Policy"),
        "version": meta.get("version", "1.0"),
        "acknowledgment": meta.get("acknowledgment", "None"),
        "effective_date": meta.get("effective_date", "N/A"),
        "review_date": meta.get("review_date", "N/A"),
        "finalized_at": meta.get("finalized_at", ""),
        "author": meta.get("author", ""),
        "source": pdf.name,
    }
    slug = re.sub(r"-v\d+\.\d+$", "", pdf.stem.lower())
    fm = "---\n" + "\n".join(f"{k}: {json.dumps(v)}" for k, v in front.items()) + "\n---\n\n"
    text = clean_body(body, title)
    (out_dir / f"{slug}.md").write_text(fm + text, encoding="utf-8")
    return {"slug": slug, **front, "chars": len(text)}


def main() -> None:
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    dst.mkdir(parents=True, exist_ok=True)
    results = [convert(p, dst) for p in sorted(src.glob("*.pdf"))]
    (dst / "_index.json").write_text(json.dumps(results, indent=2))
    for r in results:
        print(f"{r['slug'][:58]:58s} {r['doc_type'][:22]:22s} ack={r['acknowledgment']:8s} eff={r['effective_date']:18s} {r['chars']:>6d}")


if __name__ == "__main__":
    main()
