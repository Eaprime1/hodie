"""
One Hertz Operations Processor for PIXEL8 Crawler
Processes exactly one plexus stage per cycle — one operation, one move.

Philosophy: The crawler only sees active work. Files move through stages
(simplex → duplex → ... → omniplex) one at a time. Each cycle picks the
first available file from the target stage, processes it, and advances it
to the next stage. Then the processor exits.

∰◊€π¿🌌∞ — One Hertz, One Truth
"""

import shutil
import sys
import asyncio
from dataclasses import dataclass
from pathlib import Path
from typing import AsyncIterable, Optional

from ..core.local_processor import LocalProcessor
from ..core.content_types import ConversationPart, ProcessingResult
from ..processors.conversation_parser import ConversationParser
from ..processors.pattern_extractor import PatternExtractor
from ..config import CrawlerConfig


# Plexus stage progression — each file advances one step per cycle
PLEXUS_STAGES = [
    "simplex",
    "duplex",
    "triplex",
    "quadroplex",
    "multiplex",
    "omniplex",
]


@dataclass
class CycleResult:
    """
    Result of one One Hertz cycle.
    Records what was processed and where the file moved.
    """
    stage: str
    processed_file: Path
    next_stage: str
    result: ProcessingResult
    moved_to: Path


class OneHertzProcessor(LocalProcessor):
    """
    Processes exactly one file from one plexus stage per cycle.

    Usage:
        processor = OneHertzProcessor(config)
        cycle = await processor.run_cycle("simplex", Path("plexus/"))
        if cycle:
            print(f"Processed: {cycle.processed_file.name}")
            print(f"Moved to: {cycle.moved_to}")
    """

    def __init__(self, config: Optional[CrawlerConfig] = None):
        super().__init__(config)
        # Internal pipeline: parse then extract patterns
        self._pipeline = ConversationParser(self.config) + PatternExtractor(self.config)

    async def process(
        self,
        content: AsyncIterable[ConversationPart]
    ) -> AsyncIterable[ConversationPart]:
        """Pass-through — satisfies LocalProcessor ABC. Use run_cycle() instead."""
        async for part in content:
            yield part

    async def run_cycle(
        self,
        stage_name: str,
        plexus_root: Path,
    ) -> Optional[CycleResult]:
        """
        Execute one One Hertz cycle:
        1. Find the first processable file in stage_name/
        2. Process it through the full pipeline
        3. Save result to summaries_dir
        4. Move the file to the next plexus stage
        5. Return a CycleResult

        Args:
            stage_name: Plexus stage to process (e.g. "simplex")
            plexus_root: Root directory containing all plexus stage subdirs

        Returns:
            CycleResult if a file was processed, None if the stage is empty
        """
        stage_dir = plexus_root / stage_name

        if not stage_dir.exists():
            self.logger.info("Stage directory does not exist: %s", stage_dir)
            print(f"  Stage '{stage_name}' directory not found at {stage_dir}")
            return None

        # Find processable files in this stage
        candidates = self.config.get_conversation_paths(stage_dir)

        if not candidates:
            print(f"  Stage '{stage_name}' is empty — cycle complete.")
            self.logger.info("Stage '%s' is empty", stage_name)
            return None

        # One Hertz: pick only the first file
        target_file = candidates[0]
        print(f"  Processing: {target_file.name}")

        # Process through full pipeline
        result = await self._pipeline.process_file(target_file)
        result.aggregate_patterns()
        result.aggregate_entities()
        result.aggregate_topics()
        result.generate_verification_seal()

        # Save processing result
        output_path = self.config.summaries_dir / f"{target_file.stem}_one_hertz.json"
        result.save(output_path)
        self.logger.info("Saved result to %s", output_path)

        # Determine next stage
        next_stage = _next_stage(stage_name)

        # Move file to next stage
        next_dir = plexus_root / next_stage
        next_dir.mkdir(parents=True, exist_ok=True)
        moved_to = next_dir / target_file.name
        shutil.move(str(target_file), str(moved_to))

        print(f"  Moved → {next_stage}/{target_file.name}")
        print(f"  Seal:  {result.verification_seal}")

        return CycleResult(
            stage=stage_name,
            processed_file=target_file,
            next_stage=next_stage,
            result=result,
            moved_to=moved_to,
        )


def _next_stage(stage_name: str) -> str:
    """Return the stage that follows stage_name in the plexus progression."""
    if stage_name not in PLEXUS_STAGES:
        return "omniplex"
    idx = PLEXUS_STAGES.index(stage_name)
    if idx >= len(PLEXUS_STAGES) - 1:
        return PLEXUS_STAGES[-1]
    return PLEXUS_STAGES[idx + 1]


async def _cli_main(stage: str, plexus_root: Path) -> None:
    """CLI entry: run one cycle and print results."""
    print(f"\n∰ One Hertz Cycle — stage: {stage}")
    print(f"  Plexus root: {plexus_root}")
    print("-" * 50)

    config = CrawlerConfig()
    processor = OneHertzProcessor(config)
    cycle = await processor.run_cycle(stage, plexus_root)

    if cycle:
        print()
        print("  Patterns:", ", ".join(cycle.result.key_patterns[:5]) or "(none)")
        print("  Topics:  ", ", ".join(cycle.result.key_topics) or "(none)")
        print()
        print("∰ Cycle complete. ∞")
    else:
        print("∰ No work available. ∞")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 -m crawler_pixel8.processors.one_hertz <stage> [plexus_root]")
        print(f"Stages: {', '.join(PLEXUS_STAGES)}")
        sys.exit(1)

    stage_arg = sys.argv[1]
    root_arg = Path(sys.argv[2]) if len(sys.argv) > 2 else Path.cwd() / "plexus"
    asyncio.run(_cli_main(stage_arg, root_arg))
