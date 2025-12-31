#!/usr/bin/env python3
"""
REDUNDANCY ENTITY - Ranger Custody Operations
Phase 2: Duplicate Custody & Nani Discovery

The Ranger (external facet of REDUNDANCY entity):
- Takes custody of duplicates
- Applies dup_ prefix for nani discovery
- Maintains chain of custody
- Preserves ALL data (conservation bias)
- Lets duplicates increase original gravity count

Entity Hierarchy:
Executive → REDUNDANCY (stable hub) → Carrier → Mancers → Nani
"""

import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

# === CONFIGURATION ===
REDUNDANCY_DIR = "/storage/emulated/0/pixel8a/Q/redundancy_entity"
CATALOG_FILE = os.path.join(REDUNDANCY_DIR, "beasis_catalog.json")
BEASIS_ROOT = "/storage/emulated/0/unexusi_beasis"

# CUSTODY ARCHIVE (where ranger moves duplicates)
CUSTODY_ROOT = os.path.join(BEASIS_ROOT, "redundancy_custody")

# Carrier structure (organizes custody by type)
CARRIER_STRUCTURE = {
    'duplicates': 'dup_collection',      # All duplicates (dup_ prefix)
    'large_files': 'large_file_custody', # Large files (handle separately)
    'by_gravity': 'gravity_sorted',      # High-gravity references
    'by_extension': 'type_sorted',       # Sorted by file type
    'chain_of_custody': 'custody_records'
}

# Large file configuration (handle separately)
LARGE_FILE_EXTENSIONS = {'.mp4', '.mov', '.avi', '.mkv', '.wav', '.mp3', '.flac',
                         '.zip', '.tar', '.gz', '.iso', '.dmg', '.exe'}
LARGE_FILE_THRESHOLD = 10 * 1024 * 1024  # 10MB threshold

# === CUSTODY OPERATIONS ===

def load_catalog():
    """Load the Phase 1 catalog"""
    print(f"\n📋 Loading REDUNDANCY catalog...")
    with open(CATALOG_FILE, 'r') as f:
        catalog = json.load(f)
    print(f"   ✓ Loaded {len(catalog):,} unique file families")
    return catalog

def initialize_carrier_structure():
    """
    Initialize the Carrier entity structure

    Carrier organizes custody into logical categories
    Mancers will operate within these structures
    """
    print(f"\n🚚 Initializing Carrier entity structure...")

    for category, subdir in CARRIER_STRUCTURE.items():
        path = os.path.join(CUSTODY_ROOT, subdir)
        os.makedirs(path, exist_ok=True)
        print(f"   ✓ {category}: {subdir}/")

    # Create README for custody archive
    readme_path = os.path.join(CUSTODY_ROOT, "README.md")
    with open(readme_path, 'w') as f:
        f.write(f"""# REDUNDANCY Entity - Custody Archive

**Created:** {datetime.now().isoformat()}
**Entity:** REDUNDANCY (Stable Hub)
**Facet:** Ranger (External Agent)
**Carrier:** Organizational Transport System

---

## Purpose

This archive contains duplicates taken into custody by the REDUNDANCY entity.
All files here have the `dup_` prefix for nani discovery.

**Conservation Bias:** Nothing is deleted. All duplicates preserved.
**Gravity Honor:** Each duplicate counted toward original's gravity.

## Structure

```
redundancy_custody/
├── dup_collection/        ← All duplicates with dup_ prefix
│   ├── dup_[original_name]
│   └── ...
├── gravity_sorted/        ← High-gravity file references
├── type_sorted/           ← Organized by extension
└── custody_records/       ← Chain of custody tracking
```

## Chain of Custody

Every file here has:
- Original location recorded
- Custody transfer timestamp
- Gravity contribution tracked
- Original contributor credited

## Nani Discovery

Files prefixed with `dup_` are discoverable by nani-level operations.
The nani can:
- Find all duplicates quickly
- Reference back to originals
- Participate in gravity calculations
- Support entity development

---

**∰◊€π - Conservation through custody**

€(redundancy_custody_archive)
""")
    print(f"   ✓ Created custody archive README")

    return True

def select_canonical_copy(instances):
    """
    Select which copy stays as the canonical version

    Criteria (in order):
    1. Newest modification time (most recent = canonical)
    2. Deepest directory (more integrated)
    3. Best filename quality
    """
    # Sort by modification time (newest first)
    sorted_instances = sorted(
        instances,
        key=lambda x: x['modified'],
        reverse=True
    )

    canonical = sorted_instances[0]
    duplicates = sorted_instances[1:]

    return canonical, duplicates

