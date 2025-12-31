#!/usr/bin/env python3
"""
13 PRIME Search - Category-Based File Discovery

Quickly find files by PRIME category without scanning 55k files!
"""

import os
import sys
import json
from pathlib import Path

# === CONFIGURATION ===
REDUNDANCY_DIR = "/storage/emulated/0/pixel8a/Q/redundancy_entity"
CATALOG_FILE = os.path.join(REDUNDANCY_DIR, "beasis_catalog.json")

PRIME_NAMES = {
    2: 'Foundation', 3: 'Duality', 5: 'Creativity', 7: 'Process',
    11: 'Structure', 13: 'Transformation', 17: 'Emergence', 19: 'Completion',
    23: 'Abundance', 29: 'Connection', 31: 'Vision', 37: 'Wisdom', 41: 'Transcendence'
}

def load_catalog_with_primes():
    """Load catalog with PRIME classifications"""
    print(f"📋 Loading catalog...", end='')
    with open(CATALOG_FILE, 'r') as f:
        catalog = json.load(f)

    # Re-classify (quick, already done in prime_collapse.py)
    from prime_collapse import classify_to_prime
    for file_hash, file_info in catalog.items():
        if 'prime_category' not in file_info:
            file_info['prime_category'] = classify_to_prime(file_info)

    print(f" ✓ {len(catalog):,} files")
    return catalog

def search_by_prime(catalog, prime_number):
    """Find all files in a PRIME category"""
    results = [
        file_info for file_info in catalog.values()
        if file_info.get('prime_category') == prime_number
    ]
    return sorted(results, key=lambda x: x['gravity_score'], reverse=True)

def search_by_keyword(catalog, keyword, prime_filter=None):
    """Search filenames, optionally within a PRIME category"""
    keyword_lower = keyword.lower()
    results = []

    for file_info in catalog.values():
        if prime_filter and file_info.get('prime_category') != prime_filter:
            continue

        if keyword_lower in file_info['filename'].lower():
            results.append(file_info)

    return sorted(results, key=lambda x: x['gravity_score'], reverse=True)

def display_results(results, limit=20):
    """Display search results"""
    print(f"\n📊 Found {len(results):,} files")

    if not results:
        return

    print(f"   Showing top {min(limit, len(results))}:\n")

    for i, file_info in enumerate(results[:limit], 1):
        prime = file_info.get('prime_category', '?')
        prime_name = PRIME_NAMES.get(prime, 'Unknown')

        filename_display = file_info['filename'][:60] + '...' if len(file_info['filename']) > 60 else file_info['filename']

        print(f"{i:3d}. {filename_display}")
        print(f"     PRIME {prime:02d} ({prime_name}) | Gravity: {file_info['gravity_score']:.1f} | Dups: {file_info['duplicate_count']}")
        print(f"     Path: {file_info['instances'][0]['path']}")
        print()

def main():
    """Interactive search"""
    if len(sys.argv) < 2:
        print("""
13 PRIME Search - Find files by category

Usage:
  python prime_search.py <command> [args]

Commands:
  prime <number>              - List files in PRIME category
  find <keyword>              - Find files by name
  find <keyword> <prime>      - Find files in PRIME category
  stats                       - Show PRIME distribution

Examples:
  python prime_search.py prime 5          # All creative files
  python prime_search.py find entity      # All files with "entity"
  python prime_search.py find entity 5    # Entities in Creativity
  python prime_search.py stats            # Show distribution
        """)
        sys.exit(0)

    command = sys.argv[1].lower()

    # Load catalog
    catalog = load_catalog_with_primes()

    if command == 'prime':
        if len(sys.argv) < 3:
            print("❌ Usage: prime_search.py prime <number>")
            sys.exit(1)

        prime_num = int(sys.argv[2])
        prime_name = PRIME_NAMES.get(prime_num, 'Unknown')

        print(f"\n🔍 PRIME {prime_num:02d}: {prime_name}")
        results = search_by_prime(catalog, prime_num)
        display_results(results, limit=50)

    elif command == 'find':
        if len(sys.argv) < 3:
            print("❌ Usage: prime_search.py find <keyword> [prime]")
            sys.exit(1)

        keyword = sys.argv[2]
        prime_filter = int(sys.argv[3]) if len(sys.argv) > 3 else None

        if prime_filter:
            prime_name = PRIME_NAMES.get(prime_filter, 'Unknown')
            print(f"\n🔍 Searching for '{keyword}' in PRIME {prime_filter:02d} ({prime_name})")
        else:
            print(f"\n🔍 Searching for '{keyword}' across all PRIMEs")

        results = search_by_keyword(catalog, keyword, prime_filter)
        display_results(results, limit=30)

    elif command == 'stats':
        print(f"\n📊 13 PRIME Distribution\n")

        from collections import defaultdict
        prime_counts = defaultdict(int)

        for file_info in catalog.values():
            prime = file_info.get('prime_category', 41)
            prime_counts[prime] += 1

        total = len(catalog)

        for prime in sorted(prime_counts.keys()):
            name = PRIME_NAMES.get(prime, 'Unknown')
            count = prime_counts[prime]
            pct = count / total * 100

            bar_length = int(pct / 2)  # Max 50 chars
            bar = '█' * bar_length

            print(f"PRIME {prime:02d} {name:15s} [{bar:<50s}] {count:5,} ({pct:5.1f}%)")

    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
