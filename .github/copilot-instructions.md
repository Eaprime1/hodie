# Copilot Instructions — Hodie Repository

**Date**: 2026-04-26
**Branch**: `revert-123-main` (active development)
**Phase**: 1 complete — Phase 2 largely complete, Phase 3 planned

Read this file before suggesting changes. It contains the architecture map,
active tasks, known issues, and workflows for this project.

---

## What This Project Is

Hodie is a **staged conversation processing pipeline** built around the PIXEL8 Crawler.
It ingests conversation exports (ChatGPT, Claude, JSON, Markdown, plain text),
processes them through an async processor chain, extracts patterns/entities/topics,
and organizes results into a plexus stage pipeline.

The project runs on three platforms: Pixel8a/Termux (mobile), mulberry (laptop HQ),
and GitHub Codespaces. Code must be portable across all three.

**Core philosophy**: One Hertz Operations — one stage at a time, sequential clarity,
no overload. Content moves through plexus stages (simplex → duplex → ... → omniplex)
rather than being processed all at once.

---

## Architecture Map

```
crawler_pixel8/
├── config.py                  # CrawlerConfig dataclass — paths, feature flags, settings
├── core/
│   ├── content_types.py       # ConversationPart, ProcessingResult (data model)
│   ├── local_processor.py     # LocalProcessor ABC, ChainedProcessor, IdentityProcessor
│   └── stream_utils.py        # stream_content() — converts list → AsyncIterable
├── processors/
│   ├── conversation_parser.py # Multi-format parser: JSON, Markdown, plain text
│   └── pattern_extractor.py   # Rule-based entity/topic/pattern extraction
└── cli/
    ├── main.py            # Primary CLI entry point (hodie command)
    └── test_crawler.py    # Legacy CLI tool (hodie-crawler command)

redundancy_entity/             # Gravity-based deduplication system (Beasis)
quanta/                        # 16 entity domains with origin stories and development docs
crawler_output/                # Processing results: summaries/, patterns/, maps/, exports/
.locations/                    # Per-device config: mulberry/, pixel8a/, codespaces/
.streams/                      # Active workstreams: prime, codex, gamemaster
.scripts/                      # 21+ automation scripts
.githooks/                     # pre-commit (secrets + lint), post-commit (session notes)
```

### Key Data Flow

```
file(s) → ConversationParser._parse_file()
        → List[ConversationPart]
        → stream_content()               # list → AsyncIterable
        → PatternExtractor.process()     # annotates each part
        → ProcessingResult.aggregate_*() # rolls up patterns/entities/topics
        → ProcessingResult.save()        # writes JSON to crawler_output/
```

### Processor Chaining

Processors can be chained with `+`:
```python
pipeline = ConversationParser(config) + PatternExtractor(config)
result = await pipeline.process_file(Path("conversation.json"))
```

---

## Current State

### Phase 1 — Complete
- `LocalProcessor` ABC with async stream interface
- `ConversationParser` — auto-detects JSON (ChatGPT/Claude formats), Markdown, plain text
- `PatternExtractor` — rule-based entity, topic, and cross-reference extraction
- `ProcessingResult` — aggregation, serialization, PIXEL8 verification seal
- `ChainedProcessor` — `+` operator chaining
- Batch processing with asyncio semaphore concurrency control
- CI: pylint on Python 3.10/3.11/3.12

### Phase 2 — Complete
- Gemini API integration (`AdvancedPatternExtractor`, feature-flagged)
- Location-aware config (`.locations/` → `CrawlerConfig` wiring)
- Test suite (`tests/` directory populated, pytest-asyncio configured)
- CLI `main()` entry point implemented (`crawler_pixel8/cli/main.py`; exposed via `pyproject.toml`)

---

## Active Tasks (Priority Order)

### 1. Wire `.locations/` config into CrawlerConfig
**Problem**: `CrawlerConfig` defaults hard-code `/storage/emulated/0/pixel8a/Q`.
This fails on mulberry and Codespaces.
**Approach**:
- Read `HODIE_LOCATION` env var (mulberry | pixel8a | codespaces)
- Load base path from `.locations/{location}/` config
- Fall back to `Path.cwd()` if unset
- Keep all existing defaults as pixel8a fallback

