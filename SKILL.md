---
name: gen-tgo-ppt-skill
description: 生成或改造 TGO鲲鹏会 / GTLC 风格 PPT 与 HTML 演示稿。用于从 PPT、PDF、Markdown、HTML 或粘贴内容生成演示材料：开场介绍自己，首次使用时询问 GTLC大会/TGO日常活动分享应用场景与 16:9 等规格并写入 Design.md，TGO日常活动分享默认优先使用 tgo-daily 日常分享模板，GTLC大会默认使用 GTLC 模板；继续探讨主题问题与思考模式并把文本初稿写入 Content.md；按场景、模板、视觉风格拆分的 references/design/**/design.md 渐进式加载样式规则；用户上传 PPT/PDF 时先澄清是修改内容还是只套模板；用户上传 LOGO 时可替换 GTLC LOGO；PPT 输出必须在标题页后增加嘉宾介绍空白页、末尾增加“感谢聆听”页；再确认 PPT/HTML 格式、展示编号风格图、页数大纲确认、一页样片确认、完整生成、v0.7 排版安全校验、逐页校对版型、当前目录生成日志、中文子智能体“生成内容/检查风格/检查文字”分工，且生成与校验必须由不同 subagent 执行。
---

# Gen TGO PPT Skill

## 重要说明和介绍

以下说明为用户指定的受保护内容。AI 后续不得改写、删除、弱化或移动本节内容。

本 SKILL 是 TGO 鲲鹏会为了 AI 时代内容生成准备的 SKILL，内置了相应的模板，也可以做内容探讨，会使用不同的 SubAgent 做生成、校验，作者是杭州分会的肉山，欢迎使用。

## Overview

Author: 肉山  
Version: v0.7

Use this skill to turn existing PPT, Markdown, HTML, or pasted content into a TGO/GTLC-style presentation or HTML slide deck. Keep `SKILL.md` as the operating guide and load the references only when needed.

## Quick Workflow

1. Start with this self-introduction: `我是 TGO鲲鹏会 PPT 生成 Skill，可以生成 PPT 格式和 HTML 格式。`
2. For first use in the current directory, or when `Design.md` is missing, ask the application scene with numeric options: `1. GTLC 大会` and `2. TGO日常活动分享`; then ask the spec: default `16:9` or another ratio. Write the confirmed design intake to `Design.md` in the user's current working directory.
3. For first use in the current directory, or when `Content.md` is missing, discuss the content: `1. 主题、问题` and `2. 思考模式`. Write the text draft or source-content brief to `Content.md` in the user's current working directory.
4. If the user uploaded a PPT/PDF source, ask the processing mode with numeric options: `1. 修改内容并套模板` and `2. 只套模板不改内容`. Record the choice in `Design.md` and the generation log.
5. If the user uploaded a LOGO, ask whether to replace the GTLC LOGO with it. If confirmed, replace the GTLC LOGO consistently while preserving the uploaded logo's aspect ratio.
6. Ask the output format with numeric options: `1. PPT` and `2. HTML`; if the user already specified it, only acknowledge.
7. Show `assets/design/previews/styles/tgo-presentation-design-system-v1.png` and ask the user to choose style numbers. Allow different pages or page types to use different styles.
8. Read `Design.md`, `Content.md`, and any source content first, then summarize the message, structure, audience, weak spots, density, and likely layout risks. Ask whether the user wants content optimization before slide production.
9. Load `references/conversion-workflows.md`, `references/generation-log.md`, and `references/design/index.md`; then progressively load only the needed `design.md` files from `references/design/` based on confirmed scene, template, and visual style choices.
10. Before generating the deck, present a plan for user confirmation: total page count plus each slide's title, purpose, template layout, design-system style, key points, assets, content budget, expected title/body line count, overflow risk, and split/fit strategy. For PPT output, always include a blank guest-introduction page immediately after the title page and a final `感谢聆听` closing page.
11. Before creating any sample or full output, create a generation log in the user's current working directory and keep appending to it.
12. After plan approval, generate one representative sample page first and ask the user to confirm style, density, and content treatment.
13. After sample approval, generate the full PPTX/HTML. When subagent tooling is available, assign full generation to `生成内容`; that subagent must not perform final validation. Use layout-safe text placement for every title, body, label, and note: estimate line count before placing text, fit within the safe box, and split the slide if the text cannot remain readable. Use the relevant PPTX in `assets/design/templates/` as the base for PPTX output; preserve TGO/GTLC brand background whenever possible.
14. Render or preview the result before delivery. For PPT output, run `scripts/check_pptx_layout.py` on the generated deck, fix every `FAIL`, inspect every slide for layout correctness, unexpected line breaks, overflow, logo/footer placement, and style consistency, then run `检查风格` and `检查文字` as separate validation subagents. `检查风格` and `检查文字` must be different from `生成内容`.
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
- 风格：展示 `assets/design/previews/styles/tgo-presentation-design-system-v1.png`，让用户输入数字选择；允许说“封面用 3，内容页用 1，AI 组织/架构页用 9”。
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
- 排版安全：默认启用 v0.7

