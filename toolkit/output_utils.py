from __future__ import annotations

import json
from pathlib import Path
from typing import Any

MAX_CELL_WIDTH = 120

TABLE_CHARS = {
    "utf8": {
        "h": "─",
        "v": "│",
        "tl": "┌",
        "tr": "┐",
        "bl": "└",
        "br": "┘",
        "jt": "┬",
        "jb": "┴",
        "jl": "├",
        "jr": "┤",
        "jc": "┼",
    },
    "ascii": {
        "h": "-",
        "v": "|",
        "tl": "+",
        "tr": "+",
        "bl": "+",
        "br": "+",
        "jt": "+",
        "jb": "+",
        "jl": "+",
        "jr": "+",
        "jc": "+",
    },
}


def validate_file(path: str, expected_suffix: str) -> Path:
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(path)
    if file_path.suffix.lower() != expected_suffix:
        raise ValueError("INVALID_FILE_TYPE")
    return file_path


def _truncate(text: str, width: int) -> str:
    if len(text) > width:
        return text[: width - 3] + "..."
    return text


def _sanitize(text: str) -> str:
    return text.replace("\r\n", " ").replace("\n", " ").replace("\r", " ").replace("\t", " ")


def print_json(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def _border(widths: list[int], charset: dict[str, str], left: str, mid: str, right: str) -> str:
    parts: list[str] = [left]
    for idx, width in enumerate(widths):
        parts.append(charset["h"] * (width + 2))
        parts.append(mid if idx < len(widths) - 1 else right)
    return "".join(parts)


def _row(values: list[str], widths: list[int], charset: dict[str, str]) -> str:
    cells = [f" {value.ljust(widths[idx])} " for idx, value in enumerate(values)]
    return f"{charset['v']}" + f"{charset['v']}".join(cells) + f"{charset['v']}"


def render_table(headers: list[str], rows: list[list[str]], charset_name: str = "utf8") -> str:
    if charset_name not in TABLE_CHARS:
        charset_name = "utf8"
    charset = TABLE_CHARS[charset_name]

    str_headers = [_sanitize(str(item)) for item in headers]
    str_rows = [[_sanitize(str(cell)) for cell in row] for row in rows]
    widths = [len(h) for h in str_headers]
    for row in str_rows:
        for idx, cell in enumerate(row):
            widths[idx] = max(widths[idx], len(cell))

    widths = [min(w, MAX_CELL_WIDTH) for w in widths]
    str_headers = [_truncate(h, MAX_CELL_WIDTH) for h in str_headers]
    str_rows = [[_truncate(cell, MAX_CELL_WIDTH) for cell in row] for row in str_rows]

    lines = [
        _border(widths, charset, charset["tl"], charset["jt"], charset["tr"]),
        _row(str_headers, widths, charset),
        _border(widths, charset, charset["jl"], charset["jc"], charset["jr"]),
    ]
    for row in str_rows:
        lines.append(_row(row, widths, charset))
    lines.append(_border(widths, charset, charset["bl"], charset["jb"], charset["br"]))
    return "\n".join(lines)


def print_error(code: str, message: str, details: dict[str, Any] | None = None) -> None:
    payload: dict[str, Any] = {
        "ok": False,
        "error": {"code": code, "message": message},
    }
    if details:
        payload["error"]["details"] = details
    print_json(payload)
