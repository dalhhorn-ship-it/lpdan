# PRD: Template update 1.1.0 to 1.2.0, "Proven by evals" on the landing page, Evals tab on the public dashboard

> Status: draft · 2026-11-11 · awaiting Dan's approval in chat · Owner: product-manager · Backlog: M1 / "Template update 2026-11"

## Problem
lpdan is on decision tree 1.1.0 (last sync 2edcba8). danfactory origin/main (9cb70c5) is 1.2.0: an eval harness, an Evals tab, roadmap views (6-month, Gantt, Releases), a Carbon-styled dashboard, delivery backflow, auto-compact handoff loop and security hardening. Our landing page and public dashboard therefore describe an older template, and the page has no evidence section. The brief's eval numbers and the Carbon/roadmap-view claims must be true to the README (GOAL.md constraint), and the public copy must not leak SEC-n or security items.

## Goal and success measure
Serves GOAL.md Outcome, constraint "every claim must be true to the danfactory repo" and AC 1, 2, 5, 7. Success: lpdan runs 1.2.0, the page quotes the README for every new claim, the public dashboard shows the new tabs and views with no security text, all checks green.

## Users and user stories
- As a vibe coder, I want evidence that the template works so that I trust it before cloning.
- As a visitor, I want honest limits stated so that I am not sold on a perfect score.
- As Dan, I want lpdan on the current template so that the page and the template do not drift.

## Scope
Three slices, in this order (risk-first: the sync changes everything else).
1. **Template sync 1.1.0 to 1.2.0** (L).
   - Copy as-is: scripts/evals.py, evals_graders.py, evals/, docs/policies/evals.md; scripts/obs/ modules theme, delivery, evals_data, evals_flow, evals_views, tab_evals, roadmap_data, roadmap_views, plus changed model.py and tab_docs.py; scripts ci_runs, metrics, docs_index, adopt, adopt_scan, cf_scaffold, install-codegraph.sh, install-skill.sh; .claude hooks, agents, skills (dashboard, handoff, security-audit-run, ship); plugin/skills/adopt/SKILL.md; new and changed .factory/tests; docs/policies; docs/operating-model.
   - Merge by hand: scripts/dashboard.py (port lpdan-only tabs Security and Deploy into scripts/obs/tab_*.py using Carbon classes and var(--...) tokens, no hex); .claude/settings.json (template hooks and deny rules, keep lpdan-only allow rules); factory.json (add evals and dashboard blocks with roadmap_view, size_days, wip; version 1.2.0; keep project, deploy, integrations.dashboard_url).
   - Never overwrite: GOAL, BACKLOG, OPERATING-MODEL, TECH-DEBT, specs, decisions, public, worker, wrangler.jsonc, metrics, HANDOFF.
   - Caution: "copy as-is" of metrics.py replaces a file listed under "never overwrite: metrics" (the metrics/ data). Treated as scripts/metrics.py only; see Open questions.
2. **Landing page** (M). public/index.html: new "Proven by evals" section: one-line method (real tasks in throwaway copies, graded on what happened, not what was said); published numbers 2026-11-11, 10 tasks x 3 runs, haiku 30/30 for 0.46 USD, sonnet 30/30 for 2.43 USD; honest caveats (suite still easy, both models pass everything; "direct deploy" task is weak proof because the agent declines before the guard fires); link to the public dashboard's Evals tab. Dashboard section updated to mention the Evals tab, the roadmap views and "styled after Carbon" (no IBM logo, not called an IBM product). Quote the README, not paraphrase. Refresh tests/fixtures/danfactory-README.md from README at 9cb70c5.
3. **Public dashboard** (M). scripts/site_dashboard.py to public/dashboard/index.html: BAR_CSS uses var(--border-subtle-01), text var(--text-primary). Security filter applied in public(d) before any view renders, including rv-* roadmap views (6-month, Gantt, Releases); leaks() keeps failing the build; new test with an open SEC-1 item in the Gantt. Publish the Evals tab (data source: open decision below).

## Non-goals
- No new JS, third-party requests, trackers, or IBM branding.
- No change to GOAL, OPERATING-MODEL, specs or decisions content except new ADR(s) for the sync.
- No claim that the suite proves safety; no invented numbers.
- No Lighthouse or page redesign beyond the two sections.