## 备注

## 排版安全约束

- 标题行数：
- 正文条数：
- 字号下限：
- Logo/页脚安全区：
- 超框处理：
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
- Treat mandatory pages as hard validation items: page 2 may contain only the `嘉宾介绍` title unless the user explicitly provides guest content, and the final page must contain `感谢聆听` unless the user explicitly overrides the closing copy in the plan and log.
- If the user supplied a replacement LOGO and confirmed replacement, use it wherever the GTLC LOGO would appear. Preserve aspect ratio, align to the original logo anchor, and adjust size only enough to avoid distortion or collision.
- If no replacement LOGO is confirmed, keep the GTLC LOGO.

## Layout Safety Constraints

Use the v0.7 layout safety policy for every PPTX and HTML output. `v07.md` is the detailed change record; `SKILL.md` is the operative rule source.

- Before generation, assign each slide a content budget: title line count, body bullet count, table/node count, expected density, overflow risk, and whether the slide may need splitting.
- Keep default 16:9 text margins at or above 0.45 in. Treat the top-right GTLC/logo area and the bottom footer strip as text keep-out zones unless the shape is the actual logo/footer.
- When using a half-size 16:9 deck (`13.333 in x 7.5 in`), scale coordinates, keep-out zones, margins, and type-size thresholds by `0.5`; still render and visually re-check the result.
- Cover pages and other visual-heavy pages must define explicit text-safe zones and visual keep-out zones before placing text. Do not let subtitle, date, speaker, or metadata boxes enter the GTLC main-visual area, even if they remain inside the slide bounds.
- For GTLC dark cover/closing pages that use the large conference background mark, prefer the safe solid-panel treatment: use a lightly blurred/dimmed full-slide background, then place all page copy inside a centered opaque deep-blue content panel. The panel fill must be fully opaque, not glass-transparent; no background image may show through inside the content panel.
- Solid-panel cover/closing content boxes must size from measured content width and height, keep balanced top/bottom padding, and never force a title, subtitle, date, sponsor name, or closing copy to wrap or overflow. If the longest line does not fit, enlarge the panel within the safe area or reduce font size within readable limits before rendering.
- Cover/closing pages must use explicit fonts for every run, with the fallback chain resolved at generation time. Do not leave key title-page or closing-page text on theme fonts such as `+mj-lt`, `+mn-lt`, Calibri, or unset font names.
- Short key-value rows and project facts such as `时间：...`、`地点：...`、`合作身份：...` should be treated as single-line information items unless the plan explicitly budgets a wrap. Widen the text box, remove unnecessary spaces, or reduce wording before allowing these rows to break.
- Default minimum readable sizes: body text 20 pt, supporting text 16 pt, table/caption text 14 pt. Text under 14 pt requires a log note; text under 12 pt is not allowed without explicit user approval.
- Cover and section titles may be large, but if a title wraps, recalculate the following text and object positions. A wrapped title must not cover subtitles, bullets, charts, or metadata.
- Default content budget: common content pages should stay within 5 bullets, each about 28 Chinese characters or equivalent; two-column pages should stay within 4 bullets per column; dense tables should be split or summarized when they exceed about 6 rows x 5 columns.
- When content does not fit, use this order: shorten or merge text, enlarge the box inside the safe area, reduce font size within limits, switch layout, split the slide, then ask for user confirmation if full source fidelity still cannot fit.
- For PPTX generation, every text shape must go through a fit/split check such as `fit_text_to_box`, `estimate_text_lines`, or equivalent logic. Do not write long text directly into a fixed box and hope PowerPoint handles it.
- For HTML generation, enforce the same safe areas with CSS variables, fixed 16:9 slide geometry, and overflow rules that prevent text from covering later content.

