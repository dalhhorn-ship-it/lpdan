# PRD: Agents navigate docs index-first

> Status: draft · 2026-11-07 · Owner: product-manager · Backlog: M1 / "Agents navigate docs index-first" (#process)

## Problem
The main agent is told to read docs/INDEX.md first and use offset/limit reads (CLAUDE.md, session_start hook, token-economy.md lines 6-10). 9 of 19 subagents never mention the index (developer, reviewer, product-manager, code-writer, bulk-reader, test-runner, data-builder, spreadsheet-architect, deploy-watcher). The large-read guard deliberately lets subagents through, so they can read whole big files. This session delegations stayed directed only because briefs named files and lines. That is luck, not a rule. Also, docs/knowledge-graph.json (104 edges) is used by no agent, so finding neighbouring docs means reading files.

## Goal and success measure
Supports the GOAL.md token-spend and context-loss pain. Success: subagents start from the index; neighbours are found without file reads. Measured cheaply: (a) a test that every in-scope agent mentions docs/INDEX.md; (b) count of whole >350-line reads inside subagents and weighted tokens per session (metrics/tokens.jsonl), compared over the 5 sessions before and after. Expect a modest effect; report it honestly, including "no change".

## Users and user stories
- As Dan, I want subagents to find docs the cheap way so that delegation costs less without longer briefs.
- As an agent, I want to list a doc's neighbours with summaries so that I read only what is relevant.

## Scope
1. One shared line (about 25 words) in the 7 agents that read or write docs/code: developer, reviewer, product-manager, code-writer, data-builder, spreadsheet-architect, bulk-reader: "Find things via docs/INDEX.md; read at the file:line it lists; for files over 350 lines use offset/limit." bulk-reader gets a variant (summarise, don't dump).
2. `python3 scripts/docs_index.py --related <doc>`: prints docs linking to and from it, one line each with summary, from docs/knowledge-graph.json. Mentioned once in token-economy.md and in the same agent line.
3. Measurement note in docs/policies/token-economy.md (what to compare, no new tooling).

## Non-goals
- test-runner and deploy-watcher: they run commands and read logs, not docs. Cut: the line is pure prompt cost.
- Subagent read budget or block (soft warning too): risks slowing agents and fighting the "disposable context" design. Revisit only if measurement shows whole large reads persist.
- Enabling codegraph; changing the main-agent guard; new dashboards.

## Acceptance criteria
1. Given the 7 in-scope agent files, when the test runs, then each contains "docs/INDEX.md" and the test fails if one is removed.
2. Given a fixture graph, when `--related a.md` runs, then it lists exactly the docs linked to or from a.md, each with its summary, sorted, and exits 0.
3. Given a doc with no edges, when `--related` runs, then it prints "no related docs" and exits 0.
4. Given an unknown doc path, when `--related` runs, then it exits non-zero with a clear message.
5. Given a stale graph (older than docs), when `--related` runs, then it warns to regenerate.
6. token-economy.md references `--related`; `bash scripts/check.sh` and `python3 scripts/metrics.py test` pass.

## UX / behaviour notes
Output is plain text, at most about 20 lines; truncated with a count when longer.

## Risks and assumptions
- Riskiest: agents ignore the line. Test cheaply by checking, after a few sessions, whether subagent whole large reads drop; if not, the prompt text was the wrong lever.
- Prompt bloat is paid on every delegation: hence one short line and only 7 agents.
- A stale index misleads: `--related` warns; check.sh already regenerates.

## Effort and sequencing
S-M (about half a day). Foundation lane, no dependencies. Slice 1: agent lines plus test. Slice 2: `--related` plus test. Build here first (dogfood for a few sessions, gather measurement), then upstream to danfactory as one branch and PR, since template files are shared and a measured result makes a better PR.

## Open questions
1. Agree to skip test-runner and deploy-watcher?
2. Build here first then upstream, or upstream first?
3. Is a 5-session before/after comparison enough evidence, or drop measurement?