## Acceptance criteria
1. Given the sync, when `python3 scripts/metrics.py test` runs twice, then green both times, and `bash scripts/check.sh` ok.
2. Given factory.json, then version 1.2.0, evals and dashboard blocks present, project/deploy/integrations.dashboard_url unchanged; settings.json has template hooks and deny rules plus lpdan allow rules.
3. Given the private dashboard, when generated, then Security and Deploy tabs still exist, built from scripts/obs/tab_*.py using Carbon classes and var(--...) tokens, with no hex colours.
4. Given the landing page, when read, then "Proven by evals" shows the method line, the date, 10 x 3, both pass counts and costs, the "suite still easy" caveat, the weak "direct deploy" proof caveat, and a working link to the dashboard Evals tab.
5. Given any new landing claim, then it is a README quote (or cited doc) present in tests/fixtures/danfactory-README.md at 9cb70c5, and tests/check_page.py passes (claims, snippets, budgets: index.html <= 64 KB, public/ <= 300 KB or ADR).
6. Given the Dashboard section, then it mentions Evals tab, roadmap views and "styled after Carbon", with no IBM logo and no "IBM product" wording.
7. Given a data set with an open SEC-1 item, when the public dashboard is built, then SEC-1 and security items are absent from Overview, Roadmap, 6-month, Gantt and Releases, and a test proves it for the Gantt.
8. Given a leak, when site_dashboard.py runs, then leaks() fails the build.
9. Given the built public dashboard, when screenshotted at 390 and 1440 px, light and dark, then no horizontal scroll, zero external requests, and no "SEC-" or "secur" text outside fixed findings.
10. Given `node tests/smoke.mjs` and `python3 tests/check_page.py`, then both pass.
11. Given done, then backlog ticked, docs synced, shipped via git with deploy-watcher in the background.

## UX / behaviour notes
- Evals empty state (option c) must say plainly that lpdan has no runs of its own.
- If template data is shown (option a), label it "danfactory template evals" everywhere, including the page link text, so it is never read as lpdan's own result.
- The page numbers are dated 2026-11-11 and stated as a single run set, not a trend.

## Risks and assumptions
- **Truth-rule risk 1 (checked by main agent against `git show 9cb70c5:README.md`).** In the README (line 45-46, 87, 103): the Evals tab and its five views, the roadmap views ("optional 6-month, proposed Gantt and Releases views"), "Styled after IBM's open-source Carbon design system, light and dark, offline, no JavaScript", and the method ("10 tasks run headless in throwaway copies of the template, checked on files, git diff and commands (not wording) ... never in CI"). **Not in the README:** the 2026-11-11 numbers. They are in the template's `metrics/evals.jsonl` at 9cb70c5 and match exactly: set `baseline-haiku-2026-11-11` 30/30, 0.46 USD; `baseline-sonnet-2026-11-11` 30/30, 2.43 USD (the file also holds 15 spike runs, excluded). Mitigation: the page cites them as "danfactory metrics/evals.jsonl, 2026-11-11" (not as a README quote), and check_page.py gets a fixture of that file so the numbers are verified, or Dan upstreams one results line to the README first.
- **Truth-rule risk 2: "quote the README"** is only possible for text that exists there; AC 5 enforces it.
- **Risk 3: security leak** via the new rv-* views, which bypass today's filter if it runs after rendering. Mitigated by filtering inside public(d) first and by the Gantt test (AC 7).
- **Risk 4: budget.** New CSS/tab content may exceed public/ 300 KB; check on a branch early.
- **Risk 5: hand-merge** of dashboard.py and settings.json could drop lpdan-only tabs or allow rules. Diff before/after the generated tab list.
- **Risk 6: hex colours** or IBM wording slipping in; grep gate.
- Assumption: public dashboard stays one self-contained page, no JS required.

## Effort and sequencing
L overall, value lane for slices 2-3, technical-foundation (#foundation) for slice 1. Order: 1, then 3, then 2 (the page links to a live Evals tab, and the numbers claim should be verified first). Slice 1 can ship alone. Backlog placement: M1 (target 2026-11-20): it is the page's current-truth work and the launch item (noindex removal) should wait for it; M2 is "ideas, not committed" and this is committed.

## Open questions
1. **Evals data source for the public Evals tab. Recommendation: (a)** copy the template's metrics/evals.jsonl and evals-baseline.json, labelled "danfactory template evals". Reason: free, and the page's published numbers are exactly those; it shows a real tab. (b) running `python3 scripts/evals.py run` in lpdan costs tokens and tests a landing-page repo with little relevance to the template's guards, so it is not representative of what we sell. (c) the empty state is honest but leaves the page's link pointing at nothing. Caveat on (a): it must be clear these are not lpdan runs.
2. The numbers are in metrics/evals.jsonl, not the README (feature wording is in the README). Cite the jsonl on the page with a test fixture (recommended), or add a results line to the danfactory README first?
3. "Copy as-is: metrics" vs "never overwrite: metrics": confirm scripts/metrics.py is replaced and the metrics/ data directory is kept.
4. Does "no SEC- or 'secur' text outside fixed findings" mean fixed findings may still show, as in the 2026-11-07 revision (which hides new/open ones, not fixed ones)? Confirm.
5. Is a short ADR for the 1.2.0 sync wanted (recommended, yes)?
