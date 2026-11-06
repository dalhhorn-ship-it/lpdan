# Operating model

> Approved by Dan on 2026-11-06, with rigor raised to L2. How this project is built: chosen path(s), rigor, agents, practices, gates, budgets. Written from the `choose-path` decision tree; revised by `retro`.

## Path and rigor
- **Q0:** a draft exists, but it was started from this template. No adopt-existing needed.
- **Primary: documents-content** (Q3: the deliverable is a page of copy and challenge files). The biggest risk is the truth of the copy (BACKLOG M1: "truth of the copy and the dashboard visual are the risks").
- **Secondary: software-product** (Q9/Q10): it must be reachable on the public internet, so it needs tests, CI, preview URLs and git → Cloudflare. Its gates (tests green, preview smoke) apply on top of the primary path.
- **Rigor: L2 (standard)**, chosen by Dan over the proposed L1. The tree's Q8 puts "public internet" at L3; Dan chose L2 because the page holds no user data or money and rollback is `git revert`. Log it as a `[tree-gap]` learning: "static, data-free public page → L2".
- Design and decisions: docs/design/ARCHITECTURE.md, ADR docs/decisions/0002-static-page-worker-assets-no-build.md.

## Agents and skills
Roster: product-manager, software-architect, developer, test-runner, reviewer, task-completion-validator, code-quality-pragmatist, karen, jenny, ui-comprehensive-tester, deploy-watcher, doc-keeper (bulk-reader and ultrathink-debugger when their triggers fire).

| When | Use |
|---|---|
| Backlog re-slice after this plan is approved | product-manager |
| After every slice, before the dashboard refresh (Dan, 2026-11-06) | product-manager re-proposes the build sequence: reorders open items in docs/BACKLOG.md and updates the `> Sequence:` line; the Roadmap tab shows that order |
| Specified slice (S1, S3–S7 in ARCHITECTURE.md) | developer (Sonnet), one slice per PR |
| Small fixes (< ~50 lines), spike S0, scaffold S2, OG S8 | main agent |
| Failing or noisy tests | test-runner |
| Every slice (L2 ladder) | test-runner green; `reviewer` before merge; `task-completion-validator` for M/L items; `code-quality-pragmatist` for a new abstraction or a diff over ~300 lines |
| Any UI slice | ui-comprehensive-tester with the block-colour / magenta / 375px checklist |
| Milestone end (M1 launch) | `karen` always; `jenny` (the spec has > 5 ACs); then `retro` |
| Truth pass (S9) | reviewer (claims vs repo, fresh context), then karen and jenny at milestone end |
| Reading index.html (> 350 lines) | targeted slices, or bulk-reader |
| After every push | deploy-watcher, in the background |
| End of every task | doc-keeper / docs-sync |

## Practices and habits
- The spec is the approved outline (documents-content step 1). Copy changes go through the spec first.
- One vertical slice per PR, riskiest first. Tests (check + smoke) are updated in the same PR.
- No build step, no framework, no new runtime dependencies. Dev dependencies: wrangler, playwright only.
- Challenge files in public/challenges/ are the source of truth and ship unchanged.

## Policies
All of docs/policies/* apply. Security: no secrets in the repo; `CLOUDFLARE_API_TOKEN` lives only in GitHub Actions secrets. No security audit required at L2 (only on request or before an L3 release). Async delivery: never wait on deploys.

## Commands (set in factory.json on approval)
| Key | Value | Note |
|---|---|---|
| `phase` | `"build"` | after approval |
| `paths.primary` | `"documents-content"` | |
| `paths.secondary` | `["software-product"]` | |
| `agents.roster` | `["product-manager","software-architect","developer","test-runner","reviewer","task-completion-validator","code-quality-pragmatist","karen","jenny","ui-comprehensive-tester","deploy-watcher","doc-keeper"]` | |
| `commands.test` | `"python3 tests/check_page.py && node tests/smoke.mjs"` | < 10 s; prints "N passed, M failed" |
| `commands.test_affected` | `"python3 tests/check_page.py"` | < 1 s; pre-push gate |
| `commands.coverage` | `""` | no domain code; coverage n/a |
| `commands.lint` | `"node --check public/copy.js && node --check tests/smoke.mjs && python3 -m py_compile tests/check_page.py"` | syntax only |
| `commands.build` | `"npm run build"` | set by cf_scaffold.py; a no-op echo |
| `commands.deploy` | `""` | the git push is the deploy; deploy-watcher records `metrics.py deploy --seconds` |
| `integrations.deploy.*` | filled by `cf_scaffold.py --name <worker>`; add `workers_subdomain` and `production_url` after the first deploy | |

## Quality gates
- [ ] `metrics.py test` green locally and in CI; `bash scripts/check.sh` green
- [ ] Snippets verbatim vs the pinned README; no third-party URLs; design rules hold (all automated)
- [ ] Preview URL looked at on a phone-width viewport before merge (UI slices)
- [ ] Truth pass by reviewer and jenny, then Dan, before launch (removing noindex)
- [ ] Lighthouse mobile ≥ 90 for Performance, Accessibility and Best Practices at launch

## Deploy
Cloudflare Workers + static assets from ./public. Route B (GitHub Actions, templates/deploy-cloudflare.yml), production branch `main`, PR previews `pr-<n>-<worker>.<subdomain>.workers.dev`. URL: `*.workers.dev` until a domain is chosen. Rollback: `git revert` + push. Workflow fix needed so that `public/**/*.md` changes still deploy (see ARCHITECTURE.md, Deploy).

## Budgets
| Budget | Value | Why |
|---|---|---|
| `test_seconds` | 30 (from 120) | the suite is ~10 s; a tight budget flags a slow smoke test early |
| `affected_test_seconds` | 5 (from 30) | the static check is < 1 s |
| `deploy_seconds` | 180 (unchanged) | |
| `min_coverage_pct` / `max_coverage_drop_pct` | unchanged, inert | no coverage report for a static page |
| Page weight | see ARCHITECTURE.md, Performance budget (enforced in check_page.py) | |

## Deviations from path defaults
- documents-content: no docx/pptx/pdf export; the HTML page is the single source.
- software-product: no TDD of domain logic (there is none); tests are content and rendering checks. The spec plus ADR 0002 replace a separate walking-skeleton spec.
- Rigor L2 despite "public internet" mapping to L3 (above).
- Copy not in the spec: only the closing headline "Give your next project rails, not rules" stays (Dan, 2026-11-06). Remove the "Share feedback" button and the "Real, not a render" caption copy; no "Challenges" nav link.
