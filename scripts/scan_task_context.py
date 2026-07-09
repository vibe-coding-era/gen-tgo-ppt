#!/usr/bin/env python3
"""Summarize a TGO/GTLC deck workspace into a compact JSON context."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


EXCLUDED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".DS_Store",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
    "node_modules",
}

SOURCE_EXTS = {".pptx", ".pdf", ".md", ".html", ".htm", ".txt"}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}
OUTPUT_EXTS = {".pptx", ".pdf", ".html", ".htm", ".webp", ".png", ".jpg", ".jpeg"}
LOG_PATTERNS = ("gen-tgo-ppt-", "generation-log")
CHINESE_GENERATION_LOG = "\u751f\u6210\u65e5\u5fd7"
SOURCE_EXCLUDED_NAMES = {"Design.md", "Content.md", "README.md"}
LOGO_REJECT_TOKENS = (
    "contact-sheet",
    "contactsheet",
    "preview",
    "slide-",
    "page-",
    "render",
    "screenshot",
    "overview",
    "总览",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def file_info(path: Path, root: Path) -> dict:
    stat = path.stat()
    return {
        "path": rel(path, root),
        "name": path.name,
        "ext": path.suffix.lower(),
        "size_bytes": stat.st_size,
        "modified": datetime.fromtimestamp(stat.st_mtime, timezone.utc).replace(microsecond=0).isoformat(),
    }


def iter_files(root: Path, max_files: int):
    count = 0
    for path in root.rglob("*"):
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        if not path.is_file():
            continue
        count += 1
        if count > max_files:
            yield None
            return
        yield path


def looks_like_logo(path: Path) -> bool:
    lower = path.name.lower()
    if any(token in lower for token in LOGO_REJECT_TOKENS):
        return False
    stem = path.stem.lower()
    return "logo" in lower or "brand" in lower or stem in {"gtlc", "tgo"}


def is_generation_log_name(name: str) -> bool:
    lower_name = name.lower()
    return lower_name.startswith(LOG_PATTERNS) or CHINESE_GENERATION_LOG in name


def is_ssot_name(name: str) -> bool:
    return "ssot" in name.lower()


def is_source_candidate(path: Path) -> bool:
    name = path.name
    if name in SOURCE_EXCLUDED_NAMES:
        return False
    if is_generation_log_name(name) or is_ssot_name(name):
        return False
    return path.suffix.lower() in SOURCE_EXTS


def classify_file(path: Path, root: Path) -> list[str]:
    name = path.name
    lower_name = name.lower()
    ext = path.suffix.lower()
    categories: list[str] = []

    if name == "Design.md":
        categories.append("design_file")
    if name == "Content.md":
        categories.append("content_file")
    if is_source_candidate(path):
        categories.append("source_candidate")
    if ext in IMAGE_EXTS:
        categories.append("image")
    if ext in IMAGE_EXTS and looks_like_logo(path):
        categories.append("logo_candidate")
    if ext in OUTPUT_EXTS and ("output" in path.parts or "outputs" in path.parts or "preview" in lower_name):
        categories.append("output_candidate")
    if ext == ".ndjson" and "inspect" in lower_name:
        categories.append("inspect_report")
    if ext == ".json" and ("layout" in lower_name or "manifest" in lower_name):
        categories.append("machine_report")
    if lower_name.endswith(".pptx.inspect.ndjson"):
        categories.append("pptx_inspect_report")
    if is_generation_log_name(name):
        categories.append("generation_log")
    if is_ssot_name(name):
        categories.append("ssot")

    return categories


def top_recent(files: list[dict], limit: int) -> list[dict]:
    return sorted(files, key=lambda item: item["modified"], reverse=True)[:limit]


def rule_hints(categories: dict[str, list[dict]]) -> list[str]:
    hints: set[str] = set()
    if not categories.get("design_file") or not categories.get("content_file"):
        hints.add("references/rule-intake.md")
    if categories.get("source_candidate"):
        hints.add("references/conversion-workflows.md")
    if categories.get("design_file"):
        hints.add("references/design/index.md")
        hints.add("references/design/shared/design.md")
    if categories.get("logo_candidate"):
        hints.add("references/rule-ppt-structure.md")
    if categories.get("output_candidate"):
        hints.add("references/rule-layout-safety-v1.md")
        hints.add("references/rule-validation.md")
    if categories.get("generation_log"):
        hints.add("references/generation-log.md")
    return sorted(hints)


def build_summary(root: Path, max_files: int, recent_limit: int) -> dict:
    categories: dict[str, list[dict]] = defaultdict(list)
    ext_counts: dict[str, int] = defaultdict(int)
    scanned = 0
    truncated = False

    for path in iter_files(root, max_files=max_files):
        if path is None:
            truncated = True
            break
        scanned += 1
        ext_counts[path.suffix.lower() or "<none>"] += 1
        info = file_info(path, root)
        for category in classify_file(path, root):
            categories[category].append(info)

    compact_categories = {
        name: {
            "count": len(items),
            "recent": top_recent(items, recent_limit),
        }
        for name, items in sorted(categories.items())
    }

    return {
        "root": root.as_posix(),
        "generated_at": utc_now(),
        "scanned_files": scanned,
        "scan_limit": max_files,
        "truncated": truncated,
        "extension_counts": dict(sorted(ext_counts.items())),
        "categories": compact_categories,
        "rule_hints": rule_hints(categories),
        "status_flags": {
            "has_design_md": bool(categories.get("design_file")),
            "has_content_md": bool(categories.get("content_file")),
            "has_generation_log": bool(categories.get("generation_log")),
            "has_pptx_output_candidate": any(item["ext"] == ".pptx" for item in categories.get("output_candidate", [])),
            "has_machine_reports": bool(categories.get("machine_report") or categories.get("inspect_report")),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize a deck workspace into compact JSON.")
    parser.add_argument("root", nargs="?", default=".", type=Path, help="Workspace root to scan.")
    parser.add_argument("--max-files", type=int, default=5000, help="Maximum files to scan before truncating.")
    parser.add_argument("--recent-limit", type=int, default=8, help="Recent file records to keep per category.")
    parser.add_argument("--output", type=Path, help="Write JSON to this path instead of stdout.")
    args = parser.parse_args()

    root = args.root.resolve()
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Root is not a directory: {root}")
    if args.max_files < 1:
        raise SystemExit("--max-files must be >= 1")
    if args.recent_limit < 1:
        raise SystemExit("--recent-limit must be >= 1")

    summary = build_summary(root, args.max_files, args.recent_limit)
    text = json.dumps(summary, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


if __name__ == "__main__":
    main()