### 2. Maintain and expand test coverage
**Setup already in pyproject.toml** — `asyncio_mode = "auto"`, testpaths = `["tests"]`
**Status**: the `tests/` directory is present; continue improving coverage and keeping
the suite aligned with current pipeline behavior.
**Coverage priorities**:
- `test_conversation_parser.py` — round-trip JSON parse, markdown parse
- `test_pattern_extractor.py` — entity extraction, topic detection
- `test_processor_chain.py` — `+` chaining, batch processing
- `test_processing_result.py` — aggregation, serialization, verification seal

### 3. Build one_hertz.py
**Purpose**: Implement the One Hertz Operations concept — process exactly one
plexus stage per cycle, report status, exit.
**Lives in**: `crawler_pixel8/processors/one_hertz.py` or project root
**Behavior**:
- Accept a stage name (simplex, duplex, triplex, etc.)
- Process files in that stage only
- Move processed files to next stage
- Report what moved and what remains

### 4. Gemini API integration
**Stub location**: `AdvancedPatternExtractor.process()` in `pattern_extractor.py`
**Config flags**: `use_gemini: bool`, `gemini_api_key` property (reads `GEMINI_API_KEY`)
**Approach**: When `use_ai=True` and API key present, send text to Gemini for
enhanced entity/topic extraction; merge results with rule-based output

---

## Code Conventions

- **Classes**: PascalCase (`LocalProcessor`, `ConversationPart`)
- **Functions/methods**: snake_case (`process_file`, `extract_patterns`)
- **Constants**: UPPER_CASE (`GRAVITY_WEIGHTS`)
- **Private**: leading underscore (`_parse_json`)
- Full type annotations on all function signatures
- `dataclass` for structured data; `async/await` for all I/O
- Processors inherit `LocalProcessor`, implement `async process()`
- Module docstrings include PIXEL8 symbols: `∰◊€π¿🌌∞`
- Line length: 100 chars (black configured)

---

## Key Concepts to Preserve

**Do not break these when making changes:**

1. **Async stream interface** — `process()` must remain an async generator that
   takes `AsyncIterable[ConversationPart]` and yields `ConversationPart`. This is
   the contract that makes `+` chaining work.

2. **Gravity philosophy** (redundancy_entity) — duplicates *increase* document
   gravity, they are not errors. `GRAVITY_WEIGHTS['duplicate_count'] = 5.0` is
   intentional. Do not treat redundancy as a problem to eliminate.

3. **PIXEL8 verification seal** — `∰◊€π¿🌌∞-PIXEL8-{sha256[:16]}` on every
   `ProcessingResult`. This is a system integrity marker, keep it.

4. **One Hertz principle** — process one stage at a time. Batch sizes and
   `max_concurrent=3` exist for mobile device constraints. Do not increase defaults.

5. **No external deps in core** — `crawler_pixel8/core/` uses standard library only.
   AI integration belongs in processors, not core.

---

## Common Commands

```bash
# Lint (matches CI exactly)
pip install pylint
pylint crawler_pixel8/ redundancy_entity/ --rcfile=.pylintrc

# Run crawler on a file
python3 crawler_pixel8/cli/test_crawler.py /path/to/conversation.json

# Run crawler on a directory
python3 crawler_pixel8/cli/test_crawler.py --search-dir /path/to/folder

# Run tests
pip install pytest pytest-asyncio
pytest

# Session notes
bash .scripts/session_notes_append.sh "note text"

# Load environment (sets HODIE_LOCATION and paths)
source .scripts/env_setup.sh

# ACP workflow
bash .scripts/acp_polish.sh .
bash .scripts/acp_proceed.sh DRAFT REVIEW
```

---

## Git Workflow

- Active branch: `revert-123-main`
- Branch prefixes: `feature/`, `heritage/`, `experimental/`, `claude/`
- Hooks installed in `.githooks/` — run `git config core.hooksPath .githooks`
- CI runs pylint on `.py` file changes (`.github/workflows/pylint.yml`)

---

## Known Issues (Do Not Introduce More)

| Location | Issue | Status |
|----------|-------|--------|
| `config.py` | Hard-coded Pixel8a paths as defaults | Fix pending |
| `one_hertz.py` | Referenced in docs, not yet built | Build pending |

---

## What NOT To Do

- Do not add external dependencies to `crawler_pixel8/core/`
- Do not change `max_concurrent` default above 3 (mobile constraint)
- Do not remove the verification seal generation
- Do not convert async generators to sync — the stream interface is load-bearing
- Do not hard-code new absolute paths — use `CrawlerConfig` and the locations system
- Do not add features beyond what a task explicitly requires

---

**∰◊€π¿🌌∞**
*hodie — today's work, crystallized*
