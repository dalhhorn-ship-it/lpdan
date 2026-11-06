# 0002 — Static single page on Worker static assets, no build step, self-hosted fonts, GPM Keynote design system

> Status: accepted (Dan, 2026-11-06) · Date: 2026-11-06

## Context
GOAL.md and the spec ask for one static, free page with no backend, forms, trackers or third-party requests. It must work without JS, be mobile-first and WCAG AA, deploy via git to Cloudflare, and be maintained by one person for months to years at rigor L2. The page and 7 challenge `.md` files ship unchanged. Dan supplied the GPM Keynote design system (a 1920px slide system: Archivo fonts, square, no shadows, gradients or icons). The spec's build constraints say "system fonts, no CDN".

## Options
1. **Hand-written `public/index.html` with inline CSS, served as Worker static assets (cf_scaffold.py), no build step.** Pros: zero dependencies to run the page; what you edit is what ships; deploy in seconds; matches the spec ("single index.html, inline CSS"). Cons: no templating, so repeated markup (7 cards, 8 FAQ items) is written by hand; design rules are kept by tests, not by a type system.
2. **Static-site generator (Astro/11ty) or a Vite build.** Pros: components and partials; Markdown → HTML for the challenges. Cons: a Node toolchain, lockfile churn and a build in every deploy for one page; it breaks the "challenge files ship unchanged" simplicity; more for Dan to maintain.
3. **Cloudflare Pages instead of a Worker.** Pros: no Worker code at all. Cons: the template's deploy path, `/version` proof-of-deploy and deploy-watcher are built for Workers; it would be the only project off the standard route.

Challenge files: (a) serve the raw `.md` as `text/plain; charset=utf-8` (readable in every browser) plus a `download` link; (b) render to HTML at build time (needs a Markdown dependency and a build step, and makes a second copy that can drift); (c) link to GitHub's rendering (depends on the lpdan repo being public and is a third-party hop). We pick (a).

Fonts: (a) self-host the two latin-subset Archivo woff2 files (56 KB) with the OFL licence; (b) system fonts as the spec says (loses the design system's identity); (c) Google Fonts CDN (third-party request; violates AC 1). We pick (a).

Theme: Midnight only. Daylight is kept for a later print stylesheet; no `prefers-color-scheme` switch (reasons in docs/design/ARCHITECTURE.md).

## Decision
Option 1 with challenges (a), fonts (a) and Midnight only. The GPM Keynote tokens become CSS custom properties named after tokens.json. Slide sizes are translated to a responsive `clamp()` scale with a 16px floor for web text. Hard rules (no shadow, radius, gradient, non-token colours, magenta text under 24px, third-party URLs) are enforced by `tests/check_page.py` and `tests/smoke.mjs`. The Worker is the scaffold's unchanged `/version` + `/health` + ASSETS. `_headers` carries the security headers, the `.md` content type and a temporary noindex.

## Consequences
- Easier: edits are instant to check locally; deploys are a few hundred KB; no framework upgrades.
- Harder: repeated markup is hand-maintained, and the tests catch drift. A spike (S0) must confirm that `_headers` can set the `.md` content type on Workers assets; the fallback is 5 lines in worker/index.ts.
- Spec wording "system fonts" is superseded by "self-hosted fonts, no third-party requests". Dan must approve this.
- Measured: page weight and request budgets (in check_page.py), push-to-live seconds (deploy-watcher), Lighthouse mobile ≥ 90 ×3 at launch.
- Revisit if the site grows beyond one page or needs translations (M2): then a static generator becomes worth its cost.