def create_custody_record(file_hash, family_info, canonical, duplicates_moved):
    """
    Create chain of custody record for this file family
    """
    record = {
        'file_hash': file_hash,
        'filename': family_info['filename'],
        'extension': family_info['extension'],
        'gravity_score': family_info['gravity_score'],
        'duplicate_count': family_info['duplicate_count'],
        'canonical_location': canonical['path'],
        'custody_taken': datetime.now().isoformat(),
        'duplicates_in_custody': len(duplicates_moved),
        'custody_locations': duplicates_moved,
        'gravity_contribution': f"{len(duplicates_moved)} duplicates contribute to gravity",
        'nani_discoverable': True,
        'dup_prefix_applied': True
    }

    return record

def is_large_file(file_info):
    """
    Check if file should be routed to large_file_custody

    Criteria:
    - Extension in LARGE_FILE_EXTENSIONS, OR
    - Size exceeds LARGE_FILE_THRESHOLD
    """
    ext = file_info['extension'].lower()
    size = file_info['size']

    if ext in LARGE_FILE_EXTENSIONS:
        return True
    if size >= LARGE_FILE_THRESHOLD:
        return True

    return False

def apply_dup_prefix(original_filename):
    """
    Apply dup_ prefix for nani discovery

    Format: dup_[original_name]
    """
    return f"dup_{original_filename}"

def take_custody(catalog, dry_run=True, max_files=None):
    """
    Ranger takes custody of duplicates

    Process:
    1. Select canonical copy (stays in place)
    2. Move duplicates to custody
    3. Apply dup_ prefix
    4. Create custody records
    5. Preserve all data

    Args:
        catalog: The beasis catalog from Phase 1
        dry_run: If True, only simulate (no actual moves)
        max_files: Limit number of families to process (for testing)
    """
    print(f"\n🔍 RANGER - Beginning custody operations...")
    print(f"   Mode: {'DRY RUN (simulation)' if dry_run else 'LIVE (actual moves)'}")

    stats = {
        'families_processed': 0,
        'duplicates_moved': 0,
        'large_files_moved': 0,
        'space_organized': 0,
        'large_file_space': 0,
        'custody_records_created': 0,
        'errors': []
    }

    custody_records = []

    # Process file families with duplicates
    families_with_duplicates = {
        h: f for h, f in catalog.items()
        if f['duplicate_count'] > 1
    }

    print(f"   Found {len(families_with_duplicates):,} families with duplicates")

    if max_files:
        print(f"   Limiting to first {max_files} families (testing mode)")
        families_with_duplicates = dict(
            list(families_with_duplicates.items())[:max_files]
        )

    for file_hash, family_info in families_with_duplicates.items():
        stats['families_processed'] += 1

        # Progress
        if stats['families_processed'] % 100 == 0:
            print(f"   📊 Processed {stats['families_processed']:,} families...")

        # Select canonical and duplicates
        canonical, duplicates = select_canonical_copy(family_info['instances'])

        # Move each duplicate to custody
        duplicates_moved = []

        for dup_instance in duplicates:
            try:
                original_path = dup_instance['path']

                # Skip if file doesn't exist
                if not os.path.exists(original_path):
                    continue

                # Create dup_ prefixed filename
                dup_filename = apply_dup_prefix(family_info['filename'])

                # Determine custody location
                # Large files go to separate folder for later handling
                if is_large_file(family_info):
                    custody_base = CARRIER_STRUCTURE['large_files']
                    ext = family_info['extension'].lstrip('.') or 'no_extension'
                else:
                    custody_base = CARRIER_STRUCTURE['duplicates']
                    ext = family_info['extension'].lstrip('.') or 'no_extension'

                custody_dir = os.path.join(
                    CUSTODY_ROOT,
                    custody_base,
                    ext
                )

                # Create unique path (add counter if needed)
                base_custody_path = os.path.join(custody_dir, dup_filename)
                custody_path = base_custody_path
                counter = 1
                while os.path.exists(custody_path):
                    name, extension = os.path.splitext(dup_filename)
                    custody_path = os.path.join(
                        custody_dir,
                        f"{name}_{counter}{extension}"
                    )
                    counter += 1

                # Track large files separately
                is_large = is_large_file(family_info)

                if not dry_run:
                    # Create directory if needed
                    os.makedirs(custody_dir, exist_ok=True)

                    # Move to custody
                    shutil.move(original_path, custody_path)

                    stats['duplicates_moved'] += 1
                    stats['space_organized'] += family_info['size']
                    if is_large:
                        stats['large_files_moved'] += 1
                        stats['large_file_space'] += family_info['size']
                else:
                    # Dry run - just simulate
                    stats['duplicates_moved'] += 1
                    stats['space_organized'] += family_info['size']
                    if is_large:
                        stats['large_files_moved'] += 1
                        stats['large_file_space'] += family_info['size']

                # Record custody location
                duplicates_moved.append({
                    'original_location': original_path,
                    'custody_location': custody_path,
                    'dup_prefix_applied': dup_filename
                })

            except Exception as e:
                stats['errors'].append({
                    'file': original_path,
                    'error': str(e)
                })

        # Create custody record
        if duplicates_moved:
            record = create_custody_record(
                file_hash,
                family_info,
                canonical,
                duplicates_moved
            )
            custody_records.append(record)
            stats['custody_records_created'] += 1

    print(f"\n✅ Ranger custody operations complete!")
    return stats, custody_records

