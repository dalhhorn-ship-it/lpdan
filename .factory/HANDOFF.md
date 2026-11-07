# Handoff — 2026-11-07 06:20 — Security audit (quick) done + dashboard Security tab

## Task
Dan asked: "run the security-audit-run", then "add this to the dashboard in a new tab". Both are done.

## State
- Done: a full quick-profile audit of ef1f8af. Reports are outside the repo at ~/security-audit-skill/lpdan/run-1/ (REPORT.md, FINDINGS-DETAIL.md, NEEDS-VALIDATION.md, findings.json, coverage-ledger.json). Both validators pass. The reports are lost when the container is reclaimed; only the summary is committed.
- Results:
  - SEC-001 confirmed, medium: adopt_scan.py and adopt.py follow symlinks planted in the adopted repo.
  - SEC-002 needs validation: the PR preview job may use the same CLOUDFLARE_API_TOKEN as production.
  - SEC-003 needs validation: the guard_bash_policy.py deploy guard is bypassable.
  - These are tracked as TD-006..008.
- Dashboard Security tab: scripts/dashboard.py render_security() reads docs/security/latest.json. Commits 28a9b2b, d1b46ff, 428afc3 and merge 32641f8 are on claude/blissful-tesla-9vxexu, which is based on origin/landing-draft (it keeps the Deploy tab). The artifact https://claude.ai/artifact/FmN8SMHSu89S6yQdjmmUKW is republished (v10).
- Branch claude/blissful-tesla-9vxexu has nothing uncommitted. It has not been merged into landing-draft and has no PR.

## Decisions (and why)
- Quick profile: Dan picked it.
- Hunters were source-only. Verifiers used a parent-built sandbox (/srv/sbx/sbx.sh: unshare, read-only mounts, tmpfs scratch, nobody, prlimit, timeout) because bwrap and nsjail are missing.
- Fixes are not applied: an audit describes fixes, and Dan decides.

## Open questions for Dan
- Fix SEC-001/003 now? Is CLOUDFLARE_API_TOKEN a repo secret or a production-environment secret (SEC-002)?
- Merge this branch into landing-draft? (Needs a PR or merge; force-push was denied.)
- Earlier ones: copyable install command in the hero; no-JS phone menu (TD-005); backlog item for TD-003.

## Next steps
1. Get Dan's answers, then fix TD-006..008 (smallest fixes are in docs/security/latest.json and docs/TECH-DEBT.md).
2. Resume the build: S4 dashboard section (PM sequence #1).

## Watch out
- Force-push is denied by the auto-mode classifier: merge instead.
- After every slice: PM re-sequence, then dashboard.py, then republish the artifact.
- Dan: they/them; English/Dutch.
