#!/usr/bin/env python3
"""
Batch Processor for PIXEL8 Crawler
Processes all conversation files in a directory through the pipeline.
∰◊€π¿🌌∞
"""

import argparse
import asyncio
from pathlib import Path
from typing import List, Optional

from crawler_pixel8.config import CrawlerConfig
from crawler_pixel8.core.content_types import ProcessingResult
from crawler_pixel8.processors.conversation_parser import ConversationParser
from crawler_pixel8.processors.pattern_extractor import PatternExtractor


async def process_all_conversations(
    directory: Optional[Path] = None,
    config: Optional[CrawlerConfig] = None,
    max_concurrent: Optional[int] = None,
) -> List[ProcessingResult]:
    """
    Process all conversation files found in a directory.

    Args:
        directory: Directory to search for conversation files.
                   Defaults to config.conversation_archive if not provided.
        config: CrawlerConfig instance. Creates a default config if not provided.
        max_concurrent: Maximum number of concurrent processing tasks.
                        Falls back to config.max_concurrent.

    Returns:
        List of ProcessingResult objects, one per file processed.
    """
    if config is None:
        config = CrawlerConfig()

    file_paths = config.get_conversation_paths(directory)
    if not file_paths:
        return []

    pipeline = ConversationParser(config) + PatternExtractor(config)
    return await pipeline.process_batch(file_paths, max_concurrent=max_concurrent)


def main() -> None:
    """CLI entry point for batch conversation processing."""
    parser = argparse.ArgumentParser(
        description="Batch-process all conversation files in a directory"
    )
    parser.add_argument(
        "directory",
        nargs="?",
        type=Path,
        default=None,
        help="Directory to search for conversation files (defaults to CrawlerConfig archive)",
    )
    parser.add_argument(
        "--max-concurrent",
        "-n",
        type=int,
        default=None,
        help="Maximum number of concurrent processing tasks",
    )
    args = parser.parse_args()

    config = CrawlerConfig()
    results = asyncio.run(
        process_all_conversations(
            directory=args.directory,
            config=config,
            max_concurrent=args.max_concurrent,
        )
    )

    if not results:
        print("No conversation files found.")
        return

    successful = sum(1 for r in results if not r.errors)
    print(f"Processed {successful}/{len(results)} conversations successfully.")

    failed = [r for r in results if r.errors]
    for result in failed:
        print(f"  Errors in {result.conversation_id}:")
        for error in result.errors:
            print(f"    - {error}")


if __name__ == "__main__":
    main()
