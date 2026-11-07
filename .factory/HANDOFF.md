# Handoff — 2026-11-07 08:15 — dashboard complete, truth pass signed off, learnings upstreamed

## Task
Dan's last asks: all danfactory dashboard tabs, hide open security issues publicly, content review sign-off, orphan docs, push upstream learnings. All done.

## State
- Done (lpdan main = 1b35b9f):
  - Dashboard: 13 tabs (194a4d8). Observability tabs from danfactory branch claude/great-pasteur-br9y8v (ADR 0005), Delivery ported from claude/dashboard-backflow-from-minespel, Deploy/Security local. Ranked-backlog roadmap mode skipped (superseded).
  - Public /dashboard/ (scripts/site_dashboard.py): fixed findings only (severity/title/state), no hardening/limits, leak guard + check_page.py test.
  - Truth pass signed off by jenny + reviewer, delegated by Dan: docs/reviews/2026-11-07-truth-pass.md (435c8d6).
  - Orphan docs: docs_index.py counts bare .md paths; tab_docs ignores INDEX edges; 0 orphans (b48db6c).
  - Upstream: danfactory branch claude/learning-doc-graph-links (0759c55) = learning + docs_index fix + test. No PR opened (Dan didn't ask). 3 other learnings were already upstream → marked [upstreamed].
- In progress: nothing. Uncommitted: none.

## Open questions for Dan
- Open a PR for danfactory claude/learning-doc-graph-links? (link: github.com/dalhhorn-ship-it/danfactory/pull/new/claude/learning-doc-graph-links)
- Agents + index: 9 of 19 agents (developer, reviewer, product-manager, code-writer, bulk-reader, test-runner, data-builder, spreadsheet-architect, deploy-watcher) never mention docs/INDEX.md; large-read guard skips subagents; no agent uses knowledge-graph.json; codegraph off. Proposed: PRD to add INDEX-first line + a `docs_index.py --related <doc>` lookup. Awaiting Dan.

## Next steps
1. Dan: confirm GitHub Issues + `challenge` label on danfactory, then remove noindex (backlog launch item); dogfood challenges 1-2; review challenge 02.
2. Before launch: `python3 scripts/site_dashboard.py` to refresh the public snapshot.

## Watch out
- Public dashboard must stay filtered: site_dashboard.py refuses to write if an open finding leaks.
- PRD gate applies to behaviour changes (docs/policies/prd-approval.md). Characters must fit the latin font subset.
- Dan: they/them; English/Dutch. Force-push denied.

## Pointers
- docs/BACKLOG.md M1, docs/specs/landing-latest-features.md (Revision), scripts/site_dashboard.py, scripts/obs/, docs/TECH-DEBT.md (TD-009 contrast)
