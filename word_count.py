#!/usr/bin/env python3
"""
Word counter for CITS4404 Deliverable 1 (.docx).

Applies the official rule: max 3000 words, excluding figures and references.

Usage:
    python word_count.py <path-to-docx>
    python word_count.py <path-to-docx> --verbose   # show per-section breakdown

Counting rules (derived from CITS4404Projects.pdf):
  INCLUDED (body):
    - All paragraph text inside Synopsis 1 / Synopsis 2 / Conclusions
    - Section headings within those regions (e.g. "1. Problem Being Solved")
  EXCLUDED:
    - Document-level metadata: title, team number, word count line,
      student info table
    - Code blocks / equation blocks (rendered as tables in docx)
    - Data tables that function as figures (Results table, Mechanism Comparison)
    - The "References" section and its numbered entries
    - Team Statement section and its table
    - "Click the image to view the sheet" placeholder text
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    from docx import Document
    from docx.document import Document as _Doc
    from docx.oxml.ns import qn
    from docx.table import Table
    from docx.text.paragraph import Paragraph
except ImportError:
    sys.stderr.write(
        "ERROR: python-docx not installed. Run:\n"
        "    pip install python-docx --break-system-packages\n"
    )
    sys.exit(2)


WORD_RE = re.compile(r"\b[\w'\-]+\b", re.UNICODE)

# Sentinels that mark transitions between counted / excluded regions.
SYNOPSIS_1_MARKER = re.compile(r"^Synopsis\s*1[:\s]", re.IGNORECASE)
SYNOPSIS_2_MARKER = re.compile(r"^Synopsis\s*2[:\s]", re.IGNORECASE)
CONCLUSIONS_MARKER = re.compile(r"^Conclusions\s*[:\s]", re.IGNORECASE)
REFERENCES_MARKER = re.compile(r"^References\s*$", re.IGNORECASE)
TEAM_STATEMENT_MARKER = re.compile(r"^Team\s+Statement\s*$", re.IGNORECASE)

# Paragraphs to always skip regardless of section.
SKIP_PATTERNS = [
    re.compile(r"Click the image to view the sheet", re.IGNORECASE),
    re.compile(r"End of Deliverable", re.IGNORECASE),
    re.compile(r"^Code block$", re.IGNORECASE),      # Feishu artefact
    re.compile(r"^Plain Text$", re.IGNORECASE),      # Feishu artefact
    re.compile(r"^\[.*?(待填写|待补充|TO BE FILLED|Add more).*?\]\s*$", re.IGNORECASE),
]


@dataclass
class SectionCounts:
    """Word counts within a specific region."""
    name: str
    paragraph_words: int = 0
    heading_words: int = 0
    table_words: int = 0
    paragraphs: list[tuple[str, int]] = field(default_factory=list)
    tables: list[tuple[str, int]] = field(default_factory=list)

    @property
    def body_total(self) -> int:
        """Paragraphs + headings (the 'strict' count)."""
        return self.paragraph_words + self.heading_words

    @property
    def with_tables(self) -> int:
        return self.body_total + self.table_words


def count_words(text: str) -> int:
    """Count words using a unicode-safe tokenizer."""
    text = text.strip()
    if not text:
        return 0
    return len(WORD_RE.findall(text))


def should_skip_paragraph(text: str) -> bool:
    """Return True for Feishu artefacts / explicit placeholders."""
    stripped = text.strip()
    if not stripped:
        return True
    for pat in SKIP_PATTERNS:
        if pat.search(stripped):
            return True
    return False


def is_heading(para: Paragraph) -> bool:
    """Detect headings via style name or numeric-section prefix.

    Feishu exports section titles with either a Heading style or plain text
    like '1. Problem Being Solved'.
    """
    style = (para.style.name or "").lower() if para.style else ""
    if style.startswith("heading"):
        return True
    stripped = para.text.strip()
    # Numeric section pattern: "1. Problem...", "6. Assessment"
    if re.match(r"^\d+\.\s+[A-Z]", stripped):
        return True
    # Named subsections in Conclusions: "Algorithm Selection Rationale",
    # "Chronological and Taxonomic Context", "Mechanism Comparison",
    # "Implication for Part 2"
    if re.match(r"^(Algorithm Selection Rationale|Chronological and Taxonomic|"
                r"Mechanism Comparison|Implication for Part)", stripped):
        return True
    return False


def iter_block_items(parent):
    """Yield paragraphs and tables in document order.

    python-docx does not provide this natively; we walk the body XML.
    """
    if isinstance(parent, _Doc):
        parent_elm = parent.element.body
    else:
        raise ValueError("Only document-level iteration is supported")
    for child in parent_elm.iterchildren():
        if child.tag == qn("w:p"):
            yield Paragraph(child, parent)
        elif child.tag == qn("w:tbl"):
            yield Table(child, parent)


def classify_region(current_section: str, para_text: str) -> str:
    """Advance the current section based on a paragraph's text."""
    stripped = para_text.strip()
    if SYNOPSIS_1_MARKER.match(stripped):
        return "synopsis_1"
    if SYNOPSIS_2_MARKER.match(stripped):
        return "synopsis_2"
    if CONCLUSIONS_MARKER.match(stripped):
        return "conclusions"
    if REFERENCES_MARKER.match(stripped):
        return "references"
    if TEAM_STATEMENT_MARKER.match(stripped):
        return "team_statement"
    return current_section


