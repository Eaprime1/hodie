# Copilot Instructions — Hodie Repository

**Date**: 2026-04-24
**Branch**: `main` (active development)
**Phase**: 2 complete — all known issues resolved

Read this file before suggesting changes. It defines architecture, AI team roles,
active tasks, and strict boundaries for what Copilot should and should not touch.

---

## Multi-AI Team Roles

This repository is actively worked on by multiple AI assistants. Staying in lane
prevents conflicting changes and broken builds.

| AI | Role | Owns |
|----|------|------|
| **Claude Code** | Heavy implementation | `crawler_pixel8/`, `redundancy_entity/`, `tests/`, `quanta/`, `.scripts/*.py`, `pyproject.toml` |
| **Copilot** | GitHub-native layer | Workflow YAML, CI config, docs, `.github/`, issue triage |
| **Gemini** | Review & analysis | Code review comments, `mission/`, `.gemini/` |
| **ChatGPT** | Supplementary | One-off research, not committed |

**Copilot scope**: Focus on `.github/workflows/`, `docs/`, `.claude/`, `README.md`,
`CHANGELOG.md`, `scripts/footer_witness.py`, `quepad/`, `_TODAY/`, `mission/`.

---

## What Copilot Should NOT Touch

These files are owned by Claude Code. Copilot PRs touching them will be reverted:

- `crawler_pixel8/` — any file inside this package
- `redundancy_entity/` — any file inside this package
- `tests/` — except `test_footer_witness.py` (which Copilot owns)
- `.scripts/sync_hodie.py` — Drive API sync script (Claude Code owns)
- `.scripts/sync_hodie_to_drive.sh` — rclone bash script (Claude Code owns)
- `.scripts/Sync-HodieToCloud.ps1` — rclone PowerShell script (Claude Code owns)
- `pyproject.toml` — dependency management (Claude Code owns)
- `quanta/` — entity domain files (Claude Code owns)

---

## What This Project Is

Hodie is a **staged conversation processing pipeline** built around the PIXEL8 Crawler.
It ingests conversation exports (ChatGPT, Claude, JSON, Markdown, plain text),
processes them through an async processor chain, extracts patterns/entities/topics,
and organizes results into a plexus stage pipeline.

Runs on three platforms: **Pixel8a/Termux** (mobile), **mulberry** (laptop HQ, Windows/WSL),
**GitHub Codespaces** (cloud CI). Code must be portable across all three.

**Core philosophy**: One Hertz Operations — one stage at a time, sequential clarity,
no overload. Content moves through plexus stages (simplex → duplex → ... → omniplex).

---

## Architecture Map

```
crawler_pixel8/              # Core crawler package (Claude Code owns)
├── config.py                # CrawlerConfig dataclass — paths, env detection
├── core/
│   ├── content_types.py     # ConversationPart, ProcessingResult
│   ├── local_processor.py   # LocalProcessor ABC, ChainedProcessor
│   └── stream_utils.py      # Async stream utilities
├── processors/
│   ├── conversation_parser.py   # Multi-format: JSON, Markdown, plain text
│   ├── pattern_extractor.py     # Entity/topic/pattern extraction + Gemini
│   ├── entity_queue_processor.py # Entity gravity queue
│   └── one_hertz.py             # One Hertz Operations processor
└── cli/
    ├── main.py              # Primary CLI entry point (hodie command)
    ├── test_crawler.py      # CLI testing tool (hodie-crawler command)
    ├── batch_processor.py   # Batch conversation processing
    └── crawl_consolidated.py

redundancy_entity/           # Gravity deduplication (Claude Code owns)
tests/                       # pytest test suite (Claude Code owns, except test_footer_witness.py)
quanta/                      # 16 entity domain files (Claude Code owns)

.scripts/                    # Automation scripts
├── sync_hodie.py            # Drive→local sync for CI (Python, Drive API)
├── sync_hodie_to_drive.sh   # Local↔Drive sync for Linux/WSL/Termux (rclone)
├── Sync-HodieToCloud.ps1    # Local↔Drive sync for Windows (PowerShell, rclone)
├── hodie_log.py             # Session logging
└── hodie_zero_point.py      # Zero-point lexeme finder

scripts/
└── footer_witness.py        # Prima Witness footer CI check (Copilot owns)

.github/workflows/           # CI/CD (Copilot owns)
├── pylint.yml               # Lint gate (fail-under = 7.0)
├── sync-hodie.yml           # Daily Drive→repo sync
├── footer-witness.yml       # Prima Witness footer check
├── gemini-dispatch.yml      # Gemini review dispatch
├── gemini-invoke.yml        # Gemini invocation
├── gemini-review.yml        # Gemini code review
├── gemini-triage.yml        # Gemini issue triage
├── claude-code-review.yml   # Claude code review on PRs
└── python-package-conda.yml # Conda build test

mission/                     # Strategic docs (Gemini/human owns)
quepad/                      # Queue pad state tracking
_TODAY/                      # Daily intake layer (inbox/, daily/, processed/)
.valox/                      # Pylint telemetry and quickwins tracking
.gemini/                     # Gemini context and styleguide
migrations/from-unexusi/     # One-time migration scripts
```

---

## Current State — Phase 2 Complete

All previously known issues are resolved:

