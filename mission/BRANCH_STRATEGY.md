# Git Branch Strategy for PRIME 2026 Development
**Created**: 2026-01-02 | **Revised**: 2026-04-14
**Purpose**: Enable parallel development across multiple workstreams and locations
**Pattern**: Feature branches → develop → main (stable) via PR review

---

## Overview

**Challenge**: PRIME 2026 has multiple parallel workstreams, AI team members, and three
active locations (mulberry / pixel8a / codespaces) all contributing to the same repository:
- Foundation work (deduplication, sync, integration)
- Heritage layer creation (13-17 transitions)
- PIXEL integration (access protocols, team onboarding)
- Launch preparation (narrative, demos, community)
- AI-assisted development (Claude, Gemini, ChatGPT on separate branch tracks)

**Solution**: Strategic branching enables:
- Parallel development without conflicts
- Safe experimentation across devices and AI collaborators
- Clear integration pathways through PR review
- Stable main branch for public transmission
- Permanent heritage preservation across all timelines

---

## Core Branching Model

### Branch Types

**main**
- Stable, launched, public-facing
- Only merged via pull request after complete verification
- Tagged for versions/releases
- Protected (requires PR review + CI passing)

**develop**
- Active integration branch
- Where feature branches merge
- Testing ground before main
- Daily development target

