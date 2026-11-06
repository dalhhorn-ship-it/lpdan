# Spec: danfactory landing page

> Status: confirmed by Dan on 2026-11-06 (see Decisions). Traces to docs/GOAL.md outcome and acceptance criteria 1-7. Facts come from /README.md and docs/operating-model/, docs/policies/. Copy is final unless Dan edits; the developer decides layout and implementation.

## Problem statement
Vibe coders who start in Lovable, Bolt, v0 or Claude hit a wall as projects grow: lost context, token burn, no tests, no traceability, deploy chaos. danfactory fixes this, but its README speaks to people who already know Claude Code. The page translates it for builders who are not pro engineers.

## User story
As a vibe coder with a growing AI-built project, I want to see in two minutes what goes wrong and how a structured workflow fixes it, so that I can start (or adopt my existing build) with copy-paste commands.

## Build constraints
Single `index.html`, inline CSS, no backend, no forms, no trackers, no third-party requests (system fonts, no CDN). Works without JS; if JS is used, only for copy buttons (progressive enhancement). Anchor nav. Tone: friendly, punchy, honest. Code blocks are verbatim from the README.

## Acceptance criteria
- Given the page loads on a 375px phone, when no scrolling happens, then the hero headline, subline and "Get danfactory on GitHub" button are visible.
- Given any code block, when compared with README.md, then it matches exactly.
- Given a visitor with JS disabled, when they read the page, then all content and links work.
- Given any numeric or feature claim, when checked against the repo, then it is true (18 agents; 8 paths plus adopt-existing; budgets 350 lines / 120k tokens).
- Given the network panel, when the page loads, then only the HTML (plus local assets) is requested.
- Given the credits section, then every project in "Credits" below is linked.
- Given the Campaign section, then it shows 7 challenge cards in order, each with level, title, one-liner, time box, skills, badge and working links to `/challenges/NN-*.md`.
- Given any challenge file, then it tells the reader to start with danfactory (README commands verbatim), say "let's start", and submit proof (repo link, dashboard screenshot, `--print` output) tagged `[challenge-N]`.
- Given the FAQ, then it works without JS (details/summary) and points to official docs by name, with no invented install URLs.
- Given the campaign copy, then scoring and badges are labelled self-reported and no prizes, rankings or participant counts are claimed.
- Given challenges 1 to 3, then they run on localhost; Cloudflare appears first in challenge 4.
- Given the farm game brief (02), then it names no existing game, title or character.

## Non-goals
Signup, forms, analytics, blog, docs mirror, testimonials, star counts, comparisons that disparage other tools.

## Sections in order (copy below)

### 0. Nav / top bar
Brand: "danfactory". Links: Why, Flow, Dashboard, Habits, Start. Button: "GitHub".