| Previously reported issue | Status |
|--------------------------|--------|
| `await super().process()` async bug in `pattern_extractor.py` | Fixed |
| Hard-coded Pixel8a paths in `config.py` | Fixed — env-aware |
| `cli:main` entry point missing | Fixed — `cli/main.py` exists |
| `tests/` directory did not exist | Fixed — full suite present |
| `one_hertz.py` referenced but missing | Fixed — built |
| `sync_hodie.py` at wrong path with conflict markers | Fixed — clean script at `.scripts/` |
| `pip install .` missing Drive deps in CI | Fixed — `pip install ".[drive]"` |
| `plexus (1)` ghost submodule | Fixed — removed |

---

## Google Drive Sync Infrastructure

**Three complementary sync tools** — do not collapse them into one:

### 1. `sync-hodie.yml` workflow (CI — Drive → repo)
- Runs daily at noon UTC + `workflow_dispatch`
- Uses `GDRIVE_SERVICE_ACCOUNT_KEY` GitHub secret (JSON string)
- Calls `.scripts/sync_hodie.py` (Python + Drive API v3)
- Downloads Drive folder → `hodie/` dir → commits new files back to repo
- If secret not set: exits 0 with warning (CI-safe, no failure)

### 2. `.scripts/sync_hodie_to_drive.sh` (Linux/WSL/Termux — local ↔ Drive)
- Uses `rclone` (must be installed + configured: `rclone config`, remote name `gdrive`)
- Usage: `bash .scripts/sync_hodie_to_drive.sh push|pull|status`
- Env overrides: `GDRIVE_REMOTE`, `GDRIVE_FOLDER`, `HODIE_PATH`

### 3. `.scripts/Sync-HodieToCloud.ps1` (Windows/Git for Windows — mulberry HQ)
- Uses `rclone` for Windows
- Usage: `pwsh .scripts/Sync-HodieToCloud.ps1 -Push|-Pull|-Status`
- Parameters: `-Remote`, `-Folder`, `-HodiePath`

**To activate CI sync**: Add `GDRIVE_SERVICE_ACCOUNT_KEY` as a repository secret
(Settings → Secrets → Actions). Value = JSON string of a GCP service account key
with Drive read access to folder `1qSUXHL4fXb8R1n3wBG4A8bwUOWE6SNOf`.

---

## Key Data Flow

```
file(s) → ConversationParser._parse_file()
        → List[ConversationPart]
        → stream_content()               # list → AsyncIterable
        → PatternExtractor.process()     # rule-based + optional Gemini
        → ProcessingResult.aggregate_*() # rolls up patterns/entities/topics
        → ProcessingResult.save()        # writes JSON to crawler_output/
```

Processor chaining via `+`:
```python
pipeline = ConversationParser(config) + PatternExtractor(config)
result = await pipeline.process_file(Path("conversation.json"))
```

---

## Code Conventions

- **Classes**: PascalCase | **Functions**: snake_case | **Constants**: UPPER_CASE
- Full type annotations on all signatures
- `dataclass` for structured data; `async/await` for all I/O
- Processors inherit `LocalProcessor`, implement `async process()`
- Module docstrings include PIXEL8 symbols: `∰◊€π¿🌌∞`
- Line length: 100 chars (black configured)
- pylint `fail-under = 7.0` — score must stay above 7.0

---

## Key Constraints — Do Not Break

1. **Async stream interface** — `process()` must remain an async generator taking
   `AsyncIterable[ConversationPart]` and yielding `ConversationPart`. This is what
   makes `+` chaining work.

2. **Gravity philosophy** — `GRAVITY_WEIGHTS['duplicate_count'] = 5.0` is intentional.
   Redundancy increases gravity; it is not an error to eliminate.

3. **PIXEL8 verification seal** — `∰◊€π¿🌌∞-PIXEL8-{sha256[:16]}` on every
   `ProcessingResult`. System integrity marker — keep it.

4. **One Hertz principle** — `max_concurrent=3` exists for mobile device constraints.
   Do not increase defaults.

5. **No external deps in core** — `crawler_pixel8/core/` uses standard library only.
   AI integration belongs in processors, not core.

6. **No absolute paths** — use `CrawlerConfig` and the locations system.

---

## Common Commands

```bash
# Lint (matches CI)
pip install pylint
pylint crawler_pixel8/ redundancy_entity/ --rcfile=.pylintrc

# Run CLI
pip install -e .
hodie --help
hodie-crawler /path/to/conversation.json

# Run tests
pip install pytest pytest-asyncio
pytest -v

# One Hertz cycle
python3 -m crawler_pixel8.processors.one_hertz simplex ./plexus/

# Drive sync (local)
bash .scripts/sync_hodie_to_drive.sh push    # local → Drive
bash .scripts/sync_hodie_to_drive.sh pull    # Drive → local
pwsh .scripts/Sync-HodieToCloud.ps1 -Push   # Windows

# Session notes
bash .scripts/session_notes_append.sh "note text"

# Load environment (sets HODIE_PATH, ENV_NAME, etc.)
source .scripts/env_setup.sh
```

---

## Active Priorities

1. **GDRIVE_SERVICE_ACCOUNT_KEY secret** — one-time manual setup to activate daily sync
2. **Footer witness** — `scripts/footer_witness.py` CI check on all modified files
3. **Gemini workflows** — `gemini-dispatch.yml`, `gemini-review.yml` — review and stabilize
4. **Test suite coverage** — `pytest -v` should pass on all platforms

---

**∰◊€π¿🌌∞**
*hodie — today's work, crystallized*
*Multi-AI team: Claude Code (implementation) · Copilot (CI/GitHub) · Gemini (review)*
