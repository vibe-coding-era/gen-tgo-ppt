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
    parser.add_argument("--format", default="待确认", help="PPT, HTML, or both.")
    parser.add_argument("--style", default="待确认", help="Selected visual style numbers.")
    parser.add_argument("--template", default="待确认", help="Template choice.")
    args = parser.parse_args()

    now = datetime.now().astimezone()
    filename = f"gen-tgo-ppt-生成日志-{now.strftime('%Y%m%d-%H%M%S')}.md"
    path = Path.cwd() / filename
    if path.exists():
        raise SystemExit(f"Refusing to overwrite existing log: {path}")

    content = f"""# gen-tgo-ppt 生成日志

- Skill 版本：v0.4
- 创建时间：{now.isoformat(timespec="seconds")}
- 当前目录：`{Path.cwd()}`
- 任务标题：{args.title}
- 来源：{args.source}
- 场景：{args.scenario}
- 输出格式：{args.format}
- 风格选择：{args.style}
- 模板选择：{args.template}

## 内容探讨

- 待记录：内容总结、是否优化、用户确认。

## 页数与大纲

- 待记录：总页数、逐页标题、布局、风格、核心内容。

## 样片

- 待记录：样片路径、预览方式、用户反馈。

## 完整输出

- 待记录：PPTX/HTML 路径、渲染或预览结果。

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
