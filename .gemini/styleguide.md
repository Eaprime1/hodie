# HODIE Code Review Style Guide

## Project context

HODIE is a universal workshop layer and staged processing pipeline built on the
Prime Progression Framework (3→5→7→11→13→17). It processes content through
plexus stages (simplex → duplex → triplex → quadroplex → omniplex) using
an async Python crawler and BBS-style daily intake automation.

Primary languages: **Python 3.8+**, **Bash**. Also markdown (heavy use).

---

## Review priorities (in order)

1. **Security** — credentials, tokens, hardcoded secrets, unsafe eval/exec patterns
2. **Portability** — no hardcoded user paths (e.g. `/home/<username>/`);
   use `$HOME`, `${BASH_SOURCE[0]}`, or `$(dirname ...)` patterns
3. **Chain of custody** — migration PRs must include `migrations/from-*/MIGRATION_LOG.md`
4. **Correctness** — does the script/code do what it claims? Proper error handling
5. **Plexus hygiene** — content staged at the correct plexus level
6. **Python hygiene** — asyncio patterns, dataclasses, type hints, pathlib
7. **Bash hygiene** — quote variables, `[[ ]]` not `[ ]`, `local` in functions,
   `set -euo pipefail` at top of scripts

---

## What NOT to flag

- Prime-progression language: "simplex", "duplex", "triplex", "omniplex", "plexus",
  "atelier", "navigo", "one hertz", "17-prime", "Ka dynamics", "heritage layer"
- Quanta entity names: "tardigradia", "perdura", "vitara", "resilia", "microversa",
  "pixel_entity", "abacusian", "wiki_entity", "jake", "unexusi", etc.
- The `∰◊€π¿🌌∞` signature — intentional collaborative marker
- Latin directory names: "rudera", "strues", "fragmenta", "pulvis", "duplicatus",
  "exemplar", "gravitar" — these are intentional naming conventions
- Single-file scripts with no unit tests — this is a tools/workshop repo
- Missing type annotations in utility scripts — not required for shell automation

---

## Python-specific guidance

- Flag: blocking I/O inside async functions without `await`
- Flag: bare `except:` without specific exception types
- Flag: mutable default arguments in function signatures
- Flag: importing `os.path` when `pathlib.Path` is available
- Do NOT flag: module docstrings with prime-progression philosophy
- Do NOT flag: `asyncio.run()` as entry point in CLI scripts

---

## Bash-specific guidance

- Flag: unquoted variables, `[ ]` instead of `[[ ]]`, missing `local`,
  missing shebang, hardcoded absolute paths
- Flag: `set -e` without `set -u` and `set -o pipefail`
- Do NOT flag: `echo -e` usage, color escape codes, interactive `read` patterns

---

## Tone

Concise and actionable. One sentence for the issue, one for the fix.
No filler. Match the One Hertz rhythm: one clear observation per cycle.
