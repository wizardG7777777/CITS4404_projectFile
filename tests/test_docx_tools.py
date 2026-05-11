from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

import toolkit.docx_tools as docx_tools


def test_docx_stats_invalid_words_per_page(capsys: pytest.CaptureFixture[str]) -> None:
    args = SimpleNamespace(
        file="fake.docx",
        output="json",
        table_charset="utf8",
        words_per_page=50,
        max_paragraphs=10,
    )
    code = docx_tools.handle_docx_stats(args)
    assert code == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["error"]["code"] == "INVALID_RANGE"


def test_docx_stats_missing_file(capsys: pytest.CaptureFixture[str]) -> None:
    args = SimpleNamespace(
        file="/not/exist.docx",
        output="json",
        table_charset="utf8",
        words_per_page=500,
        max_paragraphs=10,
    )
    code = docx_tools.handle_docx_stats(args)
    assert code == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["error"]["code"] == "FILE_NOT_FOUND"


def test_docx_stats_json_output(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    fake = {
        "total_words": 1200,
        "paragraph_count": 8,
        "paragraph_word_counts": [
            {"index": 1, "text": "Title", "word_count": 1, "is_heading": True},
            {"index": 2, "text": "Body text", "word_count": 2, "is_heading": False},
        ],
        "section_page_estimates": [
            {"section": "1 Intro", "words": 400, "estimated_pages": 1},
            {"section": "2 Methods", "words": 800, "estimated_pages": 2},
        ],
        "total_pages_estimated": 3,
        "page_estimation": {
            "words_per_page": 500,
            "estimated_by_words": 3,
            "explicit_page_breaks": 1,
            "estimated_by_explicit_breaks": 2,
        },
    }

    monkeypatch.setattr(docx_tools, "_extract_stats", lambda *_: fake)
    args = SimpleNamespace(
        file="fake.docx",
        output="json",
        table_charset="utf8",
        words_per_page=500,
        max_paragraphs=10,
    )

    code = docx_tools.handle_docx_stats(args)
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["ok"] is True
    assert payload["meta"]["total_words"] == 1200
    assert payload["meta"]["total_pages_estimated"] == 3
    assert payload["data"]["section_page_estimates"][1]["section"] == "2 Methods"

