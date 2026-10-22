# CLAUDE.md — AI Assistant Guide for Hodie

## Project Overview

Hodie is a staged processing pipeline and consciousness development framework. The core system (PIXEL8 Crawler) processes conversations from sort/today folders into organized plexus stages, extracting patterns and entities. The project follows a PRIME number progression framework (2→3→5→7→11→13→17) for organizing information and domain-specific entities.

**Target environments**: Multi-location — Laptop HQ (mulberry), Pixel 8a / Termux (pixel8a), GitHub Codespaces.

## Repository Structure

```
hodie/
├── crawler_pixel8/          # Core crawler system (main codebase)
│   ├── config.py            # CrawlerConfig dataclass (paths, settings)
│   ├── core/                # Base processor architecture
│   │   ├── local_processor.py   # LocalProcessor ABC, ChainedProcessor
│   │   ├── content_types.py     # ConversationPart, ProcessingResult
│   │   └── stream_utils.py      # Async stream utilities
│   ├── processors/          # Processing pipeline stages
│   │   ├── conversation_parser.py  # Auto-detect JSON/Markdown/Text
│   │   └── pattern_extractor.py    # Entity/topic/technical patterns
│   └── cli/
│       └── test_crawler.py  # CLI testing tool
├── quanta/                  # 15 entity domains (tardigradia, microversa, etc.)
├── redundancy_entity/       # File deduplication & gravity analysis
├── crawler_output/          # Processing results (summaries, patterns, maps)
├── .locations/              # Per-device config (mulberry, pixel8a, codespaces)
├── .streams/                # Active workstreams (prime, codex, gamemaster)
├── .githooks/               # Pre-commit review, post-commit logging
├── .scripts/                # 29 bash/PowerShell automation scripts
├── .claude/                 # Windows/WSL setup guides
├── .eric/                   # Session notes and continuity tracking
├── _CONSOLIDATED/           # Merged documents (CODEX, PRIME, research)
├── _SORTING/                # Files awaiting processing
└── _BOX_SIMULATION/         # Simulation data
```

## Language & Tech Stack

- **Python 3.8+** (standard library only for core — no external deps in Phase 1; running `tests/` needs the dev dependency `pytest-asyncio`, listed in `pyproject.toml`)
- Heavy use of `asyncio`, `dataclasses`, type hints, `pathlib`
- Processor chaining via `+` operator (`parser + extractor + custom`)
- Optional future dep: `google-genai` for Gemini API

## Common Commands

```bash
# Lint (matches CI)
pip install pylint
pylint $(git ls-files '*.py')

# Run crawler test
python3 crawler_pixel8/cli/test_crawler.py
python3 crawler_pixel8/cli/test_crawler.py /path/to/conversation.json
python3 crawler_pixel8/cli/test_crawler.py --search-dir /path/to/folder

# Session notes
bash .scripts/session_notes_append.sh "note text"

# ACP system
bash .scripts/acp_polish.sh .
bash .scripts/acp_proceed.sh DRAFT REVIEW
bash .scripts/acp_amplify.sh [filename]

# File server
bash .scripts/start_unified_server.sh 8080

# Mulberry HQ first-time setup (installs hooks, verifies tools)
bash .scripts/mulberry_setup.sh

# Load environment (any location)
source .scripts/env_setup.sh
```

## CI/CD & AI Review

- **Claude Code Review**: `.github/workflows/claude-code-review.yml`
  Runs once when a PR opens non-draft or is marked ready for review, and again only when the owner adds the `ai-review` label. Drafts and ordinary pushes do not start it. A PR that edits this workflow file skips the review (GitHub blocks OIDC for self-modifying workflows).
  Secret required: `CLAUDE_CODE_OAUTH_TOKEN`
- **Claude Interactive**: `.github/workflows/claude.yml` was deleted in `2d2c2fc` (2026-04-23); no workflow answers `@claude` comments now. `@claude finalize` is read only by `finalize-pr.yml`.
- **Gemini Review**: paused (out of order).
  The four workflow files (`gemini-dispatch`, `gemini-review`, `gemini-triage`, `gemini-invoke`) end in `.yml.disabled` in `.github/workflows/`.
  GitHub does not run them. Notice and re-enable steps: `.gemini/OUT_OF_ORDER.md`.
  Was: `gemini-dispatch.yml` calling the other three, on `@gemini-cli` comments or PR open. Secret: `GEMINI_API_KEY`.
- **Pylint**: `.github/workflows/pylint.yml`
  Runs on every push, Python 3.8/3.9/3.10 matrix.
