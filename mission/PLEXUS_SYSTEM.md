# PLEXUS Processing System
**Hodie Repository Organization**
**Date**: 2025-12-24
**Concept**: Staged processing pipeline with gravitational flow

---

## System Philosophy

**Prevent Crawler Overload**: Documents move through stages. Once processed, they exit the active pipeline so the crawler only sees what needs work.

**Gravitational Flow**: Content flows through complexity levels (simplex → omniplex) based on processing needs.

---

## Directory Structure

```
hodie/
├── plexus/              ← Processing stages
│   ├── simplex/         ← Files good as-is (1D, ready)
│   ├── duplex/          ← Duplicates to sort (2D, pairs)
│   ├── triplex/         ← Docs ready for entity processing (3D, relationships)
│   ├── quadroplex/      ← Foundations & operations (4D, structure)
│   ├── uniplex/         ← Sparkle's one-dimensional (singular focus)
│   ├── multiplex/       ← Multi-stage processing
│   └── omniplex/        ← All-encompassing (complete)
│
├── duplicatus/          ← Found duplicates (Latin: duplicated)
├── exemplar/            ← Intentional copies (templates, examples)
├── gravitar/            ← Gravity wells (duplicate collections)
│
└── rudera/              ← Debris management (Latin: ruins)
    ├── strues/          ← Piles, heaps (organized debris)
    ├── fragmenta/       ← Fragments (partial content)
    └── pulvis/          ← Dust (minimal value, origin concept)
```

---

## Plexus Stages (Processing Pipeline)

### simplex/ - Ready State
**Purpose**: Files that are complete and ready to use
**Criteria**:
- Good as-is
- No duplicates
- Properly named
- Well organized

**Action**: None needed, ready for reference/use
**Next**: Stays here or moves to archive

---

### duplex/ - Duplicate Processing
**Purpose**: Sort and handle duplicates
**Criteria**:
- Multiple copies found
- Need comparison
- Determine which to keep

**Action**: Run duplicate detection and sorting
**Next**: Keep → simplex, Extras → duplicatus or gravitar

---

### triplex/ - Entity Preparation
**Purpose**: Documents ready for entity processing
**Criteria**:
- Relationships identified
- Ready for consciousness entity work
- Structured for processing

**Action**: Entity operations (pattern recognition, connection mapping)
**Next**: Processed → quadroplex or simplex

---

### quadroplex/ - Foundations & Operations
**Purpose**: Core infrastructure and operational frameworks
**Criteria**:
- Foundation documents
- Operational procedures
- System architecture

**Action**: Build/maintain core systems
**Next**: Operational → simplex, Evolving → omniplex

---

### uniplex/ - Singular Focus (Sparkle)
**Purpose**: One-dimensional, single-purpose items
**Criteria**:
- Single clear purpose
- No complex relationships
- Sparkle-style simplicity

**Action**: Preserve simplicity, quick processing
**Next**: Complete → simplex

---

### multiplex/ - Multi-Stage Processing
**Purpose**: Items needing multiple processing passes
**Criteria**:
- Complex transformations needed
- Multiple stages required
- Interdependencies

**Action**: Stage-by-stage processing
**Next**: Complete → appropriate stage or omniplex

---

### omniplex/ - Complete Integration
**Purpose**: Fully integrated, all-encompassing
**Criteria**:
- All processing complete
- Fully integrated
- Ready for final form

**Action**: Final validation and integration
**Next**: Archive or active reference

---

## Duplicate Management

### duplicatus/ - Found Duplicates
**Purpose**: Store duplicates discovered during processing
**Structure**:
```
duplicatus/
├── by_hash/        ← Grouped by file hash
├── by_name/        ← Grouped by similar names
└── to_review/      ← Needs human decision
```

**Concept**: Latin "duplicatus" = duplicated
**Part of**: DUO (duplex) in AND, OR, NOT, ORIGIN system

---

### exemplar/ - Intentional Copies
**Purpose**: Copies that are meant to exist
**Use Cases**:
- Templates
- Examples
- Reference copies
- Backup originals

**Rule**: Never delete from exemplar - these are intentional

---

### gravitar/ - Gravity Wells
**Purpose**: Duplicate collections with gravity-weighted value
**Concept**: From Redundancy Ranger - duplicates collect like gravity
**Structure**:
```
gravitar/
├── pinnacle/       ← Best copy (highest quality)
├── verified/       ← Verified duplicates
└── chain_of_custody.json
```

**Process**:
1. Duplicates collected
2. Quality assessed (gravity weight)
3. Pinnacle copy identified
4. Rest preserved in gravity well
5. Chain of custody maintained

---

## Rudera - Debris Management

### rudera/ - Ruins & Trash
**Purpose**: Manage unwanted, broken, or debris content
**Concept**: Latin "rudera" = ruins, rubble, rubbish

### strues/ - Organized Debris
**Purpose**: Piles and heaps - organized trash
**Use**: Items that might have value but not immediately useful
**Concept**: Latin "strues" = pile, heap

