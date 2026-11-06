# Handoff — 2026-11-06 19:25 — Landing page: S1 done, next S3 (hero)

## Task
Dan's free landing page promoting danfactory to vibe coders (why/who, 3 phases, agents, dashboard/traceability, 7 habits, adopt, start) plus a 7-challenge campaign ("Vibe Ladder"). GPM Keynote design system. Ask Dan for approval at milestones; keep his dashboard artifact updated.

## State
- Done: PRD confirmed (docs/specs/landing-page.md, Decisions section); operating model approved at L2 (306b4c9); S0 spike + Worker scaffold + _headers + workflow fixes (77ac60a); S1 test harness + token layer (619d827) + review fixes (c399408). Tests: `python3 scripts/metrics.py test` green in ~3 s; `bash scripts/check.sh` ok.
- In progress: nothing half-applied.
- Branch: landing-draft (pushed), uncommitted: none. main = initial commit only.

## Decisions (and why)
- Rigor L2 (Dan chose over proposed L1; tree says L3 for public internet) — docs/OPERATING-MODEL.md
- Static single page, no build step, Worker static assets, self-hosted Archivo, midnight theme only — docs/decisions/0002-static-page-worker-assets-no-build.md
- Campaign: GitHub Issues only, honour system, no prize, no phone/email; don't claim Cloudflare is free; Claude picks test runner in challenge 3
- Copy: keep closing headline "Give your next project rails, not rules"; no Share feedback button; no Challenges nav link
- Worker name `danfactory` (Dan has not confirmed; changeable before first deploy)

## Next steps
1. S3 hero + nav + copy.js polish (developer agent), then L2 ladder: test-runner, reviewer, ui-comprehensive-tester; task-completion-validator for M items.
2. S4 dashboard section, S5 campaign (remove TD-001 gate), S6 content, S7 adopt/start/credits — per docs/design/ARCHITECTURE.md "Build plan".
3. S2 go-live once Dan adds GitHub secret CLOUDFLARE_API_TOKEN on lpdan (+ confirms Worker name): PR landing-draft → main, deploy-watcher in background, record workers_subdomain/production_url in factory.json.
4. After each slice: `python3 scripts/dashboard.py` then republish artifact https://claude.ai/artifact/FmN8SMHSu89S6yQdjmmUKW (Artifact publish, file_path dashboard/index.html).
5. Milestone end (M1): karen + jenny, then retro; S8 OG image, S9 truth pass + remove noindex.

## Watch out
- Running repo scripts like bootstrap.sh was once blocked by the auto-mode classifier; cf_scaffold.py later ran fine.
- Playwright: use the preinstalled one (require('playwright')); never `playwright install` locally. CI installs it with --no-save.
- public/index.html > 350 lines: read in slices or via bulk-reader.
- Design rules: no shadows/gradients/radius/icons; magenta text only ≥24px bold; streaks never behind text.
- Dan writes in English/Dutch; use they/them for Dan.

## Pointers
- docs/design/ARCHITECTURE.md (build plan, tokens, tests, deploy), docs/OPERATING-MODEL.md, docs/BACKLOG.md, docs/TECH-DEBT.md (TD-001..004)
- design/gpm-keynote/README.md, tokens.json; design/landing/index.html
- tests/check_page.py, tests/smoke.mjs, public/_headers, wrangler.jsonc, .github/workflows/