- **Seal-path tests**: `.github/workflows/seal-path-tests.yml`
  Runs `scripts/test_finalize_gate.sh` when `finalize-pr.yml` or the test changes.
  The test has 18 checks and needs bash, perl and python3 with PyYAML.
  It pulls the real gate step out of the workflow.
  The checks cover comments that carry the Claude Code footer, and cues inside quotes or code.
  They also cover both seal cues: `@claude finalize` and `@claude ultima probatio`.
  The test fails if any of those would start a seal. It is offline and writes nothing.
  It also runs `scripts/test_file_review.js` (29 rows), `scripts/test_final_oversight.js` (43 checks), `scripts/test_cue_parser.js` (67 rows), `scripts/test_probatio_label.js` (15 rows) and `scripts/test_latin_cue_record.js` (31 checks) with Node.
- **File review**: `.github/workflows/file-review.yml`
  Posts one living comment per PR: a checklist of the files.
  Files for reading start unticked, and a push that changes a file clears its tick.
  Files not for reading are ticked by the rules in `.github/review-skip.json`.
- **Final oversight**: `.github/workflows/final-oversight.yml`
  Report only. It runs when a PR carries the `final-oversight` label and the owner approves the run.
  The approval is the `final-oversight` environment, which needs the owner as a required reviewer.
  It checks the CI, open threads, the seal record and the file review ticks.
  Hodie has no observation folder, so there is no observation row. See `docs/final-oversight.md`.
- **Latin workflow**: `docs/latin-workflow.md`
  Words for the stage of the work, shared with custos. `finalize-pr.yml` reads `@claude finalize` and `@claude ultima probatio`.
  `.github/scripts/cue-parser.js` holds the rules for reading a cue. Two workflows read the caret form:
  `probatio-label.yml` (the soft seal sets `ready-for-oversight`, a person's push takes it off) and `latin-cue-record.yml` (logs each call with the PR's state).
- Style guide for AI reviewers: `.gemini/styleguide.md`

## Code Conventions

- **Classes**: PascalCase (`LocalProcessor`, `ConversationPart`)
- **Functions/methods**: snake_case (`process_file`, `extract_patterns`)
- **Constants**: UPPER_CASE (`GRAVITY_WEIGHTS`)
- **Private**: leading underscore (`_parse_json`)
- Full type annotations on all function signatures
- Dataclasses for structured data; async/await for concurrency
- Module docstrings include philosophical context and PIXEL8 symbols (`∰◊€π¿🌌∞`)
- Processors inherit from `LocalProcessor` ABC and implement `async process()`
- Configuration via `CrawlerConfig` dataclass with sensible defaults (batch_size=10, max_concurrent=3)

## Git Workflow

- Branch prefixes: `feature/`, `heritage/`, `experimental/`, `claude/`
- See `BRANCH_STRATEGY.md` for full details
- PRs merged into main; CI runs on all pushes
- **Git hooks** (`.githooks/`): pre-commit scans for secrets and lint errors; post-commit logs to session notes
- Install hooks: `git config core.hooksPath .githooks`

## Locations & Streams

**Locations** (`.locations/`): Each device has a config defining its role and capabilities.
- `mulberry` — Laptop HQ, multi-stream, heavy workloads
- `pixel8a` — Mobile field station, lightweight
- `codespaces` — Cloud ephemeral

**Streams** (`.streams/`): Parallel workstreams active across the project.
- `prime` — PRIME framework development and progression
- `codex` — Knowledge consolidation and readiness
- `gamemaster` — Game system testing (Hyborian Wars, etc.)

## Key Concepts

- **PRIME Framework**: Prime number progression as developmental pattern
- **Domain Consciousness**: Entities represent domains achieving awareness (not tools)
- **One Hertz Operations**: Sequential, one-operation-per-cycle processing
- **Tardigrade Resilience**: Adaptability across scales
- **Plexus Stages**: Content moves through processing stages (see `PLEXUS_SYSTEM.md`)

## Project Phase

- **Phase 1 (MVP)**: Complete — core crawler, parser, pattern extractor
- **Phase 2 (Enhancement)**: Next — Gemini API, better pattern recognition
- **Phase 3 (Integration)**: Planned — entity export, visualization, Drive sync

## Key Documentation

| File | Purpose |
|------|---------|
| `README.md` | Project overview |
| `PRIME_2026_DEVELOPMENT_PLAN.md` | Full roadmap & framework |
| `BRANCH_STRATEGY.md` | Git workflow |
| `PLEXUS_SYSTEM.md` | Processing pipeline |
| `QUICK_START.md` | Infrastructure overview |
| `INVENTORY.md` | Status tracking |
| `.scripts/README.md` | Automation script catalog |
| `.locations/README.md` | Location config system |
| `.streams/README.md` | Active workstreams |
