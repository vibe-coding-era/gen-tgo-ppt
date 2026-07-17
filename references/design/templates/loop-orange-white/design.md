# LOOP Conference Template Design

Load this file when the user chooses `D｜LOOP 大会`, `LOOP Summit`, `LOOP Orange White`, `LOOP 橙白峰会风`, or the template key `loop-orange-white`.

## Selectable Asset

- Template key: `loop-orange-white`
- Display name: `LOOP 大会`
- PPTX: `assets/design/templates/loop-orange-white/tgo-loop-summit-16x9.pptx`
- Preview PDF: `assets/design/templates/loop-orange-white/tgo-loop-summit-16x9-preview.pdf`
- Contact sheet: `assets/design/templates/loop-orange-white/tgo-loop-summit-16x9-contact-sheet.png`
- Source provenance: user-uploaded `TGO_LOOP_16x9_Brand_Template.pptx`
- Asset SHA-256: `8d1ef5e3b388c5e660ce4cd86e3c14b742d488a7b1806ce11edc25da6d00db11`
- Canvas: `13.333 × 7.5 in`, 16:9
- Slides: 7
- Masters: 1

The PPTX above is the only authoring source for the selectable LOOP conference template. Files under `assets/design/branches/loop-orange-white/` are compatibility previews and selector references, not the authoring source.

## Visual Role

LOOP Conference is the orange, white, and deep-blue summit template for AI ecosystem events, keynote talks, sponsor proposals, city chapter events, and event-facing materials. It is directly selectable but does not replace the default `light`, `white`, or `dark` GTLC templates.

## Aliases

Map all of these names to `loop-orange-white`:

- `LOOP 大会`
- `LOOP Summit`
- `LOOP Orange White`
- `LOOP 橙白峰会风`
- `D`

## Visual Direction

- Deep navy: main brand field for section, dark content, and closing pages.
- Orange: vertical or horizontal event accent and section numbering.
- White or cool light gray: title, agenda, and light content canvas.
- Preserve the LOOP summit logo, TGO logo, footer line, spacing rhythm, and native page chrome.
- Do not mix another template's logo, footer, or background into inherited LOOP pages.

## Source Slide Map

| Source slide | Archetype | Use |
| ---: | --- | --- |
| 1 | Cover | Presentation title, subtitle, speaker, organization, year |
| 2 | Keynote topic | Opening question, thesis, guest introduction base |
| 3 | Agenda | Four-part contents or navigation |
| 4 | Section divider | Section number, title, one-sentence judgment |
| 5 | Dark content | Key conclusion, quote, three insights, editable visual area |
| 6 | Light content | Framework, comparison, three-part explanation |
| 7 | Closing | Final `感谢聆听` page |

## Mandatory Page Adaptation

- New or converted PPTX output still follows the Skill structure contract.
- Page 1 inherits source slide 1.
- Page 2 must be a blank `嘉宾介绍` page: duplicate source slide 2, retain brand chrome, clear all other audience-facing content, and set the title to `嘉宾介绍`.
- If an agenda is used, page 3 inherits source slide 3.
- The final page inherits source slide 7 and must replace `Thank You / 谢谢` with the exact closing copy `感谢聆听` unless the user approves an exception.
- Treat source slides as visual frames. Duplicate the closest source slide for additional pages and edit inherited objects instead of rebuilding the brand from scratch.

## Use For

- Global or city-level AI ecosystem and innovation summits.
- Keynote speeches, sponsor benefits, partnership proposals, and event promotion.
- Materials where LOOP summit identity is stronger than the primary blue GTLC frame.

## Avoid For

- Dense board reports, budget sheets, and print-first documents.
- Materials that must remain strictly inside the primary GTLC blue template family.
- Content that cannot be made readable in the available 7 source archetypes without adding a compatible duplicate page.

## Validation

- Preserve the 13.333 × 7.5 inch canvas; apply the Skill's 0.5 layout scale.
- Render every page and compare it with the source contact sheet.
- Check title wrapping, footer/logo collisions, text overflow, and inherited image cropping.
- For template-asset inspection, use `--skip-mandatory-page-check`, native cover/closing exceptions, and visual review because the source file is a seven-archetype template rather than a finished delivery deck.
- For generated deliverables, do not skip the mandatory `嘉宾介绍` and `感谢聆听` checks.

Template-asset static check:

```bash
python scripts/check_pptx_layout.py \
  assets/design/templates/loop-orange-white/tgo-loop-summit-16x9.pptx \
  --skip-mandatory-page-check --no-check-key-page-solid-panel \
  --disable-cover-safe-zone --allow-theme-fonts-on-key-pages \
  --margin-in 0 --footer-in 0 --logo-width-in 0 --logo-height-in 0 \
  --overflow-tolerance 2.0 --large-title-pt 50
```

## Customer Choice Guidance

- `A｜GTLC Light`: default business template
- `B｜GTLC White`: dense report and print-friendly template
- `C｜GTLC Dark`: keynote opening, section, and closing template
- `D｜LOOP 大会`: orange-white/deep-blue summit template
