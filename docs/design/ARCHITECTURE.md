# Architecture: danfactory landing page

> Proposed (awaiting Dan's approval), 2026-11-06. Technical shape of the static landing page: files, CSS token layer, sections, accessibility, performance, tests, deploy, build slices. Decision record: docs/decisions/0002-static-page-worker-assets-no-build.md.

## Context
One static, mobile-first page (docs/specs/landing-page.md) plus 7 challenge files. No backend, forms, trackers or third-party requests; works without JS; WCAG AA; rigor L2 (Dan, 2026-11-06). Built in the GPM Keynote design system (design/gpm-keynote/), which is a 1920px slide system and needs a web translation. Deploys via git to a Cloudflare Worker that serves static assets.

## File layout
```
public/                      # the only thing deployed (Worker static assets)
  index.html                 # single page, inline <style> (token layer -> base -> components -> sections)
  copy.js                    # ~1 KB progressive enhancement: copy buttons only (moved out of inline for CSP)
  _headers                   # security headers, text/plain for challenge .md, noindex until launch
  fonts/archivo-latin.woff2, archivo-black-latin.woff2, OFL.txt   # self-hosted, latin subset, licence added
  dashboard/index.html       # dated snapshot of this repo's own dashboard + back link; written by scripts/site_dashboard.py
  favicon.svg                # tiny SVG favicon (replaces the inline data: URI)
  img/og.png                 # 1200x630 social preview (~15 KB), generated once with Playwright; absolute og:image URL
  challenges/01-setup.md … 07-retro-upstream.md   # source of truth, shipped byte-for-byte
worker/index.ts              # cf_scaffold.py template, unchanged: /version (git sha), /health, else ASSETS
wrangler.jsonc               # cf_scaffold.py: assets ./public, run_worker_first [/version,/health]
package.json, package-lock.json  # wrangler + playwright (pinned 1.63.0) devDependencies; "test" = static check
.github/workflows/deploy-cloudflare.yml  # from templates/, one fix (see Deploy)
tests/check_page.py          # stdlib static checks (< 1 s)
tests/smoke.mjs              # Playwright smoke against a tiny local static server (< 10 s)
tests/fixtures/danfactory-README.md  # pinned copy of the danfactory README the snippets are checked against
```
No build step, no framework, no CSS preprocessor. One Worker.

## CSS architecture
One inline `<style>` in index.html (spec: inline CSS; one request; ~15 KB). Ordered blocks, no `@layer` needed (no specificity fights in one hand-written file):
1. **Tokens** (`:root`): the only place hex colours appear; names = tokens.json names. Type scale and spacing vars.
2. **Base**: reset, body, links, focus ring, headings, `code`/`pre`, `.wrap`, `section`.
3. **Components**: `.kicker`, `.section-head`, `.btn--primary|--ghost`, `.card`, `.table`, `.code`+`.copy`, `.stat`, `.flow`, `.callout`, `.ladder-card`, `.badge`, `details.faq`, `.deco` (edge blocks + streaks), `.dash` (mock).
4. **Sections**: only layout per `#id` (grid columns, ordering). No colours here except picking a token.

No inline `style=""` attributes (move the two in the draft to classes). `color-scheme: dark`.

### Daylight theme: not used in M1
Midnight only; no `prefers-color-scheme`. Reasons: the README makes Midnight the default stage and Daylight a print/handout theme; the spec cuts the theme toggle to M2; a second theme doubles contrast QA, and Daylight cyan `#0094A8` on white is 3.6:1 (fails body text). Light values stay in tokens.json for an M2 `@media print` cheat sheet.

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

## Changes needed in the current draft (public/index.html)
1. Remove offset `box-shadow` on `.dash` (l.75, 104) and `figure img` (l.192, 196); use a `--rule` border.
2. Magenta text below 24px: `.eyebrow` 15px (l.38) → kicker with bar; `.trace i` 14px (l.190) → cyan block arrows.
3. Hover `#ff1a93` (white on it is 3.6:1, fails) → `--violet` background.
4. Non-token colours `--code #06061c`, `#e9e8f5`, `#8a8ab8`, `color-mix()` + `backdrop-filter` nav → tokens, solid nav.
5. Rename vars to token names (`--navy` → `--ground`, `--mag` → `--magenta`, …).
6. Real text under 16px (trust 15, figcaption 15, `.lvl .tb` 13, badge 12, `.team small` 13, `.path code` 15, `.habits small` 13, copy button 13, `.trace` 14, `.phase .out` 14) → `--fs-small`.
7. Badge in yellow (l.240) → magenta-tint block; yellow is diagram-only.
8. Glyphs outside the latin font subset: `→` (11×) and `●` fall back to Arial. Use CSS block arrows or drop them; `↑` (U+2191) is in the subset.
9. Campaign markup (cards, submit, help, FAQ) is missing; CSS for it exists.
10. Not in spec copy, needs Dan: closing "Give your next project rails, not rules", "Share feedback" button, the dashboard caption paragraph (l.475).
11. Snippet not verbatim: `dashboard.py --open   #` has 3 spaces; the README has 4.
12. Inline `<script>` → `copy.js` (CSP `script-src 'self'`); add an `aria-live` "Copied" status.

## Accessibility plan (contrast pairs computed, WCAG 2.x)
| Pair | Ratio | Rule |
|---|---|---|
| ink / ground · ground-raised | 19.1 · 16.7 | any size |
| ink-muted / ground · ground-raised · magenta-tint | 10.0 · 8.8 · 7.7 | any size |
| on-magenta / magenta | 4.50 (no margin) | any size; never a lighter magenta |
| on-magenta / violet | 8.0 | any size |
| magenta / ground · ground-raised | 4.2 · 3.7 | ≥ 24px bold only (large text) |
| cyan / ground · ground / cyan | 12.5 | any size; cyan blocks take ground text |
| ground / yellow · yellow / ground | 11.6 | labels only |
| lavender / ground · ground-raised | 6.1 · 5.3 | any size |
| rule / ground | 1.5 | decoration only, never the only cue |
Plus: skip link, landmarks (`nav`, `main`, `footer`), one h1 and no heading skips, `<table>` with `<th scope>`, FAQ via `<details>/<summary>`, 44px targets, cyan 3px focus ring, mock is `role="img"` with an aria-label that says "sample data", screenshot alt text, `prefers-reduced-motion` turns off smooth scroll, language `en`.

## Performance budget (test-enforced file sizes)
| Item | Budget |
|---|---|
| index.html (inline CSS) | ≤ 64 KB raw (draft 44 KB) |
| copy.js | ≤ 2 KB |
| fonts (2 woff2, latin subset, both `preload`ed, `font-display: swap`) | ≤ 60 KB total (now 56 KB) |
| dashboard screenshot (`loading="lazy"`, width/height set) | ≤ 120 KB (now 108 KB) |
| public/ without challenges | ≤ 300 KB; ≤ 6 requests on first load; 0 third-party |
Hero LCP is text (the mock is CSS, not an image). Target Lighthouse mobile ≥ 90 ×3 (AC 5), measured by hand on the preview URL.

## Content truth
- Copy source = the spec; facts = danfactory README + docs. The README is pinned in tests/fixtures/danfactory-README.md.
- `check_page.py` proves the snippets match; `check_page.py --upstream` (manual, uses the network) diffs the fixture against the live README whenever the template changes.
- Commands that are not in the README (`dashboard.py --print`, `metrics.py report`, `python3 -m http.server 8000`, `python3 --version`) are on an allowlist, each tied to the source file it must appear in (CLAUDE.md, the README, the spec).
- Human truth pass: `reviewer` (claims vs repo), then `jenny` (spec acceptance criteria), then Dan.

## Test strategy
`commands.test` = `python3 tests/check_page.py && node tests/smoke.mjs`. Each prints `N passed, M failed` so metrics.py records counts. Total < 10 s (budget 30 s). Inner loop / pre-push `commands.test_affected` = `python3 tests/check_page.py` (< 1 s).

**check_page.py (stdlib: html.parser, re, pathlib)**
1. Snippets: every `.code pre` equals a line of a README fenced block (or an allowlisted source); `data-copy` equals the pre text minus the trailing `# comment`.
2. Links: every `#anchor` has an id; every relative href/src exists under public/; external hrefs are an exact allowlist (danfactory repo + /issues, 5 credit URLs); no external `src`, `url(http`, `@import`; no `<form>`, `<input>`, `<iframe>`, inline `on*=`, inline `<script>`, `document.cookie`, `fetch(`.
3. Campaign: 7 challenge files exist with the expected names; each is linked twice (read + `download`), in order 01–07; each contains its own `[challenge-N]`; README commands quoted in them are verbatim; exactly 8 `details.faq`.
4. Design rules in `<style>`: no `box-shadow`/`text-shadow` (except `none`), no `border-radius` ≠ 0, no `*-gradient(`, `backdrop-filter`, `drop-shadow`; hex colours only in `:root` and only tokens.json dark values; px font-sizes < 16 only under `.dash`.
5. HTML basics: `lang`, charset, viewport, title, description; one h1; no heading skips; unique ids; img alt + width + height; `button type`; balanced tags.
6. Glyphs: every character in the page is inside the Google "latin" subset range.
7. Size budgets (table above). Banned phrases: "trusted by", "stars", "testimonial".

**smoke.mjs (Playwright 1.63, Chromium, a node:http server over public/ serving .md as text/plain)**: viewports 375×667 and 1440×900 with no horizontal overflow; h1, subline and primary CTA inside the first viewport; no console errors; no request leaves the origin; JS-off context: all content present, copy buttons hidden, FAQ opens; JS-on: copy writes `data-copy` to the clipboard; every element with magenta text is ≥ 24px and bold/Archivo Black; cyan/yellow backgrounds carry ground text; challenge links return 200 text/*; first Tab focuses the skip link.

**Not automated**: Lighthouse (manual, on the preview URL), external link liveness (`check_page.py --online`, manual), block-colour count per section (ui-comprehensive-tester checklist).

## Deploy
1. Dan: Cloudflare account and workers.dev subdomain; API token from the "Edit Cloudflare Workers" template → GitHub secret `CLOUDFLARE_API_TOKEN` on dalhhorn-ship-it/lpdan (`CLOUDFLARE_ACCOUNT_ID` only if needed, Account ID not Zone ID); branch protection on `main` requiring check `test`.
2. `python3 scripts/cf_scaffold.py --name <worker>` → wrangler.jsonc, worker/index.ts, workflow, package.json, lockfile, factory.json deploy block. Then add playwright and set `"test": "python3 tests/check_page.py"` (the fast required PR check; the full suite runs in ci.yml via metrics.py).
3. **Workflow fix:** `paths-ignore: "**/*.md"` and the `changes` regex `\.md$` would skip deploys of public/challenges/*.md. Change them to root-level only: `"*.md"` and `'^(docs/|metrics/|\.claude/)|^[^/]+\.md$'`.
4. ci.yml: add setup-node, `npm ci`, `npx playwright install chromium` before "Project tests".
5. Preview: each PR → `pr-<n>-<worker>.<subdomain>.workers.dev` (works after the first merge creates the Worker). Production: merge to `main` → `<worker>.<subdomain>.workers.dev`.
6. After every push: `deploy-watcher` in the background waits on `/version` = sha (scripts/wait-for-url.sh), checks `/health` and the content-type of a challenge `.md`, and records `metrics.py deploy --seconds`.
7. `_headers` sends `X-Robots-Tag: noindex` until the launch slice removes it. Rollback = `git revert` + push.

## Build plan (vertical slices → BACKLOG)
| # | Slice | BACKLOG item(s) | Who |
|---|---|---|---|
| S0 | Spike, 1 h time box: (a) `wrangler dev`: `_headers` can set `text/plain; charset=utf-8` on `/challenges/*.md` and the CSP applies (fallback: add `/challenges/*` to `run_worker_first` and set the header in worker/index.ts); (b) smoke.mjs runs with the local browsers and in CI within budget | – | main agent |
| S1 | Test harness + token layer: check_page.py, smoke.mjs, README fixture, draft fixes 1–8 and 11–12 → green | M0 check script; M1 "Single index.html…" (part) | developer; test-runner on failure |
| S2 | Walking skeleton live: scaffold, `_headers`, workflow fix, ci.yml node step, first merge → workers.dev (noindex) | M1 Deploy via git | main agent; Dan adds secret; deploy-watcher |
| S3 | Hero + nav + copy.js, above the fold at 375px | M1 Hero | developer; ui-comprehensive-tester |
| S4 | Dashboard section (mock caption, screenshot, trace, snippets) | M1 Dashboard | developer; ui-comprehensive-tester |
| S5 | Campaign: ladder, submit, help line, FAQ | M1 Campaign, FAQ | developer; ui-comprehensive-tester |
| S6 | Content sections to spec: wall, why, flow, agents/paths tables, tokens, habits | M1 Problem/flow, habits, agents/paths/tokens | developer |
| S7 | Adopt + Start + closing + credits + footer (verbatim) | M1 Adopt/start, credits/footer | developer |
| S8 | OG tags + local og.png + favicon (needs production_url) | M1 Open Graph | main agent |
| S9 | Launch: truth pass, Lighthouse ×3, remove noindex, record URL in factory.json | M1 Truth pass | reviewer → jenny → Dan; doc-keeper |
Dan's own items are separate: challenge review, dogfooding challenges 1–2, the Issues "challenge" label.

## Risks and open questions
- `.md` content-type and `_headers` on Workers static assets are not yet tested (S0a). Fallback is 5 lines in the Worker.
- Spec text says "system fonts"; the design system needs Archivo. We self-host it, so there are still no third-party requests. Needs Dan's OK (ADR 0002).
- Resolved: Dan set rigor L2 on 2026-11-06 (see OPERATING-MODEL).
- Hero fit at 375px with a 44px h1 is tight. The smoke test guards it; fallback is a 40px floor.
- The first merge publishes the draft on workers.dev. Mitigation: noindex, and don't share the URL before S9.
- README drift after template changes: run `--upstream` on every template release.
- Open: Worker name (it becomes the URL), closing-section copy, a "Challenges" nav link (not in spec), og image now or after launch.
