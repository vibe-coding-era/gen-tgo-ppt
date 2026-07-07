---
name: gen-tgo-ppt-skill
description: 生成或改造 TGO鲲鹏会 / GTLC 风格 PPT 与 HTML 演示稿。用于从 PPT、PDF、Markdown、HTML 或粘贴内容生成演示材料：开场介绍自己，首次使用时询问 GTLC大会/TGO日常活动分享应用场景与 16:9 等规格并写入 Design.md，继续探讨主题问题与思考模式并把文本初稿写入 Content.md；按场景、模板、视觉风格拆分的 references/design/**/design.md 渐进式加载样式规则；用户上传 PPT/PDF 时先澄清是修改内容还是只套模板；用户上传 LOGO 时可替换 GTLC LOGO；PPT 输出必须在标题页后增加嘉宾介绍空白页、末尾增加“感谢聆听”页；再确认 PPT/HTML 格式、展示编号风格图、页数大纲确认、一页样片确认、完整生成、逐页校对版型、当前目录生成日志、中文子智能体“检查风格/检查文字”复核的流程交付。
---

# Gen TGO PPT Skill

## Overview

Author: 肉山  
Version: v0.5

Use this skill to turn existing PPT, Markdown, HTML, or pasted content into a TGO/GTLC-style presentation or HTML slide deck. Keep `SKILL.md` as the operating guide and load the references only when needed.

## Quick Workflow

1. Start with this self-introduction: `我是 TGO鲲鹏会 PPT 生成 Skill，可以生成 PPT 格式和 HTML 格式。`
2. For first use in the current directory, or when `Design.md` is missing, ask the application scene with numeric options: `1. GTLC 大会` and `2. TGO日常活动分享`; then ask the spec: default `16:9` or another ratio. Write the confirmed design intake to `Design.md` in the user's current working directory.
3. For first use in the current directory, or when `Content.md` is missing, discuss the content: `1. 主题、问题` and `2. 思考模式`. Write the text draft or source-content brief to `Content.md` in the user's current working directory.
4. If the user uploaded a PPT/PDF source, ask the processing mode with numeric options: `1. 修改内容并套模板` and `2. 只套模板不改内容`. Record the choice in `Design.md` and the generation log.
5. If the user uploaded a LOGO, ask whether to replace the GTLC LOGO with it. If confirmed, replace the GTLC LOGO consistently while preserving the uploaded logo's aspect ratio.
6. Ask the output format with numeric options: `1. PPT` and `2. HTML`; if the user already specified it, only acknowledge.
7. Show `assets/design/previews/styles/tgo-presentation-design-system-v1.png` and ask the user to choose style numbers. Allow different pages or page types to use different styles.
8. Read `Design.md`, `Content.md`, and any source content first, then summarize the message, structure, audience, weak spots, and density. Ask whether the user wants content optimization before slide production.
9. Load `references/conversion-workflows.md`, `references/generation-log.md`, and `references/design/index.md`; then progressively load only the needed `design.md` files from `references/design/` based on confirmed scene, template, and visual style choices.
10. Before generating the deck, present a plan for user confirmation: total page count plus each slide's title, purpose, template layout, design-system style, key points, and assets. For PPT output, always include a blank guest-introduction page immediately after the title page and a final `感谢聆听` closing page.
11. Before creating any sample or full output, create a generation log in the user's current working directory and keep appending to it.
12. After plan approval, generate one representative sample page first and ask the user to confirm style, density, and content treatment.
13. After sample approval, generate the full PPTX/HTML. Use the relevant PPTX in `assets/design/templates/` as the base for PPTX output; preserve TGO/GTLC brand background whenever possible.
14. Render or preview the result before delivery. For PPT output, inspect every slide for layout correctness, unexpected line breaks, overflow, logo/footer placement, and style consistency. Then run `检查风格` and `检查文字` as separate review passes.
15. Update the generation log with output paths, review results, and unresolved issues before final delivery.

For every choice menu, accept a plain number as confirmation. If the user enters `1`, map it to the first option in the latest menu.

## Clarify Before Converting

Ask the user concise, high-value questions before making irreversible style choices:

