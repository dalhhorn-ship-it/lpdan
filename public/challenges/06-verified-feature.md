# Challenge 6: Crew (a feature at L2 with a verification team)

> Level 6 of 7 · Time box: 2-4 hours · Badge: **Crew** · Self-reported

## Goal
Add one real feature to your project at rigor L2 ("others depend on it, lives months+"), using danfactory's agents: plan, design, build, then independent checkers.

## Skills you learn
- Writing a spec with testable acceptance criteria.
- Delegating to subagents (separate helper Claudes with fresh contexts).
- Why independent verification beats "it looks done".

## danfactory features used
Rigor dial (L2), `product-manager`, `software-architect`, `developer`, the verification ladder (docs/operating-model/AGENT-ROUTING.md): `test-runner`, `reviewer` before merge, `task-completion-validator` for M/L items, `code-quality-pragmatist` if a new abstraction or a large diff, `ui-comprehensive-tester` if UI touched; at milestone end `karen`, and `jenny` when the spec has more than about 5 acceptance criteria.

## Start with danfactory
Use your farm game (or any danfactory project). Run `claude`, say **"let's start"**, and ask Claude to set the rigor to L2 for this milestone (re-run `choose-path` if OPERATING-MODEL.md says otherwise). New project? README commands: `git clone https://github.com/dalhhorn-ship-it/danfactory my-project && cd my-project && rm -rf .git && git init` then `bash scripts/bootstrap.sh "my-project" "one line description"`.

## Suggested feature (farm game)
A "market": crop prices change on a timer, and a sell screen lets you sell harvested crops (instead of auto-coins). More than 5 acceptance criteria on purpose, so `jenny` joins the milestone check. Any equally sized feature of your own is fine.

## Steps
1. Ask `product-manager` to add the feature to BACKLOG.md as an M item with a spec in `docs/specs/<slug>.md` (problem, user story, Given/When/Then criteria, non-goals).
2. Ask `software-architect` for a short design (the template routes risky or large features to it at L2+). Record the decision as an ADR in `docs/decisions/` if it is a real choice.
3. Have `developer` build it in vertical slices with tests first. Keep checking with `python3 scripts/metrics.py test`.
4. Run the L2 ladder: `reviewer` before merge, `task-completion-validator` on the item, `ui-comprehensive-tester` if the UI changed.
5. At milestone end, ask for `karen` (does the whole thing really work?) and `jenny` (does it match the spec?).
6. Update docs (`docs-sync`), tick the backlog, log shortcuts in TECH-DEBT.md, open the dashboard.

## Done when
- [ ] A spec with at least 5 Given/When/Then criteria exists in `docs/specs/`.
- [ ] Tests pass and coverage meets the budget.
- [ ] `reviewer`, `task-completion-validator`, `karen` and `jenny` each ran and you can state one finding from each (or "no findings").
- [ ] BACKLOG item ticked; dashboard regenerated.

## Submit as proof
Issue or Discussion titled `[challenge-6] Crew - <feature>` with repo link, link or paste of the spec, dashboard screenshot, `python3 scripts/dashboard.py --print` output, and the list of agents you ran with one-line findings.

## Next
Challenge 7: retro and give back (`07-retro-upstream.md`).
