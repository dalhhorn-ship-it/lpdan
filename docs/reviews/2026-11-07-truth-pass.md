# Truth pass — landing page — 2026-11-07

> Delegated by Dan in chat ("launch content review agent … to signoff that work, I wont read it myself"). Reviewers: `jenny` (spec vs implementation) and `reviewer` (claims vs README/docs/code), fresh context, read-only.

## Verdicts
- jenny: PASS WITH FIXES. reviewer: SIGN-OFF AFTER FIXES.
- Result after fixes: **signed off**, with one launch condition (below).

## Findings and resolution
| # | Finding | Resolution |
|---|---|---|
| 1 | Public Security tab still showed coverage, run status, empty "Hardening notes"/"Limits" headings and exploit-path detail of fixed findings | Public tab now lists fixed findings as severity, title, state only (scripts/site_dashboard.py `security_panel`); check_page.py fails if those strings appear |
| 2 | Gates tab "Last security audit: not recorded" vs Security tab 2026-11-07 | Audit recorded (`metrics.py record security-audit`) |
| 3 | Copy hinted "open security issues are left out" | Neutral wording on the page and dashboard bar |
| 4 | Challenge files said "Issue or Discussion"; Dan decided Issues only (spec Decisions, 2026-11-06) | All 7 files say Issue |
| 5 | PRD gate, roadmap v2 details, re-plan after every slice, deploy token in `production` environment limited to `main`: template claims? | Verified on danfactory `main`: 260b6ea, d0dae76, dashboard skill "Refresh rhythm", docs/policies/security.md line 12. True for the template; no change |
| 6 | Observability tabs "from an unmerged danfactory branch" | Verified: claude/great-pasteur-br9y8v commits not on danfactory main |
| 7 | Hero "keeps working as it grows", NVIDIA numbers without link, "no JS, no network calls" | Dan-confirmed spec copy (landing-page.md §1, §7, §8); kept |
| 8 | `X-Robots-Tag: noindex` | Deliberate until launch; launch item added to docs/BACKLOG.md M1 |

## Launch condition
The campaign CTA and help line point to GitHub Issues on dalhhorn-ship-it/danfactory. Not verifiable from this session: confirm Issues are enabled and the `challenge` label exists (M1 item "Enable GitHub Issues…") before removing noindex.
