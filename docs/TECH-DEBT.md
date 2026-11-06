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
