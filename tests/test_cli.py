from __future__ import annotations

import pytest

from toolkit.cli import build_parser


def test_pdf_accepts_table_charset_flag() -> None:
    parser = build_parser()
    args = parser.parse_args(
        [
            "pdf",
            "read-pages",
            "--file",
            "a.pdf",
            "--start-page",
            "1",
            "--end-page",
            "1",
            "--table-charset",
            "utf8",
        ]
    )
    assert args.table_charset == "utf8"


def test_csv_accepts_table_charset_flag() -> None:
    parser = build_parser()
    args = parser.parse_args(
        [
            "csv",
            "read-rows",
            "--file",
            "a.csv",
            "--start",
            "1",
            "--end",
            "1",
            "--table-charset",
            "ascii",
        ]
    )
    assert args.table_charset == "ascii"


def test_main_no_args_exits_with_help(capsys: pytest.CaptureFixture[str]) -> None:
    from toolkit.cli import main
    code = main([])
    assert code == 1
    out = capsys.readouterr().out
    assert "usage:" in out.lower()

