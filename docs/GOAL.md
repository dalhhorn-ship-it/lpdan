# Goal

> Status: confirmed by Dan on 2026-11-06.

## Outcome
A single, free, static landing page that teaches vibe coders how to run vibecoding with Claude without the project collapsing as it grows, and shows danfactory (github.com/dalhhorn-ship-it/danfactory) as the way to work and scale. It is a community give-back by Dan, not a product. After reading it, a visitor understands the problem, the 3-phase flow, and the traceability dashboard, and can start in under a minute with copy-paste commands.

## Problem
People start in Lovable, Bolt, v0 or plain Claude and ship fast. Then the project grows and they hit a wall: Claude forgets context, token spend balloons, nothing is tested, nobody can say what was built or why (no traceability), and deploys become chaos. There is no cheap, guided way to add structure without becoming a pro engineer.

## Users
- Primary: vibe coders (makers, designers, founders, PMs who build with AI) who are not necessarily professional engineers, with a prototype or a growing project.
- Secondary: developers who use Claude Code and want a leaner, more measurable setup.
- They already use: Lovable/Bolt/v0, Claude (chat or Claude Code), GitHub, sometimes Cloudflare.

## Artifact type
Document/web page: one static `index.html` (inline CSS, minimal or no JS), hosted on Cloudflare. No backend.

## Constraints
- Every claim must be true to the danfactory repo (README and docs). No invented features, stats, testimonials, user counts or GitHub stars.
- Free and open; Dan is the author (they/them if a pronoun is needed).
- Deploy via git to Cloudflare (static assets). Fast, accessible, mobile-first, works without JS.
- Maintainer: Dan. Copy must be re-checked against the README when the template changes.

## Risk profile
Public internet, no user data, no money, low blast radius. Lifetime: months to years. Rigor: L1 (light), with a manual truth-check of copy against the repo and a link check.

## Acceptance criteria
1. Page is live on a Cloudflare URL and loads with no console errors and no third-party requests.
2. Every code snippet on the page appears verbatim in the repo README (checked by hand or script).
3. Primary CTA links to https://github.com/dalhhorn-ship-it/danfactory and is visible without scrolling on mobile and desktop.
4. A first-time reader can copy the "start in 3 commands" and "adopt existing build" snippets with one click or select.
5. Lighthouse (mobile): Performance, Accessibility, Best Practices each at 90 or above.
6. Credits section names every open-source project listed in the README with a working link.
7. No signup, forms, cookies, analytics trackers or fake social proof anywhere.

## Success signals (measured without trackers)
- GitHub traffic insights: referrers and unique visitors to the repo; clicks from the page (via repo referrer).
- Clones of the repo and uses of the template (GitHub insights), stars as a soft signal only.
- Qualitative: issues, PRs, or messages from people who ran the commands.
No numeric targets are promised on the page.

## Non-goals
- No signup, newsletter, forms or any data collection.
- No analytics trackers or cookie banners.
- No backend, CMS, blog, comments or search.
- No fake social proof, testimonials, logos, counts or stars.
- No full documentation site (link to the repo docs instead).
- No comparison bashing of Lovable/Bolt/v0.

## First milestone
M1: the page live with all sections' final copy (docs/specs/landing-page.md).

## Open questions
- Custom domain, or a *.pages.dev / *.workers.dev URL for now?
- Is Cloudflare's cookieless, server-side traffic analytics acceptable, or strictly nothing?
- Has Dan set danfactory as a GitHub template repository (the page's "Use this template" CTA depends on it)?
- License of danfactory itself (README does not say); the page must not claim one.
- Dan's preferred link for credit (GitHub profile?).
