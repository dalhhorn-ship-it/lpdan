# Challenge 7: Giveback (retro, and send a learning to the template)

> Level 7 of 7 · Time box: 1 hour · Badge: **Giveback** · Self-reported

## Goal
Close the loop: run a retrospective on your project, find something that would help every danfactory project, and send it back to the template.

## Skills you learn
- Writing down what worked and what did not.
- Telling project-specific lessons from universal ones.
- Contributing to an open-source template with a pull request.

## danfactory features used
`retro` skill (writes LEARNINGS.md and tags shared learnings `[upstream]`), `metrics` skill (metrics/REPORT.md), `scripts/upstream_learnings.py`, the decision tree and agent routing docs, the dashboard.

## Start with danfactory
Use a project that has reached at least one milestone (your farm game after Challenge 6 is ideal). The template must sit next to it for the upstream script, for example a clone at `../danfactory`:
```bash
git clone https://github.com/dalhhorn-ship-it/danfactory my-project && cd my-project && rm -rf .git && git init
```
(That is the README's new-project command; for this challenge also keep a separate plain clone of danfactory at `../danfactory`.) Run `claude` in your project, say **"let's start"**, and ask for a retro.

## Steps
1. Run the `retro` skill at the milestone. Look at the dashboard and `python3 scripts/metrics.py report` for evidence (tokens, test time, alerts).
2. Make sure at least one learning applies to every project (a decision-tree gap, a routing mistake, a policy that was unclear) and is tagged `[upstream]`.
3. From the project, send it to the template (README, verbatim):
   ```bash
   python3 scripts/upstream_learnings.py --template ../danfactory
   ```
   It appends unsent entries to the template's LEARNINGS.md, marks them `[upstreamed]`, and lists which shared docs (tree, routing, paths) differ, for you to port.
4. Open a pull request in the danfactory repo with the change, and bump the tree version if you changed the tree.
5. Regenerate the dashboard.

## Done when
- [ ] `retro` ran and LEARNINGS.md has dated entries from your project.
- [ ] At least one entry was upstreamed with the script.
- [ ] A pull request to https://github.com/dalhhorn-ship-it/danfactory exists (or an Issue proposing it, if you are not ready to code it).

## Submit as proof
Issue titled `[challenge-7] Giveback - <your handle>` with the PR link, the learning in one paragraph, a dashboard screenshot, and `python3 scripts/dashboard.py --print` output.

## You finished the ladder
Collect your badges: Spark, Sprout, Greenhouse, Lift-off, Rescue, Crew, Giveback. Badges are self-reported honour-system fun, not certificates.
