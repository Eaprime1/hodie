#!/usr/bin/env python3
"""
Test script for PIXEL8 Crawler
Quick test with a single conversation file
"""

import asyncio
from pathlib import Path
import sys
import json

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from crawler_pixel8.config import CrawlerConfig
from crawler_pixel8.processors.conversation_parser import ConversationParser
from crawler_pixel8.processors.pattern_extractor import PatternExtractor


async def test_crawler(test_file: Path = None):
    """
    Test crawler with a single file

    Args:
        test_file: Path to test conversation file (auto-detects if not provided)
    """
    print("🔮 PIXEL8 Crawler Test")
    print("=" * 60)

    # Initialize config
    config = CrawlerConfig()

    # Find test file if not provided
    if not test_file:
        conversations = config.get_conversation_paths()
        if not conversations:
            print("❌ No conversation files found")
            print(f"   Looked in: {config.conversation_archive}")
            return

        test_file = conversations[0]
        print(f"✓ Auto-selected test file: {test_file.name}")
    else:
        print(f"✓ Using provided test file: {test_file.name}")

    print()

    # Create processing pipeline
    print("🔧 Setting up processing pipeline...")
    parser = ConversationParser(config)
    extractor = PatternExtractor(config)

    # Chain processors: parse → extract patterns
    pipeline = parser + extractor

    print(f"✓ Pipeline: ConversationParser → PatternExtractor")
    print()

    # Process file
    print(f"📄 Processing: {test_file}")
    print("-" * 60)

    result = await pipeline.process_file(test_file)

    # Display results
    print()
    print("📊 Results:")
    print(f"   Parts processed: {result.parts_count}")
    print(f"   Processing time: {result.processing_time:.2f}s")
    print(f"   Errors: {len(result.errors)}")

    if result.errors:
        print("\n❌ Errors:")
        for error in result.errors:
            print(f"   - {error}")

    print()
    print(f"🎯 Extracted Patterns ({len(result.key_patterns)}):")
    for pattern in result.key_patterns[:10]:  # Top 10
        print(f"   - {pattern}")

    print()
    print(f"🏷️  Extracted Topics ({len(result.key_topics)}):")
    for topic in result.key_topics:
        print(f"   - {topic}")

    print()
    print(f"🔗 Extracted Entities ({len(result.key_entities)}):")
    for entity in result.key_entities[:10]:  # Top 10
        print(f"   - {entity}")

    # Save results
    output_path = config.summaries_dir / f"{test_file.stem}_test_result.json"
    result.save(output_path)
    print()
    print(f"💾 Results saved to: {output_path}")

    # Show sample parts
    print()
    print(f"📝 Sample Parts (first 3):")
    print("-" * 60)
    for i, part in enumerate(result.parts[:3]):
        print(f"\nPart {i+1} (Turn {part.turn_number}):")
        print(f"  Role: {part.role}")
        print(f"  Text (first 200 chars): {part.text[:200]}...")
        if part.patterns:
            print(f"  Patterns: {', '.join(part.patterns[:5])}")
        if part.topics:
            print(f"  Topics: {', '.join(part.topics)}")

    print()
    print("=" * 60)
    print("✅ Test complete!")
    print()


def main():
    """Main entry point for CLI"""
    import argparse

    parser = argparse.ArgumentParser(description="Test PIXEL8 Crawler")
    parser.add_argument(
        "file",
        nargs="?",
        type=Path,
        help="Path to conversation file (auto-selects if not provided)"
    )

    args = parser.parse_args()

    # Run test
    asyncio.run(test_crawler(args.file))


if __name__ == "__main__":
    main()
