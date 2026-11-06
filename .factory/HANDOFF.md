# Handoff — 2026-11-06 19:40 — S3 done; first deploy in flight (PR #1)

## Task
Dan's free landing page promoting danfactory (spec docs/specs/landing-page.md) + 7-challenge campaign. GPM Keynote design. Ask Dan at milestones; keep dashboard artifact updated.

## State
- Done: S0, S1, S3 (hero; review fixes a2a89b1). Roadmap tab fixed (4ed7806): global sequence, done milestones collapsed, Next up strip, `> Sequence:` subtitle. PM sequence in docs/BACKLOG.md M1.
- Rule (Dan): after every slice, product-manager re-proposes the build sequence before the dashboard refresh (OPERATING-MODEL.md, AGENT-ROUTING.md).
- In flight: Dan approved go-live. PR https://github.com/dalhhorn-ship-it/lpdan/pull/1 (landing-draft → main), session subscribed to PR activity. When "test" check is green: merge via REST (`gh api -X PUT repos/dalhhorn-ship-it/lpdan/pulls/1/merge`), capture PUSHED_AT, launch deploy-watcher (background) for production `/version`; preview job is expected to fail before the first merge.
- After deploy: find workers_subdomain from the deploy job log/wrangler output, record integrations.deploy.production_url + workers_subdomain in factory.json, tell Dan the URL (noindex, don't share before S9).
- Unknown: whether CLOUDFLARE_API_TOKEN / CLOUDFLARE_ACCOUNT_ID secrets are set (proxy blocks Actions secrets API). First deploy job result answers it.
- Branch landing-draft pushed at cb48216; clean.

## Open questions for Dan
- Copyable install command in the hero? (Currently no; backlog reworded to spec.)
- No-JS section menu on phones? (TD-005)
- Add backlog item for TD-003 font licence before truth pass? (PM suggests yes)

## Next steps
1. Finish deploy (above). 2. S4 dashboard section (PM sequence #1). Then per BACKLOG order. After each slice: L2 ladder → PM re-sequence → `python3 scripts/dashboard.py` → republish https://claude.ai/artifact/FmN8SMHSu89S6yQdjmmUKW (file dashboard/index.html).

## Watch out
- gh GraphQL blocked: use `gh api` REST. Actions secrets API blocked.
- Run docs_index.py before committing docs changes (check.sh fails on stale INDEX).
- Test runs append metrics/history.jsonl: commit it with your change.
- public/index.html > 350 lines: read in slices. Design rules: no shadows/gradients/radius/icons; magenta text ≥24px bold.
- Dan: they/them; English/Dutch.
