# Handoff — 2026-11-07 07:40 — M1 build done except Dan's items

## Task
Dan: "build M1". Everything buildable in M1 is done and live on main (d95a9a8). Left: Dan's own items.

## State
- Done (all pushed to claude/blissful-tesla-9vxexu and main):
  - Upstream dashboard pulled: roadmap v2, template mode, PRD gate (7d73f58, 39a6f54). ADR 0004 = upstream 0002.
  - Clickable dashboard at /dashboard/ via scripts/site_dashboard.py; screenshots removed (9242277). PRD docs/specs/landing-latest-features.md approved.
  - M1 copy sections verified against spec (c1d0f88); #campaign + 8 FAQ + TD-001 closed (7fc794c); OG/twitter tags, img/og.png, favicon.svg, Lighthouse mobile / = 99/100/100/100, /dashboard/ = 100/96/100/100 (d95a9a8).
  - Deploys 39a6f54 and 9242277 succeeded in GitHub Actions; d95a9a8 queued at handoff. Live URL not checkable from sandbox (proxy blocks the host).
  - Dashboard artifact https://claude.ai/artifact/FmN8SMHSu89S6yQdjmmUKW v15.
- In progress: nothing. Uncommitted: none (except this note).

## Decisions (and why)
- M1 page items need no new PRD: docs/specs/landing-page.md is Dan-confirmed (2026-11-06).
- FAQ uses challenge 1's 8 items; spec's "blank page on localhost" FAQ dropped (not in challenge 1). Ask Dan.
- Contrast issues inside dashboard.py logged as tech debt (fix upstream in danfactory, then pull).

## Next steps
1. Dan: review challenge files (02 farm brief), enable Issues + "challenge" label on danfactory, dogfood challenges 1-2 on a clean machine, final truth pass.
2. Before launch: `python3 scripts/site_dashboard.py` to refresh the snapshot; remove noindex in public/_headers only after the truth pass.
3. Optional: upstream the Deploy/Security tabs to danfactory so the page label can go.

## Watch out
- Characters must be in the latin font subset (no U+2192 arrow) — tests/check_page.py LATIN.
- Force-push denied. Dan: they/them; English/Dutch.

## Pointers
- docs/BACKLOG.md M1, docs/specs/landing-page.md §9b, scripts/site_dashboard.py, docs/TECH-DEBT.md
