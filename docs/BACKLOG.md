# Backlog

> Milestones and work items; the dashboard reads this file. Seeded by `choose-path`, ticked off as part of every task's definition of done.

Format: one `## Milestone: <name>` heading per milestone (optional `(target: YYYY-MM-DD)`), then items:
`- [ ]` todo · `- [~]` in progress · `- [x]` done · `- [!]` blocked · `- [-]` dropped. Optional `(S|M|L)` size and `#tags`.
Roadmap tab: item order here is the proposed sequence. Tag technical work `#foundation` (or `#arch`, `#infra`, `#runway`, `#debt`, `#quality`, `#ci`, `#security`, `#process`) to put it in the technical-foundation lane; everything else counts as user value.

## Milestone: M0 — Project set up (target: 2026-11-08)
- [ ] Goal agreed: Dan confirms docs/GOAL.md (draft) #process
- [ ] Operating model chosen (documents-content + software-product static site, L1) #process
- [ ] Check script: copy-vs-README snippet match and link check (S) #quality

## Milestone: M1 — Launch the page (target: 2026-11-20)
Order is riskiest-first: truth of the copy and the dashboard visual are the risks.
- [ ] Hero + one-click copy of the install command, above the fold on mobile (S). AC: Given a phone viewport, when the page loads, then headline, subline and GitHub CTA are visible without scrolling.
- [ ] Dashboard section with a real screenshot or faithful static mock generated from `python3 scripts/dashboard.py` output (M). AC: shows versions, progress, backlog, tech debt, metrics and the Roadmap tab; labeled as an example if mocked.
- [ ] Problem, audience, 3-phase flow sections with final copy (M). AC: matches spec; every claim traceable to README/docs.
- [ ] 7 habits teaching section (S). AC: each habit names the template feature that enforces it.
- [ ] Agents, paths, token economy sections (M). AC: 18 agents, 8 paths plus adopt-existing, numbers match the repo.
- [ ] Adopt existing Lovable/Bolt/v0 build + start in 3 commands sections (S). AC: snippets verbatim from README.
- [ ] Credits + footer (S). AC: all README-credited projects linked.
- [ ] Single index.html: responsive, accessible (semantic HTML, contrast, keyboard), no third-party requests, no JS required (M) #quality. AC: Lighthouse mobile 90+ in all three.
- [ ] Deploy to Cloudflare via git (S) #infra. AC: live URL; page served from the main branch push.
- [ ] Open Graph/social preview tags and favicon (S). AC: link preview renders; image is local.
- [ ] Truth pass: Dan reviews all copy; run check script (S) #quality.

## Milestone: M2 — Ideas, not committed (target: )
- [ ] Short screen recording or animated terminal of the 3 phases (M)
- [ ] "Worked example": a small project run through the flow, honest about results (L)
- [ ] Dark/light toggle and print-friendly cheat sheet of the 7 habits (S)
- [ ] Translations (S per language)
- [ ] Live dashboard demo generated from the repo's own backlog in CI (M) #foundation
- [ ] Cookieless traffic stats, if Dan allows (S) #infra

## Unplanned
