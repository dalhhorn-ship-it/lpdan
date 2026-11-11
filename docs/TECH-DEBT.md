# Tech debt register

> Known shortcuts and their cost; the dashboard reads this file plus automated signals (TODO/FIXME markers, oversized files, import cycles). Updated by `retro` and `engineering:tech-debt` audits.

Format: `- [ ] TD-NNN Title — impact: high|medium|low · effort: S|M|L · area: <area>` under **Open**; move to **Resolved** with `[x]` when paid down.

## Open
- [x] TD-001 check_page.py campaign checks (links 2x in order, 8 details.faq) are gated on `id="campaign"` existing; remove the gate in slice S5 — impact: low · effort: S · area: tests — done 2026-11-07: gate removed, checks always run
- [ ] TD-002 check_page.py `--upstream` (diff fixture vs live README) and `--online` (link liveness) not implemented — impact: low · effort: S · area: tests
- [ ] TD-003 public/fonts/OFL.txt: licence text written from the standard OFL 1.1, copyright lines for Archivo/Archivo Black not verified against upstream; replace with the upstream OFL.txt files — impact: medium · effort: S · area: licence
- [ ] TD-004 Magenta-text lint in check_page.py is lexical (rule-level); smoke.mjs checks computed styles and is the real guard — impact: low · effort: S · area: tests
- [ ] TD-005 No section links in the nav below 860px (only brand + GitHub; hero links to #start). A no-JS `<details>` menu would fix it if wanted — impact: low · effort: S · area: ui
- [ ] TD-010 Dashboard tabs are CSS radio inputs, so a URL hash (dashboard/#tab-evals) cannot open a tab; the page links to dashboard/ and names the tab instead. Fix upstream in danfactory (no-JS deep links), then pull — impact: low · effort: M · area: dashboard
- [ ] TD-012 Eval fixtures (tests/fixtures/danfactory-evals.jsonl, danfactory-evals-policy.md) and metrics/evals*.json are frozen copies from danfactory 9cb70c5; refresh at the next template sync — impact: low · effort: S · area: tests

## Resolved
- [x] TD-011 Template drift: scripts/docs_index.py stays lpdan's version (template 1.2.0 lacks `--related`, upstreamed from lpdan 1b35b9f); lpdan also re-adds two security fixes the template dropped (adopt_scan.py report sanitiser, pipe-to-shell in guard_bash_policy.py). Upstream all three to danfactory so the next sync is clean — impact: medium · effort: S · area: tooling — upstreamed 2026-11-11: danfactory branch ccr-7c9c51ff-xe5z6t (caeb33a), with regression tests; no PR opened
- [x] TD-006 SEC-001 (audit 2026-11-07, confirmed medium): adopt_scan.py/adopt.py follow symlinks planted in the adopted repo and write or chmod files outside it. Fix: realpath containment plus O_NOFOLLOW/O_EXCL, a no-follow chmod walk, and a sanitised package name — impact: high · effort: M · area: tooling
- [x] TD-007 SEC-002 (confirmed by Dan: repo-level secret; code and docs fixed, see ADR 0003; token moved into environment "production" by Dan 2026-11-07): the PR preview job uses the same CLOUDFLARE_API_TOKEN as production. If it is a repo secret, scope it to the 'production' environment and give previews their own token; update security.md, cf_scaffold.py, the ship skill and the template — impact: high · effort: S · area: ci
- [x] TD-008 SEC-003 (needs validation): guard_bash_policy.py misses `bash -c "…wrangler deploy"`, heredocs, `wrangler versions deploy` and `wrangler@4 deploy`. Fix: match the raw command and widen the regex and deny rules — impact: medium · effort: S · area: agent
- [ ] TD-009 scripts/dashboard.py contrast: done-milestone list items and the header production link fall below 4.5:1 (Lighthouse a11y 96 on /dashboard/); fix upstream in danfactory's dashboard.py, then pull — impact: low · effort: S · area: dashboard
