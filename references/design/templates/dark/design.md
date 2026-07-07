# Dark Template Design

Load this file when the user chooses dark template, keynote mode, high-impact narrative, opening/closing, or AI-native stage content.

## Asset

- PPTX: `assets/design/templates/dark/tgo-gtlc-dark.pptx`
- Original source: `GTLC-PPT模版-深色.pptx`
- Visual role: dark blue gradient throughout, keynote-like visual weight.

## Layouts

- `封面`: opening cover.
- `自定义版式`: centered title divider.
- `封面 拷贝` / `封面 拷贝 1`: cover variants.
- `自我介绍 拷贝`: speaker intro.
- `目录 拷贝`: agenda.
- `内容`: default dark content.
- `封底`: closing/thanks.

## Key Positions

- Centered divider title: `x=2.891 y=5.884 w=20.885 h=3.233`
- Cover title variants: around `x=1.800 y=2.544`
- Cover body variants: around `x=1.801 y=6.054`
- Default content title: `x=1.453 y=2.488 w=18.766 h=1.312`
- Default content body: `x=1.487 y=4.200 w=20.648 h=7.849`

## Cover Safety

- Dark GTLC covers often use a left text column and a center/right conference master visual. Treat the center/right master visual as a text keep-out zone.
- For the default `26.667 x 15 in` canvas, keep left-column cover text inside approximately `x=1.5..8.4 in` unless the selected cover variant is explicitly centered.
- For the half-size `13.333 x 7.5 in` canvas, keep left-column cover text inside approximately `x=0.75..4.2 in`.
- The native left-column cover is now an explicit exception path, not the default. Use it only when the user confirms keeping the template-native cover, then record that exception in the plan, SSOT, and generation log.
- If the native left-column exception is approved, subtitle, sponsor identity, date, city, and speaker metadata should fit on one readable line inside that safe zone. If they do not fit, shorten, wrap within the left column and push following metadata down, or switch back to a centered solid-panel cover.
- When sponsor or event text would exceed the left text-safe zone, switch to a centered solid-panel cover instead of reducing safety margins.

## Solid Panel Cover/Closing

- Default for dark GTLC title and closing pages: use this solid-panel treatment on both pages.
- Background: reuse the dark GTLC full-slide raster, apply a light blur/dim treatment, and preserve the original slide aspect ratio.
- Content panel: centered, fully opaque deep GTLC blue (`#061C4C` or close), with a restrained border, shadow, and small orange accent. Do not use translucent glass for the final content area when the user requests solid coverage.
- Half-size cover panel starting point: about `w=8.2 in`, `h=3.2 in`, centered around `y=2.1 in`; resize from measured content if needed.
- Half-size closing panel starting point: about `w=7.4 in`, `h=3.3 in`, centered around `y=2.15 in`; resize from measured content if needed.
- Keep top and bottom padding visually balanced. If a line such as `GTLC 2026 大会赞助结案汇报` does not fit, enlarge the panel before wrapping.

## Use

- Best for keynote, opening, closing, major section transitions, and strong narrative claims.
- Use white text and keep copy sparse.
- Dark pages should carry less text density than white/light pages.
