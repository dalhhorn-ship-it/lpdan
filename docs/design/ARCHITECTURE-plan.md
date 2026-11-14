# Architecture: draft changes, build plan and risks

> Split from [ARCHITECTURE.md](ARCHITECTURE.md) to stay within the doc size budget (UPD-3). Same content, no changes.

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
