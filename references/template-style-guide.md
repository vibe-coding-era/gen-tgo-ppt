# TGO/GTLC Template Style Guide

Use this reference when designing PPTX pages or HTML slides in the bundled TGO/GTLC style.

## Source Assets

| Style key | Template asset | Original source file | Visual role |
| --- | --- | --- | --- |
| `white` | `assets/templates/tgo-gtlc-white.pptx` | `GTLC-PPT模版-白底.pptx` | White content pages, dark blue cover/back cover, top-right logo, bottom blue footer strip |
| `light` | `assets/templates/tgo-gtlc-light.pptx` | `GTLC-PPT模版-浅色.pptx` | Pale blue-gray content pages, dark blue cover/back cover, GTLC brand frame |
| `dark` | `assets/templates/tgo-gtlc-dark.pptx` | `GTLC-PPT模版-深色.pptx` | Dark blue gradient throughout, keynote-like visual weight |

Evidence: extracted with `python-pptx`, raw PPT theme XML, media image dimensions, and LibreOffice-rendered previews.

## Canvas

- Size: `26.667 in x 15 in`
- Ratio: `16:9`
- Equivalent PowerPoint point size: `1920 pt x 1080 pt`.
- Background raster assets are generally `3840 x 2160`; keep full-bleed art at the template canvas ratio.
- If the user specifically needs the common `13.333 in x 7.5 in` PPT size, scale coordinates and type sizes by `0.5` and visually re-check.
- Coordinate system below uses inches from the top-left corner.

## Core Colors

| Role | Hex | Notes |
| --- | --- | --- |
| Deep GTLC blue | `#001851`, `#001E64`, `#011E64`, `#012363`, `#02236A` | Dominant dark gradient background sampled from template media |
| Secondary blue | `#003D8C`, `#013F8C`, `#023D8B`, `#033886`, `#043987`, `#05408E` | Footer/logo-adjacent blue accents |
| Light page background | `#F1F4F9`, `#F2F5FA` | Main light-template content background; small sampling/rendering differences are expected |
| White page background | `#FFFFFF` | Main white-template content background |
| Body gray | `#535353` | Body text on light/white masters |
| Black | `#000000` | Small text and some white-page defaults |
| White text | `#FFFFFF` | Titles/body on dark masters |
| GTLC orange-red | `#E95529` / theme `accent5 #EE220C` | Small vertical accent bars and logo ring; use sparingly |
| Theme accent blue | `#0076BA` | Theme `accent1`, useful for links or subtle highlights |
| Theme teal | `#00A89D` | Theme `accent2`, optional secondary highlight |
| Theme green | `#1DB100` | Theme `accent3`, optional status highlight |
| Theme yellow | `#F8BA00` | Theme `accent4`, optional warning/highlight |
| Theme magenta | `#CB297B` | Theme `accent6`, optional highlight |

Avoid turning the deck into a rainbow. The real template language is restrained: deep blue, white/light background, small orange-red accent.

## Typography

Use this fallback chain:

```css
"Source Han Sans CN", "Source Han Sans CN Regular", "Source Han Sans CN Bold", "PingFang SC", "Microsoft YaHei", "Helvetica Neue", Helvetica, Arial, sans-serif
```

Observed template fonts:

- Chinese headings: `Source Han Sans CN Bold` or `Source Han Sans CN Regular`
- Western headings: `Helvetica Neue Medium`
- Theme major font: `Helvetica Neue`
- Theme minor font: `Helvetica`
- Fallbacks observed: `PingFangSC-Regular`, `微软雅黑`

Observed text sizes from XML:

| Use | Size |
| --- | --- |
| Cover / major title | `106 pt` default, with some direct title runs at `96-115 pt` |
| Large title layout | `84-106 pt` depending on layout |
| Section/content title | `64 pt` or `34 pt` for compact content pages |
| Body default | `36 pt` |
| Small labels / footer / minor text | `18 pt`, `24 pt`, `28 pt`, `31 pt` |

For generated content, prefer fewer words and larger type. If dense content is unavoidable, preserve margins and reduce body text before shrinking below `24 pt`.

Point-coordinate hints from the original 26.667 x 15 in canvas:

- Standard content title: about `x=105 pt, y=179 pt`.
- Standard content body: about `x=107 pt, y=302 pt`.
- Intro/agenda accent bar: about `x=90 pt, y=160-170 pt, w=10 pt, h=66 pt`.

## Layout Inventory

### Shared White/Light Layouts

White and light templates have 7 sample slides, 2 masters, and 9 layouts.

