# Policy: security

> Secure defaults always; full audits on request or before L3 releases.

## Always
- Secrets only in env / secret stores (`wrangler secret put`, GitHub secrets). Never in repo, docs, chat, or `wrangler.jsonc`. `.env*` and `.dev.vars` are git-ignored and read-denied.
- Least-privilege API tokens, one per environment.
- Dependencies: lockfiles committed; add dependencies deliberately.
- Production changes only via git (see `ship`).

## Cloudflare deploy credentials
- **Token:** Cloudflare → My Profile → API Tokens → Create Token → "Edit Cloudflare Workers" template, limited to your account (and only the zones you need), with an expiry. Never use the Global API Key.
- **Where it lives:** GitHub → repo Settings → Environments → `production`, with Deployment branches set to `main` only: environment secret `CLOUDFLARE_API_TOKEN` (required). Do **not** store it as a repo-level Actions secret. A `pull_request` run uses the PR branch's copy of the workflow, so a repo secret reaches any same-repo branch's code; only the environment branch rule keeps it on merged code (SEC-002). PR previews use environment `preview` with an optional, separate token (a second "Edit Cloudflare Workers" token with an expiry); without one, previews are skipped. `CLOUDFLARE_ACCOUNT_ID` is optional: Wrangler infers the account when the token covers one account. If you set it, it must be the **Account ID** (Workers & Pages sidebar), not a **Zone ID**. Both are 32 hex characters, and a Zone ID fails with `Authentication error [code: 10000]`. Only use an "Edit Cloudflare Workers" API token; R2 access keys (Access Key ID / Secret Access Key) can't deploy Workers. `gh secret set CLOUDFLARE_API_TOKEN --env production` prompts for the value, so it stays out of shell history.
- **Never:** in chat, in commits or `.env` files, in Claude settings or docs. Claude doesn't need it; GitHub Actions deploys.
- **Local:** `npx wrangler login` (browser OAuth), not a token.
- **Exposure:** PRs from forks get no secrets. Same-repo PR branches reach only the `preview` environment. The deploy job runs in `production` (add required reviewers there if you want a manual gate). Rotate on expiry or on any suspicion: revoke in Cloudflare, then set the new value in GitHub.

## On request / L3
- `security-audit-run` installs and runs Cloudflare's security-audit skill (guidance or full audit). Full-audit artifacts are written outside the repo.
- The latest audit summary (findings, hardening notes, limits; never payloads or secrets) lives in `docs/security/latest.json` and is shown in the dashboard Security tab. Each finding is also tracked as a TECH-DEBT item.
- Confirmed High/Critical findings block an L3 release.