### 1. Hero
- Eyebrow: A free template for Claude Code, by Dan
- **Headline: Vibe code with Claude. Without the wall.**
- **Subline: danfactory is a free starter kit that gives your AI-built project a goal, a plan, tests, short contexts and a live dashboard, so it keeps working as it grows.**
- Primary button: Get danfactory on GitHub -> https://github.com/dalhhorn-ship-it/danfactory
- Secondary link: Jump to the 3 commands (#start)
- Trust line (true, not social proof): Free. Open on GitHub. No signup, no tracking.
- Visual: dashboard screenshot/mock (see section 7).

### 2. The problem ("The wall")
- Headline: Vibe coding is great, until the project gets big
- Subline: The first 80% feels like magic. Then this happens.
- Bullets (each: pain, then a short explainer):
  - **Claude forgets.** Every chat has a "context": the text the AI can see right now. Long ones get fuzzy and expensive.
  - **Tokens burn.** Tokens are the small pieces of text you pay for. Re-reading the same big files every turn is how bills grow.
  - **Nothing is tested.** No checks means every change might quietly break something else.
  - **Nobody knows what was built.** No goal, no backlog, no record of why. You can't answer "where are we?"
  - **Deploys are chaos.** Push, wait, guess if it worked, repeat.
- Closer: danfactory is a set of rails for exactly these five problems. Not a framework. A template you own.

### 3. Why it exists / who it's for
- Headline: Built by Dan, for builders
- Body: "Dan built danfactory to start Claude Code projects with a guided plan instead of a blank prompt, and is sharing it back with the community for free." (Developer: keep this to what the README says: a template for starting Claude Code projects with a guided start, token savings, indexed docs, delivery metrics, on-request security audits and Cloudflare deploys via git. Dan may add a personal line.)
- "It's for you if":
  - You started in Lovable, Bolt, v0 or Claude and your project is outgrowing the chat.
  - You build with AI but aren't a professional engineer, and want guardrails, not a lecture.
  - You use Claude Code and want leaner sessions and numbers you can see.
- "Probably not for you if": you need a hosted product or support. This is a template you run yourself, and needs git and python3.

### 4. How it works: 3 phases
- Headline: Three phases, in order. No code until the goal is agreed.
- Subline: Say "let's start" and Claude knows which phase you're in.
- Cards (from the README flow table):
  1. **Agree the goal.** The `brainstorm` skill talks it through with you. Output: `docs/GOAL.md`.
  2. **Choose how to work.** The `choose-path` skill walks a decision tree and a rigor dial (L0 throwaway to L3 money/PII/public). Output: `docs/OPERATING-MODEL.md`, `factory.json`, an ADR (a short note on why you decided).
  3. **Build.** Follow the path playbook with subagents. At milestones, `retro` and `metrics` record what you learned.
- Callout: Rigor dial: L0 throwaway and just you; L1 personal, low risk; L2 others depend on it; L3 money, personal data, public internet. The highest signal wins.
- Also on demand: `security-audit-run` (audit report) and `ship` (live deploy).

### 5. The agent team
- Headline: 18 agents, but not all at once
- Subline: Cheap models do the heavy reading. Smart models make the calls. A routing table decides who works when.
- Table (README):
  - Plan & design: product-manager, software-architect (Opus), spreadsheet-architect
  - Build: developer, code-writer, data-builder
  - Cheap helpers (Haiku): bulk-reader, test-runner, doc-keeper, deploy-watcher, claude-md-compliance-checker
  - Verify: reviewer, task-completion-validator, code-quality-pragmatist, karen, jenny, ui-comprehensive-tester
  - Debug: ultrathink-debugger (Opus, only after a failed first attempt)
- Bullet: A verification ladder decides how many checkers a task gets: none at L0, up to five at L3.
- Small print: "Subagent = a helper Claude with its own fresh context that returns a short answer." Verifiers and debugger adapted from darcyegb/ClaudeCodeAgents (MIT).

### 6. Paths
- Headline: A spreadsheet isn't run like a SaaS app
- Subline: Eight paths, each with its own playbook.
- Table (README): software-product (apps, APIs, services: vertical slices, TDD, CI, git to Cloudflare); library-cli (packages, SDKs, CLIs: API-first, semver, examples as tests); data-spreadsheet (workbooks, models, CSV/reports: generator scripts + xlsx skill); documents-content (docs, decks, handbooks: outline-first); research-analysis (deep-research fan-out, sources ledger); automation-script (idempotent, dry-run, cron on Cloudflare); infra-ops (plan/apply split, least privilege); prototype-spike (time-box, kill/promote date).
- Note: "TDD = write the test first, then the code that passes it. A vertical slice = one thin piece that works end to end."

### 7. Dashboard / traceability (hero feature)
- Headline: See where your project actually is
- Subline: Every build regenerates a single-page dashboard from your own files. No account, no service.
- Bullets:
  - **Versions and phase/progress.** Know which phase you're in and how far along.
  - **Backlog.** Read straight from `docs/BACKLOG.md`.
  - **Tech debt.** Shortcuts you chose on purpose, from `docs/TECH-DEBT.md`.
  - **Key metrics.** Tests, coverage, deploys, tokens, with alerts when budgets are breached.
  - **Roadmap tab.** The proposed sequence as two swimlanes: user value vs technical foundation, so you can see if you're only shipping features and neglecting the base.
- Traceability line: Goal -> backlog item -> tests -> deploy -> metrics, all in plain files in git.
- Code: `python3 scripts/dashboard.py --open   # build + open the project dashboard`
- Cheap text version: `python3 scripts/dashboard.py --print`
- Developer note: use a real screenshot of a generated dashboard (run the script on a sample project) or a faithful mock captioned "Example dashboard". Do not show invented real-project numbers without the caption.

### 8. Token economy and short contexts
- Headline: Spend tokens on decisions, not on moving bytes
- Subline: Short contexts, cheap helpers, and a guard that stops Claude loading giant files.
- Bullets:
  - Read the docs index first, then only the lines you need.
  - A hook blocks whole reads of files over 350 lines unless a slice is requested.
  - Big reads, test logs and deploy watching go to cheap Haiku helpers.
  - At logical boundaries the `handoff` skill writes a note (40 lines or fewer); run `/clear` and the note reloads automatically.
  - A nudge appears once context passes 120k tokens; a snapshot is saved before any compaction.
  - Tokens per session are recorded, with a weighted budget so you see real cost.
- Research aside (attributed): NVIDIA's "You don't need long context" kept agents within about 2 points of full history by compacting often; in one setting, 70.2% vs 70.0% on SWE-bench Verified with Claude Opus 4.5. "This is one reported setting, not a promise for your project."
- Explainer: "Context = what Claude can see right now. Compacting = summarising it to make room."

### 9. Vibe coding with Claude: 7 habits
- Headline: 7 habits that make vibe coding last
- Subline: Good habits first; the template makes them the default.
1. **Agree a goal first.** Write what "done" means before any code. (`brainstorm` -> GOAL.md; no code until it's confirmed.)
2. **Pick an operating model.** A prototype and a payment app need different care. (`choose-path` and the rigor dial.)
3. **Keep contexts short, hand off often.** One task per session; save a note, `/clear`, continue. (`handoff`, context-watch.)
4. **Delegate big reads.** Don't make the smart model read logs. (`bulk-reader`, `test-runner`, file-size guard.)
5. **Test before you call it done.** "Done" means tests pass, docs updated, backlog ticked. (Definition of done in CLAUDE.md; `metrics.py test`.)
6. **Push and keep going.** A push is the deploy; a background watcher reports back with bounded waits. (`ship`, `deploy-watcher`, async-delivery policy.)
7. **Retro, and feed learnings back.** At milestones write down what worked, tag shared lessons `[upstream]`, send them to the template. (`retro`, `upstream_learnings.py`.)

### 9b. Campaign: the Vibe Ladder (id="campaign")
Placed after the 7 habits and before Adopt. Each challenge is done with danfactory (start from the template or adopt, brainstorm -> choose-path -> build, dashboard as proof). Challenge files are served from `/challenges/NN-*.md` (source: public/challenges/) as links and downloads.

- Headline: Learn by shipping: the Vibe Ladder
- Subline: Seven small challenges, from "does my laptop work?" to "I improved the template". Each one teaches a skill, each one is done with danfactory, and you prove it with your own dashboard.
- Intro line: Free, for fun, honour system. No signup, no leaderboard service, no prizes promised.

**Ladder cards** (each card: level, title, one-liner, time box, skills, badge, buttons "Read the challenge" and "Download .md"):
1. **Set up: git + Claude Code + danfactory.** Get your tools working and see your first dashboard. 30-45 min. Skills: terminal, git, starting Claude Code. Badge: Spark. File: 01-setup.md
2. **Your first farm game.** Plant, grow, harvest, earn coins in a small original 3D world, running on localhost. Includes a ready-made brief that seeds your goal. 2-3 h. Skills: briefing, goal setting, small builds. Badge: Sprout. File: 02-farm-game.md
3. **Tests and a green dashboard.** Test the game rules and get tests and coverage on the dashboard. Localhost. 1-2 h. Skills: testing, TDD, metrics. Badge: Greenhouse. File: 03-tests-green.md
4. **Ship to Cloudflare via git.** Push is the deploy; a background watcher reports. 1-2 h. Skills: deploys, not waiting. Badge: Lift-off. File: 04-ship-cloudflare.md
5. **Adopt an existing build.** Bring a Lovable, Bolt or v0 project (or any repo) under danfactory with `/danfactory:adopt`. 1-2 h. Skills: reading an audit, backlog and tech debt. Badge: Rescue. File: 05-adopt.md
6. **A feature with a verification team.** One L2 feature with spec, reviewer, validator, karen and jenny. 2-4 h. Skills: specs, delegation, verification. Badge: Crew. File: 06-verified-feature.md
7. **Retro and give back.** Run a retro and send an `[upstream]` learning to the template. 1 h. Skills: retros, open-source contribution. Badge: Giveback. File: 07-retro-upstream.md

Note under the ladder: "Challenges 1 to 3 run on localhost (for example `python3 -m http.server 8000` in your game folder, then open http://localhost:8000). Cloudflare comes in challenge 4."

**How to compete / submit**
- Headline: Show your work, honestly
- Steps: 1. Do the challenge with danfactory. 2. Open a GitHub Issue (or Discussion, if enabled) on dalhhorn-ship-it/danfactory titled `[challenge-N] <name> - <your project>`. 3. Include: repo link, a dashboard screenshot, and the output of `python3 scripts/dashboard.py --print` (that is the `dashboard/SUMMARY.md` table).
- Code: `python3 scripts/dashboard.py --print`
- Optional fun scoring (self-reported): one badge per challenge; bonus points for green tests, coverage at or above the budget, and low weighted tokens per session (from `python3 scripts/metrics.py report`). "Everything is self-reported. The dashboard is your receipt, not a lie detector."
- Button: Open the challenge board on GitHub (Issues page, link below).

**Help line**
- Headline: Stuck? Ask in public
- Body: "No phone, no email. Open an Issue at https://github.com/dalhhorn-ship-it/danfactory/issues titled `[challenge-N] help: <problem>` with your operating system, the command, and the exact error."

**FAQ** (accordion; use `<details>`, which works without JS)
- Q: git says "command not found". A: Install git from the official git site (git-scm.com) or your package manager, then open a new terminal.
- Q: python3 is missing. A: Install Python 3 from python.org or your package manager. Check with `python3 --version` (on some systems the command is `python`). The template uses only the standard library.
- Q: Claude Code won't start or asks me to log in. A: Run `claude` and follow the login prompt. Install and account requirements are in the official Claude Code docs; check there, they change.
- Q: I'm on Windows. A: The scripts are bash. WSL (Windows Subsystem for Linux) is the simplest route; see Microsoft's WSL docs and the Claude Code docs. Work inside the WSL terminal.
- Q: `bootstrap.sh: Permission denied`. A: Run it as `bash scripts/bootstrap.sh "my-project" "one line description"`; no executable bit needed.
- Q: Where is the dashboard? A: `dashboard/index.html` in your project. `python3 scripts/dashboard.py --open` builds and opens it; `dashboard/SUMMARY.md` is the text version.
- Q: My game page is blank on localhost. A: Serve the folder with `python3 -m http.server 8000` and open http://localhost:8000 instead of double-clicking the file; check the browser console for errors.
- Q: Why did `git init` start empty history? A: On purpose: `rm -rf .git && git init` gives you your own history, not the template's.

### 10. Adopt an existing Lovable / Bolt / v0 build
- Headline: Already built something? Bring it along
- Subline: Install danfactory as a Claude Code plugin and run one command inside your repo. It works on a `danfactory/adopt` branch and never overwrites your files.
- Code (verbatim):
```bash
/plugin install danfactory --marketplace dalhhorn-ship-it/danfactory
```
```bash
/danfactory:adopt
```
- What happens (README): 1. Scans origin, stack, tests, CI, hosting, security and quality findings into `docs/ADOPTION-REPORT.md`. 2. Uses the decision tree to choose the operating model. 3. Installs hooks, agents, skills, scripts, the docs index and CI; merges settings, `CLAUDE.md` and `.gitignore`. 4. Drafts GOAL.md from the as-built state, seeds BACKLOG.md and TECH-DEBT.md, builds the dashboard, writes `docs/NEXT-BUILDS.md`.
- Note: Lovable specifics (two-way sync, Supabase RLS, moving hosting to Cloudflare) are in `docs/operating-model/paths/adopt-existing.md`. Without plugins: `bash scripts/install-adopt-skill.sh` from a danfactory clone installs `/danfactory-adopt`.

### 11. Get started in 3 commands (id="start")
- Headline: Start in three commands
- Subline: Needs git and python3. That's it (Node only for optional extras).
- Code (verbatim):
```bash
git clone https://github.com/dalhhorn-ship-it/danfactory my-project && cd my-project && rm -rf .git && git init
```
```bash
bash scripts/bootstrap.sh "my-project" "one line description"   # flags: --codegraph, --cloudflare (auto-created Worker)
```
```bash
claude
```
- Then: say **"let's start"**. The SessionStart hook tells Claude which phase you're in.
- Alt: On GitHub click **Use this template -> Create a new repository** (only if Dan has enabled the template setting).
- Handy commands: `bash scripts/check.sh`, `python3 scripts/metrics.py test`, `python3 scripts/dashboard.py --open`.
- CTA button repeated: Get danfactory on GitHub.

### 12. Credits
- Headline: Standing on open-source shoulders
- Subline: danfactory borrows good ideas. Thank you to:
  - darcyegb/ClaudeCodeAgents (MIT): the verifier and debugger agents - https://github.com/darcyegb/ClaudeCodeAgents
  - Spotify shunt: the delegation idea behind the large-read guard - https://github.com/spotify/portal-ai-plugins/tree/main/plugins/shunt
  - codegraph by colbymchenry: local code graph - https://github.com/colbymchenry/codegraph
  - cloudflare/security-audit-skill: on-request audits - https://github.com/cloudflare/security-audit-skill
  - davila7 cloudflare-deploy skill: git-to-Cloudflare deploys - https://github.com/davila7/claude-code-templates/blob/main/cli-tool/components/skills/development/cloudflare-deploy/SKILL.md
  - NVIDIA, "You don't need long context": short contexts and handoff notes

### 13. Footer
"danfactory is a free community give-back from Dan. Not affiliated with Anthropic, Lovable, Bolt, v0 or Cloudflare. No cookies, no tracking." Links: GitHub repo, Issues (https://github.com/dalhhorn-ship-it/danfactory/issues), back to top. Do not state a license until Dan confirms one.

## Truth rules for the developer
- Use only the numbers above. Do not add star counts, users, "trusted by", or performance claims about savings (the repo measures tokens but promises no percentage).
- Repo docs live under `docs/operating-model/` (AGENT-ROUTING, DECISION-TREE, paths) and `docs/policies/`.

## Scope cuts (recommended)
- Cut from the campaign: leaderboard, automated verification of submissions, user profiles, a badge-image generator (badges are text names on the page), and a challenge-8+ ladder.
- Cut: animated demos, video, blog, translations, dark mode toggle, live GitHub API stats (a third-party request and an inviting fake-proof risk). Pushed to M2.
- Cut: full per-agent and per-path pages; link to the repo.
- Cut: a hosted "try it" playground; needs a backend.
- Keep: dashboard visual, 7 habits, and the two copy-paste blocks. They carry the value.

## Decisions (Dan, 2026-11-06)
- PRD approved. Status: confirmed.
- Campaign: GitHub Issues only (no Discussions), honour system, no prize. Help line: GitHub Issues only, no phone/email; no response time promised.
- Challenge 4: the page does not claim Cloudflare is free.
- Challenge 3: no test runner named; Claude picks it during `choose-path`.
- Other open points accepted at their defaults: no license stated until Dan adds one; "Use this template" shown only as optional ("if enabled"); no personal line for now; no traffic measurement; a `*.workers.dev` URL until a domain is chosen; dashboard visual = labelled sample mock + real day-one screenshot.
- Challenge files in public/challenges/ are the source of truth and ship unchanged.