### fragmenta/ - Fragments
**Purpose**: Partial content, incomplete files
**Use**: Pieces that might be useful for recovery or reference
**Concept**: Latin "fragmenta" = fragments

### pulvis/ - Dust
**Purpose**: Minimal value, fine debris
**Connection**: Fits ORIGIN concept (fundamental particles)
**Use**: Candidates for final deletion
**Concept**: Latin "pulvis" = dust

---

## One Hertz Operations

### Concept
One operation per cycle (one hertz = 1 Hz = one per second/cycle)
**Prevents overload**: Process one stage at a time

### Operation Sequence
```
1. Scan incoming content
2. Route to appropriate plex stage
3. Process that stage completely
4. Move to next stage or completion
5. Update PLEXUS UI
6. Next cycle
```

### Benefits
- Crawler only sees active stage
- Completed items don't reload
- Clear progress tracking
- Prevents system overload

---

## PLEXUS UI Concept

**Central Interface** for all operations:
- View all stages at once
- Track items in each plex
- Trigger one hertz ops
- Monitor progress
- Access any stage

**Dashboard View**:
```
┌─────────────────────────────────────┐
│ PLEXUS UI - Hodie Processing        │
├─────────────────────────────────────┤
│ simplex:     142 files  ✓ Ready     │
│ duplex:       89 files  ⚙ Processing│
│ triplex:      34 files  ⏳ Pending  │
│ quadroplex:   12 files  ⚙ Active    │
│ uniplex:      56 files  ✓ Complete  │
│ multiplex:     8 files  ⚙ Stage 2/4 │
│ omniplex:     23 files  ✓ Integrated│
├─────────────────────────────────────┤
│ duplicatus:   201 files  📦 Stored  │
│ gravitar:      15 wells  ⚖ Weighted│
│ rudera:        78 items  🗑 Managed │
└─────────────────────────────────────┘
```

---

## File Naming Issues

### Trailing Space Problem
**Issue**: Many folders/files have space as last character
**Impact**: Breaks paths, confuses systems, hard to access

**Detection**:
```bash
# Find folders with trailing space
find . -type d -name "* "

# Find files with trailing space
find . -type f -name "* "
```

**Fix Strategy**:
1. Scan and identify
2. Generate rename script
3. Review before execution
4. Rename in batches
5. Verify integrity

---

## Integration with Existing Systems

### Beasis (from redundancy_entity/)
- Beasis catalog → gravitar pinnacle copies
- Duplicate collections → gravitar wells
- Proof of gravity → chain of custody

### Today Folder
- Current today/ content → process through plexus stages
- today_from_drive_SAFE/ → route to appropriate plex

### Scripts Hub
- One hertz operation scripts
- Stage processors
- UI components

---

## Processing Workflow

### 1. Intake
New content arrives → Route to appropriate plex stage

### 2. One Hertz Processing
```
CYCLE 1: Process duplex (sort duplicates)
  → Good files → simplex
  → Dups → duplicatus
  → Intentional → exemplar

CYCLE 2: Process triplex (entity work)
  → Processed → simplex or quadroplex
  → Incomplete → stays in triplex

CYCLE 3: Process quadroplex (foundations)
  → Operational → simplex
  → Evolving → multiplex or omniplex
```

### 3. Completion
Fully processed → simplex or omniplex
**Result**: Crawler no longer needs to load these

---

## AND, OR, NOT, ORIGIN Connection

**DUO (Duplex)**:
- Part of logical system
- AND: both copies exist
- OR: either copy valid
- NOT: not a duplicate (unique)
- ORIGIN: source/pinnacle copy

**Pulvis (Dust)**:
- Connects to ORIGIN
- Fundamental particles
- Reduced to basics
- Starting material

---

## Next Steps

### Immediate Setup
1. ✓ Create folder structure
2. Create .gitignore for each stage
3. Add README to each plex folder
4. Create initial processing scripts

### Fix Trailing Spaces
1. Scan for all trailing space issues
2. Generate comprehensive fix list
3. Create safe rename script
4. Execute with verification

### Develop One Hertz Ops
1. Design operation sequence
2. Create processing scripts
3. Build PLEXUS UI
4. Test with sample data

### Integration
1. Route today_from_drive_SAFE through plexus
2. Connect to gravitar system
3. Link with beasis catalog
4. Establish chain of custody

---

**∰◊€π¿🌌∞**

€(plexus_system_design)
*System Status: STRUCTURED_AND_READY*
*Processing Model: ONE_HERTZ_OPERATIONS*
*Reality Anchor: Oregon Watersheds*

---

**Date**: 2025-12-24
**Repository**: github.com/Eaprime1/hodie
**Drive**: drive.google.com/drive/folders/1qSUXHL4fXb8R1n3wBG4A8bwUOWE6SNOf
**Companion**: github.com/Eaprime1/plex (automation workspace)
