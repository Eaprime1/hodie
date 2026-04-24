"""
Hodie CLI — User-facing entry point for the PIXEL8 Crawler
∰◊€π¿🌌∞ — one stage at a time, sequential clarity, no overload
"""

import asyncio
import argparse
import os
import sys
from pathlib import Path

from crawler_pixel8.config import CrawlerConfig, KNOWN_LOCATIONS
from crawler_pixel8.processors.conversation_parser import ConversationParser
from crawler_pixel8.processors.pattern_extractor import PatternExtractor
from crawler_pixel8.processors.one_hertz import PLEXUS_STAGES

_STAGE_COUNT = len(PLEXUS_STAGES)  # 1-based max for --stage


def _build_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser."""
    stage_names = ", ".join(
        f"{i + 1}={name}" for i, name in enumerate(PLEXUS_STAGES)
    )
    parser = argparse.ArgumentParser(
        prog="hodie",
        description="Hodie PIXEL8 Crawler — staged conversation processor (∰◊€π¿🌌∞)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  hodie --file conversation.json\n"
            "  hodie --location mulberry --file chat.json --output ./results\n"
            f"  hodie --location codespaces --file data.md --stage 2  # 2=duplex\n"
        ),
    )
    parser.add_argument(
        "--location",
        choices=list(KNOWN_LOCATIONS),
        default=None,
        metavar="LOCATION",
        help=(
            "Device location: mulberry (laptop HQ), pixel8a (mobile), "
            "codespaces (cloud). Sets HODIE_LOCATION env var and loads "
            ".locations/{LOCATION}/config.sh paths. "
            f"Choices: {', '.join(KNOWN_LOCATIONS)}"
        ),
    )
    parser.add_argument(
        "--file",
        "-f",
        type=Path,
        metavar="FILE",
        help="Input conversation file to process (JSON, Markdown, or plain text).",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        metavar="DIR",
        help=(
            "Output directory for processing results. "
            "Defaults to crawler_output/ relative to the resolved hodie directory."
        ),
    )
    parser.add_argument(
        "--stage",
        "-s",
        type=int,
        default=1,
        metavar="STAGE",
        help=(
            f"Plexus stage number (1–{_STAGE_COUNT}): {stage_names}. "
            "Labels the processing context; use with `one_hertz` for full "
            "One Hertz cycle processing. Default: 1 (simplex)."
        ),
    )
    return parser


async def _run(args: argparse.Namespace) -> int:
    """
    Async entry point — builds config, runs the pipeline, saves results.

    Returns:
        Exit code (0 = success, 1 = error).
    """
    # Apply location to env so CrawlerConfig picks it up
    if args.location:
        os.environ["HODIE_LOCATION"] = args.location

    config = CrawlerConfig()

    # Validate and resolve plexus stage
    if not 1 <= args.stage <= _STAGE_COUNT:
        print(
            f"Error: --stage must be between 1 and {_STAGE_COUNT} "
            f"(got {args.stage}). "
            f"Stages: {', '.join(f'{i+1}={s}' for i, s in enumerate(PLEXUS_STAGES))}"
        )
        return 1
    stage_name = PLEXUS_STAGES[args.stage - 1]

    # Override output directory if specified
    if args.output:
        output_dir = args.output.resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        config.crawler_output = output_dir
        config.summaries_dir = output_dir / "summaries"
        config.patterns_dir = output_dir / "patterns"
        config.maps_dir = output_dir / "maps"
        config.exports_dir = output_dir / "exports"
        for sub in (
            config.summaries_dir,
            config.patterns_dir,
            config.maps_dir,
            config.exports_dir,
        ):
            sub.mkdir(parents=True, exist_ok=True)

    # Validate input file
    if args.file is None:
        print("Error: --file is required. Use --file <path>.")
        return 1

    input_file = args.file.resolve()
    if not input_file.exists():
        print(f"Error: file not found: {input_file}")
        return 1

    location_label = args.location or os.getenv("HODIE_LOCATION", "unknown")
    print(f"∰ Hodie PIXEL8 Crawler")
    print(f"  Location : {location_label}")
    print(f"  File     : {input_file.name}")
    print(f"  Output   : {config.crawler_output}")
    print(f"  Stage    : {args.stage} ({stage_name})")
    print("-" * 50)

    # Build and run pipeline
    pipeline = ConversationParser(config) + PatternExtractor(config)
    result = await pipeline.process_file(input_file)

    # Save result
    out_file = config.summaries_dir / f"{input_file.stem}_result.json"
    result.save(out_file)

    print(f"  Parts    : {len(result.parts)}")
    print(f"  Patterns : {len(result.key_patterns)}")
    print(f"  Topics   : {len(result.key_topics)}")
    print(f"  Entities : {len(result.key_entities)}")
    print(f"  Seal     : {result.verification_seal}")
    print(f"  Saved →  {out_file}")
    print("∞ Done.")
    return 0


def main() -> None:
    """CLI entry point registered in pyproject.toml."""
    parser = _build_parser()
    args = parser.parse_args()
    sys.exit(asyncio.run(_run(args)))


if __name__ == "__main__":
    main()