- 开场：我是 TGO鲲鹏会 PPT 生成 Skill，可以生成 PPT 格式和 HTML 格式。
- 首次使用设计澄清：先问应用场景 `1. GTLC 大会` / `2. TGO日常活动分享`，再问规格：默认 `16:9`，或让用户提供其他比例；把确认结果写入当前目录的 `Design.md`。
- 首次使用内容探讨：继续问 `1. 主题、问题` 和 `2. 思考模式`；把文本初稿、问题定义、思考路径或用户提供的素材摘要写入当前目录的 `Content.md`。
- PPT/PDF 上传处理模式：如果用户上传 PPT 或 PDF，必须先问 `1. 修改内容并套模板` / `2. 只套模板不改内容`。选择只套模板时，保留原文、原页序和核心版面含义，只做 GTLC/TGO 视觉映射和必要排版修复。
- LOGO 替换：如果用户上传 LOGO，询问是否用该 LOGO 替换 GTLC LOGO；确认后全 deck 一致替换，保持比例，不拉伸、不裁掉识别主体。
- 场景：`1. GTLC 大会` / `2. TGO日常活动分享`
- 格式：`1. PPT` / `2. HTML`
- 风格：展示 `assets/design/previews/styles/tgo-presentation-design-system-v1.png`，让用户输入数字选择；允许说“封面用 3，内容页用 1，AI 章节用 4”。
- 内容探讨：我已读完内容，是否需要我先优化叙事结构、标题表达、页数密度或删减合并？
- 输出格式：只要 PPTX、只要 HTML，还是两者都要？
- 模板倾向：白底、浅色、深色、混用，还是由内容场景自动选择？
- 目标用途：大会开场、主题演讲、嘉宾介绍、议程/目录、复盘总结、路演材料、打印分发？
- 内容保真度：优先保持原 PPT 页数/图表，还是重排成 GTLC 风格？
- 图片处理：保留原图、替换为用户提供图片、或使用模板背景与 Logo？
- 字体约束：是否允许使用思源黑体/Helvetica/PingFang/微软雅黑替代链？
- 品牌文字：会议年份、城市、主标题、副标题、讲者、日期是否需要更新？

Do not ask about details already obvious from the source file, such as slide count, existing headings, or embedded images.

When `Design.md` or `Content.md` already exists, read and reuse it. Ask only for missing or stale items, and update the file instead of overwriting user-authored sections.

## Working Files

Create or update these Markdown files in the user's current working directory during first-use intake:

- `Design.md`: record design decisions and reusable presentation constraints.

```markdown
# Design

- 应用场景：
- 规格：
- 输出格式：
- 模板倾向：
- 风格选择：
- 处理模式：
- Logo：

## 备注
```

- `Content.md`: record the discussion outcome and the first text draft.

```markdown
# Content

## 主题、问题

## 思考模式

## 文本初稿
```

## PPT Structure And Branding

- For every PPT/PPTX output, insert a blank `嘉宾介绍` page immediately after the title/cover page. Keep it visually aligned with the selected template, but leave the content area empty unless the user provides guest information.
- For every PPT/PPTX output, append a final `感谢聆听` page as the closing page.
- Count both mandatory pages in the deck plan, sample/full generation records, and final page count.
- If the user supplied a replacement LOGO and confirmed replacement, use it wherever the GTLC LOGO would appear. Preserve aspect ratio, align to the original logo anchor, and adjust size only enough to avoid distortion or collision.
- If no replacement LOGO is confirmed, keep the GTLC LOGO.

## Progressive Design Loading

Keep `SKILL.md` as the workflow router. Do not load all design references up front.

1. After scene/spec clarification, read `references/design/index.md` and `references/design/shared/design.md`.
2. Load exactly one scenario file:
   - `GTLC 大会`: `references/design/scenarios/gtlc-conference/design.md`
   - `TGO日常活动分享`: `references/design/scenarios/tgo-daily-sharing/design.md`
3. Load template design only after the user chooses a template or after inferring one from the content:
   - `white`: `references/design/templates/white/design.md`
   - `light`: `references/design/templates/light/design.md`
   - `dark`: `references/design/templates/dark/design.md`
4. Load only selected visual style files from `references/design/visual-styles/*/design.md`. For mixed per-page or per-section styles, load each selected style file once and record the mapping in the deck plan.
5. Keep the user's working `Design.md` in the current directory as the run-specific decision record. Do not confuse it with the reusable style `design.md` files under `references/design/`.

## Required Confirmation Gates

- Gate 0: First-use intake. Ensure `Design.md` records application scene and spec, and `Content.md` records topic/problem plus thinking mode before deck planning. Create missing files in the current working directory; preserve and update existing files.
- Gate 1: Source-mode clarification. If the source is PPT/PDF, confirm whether to modify content or only apply the template before discussing optimization.
- Gate 2: Content discussion. After reading `Design.md`, `Content.md`, and the source, ask whether to optimize content before design. If the user says no, preserve wording and structure unless readability requires minor splitting.
- Gate 3: Deck plan. Present total slide count and a slide-by-slide outline. For PPT output, include the mandatory `嘉宾介绍` page after the title page and final `感谢聆听` page. Do not generate the full deck until the user confirms the plan.
- Gate 4: Generation log. Before creating a sample or full PPTX/HTML, create `./gen-tgo-ppt-生成日志-YYYYMMDD-HHMMSS.md` in the current working directory. Do not deliver generated output without this log.
- Gate 5: One-page sample. Generate one representative page first, preferably the most typical content slide or the riskiest slide. Do not generate the full deck until the user confirms the sample.
- Gate 6: Full-deck review. After full generation, inspect every slide's layout, then use the Chinese-named reviewers `检查风格` and `检查文字` before final delivery.

