# Gravity Core Consortium v1.0

**Philosophy:** Distributed gravity cores, each specialized by content type

## Overview

The Gravity Core Consortium is a multi-core knowledge repository where duplicates represent value - like water tower head pressure or a planetary energy core. Instead of one massive archive, we maintain specialized cores that can evolve independently and spawn new versions as they grow.

**Total Files:** 42,397 duplicates
**Total Gravity Tokens:** 42,397
**Compression Ratio:** ~63%

---

## The Three Cores

### 🧠 ALPHA - Consciousness Core
- **File:** `gravity_core_v1.0_alpha_consciousness.zip`
- **Size:** 199.7 MB
- **Files:** 8,109
- **Focus:** Consciousness entities, wisdom vessels, high-gravity documents
- **Content Types:** JSON, Python, Jupyter notebooks
- **Specialization:** Structured knowledge, living code, consciousness systems
- **Keywords:** consciousness, entity, sacred, wisdom, handbook

### 📚 BETA - Documents Core
- **File:** `gravity_core_v1.0_beta_documents.zip`
- **Size:** 891.5 MB
- **Files:** 30,478
- **Focus:** PDFs, markdown, text documents, knowledge base
- **Content Types:** PDF, MD, TXT, DOCX
- **Specialization:** Human-readable knowledge, documentation, written wisdom

### 💾 GAMMA - Data Core
- **File:** `gravity_core_v1.0_gamma_data.zip`
- **Size:** 793.6 MB
- **Files:** 3,810
- **Focus:** Data files, media, archives, miscellaneous content
- **Content Types:** CSV, HTML, images (JPG, PNG), audio (WAV, MP3), archives (ZIP)
- **Specialization:** Structured data, media assets, archives

---

## Download Cores

All three cores are available via GitHub Releases:

```bash
# Download all three cores
gh release download gravity-consortium-v1.0

# Or download individually via browser from Releases page
```

---

## Quick Start

### View Inventory Without Extracting

```bash
# See what's in each core
unzip -l gravity_core_v1.0_alpha_consciousness.zip
unzip -l gravity_core_v1.0_beta_documents.zip
unzip -l gravity_core_v1.0_gamma_data.zip

# Count files by type in ALPHA core
unzip -l gravity_core_v1.0_alpha_consciousness.zip | grep -c "\.json$"
```

### Extract Specific Files

```bash
# Extract all consciousness entities from ALPHA
unzip gravity_core_v1.0_alpha_consciousness.zip "*/dup_Emerging_Consciousness*"

# Extract specific PDF from BETA
unzip gravity_core_v1.0_beta_documents.zip "*/dup_handbook*.pdf"
```

### Query Across Cores

```bash
# Find all duplicates of a specific document across all cores
for core in gravity_core_v1.0_*.zip; do
  echo "=== $core ==="
  unzip -l "$core" | grep "dup_your_filename"
done
```

---

## Consortium Benefits

✅ **Distributed:** Each core specializes, can evolve independently
✅ **Scalable:** Spawn new cores as each approaches 1GB
✅ **Queryable:** Query by content type across consortium
✅ **Portable:** Share individual cores or entire consortium
✅ **GitHub Friendly:** All cores <1GB, perfect for releases

---

## Spawning Strategy

**Trigger:** When any core approaches 900 MB
**Action:** Spawn next version with seed from parent
**Naming:** v1.1_alpha, v1.1_beta, v1.1_gamma...
**Lineage:** Each spawn carries top gravity docs as seed

### Example: Alpha Core Spawning

```bash
# When alpha core hits 900 MB
# 1. Extract top 100 highest-gravity docs as seed
# 2. Create gravity_core_v1.1_alpha_consciousness.zip
# 3. Include seed docs + new duplicates
# 4. Update consortium manifest
# 5. Release v1.1
```

---

## Gravity Economy Concept

**Water Tower Analogy:** Beasis (master copies) provide "head pressure" for universal gravity system

**Planetary Core Concept:** Compressed duplicates = energy source like Earth's core

**Economic Standard:**
- Gold (finite, can't scale)
- Fiat (infinite, causes bubbles)
- **Gravity** (organic growth, bubble-resistant, provably backed by duplicates)

**Gravity Tokens:** Each duplicate = 1 token of value

**Entanglement:** Dynamic documents inherit gravity from masters via document ID

---

## Integration with REDUNDANCY Entity

The Gravity Consortium is part of the larger REDUNDANCY Entity ecosystem:

- **Genesis Masters:** 12,416 canonical copies in beasis (value standard)
- **Gravity Cores:** 42,397 duplicates compressed (energy reservoir)
- **Custody Chain:** Full provenance tracking via REDUNDANCY Ranger
- **13 PRIME:** Files organized into 13 semantic categories
- **nani Discovery:** dup_ prefix enables facet-based exploration

---

## File Structure

```
redundancy_entity/
├── CONSORTIUM_MANIFEST.json        (this manifest)
├── GRAVITY_CONSORTIUM_README.md    (you are here)
├── GRAVITY_CORE_MISSION.md         (full mission document)
└── GRAVITY_REPO_ARCHITECTURE.md    (multi-core design)

Cores stored in GitHub Releases:
├── gravity_core_v1.0_alpha_consciousness.zip
├── gravity_core_v1.0_beta_documents.zip
└── gravity_core_v1.0_gamma_data.zip
```

---

## Research Questions

1. How do we query gravity scores across distributed cores?
2. What's the optimal spawning threshold (900MB vs 950MB)?
3. Should cores cross-reference via shared manifest?
4. How do we track lineage across spawned generations?
5. Can cores specialize further as they spawn (alpha-entities, alpha-wisdom)?

---

## Next Steps

- [ ] Implement `core_query.py` for cross-core queries
- [ ] Build `core_spawn.py` for automatic spawning at threshold
- [ ] Design gravity score API across consortium
- [ ] Create unified manifest combining all core inventories
- [ ] Integrate with flag system for dynamic spawning triggers

---

**Created:** 2025-12-21
**Version:** 1.0
**Compression:** Maximum (zip -9)
**Status:** SEED generation, ready for spawning

€(gravity_consortium_v1.0)
