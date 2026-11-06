# Challenge 4: Lift-off (ship to Cloudflare via git)

> Level 4 of 7 · Time box: 1-2 hours · Badge: **Lift-off** · First challenge that leaves localhost · Self-reported

## Goal
Put your tested farm game on the internet the danfactory way: deploy via git to Cloudflare with the `ship` skill, while Claude keeps working and a background helper watches the deploy.

## Skills you learn
- What "deploy via git" means: a push is the deploy.
- Not waiting on builds (push and continue).
- Proving the new version is live, not guessing.

## danfactory features used
`ship` skill, `templates/deploy-cloudflare.yml`, `deploy-watcher` (background helper), `scripts/wait-for-url.sh`, `.githooks/pre-push`, deploy metrics (push-to-live seconds, budget 180 s), the async-delivery policy (docs/policies/async-delivery.md).

## Start with danfactory
Use your tested Challenge 3 project. Run `claude`, say **"let's start"**, and ask Claude to ship the game with the `ship` skill. Production deploys go only via git to Cloudflare; direct `wrangler deploy` is denied by the template. You need a GitHub repo for the project and a Cloudflare account; follow the `ship` skill's own instructions and Cloudflare's official docs for account steps. (Starting fresh? README commands: `git clone https://github.com/dalhhorn-ship-it/danfactory my-project && cd my-project && rm -rf .git && git init`, then `bash scripts/bootstrap.sh "my-project" "one line description"`. The `--cloudflare` flag auto-creates a Worker.)

## Steps
1. Ask Claude to run the `ship` skill and follow it. Keep the game a plain static folder.
2. Push. The push is the deploy.
3. Ask Claude to launch `deploy-watcher` in the background and continue with a small improvement meanwhile (for example a bigger field). Do not sit and refresh.
4. When the watcher reports, open the live URL and play: planting, harvesting, buying and reload-save should all work.
5. Check the deploy metrics on the dashboard (`python3 scripts/dashboard.py --open`).

## Done when
- [ ] The game is live on a public Cloudflare URL, deployed by pushing to git.
- [ ] You did not run a manual deploy command.
- [ ] `deploy-watcher` reported the result and a deploy is recorded in metrics.
- [ ] Tests still pass (`python3 scripts/metrics.py test`) and the dashboard shows the deploy.

## Submit as proof
Issue or Discussion titled `[challenge-4] Lift-off - <your game name>` with the live URL, repo link, dashboard screenshot showing deploys, and `python3 scripts/dashboard.py --print` output.

## Next
Challenge 5: adopt an existing build (`05-adopt.md`).
