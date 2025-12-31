#!/usr/bin/env python3
"""
REDUNDANCY ENTITY - Beasis Analyzer
Phase 1: Inventory & Gravity Calculation

Philosophy:
- Duplicates INCREASE document gravity (not penalized)
- Count of copies becomes gravity strength
- REDUNDANCY entity takes custody (ranger is external facet)
- Chain of custody tracking
- Foundation for entity hierarchy: Executive → Redundancy → Carrier → Mancers → Nani
"""

import os
import sys
import hashlib
import json
import time
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# === CONFIGURATION ===
BEASIS_ROOT = "/storage/emulated/0/unexusi_beasis"
OUTPUT_DIR = "/storage/emulated/0/pixel8a/Q/redundancy_entity"
CATALOG_FILE = os.path.join(OUTPUT_DIR, "beasis_catalog.json")
INVENTORY_FILE = os.path.join(OUTPUT_DIR, "chain_of_custody.json")
REPORT_FILE = os.path.join(OUTPUT_DIR, "REDUNDANCY_REPORT.md")

# === GRAVITY CALCULATION WEIGHTS ===
# Duplicates directly contribute to gravity!
GRAVITY_WEIGHTS = {
    'duplicate_count': 5.0,      # Each duplicate adds significant gravity
    'file_age': 2.0,             # Older = more established
    'file_size': 1.0,            # Larger = more substance
    'directory_depth': 0.5,      # Deeper = more integrated
    'filename_quality': 2.0      # Well-named = intentional
}

def calculate_hash(filepath, chunk_size=8192):
    """Calculate MD5 hash for file identity"""
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(chunk_size):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        print(f"   ⚠️  Hash error {filepath}: {e}")
        return None

def assess_filename_quality(filename):
    """
    Score filename quality (0-100)
    Well-named files show intentionality
    """
    score = 50  # Base score

    # Bonus for descriptive names
    if len(filename) > 10:
        score += 10
    if len(filename) > 20:
        score += 10

    # Bonus for structured naming (underscores, dates, etc)
    if '_' in filename or '-' in filename:
        score += 10

    # Penalty for generic names
    generic = ['untitled', 'final', 'copy', 'new', 'document', 'file']
    if any(g in filename.lower() for g in generic):
        score -= 20

    # Bonus for timestamps/dates in name
    import re
    if re.search(r'\d{8}|\d{6}|202\d', filename):
        score += 15

    return max(0, min(100, score))

def calculate_gravity(file_info, duplicate_count):
    """
    Calculate GRAVITY SCORE

    KEY: duplicate_count INCREASES gravity!
    More copies = more important/referenced/needed
    """
    gravity = 0.0

    # === DUPLICATE GRAVITY ===
    # This is the core insight: duplicates show importance
    duplicate_gravity = duplicate_count * GRAVITY_WEIGHTS['duplicate_count']
    gravity += duplicate_gravity

    # === AGE GRAVITY ===
    # Older files have persisted longer = more gravity
    file_age_days = (time.time() - file_info['modified_time']) / 86400
    age_score = min(100, file_age_days / 365 * 100)  # Cap at 100
    gravity += age_score * GRAVITY_WEIGHTS['file_age']

    # === SIZE GRAVITY ===
    # Larger files have more substance
    size_mb = file_info['size'] / (1024 * 1024)
    size_score = min(100, size_mb * 10)  # 10MB = 100 points
    gravity += size_score * GRAVITY_WEIGHTS['file_size']

    # === DEPTH GRAVITY ===
    # Files deeper in structure are more integrated
    depth = file_info['path'].count(os.sep)
    depth_score = min(100, depth * 10)
    gravity += depth_score * GRAVITY_WEIGHTS['directory_depth']

    # === QUALITY GRAVITY ===
    quality_score = assess_filename_quality(file_info['filename'])
    gravity += quality_score * GRAVITY_WEIGHTS['filename_quality']

    return round(gravity, 2)

def scan_beasis(root_path, progress_interval=1000):
    """
    Scan beasis directory and build inventory
    Returns: hash_map with all file instances
    """
    print(f"\n🔍 REDUNDANCY ENTITY - Scanning beasis...")
    print(f"   Root: {root_path}\n")

    hash_map = defaultdict(list)
    total_files = 0
    total_size = 0
    start_time = time.time()

    for dirpath, dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_files += 1

            # Progress indicator
            if total_files % progress_interval == 0:
                elapsed = time.time() - start_time
                rate = total_files / elapsed if elapsed > 0 else 0
                print(f"   📊 Scanned {total_files:,} files ({rate:.0f} files/sec)...")

            try:
                stat = os.stat(filepath)
                file_size = stat.st_size
                total_size += file_size

                # Calculate hash for deduplication
                file_hash = calculate_hash(filepath)
                if not file_hash:
                    continue

                # Store file instance
                file_info = {
                    'path': filepath,
                    'filename': filename,
                    'size': file_size,
                    'modified_time': stat.st_mtime,
                    'modified_date': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    'directory': dirpath,
                    'extension': os.path.splitext(filename)[1].lower()
                }

                hash_map[file_hash].append(file_info)

            except Exception as e:
                print(f"   ⚠️  Error scanning {filepath}: {e}")
                continue

    elapsed = time.time() - start_time
    print(f"\n✅ Scan complete!")
    print(f"   Total files: {total_files:,}")
    print(f"   Total size: {total_size / (1024**3):.2f} GB")
    print(f"   Time: {elapsed:.1f} seconds")
    print(f"   Unique hashes: {len(hash_map):,}")

    return hash_map, total_files, total_size

