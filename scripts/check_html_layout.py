#!/usr/bin/env python3
"""Static HTML slide layout checker for gen-tgo-ppt V1."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path


SLIDE_CLASSES = {"slide"}
AGENDA_MARKERS = {"目录", "议程", "大纲", "contents", "agenda"}


@dataclass
class Slide:
    index: int
    tag: str
    attrs: dict[str, str]
    text_chunks: list[str] = field(default_factory=list)
    inline_styles: list[str] = field(default_factory=list)

    @property
    def text(self) -> str:
        return " ".join(" ".join(self.text_chunks).split())


class SlideParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.slides: list[Slide] = []
        self.styles: list[str] = []
        self._in_style = False
        self._slide_stack: list[bool] = []
        self._current_slide: Slide | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {name.lower(): value or "" for name, value in attrs}
        classes = set(attr_map.get("class", "").split())
        is_slide = bool(classes & SLIDE_CLASSES) or "data-slide" in attr_map
        self._slide_stack.append(is_slide)
        if tag.lower() == "style":
            self._in_style = True
        if is_slide:
            slide = Slide(index=len(self.slides) + 1, tag=tag, attrs=attr_map)
            if attr_map.get("style"):
                slide.inline_styles.append(attr_map["style"])
            self.slides.append(slide)
            self._current_slide = slide
        elif self._current_slide and attr_map.get("style"):
            self._current_slide.inline_styles.append(attr_map["style"])

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "style":
            self._in_style = False
        if not self._slide_stack:
            return
        was_slide = self._slide_stack.pop()
        if was_slide:
            self._current_slide = None

    def handle_data(self, data: str) -> None:
        if self._in_style:
            self.styles.append(data)
        elif self._current_slide:
            self._current_slide.text_chunks.append(data)


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", "", text).lower()


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


def text_preview(text: str, limit: int = 36) -> str:
    compact = " ".join(text.split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3] + "..."


def level_rank(level: str) -> int:
    return {"PASS": 0, "WARN": 1, "FAIL": 2}[level]


def add_issue(issues: list[dict], level: str, slide: int | None, code: str, message: str) -> None:
    item = {"level": level, "code": code, "message": message}
    if slide is not None:
        item["slide"] = slide
    issues.append(item)


def has_16_9_evidence(slides: list[Slide], css_text: str) -> bool:
    haystacks = [css_text] + [" ".join(slide.inline_styles) for slide in slides]
    for text in haystacks:
        compact = text.replace(" ", "").lower()
        if "aspect-ratio:16/9" in compact or "aspect-ratio:1.777" in compact:
            return True
        width = re.search(r"width\s*:\s*([0-9.]+)(?:px|rem|em|in|vw)?", text, flags=re.I)
        height = re.search(r"height\s*:\s*([0-9.]+)(?:px|rem|em|in|vh|vw)?", text, flags=re.I)
        if width and height:
            w = float(width.group(1))
            h = float(height.group(1))
            if h and math.isclose(w / h, 16 / 9, rel_tol=0.02):
                return True
    return False


def is_agenda_slide(slide: Slide) -> bool:
    normalized = normalize_text(slide.text)
    return any(marker in normalized for marker in AGENDA_MARKERS)


def check_html(path: Path, args: argparse.Namespace) -> dict:
    parser = SlideParser()
    parser.feed(path.read_text(encoding=args.encoding))
    css_text = "\n".join(parser.styles)
    issues: list[dict] = []

    if not parser.slides:
        add_issue(issues, "FAIL", None, "SLIDE_SURFACE_MISSING", "No slide surface found. Use class=\"slide\" or data-slide.")

    if parser.slides and args.require_16_9 and not has_16_9_evidence(parser.slides, css_text):
        add_issue(issues, "FAIL", None, "CANVAS_16_9_MISSING", "HTML slides must declare a fixed 16:9 canvas.")

    if args.require_print_style and "@media" not in css_text.lower():
        add_issue(issues, "WARN", None, "PRINT_STYLE_MISSING", "No @media print style found for slide printing.")

    if not args.skip_mandatory_page_check and parser.slides:
        if len(parser.slides) < 2:
            add_issue(issues, "FAIL", None, "MANDATORY_GUEST_PAGE_MISSING", "Page 2 must be the mandatory guest-introduction page.")
        elif args.guest_page_title not in parser.slides[1].text:
            add_issue(issues, "FAIL", 2, "MANDATORY_GUEST_TITLE_MISSING", f"Page 2 must contain '{args.guest_page_title}'.")
        if not args.allow_custom_closing and args.closing_text not in parser.slides[-1].text:
            add_issue(issues, "FAIL", parser.slides[-1].index, "MANDATORY_CLOSING_MISSING", f"Final slide must contain '{args.closing_text}'.")

    agenda_indices = [slide.index for slide in parser.slides if is_agenda_slide(slide)]
    if agenda_indices and agenda_indices[0] != args.agenda_page_index:
        add_issue(issues, "FAIL", agenda_indices[0], "AGENDA_PAGE_ORDER", f"First agenda page is slide {agenda_indices[0]}; expected slide {args.agenda_page_index}.")

    for slide in parser.slides:
        text = slide.text
        weighted = weighted_text_len(text)
        if weighted > args.max_slide_weighted:
            add_issue(issues, "FAIL", slide.index, "TEXT_DENSITY_HIGH", f"Slide text density is {round(weighted, 1)}, above {args.max_slide_weighted}.")
        for run in re.split(r"[\n。；;.!?！？]", text):
            run_weighted = weighted_text_len(run)
            if run_weighted > args.max_text_run_weighted:
                add_issue(
                    issues,
                    "WARN",
                    slide.index,
                    "TEXT_RUN_MAY_WRAP",
                    f"Long text run may wrap unexpectedly: {text_preview(run)}",
                )
        if "MANDATORY PAGE" in text:
            add_issue(issues, "FAIL", slide.index, "AI_PLACEHOLDER_TEXT", "Slide contains AI-facing placeholder text.")

    status = "PASS"
    if issues:
        status = max((issue["level"] for issue in issues), key=level_rank)

    return {
        "file": str(path),
        "status": status,
        "slide_count": len(parser.slides),
        "slide_statuses": [
            {
                "slide": slide.index,
                "status": max(
                    [issue["level"] for issue in issues if issue.get("slide") == slide.index],
                    key=level_rank,
                    default="PASS",
                ),
            }
            for slide in parser.slides
        ],
        "issues": issues,
    }


def print_text_report(result: dict) -> None:
    print(f"{result['file']}: {result['status']} ({result['slide_count']} slides)")
    for issue in result["issues"]:
        location = f" slide {issue['slide']}" if "slide" in issue else ""
        print(f"- {issue['level']}{location} {issue['code']}: {issue['message']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Check generated HTML slide decks for layout safety issues.")
    parser.add_argument("html", nargs="+", type=Path)
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    parser.add_argument("--allow-fail", action="store_true", help="Always exit 0, even when FAIL issues are found.")
    parser.add_argument("--encoding", default="utf-8")
    parser.add_argument("--require-16-9", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--require-print-style", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--skip-mandatory-page-check", action="store_true")
    parser.add_argument("--allow-custom-closing", action="store_true")
    parser.add_argument("--guest-page-title", default="嘉宾介绍")
    parser.add_argument("--closing-text", default="感谢聆听")
    parser.add_argument("--agenda-page-index", type=int, default=3)
    parser.add_argument("--max-slide-weighted", type=float, default=1000.0)
    parser.add_argument("--max-text-run-weighted", type=float, default=220.0)
    args = parser.parse_args()

    results = [check_html(path, args) for path in args.html]
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for result in results:
            print_text_report(result)

    has_fail = any(result["status"] == "FAIL" for result in results)
    if has_fail and not args.allow_fail:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
