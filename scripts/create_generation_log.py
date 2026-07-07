#!/usr/bin/env python3
"""Create a gen-tgo-ppt generation log in the current working directory."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a gen-tgo-ppt generation log.")
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
    args = parser.parse_args()

    now = datetime.now().astimezone()
    filename = f"gen-tgo-ppt-生成日志-{now.strftime('%Y%m%d-%H%M%S')}.md"
    path = Path.cwd() / filename
    if path.exists():
        raise SystemExit(f"Refusing to overwrite existing log: {path}")

    content = f"""# gen-tgo-ppt 生成日志

- Skill 版本：v0.6
- 排版安全版本：v0.6
- 创建时间：{now.isoformat(timespec="seconds")}
- 当前目录：`{Path.cwd()}`
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
- 生成 subagent：待记录。
- 校验 subagent：待记录。
- 生成/校验是否不同 subagent：待记录。

## 设计澄清

- 应用场景：{args.scenario}
- 规格：{args.spec}
- 处理模式：{args.processing_mode}
- Logo替换：{args.logo}
- 设计输入文件：{args.design_file}
- PPT固定页：标题页后新增空白 `嘉宾介绍` 页；末尾新增 `感谢聆听` 页。

## 内容探讨

- 内容输入文件：{args.content_file}
- 主题、问题：待记录。
- 思考模式：待记录。
- 待记录：内容总结、是否优化、用户确认。

## 页数与大纲

- 待记录：总页数、逐页标题、布局、风格、核心内容，含标题页后的 `嘉宾介绍` 页和最终 `感谢聆听` 页。
- 待记录：逐页内容预算、标题/正文预计行数、密度风险、是否需要拆页或改布局。

## 样片

- 待记录：样片路径、预览方式、用户反馈。

## 完整输出

- 待记录：PPTX/HTML 路径、渲染或预览结果。

## 逐页版型校对

- 待记录：每一页是否存在样式错乱、无故换行、文本溢出、裁切、Logo/页脚碰撞，并记录修复结果。

## v0.6 排版安全校验

- 待记录：`scripts/check_pptx_layout.py` 命令、结果、FAIL/WARN 页面、修复动作与复查结果。

## Subagent 分工

- `生成内容`：待记录。
- `检查风格`：待记录。
- `检查文字`：待记录。
- 生成者是否参与校验：不得参与；待复核。
- 如果未使用独立 subagent，原因：待记录。

## 检查风格

- 待记录：`检查风格` 发现、修复、遗留问题。

## 检查文字

- 待记录：`检查文字` 发现、修复、遗留问题。

## 操作记录

- {now.isoformat(timespec="seconds")} 创建生成日志。

## 待处理问题

- 无。
"""
    path.write_text(content, encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
