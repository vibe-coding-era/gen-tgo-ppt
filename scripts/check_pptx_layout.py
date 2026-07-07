#!/usr/bin/env python3
"""Static PPTX layout checker for gen-tgo-ppt v0.6."""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

EMU_PER_IN = 914400
EMU_PER_PT = 12700


@dataclass(frozen=True)
class Rect:
    left: int
    top: int
    width: int
    height: int

    @property
    def right(self) -> int:
        return self.left + self.width

    @property
    def bottom(self) -> int:
        return self.top + self.height

    @property
    def area(self) -> int:
        return max(0, self.width) * max(0, self.height)


def inch_to_emu(value: float) -> int:
    return int(value * EMU_PER_IN)


def emu_to_in(value: int) -> float:
    return round(value / EMU_PER_IN, 3)


def emu_to_pt(value: int) -> float:
    return value / EMU_PER_PT


def shape_rect(shape) -> Rect:
    return Rect(
        int(getattr(shape, "left", 0) or 0),
        int(getattr(shape, "top", 0) or 0),
        int(getattr(shape, "width", 0) or 0),
        int(getattr(shape, "height", 0) or 0),
    )


def intersects(a: Rect, b: Rect) -> bool:
    return a.left < b.right and a.right > b.left and a.top < b.bottom and a.bottom > b.top


def intersection_area(a: Rect, b: Rect) -> int:
    if not intersects(a, b):
        return 0
    width = min(a.right, b.right) - max(a.left, b.left)
    height = min(a.bottom, b.bottom) - max(a.top, b.top)
    return max(0, width) * max(0, height)


def walk_shapes(shapes):
    for shape in shapes:
        yield shape
        try:
            if shape.shape_type == MSO_SHAPE_TYPE.GROUP:
                yield from walk_shapes(shape.shapes)
        except Exception:
            pass


def shape_text(shape) -> str:
    try:
        if not getattr(shape, "has_text_frame", False) or not shape.has_text_frame:
            return ""
        return "\n".join(paragraph.text for paragraph in shape.text_frame.paragraphs).strip()
    except Exception:
        return ""


def text_preview(text: str, limit: int = 28) -> str:
    compact = " ".join(text.split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 1] + "..."


def shape_label(shape, text: str) -> str:
    name = (getattr(shape, "name", "") or "unnamed").strip()
    preview = text_preview(text)
    if preview:
        return f"{name!r} text={preview!r}"
    return repr(name)


def font_sizes(shape, default_size: float) -> list[float]:
    sizes: list[float] = []
    try:
        for paragraph in shape.text_frame.paragraphs:
            for run in paragraph.runs:
                if run.font.size is not None:
                    sizes.append(float(run.font.size.pt))
    except Exception:
        pass
    return sizes or [default_size]


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


def estimate_lines(text: str, width_emu: int, font_size_pt: float) -> int:
    available_width_pt = max(1.0, emu_to_pt(width_emu) - 16.0)
    units_per_line = max(1.0, available_width_pt / max(font_size_pt * 0.88, 1.0))
    lines = 0
    for paragraph in text.splitlines() or [text]:
        weighted = weighted_text_len(paragraph)
        if weighted <= 0:
            lines += 1
        else:
            lines += max(1, math.ceil(weighted / units_per_line))
    return lines


def level_rank(level: str) -> int:
    return {"PASS": 0, "WARN": 1, "FAIL": 2}[level]


def add_issue(issues: list[dict], level: str, slide: int, code: str, message: str) -> None:
    issues.append({"level": level, "slide": slide, "code": code, "message": message})


