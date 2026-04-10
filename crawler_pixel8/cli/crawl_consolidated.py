#!/usr/bin/env python3
"""
Batch crawl of _CONSOLIDATED/ directory
Processes all PRIME and CODEX documents through the pipeline.
Results saved to crawler_output/ with a summary report.

Usage:
    python3 crawler_pixel8/cli/crawl_consolidated.py
    python3 crawler_pixel8/cli/crawl_consolidated.py --dir /path/to/_CONSOLIDATED
"""

import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from crawler_pixel8.config import CrawlerConfig
from crawler_pixel8.processors.conversation_parser import ConversationParser
from crawler_pixel8.processors.pattern_extractor import PatternExtractor


async def crawl_consolidated(
    consolidated_dir: Path,
    config: CrawlerConfig
) -> dict:
    """
    Crawl all processable files in consolidated_dir.
    Returns a summary dict with counts, top patterns, topics, entities.
    """
    # Find all processable files recursively
    files = []
    for ext in ["md", "txt", "json"]:
        files.extend(consolidated_dir.rglob(f"*.{ext}"))

    # Skip duplicates_check folder (meta-content, not primary docs)
    files = [
        f for f in files
        if "duplicates_check" not in str(f)
        and "Google AI Studio" not in str(f)
    ]
    files = sorted(files)

    total = len(files)
    print(f"\n∰ PIXEL8 Crawler — _CONSOLIDATED batch")
    print(f"  Found {total} files to process")
    print(f"  Output → {config.summaries_dir}")
    print("-" * 60)

    pipeline = ConversationParser(config) + PatternExtractor(config)

    results = await pipeline.process_batch(files)

    # Build aggregate summary
    all_patterns: dict = {}
    all_topics: dict = {}
    all_entities: list = []
    errors = []
    successful = 0

    for result in results:
        if result.errors:
            errors.extend(result.errors)
            continue
        successful += 1

        # Save individual result
        out_path = config.summaries_dir / f"{result.conversation_id}.json"
        result.aggregate_patterns()
        result.aggregate_entities()
        result.aggregate_topics()
        result.generate_verification_seal()
        result.save(out_path)

        # Accumulate for master summary
        for p in result.key_patterns:
            all_patterns[p] = all_patterns.get(p, 0) + 1
        for t in result.key_topics:
            all_topics[t] = all_topics.get(t, 0) + 1
        all_entities.extend(result.key_entities)

    # Top patterns and topics
    top_patterns = sorted(all_patterns.items(), key=lambda x: x[1], reverse=True)[:20]
    top_topics = sorted(all_topics.items(), key=lambda x: x[1], reverse=True)[:15]

    # Unique entities (deduplicated)
    unique_entities = sorted(set(all_entities))

    summary = {
        "crawled_at": datetime.now().isoformat(),
        "source_dir": str(consolidated_dir),
        "total_files": total,
        "successful": successful,
        "errors_count": len(errors),
        "top_patterns": [{"pattern": p, "count": c} for p, c in top_patterns],
        "top_topics": [{"topic": t, "count": c} for t, c in top_topics],
        "unique_entities_count": len(unique_entities),
        "unique_entities_sample": unique_entities[:50],
        "errors_sample": errors[:10],
    }

    # Save master summary
    summary_path = config.crawler_output / "consolidated_crawl_summary.json"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    return summary


def _print_summary(summary: dict) -> None:
    """Print human-readable summary of crawl results."""
    print()
    print("=" * 60)
    print("∰ Crawl Complete")
    print(f"  Files:    {summary['successful']}/{summary['total_files']} processed")
    print(f"  Errors:   {summary['errors_count']}")
    print(f"  Entities: {summary['unique_entities_count']} unique")
    print()

    print("Top Patterns:")
    for item in summary["top_patterns"][:10]:
        print(f"  {item['count']:3d}×  {item['pattern']}")

    print()
    print("Top Topics:")
    for item in summary["top_topics"][:10]:
        print(f"  {item['count']:3d}×  {item['topic']}")

    print()
    print("Entity Sample (first 20):")
    for e in summary["unique_entities_sample"][:20]:
        print(f"  - {e}")

    print()
    print(f"  Full summary → crawler_output/consolidated_crawl_summary.json")
    print(f"  Individual results → crawler_output/summaries/")
    print("=" * 60)
    print()


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Batch crawl _CONSOLIDATED directory")
    parser.add_argument(
        "--dir", "-d",
        type=Path,
        default=None,
        help="Path to _CONSOLIDATED dir (auto-detects from repo root if not specified)"
    )
    args = parser.parse_args()

    config = CrawlerConfig()

    if args.dir:
        consolidated_dir = args.dir
    else:
        # Auto-detect relative to this script's repo root
        repo_root = Path(__file__).parent.parent.parent
        consolidated_dir = repo_root / "_CONSOLIDATED"

    if not consolidated_dir.exists():
        print(f"Error: {consolidated_dir} not found")
        sys.exit(1)

    summary = asyncio.run(crawl_consolidated(consolidated_dir, config))
    _print_summary(summary)


if __name__ == "__main__":
    main()
