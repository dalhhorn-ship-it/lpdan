# PRD: Template update to danfactory v0.1.0 (gated autonomy + worked example)

> Status: draft · 2026-11-14 · Owner: product-manager · Backlog: Ideas → "Worked example" + new item "Template update v0.1.0"

## Problem
The page describes danfactory as of 2026-11-11. Since then the template added gated autonomy: a merge gate, locked acceptance tests written from the PRD, an issue ledger, a fixer runner that fixes issues in a sandbox and merges to staging only, a release train, parallel fixers, and learning from rejections, plus a write guard that enforces the PRD gate. Visitors can't see any of it, and the page's claims fall behind the repo.

## Scope
1. A "From supervised to gated autonomy" section: the human keeps three controls (approve the PRD, start builds, push to main); agents write tests, file issues, fix, review and gate in between. One diagram, plain words.
2. A "Worked example" section built only from the evidence in danfactory evals/spikes/pilot-semverlite/: a semver library whose code was written by the fixer runner. It reports the honest numbers (0.29 USD of useful work, 2.72 USD of failed runs from template bugs, all fixed), with links to the evidence.
3. Sync the template files lpdan uses to v0.1.0 (scripts, hooks, agents, dashboard), keeping lpdan's own records.
4. The public dashboard shows the Autonomy tab's empty state honestly, since lpdan itself runs no fixer.

## Non-goals
New claims not backed by danfactory's README/docs; turning on autonomy for lpdan itself (a static page has no acceptance suite).

## Acceptance criteria
1. Every claim in the new sections has a matching sentence or file in danfactory at v0.1.0 (checked by a claims list in the PR).
2. Numbers in the worked example match evals/spikes/pilot-semverlite/README.md exactly.
3. Page still works without JS, passes the existing accessibility and link checks, and deploys via git.
4. lpdan's check.sh and gate pass after the sync; lpdan's backlog, specs and decisions are untouched by the sync.

## Effort
M. Push to a branch, preview URL, then you approve the merge to main.