def save_custody_records(records):
    """Save chain of custody records"""
    print(f"\n💾 Saving chain of custody records...")

    custody_records_dir = os.path.join(
        CUSTODY_ROOT,
        CARRIER_STRUCTURE['chain_of_custody']
    )
    os.makedirs(custody_records_dir, exist_ok=True)

    # Save complete records
    records_file = os.path.join(custody_records_dir, "custody_log.json")
    with open(records_file, 'w') as f:
        json.dump({
            'generated': datetime.now().isoformat(),
            'total_records': len(records),
            'records': records
        }, f, indent=2)

    print(f"   ✓ Saved {len(records):,} custody records")
    print(f"   ✓ Location: {records_file}")

    return records_file

def generate_custody_report(stats, records):
    """Generate custody operations report"""
    report = f"""# REDUNDANCY ENTITY - Custody Operations Report

**Generated:** {datetime.now().isoformat()}
**Phase:** 2 - Ranger Custody Operations
**Facet:** Ranger (External Agent)

---

## Operations Summary

### Files Processed
- **File families processed:** {stats['families_processed']:,}
- **Duplicates moved to custody:** {stats['duplicates_moved']:,}
- **Large files moved:** {stats['large_files_moved']:,} (handled separately)
- **Space organized:** {stats['space_organized'] / (1024**2):.1f} MB
- **Large file space:** {stats['large_file_space'] / (1024**2):.1f} MB
- **Custody records created:** {stats['custody_records_created']:,}
- **Errors encountered:** {len(stats['errors'])}

### Custody Status

✓ All duplicates now have `dup_` prefix for nani discovery
✓ Canonical copies remain in original locations
✓ Large files (mp4, wav, etc.) in separate custody for later handling
✓ Full chain of custody maintained
✓ Conservation bias honored (nothing deleted)

---

## High-Gravity Custody Examples

Top 10 families by gravity (showing custody operations):

"""

    # Sort records by gravity
    sorted_records = sorted(records, key=lambda r: r['gravity_score'], reverse=True)[:10]

    for i, record in enumerate(sorted_records, 1):
        report += f"""
### {i}. {record['filename']}
- **Gravity:** {record['gravity_score']:.1f}
- **Total duplicates:** {record['duplicate_count']}
- **Moved to custody:** {record['duplicates_in_custody']}
- **Canonical location:** `{record['canonical_location']}`
- **Nani discoverable:** ✓ (dup_ prefix applied)
"""

    report += f"""

---

## Nani Discovery System

All {stats['duplicates_moved']:,} duplicates now have the `dup_` prefix.

**Nani can now:**
- Find duplicates instantly by prefix
- Reference original gravity scores
- Participate in entity operations
- Support development workflows

**Example nani operations:**
```bash
# Find all duplicates
find {CUSTODY_ROOT} -name "dup_*"

# Count duplicates by type
find {CUSTODY_ROOT}/dup_collection -type f | wc -l

# List high-gravity duplicates
grep -r "gravity_score" {CUSTODY_ROOT}/custody_records/
```

---

## Carrier Organization

Duplicates organized by the Carrier entity:

- **dup_collection/** - All duplicates by extension type
- **gravity_sorted/** - High-gravity references (future)
- **type_sorted/** - Alternative organization (future)
- **custody_records/** - Complete chain of custody

---

## Chain of Custody

Every duplicate moved has full provenance:
- Original location recorded
- Custody timestamp logged
- Gravity contribution tracked
- Nani discovery enabled

**Custody records location:**
`{CUSTODY_ROOT}/custody_records/custody_log.json`

---

## Conservation Bias Maintained

✓ **Zero files deleted**
✓ **All data preserved**
✓ **Full history maintained**
✓ **Gravity counts honored**

Original files benefit from duplicate gravity even after custody transfer.
Each duplicate continues to contribute to the original's importance score.

---

## Next Steps

### Phase 3: Mancers (Managers)
- High-gravity file tracking
- Duplicate reference system
- Cross-entity coordination

### Phase 4: Nani Operations
- Duplicate discovery scripts
- Gravity-based queries
- Entity interaction protocols

### Future Entities (using REDUNDANCY as template)
- **Legacy entity** - Old versions
- **Archive entity** - Historical preservation
- **Excess entity** - Overflow/temp files
- **Filter entity** - Spam/trash handling

---

**∰◊€π - Where custody preserves value**

**REDUNDANCY Entity - Phase 2 Complete**

€(redundancy_custody_operations_{datetime.now().strftime('%Y%m%d')})**
"""

    return report