def analyse(docx_path: Path) -> dict[str, SectionCounts]:
    doc = Document(str(docx_path))

    sections = {
        "metadata": SectionCounts("Metadata (title/team/WC/student table)"),
        "synopsis_1": SectionCounts("Synopsis 1: PSO"),
        "synopsis_2": SectionCounts("Synopsis 2: HHO"),
        "conclusions": SectionCounts("Conclusions: Comparative Analysis"),
        "references": SectionCounts("References"),
        "team_statement": SectionCounts("Team Statement"),
    }

    current = "metadata"
    for block in iter_block_items(doc):
        if isinstance(block, Paragraph):
            text = block.text
            # Section transition check (even if paragraph itself is skipped)
            new_section = classify_region(current, text)
            if new_section != current:
                current = new_section
                # The heading paragraph ITSELF (e.g. "Synopsis 1: PSO",
                # "Conclusions: Comparative Analysis") is a section banner.
                # Per spec, banners are part of the report structure — count
                # them under the section they introduce, as a heading.
                if current not in ("references", "team_statement", "metadata"):
                    wc = count_words(text)
                    sections[current].heading_words += wc
                    if wc:
                        sections[current].paragraphs.append((text, wc))
                continue

            if should_skip_paragraph(text):
                continue

            wc = count_words(text)
            if wc == 0:
                continue

            target = sections[current]
            if is_heading(block):
                target.heading_words += wc
            else:
                target.paragraph_words += wc
            target.paragraphs.append((text, wc))

        elif isinstance(block, Table):
            # Tables are always "figures" under our rule — count for info,
            # but never include in the strict total.
            table_text_parts = []
            for row in block.rows:
                for cell in row.cells:
                    table_text_parts.append(cell.text)
            joined = " ".join(table_text_parts)
            wc = count_words(joined)
            label = joined[:60].replace("\n", " ") + ("…" if len(joined) > 60 else "")
            sections[current].table_words += wc
            sections[current].tables.append((label, wc))

    return sections


def format_report(sections: dict[str, SectionCounts], verbose: bool, limit: int) -> str:
    lines = []
    lines.append("=" * 72)
    lines.append("CITS4404 Deliverable 1 — Word Count Report")
    lines.append("=" * 72)
    lines.append("")

    # Per-section breakdown
    counted_sections = ["synopsis_1", "synopsis_2", "conclusions"]
    excluded_sections = ["metadata", "references", "team_statement"]

    lines.append("COUNTED (body) — Synopses + Conclusions")
    lines.append("-" * 72)
    total_para = 0
    total_head = 0
    total_table = 0
    for key in counted_sections:
        s = sections[key]
        lines.append(
            f"  {s.name:50s}  "
            f"paras={s.paragraph_words:>5d}  "
            f"heads={s.heading_words:>4d}  "
            f"(tables={s.table_words})"
        )
        total_para += s.paragraph_words
        total_head += s.heading_words
        total_table += s.table_words

    lines.append("")
    lines.append("EXCLUDED per spec — shown for transparency only")
    lines.append("-" * 72)
    excluded_para = 0
    excluded_table = 0
    for key in excluded_sections:
        s = sections[key]
        subtotal = s.body_total + s.table_words
        lines.append(
            f"  {s.name:50s}  "
            f"total={subtotal:>5d}  "
            f"(paras={s.body_total}, tables={s.table_words})"
        )
        excluded_para += s.body_total
        excluded_table += s.table_words

    lines.append("")
    lines.append("=" * 72)
    lines.append("FINAL COUNTS")
    lines.append("=" * 72)

    strict = total_para + total_head
    with_tables = strict + total_table
    full_doc = strict + total_table + excluded_para + excluded_table

    def status(n: int) -> str:
        if n > limit:
            return f"❌ OVER by {n - limit}"
        remaining = limit - n
        pct = 100 * n / limit
        return f"✅ under limit ({remaining} words remaining, {pct:.1f}% used)"

    lines.append(f"  [STRICT]    Body only (Synopses + Conclusions, paragraphs + headings)")
    lines.append(f"              = {strict} words   → limit {limit}: {status(strict)}")
    lines.append("")
    lines.append(f"  [+ TABLES]  Body + in-scope tables (Results / Mechanism / equations)")
    lines.append(f"              = {with_tables} words")
    lines.append("")
    lines.append(f"  [DEBUG]     Whole document including metadata / refs / team stmt")
    lines.append(f"              = {full_doc} words")
    lines.append("")
    lines.append("  → Submit against the [STRICT] number.")
    lines.append("    It applies the official rule: 'excluding figures and references'.")
    lines.append("")

    if verbose:
        lines.append("=" * 72)
        lines.append("VERBOSE BREAKDOWN")
        lines.append("=" * 72)
        for key in counted_sections:
            s = sections[key]
            lines.append(f"\n--- {s.name} ---")
            for text, wc in s.paragraphs:
                preview = text[:90].replace("\n", " ")
                if len(text) > 90:
                    preview += "…"
                lines.append(f"  [{wc:4d}w]  {preview}")
            if s.tables:
                lines.append("  [excluded tables in this section]:")
                for label, wc in s.tables:
                    lines.append(f"    [{wc:4d}w]  {label}")

    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Count words in a CITS4404 Deliverable 1 .docx, "
                    "applying the spec's 'excluding figures and references' rule."
    )
    ap.add_argument("docx", type=Path, help="Path to the .docx file")
    ap.add_argument("-v", "--verbose", action="store_true",
                    help="Show per-paragraph breakdown")
    ap.add_argument("--limit", type=int, default=3000,
                    help="Word limit (default 3000)")
    args = ap.parse_args()

    if not args.docx.exists():
        print(f"ERROR: file not found: {args.docx}", file=sys.stderr)
        return 2

    sections = analyse(args.docx)
    report = format_report(sections, args.verbose, args.limit)
    print(report)

    strict = (sections["synopsis_1"].body_total
              + sections["synopsis_2"].body_total
              + sections["conclusions"].body_total)
    return 0 if strict <= args.limit else 1


if __name__ == "__main__":
    sys.exit(main())
