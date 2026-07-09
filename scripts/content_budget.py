#!/usr/bin/env python3
"""Estimate slide text density from Markdown or plain text."""

from __future__ import annotations

import argparse
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
SLIDE_SPLIT_RE = re.compile(r"^\s*(?:---+|<!--\s*slide\s*-->)\s*$", re.IGNORECASE)


def weighted_text_len(text: str) -> float:
    total = 0.0
    for char in text:
        if char.isspace():
            total += 0.35
        elif ord(char) > 127:
            total += 1.0
        else:
            total += 0.55
    return total


def compact_preview(text: str, limit: int = 80) -> str:
    compact = " ".join(text.split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3] + "..."


def markdown_cell(text: object) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ")


@dataclass
class Section:
    title: str
    level: int
    start_line: int
    lines: list[str]

    @property
    def text(self) -> str:
        return "\n".join(self.lines).strip()


def append_if_not_empty(sections: list[Section], section: Section) -> None:
    if section.text:
        sections.append(section)


def split_sections(text: str) -> list[Section]:
    sections: list[Section] = []
    current = Section(title="Document", level=0, start_line=1, lines=[])
    for index, line in enumerate(text.splitlines(), start=1):
        heading = HEADING_RE.match(line)
        if heading:
            append_if_not_empty(sections, current)
            current = Section(title=heading.group(2).strip(), level=len(heading.group(1)), start_line=index, lines=[])
            continue
        if SLIDE_SPLIT_RE.match(line):
            append_if_not_empty(sections, current)
            current = Section(title=f"Slide marker after line {index}", level=0, start_line=index + 1, lines=[])
            continue
        current.lines.append(line)
    append_if_not_empty(sections, current)
    if not sections:
        sections.append(Section(title="Document", level=0, start_line=1, lines=[]))
    return sections


def estimate_lines(weighted: float, units_per_line: float) -> int:
    if weighted <= 0:
        return 0
    return max(1, math.ceil(weighted / units_per_line))


def risk_level(weighted: float, estimated_lines_count: int, max_weighted: float, max_lines: int) -> str:
    if weighted > max_weighted * 1.35 or estimated_lines_count > max_lines + 3:
        return "high"
    if weighted > max_weighted or estimated_lines_count > max_lines:
        return "medium"
    return "low"


def summarize_section(section: Section, units_per_line: float, max_weighted: float, max_lines: int) -> dict:
    text = section.text
    weighted = round(weighted_text_len(text), 1)
    lines = estimate_lines(weighted, units_per_line)
    non_empty_lines = [line for line in section.lines if line.strip()]
    bullets = sum(1 for line in non_empty_lines if line.lstrip().startswith(("-", "*", "+")))
    return {
        "title": section.title,
        "level": section.level,
        "start_line": section.start_line,
        "raw_chars": len(text),
        "weighted_chars": weighted,
        "estimated_lines": lines,
        "non_empty_lines": len(non_empty_lines),
        "bullet_lines": bullets,
        "risk": risk_level(weighted, lines, max_weighted, max_lines),
        "preview": compact_preview(text),
    }


def summarize_file(path: Path, args: argparse.Namespace) -> dict:
    text = path.read_text(encoding=args.encoding)
    sections = [
        summarize_section(section, args.units_per_line, args.max_weighted, args.max_lines)
        for section in split_sections(text)
    ]
    risk_counts: dict[str, int] = {"low": 0, "medium": 0, "high": 0}
    for section in sections:
        risk_counts[section["risk"]] += 1
    return {
        "file": str(path),
        "section_count": len(sections),
        "risk_counts": risk_counts,
        "sections": sections,
    }


def render_markdown(results: list[dict]) -> str:
    lines = ["# Content Budget Summary", ""]
    for result in results:
        lines.append(f"## {result['file']}")
        lines.append("")
        lines.append(
            "| section | risk | weighted_chars | estimated_lines | start_line | preview |"
        )
        lines.append("| --- | --- | ---: | ---: | ---: | --- |")
        for section in result["sections"]:
            lines.append(
                f"| {markdown_cell(section['title'])} | {section['risk']} | {section['weighted_chars']} | "
                f"{section['estimated_lines']} | {section['start_line']} | {markdown_cell(section['preview'])} |"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Estimate slide text density from Markdown or plain text.")
    parser.add_argument("file", nargs="+", type=Path, help="Markdown or text files to inspect.")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--encoding", default="utf-8")
    parser.add_argument("--units-per-line", type=float, default=34.0, help="Weighted characters per display line.")
    parser.add_argument("--max-weighted", type=float, default=220.0, help="Medium risk threshold per section.")
    parser.add_argument("--max-lines", type=int, default=9, help="Medium risk threshold for estimated lines.")
    parser.add_argument("--output", type=Path, help="Write output to this path instead of stdout.")
    args = parser.parse_args()

    results = []
    for path in args.file:
        if not path.exists() or not path.is_file():
            raise SystemExit(f"Input file not found: {path}")
        results.append(summarize_file(path, args))

    if args.format == "json":
        text = json.dumps(results, ensure_ascii=False, indent=2)
    else:
        text = render_markdown(results)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + ("" if text.endswith("\n") else "\n"), encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()
