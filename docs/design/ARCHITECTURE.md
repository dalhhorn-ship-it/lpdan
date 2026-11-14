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

## Design tokens, type scale and section mapping

Moved to [ARCHITECTURE-tokens.md](ARCHITECTURE-tokens.md) (kept under the doc size budget).

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

## Build plan and risks

Moved to [ARCHITECTURE-plan.md](ARCHITECTURE-plan.md).
