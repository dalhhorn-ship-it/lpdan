# Handoff — 2026-11-11 — template 1.2.0 sync + evals on page and public dashboard

## Task
Dan approved docs/specs/template-update-2026-11.md (recommendations taken on all 5 open questions): sync lpdan to danfactory 9cb70c5 (tree 1.2.0), "Proven by evals" on the landing page, Evals tab on the public dashboard.

## State
- Done on branch ccr-7c9c51ff-xe5z6t (WIP checkpoint e36cf37 + final commit after it). Backlog item ticked.
- Sync: 3-way merge per file (ADR 0006). Security conflicts took the template; lpdan SEC tests still pass; 2 dropped protections ported back (adopt_scan clean(), pipe-to-shell guard).
- Dashboard: template dashboard.py + obs/tab_deploy.py, obs/tab_security.py; template delivery.py replaces lpdan tab_delivery.py.
- Public dashboard: scrub() filters SEC-n/security items from data before all views (incl. rv-* Gantt); test in .factory/tests/test_site_dashboard.py. Evals tab = danfactory template evals (metrics/evals*.json copied).
- Page: numbers checked against tests/fixtures/danfactory-evals.jsonl by check_page.py (mutation-tested). No nav link (spec §0). Hash deep link to a tab doesn't work (TD-010).
- Checks: metrics.py test green x2, check.sh ok, check_page 54/0, smoke 57/0, screenshots 390/1440 light/dark: no h-scroll, 0 external requests.

## Next
- Not deployed: production is main; waiting for Dan to say merge/PR. Then deploy-watcher in background.
- TD-011: upstream docs_index --related + the 2 security ports to danfactory.
