from __future__ import annotations

from functools import wraps
from pathlib import Path
from typing import Any, Callable

from pypdf import PdfReader

from toolkit.output_utils import print_error, print_json, render_table, validate_file


def pdf_handler(wrapped: Callable[..., int]) -> Callable[..., int]:
    @wraps(wrapped)
    def wrapper(*args: Any, **kwargs: Any) -> int:
        try:
            return wrapped(*args, **kwargs)
        except FileNotFoundError:
            print_error("FILE_NOT_FOUND", "PDF file does not exist")
        except ValueError as exc:
            code = str(exc)
            if code == "INVALID_FILE_TYPE":
                print_error(code, "Only .pdf files are supported")
            else:
                print_error("PDF_READ_ERROR", f"Failed to read PDF file: {exc}")
        except Exception as exc:  # pragma: no cover - safety net
            print_error("PDF_READ_ERROR", f"Failed to read PDF file: {exc}")
        return 1

    return wrapper


def _load_pdf(path: str) -> PdfReader:
    file_path = validate_file(path, ".pdf")
    return PdfReader(str(file_path))


def _read_page_text(reader: PdfReader, page_index: int) -> str:
    text = reader.pages[page_index].extract_text()
    return text.strip() if text else ""


def _print_pdf_output(
    command: str, file: str, page_records: list[dict[str, Any]], output: str, charset: str = "utf8"
) -> None:
    if output == "json":
        payload = {
            "ok": True,
            "command": command,
            "meta": {
                "file": file,
                "page_count": len(page_records),
                "pages": [record["page"] for record in page_records],
            },
            "data": page_records,
        }
        print_json(payload)
        return

    headers = ["page", "content"]
    rows = [[str(record["page"]), record["content"]] for record in page_records]
    print(render_table(headers, rows, charset))


@pdf_handler
def handle_pdf_read_pages(args: Any) -> int:
    if args.start_page > args.end_page:
        print_error("INVALID_RANGE", "start-page must be less than or equal to end-page")
        return 1

    reader = _load_pdf(args.file)
    total = len(reader.pages)
    if args.start_page < 1 or args.end_page > total:
        print_error(
            "PAGE_OUT_OF_RANGE",
            f"page range must be within 1..{total}",
            {"max_page": total},
        )
        return 1

    records: list[dict[str, Any]] = []
    for page in range(args.start_page, args.end_page + 1):
        records.append({"page": page, "content": _read_page_text(reader, page - 1)})
    _print_pdf_output("pdf read-pages", args.file, records, args.output, args.table_charset)
    return 0


@pdf_handler
def handle_pdf_find_keyword(args: Any) -> int:
    reader = _load_pdf(args.file)
    keyword = args.keyword
    needle = keyword.lower() if args.ignore_case else keyword

    records: list[dict[str, Any]] = []
    for idx in range(len(reader.pages)):
        text = _read_page_text(reader, idx)
        haystack = text.lower() if args.ignore_case else text
        if needle in haystack:
            records.append({"page": idx + 1, "content": text})

    _print_pdf_output("pdf find-keyword", args.file, records, args.output, args.table_charset)
    return 0
