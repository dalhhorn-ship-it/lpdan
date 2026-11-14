# Architecture: tokens, type scale and section mapping

> Split from [ARCHITECTURE.md](ARCHITECTURE.md) to stay within the doc size budget (UPD-3). Same content, no changes.

## Design-token mapping (Midnight)
| Token | CSS var | Where used |
|---|---|---|
| ground #0B0B2E | `--ground` | page bg, cards on magenta band, code bg on raised sections, text on cyan/yellow |
| ground-raised #17174A | `--ground-raised` | alt sections (Why, Paths, Tokens, Habits), cards, table even rows, code bg on ground |
| ink #FFF | `--ink` | headings, body, kickers, nav |
| ink-muted #B9B9DC | `--ink-muted` | ledes, card text, captions, footer, code comments (replaces `#8a8ab8`) |
| magenta #E6007E | `--magenta` | primary button bg, hero edge block, Flow band, card top borders (first half), table header row, numbers/headlines ≥ 24px |
| magenta-tint #4A0F3F | `--magenta-tint` | badge blocks on ladder cards, "without it" relief panels |
| violet #3D2CE0 | `--violet` | hero second block, card top borders (second half), primary-button hover, closing CTA band |
| lavender #9B7BFF | `--lavender` | step numbers on violet-bordered cards, rigor L1 label |
| cyan #2EE6F5 | `--cyan` | focus ring, streaks, flow arrows (CSS blocks), the takeaway line, "copied" state |
| yellow #F5C400 | `--yellow` | rigor L2 label only (diagram category) |
| on-magenta #FFF | `--on-magenta` | text on magenta and violet |
| rule #2C2C66 | `--rule` | hairlines, ghost-button border, table borders |
| radius-none | none | no `border-radius` anywhere (test-enforced) |

Families: `--font-display: "Archivo Black", "Archivo", Arial, sans-serif`, `--font-sans: "Archivo", Arial, sans-serif`, `--font-mono: ui-monospace, …` (system mono for code; no third font file).

## Responsive type scale and spacing
Slide sizes × ~0.8 at ≥ 1440px wide (content ≤ 1280px), floors chosen for 375px. Web minimum for real text is 16px (the 24px slide floor does not translate); the dashboard mock (role="img") may go to 12px.

| Token (slide) | CSS var | 375px → 1440px | Use |
|---|---|---|---|
| display-xl 120 | `--fs-display-xl: clamp(2.75rem, 1.8rem + 4vw, 6rem)` | 44 → 96 | hero h1 |
| display 96 | `--fs-display: clamp(2.5rem, 1.7rem + 3.4vw, 4.5rem)` | 40 → 72 | closing headline, hero numbers (`.stat`) |
| headline 52 | `--fs-headline: clamp(1.875rem, 1.4rem + 2vw, 3rem)` | 30 → 48 | h2 |
| headline-dense 44 | `--fs-headline-dense: clamp(1.5rem, 1.25rem + 1vw, 2.25rem)` | 24 → 36 | card titles (h3) |
| lead 48 | `--fs-lead: clamp(1.1875rem, 1.05rem + .6vw, 1.625rem)` | 19 → 26 | ledes, hero subline |
| title 32 | `--fs-title: clamp(1.25rem, 1.15rem + .4vw, 1.5rem)` 800 | 20 → 24 | bold list labels |
| body 28 | `--fs-body: clamp(1.0625rem, 1rem + .25vw, 1.1875rem)` | 17 → 19 | body |
| small 24 | `--fs-small: 1rem` | 16 | captions, trust line, footer, badges, copy button |
| kicker 24 | `--fs-kicker: 1rem` 800, uppercase, `letter-spacing: .16em` | 16 | kickers |
Line heights from tokens.json (`--lh-display: .95`, headline 1.02, lead 1.2, body 1.5 on web for readability). Spacing: `--space-3: .75rem`, `--space-4: 1rem`, `--space-8: 2rem`, `--space-12: 3rem`, `--space-section: clamp(4rem, 2.5rem + 6vw, 8rem)` (from space-margin 128), `--space-gutter: clamp(1.25rem, .9rem + 1.5vw, 2rem)`, `--space-footer: 4rem`. Breakpoints (min-width): 600, 900, 1200.

**Kickers are not magenta text at 16px** (4.2:1 fails). Kicker = `--ink` text with a 24×6px magenta bar before it (a block, not text). Magenta text is allowed only ≥ 24px and bold/Archivo Black (h1 emphasis, step numbers, stats, rigor L3, FAQ "+").

## Section → component mapping
| # Section (id) | Slide pattern | Components | Blocks (≤ 3) / streaks |
|---|---|---|---|
| 0 Nav | – | `.brand` (magenta square), links, `.btn--primary` small; solid `--ground`, sticky | – |
| 1 Hero (`top`) | Quote opener | kicker, h1 display-xl (magenta "Without the wall."), lede, primary + ghost buttons, trust line, `.dash` mock + "Example dashboard · sample data" caption | magenta, violet, ground-raised; streaks yes |
| 2 Wall (`wall`) | Card grid / list | section-head, 5 pain rows (magenta Archivo Black numbers ≥ 32px), closer as cyan takeaway line | ground-raised |
| 3 Why (`why`) | Card grid | two lists (for you / not for you) | ground (cards on raised) |
| 4 Flow (`flow`) | Statement (core definition, full-bleed magenta) | 3 `.card` on ground with big step numbers, rigor callout (4 labels), on-demand note | magenta, ground, ground-raised; streaks yes |
| 5 Agents (`agents`) | Data table | `<table>`: magenta header row, alternating rows; note | magenta, ground-raised |
| 6 Paths (`paths`) | Data table | `<table>` 8 rows (name, practice); TDD/slice note | magenta, ground |
| 7 Dashboard (`dashboard`) | Card grid + figure | bullets, trace flow (cyan block arrows), 2 `.code`, `<figure>` screenshot (border `--rule`, no shadow) | ground-raised |
| 8 Tokens (`tokens`) | Hero number | `.stat` ×3 (350 lines, 120k tokens, 40 lines), bullets, research `.callout` | ground |
| 9 Habits (`habits`) | Card grid | `<ol>` 7 cards, 01–07 numbers, feature tag line | ground |
| 9b Campaign (`campaign`) | Card grid + flow | 7 `.ladder-card` (`<ol>`; first 4 magenta tops, last 3 violet), `.badge` (magenta-tint block), localhost note, submit steps `.flow`, `.code`, scoring note, Issues button, help `.callout`, 8 `details.faq` | magenta, violet, magenta-tint |
| 10 Adopt (`adopt`) | Flow | 2 `.code`, ordered list, note | ground-raised |
| 11 Start (`start`) | Flow / staircase | 3 numbered `.code`, "let's start" line, optional template line, handy commands, CTA | ground-raised |
| 12 Closing | Closer (violet CTA statement) | headline + CTA, edge blocks | violet, magenta; streaks yes |
| 13 Credits (`credits`) + footer | – | `<ul>` links; footer text + nav | – |

Streaks (18°, 6–10px, `aria-hidden` `.deco` spans, `overflow:hidden` on the section) only in Hero, Flow and Closing, never behind text.