## Reusable Page Style Constraints

### Image + Project Basic Info

Use this page style for event/project context pages such as `项目基本信息`, sponsor briefing pages, venue/event photos with facts, and source-PPT pages that pair one large visual proof image with a compact fact list.

- Composition: place the main photo or visual proof on the left as the dominant element; place `项目基本信息` and its fact rows in a right-side column. The right column must stay outside the top-right logo and bottom footer keep-out zones.
- Right-column facts must use compact key-value rows with a small dot or equivalent marker plus a single text box. Typical labels include `大会主题`、`时间`、`地点`、`参会人群`、`合作身份`、`项目名称`、`负责人`、`主办方`.
- Each project-info row is a planned single-line item by default. Do not allow a row to wrap merely because the box height can contain two lines; wrapping breaks the intended rhythm of this style.
- Before placing rows, measure the longest label/value row and set a shared row text-box width from that longest row. For the standard half-size `13.333 in x 7.5 in` GTLC deck, the project-info row text area should normally be at least `3.7 in` wide; for the full-size template use at least `7.4 in`.
- Remove layout-hostile spaces inside dates and short Chinese phrases when they create awkward wrapping, for example prefer `2026年6月27-28日｜地点：杭州` over `2026 年 6 月 27-28 日，地点：杭州`.
- If a row still cannot fit safely, first widen the right column within the safe area, then shorten the row, split time and location into separate rows, or reduce font size within v0.7 readable limits. Do not silently ship wrapped rows.
- Keep row x positions, widths, bullet/dot alignment, and vertical rhythm consistent. The fact list should read as one aligned block, not as independently drifting text boxes.
- Validation must include the static checker with project-info style checks enabled and a rendered slide review. Treat `PROJECT_INFO_ITEM_WRAP`, `PROJECT_INFO_ITEM_TOO_NARROW`, `PROJECT_INFO_ITEM_NOT_RIGHT_COLUMN`, and `PROJECT_INFO_ITEM_WORD_WRAP_ENABLED` as repair items unless the generation log records an explicit exception.

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
   - `tgo-daily`: `references/design/templates/tgo-daily/design.md`
4. Load only selected visual style files from `references/design/visual-styles/*/design.md`. For mixed per-page or per-section styles, load each selected style file once and record the mapping in the deck plan.
5. Keep the user's working `Design.md` in the current directory as the run-specific decision record. Do not confuse it with the reusable style `design.md` files under `references/design/`.

## Required Confirmation Gates

- Gate 0: First-use intake. Ensure `Design.md` records application scene and spec, and `Content.md` records topic/problem plus thinking mode before deck planning. Create missing files in the current working directory; preserve and update existing files.
- Gate 1: Source-mode clarification. If the source is PPT/PDF, confirm whether to modify content or only apply the template before discussing optimization.
- Gate 2: Content discussion. After reading `Design.md`, `Content.md`, and the source, ask whether to optimize content before design. If the user says no, preserve wording and structure unless readability requires minor splitting.
- Gate 3: Deck plan. Present total slide count and a slide-by-slide outline. Include each slide's layout safety budget: title/body line estimates, density risk, text keep-out areas, and split/fit plan. For PPT output, include the mandatory `嘉宾介绍` page after the title page and final `感谢聆听` page. Do not generate the full deck until the user confirms the plan.
- Gate 4: Generation log. Before creating a sample or full PPTX/HTML, create `./gen-tgo-ppt-生成日志-YYYYMMDD-HHMMSS.md` in the current working directory. Do not deliver generated output without this log.
- Gate 5: One-page sample. Generate one representative page first, preferably the most typical content slide or the highest layout-risk slide. Validate the sample's title/body fit, keep-out zones, and readable font sizes. Do not generate the full deck until the user confirms the sample.
- Gate 6: Subagent separation. When subagent tooling is available, use `生成内容` for generation and use different subagents `检查风格` and `检查文字` for validation. A subagent that generated the deck, sample, or HTML must not approve its own output.
- Gate 7: Full-deck review. After full generation, run the PPTX layout checker when applicable, fix every `FAIL`, inspect every slide's layout, then use the Chinese-named reviewers `检查风格` and `检查文字` before final delivery.