| Layout | Use | Key positions |
| --- | --- | --- |
| `封面` | Opening cover | Full-bleed background; title placeholder `x=1.800 y=2.544 w=18.684 h=3.103`; subtitle/body `x=1.801 y=6.054 w=20.792 h=6.403` |
| `1_大标题` | Centered section divider | Title `x=3.806 y=5.688 w=19.055 h=2.748` |
| `大标题` | Section page with body | Title `x=1.268 y=2.145 w=19.055 h=2.748`; body `x=1.268 y=4.900 w=24.131 h=4.873` |
| `自我介绍` | Speaker/self introduction | Chinese label `x=1.747 y=2.226 w≈4.024 h=1.140`; English label `x=1.187 y=3.432 w=4.884 h=0.674`; body `x=1.268 y=4.952 w=24.131 h=4.873` |
| `目录` | Agenda/table of contents | Chinese label `x=1.928 y=2.195 w=3.255 h=1.140`; English label `x=1.187 y=3.328 w≈5.912 h=0.688`; body `x=1.209 y=4.874 w=24.249 h=5.351` |
| `内容1-大字标题` | Content page with large title | Title `x=1.268 y=2.145 w=19.055 h=1.839`; body `x=1.268 y=4.952 w=24.131 h=4.873` |
| `内容2-小字标题` | Default content page | Title `x=1.453 y=2.488 w=18.766 h=1.312`; body `x=1.487 y=4.200 w=20.648 h=7.849` |
| `空内容` | Blank branded page | Keep background/footer/logo only |
| `封底` | Closing / thanks | Full-bleed closing background |

### Dark Layouts

Dark template has 7 sample slides, 1 master, and 8 layouts.

| Layout | Use | Key positions |
| --- | --- | --- |
| `封面` | Opening cover | Full-bleed dark GTLC cover |
| `自定义版式` | Centered title divider | Title `x=2.891 y=5.884 w=20.885 h=3.233` |
| `封面 拷贝` / `封面 拷贝 1` | Cover variants | Title around `x=1.800 y=2.544`; body around `x=1.801 y=6.054` |
| `自我介绍 拷贝` | Speaker intro | Same label/body pattern as light/white but on dark background |
| `目录 拷贝` | Agenda | Same label/body pattern as light/white but on dark background |
| `内容` | Default dark content | Title `x=1.453 y=2.488 w=18.766 h=1.312`; body `x=1.487 y=4.200 w=20.648 h=7.849` |
| `封底` | Closing / thanks | Full-bleed dark GTLC closing background |

## Brand and Image Placement

- Full-bleed background images: `x=0 y=0 w=26.667 h=15.000` unless the template uses a tiny `x=-0.014` bleed.
- White template footer strip: `x=0 y=13.388 w=26.667 h=1.612`.
- White template top-right logo: `x=22.153 y=0.728 w=3.465 h=2.852`.
- Shared slide-number placeholder appears near `x=13.152 y=11.328 w=0.354 h=0.361`; it is not visually prominent and should not drive layout decisions.
- Keep GTLC logo in the upper-right on content pages. Do not move it into the body content zone.
- In the light and dark templates, many logo/footer/line elements are baked into full-slide background images; treat them as background assets unless the user asks for editable reconstruction.
- Keep small orange-red accent bars near section labels; do not turn them into large blocks.
- Use user images inside the body area unless the chosen template layout already calls for full-bleed imagery.

## Slide Mapping Heuristics

| Source content | PPT layout |
| --- | --- |
| Deck title, event opening | `封面` |
| Major chapter heading with little/no body | `1_大标题` or dark `自定义版式` |
| Speaker bio / self intro | `自我介绍` |
| Agenda / table of contents | `目录` |
| Short content with strong title | `内容1-大字标题` |
| Normal content, bullets, diagrams | `内容2-小字标题` or dark `内容` |
| Visual-only pause or transition | `空内容` |
| Thanks / contact / end page | `封底` |

For HTML output, mirror these same layout names as CSS classes or data attributes.

## Gotchas

- Layout names such as `封面`, `封底`, and copied variants can repeat or hide different masters. Use visual role, placeholder geometry, and background asset rather than name alone.
- Theme colors are not a complete brand specification; the key blue gradients come from raster media.
- Cover and closing text/logos are often baked into backgrounds. Replacing them may require image editing or approved replacement assets.
- Dark pages should carry less text density than white/light pages.
- LibreOffice preview can differ when fonts are missing; OpenXML geometry and rendered visual QA together are the best evidence.
