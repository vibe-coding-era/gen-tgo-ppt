# Shared Design

Load this file after the user confirms the scene and output format. It contains cross-template rules only; load scenario, template, and visual-style files separately as needed.

## Canvas

- Default size: `26.667 in x 15 in`
- Ratio: `16:9`
- Equivalent PowerPoint point size: `1920 pt x 1080 pt`
- Background rasters are generally `3840 x 2160`; keep full-bleed art at the template canvas ratio.
- If the user requests `13.333 in x 7.5 in`, scale coordinates and type sizes by `0.5`, then visually re-check.
- Static layout checks must apply the same scale to margins, keep-out zones, font thresholds, footer height, and logo areas. A half-size deck is not exempt from render review.

## Brand Palette

- Deep GTLC blue: `#001851`, `#001E64`, `#011E64`, `#012363`, `#02236A`
- Secondary blue: `#003D8C`, `#013F8C`, `#023D8B`, `#033886`, `#043987`, `#05408E`
- Light page background: `#F1F4F9`, `#F2F5FA`
- White page background: `#FFFFFF`
- Body gray: `#535353`
- GTLC orange-red: `#E95529`, theme accent `#EE220C`
- Optional accents: blue `#0076BA`, teal `#00A89D`, green `#1DB100`, yellow `#F8BA00`, magenta `#CB297B`

Keep the deck restrained. Use deep blue, white/light backgrounds, and small orange-red accents as the default language.

## Typography

Use this fallback chain:

```css
"Source Han Sans CN", "Source Han Sans CN Regular", "Source Han Sans CN Bold", "PingFang SC", "Microsoft YaHei", "Helvetica Neue", Helvetica, Arial, sans-serif
```

Observed size ranges:

- Cover / major title: `96-115 pt`, default around `106 pt`
- Section/content title: `64 pt` or `34 pt` for compact content pages
- Body default: `36 pt`
- Small labels/footer/minor text: `18-31 pt`

Prefer fewer words and larger type. If dense content is unavoidable, preserve margins and reduce wording before shrinking below `24 pt`.

## Short Info Rows

- Treat project facts, dates, locations, identities, owners, and other key-value rows as single-line items by default.
- Avoid extra spaces inside Chinese date and phrase runs when they cause awkward wrapping, such as `2026 年 6 月` instead of `2026年6月`.
- If a short info row containing `：` or `｜` wraps unexpectedly, first widen its text box within the safe area, then tighten wording or slightly reduce font size within the readable range.
- Do not rely only on vertical fit for these rows: a two-line key-value row can technically fit but still fails the intended visual rhythm.

## Image + Project Basic Info

- Use this reusable style when one large evidence image or event photo anchors the page and a compact fact list explains the project context.
- Layout: left visual area, right `项目基本信息` block. Keep the right block clear of the top-right GTLC logo and the bottom footer strip.
- The right block should contain the title plus 3-6 rows. Use a small blue dot or equivalent marker and a key-value row such as `大会主题：...`、`时间：...`、`地点：...`、`参会人群：...`、`合作身份：...`.
- Project-info rows are single-line by default. Measure the longest row first, then size every row text box from that longest row.
- In a half-size `13.333 in x 7.5 in` deck, the row text area should normally be at least `3.7 in`; in a full-size template, at least `7.4 in`.
- Prefer compact Chinese date and phrase formatting to preserve the single-line rhythm, for example `2026年6月27-28日｜地点：杭州`.
- Validate by rendering the page and running `scripts/check_pptx_layout.py`; any `PROJECT_INFO_*` or `SHORT_INFO_UNEXPECTED_WRAP` issue must be fixed or explicitly recorded as a deliberate exception.

## Required PPT Pages

- Insert a blank `嘉宾介绍` page immediately after the title/cover page for every PPT/PPTX output.
- Put the agenda/table-of-contents page immediately after `嘉宾介绍` as page 3 whenever an agenda page is used. Body content starts after the agenda.
- Append a final `感谢聆听` page for every PPT/PPTX output.
- Count these pages in the deck plan, final page count, and generation log.
- The `嘉宾介绍` page should not contain helper labels, instructions, or placeholder explanations. If the user supplies guest content, record the exception in the plan and log.
- The agenda page should contain only agenda heading, section numbers, section names, and short structure notes. Keep narrative thesis/problem titles on the first body page, not on the agenda page.
- The final page should contain the exact closing copy `感谢聆听` unless the user explicitly approves alternate closing copy in the plan and log.

## Logo Rules

- Keep GTLC logo placement unless the user uploads a replacement LOGO and confirms replacement.
- When replacing, preserve the uploaded logo's aspect ratio, align to the original logo anchor, and adjust size only enough to avoid distortion or collision.
- Do not replace GTLC logo merely because a LOGO file exists.

## Visual Keep-Out Rules

- Treat template identity art, large conference marks, and full-bleed visual anchors as keep-out zones for text.
- Cover pages that use a left text column plus center/right GTLC master visual must keep all left-column titles, subtitles, dates, speaker names, and metadata inside the declared left text-safe zone.
- If a template or page type lacks a machine-readable keep-out zone, `检查风格` must verify the rendered slide manually and record the result.

## Solid Panel Cover/Closing

- For dark GTLC title and closing pages, use the same centered solid content panel by default.
- Do not apply the solid panel only to the closing page while leaving the title page on the native left-column cover. Keeping a native left-column title page requires explicit user confirmation recorded in the plan, SSOT, and generation log.
- Background treatment: preserve the GTLC background raster at the slide ratio, apply only light blur/dimming, and never stretch or crop it off-ratio.
- Content panel: fully opaque deep blue, recommended `#061C4C` or close GTLC deep blue; no background may show through inside the panel.
- Panel sizing: calculate width from the longest text line plus horizontal padding; calculate height from text stack, separators, and balanced top/bottom padding.
- Typography: explicitly set fonts for all title-page and closing-page runs using the declared fallback chain; do not rely on theme fonts or renderer fallback.
- Text fitting: page title, subtitle, sponsor identity, date, `感谢聆听`, and closing metadata must fit as intended without unexpected wrapping, clipping, or overflow.

## Validation

- Render or preview every slide before delivery.
- Check unexpected line breaks, text overflow, clipped words, placeholder style drift, object collisions, and logo/footer placement.
- Confirm the generated deck has the mandatory blank `嘉宾介绍` page and `感谢聆听` closing page.
- Confirm title and closing pages both have the centered solid panel unless a recorded user-approved exception keeps the native title layout.
- On solid-panel title/closing pages, confirm the panel is visually opaque and has balanced padding above and below the text group.
