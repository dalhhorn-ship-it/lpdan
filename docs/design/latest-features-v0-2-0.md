# Latest features: danfactory v0.2.0 (brief for the landing page)

> Source of truth: danfactory tag v0.2.0 (commit 7428d46). Every line below is checkable in that repo; keep claims to what is here. Claims map: docs/claims-v0-2-0.md.

## In one line
Agents do the middle of the work on their own; you keep three controls: **approve the PRD, start the builds, push to main.**

## What's new
- **PRD write guard.** No approved PRD, no product code: a hook blocks the edit (also shell writes), and the merge gate checks every commit again. Waivers must quote your own words.
- **Merge gate.** One command, one verdict with reason codes, same locally and in CI: structure, build, lint, tests, coverage, acceptance, protected paths, PRD, review, security, size.
- **Locked acceptance tests.** A test-writer agent turns each PRD criterion into a test. A test is admitted only if it fails before the build and passes on an independent second implementation; open points come back to you as PRD questions. Builders cannot edit these tests.
- **Issue ledger.** Failing tests become issue files, one per root cause; fixed ones move to `issues/fixed/`, regressions reopen.
- **Fixer runner (optional autonomy pack).** One fresh agent per issue in a sandbox with no keys and no network; a separate read-only agent reviews; the gate decides. Max 3 attempts per issue, 5 USD per day, 2 USD per run, up to 4 fixers in parallel. Fixes merge to `staging` only.
- **Release train.** Staging is re-verified as a batch; a report prints the exact commands; you promote to main. A failed smoke test prepares a revert branch and an issue.
- **Learning loop.** Recurring rejection reasons become candidate rules for your retro; evals check the fixers' behaviour.
- **Lean by default.** The autonomy pack (about 4,800 lines) is only installed when you choose autonomy mode. Size budgets flag big files, growth and heavy docs on the dashboard.
- **Proven, not promised.** Pilot: a semver library from a 10-criterion PRD, fixed on attempt 1 for 0.22 USD (evidence in danfactory `evals/spikes/pilot-semverlite/`).

## Prompt for the visual (article-style system diagram)

```
Create a clean, hand-drawn-style system diagram (like an engineering whiteboard sketch: rounded boxes with
slightly sketchy outlines, diagonal-hatched or dashed borders per group, small icons, short labels, thin
arrows with tiny lowercase labels). Landscape 16:9, generous white space, readable at 1200 px wide.
Background #0B0B2E (deep navy). Text #FFFFFF, secondary text #B9B9DC. Human-owned items in magenta
#E6007E with white text. Agent teams in raised navy #17174A boxes with colored hatched borders: test
writers lavender #9B7BFF, issue finders cyan #2EE6F5, fixers violet #3D2CE0. Gates and checks in yellow
#F5C400 outlines. Arrows cyan #2EE6F5. No logos, no people, no extra text beyond the labels below.

Title (top left): "How danfactory builds with agents, safely"
Subtitle: "Agents do the middle. You keep three controls."

Top row, left to right:
1. Magenta box "You approve the PRD" (icon: checkmark on a document) -> arrow labelled "locked criteria"
2. Lavender-hatched team box "Test writers" — "write acceptance tests from the PRD; admitted only if they
   fail first and pass on an independent second reading" -> arrow "admitted tests"
3. Cyan-hatched team box "Issue finders" — "replay the tests, file one issue per root cause"
   -> arrow "one issue each"
4. Violet-hatched team box "Fixers" — "one agent per issue, in a sandbox: no keys, no network;
   max 3 attempts, 5 USD/day" -> arrow "fix"
5. Small box "Independent reviewer (read-only)" -> arrow "verdict"

Middle: a wide yellow-outlined box "Merge gate" with a row of small chips:
structure · build · lint · tests · coverage · acceptance · protected · PRD · review · security · size.
Arrow from the gate back to "Fixers" labelled "rejected: reasons, rework". Arrow forward labelled
"pass" to a box "staging branch (fixes stack up)".

Bottom band (full width, dashed outline): "Shared repository" containing three small items:
"acceptance tests (locked)" with a padlock icon, "issues/open · issues/fixed" as two folder icons
(red tint and green tint), "rules & evals" with a gear icon.

Right column, top to bottom (a separate lane like a release pipeline):
"Release train: re-verify staging as a batch" -> "Release report (exact commands)" -> magenta box
"You push to main" -> small box "Deploy". A dashed arrow from "Deploy" back to "Issue finders" labelled
"failed smoke -> revert branch + new issue".

A thin curved arrow from the Merge gate down to "rules & evals" labelled "recurring rejections ->
candidate rules", and from "rules & evals" back up to the agent teams labelled "learning loop".

Left margin, a vertical legend titled "Layers of safety" with 6 numbered stacked bars, darkest at the
bottom: 1 PRD write guard, 2 locked acceptance tests, 3 sandboxed fixers + caps, 4 independent review,
5 merge gate, 6 staging + you push to main.
Small footer, muted: "Autonomy is optional: new projects start without it."
```

Alt text for the image: "Diagram: you approve the PRD; test writers, issue finders and fixers work through a merge gate to a staging branch; you push to main. Six layers of safety: PRD write guard, locked tests, sandboxed fixers with caps, independent review, merge gate, staging."
