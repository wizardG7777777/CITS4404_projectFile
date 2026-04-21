"""Deliverable 1 compliance checkers.

Five checkers reachable through the `toolkit check` CLI:
  structure   - Q1..Q6 headings present
  equations   - at least one math/code block (required for detail submissions)
  comparison  - comparison matrix covers required dimensions & roster
  format      - word limit, IEEE cross-refs, Team Statement, placeholder scan
  citations   - references cross-checked against a verified-citations CSV
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from typing import Any

from toolkit.output_utils import print_error, print_json


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

WORD_RE = re.compile(r"[A-Za-z][A-Za-z\-']*")
CITE_RE = re.compile(r"\[(\d{1,3})\]")
REF_LINE_RE = re.compile(r"^\s*\[(\d{1,3})\]\s+(.+)$", re.MULTILINE)
FENCED_BLOCK_RE = re.compile(r"```[\s\S]*?```", re.MULTILINE)
INLINE_CODE_RE = re.compile(r"`[^`]*`")
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)

PLACEHOLDER_PATTERNS = [
    r"\bTODO\b",
    r"\bTBD\b",
    r"\bFIXME\b",
    r"\[CITATION REMOVED\]",
    r"\[citation needs verification\]",
    r"needs verification",
    r"XXX+",
    r"\bplaceholder\b",
]

# Six required question sections (case-insensitive substring tests).
# Each tuple is (label, regex-alternatives).
Q_PATTERNS: list[tuple[str, str]] = [
    ("Q1_Problem",        r"problem(\s+being\s+solved)?|what\s+problem"),
    ("Q2_PreviousFail",   r"previous\s+failures?|previous\s+attempts|why.*failed"),
    ("Q3_Novelty",        r"novelty|new\s+idea|core\s+innovation|core\s+equation"),
    ("Q4_Demonstration",  r"demonstration|demonstrated|validation|experiments?"),
    ("Q5_Results",        r"\bresults?\b|outcomes?"),
    ("Q6_Assessment",     r"assessment|evaluation|critique"),
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _strip_markdown_for_wordcount(text: str) -> str:
    text = FENCED_BLOCK_RE.sub(" ", text)
    text = INLINE_CODE_RE.sub(" ", text)
    text = re.sub(r"^#+\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"\!\[.*?\]\(.*?\)", " ", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[*_>`~|]", " ", text)
    return text


def _word_count(text: str) -> int:
    return len(WORD_RE.findall(_strip_markdown_for_wordcount(text)))


def _headings(text: str) -> list[str]:
    return [m.strip() for m in HEADING_RE.findall(text)]


def _emit(payload: dict[str, Any], as_json: bool) -> int:
    if as_json:
        print_json(payload)
    else:
        _print_human(payload)
    return 0 if payload["ok"] else 1


def _print_human(payload: dict[str, Any]) -> None:
    tool = payload.get("tool", "?")
    status = "OK" if payload["ok"] else "FAIL"
    print(f"[{status}] {tool}  file={payload.get('file', '?')}")
    for f in payload.get("findings", []):
        lvl = f.get("level", "info").upper()
        print(f"  - {lvl}: {f.get('message', '')}")
    summary = payload.get("summary", {})
    if summary:
        print(f"  summary: {summary}")


def _finding(level: str, message: str, **detail: Any) -> dict[str, Any]:
    entry: dict[str, Any] = {"level": level, "message": message}
    if detail:
        entry["detail"] = detail
    return entry


def _summarize(findings: list[dict[str, Any]]) -> dict[str, int]:
    out = {"errors": 0, "warnings": 0, "infos": 0}
    for f in findings:
        lvl = f.get("level", "info")
        if lvl == "error":
            out["errors"] += 1
        elif lvl == "warning":
            out["warnings"] += 1
        else:
            out["infos"] += 1
    return out


# ---------------------------------------------------------------------------
# T1: structure
# ---------------------------------------------------------------------------

def check_structure(file_path: Path) -> dict[str, Any]:
    text = _read(file_path)
    headings = _headings(text)
    joined = "\n".join(headings).lower()
    findings: list[dict[str, Any]] = []
    missing: list[str] = []
    for label, pattern in Q_PATTERNS:
        if not re.search(pattern, joined, re.IGNORECASE):
            missing.append(label)
            findings.append(_finding("error", f"missing required section: {label}"))
    if not missing:
        findings.append(_finding("info", "all six Q1..Q6 sections detected"))
    summary = _summarize(findings)
    return {
        "ok": not missing,
        "tool": "structure",
        "file": str(file_path),
        "findings": findings,
        "summary": summary,
        "detail": {"headings_found": headings, "missing_sections": missing},
    }


def handle_check_structure(args: argparse.Namespace) -> int:
    return _run_on_target(args, check_structure)


# ---------------------------------------------------------------------------
# T2: equations
# ---------------------------------------------------------------------------

MATH_HINT_RE = re.compile(r"[=+\-*/^]|\\[a-zA-Z]+|\b(?:sin|cos|log|exp|sqrt)\b")


def check_equations(file_path: Path) -> dict[str, Any]:
    text = _read(file_path)
    blocks = FENCED_BLOCK_RE.findall(text)
    math_blocks = [b for b in blocks if MATH_HINT_RE.search(b)]
    findings: list[dict[str, Any]] = []
    if not blocks:
        findings.append(_finding("error", "no fenced code/equation block found"))
    elif not math_blocks:
        findings.append(_finding(
            "warning",
            f"{len(blocks)} fenced block(s) found but none contain math operators",
        ))
    else:
        findings.append(_finding(
            "info",
            f"{len(math_blocks)} equation-like block(s) detected",
        ))
    ok = bool(math_blocks)
    return {
        "ok": ok,
        "tool": "equations",
        "file": str(file_path),
        "findings": findings,
        "summary": _summarize(findings),
        "detail": {"fenced_blocks": len(blocks), "math_blocks": len(math_blocks)},
    }


def handle_check_equations(args: argparse.Namespace) -> int:
    return _run_on_target(args, check_equations)


# ---------------------------------------------------------------------------
# T3: comparison
# ---------------------------------------------------------------------------

DEFAULT_ROSTER = [
    "ACO", "PSO", "ABC", "BBO", "CS", "FA", "BA", "FFO", "KH", "SMO",
    "GWO", "CSO", "MFO", "EHO", "WOA", "DA", "SSA", "GOA", "HHO", "MRFO",
]

DIMENSION_PATTERNS: dict[str, str] = {
    "mechanism": r"mechanism|机制|update|更新|operator|算子",
    "balance":   r"exploration|exploitation|balance|平衡|开发|探索",
    "chronology": r"chronolog|timeline|年代|演进|history|1992|1995|20\d{2}",
}


def check_comparison(file_path: Path, roster: list[str] | None = None) -> dict[str, Any]:
    text = _read(file_path)
    findings: list[dict[str, Any]] = []
    lower = text.lower()
    missing_dims = [
        dim for dim, pat in DIMENSION_PATTERNS.items()
        if not re.search(pat, text, re.IGNORECASE)
    ]
    for dim in missing_dims:
        findings.append(_finding("error", f"comparison dimension missing: {dim}"))
    roster = roster or DEFAULT_ROSTER
    missing_algos = [a for a in roster if a.lower() not in lower]
    for a in missing_algos:
        findings.append(_finding("warning", f"algorithm not mentioned: {a}"))
    if not missing_dims and not missing_algos:
        findings.append(_finding("info", "all dimensions and roster covered"))
    ok = not missing_dims
    return {
        "ok": ok,
        "tool": "comparison",
        "file": str(file_path),
        "findings": findings,
        "summary": _summarize(findings),
        "detail": {
            "missing_dimensions": missing_dims,
            "missing_algorithms": missing_algos,
            "roster_size": len(roster),
        },
    }


def handle_check_comparison(args: argparse.Namespace) -> int:
    roster = None
    if args.roster:
        roster = [x.strip() for x in args.roster.split(",") if x.strip()]

    def _runner(path: Path) -> dict[str, Any]:
        return check_comparison(path, roster=roster)

    return _run_on_target(args, _runner)


# ---------------------------------------------------------------------------
# T4: format
# ---------------------------------------------------------------------------

IEEE_HEURISTIC_RE = re.compile(
    r'^\s*\[\d{1,3}\]\s+.+?,\s*".+?,"\s*.+?,\s*(19|20)\d{2}\.?',
    re.MULTILINE,
)
TEAM_STATEMENT_RE = re.compile(r"^#{1,6}\s*team\s+statement\b", re.IGNORECASE | re.MULTILINE)


def check_format(
    file_path: Path,
    word_limit: int = 3000,
    require_team_statement: bool = True,
) -> dict[str, Any]:
    text = _read(file_path)
    findings: list[dict[str, Any]] = []

    # Word count
    wc = _word_count(text)
    if wc > word_limit:
        findings.append(_finding(
            "error",
            f"word count {wc} exceeds limit {word_limit}",
            word_count=wc,
            limit=word_limit,
        ))
    else:
        findings.append(_finding("info", f"word count {wc} within limit {word_limit}"))

    # Team Statement
    if require_team_statement and not TEAM_STATEMENT_RE.search(text):
        findings.append(_finding("error", "Team Statement heading not found"))

    # Placeholder scan
    for pat in PLACEHOLDER_PATTERNS:
        matches = re.findall(pat, text, re.IGNORECASE)
        if matches:
            findings.append(_finding(
                "error",
                f"placeholder token '{pat}' found ({len(matches)} occurrences)",
                pattern=pat,
                count=len(matches),
            ))

    # Citation cross-refs
    cited = {int(n) for n in CITE_RE.findall(text)}
    refs: dict[int, str] = {}
    for m in REF_LINE_RE.finditer(text):
        refs[int(m.group(1))] = m.group(2).strip()
    cited_without_ref = sorted(cited - refs.keys())
    refs_without_cite = sorted(refs.keys() - cited)
    for n in cited_without_ref:
        findings.append(_finding("error", f"citation [{n}] has no matching reference"))
    for n in refs_without_cite:
        findings.append(_finding("warning", f"reference [{n}] never cited in body"))

    # IEEE heuristic: every reference line should look IEEE-ish
    non_ieee: list[int] = []
    for n, body in refs.items():
        probe = f"[{n}] {body}"
        if not IEEE_HEURISTIC_RE.match(probe):
            non_ieee.append(n)
    for n in non_ieee:
        findings.append(_finding(
            "warning",
            f"reference [{n}] does not match IEEE heuristic (author, \"title,\" venue, year)",
        ))

    summary = _summarize(findings)
    return {
        "ok": summary["errors"] == 0,
        "tool": "format",
        "file": str(file_path),
        "findings": findings,
        "summary": summary,
        "detail": {
            "word_count": wc,
            "word_limit": word_limit,
            "citations_total": len(cited),
            "references_total": len(refs),
            "cited_without_ref": cited_without_ref,
            "refs_without_cite": refs_without_cite,
            "refs_failing_ieee_heuristic": non_ieee,
        },
    }


def handle_check_format(args: argparse.Namespace) -> int:
    def _runner(path: Path) -> dict[str, Any]:
        return check_format(
            path,
            word_limit=args.word_limit,
            require_team_statement=not args.no_team_statement,
        )

    return _run_on_target(args, _runner)


# ---------------------------------------------------------------------------
# T6: citations
# ---------------------------------------------------------------------------

def _load_verified_db(csv_path: Path) -> dict[str, str]:
    """CSV columns: key,status,note.  key is a short lookup token (DOI or keyphrase)."""
    out: dict[str, str] = {}
    with csv_path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            key = (row.get("key") or "").strip().lower()
            status = (row.get("status") or "").strip().lower()
            if key:
                out[key] = status
    return out


def check_citations(file_path: Path, db_path: Path | None) -> dict[str, Any]:
    text = _read(file_path)
    findings: list[dict[str, Any]] = []
    refs: list[tuple[int, str]] = []
    for m in REF_LINE_RE.finditer(text):
        refs.append((int(m.group(1)), m.group(2).strip()))
    if not refs:
        findings.append(_finding("warning", "no references found"))

    db: dict[str, str] = {}
    if db_path and db_path.exists():
        db = _load_verified_db(db_path)
    elif db_path:
        findings.append(_finding("error", f"verified-db not found: {db_path}"))

    per_ref: list[dict[str, Any]] = []
    unverified = 0
    for n, body in refs:
        body_l = body.lower()
        matched_status = None
        matched_key = None
        for key, status in db.items():
            if not key:
                continue
            # Word-boundary match to avoid short-key substring collisions
            # (e.g., CSV key "shi" spuriously matching "rashid").
            if re.search(rf"\b{re.escape(key)}\b", body_l):
                matched_status = status
                matched_key = key
                break
        if matched_status in {"verified", "ok"}:
            per_ref.append({"n": n, "status": "verified", "matched": matched_key})
        elif matched_status in {"pending", "needs_check", "unverified"}:
            per_ref.append({"n": n, "status": matched_status, "matched": matched_key})
            findings.append(_finding("warning", f"reference [{n}] flagged as {matched_status}"))
            unverified += 1
        else:
            per_ref.append({"n": n, "status": "unknown", "matched": None})
            findings.append(_finding(
                "warning",
                f"reference [{n}] not found in verified-db",
            ))
            unverified += 1

    if db and unverified == 0 and refs:
        findings.append(_finding("info", f"all {len(refs)} references verified"))

    summary = _summarize(findings)
    return {
        "ok": summary["errors"] == 0,
        "tool": "citations",
        "file": str(file_path),
        "findings": findings,
        "summary": summary,
        "detail": {
            "total_refs": len(refs),
            "verified_count": sum(1 for r in per_ref if r["status"] == "verified"),
            "per_reference": per_ref,
            "db_entries": len(db),
        },
    }


def handle_check_citations(args: argparse.Namespace) -> int:
    db_path = Path(args.verified_db) if args.verified_db else None

    def _runner(path: Path) -> dict[str, Any]:
        return check_citations(path, db_path)

    return _run_on_target(args, _runner)


# ---------------------------------------------------------------------------
# Shared runner
# ---------------------------------------------------------------------------

def _iter_targets(args: argparse.Namespace) -> list[Path]:
    if args.file:
        p = Path(args.file)
        if not p.exists():
            raise FileNotFoundError(args.file)
        return [p]
    if args.dir:
        d = Path(args.dir)
        if not d.exists():
            raise FileNotFoundError(args.dir)
        return sorted(d.glob("*.md"))
    raise ValueError("either --file or --dir is required")


def _run_on_target(args: argparse.Namespace, runner) -> int:
    as_json = getattr(args, "output", "json") == "json"
    try:
        targets = _iter_targets(args)
    except FileNotFoundError as exc:
        print_error("FILE_NOT_FOUND", str(exc))
        return 1
    except ValueError as exc:
        print_error("BAD_ARGS", str(exc))
        return 1

    if len(targets) == 1:
        payload = runner(targets[0])
        return _emit(payload, as_json)

    # Multiple files: emit an aggregate report.
    reports = [runner(p) for p in targets]
    aggregate = {
        "ok": all(r["ok"] for r in reports),
        "tool": reports[0]["tool"] if reports else "?",
        "files": len(reports),
        "reports": reports,
        "summary": {
            "errors": sum(r["summary"].get("errors", 0) for r in reports),
            "warnings": sum(r["summary"].get("warnings", 0) for r in reports),
            "failed_files": [r["file"] for r in reports if not r["ok"]],
        },
    }
    if as_json:
        print_json(aggregate)
    else:
        for r in reports:
            _print_human(r)
        print(f"\n[aggregate] {aggregate['summary']}")
    return 0 if aggregate["ok"] else 1
