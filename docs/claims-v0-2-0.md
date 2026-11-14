# Claims list: landing page sections added for danfactory v0.2.0 (UPD-3)

> Every claim in the "From supervised to gated autonomy" (`#autonomy`) and "Worked example" (`#example`) sections of public/index.html, mapped to a file and line in the danfactory repo at commit 4c6a68d1ab484b66fa2d5563da71e7916512d449 (main; the v0.2.0 tag was not yet cut). Spec: [template-update-v0-2-0.md](specs/template-update-v0-2-0.md). README lines are also in tests/fixtures/danfactory-README.md.

## From supervised to gated autonomy

| Claim on the page | danfactory source |
|---|---|
| The autonomy pack is optional; new projects start without it | README.md:91, 93 |
| You approve the PRD: no approved PRD, no product code; a hook blocks the edit | README.md:86; docs/policies/prd-approval.md:3; .claude/hooks/guard_prd_write.py |
| The merge gate checks it again on every commit | README.md:86; docs/policies/merge-gate.md:21 (check `prd`) |
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
| 2.72 USD on six runs that failed for template reasons, each since fixed with a test | README:17-24 |
| Failures such as hook caches counted as tampering and a stale docs index on staging | README:18 (item 1), README:20 (item 3) |
| 3.01 USD of the 5 USD daily cap in all | README:26 |
| After the merge 11 of 11 pass; none of 12 invalid strings accepted, including ones the tests do not cover | README:14 |
| Evidence folder: PRD, tests, runner log, whole repo as a git bundle | files prd-semver-core.md, test_semver_core_agent_written.py, runner-2026-11-13.jsonl, pilot-semverlite.bundle; README:28-33 |
| Link target | https://github.com/dalhhorn-ship-it/danfactory/tree/main/evals/spikes/pilot-semverlite |

Also refreshed to 4c6a68d: the bootstrap command line in the "start in three commands" section (README.md:13, now lists `--with-autonomy` and `--template-ref`).