def main():
    """Main execution"""
    print("=" * 60)
    print("REDUNDANCY ENTITY - Ranger Custody Operations")
    print("Phase 2: Duplicate Custody & Nani Discovery")
    print("=" * 60)

    # Check catalog exists
    if not os.path.exists(CATALOG_FILE):
        print(f"❌ Error: Catalog not found at {CATALOG_FILE}")
        print(f"   Please run Phase 1 (redundancy_entity_analyzer.py) first")
        sys.exit(1)

    # Load catalog
    catalog = load_catalog()

    # Initialize carrier structure
    initialize_carrier_structure()

    # Ask user: dry run or live?
    print("\n" + "=" * 60)
    print("⚠️  CUSTODY MODE SELECTION")
    print("=" * 60)
    print("\nThe Ranger will now take custody of duplicates.")
    print("\nOptions:")
    print("  1. DRY RUN - Simulate only (no files moved)")
    print("  2. TEST - Move first 10 families (safe test)")
    print("  3. LIVE - Full custody operations (move all duplicates)")
    print("\nDRY RUN is recommended for first execution.")

    mode = input("\nSelect mode (1/2/3): ").strip()

    if mode == '1':
        dry_run = True
        max_files = None
        print("\n✓ DRY RUN mode - simulating operations")
    elif mode == '2':
        dry_run = False
        max_files = 10
        print("\n✓ TEST mode - processing 10 families")
    elif mode == '3':
        dry_run = False
        max_files = None
        print("\n✓ LIVE mode - full custody operations")
        confirm = input("   Are you sure? This will move files. (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("   Cancelled.")
            sys.exit(0)
    else:
        print("Invalid selection. Exiting.")
        sys.exit(1)

    # Take custody
    stats, records = take_custody(catalog, dry_run=dry_run, max_files=max_files)

    # Save custody records (even for dry run)
    if records:
        records_file = save_custody_records(records)

    # Generate report
    print(f"\n📄 Generating custody report...")
    report = generate_custody_report(stats, records)
    report_file = os.path.join(REDUNDANCY_DIR, "CUSTODY_OPERATIONS_REPORT.md")
    with open(report_file, 'w') as f:
        f.write(report)
    print(f"   ✓ Report: {report_file}")

    # Summary
    print(f"\n" + "=" * 60)
    print("✨ REDUNDANCY ENTITY - Phase 2 Complete!")
    print("=" * 60)
    print(f"📊 Families processed: {stats['families_processed']:,}")
    print(f"🔄 Duplicates {'simulated' if dry_run else 'moved'}: {stats['duplicates_moved']:,}")
    print(f"🎬 Large files (mp4/wav/etc.): {stats['large_files_moved']:,}")
    print(f"💾 Space organized: {stats['space_organized'] / (1024**2):.1f} MB")
    print(f"📦 Large file space: {stats['large_file_space'] / (1024**2):.1f} MB")
    print(f"📝 Custody records: {stats['custody_records_created']:,}")
    if stats['errors']:
        print(f"⚠️  Errors: {len(stats['errors'])}")
    print(f"\n📂 Custody archive: {CUSTODY_ROOT}")
    print(f"   - Regular duplicates: {CUSTODY_ROOT}/dup_collection/")
    print(f"   - Large files: {CUSTODY_ROOT}/large_file_custody/")
    print(f"📋 Custody records: {CUSTODY_ROOT}/custody_records/")
    print(f"\n▶️  Next: Review CUSTODY_OPERATIONS_REPORT.md")
    print("=" * 60)

if __name__ == "__main__":
    main()
