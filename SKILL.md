---
name: gen-tgo-ppt-skill
description: 生成或改造 TGO鲲鹏会 / GTLC 风格 PPT 与 HTML 演示稿。用于从 PPT、Markdown、HTML 或粘贴内容生成演示材料：开场介绍自己，询问 GTLC/日常分享场景与 PPT/HTML 格式，展示编号风格图供用户选择，按内容探讨、页数大纲确认、一页样片确认、完整生成、当前目录生成日志、中文子智能体“检查风格/检查文字”复核的流程交付。
---

# Gen TGO PPT Skill

## Overview

Author: 肉山  
Version: v0.4

Use this skill to turn existing PPT, Markdown, HTML, or pasted content into a TGO/GTLC-style presentation or HTML slide deck. Keep `SKILL.md` as the operating guide and load the references only when needed.

## Quick Workflow

1. Start with this self-introduction: `我是 TGO鲲鹏会 PPT 生成 Skill，可以生成 PPT 格式和 HTML 格式。`
2. Ask the scene with numeric options: `1. 用于 GTLC` and `2. 用于日常分享`.
3. Ask the output format with numeric options: `1. PPT` and `2. HTML`; if the user already specified it, only acknowledge.
4. Show `assets/previews/tgo-presentation-design-system-v1.png` and ask the user to choose style numbers. Allow different pages or page types to use different styles.
5. Read the source content first, then summarize the message, structure, audience, weak spots, and density. Ask whether the user wants content optimization before slide production.
6. Load `references/template-style-guide.md`, `references/conversion-workflows.md`, and `references/presentation-design-system-v1.md`.
7. Before generating the deck, present a plan for user confirmation: total page count plus each slide's title, purpose, template layout, design-system style, key points, and assets.
8. Before creating any sample or full output, create a generation log in the user's current working directory and keep appending to it.
9. After plan approval, generate one representative sample page first and ask the user to confirm style, density, and content treatment.
10. After sample approval, generate the full PPTX/HTML. Use the relevant PPTX in `assets/templates/` as the base for PPTX output; preserve TGO/GTLC brand background whenever possible.
11. Render or preview the result before delivery. Then run `检查风格` and `检查文字` as separate review passes.
12. Update the generation log with output paths, review results, and unresolved issues before final delivery.

For every choice menu, accept a plain number as confirmation. If the user enters `1`, map it to the first option in the latest menu.

## Clarify Before Converting

Ask the user concise, high-value questions before making irreversible style choices:

- 开场：我是 TGO鲲鹏会 PPT 生成 Skill，可以生成 PPT 格式和 HTML 格式。
- 场景：`1. 用于 GTLC` / `2. 用于日常分享`
- 格式：`1. PPT` / `2. HTML`
- 风格：展示 `assets/previews/tgo-presentation-design-system-v1.png`，让用户输入数字选择；允许说“封面用 3，内容页用 1，AI 章节用 4”。
- 内容探讨：我已读完内容，是否需要我先优化叙事结构、标题表达、页数密度或删减合并？
- 输出格式：只要 PPTX、只要 HTML，还是两者都要？
- 模板倾向：白底、浅色、深色、混用，还是由内容场景自动选择？
- 目标用途：大会开场、主题演讲、嘉宾介绍、议程/目录、复盘总结、路演材料、打印分发？
- 内容保真度：优先保持原 PPT 页数/图表，还是重排成 GTLC 风格？
- 图片处理：保留原图、替换为用户提供图片、或使用模板背景与 Logo？
- 字体约束：是否允许使用思源黑体/Helvetica/PingFang/微软雅黑替代链？
- 品牌文字：会议年份、城市、主标题、副标题、讲者、日期是否需要更新？

Do not ask about details already obvious from the source file, such as slide count, existing headings, or embedded images.

## Required Confirmation Gates

- Gate 1: Content discussion. After reading the source, ask whether to optimize content before design. If the user says no, preserve wording and structure unless readability requires minor splitting.
- Gate 2: Deck plan. Present total slide count and a slide-by-slide outline. Do not generate the full deck until the user confirms the plan.
- Gate 3: Generation log. Before creating a sample or full PPTX/HTML, create `./gen-tgo-ppt-生成日志-YYYYMMDD-HHMMSS.md` in the current working directory. Do not deliver generated output without this log.
- Gate 4: One-page sample. Generate one representative page first, preferably the most typical content slide or the riskiest slide. Do not generate the full deck until the user confirms the sample.
- Gate 5: Full-deck review. After full generation, use the Chinese-named reviewers `检查风格` and `检查文字` before final delivery.

If the user explicitly says to skip confirmations, still produce the plan and sample as execution records unless the request is urgent and unambiguous. Never skip final style/content review.

## Generation Log

