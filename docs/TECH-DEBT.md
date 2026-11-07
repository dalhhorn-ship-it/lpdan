# Tech debt register

> Known shortcuts and their cost; the dashboard reads this file plus automated signals (TODO/FIXME markers, oversized files, import cycles). Updated by `retro` and `engineering:tech-debt` audits.

Format: `- [ ] TD-NNN Title — impact: high|medium|low · effort: S|M|L · area: <area>` under **Open**; move to **Resolved** with `[x]` when paid down.

## Open
- [ ] TD-001 check_page.py campaign checks (links 2x in order, 8 details.faq) are gated on `id="campaign"` existing; remove the gate in slice S5 — impact: low · effort: S · area: tests
- [ ] TD-002 check_page.py `--upstream` (diff fixture vs live README) and `--online` (link liveness) not implemented — impact: low · effort: S · area: tests
- [ ] TD-003 public/fonts/OFL.txt: licence text written from the standard OFL 1.1, copyright lines for Archivo/Archivo Black not verified against upstream; replace with the upstream OFL.txt files — impact: medium · effort: S · area: licence
- [ ] TD-004 Magenta-text lint in check_page.py is lexical (rule-level); smoke.mjs checks computed styles and is the real guard — impact: low · effort: S · area: tests
- [ ] TD-005 No section links in the nav below 860px (only brand + GitHub; hero links to #start). A no-JS `<details>` menu would fix it if wanted — impact: low · effort: S · area: ui

## Resolved
- [x] TD-006 SEC-001 (audit 2026-11-07, confirmed medium): adopt_scan.py/adopt.py follow symlinks planted in the adopted repo and write or chmod files outside it. Fix: realpath containment plus O_NOFOLLOW/O_EXCL, a no-follow chmod walk, and a sanitised package name — impact: high · effort: M · area: tooling
- [~] TD-007 SEC-002 (confirmed by Dan: repo-level secret; code and docs fixed, see ADR 0003; owner must move the token into environment "production"): the PR preview job uses the same CLOUDFLARE_API_TOKEN as production. If it is a repo secret, scope it to the 'production' environment and give previews their own token; update security.md, cf_scaffold.py, the ship skill and the template — impact: high · effort: S · area: ci
- [x] TD-008 SEC-003 (needs validation): guard_bash_policy.py misses `bash -c "…wrangler deploy"`, heredocs, `wrangler versions deploy` and `wrangler@4 deploy`. Fix: match the raw command and widen the regex and deny rules — impact: medium · effort: S · area: agent