If the user explicitly says to skip confirmations, still produce the plan and sample as execution records unless the request is urgent and unambiguous. Never skip final style/content review.

## Generation Log

- Create the log in the directory where the user invoked the generation task, not inside the skill directory.
- Use this filename pattern: `gen-tgo-ppt-生成日志-YYYYMMDD-HHMMSS.md`.
- Create the log before generating the first sample page or full output. If the current directory is not writable, stop before generation and ask the user for a writable current directory.
- Keep the log updated with: `Design.md` path, `Content.md` path, source file, scene, spec, PPT/PDF processing mode, logo replacement decision, output format, style choices, template choice, content optimization decision, confirmed page plan, mandatory guest-introduction/closing pages, sample path, final output paths, commands/tools used, per-slide layout review, `检查风格` results, `检查文字` results, and deferred issues.
- Use `scripts/create_generation_log.py` from the user's current directory when convenient, then append manually as decisions and artifacts are produced.
- Mention the log path in the final response.

## Template Selection

- `assets/design/templates/white/tgo-gtlc-white.pptx`: white content pages, dark blue cover/back cover, blue footer strip and top-right GTLC logo. Use for formal, documentation-like, or print-friendly decks.
- `assets/design/templates/light/tgo-gtlc-light.pptx`: pale blue-gray content pages with the same GTLC brand framing. Use as the default for readable business presentations.
- `assets/design/templates/dark/tgo-gtlc-dark.pptx`: dark blue gradient throughout. Use for keynote, opening, closing, and high-impact narrative decks.

If the user does not choose, default to `light` for mixed content, `white` for dense text/tables, and `dark` for short keynote-style decks.

## Required Resources

- Read `references/conversion-workflows.md` for source-specific conversion rules.
- Read `references/generation-log.md` before generating any sample or full PPTX/HTML.
- Read `references/design/index.md` to decide which reusable style `design.md` files to load.
- Read `references/design/shared/design.md` after the scene/spec clarification.
- Read only the relevant scenario, template, and visual style `design.md` files under `references/design/`.
- Read `references/template-manifest.json` only when a machine-readable summary is enough.
- Use `assets/design/previews/templates/template-contact-sheet.png` when the user needs a quick visual choice among the three templates.
- Use `assets/design/previews/styles/tgo-presentation-design-system-v1.png` to show the eight numbered design styles visually.

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

- Open or render the deck and inspect every slide, not only samples. Use slide screenshots/contact sheets when possible.
- Confirm the title page is followed immediately by a blank `嘉宾介绍` page and the final page is `感谢聆听`.
- Confirm 16:9 canvas uses 26.667 in x 15 in or preserves template dimensions.
- Confirm title/body placeholders match the selected template positions within a small visual tolerance.
- Confirm top-right logo, bottom footer strip, and full-bleed backgrounds are not stretched or cropped incorrectly.
- Confirm there are no unexpected line breaks, text overflows, clipped words, style-mismatched placeholders, or content colliding with logos/footer/background elements.
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
  - `检查风格`: visual review only, including every slide's template choice, colors, typography, layout positions, logo/footer/background placement, contrast, overflow, unexpected line breaks, mandatory guest-introduction/closing pages, and slide rhythm.
  - `检查文字`: wording and content review only, including logical flow, missing context, source fidelity, title accuracy, slide density, duplicated points, and whether optimization choices match user approval.
- In user-facing plans and review records, use only `生成内容`, `检查风格`, and `检查文字`; do not expose English worker names.
- If subagents are unavailable, run two clearly separated self-review passes and tell the user that independent subagents were not available.

## Guardrails

- Do not invent a new TGO/GTLC brand palette when a bundled template contains the needed asset.
- Do not remove or redraw the GTLC logo unless the user provides an approved replacement.
- Do not replace the GTLC logo merely because a LOGO file exists; ask for confirmation first, then replace consistently.
- Do not force every source slide into the same layout; map by intent: cover, section, intro, agenda, content, summary, closing.
- Do not skip the mandatory blank `嘉宾介绍` page or final `感谢聆听` page for PPT/PPTX output unless the user explicitly overrides this rule.
- Do not force one design-system style across every page. Allow per-page or per-section style choices while preserving the TGO/GTLC brand background and identity layer.
- Do not over-question. Ask about template choice, output format, fidelity, images, and event metadata first; infer the rest from the source.
- Do not deliver generated PPTX/HTML without a generation log in the current directory.
- If required fonts are missing, use this fallback order: Source Han Sans CN, PingFang SC, Microsoft YaHei, Helvetica Neue, Helvetica, Arial, sans-serif.
- If the user requests standard half-size PPT dimensions, scale the original template coordinates and type sizes by `0.5`, then re-render to verify.