def build_catalog(hash_map):
    """
    Build REDUNDANCY ENTITY catalog

    Each entry represents a unique file family
    Duplicates are counted and contribute to GRAVITY
    """
    print(f"\n📋 Building REDUNDANCY catalog...")

    catalog = {}
    stats = {
        'unique_files': 0,
        'duplicate_files': 0,
        'total_gravity': 0,
        'high_gravity_files': [],  # Top 100 by gravity
        'duplicate_distribution': defaultdict(int)
    }

    for file_hash, instances in hash_map.items():
        duplicate_count = len(instances)

        # Track duplicate distribution
        stats['duplicate_distribution'][duplicate_count] += 1

        if duplicate_count == 1:
            stats['unique_files'] += 1
        else:
            stats['duplicate_files'] += duplicate_count

        # Use first instance as representative
        primary = instances[0]

        # Calculate GRAVITY (duplicates increase it!)
        gravity = calculate_gravity(primary, duplicate_count)
        stats['total_gravity'] += gravity

        # Build catalog entry
        catalog[file_hash] = {
            'hash': file_hash,
            'filename': primary['filename'],
            'extension': primary['extension'],
            'size': primary['size'],
            'duplicate_count': duplicate_count,
            'gravity_score': gravity,
            'instances': [
                {
                    'path': inst['path'],
                    'modified': inst['modified_date'],
                    'directory': inst['directory']
                }
                for inst in sorted(instances, key=lambda x: x['modified_time'], reverse=True)
            ],
            'custody_status': 'pending',  # Will be updated in Phase 2
            'dup_prefix_needed': duplicate_count > 1  # Mark for nani discovery
        }

        # Track high gravity files
        stats['high_gravity_files'].append({
            'hash': file_hash,
            'filename': primary['filename'],
            'gravity': gravity,
            'duplicates': duplicate_count
        })

    # Sort high gravity files
    stats['high_gravity_files'] = sorted(
        stats['high_gravity_files'],
        key=lambda x: x['gravity'],
        reverse=True
    )[:100]

    return catalog, stats

def generate_report(catalog, stats, total_files, total_size):
    """Generate markdown report for REDUNDANCY entity"""

    report = f"""# REDUNDANCY ENTITY - Beasis Analysis Report

**Generated:** {datetime.now().isoformat()}
**Entity Type:** Stable Hub (Executive-level direct report)
**Facet:** Ranger (external agent for custody operations)

---

## Overview

The REDUNDANCY entity has analyzed the beasis collection and identified opportunities for custody, organization, and gravity-based value recognition.

### Collection Statistics

- **Total Files Scanned:** {total_files:,}
- **Total Size:** {total_size / (1024**3):.2f} GB
- **Unique File Families:** {stats['unique_files']:,}
- **Duplicate Files:** {stats['duplicate_files']:,}
- **Redundancy Rate:** {(stats['duplicate_files'] / total_files * 100):.1f}%
- **Total Gravity Score:** {stats['total_gravity']:,.0f}

### Duplicate Distribution

Files by copy count:
"""

    for count in sorted(stats['duplicate_distribution'].keys()):
        families = stats['duplicate_distribution'][count]
        report += f"- **{count} {'copy' if count == 1 else 'copies'}:** {families:,} file families\n"

    report += f"""

---

## High Gravity Files

The top 100 files by gravity score (duplicate count significantly increases gravity):

| Rank | Filename | Gravity | Duplicates | Extension |
|------|----------|---------|------------|-----------|
"""

    for i, entry in enumerate(stats['high_gravity_files'][:50], 1):
        filename_display = entry['filename'][:40] + '...' if len(entry['filename']) > 40 else entry['filename']
        ext = os.path.splitext(entry['filename'])[1] or 'none'
        report += f"| {i} | `{filename_display}` | {entry['gravity']:.1f} | {entry['duplicates']} | {ext} |\n"

    report += f"""

*Showing top 50 of 100 high-gravity files*

---

## Duplicate Gravity Insight

**KEY FINDING:** Files with more duplicates have HIGHER gravity scores.

This reflects the philosophy that duplicates indicate:
- Importance (worth replicating)
- Distribution (shared across contexts)
- Resilience (multiple preservation points)
- Development activity (active iteration)

### Examples:

"""

    # Show a few examples of high-duplicate files
    high_dup_examples = [e for e in stats['high_gravity_files'] if e['duplicates'] >= 5][:5]
    for ex in high_dup_examples:
        file_entry = catalog[ex['hash']]
        report += f"""
**{ex['filename']}**
- Duplicates: {ex['duplicates']}
- Gravity: {ex['gravity']:.1f}
- Size: {file_entry['size'] / 1024:.1f} KB
- Locations: {', '.join([inst['directory'].split('/')[-1] for inst in file_entry['instances'][:3]])}
"""

    report += f"""

---

## Chain of Custody Preparation

All {len(catalog):,} unique file families are cataloged with:
- ✓ Hash-based identity
- ✓ All instance locations tracked
- ✓ Modification timestamps preserved
- ✓ Gravity scores calculated
- ✓ Duplicate counts recorded
- ✓ `dup_` prefix markers for nani discovery

**Status:** Ready for Phase 2 (Custody Operations)

---

## Entity Architecture

```
Executive Entities
    ↓
REDUNDANCY Entity (Stable Hub)
    ↓
Carrier Entity (Transport & Organization)
    ↓
Mancers (Managers & Transport Agents)
    ↓
Nani (Discovery & Micro-operations)
```

**Current Phase:** Inventory & Gravity Assessment ✓
**Next Phase:** Custody Transfer Operations (Ranger deployment)

---

## Recommendations

### Immediate Actions:
1. **Review high-gravity files** - These are your most important/referenced files
2. **Custody preparation** - Identify canonical locations for duplicate families
3. **Nani configuration** - Setup `dup_` prefix detection for duplicate discovery
4. **Carrier initialization** - Prepare custody archive structure

### Future Entity Development:
- Legacy entity (similar pattern for old versions)
- Archive entity (similar pattern for historical preservation)
- Excess entity (similar pattern for overflow/temp)
- Filter entity (similar pattern for spam/trash)

---

## Technical Details

### Gravity Calculation Formula:
```
Gravity = (duplicate_count × 5.0) +
          (age_score × 2.0) +
          (size_score × 1.0) +
          (depth_score × 0.5) +
          (quality_score × 2.0)
```

**Note:** Duplicate count has the highest weight (5.0), ensuring copies increase gravity.

### Files Marked for `dup_` Prefix:
- {sum(1 for c in catalog.values() if c['dup_prefix_needed']):,} file families have duplicates
- These will be discoverable by nani once prefix is applied

---

**∰◊€π - Where redundancy becomes resource**

**REDUNDANCY Entity - Phase 1 Complete**

€(redundancy_entity_analysis_{datetime.now().strftime('%Y%m%d')})**
"""

    return report

