# Design Resource Index

Use this index only to route progressive loading after the user's clarification. Do not load every design file by default.

## Always Load

- `references/design/shared/design.md`: canvas, brand colors, typography, required PPT pages, logo rules, and validation rules.

## Load By Scenario

- `references/design/scenarios/gtlc-conference/design.md`: load when the scene is `GTLC 大会`.
- `references/design/scenarios/tgo-daily-sharing/design.md`: load when the scene is `TGO日常活动分享`.

## Load By Template Choice

- `references/design/templates/white/design.md`: load when the user chooses white template or dense/print-friendly content implies it.
- `references/design/templates/light/design.md`: load when the user chooses light template or no template is specified for normal business sharing.
- `references/design/templates/dark/design.md`: load when the user chooses dark template or keynote/opening/high-impact narrative implies it.

## Load By Visual Style Number

- `1`: `references/design/visual-styles/style-01-executive-board/design.md`
- `2`: `references/design/visual-styles/style-02-silicon-valley/design.md`
- `3`: `references/design/visual-styles/style-03-big-tech-keynote/design.md`
- `4`: `references/design/visual-styles/style-04-ai-native/design.md`
- `5`: `references/design/visual-styles/style-05-data-intelligence/design.md`
- `6`: `references/design/visual-styles/style-06-minimal-luxury/design.md`
- `7`: `references/design/visual-styles/style-07-chinese-business/design.md`
- `8`: `references/design/visual-styles/style-08-creative-festival/design.md`

If the user assigns different styles to different pages or sections, load only the selected style files and record the mapping in the deck plan.

## Assets

- Template preview: `assets/design/previews/templates/template-contact-sheet.png`
- Visual style preview: `assets/design/previews/styles/tgo-presentation-design-system-v1.png`
- White PPTX: `assets/design/templates/white/tgo-gtlc-white.pptx`
- Light PPTX: `assets/design/templates/light/tgo-gtlc-light.pptx`
- Dark PPTX: `assets/design/templates/dark/tgo-gtlc-dark.pptx`
