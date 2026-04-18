---
description: Audit Q6 (Assessment) sections of algorithm synopses for critical depth. Accepts a file path or a directory.
argument-hint: <file-or-directory-path>
---

# Audit Q6 sections for critical depth

Target: `$ARGUMENTS`

## What to do

1. **Resolve the target.**
   - If `$ARGUMENTS` is a single `.md` file → audit that one file.
   - If it is a directory → enumerate `*.md` files (exclude `README*.md` and `*comparison*.md`, which are not synopses).
   - If empty → default to `docs/survey_drafts/` and `docs/` submission files (pso/woa_synopsis_submission.md).

2. **Ensure the audit output directory exists:** `docs/audits/`. Create it if missing.

3. **Run audits in parallel.** For each target file, invoke the `q6-auditor` subagent via the Agent tool. Batch all invocations in a single message for parallelism. Each call must:
   - Use `subagent_type: "q6-auditor"`
   - Pass the file path as the prompt
   - Instruct the subagent to write its JSON verdict to `docs/audits/<basename>.q6audit.json`

4. **After all subagents return**, read the per-file JSON reports and produce a single aggregated markdown report at `docs/audits/q6_audit_summary.md` with:
   - A table: `file | overall_grade | critical_citation | balanced_judgment | part2_relevance`
   - A "Files needing revision" section listing anything graded P or N, with their `improvement_suggestions`
   - A one-line overall pass/fail verdict (pass = no N grades and ≤1 P grade)

5. **Report back to the user** with:
   - The path to the summary report
   - Count of HD / D / C / P / N
   - Top 3 files to revise (if any)

## Constraints

- Do not modify synopsis files — audit is read-only.
- Do not spawn web searches; the subagent is restricted to file reads.
- If a subagent returns `ok: false` (Q6 not found), flag the file in the summary but continue.
