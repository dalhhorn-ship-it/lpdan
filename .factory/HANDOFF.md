# Handoff — 2026-11-07 — S2 live on workers.dev; next S4 dashboard section

## Task
Dan's free landing page promoting danfactory (spec docs/specs/landing-page.md) + 7-challenge campaign. GPM Keynote design. Ask Dan at milestones; keep dashboard artifact updated.

## State
- Done: S0, S1, S3 (hero; review fixes a2a89b1). Roadmap tab fixed (4ed7806): global sequence, done milestones collapsed, Next up strip, `> Sequence:` subtitle. PM sequence in docs/BACKLOG.md M1.
- Rule (Dan): after every slice, product-manager re-proposes the build sequence before the dashboard refresh (OPERATING-MODEL.md, AGENT-ROUTING.md).
- LIVE: https://danfactory.dalhhorn.workers.dev (ef1f8af, noindex header; smoke ok). Session env "lpdan" allows that host. landing-draft is ahead of main (deploy record, handoff); next PR carries it.

## Open questions for Dan
- Copyable install command in the hero? (Currently no; backlog reworded to spec.)
- No-JS section menu on phones? (TD-005)
- Add backlog item for TD-003 font licence before truth pass? (PM suggests yes)

## Next steps
1. S4 dashboard section (PM sequence #1). Then per BACKLOG order. After each slice: L2 ladder → PM re-sequence → `python3 scripts/dashboard.py` → republish https://claude.ai/artifact/FmN8SMHSu89S6yQdjmmUKW (file dashboard/index.html).

## Watch out
- gh GraphQL blocked: use `gh api` REST. Actions secrets API blocked.
- Run docs_index.py before committing docs changes (check.sh fails on stale INDEX).
- Test runs append metrics/history.jsonl: commit it with your change.
- public/index.html > 350 lines: read in slices. Design rules: no shadows/gradients/radius/icons; magenta text ≥24px bold.
- Dan: they/them; English/Dutch.
