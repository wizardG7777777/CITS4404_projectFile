from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Any, Callable
from zipfile import ZipFile

from toolkit.output_utils import print_error, print_json, render_table, validate_file

try:
    from docx import Document
except Exception:  # pragma: no cover - optional dependency until installed
    Document = None


WORD_RE = re.compile(r"\b[\w'-]+\b", re.UNICODE)
HEADING_RE = re.compile(r"^\s*(\d+(\.\d+)*\.?)\s+.+$")


@dataclass
class SectionStat:
    section: str
    words: int
    estimated_pages: int


def docx_handler(wrapped: Callable[..., int]) -> Callable[..., int]:
    def wrapper(*args: Any, **kwargs: Any) -> int:
        try:
            return wrapped(*args, **kwargs)
        except FileNotFoundError:
            print_error("FILE_NOT_FOUND", "DOCX file does not exist")
        except ValueError as exc:
            code = str(exc)
            if code == "INVALID_FILE_TYPE":
                print_error(code, "Only .docx files are supported")
            elif code == "DOCX_LIB_MISSING":
                print_error("MISSING_DEPENDENCY", "python-docx is required. Run: uv add python-docx")
            else:
                print_error("DOCX_READ_ERROR", f"Failed to read DOCX file: {exc}")
        except Exception as exc:  # pragma: no cover - safety net
            print_error("DOCX_READ_ERROR", f"Failed to read DOCX file: {exc}")
        return 1

    return wrapper


def _count_words(text: str) -> int:
    text = text.strip()
    if not text:
        return 0
    return len(WORD_RE.findall(text))


def _is_heading(paragraph: Any) -> bool:
    text = (paragraph.text or "").strip()
    style_name = ""
    if getattr(paragraph, "style", None) and getattr(paragraph.style, "name", None):
        style_name = str(paragraph.style.name).lower()
    return style_name.startswith("heading") or bool(HEADING_RE.match(text))


def _estimate_pages(word_count: int, words_per_page: int) -> int:
    if word_count <= 0:
        return 0
    return max(1, math.ceil(word_count / words_per_page))


def _count_explicit_page_breaks(docx_path: str) -> int:
    # Count explicit page breaks from document XML.
    with ZipFile(docx_path) as zf:
        xml = zf.read("word/document.xml").decode("utf-8", errors="ignore")
    return xml.count('w:br w:type="page"') + xml.count("w:lastRenderedPageBreak")


def _extract_stats(file_path: str, words_per_page: int) -> dict[str, Any]:
    if Document is None:
        raise ValueError("DOCX_LIB_MISSING")

    validate_file(file_path, ".docx")
    doc = Document(file_path)
    paragraphs = list(doc.paragraphs)

    paragraph_stats: list[dict[str, Any]] = []
    total_words = 0
    section_words: dict[str, int] = {}
    current_section = "Document"

    for idx, para in enumerate(paragraphs, start=1):
        text = (para.text or "").strip()
        words = _count_words(text)
        total_words += words
        paragraph_stats.append(
            {
                "index": idx,
                "text": text,
                "word_count": words,
                "is_heading": _is_heading(para),
            }
        )

        if _is_heading(para) and text:
            current_section = text
            section_words.setdefault(current_section, 0)
            continue
        section_words.setdefault(current_section, 0)
        section_words[current_section] += words

    explicit_breaks = _count_explicit_page_breaks(file_path)
    estimated_pages_by_words = _estimate_pages(total_words, words_per_page)
    explicit_pages = explicit_breaks + 1 if paragraphs else 0
    total_estimated_pages = max(estimated_pages_by_words, explicit_pages)

    sections: list[SectionStat] = []
    for section_name, words in section_words.items():
        sections.append(
            SectionStat(
                section=section_name,
                words=words,
                estimated_pages=_estimate_pages(words, words_per_page),
            )
        )

    sections.sort(key=lambda item: item.section)
    return {
        "total_words": total_words,
        "paragraph_count": len(paragraphs),
        "paragraph_word_counts": paragraph_stats,
        "section_page_estimates": [
            {"section": item.section, "words": item.words, "estimated_pages": item.estimated_pages}
            for item in sections
        ],
        "total_pages_estimated": total_estimated_pages,
        "page_estimation": {
            "words_per_page": words_per_page,
            "estimated_by_words": estimated_pages_by_words,
            "explicit_page_breaks": explicit_breaks,
            "estimated_by_explicit_breaks": explicit_pages,
        },
    }


def _print_docx_output(args: Any, stats: dict[str, Any]) -> None:
    if args.output == "json":
        payload = {
            "ok": True,
            "command": "docx stats",
            "meta": {
                "file": args.file,
                "paragraph_count": stats["paragraph_count"],
                "total_words": stats["total_words"],
                "total_pages_estimated": stats["total_pages_estimated"],
            },
            "data": {
                "page_estimation": stats["page_estimation"],
                "section_page_estimates": stats["section_page_estimates"],
                "paragraph_word_counts": stats["paragraph_word_counts"],
            },
        }
        print_json(payload)
        return

    print(
        render_table(
            ["metric", "value"],
            [
                ["total_words", str(stats["total_words"])],
                ["paragraph_count", str(stats["paragraph_count"])],
                ["total_pages_estimated", str(stats["total_pages_estimated"])],
                ["words_per_page", str(stats["page_estimation"]["words_per_page"])],
                ["explicit_page_breaks", str(stats["page_estimation"]["explicit_page_breaks"])],
            ],
            args.table_charset,
        )
    )

    section_rows = [
        [item["section"], str(item["words"]), str(item["estimated_pages"])]
        for item in stats["section_page_estimates"]
    ]
    print("")
    print(render_table(["section", "words", "estimated_pages"], section_rows, args.table_charset))

    para_rows = [
        [
            str(item["index"]),
            str(item["word_count"]),
            "yes" if item["is_heading"] else "no",
            item["text"],
        ]
        for item in stats["paragraph_word_counts"][: args.max_paragraphs]
    ]
    print("")
    print(render_table(["paragraph", "words", "heading", "text"], para_rows, args.table_charset))


@docx_handler
def handle_docx_stats(args: Any) -> int:
    if args.words_per_page < 100:
        print_error("INVALID_RANGE", "words-per-page must be >= 100")
        return 1
    if args.max_paragraphs < 1:
        print_error("INVALID_RANGE", "max-paragraphs must be >= 1")
        return 1

    stats = _extract_stats(args.file, args.words_per_page)
    _print_docx_output(args, stats)
    return 0