- Create the log in the directory where the user invoked the generation task, not inside the skill directory.
- Use this filename pattern: `gen-tgo-ppt-生成日志-YYYYMMDD-HHMMSS.md`.
- Create the log before generating the first sample page or full output. If the current directory is not writable, stop before generation and ask the user for a writable current directory.
- Keep the log updated with: source file, scene, output format, style choices, template choice, content optimization decision, confirmed page plan, sample path, final output paths, commands/tools used, `检查风格` results, `检查文字` results, and deferred issues.
- Use `scripts/create_generation_log.py` from the user's current directory when convenient, then append manually as decisions and artifacts are produced.
- Mention the log path in the final response.

## Template Selection

- `assets/templates/tgo-gtlc-white.pptx`: white content pages, dark blue cover/back cover, blue footer strip and top-right GTLC logo. Use for formal, documentation-like, or print-friendly decks.
- `assets/templates/tgo-gtlc-light.pptx`: pale blue-gray content pages with the same GTLC brand framing. Use as the default for readable business presentations.
- `assets/templates/tgo-gtlc-dark.pptx`: dark blue gradient throughout. Use for keynote, opening, closing, and high-impact narrative decks.

If the user does not choose, default to `light` for mixed content, `white` for dense text/tables, and `dark` for short keynote-style decks.

## Required Resources

- Read `references/template-style-guide.md` for exact canvas size, colors, fonts, layout names, and object positions.
- Read `references/conversion-workflows.md` for source-specific conversion rules.
- Read `references/presentation-design-system-v1.md` when the user chooses a world-class visual style, asks for higher visual quality, or needs mixed per-page style treatment.
- Read `references/generation-log.md` before generating any sample or full PPTX/HTML.
- Read `references/template-manifest.json` when a machine-readable summary is enough.
- Use `assets/previews/template-contact-sheet.png` when the user needs a quick visual choice among the three templates.
- Use `assets/previews/tgo-presentation-design-system-v1.png` to show the eight numbered design styles visually.

## Useful Script

Run the read-only inspector when you need to compare an input PPTX with the GTLC templates:

```bash
python scripts/inspect_pptx_style.py path/to/deck.pptx
```

It prints canvas size, theme colors, template layouts, placeholder positions, media dimensions, and inherited text-style hints. Use it as evidence, not as a generator.

Create a generation log from the user's current directory:

```bash
python /path/to/gen-tgo-ppt-skill/scripts/create_generation_log.py --title "演示稿标题" --source "source.md" --format PPT
```

Resolve the script path relative to this skill directory, but run it from the user's current working directory. The script prints the created log path. Append to that file throughout the run.

## Validation

For PPTX output:

- Open or render the deck and inspect at least cover, one content slide, one dense slide, and closing slide.
- Confirm 16:9 canvas uses 26.667 in x 15 in or preserves template dimensions.
- Confirm title/body placeholders match the selected template positions within a small visual tolerance.
- Confirm top-right logo, bottom footer strip, and full-bleed backgrounds are not stretched or cropped incorrectly.
- Confirm text contrast: dark text on white/light pages, white text on dark pages.
- Confirm the generation log exists in the current working directory and includes sample/final output paths.

For HTML output:

- Use a fixed 16:9 slide canvas and CSS variables from the style guide.
- Verify desktop and mobile/print preview states.
- Confirm the HTML version visually preserves the same hierarchy, margins, logo/footer treatment, and background choice.
- Confirm the generation log exists in the current working directory and includes sample/final output paths.

Independent review:

- Use these exact Chinese subagent names whenever subagent tooling is available:
  - `生成内容`: deck/HTML generation worker, only when generation is delegated away from the lead.
  - `检查风格`: visual review only, including template choice, colors, typography, layout positions, logo/footer/background placement, contrast, overflow, and slide rhythm.
  - `检查文字`: wording and content review only, including logical flow, missing context, source fidelity, title accuracy, slide density, duplicated points, and whether optimization choices match user approval.
- In user-facing plans and review records, use only `生成内容`, `检查风格`, and `检查文字`; do not expose English worker names.
- If subagents are unavailable, run two clearly separated self-review passes and tell the user that independent subagents were not available.

## Guardrails

- Do not invent a new TGO/GTLC brand palette when a bundled template contains the needed asset.
- Do not remove or redraw the GTLC logo unless the user provides an approved replacement.
- Do not force every source slide into the same layout; map by intent: cover, section, intro, agenda, content, summary, closing.
- Do not force one design-system style across every page. Allow per-page or per-section style choices while preserving the TGO/GTLC brand background and identity layer.
- Do not over-question. Ask about template choice, output format, fidelity, images, and event metadata first; infer the rest from the source.
- Do not deliver generated PPTX/HTML without a generation log in the current directory.
- If required fonts are missing, use this fallback order: Source Han Sans CN, PingFang SC, Microsoft YaHei, Helvetica Neue, Helvetica, Arial, sans-serif.
- If the user requests standard half-size PPT dimensions, scale the original template coordinates and type sizes by `0.5`, then re-render to verify.
