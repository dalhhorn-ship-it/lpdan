# Claims list: landing page sections for danfactory v0.2.0 (UPD-3, UPD-4)

> Every claim in the "From supervised to gated autonomy" (`#autonomy`) and "Worked example" (`#example`) sections of public/index.html, and in "New in v0.2.0" (`#safely`), mapped to a file and line in the danfactory repo at tag v0.2.0, commit 7428d462441c3faaef6e006e51f405f26620559f. Re-checked at the tag on 2026-11-15 (first written against 4c6a68d, which is not in danfactory's history any more; rows were checked by text). Specs: [template-update-v0-2-0.md](specs/template-update-v0-2-0.md), [landing-v0-2-0-features.md](specs/landing-v0-2-0-features.md). Numbers in `#safely` are tested by tests/check_page.py against tests/fixtures/danfactory-v0-2-0-facts.json (extracted at the tag). README lines are also in tests/fixtures/danfactory-README.md.

## From supervised to gated autonomy

| Claim on the page | danfactory source |
|---|---|
| The autonomy pack is optional; new projects start without it | README.md:91, 93 |
| You approve the PRD: no approved PRD, no product code; a hook blocks the edit | README.md:86; docs/policies/prd-approval.md:26-27; .claude/hooks/guard_prd_write.py |
| The merge gate checks it again on every product-code commit | README.md:86; docs/policies/merge-gate.md:21 (check `prd`: product-code commits in range) |
| You start the builds; nothing starts a run for you | docs/policies/runner.md:10 ("You start every run; nothing starts one for you") |
| Within an attempt limit and a daily budget | docs/policies/runner.md:8 (`max_attempts` 3, `daily_budget_usd` 5); README.md:104 |
| Fixes merge to a `staging` branch only | README.md:104; docs/policies/runner.md:22 |
| The release report prints the exact commands and you run them; nothing reaches main by itself | README.md:105; docs/policies/runner-release.md:5-8 |
| Agents write acceptance tests from your PRD | .claude/agents/test-writer.md:3; docs/policies/prd-approval.md:19 |
| Agents file an issue for each root cause of the failing tests | .claude/agents/finder.md:3; README.md:62 |
| A fixer fixes it in a sandbox | docs/policies/runner.md:18, 20 |
| A second agent reviews the fix | docs/policies/runner.md:20; README.md:104 |
| It passes through the merge gate | README.md:48; docs/policies/runner.md:21; docs/policies/merge-gate.md:17-21 |
| This site does not use the pack (static page, no acceptance suite) | lpdan factory.json `packs.autonomy` false; PRD non-goals |
| Link: How the pack works | README.md:91 (heading "Autonomy pack") |

The diagram repeats the same seven steps: approve PRD (human), write tests, file issues, start build (human), fix/review/gate, merge to staging only, push to main (human).

## Worked example (pilot 2, evals/spikes/pilot-semverlite/README.md)

| Claim on the page | Source line |
|---|---|
| Library project made from the template; 10-criterion PRD of Semantic Versioning 2.0.0 | README:3-4 |
| After the PRD the runs were unattended | README:6 ("What ran, unattended after the PRD") |
| 11 tests written from the PRD, covering all 10 criteria | README:9 ("11 tests, 10/10 criteria mapped") |
| All 11 admitted: fail before the build, pass on an independent implementation | README:10 |
| Second reading cost 0.07 USD | README:10 |
| Fixed the one issue on attempt 1 for 0.22 USD; gate pass, review ship, merged to staging, main untouched | README:12 |
| 0.29 USD of useful work (0.22 + 0.07) | README:26 ("useful work 0.29 USD"); the sum is arithmetic on lines 10 and 12 |
| 2.72 USD on six runs that failed for template reasons, each since fixed with a test | README:17-24. Note: the runner log shows 12 failed attempts in 4 parked runs (2.7214 USD); "six" is the README's wording and matches the six fixes listed. Upstream inconsistency, reported to Dan 2026-11-15. |
| Failures such as hook caches counted as tampering and a stale docs index on staging | README:18 (item 1), README:20 (item 3) |
| 3.01 USD of the 5 USD daily cap in all | README:26 |
| After the merge 11 of 11 pass; none of 12 invalid strings accepted, including ones the tests do not cover | README:14 |
| Evidence folder: PRD, tests, runner log, whole repo as a git bundle | files prd-semver-core.md, test_semver_core_agent_written.py, runner-2026-11-13.jsonl, pilot-semverlite.bundle; README:28-33 |
| Link target | https://github.com/dalhhorn-ship-it/danfactory/tree/main/evals/spikes/pilot-semverlite |

## New in v0.2.0 (`#safely`, UPD-4)

| Claim on the page | danfactory source (v0.2.0) |
|---|---|
| Agents do the middle; you keep three controls | docs/decisions/0010-release-train-parallel-fixers-learning.md:6; runner.md:10; runner-release.md:6 |
| PRD write guard blocks the edit, shell writes too | .claude/hooks/guard_prd_write.py; docs/policies/prd-approval.md:26-27 |
| Gate re-checks product-code commits | docs/policies/merge-gate.md:21 |
| A waiver must quote your own words | docs/policies/prd-approval.md:28 |
| One command, one verdict with reason codes, same locally and in CI | docs/policies/merge-gate.md:6 (`python3 scripts/gate.py`); .github/workflows/ci.yml:8, 24 |
| Eleven checks, from structure to size | scripts/gate.py:412-414 (`CHECKS`) |
| Test writer turns each PRD criterion into a test | .claude/agents/test-writer.md:16-17, 19 |
| From rigor L2, admitted only if fails before the build and passes on an independent second implementation | docs/policies/merge-gate.md:36 |
| Open points come back as PRD questions | .claude/agents/test-writer.md:19 |
| Failing tests become issue files, one per root cause | docs/policies/issue-ledger.md:14, 17; .claude/agents/finder.md:3 |
| Fixed ones move to `issues/fixed/`, a regression reopens | docs/policies/issue-ledger.md:7 |
| One sandboxed agent per attempt, without network | docs/policies/runner.md:5, 17, 18, 20 |
| A read-only agent reviews, the gate decides | docs/policies/runner.md:20, 21 |
| At most 3 attempts per issue, 5 USD a day, 2 USD a run | factory.json:78-80; docs/policies/runner.md:8 |
| 4 fixers in parallel (hard cap; default 1) | factory.json:84; docs/policies/runner.md:27 |
| Fixes merge to `staging` only | docs/policies/runner.md:22; runner-release.md:6 |
| Staging re-verified as a batch; report prints the exact commands; you promote | docs/policies/runner-release.md:7, 8, 11-13 |
| Failed smoke test prepares a revert branch and an issue | docs/policies/runner-release.md:16 |
| Recurring rejection reasons become candidate rules for the retro; evals check the fixers | docs/policies/runner-release.md:19 |
| Autonomy pack: 36 files, about 5,100 lines, only if you choose autonomy | packs/autonomy.json (36 files, 5,098 lines counted at the tag); scripts/bootstrap.sh:77; README.md:93-99. The brief said "about 4,800"; ADR 0011 says "about 4,500"; the page uses the count. |
| Size budgets flag big files, growth and heavy docs on the dashboard | factory.json:46-54; README.md:46, 87 |
| New projects start without autonomy | README.md:93; factory.json:76 |
| Diagram: same flow and six layers as the brief; fixer box says "one sandboxed agent per attempt" (the brief's "one agent per issue" is not what runner.md says) | runner.md:5, 17 |

Also refreshed to 4c6a68d: the bootstrap command line in the "start in three commands" section (README.md:13, now lists `--with-autonomy` and `--template-ref`).
