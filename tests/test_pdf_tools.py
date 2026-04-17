from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

import toolkit.pdf_tools as pdf_tools


class _FakePage:
    def __init__(self, text: str) -> None:
        self._text = text

    def extract_text(self) -> str:
        return self._text


class _FakeReader:
    def __init__(self, texts: list[str]) -> None:
        self.pages = [_FakePage(text) for text in texts]


def test_pdf_read_pages_out_of_range(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(pdf_tools, "_load_pdf", lambda _: _FakeReader(["p1", "p2"]))
    args = SimpleNamespace(file="fake.pdf", start_page=1, end_page=3, output="json", table_charset="utf8")

    code = pdf_tools.handle_pdf_read_pages(args)
    assert code == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["error"]["code"] == "PAGE_OUT_OF_RANGE"


def test_pdf_read_pages_success_json(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(pdf_tools, "_load_pdf", lambda _: _FakeReader(["alpha", "beta", "gamma"]))
    args = SimpleNamespace(file="fake.pdf", start_page=1, end_page=2, output="json", table_charset="utf8")

    code = pdf_tools.handle_pdf_read_pages(args)
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["ok"] is True
    assert payload["meta"]["page_count"] == 2
    assert payload["meta"]["pages"] == [1, 2]
    assert payload["data"][0]["content"] == "alpha"
    assert payload["data"][1]["content"] == "beta"


def test_pdf_read_pages_success_table(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(pdf_tools, "_load_pdf", lambda _: _FakeReader(["alpha"]))
    args = SimpleNamespace(file="fake.pdf", start_page=1, end_page=1, output="table", table_charset="ascii")

    code = pdf_tools.handle_pdf_read_pages(args)
    assert code == 0
    out = capsys.readouterr().out
    assert "page" in out
    assert "content" in out
    assert "alpha" in out


def test_pdf_find_keyword_ignore_case(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(pdf_tools, "_load_pdf", lambda _: _FakeReader(["alpha", "Swarm paper", "beta"]))
    args = SimpleNamespace(file="fake.pdf", keyword="swarm", ignore_case=True, output="json", table_charset="utf8")

    code = pdf_tools.handle_pdf_find_keyword(args)
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["ok"] is True
    assert payload["meta"]["pages"] == [2]
    assert payload["data"][0]["page"] == 2


def test_pdf_find_keyword_case_sensitive(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(pdf_tools, "_load_pdf", lambda _: _FakeReader(["Swarm", "swarm", "SWARM"]))
    args = SimpleNamespace(file="fake.pdf", keyword="Swarm", ignore_case=False, output="json", table_charset="utf8")

    code = pdf_tools.handle_pdf_find_keyword(args)
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    pages = payload["meta"]["pages"]
    assert pages == [1]


def test_pdf_file_not_found(capsys: pytest.CaptureFixture[str]) -> None:
    args = SimpleNamespace(file="/nonexistent/file.pdf", start_page=1, end_page=1, output="json", table_charset="utf8")
    code = pdf_tools.handle_pdf_read_pages(args)
    assert code == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["error"]["code"] == "FILE_NOT_FOUND"


def test_pdf_invalid_file_type(tmp_path, capsys: pytest.CaptureFixture[str]) -> None:
    bad_file = tmp_path / "data.txt"
    bad_file.write_text("not a pdf", encoding="utf-8")
    args = SimpleNamespace(file=str(bad_file), start_page=1, end_page=1, output="json", table_charset="utf8")
    code = pdf_tools.handle_pdf_read_pages(args)
    assert code == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["error"]["code"] == "INVALID_FILE_TYPE"
