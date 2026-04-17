from __future__ import annotations

import json
from types import SimpleNamespace

import pandas as pd
import pytest

from toolkit.csv_tools import (
    _build_mask,
    _parse_where_expression,
    handle_csv_filter_rows,
    handle_csv_find_columns,
    handle_csv_read_cols,
    handle_csv_read_rows,
)


def test_parse_where_expression_valid_contains() -> None:
    clause = _parse_where_expression("City contains Perth")
    assert clause.column == "City"
    assert clause.operator == "contains"
    assert clause.value == "Perth"


def test_parse_where_expression_no_spaces() -> None:
    clause = _parse_where_expression("City=Perth")
    assert clause.column == "City"
    assert clause.operator == "="
    assert clause.value == "Perth"


def test_parse_where_expression_invalid() -> None:
    with pytest.raises(ValueError, match="INVALID_WHERE_EXPRESSION"):
        _parse_where_expression("BrokenExpression")


def test_build_mask_type_mismatch() -> None:
    df = pd.DataFrame({"Name": ["Alice", "Bob"]})
    clause = _parse_where_expression("Name>=1")
    with pytest.raises(TypeError, match="TYPE_MISMATCH"):
        _build_mask(df, clause)


def test_build_mask_type_mismatch_non_numeric_value() -> None:
    df = pd.DataFrame({"Age": [25, 30]})
    clause = _parse_where_expression("Age>=abc")
    with pytest.raises(TypeError, match="TYPE_MISMATCH"):
        _build_mask(df, clause)


def test_build_mask_operators() -> None:
    df = pd.DataFrame({"Age": [20, 30, 40], "Name": ["Alice", "Bob", "Charlie"]})

    assert _build_mask(df, _parse_where_expression("Age=30")).tolist() == [False, True, False]
    assert _build_mask(df, _parse_where_expression("Age!=30")).tolist() == [True, False, True]
    assert _build_mask(df, _parse_where_expression("Age>25")).tolist() == [False, True, True]
    assert _build_mask(df, _parse_where_expression("Age<35")).tolist() == [True, True, False]
    assert _build_mask(df, _parse_where_expression("Age<=30")).tolist() == [True, True, False]
    assert _build_mask(df, _parse_where_expression("Name~=^A")).tolist() == [True, False, False]


def test_csv_read_rows_table_keeps_header(tmp_path, capsys: pytest.CaptureFixture[str]) -> None:
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text("Name,Age\nAlice,30\nBob,25\n", encoding="utf-8")
    args = SimpleNamespace(
        file=str(csv_file),
        start=2,
        end=2,
        output="table",
        table_charset="ascii",
    )

    code = handle_csv_read_rows(args)
    assert code == 0
    out = capsys.readouterr().out
    assert "Name" in out
    assert "Age" in out
    assert "Bob" in out


def test_csv_read_rows_invalid_range(tmp_path, capsys: pytest.CaptureFixture[str]) -> None:
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text("Name,Age\nAlice,30\n", encoding="utf-8")
    args = SimpleNamespace(file=str(csv_file), start=2, end=1, output="json", table_charset="utf8")
    code = handle_csv_read_rows(args)
    assert code == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["error"]["code"] == "INVALID_RANGE"


def test_csv_read_cols_success(tmp_path, capsys: pytest.CaptureFixture[str]) -> None:
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text("A,B,C,D\n1,2,3,4\n5,6,7,8\n", encoding="utf-8")
    args = SimpleNamespace(file=str(csv_file), start_col=2, end_col=3, output="table", table_charset="utf8")

    code = handle_csv_read_cols(args)
    assert code == 0
    out = capsys.readouterr().out
    assert "B" in out
    assert "C" in out
    assert "A" not in out
    assert "D" not in out


def test_csv_read_cols_out_of_bounds(tmp_path, capsys: pytest.CaptureFixture[str]) -> None:
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text("A,B\n1,2\n", encoding="utf-8")
    args = SimpleNamespace(file=str(csv_file), start_col=1, end_col=3, output="json", table_charset="utf8")
    code = handle_csv_read_cols(args)
    assert code == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["error"]["code"] == "INVALID_RANGE"


def test_csv_find_columns_success(tmp_path, capsys: pytest.CaptureFixture[str]) -> None:
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text("UserName,Age,UserEmail\nAlice,30,a@b.com\n", encoding="utf-8")
    args = SimpleNamespace(file=str(csv_file), keyword="User", ignore_case=False, output="json", table_charset="utf8")

    code = handle_csv_find_columns(args)
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["ok"] is True
    assert payload["meta"]["row_count"] == 2
    assert "UserName" in [r["matched_columns"] for r in payload["data"]]
    assert "UserEmail" in [r["matched_columns"] for r in payload["data"]]


def test_csv_find_columns_ignore_case(tmp_path, capsys: pytest.CaptureFixture[str]) -> None:
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text("Username,AGE\nAlice,30\n", encoding="utf-8")
    args = SimpleNamespace(file=str(csv_file), keyword="age", ignore_case=True, output="json", table_charset="utf8")

    code = handle_csv_find_columns(args)
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    columns = [r["matched_columns"] for r in payload["data"]]
    assert "AGE" in columns


def test_csv_filter_rows_column_not_found(tmp_path, capsys: pytest.CaptureFixture[str]) -> None:
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text("Name,Age\nAlice,30\nBob,25\n", encoding="utf-8")
    args = SimpleNamespace(
        file=str(csv_file),
        where=["Unknown=1"],
        output="json",
        table_charset="utf8",
    )

    code = handle_csv_filter_rows(args)
    assert code == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["ok"] is False
    assert payload["error"]["code"] == "COLUMN_NOT_FOUND"


def test_csv_filter_rows_multi_where(tmp_path, capsys: pytest.CaptureFixture[str]) -> None:
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text("Name,Age,City\nAlice,30,Perth\nBob,25,Sydney\nCharlie,30,Perth\n", encoding="utf-8")
    args = SimpleNamespace(
        file=str(csv_file),
        where=["Age=30", "City contains Perth"],
        output="json",
        table_charset="utf8",
    )

    code = handle_csv_filter_rows(args)
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert len(payload["data"]) == 2
    names = {r["Name"] for r in payload["data"]}
    assert names == {"Alice", "Charlie"}


def test_csv_file_not_found(capsys: pytest.CaptureFixture[str]) -> None:
    args = SimpleNamespace(file="/nonexistent/file.csv", start=1, end=1, output="json", table_charset="utf8")
    code = handle_csv_read_rows(args)
    assert code == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["error"]["code"] == "FILE_NOT_FOUND"


def test_csv_invalid_file_type(tmp_path, capsys: pytest.CaptureFixture[str]) -> None:
    bad_file = tmp_path / "data.txt"
    bad_file.write_text("not a csv", encoding="utf-8")
    args = SimpleNamespace(file=str(bad_file), start=1, end=1, output="json", table_charset="utf8")
    code = handle_csv_read_rows(args)
    assert code == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["error"]["code"] == "INVALID_FILE_TYPE"
