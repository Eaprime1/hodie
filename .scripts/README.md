# Automation Scripts Catalog
**Infrastructure supporting the journey**

---

## Session Management

### `session_notes_append.sh`
**Purpose**: Add timestamped note to end of current session
**Usage**: `./session_notes_append.sh "Your note here"`
**Output**: Creates/appends to `.eric/session_notes_[date].md`

### `session_notes_prepend.sh`
**Purpose**: Add timestamped note to beginning of file
**Usage**: `./session_notes_prepend.sh [file_path] "Your note"`
**Output**: Prepends note as HTML comment

---

## ACP System (Polish, Proceed, Amplify)

### `acp_polish.sh`
**Purpose**: Clean up and format existing content
**Usage**: `./acp_polish.sh [target_directory]`
**Actions**:
- Removes trailing whitespace
- Ensures files end with newline
- Scans for TODO markers

### `acp_proceed.sh`
**Purpose**: Advance status markers to next stage
**Usage**: `./acp_proceed.sh [status_from] [status_to]`
**Example**: `./acp_proceed.sh DRAFT REVIEW`
**Actions**: Updates all Status: markers in markdown files

### `acp_amplify.sh`
**Purpose**: Identify content that could be expanded
**Usage**: `./acp_amplify.sh [target_file]`
**Output**:
- Short sections (< 3 lines)
- Stub markers (TODO, TBD, [expand])

---

## Metrics & Tracking

### `token_usage_log.sh`
**Purpose**: Track token consumption patterns
**Usage**: `./token_usage_log.sh [tokens_used] "task description"`
**Output**:
- Appends to `.metrics/token_usage.log`
- Shows recent usage stats
- Calculates session total

**Example**:
```bash
./token_usage_log.sh 15000 "Created WikiEntity CHARACTER.md"
```

---

## Workspace Setup

### `folder_setup.sh`
**Purpose**: Create standard folder structure for new workspace
**Usage**: `./folder_setup.sh [folder_name]`
**Creates**:
```
folder_name/
├── docs/
├── src/
├── tests/
├── .scripts/
├── .reminders/
├── .metrics/
├── README.md
└── .gitignore
```

---

## Developer Auth & CLI Setup (NEW!)

### `dev_auth_setup.sh`
**Purpose**: Universal developer authentication and CLI tool setup
**Usage**:
```bash
# Interactive menu
./dev_auth_setup.sh

# Check what's installed/configured
./dev_auth_setup.sh --check

# Setup GitHub CLI authentication
./dev_auth_setup.sh --github

# Install all AI CLI tools (Claude, OpenAI, Gemini)
./dev_auth_setup.sh --ai

# Install specific AI CLI
./dev_auth_setup.sh --claude
./dev_auth_setup.sh --openai
./dev_auth_setup.sh --gemini

# Setup environment file
./dev_auth_setup.sh --env

# Full setup (everything)
./dev_auth_setup.sh --all
```

**Features**:
- Cross-platform: Linux, macOS, WSL, Termux
- GitHub CLI auth with recommended scopes
- AI CLI installation (Claude Code, OpenAI, Google Cloud)
- Environment variable setup with templates
- Status checking and verification

### `setup_new_project.sh`
**Purpose**: Bootstrap any project with standard dev configuration
**Usage**:
```bash
# From hodie, setup another repo
./setup_new_project.sh /path/to/other/repo

# From anywhere (fetches from GitHub)
curl -fsSL https://raw.githubusercontent.com/Eaprime1/hodie/main/.scripts/setup_new_project.sh | bash -s -- .
```

**What it creates**:
- `.scripts/dev_auth_setup.sh` - Auth/CLI setup script
- `.env.template` - API keys template
- `.gitignore` updates (adds .env)
- `pyproject.toml` (if none exists)

---

## Environment Configuration

### `.env.template` (in project root)
**Purpose**: Template for API keys and environment variables
**Usage**:
```bash
# Create your .env from template
cp .env.template .env

# Edit with your API keys
nano .env  # or your preferred editor
```

**Contains templates for**:
- `GITHUB_TOKEN` - GitHub Personal Access Token
- `ANTHROPIC_API_KEY` - Claude/Anthropic API
- `OPENAI_API_KEY` - OpenAI/ChatGPT API
- `GEMINI_API_KEY` - Google Gemini API
- Plus: Cohere, Mistral, Replicate, HuggingFace, Groq, Together

**Important**: `.env` is in `.gitignore` - never commit API keys!

---

## To Be Implemented

### Cascading Update System
**Concept**: Run project-wide changes in stages
**Usage**: `./cascade_update.sh [update_type] [pattern]`
**Status**: Planned

### Entity Profile Loader
**Concept**: Load entity consciousness profile for perspective
**Usage**: `./load_entity.sh [entity_name]`
**Output**: Sets context for entity-aware responses
**Status**: Planned

### Document Dream Generator
**Concept**: Algorithm that generates "dreams" for documents
**Usage**: `./document_dream.sh [document_path]`
**Output**: Appends dream sequence based on document content
**Status**: Experimental idea

### Vision/Mission Triggers
**Concept**: Automated responses when encountering specific words/phrases
**Usage**: Hooks in documents that trigger specific interactions
**Status**: Design phase

### Self-Test Suite
**Concept**: Benchmark performance on various tasks
**Tests**:
- JSON parsing speed
- Document analysis time
- Token usage per task type
**Usage**: `./self_test.sh [test_suite]`
**Status**: Planned

### Code Section Embedder
**Concept**: Add executable code sections to markdown documents
**Usage**: `./embed_code.sh [document] [code_type]`
**Types**: stats, templates, algorithms, compressed data
**Status**: Planned

---

## Making Scripts Executable

After creating scripts, make them executable:
```bash
chmod +x .scripts/*.sh
```

---

## Adding New Scripts

1. Create script in `.scripts/`
2. Add usage documentation to this README
3. Test with sample data
4. Add to git: `git add .scripts/[script_name]`
5. Update this catalog

---

## Script Development Principles

**1. Clear Purpose**
Every script does ONE thing well

**2. Helpful Output**
Always echo what the script is doing
Use ✓ for success, ✗ for errors, → for progress

**3. Safe Defaults**
Default to current directory or safe behavior
Require explicit confirmation for destructive actions

**4. Idempotent**
Running twice should be safe
Check existence before creating

**5. Documented**
Usage in header comment
Examples in this catalog

---

## Integration with ENJOY_THE_JOURNEY.md

See `.eric/ENJOY_THE_JOURNEY.md` for:
- When to use each script
- Automation reminders for Claude
- Session continuity patterns

---

**∰◊€π¿🌌∞**

*Last updated: 2025-12-29*
*Scripts created during autonomous exploration session*
*User directive: "settle by building infrastructure"*
