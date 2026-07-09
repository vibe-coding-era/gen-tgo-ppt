#!/usr/bin/env python3
"""Compress check_pptx_layout.py JSON output into a short report."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path


def slide_sort_value(value) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 10**9


def load_json(path: str | None):
    if not path or path == "-":
        return json.load(sys.stdin)
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def normalize_results(data) -> list[dict]:
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        return [data]
    raise SystemExit("Expected a JSON object or list from check_pptx_layout.py --json")


def summarize(results: list[dict], max_issues: int) -> dict:
    status_counts = Counter()
    issue_level_counts = Counter()
    issue_code_counts = Counter()
    slide_issue_counts: dict[str, Counter] = defaultdict(Counter)
    decks = []

    for result in results:
        status = result.get("status", "UNKNOWN")
        status_counts[status] += 1
        issues = result.get("issues", [])
        for issue in issues:
            level = issue.get("level", "UNKNOWN")
            code = issue.get("code", "UNKNOWN")
            slide = str(issue.get("slide", "?"))
            issue_level_counts[level] += 1
            issue_code_counts[code] += 1
            slide_issue_counts[slide][level] += 1

        top_issues = sorted(
            issues,
            key=lambda issue: (
                {"FAIL": 0, "WARN": 1}.get(issue.get("level"), 2),
                slide_sort_value(issue.get("slide")),
                issue.get("code", ""),
            ),
        )[:max_issues]
        decks.append(
            {
                "file": result.get("file"),
                "status": status,
                "slide_count": result.get("slide_count"),
                "layout_scale": result.get("layout_scale"),
                "issue_counts": dict(Counter(issue.get("level", "UNKNOWN") for issue in issues)),
                "top_issues": [
                    {
                        "level": issue.get("level"),
                        "slide": issue.get("slide"),
                        "code": issue.get("code"),
                        "message": issue.get("message"),
                    }
                    for issue in top_issues
                ],
            }
        )

    return {
        "deck_count": len(results),
        "status_counts": dict(status_counts),
        "issue_level_counts": dict(issue_level_counts),
        "issue_code_counts": dict(issue_code_counts.most_common()),
        "slides_with_issues": {
            slide: dict(counts)
            for slide, counts in sorted(slide_issue_counts.items(), key=lambda item: slide_sort_value(item[0]))
        },
        "decks": decks,
    }


def render_markdown(summary: dict) -> str:
    lines = ["# PPTX Layout Report Summary", ""]
    lines.append(
        f"- deck_count: {summary['deck_count']}"
    )
    lines.append(f"- status_counts: {summary['status_counts']}")
    lines.append(f"- issue_level_counts: {summary['issue_level_counts']}")
    lines.append("")
    lines.append("## Issue Codes")
    lines.append("")
    lines.append("| code | count |")
    lines.append("| --- | ---: |")
    for code, count in summary["issue_code_counts"].items():
        lines.append(f"| {code} | {count} |")
    lines.append("")
    lines.append("## Decks")
    lines.append("")
    for deck in summary["decks"]:
        lines.append(f"### {deck['file']}")
        lines.append("")
        lines.append(f"- status: {deck['status']}")
        lines.append(f"- slide_count: {deck['slide_count']}")
        lines.append(f"- issue_counts: {deck['issue_counts']}")
        if deck["top_issues"]:
            lines.append("")
            lines.append("| level | slide | code | message |")
            lines.append("| --- | ---: | --- | --- |")
            for issue in deck["top_issues"]:
                message = str(issue.get("message") or "").replace("|", "\\|")
                code = str(issue.get("code") or "").replace("|", "\\|")
                lines.append(f"| {issue.get('level')} | {issue.get('slide')} | {code} | {message} |")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize check_pptx_layout.py --json output.")
    parser.add_argument("json_report", nargs="?", default="-", help="JSON report path, or stdin when omitted/-")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--max-issues", type=int, default=12, help="Maximum issues to keep per deck.")
    parser.add_argument("--output", type=Path, help="Write output to this path instead of stdout.")
    args = parser.parse_args()

    if args.max_issues < 1:
        raise SystemExit("--max-issues must be >= 1")

    summary = summarize(normalize_results(load_json(args.json_report)), args.max_issues)
    if args.format == "json":
        text = json.dumps(summary, ensure_ascii=False, indent=2)
    else:
        text = render_markdown(summary)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + ("" if text.endswith("\n") else "\n"), encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()
