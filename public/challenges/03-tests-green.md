# Challenge 3: Greenhouse (tests and a green dashboard)

> Level 3 of 7 · Time box: 1-2 hours · Badge: **Greenhouse** · Runs on localhost · Self-reported

## Goal
Make your Challenge 2 farm game testable: add tests for the game rules, record them with danfactory's metrics, and get the dashboard's tests and coverage tiles green.

## Skills you learn
- What a test is, and why "it works on my screen" is not enough.
- Separating game rules (growth timers, coins, shop) from drawing code, so rules can be tested.
- Reading metrics and budgets.

## danfactory features used
`python3 scripts/metrics.py test`, `metrics.py report`, coverage budget in `factory.json` (the template's default minimum is 80%), the `test-runner` helper agent, the dashboard.

## Start with danfactory
Work inside your Challenge 2 project (created from the template with the README commands). Run `claude` and say **"let's start"**. Paste this challenge file or point Claude at it, and ask it to treat the work as a new milestone in BACKLOG.md. If you are starting fresh, first run the README commands:
```bash
git clone https://github.com/dalhhorn-ship-it/danfactory my-project && cd my-project && rm -rf .git && git init
```
```bash
bash scripts/bootstrap.sh "my-project" "one line description"   # flags: --codegraph, --cloudflare (auto-created Worker)
```

## Steps
1. Ask Claude to move the pure game rules (grow stages, harvest reward, buying seeds, save/load serialisation) into a module that does not touch the 3D scene.
2. Decide the test command with Claude. Use something that runs on your machine; if you have Node, its built-in test runner is a simple choice, but you do not need Node if Claude picks another approach. Make sure the command is recorded in the project's `factory.json` commands via `choose-path` (re-run it if needed).
3. Write the tests first for at least these rules: crop grows through stages by time; harvest adds the right coins; cannot buy without enough coins; save then load returns the same state.
4. Run the tests the danfactory way:
   ```bash
   python3 scripts/metrics.py test
   ```
   It prints one line when green. If it fails or the output is long, hand it to `test-runner` (Claude does this per CLAUDE.md).
5. Check coverage against the budget, then generate the report:
   ```bash
   python3 scripts/metrics.py report
   ```
6. Open the dashboard:
   ```bash
   python3 scripts/dashboard.py --open
   ```
7. Tick the backlog items and log any shortcut in `docs/TECH-DEBT.md`.

## Done when
- [ ] At least 4 meaningful tests pass via `python3 scripts/metrics.py test`, and none are skipped.
- [ ] Coverage is recorded and is at or above the budget in `factory.json` (or you explain, in TECH-DEBT.md, why not).
- [ ] The dashboard shows tests and coverage tiles populated, with no failing alert about them.
- [ ] The game still plays as in Challenge 2.

## Submit as proof
Issue or Discussion titled `[challenge-3] Greenhouse - <your game name>` with repo link, dashboard screenshot (tests and coverage visible), and the `python3 scripts/dashboard.py --print` output.

Optional self-reported bonus: coverage above the budget; weighted tokens for the session below the budget (see `metrics.py report`).

## Next
Challenge 4: ship to Cloudflare (`04-ship-cloudflare.md`).
