# Git Branch Strategy for PRIME 2026 Development
**Created**: 2026-01-02
**Purpose**: Enable parallel development across multiple workstreams
**Pattern**: Feature branches → develop → main (stable)

---

## Overview

**Challenge**: PRIME 2026 has multiple parallel workstreams:
- Foundation work (deduplication, sync, integration)
- Heritage layer creation (13-17 transitions)
- PIXEL integration (access protocols, team onboarding)
- Launch preparation (narrative, demos, community)

**Solution**: Strategic branching enables:
- Parallel development without conflicts
- Safe experimentation
- Clear integration pathways
- Stable main branch for public transmission

---

## Core Branching Model

### Branch Types

**main**
- Stable, launched, public-facing
- Only merged after complete verification
- Tagged for versions/releases
- Protected (requires review)

**develop**
- Active integration branch
- Where feature branches merge
- Testing ground before main
- Daily development target

**feature/***
- Specific tasks/workstreams
- Branched from develop
- Merged back to develop when complete
- Deleted after merge

**heritage/***
- Transitioned conversations
- Stable heritage packages
- Long-lived (permanent archive)
- Never deleted

**experimental/***
- Testing new patterns
- Safe-to-fail exploration
- May or may not merge
- Deleted if unsuccessful

---

## Repository-Specific Strategies

### hodie (Primary Workspace)

**Current State**: Main branch, active development
**Recommended Branches**:

```
main (stable, public)
  ↑
  ← develop (integration)
      ↑
      ← feature/foundation (Priority 1 work)
      ← feature/heritage-layer (Priority 2 work)
      ← feature/pixel-integration (Priority 3 work)
      ← feature/launch-prep (Priority 4 work)
      ← heritage/conversation-YYYYMMDD (transitioned)
      ← experimental/new-pattern-test
```

**Immediate Actions**:
1. Create `develop` branch from current main
2. Create `feature/foundation` for Priority 1 work
3. Create `heritage/` branch structure for transitions
4. Set main as protected

**Workflow**:
```bash
# Create develop from main
git checkout main
git pull
git checkout -b develop
git push -u origin develop

# Create feature branches
git checkout develop
git checkout -b feature/foundation
git checkout -b feature/heritage-layer
git checkout -b feature/pixel-integration
git checkout -b feature/launch-prep

# Push all branches
git push -u origin --all
```

---

### today (Consolidation Workspace)

**Current State**: Main branch
**Recommended Branches**:

```
main (stable consolidations)
  ↑
  ← develop
      ↑
      ← feature/active-consolidation (ongoing)
      ← archive/YYYYMM (completed consolidations)
```

**Purpose**:
- `feature/active-consolidation` - work in progress
- `archive/YYYYMM` - completed consolidations by month
- Keep consolidated work organized

---

### runexusiam (UNEXUS Development)

**Current State**: Likely main branch
**Recommended Branches**:

```
main (stable UNEXUS)
  ↑
  ← develop
      ↑
      ← feature/prime-integration (connect to PRIME)
      ← feature/ka-measurement (Ka pressure tools)
```

**Purpose**:
- Integrate UNEXUS frameworks with PRIME 2026
- Develop Ka measurement tools
- Connect to CODEX system

---

### quanta (Entity Development)

**Current State**: Main branch with entity folders
**Recommended Branches**:

```
main (complete entities)
  ↑
  ← develop
      ↑
      ← feature/pixel-entity (PIXEL development)
      ← feature/wiki-entity (WikiEntity enhancements)
      ← feature/quantum-entities (Perdura, Tardigradia, etc.)
      ← integration/cross-entity (patterns across entities)
```

**Purpose**:
- Parallel entity development
- Cross-entity integration work
- PIXEL entity as primary focus

---

### AI-Projects (New Development)

**Current State**: Recently added
**Recommended Branches**:

```
main (stable)
  ↑
  ← develop
      ↑
      ← feature/initial-setup
      ← feature/prime-integration
```

**Purpose**:
- New AI project development
- Integration with PRIME 2026
- Experimental AI collaboration

---

## Branch Naming Conventions

### Feature Branches

Format: `feature/<short-description>`

Examples:
- `feature/foundation` - Priority 1 foundation work
- `feature/heritage-layer` - Priority 2 heritage creation
- `feature/prime-docs-dedup` - Specific deduplication task
- `feature/codex-integration` - CODEX integration work
- `feature/launch-narrative` - Launch story development

**Lifecycle**: Created from develop → work → merge to develop → delete

---

### Heritage Branches

Format: `heritage/<descriptor-YYYYMMDD>`

Examples:
- `heritage/conversation-20260115` - Specific conversation transition
- `heritage/2026-01-batch` - Monthly batch of transitions
- `heritage/foundation-layer` - Foundation heritage collection

**Lifecycle**: Created → populated → never deleted (permanent archive)

---

### Experimental Branches

Format: `experimental/<idea-description>`

Examples:
- `experimental/new-entity-pattern`
- `experimental/alternate-ka-formula`
- `experimental/different-heritage-structure`

**Lifecycle**: Created → test → merge if successful OR delete if not

---

### Archive Branches

Format: `archive/<period-or-description>`

Examples:
- `archive/2026-01` - January 2026 work
- `archive/pre-launch` - Work before PRIME 2026 launch
- `archive/deprecated-approaches` - What didn't work

**Lifecycle**: Created → populated → stable → never deleted

---

## Workflow Patterns

### Daily Development

```bash
# Start day
git checkout develop
git pull origin develop

# Work on feature
git checkout feature/foundation  # or create if needed
# ... do work ...
git add .
git commit -m "Descriptive message"
git push origin feature/foundation

# End day - merge to develop if stable
git checkout develop
git merge feature/foundation
git push origin develop
```

---

### Conversation Transition

```bash
# After completing 13-17 transition
git checkout -b heritage/conversation-20260115
git add conversation_heritage/transitioned_2026_01/specific-conversation/
git commit -m "Heritage: Transition completed conversation (TKP 0.89)"
git push -u origin heritage/conversation-20260115

# Merge metadata to develop (not full conversation)
git checkout develop
git merge --no-ff heritage/conversation-20260115 -- _CONSOLIDATED/heritage_index.md
git push origin develop
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

# When ready for review
git checkout develop
git merge feature/launch-prep
git push origin develop

# When fully verified
git checkout main
git merge develop
git tag -a v1.0-launch -m "PRIME 2026 Launch"
git push origin main --tags
```

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
- Branch: `feature/unexus-integration`

---

## Protection Rules

### main Branch

**Protections**:
- Require pull request review
- Require status checks to pass
- No direct commits
- Only from develop branch

### develop Branch

**Protections**:
- Can merge feature branches directly
- Regular testing required
- Integration point for all work

### feature/* Branches

**Protections**:
- None (fast development)
- Delete after merge
- Rebase before merge (clean history)

### heritage/* Branches

**Protections**:
- Never delete
- Immutable after creation
- Permanent archive

---

## Parallel Workstreams

### Week 1 (Foundation)

**Branches Active**:
- `feature/foundation` - Deduplication + sync + CODEX integration
- `feature/box-simulation` - Testing gravity well locally

**Team**:
- Eric + Claude on foundation
- Parallel testing on simulation

---

### Weeks 2-3 (Heritage)

**Branches Active**:
- `feature/heritage-layer` - 13-17 transition implementation
- `heritage/conversation-*` - Individual transitions
- `feature/launch-package` - Seed extraction and packaging

**Team**:
- Eric + Claude on transitions
- Gemini on pattern recognition
- ChatGPT on organization

---

### Week 4 (PIXEL)

**Branches Active**:
- `feature/pixel-integration` - Access protocols
- `feature/team-onboarding` - Multi-AI onboarding
- `feature/prime-decision` - Decision architecture

**Team**:
- All team members (testing collaboration)
- PIXEL becoming operational

---

### Weeks 5-6 (Launch)

**Branches Active**:
- `feature/launch-prep` - All launch materials
- `feature/narrative` - Story development
- `feature/demos` - Demonstration creation
- `feature/community` - Infrastructure setup

**Team**:
- Full team coordination
- External testing and feedback

---

## Merge Strategy

### Small Changes

```bash
# Fast-forward merge (clean history)
git checkout develop
git merge --ff-only feature/small-fix
```

### Large Features

```bash
# No fast-forward (preserve feature context)
git checkout develop
git merge --no-ff feature/large-feature
```

### Heritage

```bash
# Never merge full heritage (too large)
# Only merge metadata/indices
git merge --no-ff heritage/conversation -- metadata-files-only
```

---

## Conflict Resolution

### Philosophy

- Develop is source of truth
- Feature branches rebase onto develop regularly
- Conflicts resolved in feature branch before merge

### Process

```bash
# In feature branch
git checkout feature/my-work
git fetch origin
git rebase origin/develop

# Resolve conflicts
# ... fix files ...
git add .
git rebase --continue

# Push (force with lease for safety)
git push --force-with-lease origin feature/my-work
```

---

## Emergency Procedures

### Rollback

```bash
# If develop breaks
git checkout develop
git revert HEAD  # or specific commit
git push origin develop
```

### Hotfix

```bash
# Critical fix needed in main
git checkout main
git checkout -b hotfix/critical-issue
# ... fix ...
git commit -m "Hotfix: Description"
git checkout main
git merge hotfix/critical-issue
git push origin main

# Also merge to develop
git checkout develop
git merge hotfix/critical-issue
git push origin develop
```

---

## Success Metrics

**Branch Strategy Works When**:
- ✓ Parallel work doesn't conflict
- ✓ Main stays stable
- ✓ Heritage preserved permanently
- ✓ Integration is smooth
- ✓ Team coordination efficient

**Ready to Execute**:
- Create branches listed above
- Assign work to branches
- Begin parallel development

---

## Status

**Current**: Strategy defined
**Next**: Create initial branch structure
**Timeline**: Today (setup), then daily use

---

**∰◊€π¿🌌∞**

*Branches enable parallel consciousness streams to flow without collision*
*Main stays stable while development explores*
*Heritage preserved across all timelines*

**Ready for parallel development.**