def check_pptx(path: Path, args: argparse.Namespace) -> dict:
    prs = Presentation(path)
    slide_w = int(prs.slide_width)
    slide_h = int(prs.slide_height)
    page = Rect(0, 0, slide_w, slide_h)
    margin = inch_to_emu(args.margin_in)
    footer = Rect(0, slide_h - inch_to_emu(args.footer_in), slide_w, inch_to_emu(args.footer_in))
    logo = Rect(
        slide_w - inch_to_emu(args.logo_width_in) - margin,
        margin,
        inch_to_emu(args.logo_width_in),
        inch_to_emu(args.logo_height_in),
    )
    issues: list[dict] = []
    slide_statuses = []

    for slide_index, slide in enumerate(prs.slides, start=1):
        text_shapes = []
        slide_issues_start = len(issues)
        for shape in walk_shapes(slide.shapes):
            text = shape_text(shape)
            if not text:
                continue

            rect = shape_rect(shape)
            label = shape_label(shape, text)
            text_shapes.append((shape, text, rect))

            if (
                rect.left < -args.bounds_tolerance_emu
                or rect.top < -args.bounds_tolerance_emu
                or rect.right > page.right + args.bounds_tolerance_emu
                or rect.bottom > page.bottom + args.bounds_tolerance_emu
            ):
                add_issue(
                    issues,
                    "FAIL",
                    slide_index,
                    "TEXT_OUT_OF_SLIDE",
                    f"{label} extends outside slide bounds at "
                    f"x={emu_to_in(rect.left)}, y={emu_to_in(rect.top)}, "
                    f"w={emu_to_in(rect.width)}, h={emu_to_in(rect.height)}.",
                )

            if intersects(rect, footer):
                level = "FAIL" if args.fail_on_keepout else "WARN"
                add_issue(issues, level, slide_index, "FOOTER_KEEP_OUT", f"{label} intersects footer keep-out area.")

            if intersects(rect, logo):
                level = "FAIL" if args.fail_on_keepout else "WARN"
                add_issue(issues, level, slide_index, "LOGO_KEEP_OUT", f"{label} intersects top-right logo keep-out area.")

            sizes = font_sizes(shape, args.default_font_pt)
            min_size = min(sizes)
            max_size = max(sizes)
            if min_size < args.hard_min_font_pt:
                add_issue(issues, "FAIL", slide_index, "FONT_TOO_SMALL", f"{label} uses {min_size:.1f}pt text.")
            elif min_size < args.warn_min_font_pt:
                add_issue(issues, "WARN", slide_index, "FONT_SMALL", f"{label} uses {min_size:.1f}pt text.")

            estimated_lines = estimate_lines(text, rect.width, max_size)
            required_height_pt = estimated_lines * max_size * args.line_height
            available_height_pt = max(1.0, emu_to_pt(rect.height) - 10.0)
            if required_height_pt > available_height_pt * args.overflow_tolerance:
                add_issue(
                    issues,
                    "FAIL",
                    slide_index,
                    "TEXT_MAY_OVERFLOW",
                    f"{label} likely needs {required_height_pt:.1f}pt height "
                    f"for about {estimated_lines} lines, available {available_height_pt:.1f}pt.",
                )

            if max_size >= args.large_title_pt and estimated_lines > args.max_large_title_lines:
                add_issue(
                    issues,
                    "WARN",
                    slide_index,
                    "LARGE_TITLE_WRAP",
                    f"{label} has large text ({max_size:.1f}pt) estimated at {estimated_lines} lines.",
                )

        for i, (_, _, rect_a) in enumerate(text_shapes):
            for shape_b, _, rect_b in text_shapes[i + 1 :]:
                area = intersection_area(rect_a, rect_b)
                if not area:
                    continue
                overlap_ratio = area / max(1, min(rect_a.area, rect_b.area))
                if overlap_ratio >= args.overlap_ratio:
                    label_b = shape_label(shape_b, shape_text(shape_b))
                    add_issue(
                        issues,
                        "FAIL",
                        slide_index,
                        "TEXT_OVERLAP",
                        f"Text shapes overlap by {overlap_ratio:.0%}; later shape is {label_b}.",
                    )

        slide_issues = issues[slide_issues_start:]
        status = "PASS"
        if any(issue["level"] == "FAIL" for issue in slide_issues):
            status = "FAIL"
        elif slide_issues:
            status = "WARN"
        slide_statuses.append({"slide": slide_index, "status": status})

    deck_status = "PASS"
    if any(issue["level"] == "FAIL" for issue in issues):
        deck_status = "FAIL"
    elif issues:
        deck_status = "WARN"

    return {
        "file": str(path),
        "status": deck_status,
        "slide_count": len(prs.slides),
        "canvas_in": {"width": emu_to_in(slide_w), "height": emu_to_in(slide_h)},
        "slide_statuses": slide_statuses,
        "issues": issues,
    }


def print_text_report(result: dict) -> None:
    print(f"{result['status']} {result['file']} ({result['slide_count']} slides)")
    for item in result["slide_statuses"]:
        print(f"- slide {item['slide']}: {item['status']}")
    for issue in result["issues"]:
        print(f"[{issue['level']}] slide {issue['slide']} {issue['code']}: {issue['message']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Check generated PPTX files for layout safety issues.")
    parser.add_argument("pptx", nargs="+", type=Path)
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    parser.add_argument("--allow-fail", action="store_true", help="Always exit 0, even when FAIL issues are found.")
    parser.add_argument("--fail-on-keepout", action="store_true", help="Treat logo/footer keep-out intersections as FAIL.")
    parser.add_argument("--margin-in", type=float, default=0.45)
    parser.add_argument("--footer-in", type=float, default=0.75)
    parser.add_argument("--logo-width-in", type=float, default=3.2)
    parser.add_argument("--logo-height-in", type=float, default=1.0)
    parser.add_argument("--default-font-pt", type=float, default=20.0)
    parser.add_argument("--warn-min-font-pt", type=float, default=14.0)
    parser.add_argument("--hard-min-font-pt", type=float, default=12.0)
    parser.add_argument("--large-title-pt", type=float, default=38.0)
    parser.add_argument("--max-large-title-lines", type=int, default=2)
    parser.add_argument("--line-height", type=float, default=1.2)
    parser.add_argument("--overflow-tolerance", type=float, default=1.08)
    parser.add_argument("--overlap-ratio", type=float, default=0.08)
    parser.add_argument("--bounds-tolerance-emu", type=int, default=1000)
    args = parser.parse_args()

    results = [check_pptx(path, args) for path in args.pptx]
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for index, result in enumerate(results):
            if index:
                print()
            print_text_report(result)

    has_fail = any(result["status"] == "FAIL" for result in results)
    if has_fail and not args.allow_fail:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
