from __future__ import annotations

import re
from dataclasses import dataclass
from functools import wraps
from pathlib import Path
from typing import Any, Callable

import pandas as pd

from toolkit.output_utils import print_error, print_json, render_table, validate_file

SUPPORTED_OPERATORS = ("contains", "~=", "!=", ">=", "<=", "=", ">", "<")

WHERE_RE = re.compile(
    r"^(?P<col>.*?)\s*(?P<op>contains|~=|!=|>=|<=|=|>|<)\s*(?P<val>.+)$"
)


@dataclass
class WhereClause:
    column: str
    operator: str
    value: str


def csv_handler(wrapped: Callable[..., int]) -> Callable[..., int]:
    @wraps(wrapped)
    def wrapper(*args: Any, **kwargs: Any) -> int:
        try:
            return wrapped(*args, **kwargs)
        except FileNotFoundError:
            print_error("FILE_NOT_FOUND", "CSV file does not exist")
        except KeyError:
            print_error("COLUMN_NOT_FOUND", "Column in where expression was not found")
        except TypeError as exc:
            code = str(exc)
            if code == "TYPE_MISMATCH":
                print_error("TYPE_MISMATCH", "Numeric comparison used on non-numeric column")
            else:
                print_error("CSV_READ_ERROR", f"Failed to read CSV file: {exc}")
        except ValueError as exc:
            code = str(exc)
            if code == "INVALID_FILE_TYPE":
                print_error(code, "Only .csv files are supported")
            elif code == "INVALID_WHERE_EXPRESSION":
                print_error(code, "Where expression must match <column> <operator> <value>")
            else:
                print_error("CSV_READ_ERROR", f"Failed to read CSV file: {exc}")
        except Exception as exc:  # pragma: no cover - safety net
            print_error("CSV_READ_ERROR", f"Failed to read CSV file: {exc}")
        return 1

    return wrapper


def _load_csv(path: str) -> pd.DataFrame:
    file_path = validate_file(path, ".csv")
    try:
        df = pd.read_csv(file_path, sep=None, engine="python")
    except Exception:
        df = pd.read_csv(file_path, sep=";", engine="python")
    df.columns = [str(col).strip().lstrip("\ufeff") for col in df.columns]
    return df


def _to_rows(df: pd.DataFrame) -> list[list[str]]:
    return df.fillna("").astype(str).values.tolist()


def _print_df_table(df: pd.DataFrame, charset: str) -> None:
    headers = [str(col) for col in df.columns]
    rows = _to_rows(df)
    print(render_table(headers, rows, charset))


def _parse_where_expression(expr: str) -> WhereClause:
    m = WHERE_RE.match(expr.strip())
    if not m:
        raise ValueError("INVALID_WHERE_EXPRESSION")
    column = m.group("col").strip()
    operator = m.group("op")
    value = m.group("val").strip().strip("\"'")
    if not column or not value or operator not in SUPPORTED_OPERATORS:
        raise ValueError("INVALID_WHERE_EXPRESSION")
    return WhereClause(column=column, operator=operator, value=value)


def _build_mask(df: pd.DataFrame, clause: WhereClause) -> pd.Series:
    if clause.column not in df.columns:
        raise KeyError("COLUMN_NOT_FOUND")

    series = df[clause.column]
    op = clause.operator
    value = clause.value

    if op in (">", ">=", "<", "<="):
        non_null = series.dropna()
        converted = pd.to_numeric(non_null, errors="coerce")
        if converted.isna().any():
            raise TypeError("TYPE_MISMATCH")
        left = pd.to_numeric(series, errors="coerce")
        try:
            right = float(value)
        except ValueError as exc:
            raise TypeError("TYPE_MISMATCH") from exc
        if op == ">":
            return left > right
        if op == ">=":
            return left >= right
        if op == "<":
            return left < right
        return left <= right

    if op == "=":
        return series.astype(str) == value
    if op == "!=":
        return series.astype(str) != value
    if op == "contains":
        return series.astype(str).str.contains(value, regex=False, na=False)
    if op == "~=":
        try:
            return series.astype(str).str.contains(value, regex=True, na=False)
        except re.error as exc:
            raise ValueError("INVALID_WHERE_EXPRESSION") from exc

    raise ValueError("INVALID_WHERE_EXPRESSION")


def _print_output(command: str, df: pd.DataFrame, args: Any) -> None:
    if args.output == "json":
        payload = {
            "ok": True,
            "command": command,
            "meta": {
                "file": args.file,
                "row_count": int(len(df)),
                "columns": [str(col) for col in df.columns],
            },
            "data": df.where(pd.notna(df), None).to_dict(orient="records"),
        }
        print_json(payload)
        return
    _print_df_table(df, args.table_charset)


@csv_handler
def handle_csv_read_rows(args: Any) -> int:
    if args.start < 1 or args.end < 1:
        print_error("INVALID_RANGE", "start and end must be greater than or equal to 1")
        return 1
    if args.start > args.end:
        print_error("INVALID_RANGE", "start must be less than or equal to end")
        return 1
    df = _load_csv(args.file)
    start_idx = args.start - 1
    end_idx = args.end
    filtered = df.iloc[start_idx:end_idx]
    _print_output("csv read-rows", filtered, args)
    return 0


@csv_handler
def handle_csv_read_cols(args: Any) -> int:
    if args.start_col < 1 or args.end_col < 1:
        print_error("INVALID_RANGE", "start-col and end-col must be >= 1")
        return 1
    if args.start_col > args.end_col:
        print_error("INVALID_RANGE", "start-col must be less than or equal to end-col")
        return 1
    df = _load_csv(args.file)
    if args.end_col > len(df.columns):
        print_error("INVALID_RANGE", "column range is out of bounds")
        return 1
    filtered = df.iloc[:, args.start_col - 1 : args.end_col]
    _print_output("csv read-cols", filtered, args)
    return 0


@csv_handler
def handle_csv_find_columns(args: Any) -> int:
    df = _load_csv(args.file)
    keyword = args.keyword.lower() if args.ignore_case else args.keyword
    matches = []
    for col in df.columns:
        col_name = str(col)
        target = col_name.lower() if args.ignore_case else col_name
        if keyword in target:
            matches.append(col_name)

    result_df = pd.DataFrame({"matched_columns": matches})
    _print_output("csv find-columns", result_df, args)
    return 0


@csv_handler
def handle_csv_filter_rows(args: Any) -> int:
    df = _load_csv(args.file)
    mask = pd.Series([True] * len(df))
    for expr in args.where:
        clause = _parse_where_expression(expr)
        clause_mask = _build_mask(df, clause)
        mask &= clause_mask.fillna(False)
    filtered = df[mask]
    _print_output("csv filter-rows", filtered, args)
    return 0
