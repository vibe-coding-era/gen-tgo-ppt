#!/usr/bin/env python3
"""Create or preview a mode-aware gen-tgo-ppt V1.1 generation log."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

SKILL_VERSION = "V1.1"
LAYOUT_SAFETY_VERSION = "V1"
LOG_MODES = ("create", "convert", "repair", "check_only")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create or preview a gen-tgo-ppt V1.1 generation log.")
    parser.add_argument("--mode", choices=LOG_MODES, default="create", help="Task mode; handoff has no generation log.")
    parser.add_argument("--title", default="TGO演示稿生成", help="Task or deck title.")
    parser.add_argument("--source", default="待补充", help="Source file or content description.")
    parser.add_argument("--scenario", default="待确认", help="GTLC or daily sharing.")
    parser.add_argument("--spec", default="16:9", help="Slide ratio/spec, such as 16:9.")
    parser.add_argument("--format", default="待确认", help="PPT, HTML, or both.")
    parser.add_argument("--style", default="待确认", help="Selected visual style numbers.")
    parser.add_argument("--template", default="待确认", help="Template choice.")
    parser.add_argument("--design-file", default="Design.md", help="Design intake file path.")
    parser.add_argument("--content-file", default="Content.md", help="Content draft file path.")
    parser.add_argument(
        "--processing-mode",
        default="待确认",
        help="For PPT/PDF sources: modify content and apply template, or template-only.",
    )
    parser.add_argument("--logo", default="默认GTLC LOGO", help="Logo replacement decision or uploaded logo path.")
    parser.add_argument("--dry-run", action="store_true", help="Print the complete log without writing a file.")
    return parser


def render_log(args: argparse.Namespace, now: datetime, cwd: Path) -> str:
    return f"""# gen-tgo-ppt 生成日志

- Skill 版本：{SKILL_VERSION}
- 排版安全版本：{LAYOUT_SAFETY_VERSION}
- 任务模式：{args.mode}
- 创建时间：{now.isoformat(timespec="seconds")}
- 当前目录：`{cwd}`
- 任务标题：{args.title}
- Design.md：{args.design_file}
- Content.md：{args.content_file}
- 来源：{args.source}
- 场景：{args.scenario}
- 规格：{args.spec}
- 输出格式：{args.format}
- 处理模式：{args.processing_mode}
- Logo替换：{args.logo}
- 风格选择：{args.style}
- 模板选择：{args.template}

## 澄清与内容边界

- 待记录：用户明确要求、内容是否允许改写、覆盖决定与不可逆边界。
- 待记录：`check_only` 保持源文件只读；`repair` 记录来源与回滚点。

## 页数、大纲与文本预算

- 待记录：逐页标题、目的、布局、核心内容、资产、预计行数、密度风险与拆页策略。
- 待记录：适用时确认标题页、`嘉宾介绍`、目录、正文与 `感谢聆听` 的顺序。

## 样片与用户决定

- 待记录：样片路径、预览方式、用户反馈；若跳过，记录用户决定和原因。

## 完整输出

- 待记录：PPTX/HTML 路径、来源保留情况、覆盖确认与回滚点。

## PPTX/HTML 检查与逐页复核

- 待记录：检查命令、PASS/WARN/FAIL、异常页、修复动作、复查和渲染证据。

## 失败、重试与降级

- 待记录：稳定错误码、失败分类、改变的条件、重试次数、降级范围与影响。

## 通道分工与交接

- `生成内容`：待记录 / not_applicable。
- `检查风格`：待记录 / not_applicable。
- `检查文字`：待记录 / not_applicable。
- 执行方式：单 Agent 分离自检 / 独立通道；不得误标独立验证。

## SSOT（若适用）

- 待记录：SSOT 路径、冲突与裁决、唯一执行计划；不适用时写明理由。

## 操作记录

- {now.isoformat(timespec="seconds")} 创建生成日志。

## 遗留问题

- 待核对：完成前补齐产物、检查、证据、例外与遗留问题；未填写不得视为“无”。
"""


def main() -> None:
    args = build_parser().parse_args()
    now = datetime.now().astimezone()
    cwd = Path.cwd()
    content = render_log(args, now, cwd)
    if args.dry_run:
        print(content, end="")
        return

    path = cwd / f"gen-tgo-ppt-生成日志-{now.strftime('%Y%m%d-%H%M%S')}.md"
    if path.exists():
        raise SystemExit(f"E_OUTPUT_EXISTS: refusing to overwrite existing log: {path}; action=choose a new timestamp")
    try:
        path.write_text(content, encoding="utf-8")
    except OSError as exc:
        raise SystemExit(f"E_WORKDIR_READONLY: cannot write generation log in {cwd}: {exc}; action=provide a writable directory") from None
    print(path)


if __name__ == "__main__":
    main()
