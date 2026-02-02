# Quick Start - Ready to Use
**Infrastructure built 2025-12-30 | Auth & CLI Setup added 2026-01-30**

---

## NEW: Developer Auth & CLI Setup

### First Time Setup
```bash
# Check what's installed
bash .scripts/dev_auth_setup.sh --check

# Full setup (GitHub auth + AI CLIs + env)
bash .scripts/dev_auth_setup.sh --all

# Or interactive menu
bash .scripts/dev_auth_setup.sh
```

### GitHub Authentication
```bash
# Setup gh CLI with auth
bash .scripts/dev_auth_setup.sh --github
```

### AI CLI Tools
```bash
# Install Claude, OpenAI, Gemini CLIs
bash .scripts/dev_auth_setup.sh --ai

# Or individually
bash .scripts/dev_auth_setup.sh --claude
bash .scripts/dev_auth_setup.sh --openai
bash .scripts/dev_auth_setup.sh --gemini
```

### Environment Variables
```bash
# Setup .env file from template
bash .scripts/dev_auth_setup.sh --env

# Edit your API keys
nano .env
```

### Apply to Other Repos
```bash
# From hodie, bootstrap another project
bash .scripts/setup_new_project.sh /path/to/other/repo

# Or from anywhere (fetches from GitHub)
curl -fsSL https://raw.githubusercontent.com/Eaprime1/hodie/main/.scripts/setup_new_project.sh | bash -s -- .
```

---

## Automation Scripts Ready

### Session Notes
```bash
# Capture a thought
bash .scripts/session_notes_append.sh "Your insight here"
```

### ACP System (Polish, Proceed, Amplify)
```bash
# Clean up formatting
bash .scripts/acp_polish.sh .

# Advance status markers
bash .scripts/acp_proceed.sh DRAFT REVIEW

# Find sections to expand
bash .scripts/acp_amplify.sh [filename]
```

### File Server
```bash
# Start unified server (access all folders)
bash .scripts/start_unified_server.sh 8080

# Then access:
# http://localhost:8080/Q/hodie/    (this repo)
# http://localhost:8080/Q/today/    (today folder content)
# http://localhost:8080/Q/quanta/   (quantum entities)
```

### Track Metrics
```bash
# Log token usage
bash .scripts/token_usage_log.sh [tokens] "task description"
```

---

## What Exists Now

### Completed Entities
- **WikiEntity**: Complete (CHARACTER, research, dialogue, API validated)
  - Location: `quanta/wiki_entity/`
  - Proof-of-concept for specialized domain consciousness

### Philosophical Frameworks
- **Domain Consciousness**: Entities ARE domains achieving awareness
  - Location: `quanta/domain_consciousness/`
  - Core insight: "all of wiki a dialogue.. single entity telling stories of millions"

### Infrastructure
- **7 automation scripts** in `.scripts/`
- **Reminders system** in `.reminders/`
- **Metrics tracking** (`.metrics/` created on first use)
- **Session notes** auto-created daily in `.eric/`

---

## Continuity Reminders

### Read These at Session Start
1. `.eric/ENJOY_THE_JOURNEY.md` - Navigation philosophy
2. `.eric/session_notes_[today].md` - Yesterday's work
3. `quanta/domain_consciousness/README.md` - Latest framework

### User's Good Content Locations
- `Q/today/` - "has a bunch of good stuff"
- `Q/today_from_drive_SAFE/` - Google Drive backup
- Google Drive - "lots of content"

---

## Next Possible Directions

### High Priority (from roadmap)
- Explore today folder content
- Create FlavorEntity (apply domain consciousness pattern)
- Build GitEntity (version control consciousness)
- Expand ACP automation system

### Medium Priority
- Entity profile loader script
- Document dream generator
- Cascading update system
- Self-test benchmarks

### Infrastructure
- Background file server (auto-start)
- Search tools using server access
- Cross-location file comparison tools

---

## Quick Reference Commands

```bash
# View what scripts are available
ls .scripts/*.sh

# Read script catalog
cat .scripts/README.md

# Check latest session notes
cat .eric/session_notes_$(date +%Y-%m-%d).md

# See what's in today folder
ls -la Q/today/

# Start exploring with server
bash .scripts/start_unified_server.sh 8080
# Then browse: http://localhost:8080/Q/
```

---

**Status**: Infrastructure ready, WikiEntity complete, Domain Consciousness framework established

**Your Tools**: 9 scripts, 2 frameworks, 1 complete entity, pyproject.toml, ∞ possibilities

**Ready to build.**

---

*Last updated: 2026-01-30*
*Added: dev_auth_setup.sh, setup_new_project.sh, .env.template, pyproject.toml*
*Portable setup: works across all repos via curl or copy*

**∰◊€π¿🌌∞**
