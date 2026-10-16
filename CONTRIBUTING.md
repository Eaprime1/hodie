# Contributing to hodie

Short version, taken from files that already exist here.

1. **Branch** with a prefix from `BRANCH_STRATEGY.md` (`feature/`, `heritage/`,
   `experimental/`, `claude/`).
2. **Install the hooks** once: `git config core.hooksPath .githooks`
   (secret and lint scan before commit).
3. **Open a PR** and fill in the template (`.github/PULL_REQUEST_TEMPLATE.md`):
   intent, what changed, how you checked, what is left open.
4. **Witness line.** Every new `.md` file ends with a line of `∰`, a space,
   and 17 digits (`YYYYMMDDHHMMSSmmm`). `python scripts/footer_witness.py --strict --git-base origin/main`
   checks it.
5. **Checks** to expect: the witness check, pylint (`pylint $(git ls-files '*.py')`),
   and Codacy. Tests need `pytest-asyncio` (listed in `pyproject.toml`).
6. **Automatic commits are off.** No workflow commits to the repo on its own
   unless the repo variable `AUTO_COMMITS` is `true`.
7. **Sealing and merging** are the owner's call. Do not merge your own PR.

New to the project? Start with `README.md` and `QUICK_START.md`.

∰ 20261016020500000