If the user explicitly says to skip confirmations, still produce the plan and sample as execution records unless the request is urgent and unambiguous. Never skip final style/content review.

## Generation Log

- Create the log in the directory where the user invoked the generation task, not inside the skill directory.
- Use this filename pattern: `gen-tgo-ppt-生成日志-YYYYMMDD-HHMMSS.md`.
- Create the log before generating the first sample page or full output. If the current directory is not writable, stop before generation and ask the user for a writable current directory.
- Keep the log updated with: skill version, layout safety version, `Design.md` path, `Content.md` path, source file, scene, spec, PPT/PDF processing mode, logo replacement decision, output format, style choices, template choice, content optimization decision, confirmed page plan, per-slide content budget, mandatory guest-introduction/closing pages, sample path, final output paths, commands/tools used, PPTX layout-check command/results, generation subagent name, validation subagent names, proof that validation subagents differ from the generation subagent, per-slide layout review, `检查风格` results, `检查文字` results, and deferred issues.
- Use `scripts/create_generation_log.py` from the user's current directory when convenient, then append manually as decisions and artifacts are produced.
- Mention the log path in the final response.

## Template Selection

- `assets/design/templates/white/tgo-gtlc-white.pptx`: white content pages, dark blue cover/back cover, blue footer strip and top-right GTLC logo. Use for formal, documentation-like, or print-friendly decks.
- `assets/design/templates/light/tgo-gtlc-light.pptx`: pale blue-gray content pages with the same GTLC brand framing. Use as the default for readable business presentations.
- `assets/design/templates/dark/tgo-gtlc-dark.pptx`: dark blue gradient throughout. Use for keynote, opening, closing, and high-impact narrative decks.
- `assets/design/templates/tgo-daily/tgo-daily-sharing-16-9.pptx`: TGO daily sharing template for `TGO日常活动分享`, community salon sharing, member internal sharing, and other non-GTLC scenes.

If the user does not choose, default to `tgo-daily` for `TGO日常活动分享`, `light` for mixed GTLC content, `white` for dense text/tables, and `dark` for short keynote-style decks.

## Required Resources

- Read `references/conversion-workflows.md` for source-specific conversion rules.
- Read `references/generation-log.md` before generating any sample or full PPTX/HTML.
- Read `v07.md` when the task concerns overflow, layout safety, version v0.7 changes, or detailed acceptance criteria.
- Read `references/design/index.md` to decide which reusable style `design.md` files to load.
- Read `references/design/shared/design.md` after the scene/spec clarification.
- Read only the relevant scenario, template, and visual style `design.md` files under `references/design/`.
- Read `references/template-manifest.json` only when a machine-readable summary is enough.
- Use `assets/design/previews/templates/template-contact-sheet.png` when the user needs a quick visual choice among the available templates.
- Use `assets/design/previews/styles/tgo-presentation-design-system-v1.png` to show the nine numbered design styles visually.

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

Run the static PPTX layout checker after generating a PPTX and before final review:

```bash
python /path/to/gen-tgo-ppt-skill/scripts/check_pptx_layout.py path/to/generated.pptx
```

Treat any `FAIL` as a required fix before delivery. Treat `WARN` as a manual review item and record the decision in the generation log.

## Validation

For PPTX output:

- Run `scripts/check_pptx_layout.py` on the generated PPTX before final delivery. Re-run it after fixes when any `FAIL` appears.
- Open or render the deck and inspect every slide, not only samples. Use slide screenshots/contact sheets when possible.
- Confirm the title page is followed immediately by a blank `嘉宾介绍` page and the final page is `感谢聆听`; fail the review if helper text such as `MANDATORY PAGE` or placeholder explanations remain.
- Confirm 16:9 canvas uses 26.667 in x 15 in or preserves template dimensions.
- Confirm title/body placeholders match the selected template positions within a small visual tolerance.
- Confirm top-right logo, bottom footer strip, and full-bleed backgrounds are not stretched or cropped incorrectly.
- Confirm cover and section pages respect their text-safe zones and do not place text over the main visual/background identity layer.
- For solid-panel cover/closing pages, confirm the panel is opaque, the background is not visible through the panel, panel padding is visually balanced, and every line fits without wrapping or clipping.
- Confirm every slide respects the v0.7 content budget or has a logged split/fit reason.
- Confirm there are no unexpected line breaks, text overflows, clipped words, style-mismatched placeholders, or content colliding with logos/footer/background elements.
- Confirm short project-info rows and other key-value facts do not wrap unexpectedly; run the checker with the default short-info wrap warning enabled and treat any unplanned wrap as a required repair.
- On `Image + Project Basic Info` pages, confirm the left visual and right fact column keep clear hierarchy, every fact row remains one line, row widths are shared or visually aligned, row bullets/dots align, and the fact column avoids logo/footer keep-out zones.
- Confirm there are no `FAIL` results from the static checker, no text boxes outside the slide, no high-risk overlaps, and no unreadably small text.
- Confirm text contrast: dark text on white/light pages, white text on dark pages.
- Confirm the generation log exists in the current working directory and includes sample/final output paths.

