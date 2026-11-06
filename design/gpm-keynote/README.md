# GPM Keynote

Loud, square, midnight-and-magenta. A keynote system for big statements with very few words — first used for the GPM offsite keynote “Everything Must Change” (November 2026).

## Content fundamentals
- **One idea per slide.** The headline is the argument (an action title), not a topic label: “We delivered *despite* our foundation”, not “Foundation”.
- **Few words.** Headline ≤ 12 words. Supporting text ≤ 3 lines. Everything else goes in speaker notes.
- **Storyline first.** Structure decks pyramid-style (Minto / SCQA): situation, complication, question, answer; one governing thought; 10–15 main slides; detail goes to an appendix.
- **Uppercase for display, sentence case for text.** Display styles are uppercase; `lead`, `title`, `body`, `small` are sentence case. Kickers are uppercase and tracked.
- **Numbers are heroes.** A single figure (5 CRMs, 8 GW, 3×) is set at `display` size or larger, on a `magenta` block or in `magenta` on `ground`.
- **Voice:** direct, first-person plural (“we”), no jargon soup, no hedging. Curly quotes and apostrophes.

## Visual foundations
- **Canvas:** 1920 × 1080, `space-margin` (128px) on all sides; a footer/source line sits pinned at `space-footer` from the bottom, set in `small` / `ink-muted`.
- **Ground:** `ground` (midnight) is the default stage; the Daylight theme exists for print and handouts.
- **Identity colour:** `magenta` carries the statements. Full-bleed magenta slides are reserved for the opening quote and the core definition; `violet` takes the one call-to-action statement slide.
- **Blocks:** square slabs (`radius-none`) in `magenta`, `violet`, `ground` and `magenta-tint`, bleeding off the right or top edge on title, statement and closing slides. Never more than three block colours on one slide.
- **Light streaks:** the one pattern — thin diagonal stripes (rotated 18°, 6–10px wide) in `cyan`, `magenta` or white, crossing the edge blocks. Title, statement and closing slides only; never behind body text.
- **Signal:** `cyan` marks direction and the takeaway — arrows, “we are here” / “next step” labels, the one line the audience should remember.
- **No** shadows, gradients, rounded corners, icons or photos.

## Slide patterns
Every content slide opens with the same header block at the top margin: a `kicker` in `magenta`, then a `headline` (or `headline-dense` on appendix slides), `space-3` apart.

| Pattern | Use | Build |
| --- | --- | --- |
| **Quote opener / closer** | First and last slide | Magenta (opener) or ground (closer) slide; quote in `display`, attribution or ask in `lead`; edge blocks + streaks on the right third. |
| **Statement** | A pivot or definition | Kicker, then `display-xl` sentence; one key word in `magenta`; optional `lead` line in `ink-muted`. |
| **Card grid** | Wins, shifts, steps (3–8 items) | `ground-raised` cards, 6px top border in `magenta` (first half) or `violet` (second half); kicker label, short `headline-dense` result, one `body` line. Big step numbers (`01`) in Archivo Black. |
| **Hero number** | One striking figure | Two or three tall blocks side by side, the number at 240px, label as uppercase `title`. |
| **Flow / staircase** | Process or maturity | Steps in a row, `space-4` apart; done steps `magenta`, current or next outlined in `cyan`, future in `ground-raised`. A rule underneath groups steps (“where Product must lead”). |
| **Data table** | Framework mappings, appendix detail | `magenta` header row, rows alternating `ground-raised` / `ground`, `small`–`body` size, column widths set explicitly. |
| **Appendix** | Recreated frameworks and sources | Kicker “Appendix A · …”, `headline-dense`, 96px top margin, dense table or column layout, source line in the footer, full detail in speaker notes. |

## Type
Archivo Black for display, Archivo (400 / 700 / 800) for text — both from Google Fonts. Nothing on a slide is smaller than 24px. Display leading 0.95–1.05; kickers tracked 4px.

## Iconography
None. Shapes, blocks and numbers do the work; arrows are plain `cyan` block arrows.

## Contrast notes
- `ink` on `ground`, `on-magenta` on `magenta` and `violet` pass 4.5:1.
- `magenta` text on midnight `ground` is about 4:1 — use it only at 24px bold and up (kickers, headlines, numbers).
- `yellow` and `cyan` blocks take `ground` (dark) text, never white.
