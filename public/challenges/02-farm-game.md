# Challenge 2: Sprout (build your first farm game)

> Level 2 of 7 · Time box: 2-3 hours · Badge: **Sprout** · Runs on localhost · Self-reported

## Goal
Build a small, original 3D farm game with coins, running from a single static folder on your own computer, using danfactory from the first message.

## Skills you learn
- Turning a brief into GOAL.md with the `brainstorm` skill.
- Picking an operating model with `choose-path`.
- Keeping a build small (time box, non-goals).

## danfactory features used
`brainstorm`, `choose-path`, the prototype-spike or software-product path, BACKLOG.md, the dashboard.

## Start with danfactory
New project (README, verbatim):
```bash
git clone https://github.com/dalhhorn-ship-it/danfactory my-project && cd my-project && rm -rf .git && git init
```
```bash
bash scripts/bootstrap.sh "my-project" "one line description"   # flags: --codegraph, --cloudflare (auto-created Worker)
```
Then run `claude`, say **"let's start"**, and paste the brief below (or tell Claude: "Use challenge-brief.md as the starting point for the goal"). Save the brief as `challenge-brief.md` in the project root first if you prefer pointing to a file. Claude walks the phases: brainstorm, then choose-path, then build.

## The standard brief (copy from here to the end of the code block)

```markdown
# Brief: a small original farm game

## Outcome
A tiny 3D farm game that runs in the browser from one static folder. The player has a field of tiles, plants seeds, waits for crops to grow, harvests them for coins, and buys more seeds. The game is original; invent your own name, art style and crops.

## Users
Me, and friends I send the folder to. Played in a desktop browser. Used for fun and to learn.

## Must-have features (keep it easy)
1. A 3D field of tiles (for example 6x6) that I can look around: orbit/zoom the camera, or walk a simple character.
2. Click a tile to plant a seed. The crop grows through at least 3 visible stages on a timer (use a short timer, 10-30 seconds, so testing is quick).
3. Click a ready crop to harvest it. Harvesting adds coins.
4. A coins counter always visible on screen.
5. A small shop: buy seeds with coins (at least 2 crop types with different cost, grow time and reward).
6. Save and load with localStorage: coins, tiles and growth progress survive a page reload. Crops keep growing while the page was closed (compute from timestamps).

## Non-goals
- No multiplayer, accounts, server or database.
- No animals, weather, quests, trading or day/night cycle.
- No mobile touch polish, no sound, no complex models: boxes, spheres and colors are fine.
- No build tools (no npm, bundler or framework). No deploy in this challenge.
- Do not copy the names, characters or art of any existing game.

## Acceptance criteria
1. Given the folder is served with `python3 -m http.server 8000`, when I open http://localhost:8000, then the 3D field renders with no console errors.
2. Given an empty tile and at least one seed, when I click the tile, then a crop appears and a seed is used up.
3. Given a planted crop, when its timer finishes, then it shows its final stage and can be harvested.
4. Given a harvest, then my coins increase by that crop's reward.
5. Given I have enough coins, when I buy seeds, then coins drop by the price and my seeds increase; given not enough coins, then nothing is bought and I see a message.
6. Given I reload the page, then coins, tiles and growth progress are restored.

## Suggested path and rigor
Path: prototype-spike at L0 (fastest, throwaway, kill/promote date) or software-product at L1 if you want to keep building. Time box: one session of 2-3 hours.

## Suggested stack (no build step)
Plain HTML + JavaScript modules in one folder (index.html, game.js, style.css). three.js loaded from a CDN with an import map, or download the single three.module.js file into the folder (vendored). Run locally with `python3 -m http.server 8000` and open http://localhost:8000 (opening index.html by double-click can block module loading).

## Definition of done
Acceptance criteria 1-6 pass by hand, GOAL.md and BACKLOG.md reflect what was built, and the dashboard is regenerated.
```

## Run it locally
In the folder with `index.html`:
```bash
python3 -m http.server 8000
```
Then open http://localhost:8000.

## Done when
- [ ] GOAL.md was written through `brainstorm` and you confirmed it.
- [ ] OPERATING-MODEL.md exists (via `choose-path`), with the path and rigor you picked.
- [ ] All six acceptance criteria in the brief pass when you play it.
- [ ] BACKLOG.md items are ticked and the dashboard is regenerated (`python3 scripts/dashboard.py --open`).

## Submit as proof
Issue or Discussion titled `[challenge-2] Sprout - <your game name>` with:
1. Repo link (or a screen recording or screenshot of the game if it stays local).
2. Dashboard screenshot.
3. Output of `python3 scripts/dashboard.py --print` in a code block.
4. One sentence: what Claude got wrong first, and how you fixed it (optional, and our favorite).

## Optional bonus ideas (self-reported)
A third crop, a day counter, a "sell all" button, a nicer camera. Do not let them break the time box.

## Next
Challenge 3: tests and a green dashboard (`03-tests-green.md`).
