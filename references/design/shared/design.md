# Shared Design

Load this file after the user confirms the scene and output format. It contains cross-template rules only; load scenario, template, and visual-style files separately as needed.

## Canvas

- Default size: `26.667 in x 15 in`
- Ratio: `16:9`
- Equivalent PowerPoint point size: `1920 pt x 1080 pt`
- Background rasters are generally `3840 x 2160`; keep full-bleed art at the template canvas ratio.
- If the user requests `13.333 in x 7.5 in`, scale coordinates and type sizes by `0.5`, then visually re-check.

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

## Required PPT Pages

- Insert a blank `嘉宾介绍` page immediately after the title/cover page for every PPT/PPTX output.
- Append a final `感谢聆听` page for every PPT/PPTX output.
- Count these pages in the deck plan, final page count, and generation log.

## Logo Rules

- Keep GTLC logo placement unless the user uploads a replacement LOGO and confirms replacement.
- When replacing, preserve the uploaded logo's aspect ratio, align to the original logo anchor, and adjust size only enough to avoid distortion or collision.
- Do not replace GTLC logo merely because a LOGO file exists.

## Validation

- Render or preview every slide before delivery.
- Check unexpected line breaks, text overflow, clipped words, placeholder style drift, object collisions, and logo/footer placement.
- Confirm the generated deck has the mandatory `嘉宾介绍` and `感谢聆听` pages.
