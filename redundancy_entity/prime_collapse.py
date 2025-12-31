#!/usr/bin/env python3
"""
13 PRIME Pyramidic Collapse
Transform beasis into navigable knowledge structure

Transforms 55,022 files → 13 semantic categories
Makes searching, reading, discovery natural through seed ideas
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# === CONFIGURATION ===
REDUNDANCY_DIR = "/storage/emulated/0/pixel8a/Q/redundancy_entity"
CATALOG_FILE = os.path.join(REDUNDANCY_DIR, "beasis_catalog.json")
BEASIS_ROOT = "/storage/emulated/0/unexusi_beasis"
PRIME_ROOT = os.path.join(BEASIS_ROOT, "beasis_13prime")

# === 13 PRIME FRAMEWORK ===
PRIME_CATEGORIES = {
    2: {
        'name': 'Foundation',
        'seed': 'What is the foundation?',
        'description': 'Core concepts, definitions, setup, guides',
        'keywords': ['readme', 'manifest', 'guide', 'setup', 'init', 'index', 'intro']
    },
    3: {
        'name': 'Duality',
        'seed': 'What are the pairs?',
        'description': 'Relationships, conversations, Q&A, comparisons',
        'keywords': ['conversation', 'chat', 'q&a', 'dialogue', 'pair', 'relationship']
    },
    5: {
        'name': 'Creativity',
        'seed': 'What creates?',
        'description': 'Generative content, scripts, entities, creative works',
        'keywords': ['entity', 'consciousness', 'creative', 'generate', 'create', 'script']
    },
    7: {
        'name': 'Process',
        'seed': 'What flows?',
        'description': 'Workflows, procedures, ceremonial flows, steps',
        'keywords': ['flow', 'workflow', 'step', 'procedure', 'process', 'ceremonial']
    },
    11: {
        'name': 'Structure',
        'seed': 'What organizes?',
        'description': 'Frameworks, architectures, schemas, structured data',
        'keywords': ['framework', 'structure', 'schema', 'architecture', 'organized']
    },
    13: {
        'name': 'Transformation',
        'seed': 'What changes?',
        'description': 'Evolution, development, transitions, version histories',
        'keywords': ['transform', 'transition', 'evolution', 'change', 'develop', '13-17']
    },
    17: {
        'name': 'Emergence',
        'seed': 'What emerges?',
        'description': 'Novel insights, consciousness, emergent patterns',
        'keywords': ['emerging', 'emerge', 'sacred', 'novel', 'birth', 'arising']
    },
    19: {
        'name': 'Completion',
        'seed': 'What completes?',
        'description': 'Final versions, summaries, conclusions, finished works',
        'keywords': ['final', 'complete', 'summary', 'conclusion', 'finished', 'done']
    },
    23: {
        'name': 'Abundance',
        'seed': 'What multiplies?',
        'description': 'High-duplicate content, distributed wisdom, replication',
        'keywords': ['abundance', 'multiple', 'replicate', 'distribute', 'fountain']
    },
    29: {
        'name': 'Connection',
        'seed': 'What connects?',
        'description': 'References, links, networks, cross-references',
        'keywords': ['link', 'reference', 'network', 'connect', 'relation', 'web']
    },
    31: {
        'name': 'Vision',
        'seed': 'What sees?',
        'description': 'Visual content, maps, diagrams, media',
        'keywords': ['visual', 'map', 'diagram', 'image', 'video', 'graphic']
    },
    37: {
        'name': 'Wisdom',
        'seed': 'What teaches?',
        'description': 'Handbooks, teaching materials, wisdom vessels',
        'keywords': ['handbook', 'wisdom', 'teach', 'vessel', 'knowledge', 'formulae']
    },
    41: {
        'name': 'Transcendence',
        'seed': 'What exceeds?',
        'description': 'Meta-documents, self-referential, beyond-category',
        'keywords': ['meta', 'transcend', 'beyond', 'exceed', 'infinite']
    }
}

def load_catalog():
    """Load REDUNDANCY catalog"""
    print(f"\n📋 Loading REDUNDANCY catalog...")
    with open(CATALOG_FILE, 'r') as f:
        catalog = json.load(f)
    print(f"   ✓ Loaded {len(catalog):,} unique file families")
    return catalog

def classify_to_prime(file_info):
    """
    Classify file to PRIME category

    Uses multiple signals:
    - Filename keywords
    - Extension
    - Duplicate count (high dup → Abundance)
    - Gravity score
    """
    filename = file_info['filename'].lower()
    ext = file_info['extension'].lower()
    dup_count = file_info['duplicate_count']
    gravity = file_info['gravity_score']

    scores = defaultdict(int)

    # Check keywords for each PRIME
    for prime, info in PRIME_CATEGORIES.items():
        for keyword in info['keywords']:
            if keyword in filename:
                scores[prime] += 10

    # Extension-based classification
    if ext == '.py':
        scores[5] += 15  # Creativity (scripts)
    elif ext == '.json':
        scores[11] += 10  # Structure
    elif ext in ['.md', '.txt']:
        if 'conversation' in filename or 'chat' in filename:
            scores[3] += 15  # Duality
        elif 'final' in filename or 'complete' in filename:
            scores[19] += 15  # Completion
        else:
            scores[2] += 5  # Foundation (docs)
    elif ext in ['.pdf', '.png', '.jpg', '.jpeg']:
        scores[31] += 15  # Vision
    elif ext in ['.mp4', '.mov', '.avi']:
        scores[31] += 20  # Vision (media)
    elif ext in ['.wav', '.mp3', '.flac']:
        scores[31] += 10  # Vision (audio)

    # High duplicates → Abundance
    if dup_count > 50:
        scores[23] += 30
    elif dup_count > 20:
        scores[23] += 20
    elif dup_count > 10:
        scores[23] += 10

    # High gravity → could be Wisdom or Emergence
    if gravity > 500:
        scores[37] += 10  # Wisdom
        scores[17] += 10  # Emergence

    # Special patterns
    if 'entity' in filename or 'consciousness' in filename:
        if 'emerging' in filename:
            scores[17] += 20  # Emergence
        else:
            scores[5] += 15  # Creativity

    if 'sacred' in filename:
        scores[17] += 20  # Emergence

    if 'handbook' in filename or 'formulae' in filename:
        scores[37] += 25  # Wisdom

    if 'flow' in filename or 'ceremonial' in filename:
        scores[7] += 20  # Process

    if '13-17' in filename or 'transition' in filename:
        scores[13] += 25  # Transformation

    if 'readme' in filename or 'manifest' in filename:
        scores[2] += 25  # Foundation

    # Get highest scoring PRIME
    if scores:
        return max(scores.items(), key=lambda x: x[1])[0]
    else:
        # Default: Foundation
        return 2

def create_prime_structure():
    """Create 13 PRIME directory structure"""
    print(f"\n🏗️  Creating 13 PRIME pyramidic structure...")

    for prime, info in PRIME_CATEGORIES.items():
        prime_dir = os.path.join(PRIME_ROOT, f"PRIME_{prime:02d}_{info['name']}")
        os.makedirs(prime_dir, exist_ok=True)
        print(f"   ✓ PRIME {prime:02d}: {info['name']}")

    print(f"\n   Structure created at: {PRIME_ROOT}")
    return True

def generate_seed_file(prime, files_in_category):
    """
    Generate seed_idea.md for a PRIME category

    Includes:
    - Seed question
    - Quick discovery (what's here)
    - High-gravity items
    - Connections to other PRIMEs
    - Browse stats
    """
    info = PRIME_CATEGORIES[prime]
    prime_dir = os.path.join(PRIME_ROOT, f"PRIME_{prime:02d}_{info['name']}")

    # Sort by gravity
    sorted_files = sorted(files_in_category, key=lambda x: x['gravity_score'], reverse=True)

    # Extension counts
    ext_counts = defaultdict(int)
    for f in files_in_category:
        ext_counts[f['extension']] += 1

    # Top extensions
    top_exts = sorted(ext_counts.items(), key=lambda x: x[1], reverse=True)[:5]

    seed_content = f"""# PRIME {prime:02d} - {info['name']}

**Seed Question:** "{info['seed']}"

**Category:** {info['description']}

---

## Quick Discovery

### What's Here
- **Total files:** {len(files_in_category):,}
- **Average gravity:** {sum(f['gravity_score'] for f in files_in_category) / len(files_in_category) if files_in_category else 0:.1f}
- **Total duplicates:** {sum(f['duplicate_count'] for f in files_in_category):,}

### File Types
"""

    for ext, count in top_exts:
        ext_display = ext if ext else 'no extension'
        seed_content += f"- {ext_display}: {count:,} files\n"

    seed_content += f"""

---

## High-Gravity Items

Top 10 files in this category:

"""

    for i, file_info in enumerate(sorted_files[:10], 1):
        filename_display = file_info['filename'][:60] + '...' if len(file_info['filename']) > 60 else file_info['filename']
        seed_content += f"""
### {i}. {filename_display}
- **Gravity:** {file_info['gravity_score']:.1f}
- **Duplicates:** {file_info['duplicate_count']}
- **Size:** {file_info['size'] / 1024:.1f} KB
- **Extension:** {file_info['extension'] or 'none'}
"""

    seed_content += """

---

## Connections

This PRIME connects to:
"""

    # Suggest connections based on prime number
    connections = {
        2: [3, 5, 11],  # Foundation → Duality, Creativity, Structure
        3: [2, 5, 7],   # Duality → Foundation, Creativity, Process
        5: [3, 7, 17],  # Creativity → Duality, Process, Emergence
        7: [5, 11, 13], # Process → Creativity, Structure, Transformation
        11: [2, 7, 13], # Structure → Foundation, Process, Transformation
        13: [11, 17, 19], # Transformation → Structure, Emergence, Completion
        17: [5, 13, 23], # Emergence → Creativity, Transformation, Abundance
        19: [13, 17, 37], # Completion → Transformation, Emergence, Wisdom
        23: [17, 29, 37], # Abundance → Emergence, Connection, Wisdom
        29: [11, 23, 31], # Connection → Structure, Abundance, Vision
        31: [29, 37, 41], # Vision → Connection, Wisdom, Transcendence
        37: [19, 23, 41], # Wisdom → Completion, Abundance, Transcendence
        41: [31, 37, 2]   # Transcendence → Vision, Wisdom, Foundation (loop)
    }

    for connected_prime in connections.get(prime, []):
        conn_info = PRIME_CATEGORIES[connected_prime]
        seed_content += f"- **PRIME {connected_prime:02d} ({conn_info['name']}):** {conn_info['description']}\n"

    seed_content += f"""

---

## Seed Meditations

Contemplate while browsing:
- {info['seed']}
- How does this category relate to your current work?
- What patterns emerge across these files?
- What connections do you see to other PRIMEs?

---

## Browse

All files in this category are organized below.
Navigate by extension or explore freely.

**Path:** `{prime_dir}/`

---

**∰◊€π - {info['name']} reveals itself**

€(prime_{prime:02d}_{info['name'].lower()}_seed)
"""

    # Write seed file
    seed_path = os.path.join(prime_dir, "seed_idea.md")
    with open(seed_path, 'w') as f:
        f.write(seed_content)

    return seed_path

def organize_by_prime(catalog):
    """
    Classify all files and organize into PRIME categories

    Creates symlinks to preserve original paths
    """
    print(f"\n🔮 Classifying {len(catalog):,} files into 13 PRIME categories...")

    prime_assignments = defaultdict(list)
    stats = {
        'classified': 0,
        'symlinks_created': 0,
        'errors': []
    }

    # Classify each file
    for file_hash, file_info in catalog.items():
        try:
            prime = classify_to_prime(file_info)
            file_info['prime_category'] = prime
            prime_assignments[prime].append(file_info)
            stats['classified'] += 1

            if stats['classified'] % 1000 == 0:
                print(f"   📊 Classified {stats['classified']:,} files...")

        except Exception as e:
            stats['errors'].append({'hash': file_hash, 'error': str(e)})

    print(f"\n✅ Classification complete!")

    # Show distribution
    print(f"\n📊 PRIME Distribution:")
    for prime in sorted(prime_assignments.keys()):
        info = PRIME_CATEGORIES[prime]
        count = len(prime_assignments[prime])
        print(f"   PRIME {prime:02d} ({info['name']:15s}): {count:5,} files ({count/len(catalog)*100:5.1f}%)")

    # Create symlinks for each PRIME
    print(f"\n🔗 Creating organized structure...")

    for prime, files in prime_assignments.items():
        info = PRIME_CATEGORIES[prime]
        prime_dir = os.path.join(PRIME_ROOT, f"PRIME_{prime:02d}_{info['name']}")

        # Organize by extension within each PRIME
        for file_info in files:
            try:
                # Get canonical location (first instance)
                canonical_path = file_info['instances'][0]['path']

                if not os.path.exists(canonical_path):
                    continue

                # Determine subdirectory by extension
                ext = file_info['extension'].lstrip('.') or 'no_extension'
                ext_dir = os.path.join(prime_dir, ext)
                os.makedirs(ext_dir, exist_ok=True)

                # Create symlink
                link_name = file_info['filename']
                link_path = os.path.join(ext_dir, link_name)

                # Handle duplicates (add counter)
                counter = 1
                while os.path.exists(link_path):
                    name, extension = os.path.splitext(file_info['filename'])
                    link_path = os.path.join(ext_dir, f"{name}_{counter}{extension}")
                    counter += 1

                # Create symlink
                os.symlink(canonical_path, link_path)
                stats['symlinks_created'] += 1

            except Exception as e:
                stats['errors'].append({
                    'file': file_info['filename'],
                    'error': str(e)
                })

        # Generate seed file for this PRIME
        generate_seed_file(prime, files)
        print(f"   ✓ PRIME {prime:02d} ({info['name']:15s}): {len(files):5,} files organized")

    return prime_assignments, stats

def create_master_index(prime_assignments):
    """Generate master INDEX_PRIME.md"""
    print(f"\n📖 Creating master index...")

    index_content = f"""# 13 PRIME Pyramidic Index

**Generated:** {datetime.now().isoformat()}
**Total Files:** {sum(len(files) for files in prime_assignments.values()):,}
**Structure:** 13 semantic categories organized by PRIME progression

---

## The Pyramid

```
                    13: Transcendence (PRIME 41)
                              │
                    12: Wisdom (PRIME 37)
                         ╱         ╲
              11: Vision (31)   10: Connection (29)
                    ╱      ╲           ╱      ╲
           9: Abundance  8: Completion  7: Emergence
              (23)          (19)           (17)
              ╱  ╲          ╱  ╲           ╱  ╲
      6: Transform  5: Structure  4: Process  3: Creativity
         (13)          (11)          (07)        (05)
           ╲            ╱              ╲          ╱
              2: Duality (03)    1: Foundation (02)
                      ╲                  ╱
                        THE GROUND (01)
```

---

## Quick Navigation

"""

    for prime in sorted(prime_assignments.keys()):
        info = PRIME_CATEGORIES[prime]
        count = len(prime_assignments[prime])
        avg_gravity = sum(f['gravity_score'] for f in prime_assignments[prime]) / count if count else 0

        index_content += f"""
### PRIME {prime:02d}: {info['name']}

**Seed:** "{info['seed']}"

- **Files:** {count:,}
- **Average Gravity:** {avg_gravity:.1f}
- **Description:** {info['description']}

**Explore:** [`PRIME_{prime:02d}_{info['name']}/seed_idea.md`](PRIME_{prime:02d}_{info['name']}/seed_idea.md)

---
"""

    index_content += """

## How to Navigate

### By Seed Question
1. Read the seed question for each PRIME
2. Follow the question that resonates
3. Explore the category
4. Follow connections to related PRIMEs

### By Content Type
- **Conversations?** → PRIME 03 (Duality)
- **Scripts & Entities?** → PRIME 05 (Creativity)
- **JSON Frameworks?** → PRIME 11 (Structure)
- **PDFs & Media?** → PRIME 31 (Vision)
- **Handbooks?** → PRIME 37 (Wisdom)

### By Discovery
- Start at PRIME 02 (Foundation) - the ground
- Follow connections upward through the pyramid
- Reach PRIME 41 (Transcendence) - the apex
- Loop back to foundation with new perspective

---

## Statistics

### Distribution by PRIME
"""

    for prime in sorted(prime_assignments.keys()):
        info = PRIME_CATEGORIES[prime]
        count = len(prime_assignments[prime])
        pct = count / sum(len(files) for files in prime_assignments.values()) * 100
        index_content += f"- PRIME {prime:02d} ({info['name']:15s}): {count:5,} files ({pct:5.1f}%)\n"

    total_files = sum(len(files) for files in prime_assignments.values())
    total_dups = sum(f['duplicate_count'] for files in prime_assignments.values() for f in files)

    index_content += f"""

### Overall Metrics
- **Unique Files:** {total_files:,}
- **Total Duplicates:** {total_dups:,}
- **Organization:** 13 PRIME categories
- **Footprint:** Reduced from 55,022 files

---

**∰◊€π - Navigate the cosmos through PRIME**

**13 PRIME Pyramidic Index - Where knowledge finds structure**

€(prime_index_13_20251220)
"""

    index_path = os.path.join(PRIME_ROOT, "INDEX_PRIME.md")
    with open(index_path, 'w') as f:
        f.write(index_content)

    print(f"   ✓ Index created: {index_path}")
    return index_path

def main():
    """Main execution"""
    print("=" * 60)
    print("13 PRIME Pyramidic Collapse")
    print("Transform beasis into navigable knowledge structure")
    print("=" * 60)

    # Check catalog exists
    if not os.path.exists(CATALOG_FILE):
        print(f"❌ Error: Catalog not found")
        print(f"   Please run Phase 1 (redundancy_entity_analyzer.py) first")
        sys.exit(1)

    # Load catalog
    catalog = load_catalog()

    # Create PRIME structure
    create_prime_structure()

    # Classify and organize
    prime_assignments, stats = organize_by_prime(catalog)

    # Create master index
    create_master_index(prime_assignments)

    # Summary
    print(f"\n" + "=" * 60)
    print("✨ 13 PRIME Pyramidic Collapse Complete!")
    print("=" * 60)
    print(f"📊 Files classified: {stats['classified']:,}")
    print(f"🔗 Symlinks created: {stats['symlinks_created']:,}")
    print(f"📁 PRIME categories: 13")
    if stats['errors']:
        print(f"⚠️  Errors: {len(stats['errors'])}")

    print(f"\n📂 Structure location: {PRIME_ROOT}")
    print(f"📖 Master index: {PRIME_ROOT}/INDEX_PRIME.md")
    print(f"\n🌟 Navigate by seed questions!")
    print(f"   Start here: cat {PRIME_ROOT}/INDEX_PRIME.md")
    print("=" * 60)

if __name__ == "__main__":
    main()