For HTML output:

- Use a fixed 16:9 slide canvas and CSS variables from the style guide.
- Enforce v0.7 safe areas for title, body, logo, footer, captions, and navigation controls.
- Verify desktop and mobile/print preview states.
- Confirm the HTML version visually preserves the same hierarchy, margins, logo/footer treatment, and background choice.
- Confirm text does not overflow, clip, cover later content, or collapse below readable sizes.
- Confirm the generation log exists in the current working directory and includes sample/final output paths.

Independent review:

- Use these exact Chinese subagent names whenever subagent tooling is available:
  - `生成内容`: deck/HTML generation worker for sample and full output.
  - `检查风格`: visual review only, including every slide's template choice, colors, typography, layout positions, logo/footer/background placement, v0.7 layout-check results, contrast, overflow, unexpected line breaks, mandatory guest-introduction/closing pages, and slide rhythm.
  - `检查文字`: wording and content review only, including logical flow, missing context, source fidelity, title accuracy, slide density, duplicated points, and whether optimization choices match user approval.
- Generation and validation must use different subagents. `生成内容` must not perform `检查风格` or `检查文字`, and a validation subagent must not validate content it generated.
- If generation is handled by the lead because subagent tooling is unavailable, still run `检查风格` and `检查文字` as separate subagents when possible. If no subagents are available at all, run two clearly separated self-review passes, record the limitation in the generation log, and tell the user that independent subagents were not available.
- In user-facing plans and review records, use only `生成内容`, `检查风格`, and `检查文字`; do not expose English worker names.

## Guardrails

- Do not modify, delete, weaken, or move the protected `重要说明和介绍` section. Preserve its wording exactly in future AI edits.
- Do not invent a new TGO/GTLC brand palette when a bundled template contains the needed asset.
- Do not remove or redraw the GTLC logo unless the user provides an approved replacement.
- Do not replace the GTLC logo merely because a LOGO file exists; ask for confirmation first, then replace consistently.
- Do not force every source slide into the same layout; map by intent: cover, section, intro, agenda, content, summary, closing.
- Do not skip the mandatory blank `嘉宾介绍` page or final `感谢聆听` page for PPT/PPTX output unless the user explicitly overrides this rule.
- Do not force one design-system style across every page. Allow per-page or per-section style choices while preserving the TGO/GTLC brand background and identity layer.
- Do not over-question. Ask about template choice, output format, fidelity, images, and event metadata first; infer the rest from the source.
- Do not deliver generated PPTX/HTML without a generation log in the current directory.
- Do not let the same subagent both generate and validate the same deck, sample, or HTML output when subagent tooling is available.
- Do not deliver generated PPTX/HTML with known text overflow, clipped words, out-of-slide text boxes, severe overlaps, unreadably small text, or unresolved `FAIL` results from the PPTX layout checker.
- Do not shrink text below the v0.7 minimums simply to preserve the original page count. Split the slide or ask for approval when full fidelity conflicts with readability.
- Do not let wrapped titles cover subtitles, body text, charts, captions, logos, or footers. Recalculate vertical spacing after title wrapping.
- If required fonts are missing, use this fallback order: Source Han Sans CN, PingFang SC, Microsoft YaHei, Helvetica Neue, Helvetica, Arial, sans-serif.
- If the user requests standard half-size PPT dimensions, scale the original template coordinates and type sizes by `0.5`, then re-render to verify.
