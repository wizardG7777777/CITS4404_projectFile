from __future__ import annotations

import argparse
from typing import Callable

from toolkit.csv_tools import (
    handle_csv_filter_rows,
    handle_csv_find_columns,
    handle_csv_read_cols,
    handle_csv_read_rows,
)
from toolkit.output_utils import print_error
from toolkit.pdf_tools import handle_pdf_find_keyword, handle_pdf_read_pages


def _add_csv_common_output_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--output", choices=["table", "json"], default="table")
    parser.add_argument("--table-charset", choices=["utf8", "ascii"], default="utf8")


def _add_pdf_common_output_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--output", choices=["table", "json"], default="table")
    parser.add_argument("--table-charset", choices=["utf8", "ascii"], default="utf8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="toolkit", description="CSV/PDF reader toolkit")
    subparsers = parser.add_subparsers(dest="resource")

    csv_parser = subparsers.add_parser("csv", help="CSV operations")
    csv_subparsers = csv_parser.add_subparsers(dest="command")

    csv_read_rows = csv_subparsers.add_parser("read-rows", help="Read a row range from CSV")
    csv_read_rows.add_argument("--file", required=True)
    csv_read_rows.add_argument("--start", type=int, required=True)
    csv_read_rows.add_argument("--end", type=int, required=True)
    _add_csv_common_output_args(csv_read_rows)
    csv_read_rows.set_defaults(handler=handle_csv_read_rows)

    csv_read_cols = csv_subparsers.add_parser("read-cols", help="Read a column range from CSV")
    csv_read_cols.add_argument("--file", required=True)
    csv_read_cols.add_argument("--start-col", type=int, required=True)
    csv_read_cols.add_argument("--end-col", type=int, required=True)
    _add_csv_common_output_args(csv_read_cols)
    csv_read_cols.set_defaults(handler=handle_csv_read_cols)

    csv_find_columns = csv_subparsers.add_parser("find-columns", help="Find columns by keyword")
    csv_find_columns.add_argument("--file", required=True)
    csv_find_columns.add_argument("--keyword", required=True)
    csv_find_columns.add_argument("--ignore-case", action="store_true")
    _add_csv_common_output_args(csv_find_columns)
    csv_find_columns.set_defaults(handler=handle_csv_find_columns)

    csv_filter_rows = csv_subparsers.add_parser("filter-rows", help="Filter rows by where clauses")
    csv_filter_rows.add_argument("--file", required=True)
    csv_filter_rows.add_argument("--where", action="append", required=True)
    _add_csv_common_output_args(csv_filter_rows)
    csv_filter_rows.set_defaults(handler=handle_csv_filter_rows)

    pdf_parser = subparsers.add_parser("pdf", help="PDF operations")
    pdf_subparsers = pdf_parser.add_subparsers(dest="command")

    pdf_read_pages = pdf_subparsers.add_parser("read-pages", help="Read a page range from PDF")
    pdf_read_pages.add_argument("--file", required=True)
    pdf_read_pages.add_argument("--start-page", type=int, required=True)
    pdf_read_pages.add_argument("--end-page", type=int, required=True)
    _add_pdf_common_output_args(pdf_read_pages)
    pdf_read_pages.set_defaults(handler=handle_pdf_read_pages)

    pdf_find_keyword = pdf_subparsers.add_parser("find-keyword", help="Find keyword in PDF pages")
    pdf_find_keyword.add_argument("--file", required=True)
    pdf_find_keyword.add_argument("--keyword", required=True)
    pdf_find_keyword.add_argument("--ignore-case", action="store_true")
    _add_pdf_common_output_args(pdf_find_keyword)
    pdf_find_keyword.set_defaults(handler=handle_pdf_find_keyword)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    handler: Callable[..., int] | None = getattr(args, "handler", None)
    if not handler:
        parser.print_help()
        return 1
    try:
        return handler(args)
    except BrokenPipeError:
        return 0
    except Exception as exc:  # pragma: no cover - safety net
        print_error("UNEXPECTED_ERROR", f"Unexpected runtime failure: {exc}")
        return 1
