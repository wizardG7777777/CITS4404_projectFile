from __future__ import annotations

import json

import pytest

from toolkit.output_utils import (
    MAX_CELL_WIDTH,
    print_error,
    render_table,
    validate_file,
)


def test_validate_file_success(tmp_path) -> None:
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("a,b", encoding="utf-8")
    path = validate_file(str(csv_file), ".csv")
    assert path.name == "test.csv"


def test_validate_file_not_found() -> None:
    with pytest.raises(FileNotFoundError):
        validate_file("/nonexistent/file.csv", ".csv")


def test_validate_file_invalid_type(tmp_path) -> None:
    txt_file = tmp_path / "test.txt"
    txt_file.write_text("hello", encoding="utf-8")
    with pytest.raises(ValueError, match="INVALID_FILE_TYPE"):
        validate_file(str(txt_file), ".csv")


def test_render_table_utf8() -> None:
    table = render_table(["Name", "Age"], [["Alice", "30"]], charset_name="utf8")
    assert "┌" in table
    assert "│" in table
    assert "Alice" in table
    assert "Age" in table


def test_render_table_ascii() -> None:
    table = render_table(["Name", "Age"], [["Alice", "30"]], charset_name="ascii")
    assert "+" in table
    assert "|" in table
    assert "Alice" in table


def test_render_table_sanitize_newlines() -> None:
    table = render_table(["Col"], [["line1\nline2"]], charset_name="ascii")
    lines = table.splitlines()
    cell_line = [line for line in lines if "line1" in line or "line2" in line][0]
    assert "\n" not in cell_line
    assert "line1 line2" in cell_line


def test_render_table_truncate_long_text() -> None:
    long_text = "x" * (MAX_CELL_WIDTH + 10)
    table = render_table(["Col"], [[long_text]], charset_name="ascii")
    assert "..." in table
    # The cell should be truncated to MAX_CELL_WIDTH characters
    line_with_cell = [line for line in table.splitlines() if "x" in line][0]
    # Count raw x's in that line (excluding padding and borders)
    raw = line_with_cell.strip("| ")
    assert len(raw) <= MAX_CELL_WIDTH


def test_print_error_with_details(capsys: pytest.CaptureFixture[str]) -> None:
    print_error("ERR_CODE", "Something went wrong", details={"foo": 42})
    out = capsys.readouterr().out
    payload = json.loads(out)
    assert payload["ok"] is False
    assert payload["error"]["code"] == "ERR_CODE"
    assert payload["error"]["message"] == "Something went wrong"
    assert payload["error"]["details"] == {"foo": 42}


def test_print_error_without_details(capsys: pytest.CaptureFixture[str]) -> None:
    print_error("ERR_CODE", "Something went wrong")
    out = capsys.readouterr().out
    payload = json.loads(out)
    assert payload["ok"] is False
    assert "details" not in payload["error"]
