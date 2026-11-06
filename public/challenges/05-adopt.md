# Challenge 5: Rescue (adopt an existing Lovable, Bolt or v0 build)

> Level 5 of 7 · Time box: 1-2 hours · Badge: **Rescue** · Self-reported

## Goal
Take a project that was built without danfactory (an app from Lovable, Bolt, v0, or any repo) and bring it under danfactory's rails without overwriting anything.

## Skills you learn
- Reading an honest as-built report of your own project.
- Using the decision tree for an existing build.
- Turning an unstructured project into a goal, a backlog and a tech-debt list.

## danfactory features used
The `adopt` skill (plugin), `docs/ADOPTION-REPORT.md`, the decision tree (Q0 adopt-existing), seeded BACKLOG.md and TECH-DEBT.md, `docs/NEXT-BUILDS.md`, the dashboard. Lovable specifics (two-way sync, Supabase RLS, moving hosting to Cloudflare) are in `docs/operating-model/paths/adopt-existing.md` in the danfactory repo.

## Start with danfactory
Get any existing build into a git repo of your own (export or sync it from the tool). Then, in a Claude Code session in that repo, install danfactory once as a plugin (README, verbatim):
```bash
/plugin install danfactory --marketplace dalhhorn-ship-it/danfactory
```
Then run:
```bash
/danfactory:adopt
```
It works on a `danfactory/adopt` branch and never overwrites your files. Without plugins, run `bash scripts/install-adopt-skill.sh` from a danfactory clone; it installs `/danfactory-adopt` for your user. Say "let's start" afterwards and let Claude tell you which phase you are in.

No existing build? Use your Challenge 2 farm game, or any small app you or a friend made.

## Steps
1. Run the adopt command above on a branch-safe repo (commit or stash your work first).
2. Read `docs/ADOPTION-REPORT.md`: origin, stack, tests, CI, hosting, security and quality findings.
3. Confirm the operating model it proposes via the decision tree, or change it with a reason.
4. Review the drafted GOAL.md (written from the as-built state). Edit it so it says what you actually want.
5. Look at the seeded BACKLOG.md and TECH-DEBT.md, and `docs/NEXT-BUILDS.md`.
6. Open the dashboard: `python3 scripts/dashboard.py --open`.
7. Review the `danfactory/adopt` branch diff before merging.

## Done when
- [ ] `docs/ADOPTION-REPORT.md` exists and you read it.
- [ ] GOAL.md, BACKLOG.md and TECH-DEBT.md exist, and you edited GOAL.md to match your intent.
- [ ] The dashboard builds for the adopted project.
- [ ] Nothing of yours was overwritten (check the branch diff).

## Submit as proof
Issue or Discussion titled `[challenge-5] Rescue - <project>` with repo link (or say it is private), dashboard screenshot, `python3 scripts/dashboard.py --print` output, and one finding from ADOPTION-REPORT.md that surprised you. Do not paste secrets or private data.

## Next
Challenge 6: a feature built with a verification team (`06-verified-feature.md`).
