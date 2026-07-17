#!/usr/bin/env python3
"""Create or preview a mode-aware gen-tgo-ppt V1.2 generation log."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

SKILL_VERSION = "V1.2"
LAYOUT_SAFETY_VERSION = "V1"
TEMPLATE_BUNDLE_VERSION = "V1.1"
LOG_MODES = ("create", "convert", "repair", "check_only")
SOURCE_AUTHORITIES = (
    "unconfirmed",
    "current_turn",
    "explicit_path",
    "confirmed_workspace",
    "confirmed_continuation",
    "not_applicable",
)
SOURCE_REQUIRED_MODES = {"create", "convert", "repair"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create or preview a gen-tgo-ppt V1.2 generation log.")
    parser.add_argument("--mode", choices=LOG_MODES, default="create", help="Task mode; handoff has no generation log.")
    parser.add_argument("--title", default="TGO演示稿生成", help="Task or deck title.")
    parser.add_argument("--source", default="待补充", help="Source file or content description.")
    parser.add_argument(
        "--source-authority",
        choices=SOURCE_AUTHORITIES,
        default="unconfirmed",
        help=(
            "How the source became active for this task. create/convert/repair require "
            "current_turn, explicit_path, confirmed_workspace, or confirmed_continuation."
        ),
    )
    parser.add_argument("--scenario", default="待确认", help="GTLC or daily sharing.")
    parser.add_argument("--spec", default="16:9", help="Slide ratio/spec, such as 16:9.")
    parser.add_argument("--format", default="待确认", help="PPT, HTML, or both.")
    parser.add_argument("--style", default="待确认", help="Selected visual style numbers.")
    parser.add_argument("--template", default="待确认", help="Template choice.")
    parser.add_argument(
        "--clarification-status",
        default="待确认",
        help="Whether missing create inputs were clarified with the user.",
    )
    parser.add_argument(
        "--brief-confirmation",
        default="待确认",
        help="User decision on the parsed content brief.",
    )
    parser.add_argument(
        "--style-confirmation",
        default="待确认",
        help="User decision on the displayed template and visual style selection.",
    )
    parser.add_argument(
        "--sample-confirmation",
        default="待确认",
        help="User decision on the representative sample slide, or an explicit skip decision.",
    )
    parser.add_argument(
        "--asset-source-strategy",
        default="待确认",
        help="Allowed asset sources, such as user assets, confirmed local licensed assets, or approved AI visuals.",
    )
    parser.add_argument(
        "--page-expression-plan",
        default="待记录",
        help="Page-level expression type, visual carrier, asset source, and style constraint record path or summary.",
    )
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
- 模板包版本：{TEMPLATE_BUNDLE_VERSION}
- 任务模式：{args.mode}
- 创建时间：{now.isoformat(timespec="seconds")}
- 当前目录：`{cwd}`
- 任务标题：{args.title}
- Design.md：{args.design_file}
- Content.md：{args.content_file}
- 来源：{args.source}
- 输入归属：{args.source_authority}
- 场景：{args.scenario}
- 规格：{args.spec}
- 输出格式：{args.format}
- 处理模式：{args.processing_mode}
- Logo替换：{args.logo}
- 风格选择：{args.style}
- 模板选择：{args.template}
- 澄清状态：{args.clarification_status}
- Brief 确认：{args.brief_confirmation}
- 风格确认：{args.style_confirmation}
- 样片确认：{args.sample_confirmation}
- 资产来源策略：{args.asset_source_strategy}
- 页级视觉表达：{args.page_expression_plan}

## V1.2 必经确认门

- 待记录：缺失字段的澄清问题、用户回答与“无需澄清”的依据；未完成澄清不得进入完整生成。
- 待记录：解析后的 Brief、用户确认或修改；未确认不得进入风格或样片后的完整生成。
- 待记录：已展示的模板/风格预览、用户选择或“智能推荐”的确认；不得静默套用默认风格。
- 待记录：代表性样片、预览证据与用户确认；跳过仅限用户明确决定并记录原因。

## 澄清与内容边界

- 待记录：用户明确要求、内容是否允许改写、覆盖决定与不可逆边界。
- 待记录：执行意图证据、已确认输入路径及其归属；工作区存在性或历史记忆不能代替确认。
- 待记录：`check_only` 保持源文件只读；`repair` 记录来源与回滚点。

## 页数、大纲与文本预算

- 待记录：逐页标题、目的、布局、核心内容、资产、预计行数、密度风险与拆页策略。
- 待记录：每个核心内容页的表达类型、视觉载体、资产来源和所选风格约束；图片、图表与图解须服务于观点，不得仅作装饰。
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
    if args.mode in SOURCE_REQUIRED_MODES and args.source_authority in {"unconfirmed", "not_applicable"}:
        raise SystemExit(
            "E_INPUT_UNCONFIRMED: create/convert/repair requires an active source authority; "
            "action=confirm current-turn content, an explicit path, a workspace candidate, or a continuation source"
        )
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
