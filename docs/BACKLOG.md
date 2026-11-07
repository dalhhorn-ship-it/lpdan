# Backlog

> Milestones and work items; the dashboard reads this file. Seeded by `choose-path`, ticked off as part of every task's definition of done.

Format: one `## Milestone: <name>` heading per milestone (optional `(target: YYYY-MM-DD)`), then items:
`- [ ]` todo · `- [~]` in progress · `- [x]` done · `- [!]` blocked · `- [-]` dropped. Optional `(S|M|L)` size and `#tags`.
Roadmap tab: item order here is the proposed sequence. Tag technical work `#foundation` (or `#arch`, `#infra`, `#runway`, `#debt`, `#quality`, `#ci`, `#security`, `#process`) to put it in the technical-foundation lane; everything else counts as user value.

## Milestone: M0 — Project set up (target: 2026-11-08)
- [x] Goal agreed: Dan confirms docs/GOAL.md #process
- [x] Operating model chosen (documents-content + software-product static site, L2) #process
- [x] Check script: copy-vs-README snippet match and link check (S) #quality

## Milestone: M1 — Launch the page (target: 2026-11-20)
> Sequence: proposed by product-manager 2026-11-06 — riskiest-first (dashboard visual, then truth of the copy), with deploy pulled forward so Dan can unblock the Cloudflare token and review on a live URL, then campaign/FAQ with TD-001 right behind them, and polish, dogfooding and the final truth pass last.
- [x] Hero: headline, subline and GitHub CTA above the fold on mobile (S); one-click copy lives with the #start commands. AC: Given a phone viewport, when the page loads, then headline, subline and GitHub CTA are visible without scrolling.
- [x] Challenge files 01-07 drafted in public/challenges/ (L). AC: each has goal, skills, danfactory features, time box, steps, done-when, proof.
- [x] Dashboard section with a real screenshot or faithful static mock generated from `python3 scripts/dashboard.py` output (M). AC: shows versions, progress, backlog, tech debt, metrics and the Roadmap tab; labeled as an example if mocked.
- [x] Deploy to Cloudflare via git (S) #infra. AC: live URL; page served from the main branch push.
- [x] Problem, audience, 3-phase flow sections with final copy (M). AC: matches spec; every claim traceable to README/docs.
- [x] Agents, paths, token economy sections (M). AC: 18 agents, 8 paths plus adopt-existing, numbers match the repo.
- [x] 7 habits teaching section (S). AC: each habit names the template feature that enforces it.
- [x] Adopt existing Lovable/Bolt/v0 build + start in 3 commands sections (S). AC: snippets verbatim from README.
- [ ] Dan reviews challenge files and the farm game brief (02) for tone and truth (S) #quality
- [ ] Enable GitHub Issues/Discussions on danfactory with a "challenge" label and `[challenge-N]` title convention (S) #process
- [x] Campaign section on the page: 7 challenge cards, submit steps, help line (M). AC: matches spec section 9b; links to /challenges/*.md work.
- [x] FAQ accordion with details/summary (S). AC: works without JS; answers match challenge 1 file.
- [x] S5: remove the campaign-check gate in tests/check_page.py (TD-001) (S) #quality
- [x] Credits + footer (S). AC: all README-credited projects linked.
- [x] Single index.html: responsive, accessible (semantic HTML, contrast, keyboard), no third-party requests, no JS required (M) #quality. AC: Lighthouse mobile 90+ in all three.
- [x] Open Graph/social preview tags and favicon (S). AC: link preview renders; image is local.
- [ ] Dogfood: run challenges 1 and 2 end to end on a clean machine and fix snags in the files and FAQ (M) #quality
- [x] Landing: latest features copy + clickable dashboard (M, [PRD approved](specs/landing-latest-features.md)). AC: see PRD; budgets green, works without JS.
- [x] Truth pass: Dan reviews all copy; run check script (S) #quality. Delegated by Dan to jenny + reviewer, signed off 2026-11-07: [record](reviews/2026-11-07-truth-pass.md).
- [ ] Launch: remove `X-Robots-Tag: noindex` from public/_headers once GitHub Issues + `challenge` label are confirmed on danfactory (S) #process

## Milestone: M2 — Ideas, not committed (target: )
- [ ] Short screen recording or animated terminal of the 3 phases (M)
- [ ] "Worked example": a small project run through the flow, honest about results (L)
- [ ] Dark/light toggle and print-friendly cheat sheet of the 7 habits (S)
- [ ] Translations (S per language)
- [ ] Challenge 8+ ideas: a data-spreadsheet challenge, a library-cli challenge, an automation-script challenge (M each)
- [ ] Community showcase page of self-submitted projects, with consent (M)
- [ ] Live dashboard demo generated from the repo's own backlog in CI (M) #foundation
- [ ] Cookieless traffic stats, if Dan allows (S) #infra

## Unplanned