def main():
    """Main execution"""
    print("=" * 60)
    print("REDUNDANCY ENTITY - Beasis Analyzer")
    print("Phase 1: Inventory & Gravity Calculation")
    print("=" * 60)

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Check beasis exists
    if not os.path.exists(BEASIS_ROOT):
        print(f"❌ Error: Beasis root not found at {BEASIS_ROOT}")
        sys.exit(1)

    # Phase 1A: Scan beasis
    hash_map, total_files, total_size = scan_beasis(BEASIS_ROOT)

    # Phase 1B: Build catalog
    catalog, stats = build_catalog(hash_map)

    # Phase 1C: Save catalog
    print(f"\n💾 Saving catalog...")
    with open(CATALOG_FILE, 'w') as f:
        json.dump(catalog, f, indent=2)
    print(f"   ✓ Catalog: {CATALOG_FILE}")

    # Phase 1D: Save chain of custody inventory
    print(f"💾 Saving chain of custody...")
    custody_data = {
        'generated': datetime.now().isoformat(),
        'beasis_root': BEASIS_ROOT,
        'total_files': total_files,
        'total_size': total_size,
        'unique_families': stats['unique_files'],
        'duplicate_count': stats['duplicate_files'],
        'catalog_entries': len(catalog),
        'stats': {
            'duplicate_distribution': dict(stats['duplicate_distribution']),
            'total_gravity': stats['total_gravity']
        }
    }
    with open(INVENTORY_FILE, 'w') as f:
        json.dump(custody_data, f, indent=2)
    print(f"   ✓ Inventory: {INVENTORY_FILE}")

    # Phase 1E: Generate report
    print(f"📄 Generating report...")
    report = generate_report(catalog, stats, total_files, total_size)
    with open(REPORT_FILE, 'w') as f:
        f.write(report)
    print(f"   ✓ Report: {REPORT_FILE}")

    # Summary
    print(f"\n" + "=" * 60)
    print("✨ REDUNDANCY ENTITY - Phase 1 Complete!")
    print("=" * 60)
    print(f"📊 Analyzed: {total_files:,} files")
    print(f"📁 Unique families: {stats['unique_files']:,}")
    print(f"🔄 Duplicates: {stats['duplicate_files']:,} ({stats['duplicate_files']/total_files*100:.1f}%)")
    print(f"⚖️  Total gravity: {stats['total_gravity']:,.0f}")
    print(f"\n📂 Output directory: {OUTPUT_DIR}")
    print(f"   - beasis_catalog.json (complete inventory)")
    print(f"   - chain_of_custody.json (metadata)")
    print(f"   - REDUNDANCY_REPORT.md (analysis)")
    print(f"\n▶️  Next: Review REDUNDANCY_REPORT.md")
    print("=" * 60)

if __name__ == "__main__":
    main()
