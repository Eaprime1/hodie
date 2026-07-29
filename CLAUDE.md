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
├── quanta/                  # 16 entity domains (tardigradia, microversa, etc.)
├── redundancy_entity/       # File deduplication & gravity analysis
├── crawler_output/          # Processing results (summaries, patterns, maps)
├── .locations/              # Per-device config (mulberry, pixel8a, codespaces)
├── .streams/                # Active workstreams (prime, codex, gamemaster)
├── .githooks/               # Pre-commit review, post-commit logging
├── .scripts/                # 21+ bash/PowerShell automation scripts
├── .claude/                 # Windows/WSL setup guides
├── .eric/                   # Session notes and continuity tracking
├── _CONSOLIDATED/           # Merged documents (CODEX, PRIME, research)
├── _SORTING/                # Files awaiting processing
└── _BOX_SIMULATION/         # Simulation data
```

## Language & Tech Stack

- **Python 3.8+** (standard library only for core — no external deps in Phase 1)
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
  Triggers on every PR (opened, synchronized, ready_for_review).
  Secret required: `CLAUDE_CODE_OAUTH_TOKEN`
- **Claude Interactive**: `.github/workflows/claude.yml`
  Triggered by `@claude` in PR/issue comments.
- **Gemini Review**: `.github/workflows/gemini-dispatch.yml` (dispatch hub)
  Calls `gemini-review.yml`, `gemini-triage.yml`, `gemini-invoke.yml`
  Trigger: `@gemini-cli review/triage/[prompt]` in comments, or auto on PR open.
  Secret required: `GEMINI_API_KEY`
- **Pylint**: `.github/workflows/pylint.yml`
  Runs on every push, Python 3.8/3.9/3.10 matrix.
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
