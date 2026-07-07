# TGO/GTLC Conversion Workflows

Use this reference when the source material is PPT, PDF, Markdown, HTML, or pasted content.

## Shared Steps

1. Introduce yourself: `我是 TGO鲲鹏会 PPT 生成 Skill，可以生成 PPT 格式和 HTML 格式。`
2. Ask the scenario with numeric options: `1. GTLC 大会` and `2. TGO日常活动分享`.
3. If the source is PPT/PDF, ask the processing mode with numeric options: `1. 修改内容并套模板` and `2. 只套模板不改内容`.
4. If the user uploaded a LOGO, ask whether to replace the GTLC LOGO with it.
5. Ask the output format with numeric options: `1. PPT` and `2. HTML`.
6. Show the eight-style preview image from `assets/design/previews/styles/tgo-presentation-design-system-v1.png`, then ask the user to choose style numbers. Accept one number, multiple numbers, or per-page/per-section mapping.
7. Read the source content end to end before asking detailed design questions.
8. Summarize the content in plain language: core message, audience, key sections, weak spots, likely slide density, and any missing context.
9. Ask whether to optimize content. Optimization can include clearer titles, section reordering, deduplication, density reduction, stronger story arc, bilingual title treatment, or speaker-note suggestions. If the user chose `只套模板不改内容`, do not optimize wording or structure.
10. Clarify event metadata, fidelity, image policy, logo replacement, and per-page style assignments only when needed.
11. Extract source structure into a neutral outline: deck title, sections, slide titles, body blocks, images, charts/tables, speaker notes, and closing content.
12. Produce a deck plan for user confirmation before generating the deck. Include total slide count and each slide's outline. For PPT output, include a blank `嘉宾介绍` page immediately after the title page and a final `感谢聆听` page.
13. Map each unit to the closest GTLC layout from the selected template `references/design/templates/*/design.md` file and to the selected visual style `references/design/visual-styles/*/design.md` file.
14. Create a generation log in the user's current working directory before creating the sample page.
15. Generate one representative sample page and wait for user confirmation.
16. Generate PPTX from the chosen template asset or generate HTML with equivalent CSS.
17. Render/preview every slide and fix visual issues before delivery, including style drift, unexpected line breaks, overflow, and logo/footer collisions.
18. Run independent style review with `检查风格`, then independent wording/content review with `检查文字`.
19. Update the generation log with outputs, checks, fixes, and deferred issues.

## Required Approval Gates

### Gate 0: Progressive Design Loading

Before detailed design work, read `references/design/index.md` and load only:

- `references/design/shared/design.md`
- The confirmed scenario `design.md`
- The selected or inferred template `design.md`
- The selected visual-style `design.md` files

Do not load all scenario, template, and visual-style files just because they exist.

### Gate 1: Content Discussion

Before this gate, complete the scene, format, and style selection menus. Use plain numeric options and allow the user to respond with only a number.

If the source is PPT/PDF, first ask:

```text
你希望我 1. 修改内容并套模板，还是 2. 只套模板不改内容？
```

If the user chooses `只套模板不改内容`, preserve wording, slide order, slide intent, figures, and speaker-note meaning unless a minimal split is required to avoid overflow.

After reading the source, ask:

```text
我已读完内容。是否需要我先优化叙事结构、标题表达、页数密度或删减合并？
```

If the user asks for optimization, present a short optimization proposal before the deck plan. If the user declines, preserve content intent and wording unless splitting is needed for readability.

### Gate 2: Deck Plan

Before generating PPTX or HTML, present a table like:

| Page | Layout | Title | Purpose | Key content | Assets/notes |
| --- | --- | --- | --- | --- | --- |
| 1 | `封面` | ... | Opening | ... | Template background |

The plan must include total page count and the selected design-system style for every slide or section. Wait for user confirmation before making the deck.

For PPT output, the plan must include:

- Page 2 as a blank `嘉宾介绍` page immediately after the title page.
- The final page as `感谢聆听`.

### Gate 3: One-Page Sample

Before creating the sample, create a log file in the user's current working directory:

```text
gen-tgo-ppt-生成日志-YYYYMMDD-HHMMSS.md
```

Record the source, scene, format, style choices, template, content optimization decision, and confirmed deck plan. Use `scripts/create_generation_log.py` if convenient, but only from the user's current directory.

After plan approval, create one representative sample page first. Prefer:

- The most common content slide if the deck is mostly informational.
- The riskiest dense slide if readability is the main concern.
- A cover or section page only when brand tone is the main risk.

Show the sample as a rendered preview when possible. Ask the user to confirm style, density, and content treatment before generating the full deck.

### Gate 4: Independent Reviews

After full generation:

1. Inspect every rendered slide yourself first, preferably using screenshots/contact sheets. Fix template drift, unexpected line breaks, text overflow, clipped words, object collisions, logo/footer placement, and the mandatory `嘉宾介绍`/`感谢聆听` pages.
2. Launch a subagent named `检查风格` if available. Its scope is visual only: template fidelity, colors, fonts, layout positions, logo/footer/background placement, contrast, overflow, unexpected line breaks, and page rhythm.
3. Launch a subagent named `检查文字` if available. Its scope is wording and content only: Chinese expression, typos, source fidelity, logic, missing context, factual consistency, title accuracy, density, duplicated points, and alignment with any approved optimization.
4. Fix blocking findings before final delivery, or clearly record deferred findings with the user's approval.

