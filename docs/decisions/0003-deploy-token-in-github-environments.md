# 0003 — Cloudflare deploy token lives in GitHub environments, not repo-level secrets

> Status: accepted (Dan asked for the SEC findings to be fixed, 2026-11-07) · Date: 2026-11-07

## Context
The security audit of 2026-11-07 (SEC-002, docs/security/latest.json) found that `CLOUDFLARE_API_TOKEN` was a repo-level Actions secret, as the docs told operators to set it up. The `pull_request` preview job runs code from the PR branch (`npm ci`, the build, and the PR's own copy of the workflow) with that same token. Anyone who can push a branch to this repo could therefore deploy to production without merging, without the "test" check, and without the `production` environment gate. A guard written in the workflow file cannot fix this, because a PR branch can edit the workflow.

## Options
1. **Environment-scoped secrets.** Put the production token in environment `production` with deployment branches limited to `main`. Previews use environment `preview` with an optional, separate token. Pros: GitHub itself enforces the boundary, even against an edited workflow. Cons: a one-time settings change for the owner, and a second token if previews are wanted.
2. **Drop previews entirely.** Pros: simplest. Cons: no per-PR preview URL, which the ship flow relies on for review.
3. **Keep repo secrets and restrict who can push.** Pros: no change. Cons: depends on never adding a collaborator or bot, and is invisible in the source.

## Decision
Option 1. The preview job declares `environment: preview` and skips the upload when that environment has no token. The deploy job stays in `production`. The template, cf_scaffold.py, the ship skill and docs/policies/security.md tell new projects to set it up this way.

## Consequences
- The owner must move the token: create it under the `production` environment, set the branch rule to `main`, then delete the repo-level secret. Done by Dan on 2026-11-07.
- PR previews are skipped until a separate preview token is added to environment `preview`.
- Same-repo branches can no longer reach a token that can deploy to production.
