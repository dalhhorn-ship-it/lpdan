# PRD: Landing page: latest features and clickable dashboard

> Status: draft · 2026-11-07 · Owner: product-manager · Backlog: M1 / "Landing: latest features + clickable dashboard"

## Problem
Dan's ask: "update the landing page with latest features we have build and make the dashboad on the site clickable". The page (public/index.html, spec docs/specs/landing-page.md) predates the Roadmap sequencing, the PRD gate and security hardening. The #dashboard section shows two static screenshots, so a visitor cannot try the thing being sold.

## Goal and success measure
Serves GOAL.md Outcome and constraint "every claim must be true to the repo" (AC 1, 5, 7). Success: a visitor can open a real dashboard from the page, and every new claim traces to README/docs. Measured by the checks below, not by trackers.

## Users and user stories
- As a vibe coder, I want to click through a real dashboard so that I see what I get before cloning.
- As a returning visitor, I want the page to reflect the current template so that I trust it is maintained.
- As Dan, I want honest labels so that the page never promises what the template lacks.

## Scope
1. Copy updates (each line cites its source in the PR):
   - #dashboard: Roadmap tab = one global build sequence 1..N across lanes, "Next up" strip (top 3), per-milestone "Sequence:" why-line, finished milestones collapse, PRD draft/approved badges (upstream README line 45).
   - 7 habits / phases flow: PRD approval gate (docs/policies/prd-approval.md): a PRD approved by the user in chat before code; product-manager re-proposes the order after each slice.
   - Security or trust line: deploy token in a GitHub environment restricted to main (docs/policies/security.md).
   - Deploy and Security dashboard tabs: mention only labeled "in this site's own dashboard, not yet in the template".
2. Clickable dashboard (see Open questions): a link or embedded self-contained page of the generated dashboard, with the existing screenshots kept or replaced per the chosen option. Labeled as "this project's own live dashboard, generated <date>".

## Non-goals
- Template mode for maintainers (low visitor value).
- New JS, third-party requests, trackers, or a live-updating dashboard (CI generation stays in M2).
- Redesigning the page or changing other sections.
- Claiming Deploy/Security tabs ship in the template.

## Acceptance criteria
1. Given the page, when I click the dashboard section's call to action, then a real dashboard opens with working Overview, Roadmap, Deploy and Security tabs.
2. Given JS disabled, when I switch tabs, then they work (CSS radio inputs).
3. Given keyboard only, when I tab to the tab controls and press arrow/space, then tabs switch with a visible focus ring, and there is a link back to the landing page.
4. Given the new copy, when compared with README/docs, then each claim maps to a cited source, and tests/check_page.py claim/snippet checks pass.
5. Given the Deploy and Security tabs, when mentioned anywhere, then they are labeled as not yet in the upstream template.
6. Given the budgets, when tests/check_page.py runs, then index.html ≤ 64 KB, each image ≤ 120 KB, public/ ≤ 300 KB all pass (budget changes, if any, are made in that file with an ADR).
7. Given `python3 scripts/metrics.py test` and `bash scripts/check.sh`, then both pass with nothing skipped.
8. Given the served dashboard, when scanned, then it has no secrets, no third-party requests, and the privacy review in Risks is done.
9. Given the page, then Lighthouse mobile stays at 90+ and no console errors appear.

## UX / behaviour notes
- Dashboard shows real numbers, including red ones; the caption says so ("real, unedited").
- A stale snapshot is dated in the caption and in the dashboard header.
- If a screenshot is dropped, the section keeps a text description of each tab.

## Risks and assumptions
- Riskiest: the budget trade-off. Serving the 37.7 KB dashboard pushes public/ to about 325 KB, over 300 KB. Check cheaply by running the check script on a branch.
- Privacy/truth: real red metrics (50% deploy failure, over-budget tokens), branch name, security findings (all fixed; repo is public). Review before publishing; do not hand-edit numbers.
- Snapshot goes stale; mitigate with a date and a refresh step in the release routine.
- Copy drifts from the upstream template; mitigate with citations.

## Effort and sequencing
M, value lane. Slices: (1) copy updates, S; (2) clickable dashboard, M, after the open question is answered. Slice 1 can ship alone.

## Open questions
1. Budget: (A) drop both screenshots (about -184 KB), serve the dashboard copy; (B) keep one screenshot (about 90 KB) plus the dashboard copy, which needs the cap raised to about 340 KB; (C) raise the cap and keep both. Recommendation: A. A clickable page replaces the screenshots, keeps the 300 KB discipline, and shows real state. If Dan wants a visual before clicking, B with a raised cap.
2. Okay to publish the live dashboard with real red metrics and security history (recommended yes: honest, all findings fixed), or sanitize?
3. Deliver as a separate page (public/dashboard/index.html, linked) or embedded in the section? Recommendation: separate page, so the landing page stays under 64 KB and the dashboard is full-width.