If subagents are unavailable, do two separated self-review passes and disclose that limitation.

When generation itself is delegated to a worker, name that subagent `生成内容`. Do not use English subagent names in user-facing output.

Update the generation log before final delivery. The final response must include the log path.

## PPTX to PPTX

- Use the chosen template PPTX as the base deck.
- Ask whether to modify content or only apply the template before changing any wording or structure.
- Insert a blank `嘉宾介绍` page immediately after the destination title page.
- Append a final `感谢聆听` page.
- Preserve source slide intent, not necessarily original decoration.
- Reuse original images/charts only when they remain readable inside GTLC body zones.
- Convert source title slides to `封面`, agenda slides to `目录`, section dividers to `1_大标题`/`自定义版式`, normal slides to `内容2-小字标题`/`内容`.
- If the source already has strong brand constraints, ask whether to merge brands or fully restyle to GTLC.
- Validate by comparing source page count and checking that every source slide has a mapped destination or an explicit merge/drop decision.

## PDF to PPTX

- Ask whether to modify content or only apply the template before extracting or rewriting content.
- If the user chooses `只套模板不改内容`, preserve PDF text order and page meaning; recreate editable text only when reliable, otherwise use extracted images or conservative text blocks.
- If the user chooses `修改内容并套模板`, extract the PDF structure, propose content edits, and wait for approval before rewriting.
- Insert the mandatory blank `嘉宾介绍` page after the title page and append the final `感谢聆听` page.
- Render the PDF pages and the generated PPTX pages to compare content coverage and spot missing text, clipped graphics, or unwanted wraps.

## Markdown to PPTX

Suggested mapping:

| Markdown pattern | Destination |
| --- | --- |
| First `#` | Cover title |
| Top metadata block | Cover subtitle/date/speaker |
| `##` | New section or slide title |
| `###` | Subsection title inside current section |
| Bullet lists | Body placeholder |
| Images | Body image zone; ask before full-bleed use |
| Tables | Simplify or split across slides |
| Code blocks | Use high-contrast monospaced blocks only when essential |

For dense Markdown, split by idea rather than by heading alone. Prefer 1 message per slide.

## HTML to PPTX

- Parse semantic structure first: headings, sections, articles, lists, tables, figures, captions.
- Ignore most decorative CSS unless the user asks for high fidelity.
- Preserve tables/charts only when readable; otherwise summarize or split.
- Ask before screenshotting entire HTML pages into slides. It usually hurts editability.
- If the source HTML is already a slide deck, keep slide boundaries and restyle each slide.

## PPT/PDF/Markdown/HTML to HTML Slides

Generate a standalone HTML file or app that uses:

- A fixed 16:9 slide surface.
- CSS variables for `--gtlc-blue-deep`, `--gtlc-blue`, `--gtlc-bg-light`, `--gtlc-orange`, `--gtlc-text`, and `--gtlc-muted`.
- Template classes such as `.slide.cover`, `.slide.section`, `.slide.intro`, `.slide.agenda`, `.slide.content`, `.slide.blank`, `.slide.closing`.
- The same logo/footer/background positions described in the selected template `design.md`.
- Print styles that preserve one slide per page when possible.

For web/mobile viewing, allow the slide canvas to scale down while preserving the 16:9 ratio. Do not reflow slide internals into a normal article unless the user explicitly asks for a web page instead of an HTML slide deck.

## Clarification Checklist

Ask only the relevant subset:

- 需要 PPTX、HTML，还是两者？
- 场景是 `1. GTLC 大会` 还是 `2. TGO日常活动分享`？
- 如果上传的是 PPT/PDF：希望 `1. 修改内容并套模板`，还是 `2. 只套模板不改内容`？
- 如果上传了 LOGO：是否用上传的 LOGO 替换 GTLC LOGO？
- 格式是 `1. PPT` 还是 `2. HTML`？
- 八大视觉风格选择哪个数字？是否需要不同页使用不同风格？
- 希望使用白底、浅色、深色，混用深色封面/章节页和浅色内容页，还是我根据内容自动选择？
- 输出更重视保留原文件结构，还是重排成 TGO/GTLC 演讲效果？
- 是否替换会议年份、城市、主标题、副标题、讲者、日期？
- 原图、图表、Logo 是否全部保留？有无必须删除或替换的图片？
- 内容是否允许拆分、压缩、改写标题？
- 是否希望我先优化内容：重排结构、压缩页数、强化标题、合并重复点、补充讲述逻辑？
- 是否需要双语标题或英文小标题？
- 是否面向大屏演讲、线上分享、打印、还是网页浏览？
- 是否必须使用标准 `13.333 x 7.5 in` 页面尺寸？如果是，需要整体缩放并重新校验。

## Quality Bar

The result should feel like it came from the GTLC template, not like content pasted onto a generic blue deck. Prioritize:

- Consistent brand frame.
- Large, readable type.
- Sparse orange-red accents.
- Strong contrast.
- Clean mapping of source structure to GTLC layout roles.
- No body text colliding with the top-right logo or bottom footer.
- No unexpected line breaks, clipped text, overflow, or style-mismatched placeholders on any slide.
- For PPT output, Page 2 is the blank `嘉宾介绍` page and the final page is `感谢聆听`.
- Uploaded replacement LOGO is used only after confirmation, consistently and without distortion.
- User-approved plan and sample page before full deck generation.
- Independent `检查风格` and `检查文字` review evidence before final delivery.
- A generation log in the current working directory with sample/final output paths and review records.
