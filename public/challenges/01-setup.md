# Challenge 1: Spark (set up git, Claude Code and danfactory)

> Level 1 of 7 · Time box: 30-45 minutes · Badge: **Spark** · Self-reported

## Goal
Get a working toolbox and a fresh danfactory project that reports its own status. Nothing is built yet; that is the point.

## Skills you learn
- Using git and a terminal at a basic level.
- Starting Claude Code in a project folder.
- Reading the project dashboard.

## danfactory features used
Template clone, `scripts/bootstrap.sh`, the SessionStart hook ("which phase am I in?"), the `dashboard` script.

## Steps
1. Check the tools exist: `git --version` and `python3 --version`. Missing? See the FAQ below.
2. Make sure Claude Code is installed and you can log in (see the official Claude Code docs for your system). Run `claude --version` or just `claude` once and finish the login.
3. Create your project from danfactory (README, verbatim):
   ```bash
   git clone https://github.com/dalhhorn-ship-it/danfactory my-project && cd my-project && rm -rf .git && git init
   ```
4. Bootstrap (README, verbatim):
   ```bash
   bash scripts/bootstrap.sh "my-project" "one line description"   # flags: --codegraph, --cloudflare (auto-created Worker)
   ```
5. Start Claude Code with `claude` and say **"let's start"**. The SessionStart hook tells Claude which phase you are in. You can stop after Claude asks its first brainstorm question; you do not need to finish a goal yet.
6. Build the dashboard and open it:
   ```bash
   python3 scripts/dashboard.py --open
   ```
7. Print the cheap text status:
   ```bash
   python3 scripts/dashboard.py --print
   ```

## Done when
- [ ] `git`, `python3` and `claude` all run on your machine.
- [ ] Your project folder exists with its own fresh git history.
- [ ] Claude, on "let's start", knows you are in the brainstorm phase.
- [ ] The dashboard opens in your browser (file: `dashboard/index.html`).

## Submit as proof
Open a GitHub Issue (or Discussion if enabled) on https://github.com/dalhhorn-ship-it/danfactory titled `[challenge-1] Spark - <your name or handle>` with:
1. Link to your project repo (public) or say it stays local.
2. Screenshot of the dashboard.
3. The output of `python3 scripts/dashboard.py --print` pasted in a code block.

Everything is self-reported. Nobody is checking your machine.

## FAQ (common snags)
- **`git: command not found`.** Install git from the official git site (git-scm.com) or your system's package manager, then open a new terminal.
- **`python3: command not found`.** Install Python 3 from the official Python site (python.org) or your package manager. On some systems the command is `python`; check with `python --version`. The template needs python3 only (standard library, no pip installs).
- **Claude Code won't start or asks to log in.** Run `claude` and follow the login prompt. Follow the official Claude Code docs for install and account requirements; they change, so we do not copy them here.
- **I'm on Windows.** The template's scripts are bash scripts. Using WSL (Windows Subsystem for Linux) is the simplest route; see Microsoft's WSL docs and the official Claude Code docs for Windows notes. Do the whole challenge inside the WSL terminal.
- **`bootstrap.sh: Permission denied`.** Run it through bash as written: `bash scripts/bootstrap.sh ...`. That does not need the executable bit.
- **Where is the dashboard?** `dashboard/index.html` in your project. `python3 scripts/dashboard.py --open` builds and opens it. The text version is `dashboard/SUMMARY.md`.
- **`git init` complains or I lost the template history.** That is expected: `rm -rf .git && git init` starts your own history on purpose.
- **Claude doesn't mention a phase.** Make sure you started `claude` inside the project folder, and say "let's start".

## Help line
No phone or email. Open an Issue on https://github.com/dalhhorn-ship-it/danfactory titled `[challenge-1] help: <short problem>`. Include your operating system, the command you ran, and the exact error text.

## Next
Challenge 2: your first farm game (`02-farm-game.md`).