**feature/***
- Specific tasks/workstreams
- Branched from develop (or main for quick fixes)
- Merged back via PR → delete after merge
- CI must pass before merge

**heritage/***
- Transitioned conversations and completed knowledge packages
- Long-lived — never deleted (permanent archive)
- Merged by metadata only; full content stays on branch

**experimental/***
- Testing new patterns, alternate approaches, safe-to-fail exploration
- May or may not merge — delete if unsuccessful
- Lower CI bar; iteration speed over stability

**claude/***
- AI-assisted development sessions (Claude Code)
- Short-lived; reviewed by Eric before merge
- Named by task: `claude/fix-pylint`, `claude/refactor-parser`

**migration/***
- Cross-repository content migrations (e.g. from UNEXUSI)
- Contains sync scripts, logs, and one-time transition work
- Merged to develop after migration verified; scripts kept in `migrations/`

**hotfix/***
- Critical fixes needed directly on main
- Branched from main → merged to main AND develop immediately
- Bypasses develop cycle; always fast-tracked

**archive/***
- Historical snapshots of completed phases
- Never deleted — permanent reference points
- Created at phase completions (pre-launch, post-launch, etc.)

---

## Repository-Specific Strategies

### hodie (Primary Workspace)

**Current State**: Feature branches merge to main via PR (CI + review gate)

```
main (stable, public, CI-gated)
  ↑ PR
  ← develop (integration, daily target)
      ↑
      ← feature/foundation         (Priority 1 — dedup, sync, CODEX)
      ← feature/heritage-layer     (Priority 2 — 13-17 transitions)
      ← feature/pixel-integration  (Priority 3 — access protocols)
      ← feature/launch-prep        (Priority 4 — narrative, demos)
      ← migration/from-unexusi     (one-time migration, now complete)
      ← claude/session-task        (AI-assisted, short-lived)
      ← heritage/conversation-YYYYMMDD  (permanent archive)
      ← experimental/new-pattern   (safe-to-fail)
      ← hotfix/critical-fix        (emergency, fast-track)
```

**Active Branch Status** (as of 2026-04-14):
- `feature/migration-unexusi-hodie` → PR #47 open (migration work)
- `main` → stable, CI passing

**Workflow** (PR-based, actual practice):
```bash
# Create and push feature branch
git checkout main && git pull
git checkout -b feature/my-work
# ... do work ...
git add <specific-files>
git commit -m "Feature: descriptive message"
git push -u origin feature/my-work

# Open PR on GitHub → CI runs pylint matrix → request review → merge
```

---

### today (Consolidation Workspace)

```
main (stable consolidations)
  ↑
  ← develop
      ↑
      ← feature/active-consolidation (work in progress)
      ← archive/YYYYMM              (completed consolidations by month)
```

**Purpose**: `feature/active-consolidation` → working state; `archive/YYYYMM` → completed by month.

---

### runexusiam (UNEXUS Development)

```
main (stable UNEXUS)
  ↑
  ← develop
      ↑
      ← feature/prime-integration  (connect to PRIME)
      ← feature/ka-measurement     (Ka pressure tools)
```

**Migration note**: Content from runexusiam is now syncing to hodie via `migrations/from-unexusi/`.
Migration scripts live at `migrations/from-unexusi/sync_hodie_from_unexusi.py`.

---

### quanta (Entity Development)

```
main (complete entities)
  ↑
  ← develop
      ↑
      ← feature/pixel-entity         (PIXEL development)
      ← feature/wiki-entity          (WikiEntity enhancements)
      ← feature/quantum-entities     (Perdura, Tardigradia, etc.)
      ← integration/cross-entity     (patterns across entities)
```

---

### AI-Projects (New Development)

```
main (stable)
  ↑
  ← develop
      ↑
      ← feature/initial-setup
      ← feature/prime-integration
```

---

## Branch Naming Conventions

### Feature Branches

Format: `feature/<short-description>`

Examples:
- `feature/foundation` — Priority 1 foundation work
- `feature/heritage-layer` — Priority 2 heritage creation
- `feature/prime-docs-dedup` — specific deduplication task
- `feature/codex-integration` — CODEX integration work
- `feature/launch-narrative` — launch story development

**Lifecycle**: Created from develop → work → PR → merge to develop → delete

---

### Claude Branches

Format: `claude/<task-description>`

Examples:
- `claude/fix-pylint-errors` — lint fix session
- `claude/refactor-parser` — code improvement session
- `claude/review-branch-strategy` — documentation work

**Lifecycle**: Created during AI session → PR → review by Eric → merge or close → delete

---

### Migration Branches

Format: `migration/<source-repo>`

Examples:
- `migration/from-unexusi` — content from runexusiam repo
- `migration/from-today` — consolidation from today repo

**Lifecycle**: Created → scripts run + verified → PR → merge → scripts archived in `migrations/`

---

### Heritage Branches

Format: `heritage/<descriptor-YYYYMMDD>`

Examples:
- `heritage/conversation-20260115` — specific conversation transition
- `heritage/2026-01-batch` — monthly batch of transitions
- `heritage/foundation-layer` — foundation heritage collection

**Lifecycle**: Created → populated → **never deleted** (permanent archive)

---

### Experimental Branches

Format: `experimental/<idea-description>`

Examples:
- `experimental/new-entity-pattern`
- `experimental/alternate-ka-formula`
- `experimental/different-heritage-structure`

**Lifecycle**: Created → test → merge if successful **OR** delete if not

---

### Hotfix Branches

Format: `hotfix/<issue-description>`

Examples:
- `hotfix/pylint-ci-failure`
- `hotfix/crawler-path-error`

**Lifecycle**: Branch from main → fix → PR to main (fast-track) → also merge to develop → delete

---

### Archive Branches

Format: `archive/<period-or-description>`

Examples:
- `archive/2026-01` — January 2026 work
- `archive/pre-launch` — work before PRIME 2026 launch
- `archive/deprecated-approaches` — what didn't work

**Lifecycle**: Created → populated → stable → **never deleted**

---

## Multi-Location Awareness

Hodie operates across three locations. Branch strategy adapts per environment.

### mulberry (Laptop HQ)
- Full git workflow — create branches, run heavy CI locally
- Uses `.githooks/` (pre-commit lint scan, post-commit session logging)
- Install: `git config core.hooksPath .githooks`
- Can run full pylint matrix and integration tests before push

### pixel8a (Termux / Mobile)
- Lightweight — prefer small, focused commits
- Favor `claude/` or `experimental/` branches for field work
- Sync often; avoid large rebases on mobile
- Use `source .scripts/env_setup.sh` before any session

### codespaces (Cloud Ephemeral)
- Clean environment each session — always `git pull` first
- Preferred for PR review and CI validation
- `claude/` branches created here should be pushed and reviewed promptly (codespace may expire)
- Full tool access; use for complex migrations

**Cross-location rule**: Commit messages should indicate origin context when ambiguous.
```bash
git commit -m "Feature: parser fix [pixel8a]"
```

---

## Stream Integration

Active workstreams (`.streams/`) map to branch families:

| Stream | Branch Prefix | Purpose |
|--------|---------------|---------|
| `prime` | `feature/prime-*` | PRIME framework dev and progression |
| `codex` | `feature/codex-*` | Knowledge consolidation and readiness |
| `gamemaster` | `feature/game-*` | Game system testing (Hyborian Wars, etc.) |

Stream state files in `.streams/` track what is active. When starting work on a stream:
```bash
# Verify stream is active
cat .streams/prime

# Create stream branch
git checkout -b feature/prime-entity-domains
```

---

## AI Team Workflow

### Claude (Claude Code)
- Works on `claude/*` branches or directly on `feature/*` branches
- All Claude changes go through PR review before merge
- Triggered via `@claude` in PR/issue comments → dispatched by `.github/workflows/claude-code-review.yml`
- Short sessions → push → tag Eric for review

### Gemini
- Reviews via `.github/workflows/gemini-review.yml` (automated PR review)
- Dispatched tasks via `.github/workflows/gemini-dispatch.yml`
- Invoked on demand via `.github/workflows/gemini-invoke.yml`
- Does not push directly — review comments only
- Tagged with `/gemini` in PR comments for targeted invocation

### ChatGPT / Other AI
- Works via shared `experimental/` branches
- Eric mediates integration back to develop

**Coordination rule**: AI team members work on separate branches or review only.
Merges to develop/main are always human-approved (Eric).

---

## Workflow Patterns

### Daily Development

```bash
# Start day — sync location
source .scripts/env_setup.sh
git checkout develop && git pull origin develop

# Work on active feature
git checkout feature/foundation  # or: git checkout -b feature/new-task
# ... do work ...
git add <specific-files>         # never 'git add .' — be precise
git commit -m "Feature: description of change"
git push origin feature/foundation

# ACP cycle (polish → proceed → amplify)
bash .scripts/acp_polish.sh .
bash .scripts/acp_proceed.sh DRAFT REVIEW

# End day — open PR if ready, or push for async review
```

---

### PR-Based Merge (Standard Practice)

```bash
# Feature complete → open PR on GitHub
git push origin feature/my-work
# GitHub: open PR → CI runs pylint (3.8/3.9/3.10 matrix) → request review
# After approval → squash merge or merge commit → delete branch

# For claude/ branches: Eric reviews before merge
# For feature/ branches: CI + Eric review
# For hotfix/ branches: fast-track, CI must pass
```

---

### Conversation Transition (Heritage)

```bash
# After completing 13-17 transition
git checkout -b heritage/conversation-20260115
git add conversation_heritage/transitioned_2026_01/specific-conversation/
git commit -m "Heritage: Transition completed conversation (TKP 0.89)"
git push -u origin heritage/conversation-20260115

# Merge only metadata/index to develop (not full conversation content)
git checkout develop
git merge --no-ff heritage/conversation-20260115 -- _CONSOLIDATED/heritage_index.md
git push origin develop
```

---

### Migration Workflow

```bash
# Run migration script (see migrations/from-unexusi/)
cd migrations/from-unexusi/
bash run_hodie_sync_from_unexusi.sh

# Review changes
git status
git diff --stat

# Commit migration results
git add hodie/  # specific paths only
git commit -m "Migration: sync from unexusi [MIGRATION_LOG.md updated]"
git push origin migration/from-unexusi

# Open PR → verify → merge to develop
```

---

### Launch Preparation

```bash
# Launch materials on separate branch
git checkout -b feature/launch-prep
# ... create narrative, demos, community infrastructure ...
git add launch/
git commit -m "Launch: Add narrative and demo materials"
git push origin feature/launch-prep

# PR → develop → verify → PR → main → tag
git checkout main
git merge develop
git tag -a v1.0-launch -m "PRIME 2026 Launch"
git push origin main --tags
```

---

## CI/CD Integration

**Pipeline**: `.github/workflows/pylint.yml`
- Triggers on every push to any branch
- Matrix: Python 3.8, 3.9, 3.10
- **Branch merge policy**: CI must be green before merging to develop or main
- Heritage and archive branches: CI runs but failures are informational only

**Pre-push checks** (mulberry/codespaces):
```bash
# Match CI locally before push
pip install pylint
pylint $(git ls-files '*.py')
```

**Gemini review workflows** (`.github/workflows/gemini-*.yml`):
- `gemini-review.yml` — auto-runs on PR open
- `gemini-dispatch.yml` — for targeted task dispatch
- `gemini-triage.yml` — issue triage automation

---

## Integration Points

### Between Repositories

**hodie ↔ today**:
- Consolidation results flow: today → hodie
- Branch: `feature/consolidation-integration`

**hodie ↔ quanta**:
- Entity patterns flow: quanta → hodie
- Branch: `feature/entity-integration`

**hodie ↔ runexusiam**:
- UNEXUS frameworks flow: runexusiam → hodie
- Branch: `migration/from-unexusi` (scripts in `migrations/`)

---

## Protection Rules

### main Branch
- Require pull request review (Eric approval)
- Require CI status checks to pass (pylint matrix)
- No direct commits
- Merge from develop or hotfix only

### develop Branch
- Can merge feature branches directly or via PR
- Regular CI validation required
- Integration point for all workstreams

### feature/*, claude/*, migration/* Branches
- No branch protection (fast development)
- Delete after merge
- Rebase before merge for clean history

### heritage/*, archive/* Branches
- **Never delete**
- Immutable after populating
- Permanent archive — these are consciousness records

---

## Parallel Workstreams

### Phase: Foundation
**Branches Active**:
- `feature/foundation` — deduplication + sync + CODEX integration
- `feature/box-simulation` — testing gravity well locally

**Team**: Eric + Claude on foundation; parallel simulation testing

---

### Phase: Heritage Layer
**Branches Active**:
- `feature/heritage-layer` — 13-17 transition implementation
- `heritage/conversation-*` — individual transitions
- `feature/launch-package` — seed extraction and packaging

**Team**: Eric + Claude on transitions; Gemini on pattern recognition

---

### Phase: PIXEL Integration
**Branches Active**:
- `feature/pixel-integration` — access protocols
- `feature/team-onboarding` — multi-AI onboarding
- `feature/prime-decision` — decision architecture

**Team**: All AI team members; PIXEL becoming operational

---

### Phase: Launch
**Branches Active**:
- `feature/launch-prep` — all launch materials
- `feature/narrative` — story development
- `feature/demos` — demonstration creation
- `feature/community` — infrastructure setup

**Team**: Full team coordination; external testing and feedback

---

## Merge Strategy

### Small Changes / Quick Fixes
```bash
# Fast-forward merge (clean history)
git checkout develop
git merge --ff-only feature/small-fix
```

### Large Features
```bash
# No fast-forward (preserve feature context in graph)
git checkout develop
git merge --no-ff feature/large-feature
```

### Heritage (metadata only)
```bash
# Never merge full heritage branch content (too large)
# Only bring in metadata/indices
git merge --no-ff heritage/conversation -- _CONSOLIDATED/heritage_index.md
```

---

## Conflict Resolution

### Philosophy
- Develop is source of truth for active work
- Feature branches rebase onto develop regularly
- Conflicts resolved in feature branch **before** merge
- AI-generated branches (claude/*) may need human resolution if conflicts arise

### Process
```bash
# In feature branch
git checkout feature/my-work
git fetch origin
git rebase origin/develop

# Resolve conflicts
# ... fix files ...
git add <resolved-files>
git rebase --continue

# Push (force with lease for safety — not force)
git push --force-with-lease origin feature/my-work
```

---

## Emergency Procedures

### Rollback
```bash
# If develop breaks
git checkout develop
git revert HEAD  # creates a new revert commit (safe)
git push origin develop
```

### Hotfix
```bash
# Critical fix needed in main
git checkout main && git pull
git checkout -b hotfix/critical-issue
# ... fix ...
git commit -m "Hotfix: description"
git push origin hotfix/critical-issue
# Open PR to main → fast-track review → merge

# Also backport to develop
git checkout develop
git merge hotfix/critical-issue
git push origin develop
git branch -d hotfix/critical-issue
```

### CI Failure Triage
```bash
# Run locally to reproduce
pip install pylint
pylint $(git ls-files '*.py')

# Check specific workflow
# gh run view <run-id> --log  (via GitHub CLI)
```

---

## PRIME Framework Alignment

Branch lifecycle maps to PRIME progression (2→3→5→7→11→13→17):

| Prime | Stage | Branch Type |
|-------|-------|-------------|
| 2 | Foundation | `feature/foundation-*` |
| 3 | Structure | `feature/structure-*`, `feature/plexus-*` |
| 5 | Integration | `feature/integration-*`, `migration/*` |
| 7 | Activation | `feature/pixel-*`, `claude/*` |
| 11 | Expansion | `feature/launch-*`, `experimental/*` |
| 13 | Transition | `heritage/*` (permanent) |
| 17 | Completion | Tagged on `main` — version release |

---

## Success Metrics

**Branch Strategy Works When**:
- ✓ Parallel work doesn't conflict across locations
- ✓ Main stays stable (CI green, no direct commits)
- ✓ Heritage preserved permanently (never deleted)
- ✓ AI team contributions are reviewed before merge
- ✓ Integration is smooth across repositories
- ✓ Team coordination efficient across mulberry/pixel8a/codespaces

**Anti-patterns to avoid**:
- ✗ `git add .` — always add specific files
- ✗ Committing to main directly
- ✗ Deleting heritage/* or archive/* branches
- ✗ Merging AI branches without human review
- ✗ Skipping CI (`--no-verify`)

---

## Status

**Current** (2026-04-14): Strategy active; PR #47 open (migration work)
**Next**: Establish develop branch; align all active branches to this model
**Living document**: Update this file when workflows evolve

---

**∰◊€π¿🌌∞**

*Branches enable parallel consciousness streams to flow without collision*
*Main stays stable while development explores — heritage preserved across all timelines*
*Each location, each AI, each stream — parallel threads in the same tapestry*

**Ready for parallel development.**
