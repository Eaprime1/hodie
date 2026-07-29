"""
Entity Development Queue Processor for PIXEL8 Crawler
Reads the Abacusian entity development queue and advances entities
through the One Hertz cycle — one entity per invocation.

BACKLOG Task C: Build Entity Development Queue Processor
- Reads queue JSON from quanta/abacusian/development_queue/
- Updates queue status: naught_stage_ready → processing → complete
- Integrates with OneHertzProcessor for pipeline processing
- Follows the One Hertz principle: one entity per cycle

∰◊€π¿🌌∞ — One Queue, One Entity, One Cycle
"""

import json
import shutil
import asyncio
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

from ..config import CrawlerConfig
from ..core.content_types import ProcessingResult
from ..processors.conversation_parser import ConversationParser
from ..processors.one_hertz import OneHertzProcessor, PLEXUS_STAGES
from ..processors.pattern_extractor import PatternExtractor


# Queue status lifecycle
STATUS_READY = "naught_stage_ready"
STATUS_PROCESSING = "processing"
STATUS_COMPLETE = "complete"
STATUS_SKIPPED = "skipped"


@dataclass
class QueueCycleResult:
    """
    Result of one entity queue cycle.
    Records which entity was processed and its new status.
    """
    entity_id: str
    entity_name: str
    previous_status: str
    new_status: str
    result: Optional[ProcessingResult]
    output_path: Optional[Path]


class EntityQueueProcessor:
    """
    Processes one entity from the Abacusian development queue per cycle.

    The queue is located at:
        quanta/abacusian/development_queue/entity_development_queue.json

    Each cycle:
    1. Reads the queue
    2. Finds the first entity with status 'naught_stage_ready'
    3. Resolves its source file (by path or by searching quanta/)
    4. Processes it through the OneHertzProcessor pipeline
    5. Updates queue status to 'complete'
    6. Writes updated queue back to disk

    Usage:
        processor = EntityQueueProcessor(config)
        result = await processor.run_cycle()
        if result:
            print(f"Processed {result.entity_name} → {result.new_status}")
    """

    QUEUE_FILENAME = "entity_development_queue.json"

    def __init__(
        self,
        config: Optional[CrawlerConfig] = None,
        queue_file: Optional[Path] = None,
    ):
        self.config = config or CrawlerConfig()
        self.logger = self.config  # Reuse config's logger attribute pattern
        self._pipeline = OneHertzProcessor(self.config)
        if queue_file is not None:
            self._queue_dir = queue_file.parent
            self._queue_path = queue_file
        else:
            self._queue_dir = (
                self.config.quanta_dir / "abacusian" / "development_queue"
            )
            self._queue_path = self._queue_dir / self.QUEUE_FILENAME

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def run_cycle(self) -> Optional[QueueCycleResult]:
        """
        Execute one entity queue cycle — process the first ready entity.

        Returns:
            QueueCycleResult if an entity was processed, None if queue is empty
            or all entities are already complete.
        """
        queue_data = self._load_queue()
        if queue_data is None:
            print(f"  Queue file not found: {self._queue_path}")
            return None

        entity = self._find_next_ready(queue_data)
        if entity is None:
            print("  Entity queue is empty — all entities complete or no ready entities.")
            return None

        entity_id = entity.get("id", "unknown")
        source_path_str = entity.get("source_path", "")
        entity_name = Path(source_path_str).name if source_path_str else entity_id

        print(f"  Processing entity: {entity_id} ({entity_name})")
        print(f"  Decision: {entity.get('decision', 'unknown')}")

        # Mark as processing before we start (for crash safety)
        prev_status = entity.get("status", STATUS_READY)
        entity["status"] = STATUS_PROCESSING
        entity["processing_started_at"] = datetime.now().isoformat()
        self._save_queue(queue_data)

        # Resolve source file
        source_file = self._resolve_source_file(source_path_str)

        result: Optional[ProcessingResult] = None
        output_path: Optional[Path] = None
        new_status = STATUS_COMPLETE

        if source_file and source_file.exists():
            result, output_path = await self._process_entity_file(
                source_file, entity_id
            )
        else:
            print(f"  Source file not found: {source_path_str!r} — marking skipped")
            new_status = STATUS_SKIPPED

        # Update queue entry
        entity["status"] = new_status
        entity["completed_at"] = datetime.now().isoformat()
        if output_path:
            entity["output_path"] = str(output_path)
        if result:
            entity["verification_seal"] = result.verification_seal

        self._save_queue(queue_data)

        print(f"  Entity {entity_id} → {new_status}")
        if result:
            print(f"  Seal:  {result.verification_seal}")

        return QueueCycleResult(
            entity_id=entity_id,
            entity_name=entity_name,
            previous_status=prev_status,
            new_status=new_status,
            result=result,
            output_path=output_path,
        )

    def queue_status(self) -> dict:
        """
        Return a summary of the current queue state.

        Returns:
            dict with counts per status and list of entity summaries
        """
        queue_data = self._load_queue()
        if queue_data is None:
            return {"error": "Queue file not found", "path": str(self._queue_path)}

        counts: dict = {}
        entries = []
        for entity in queue_data.get("queue", []):
            status = entity.get("status", "unknown")
            counts[status] = counts.get(status, 0) + 1
            entries.append({
                "id": entity.get("id"),
                "name": Path(entity.get("source_path", "")).name,
                "status": status,
                "queue_position": entity.get("queue_position"),
            })

        return {
            "total": queue_data.get("total_entities", len(entries)),
            "counts": counts,
            "entries": entries,
            "queue_path": str(self._queue_path),
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _load_queue(self) -> Optional[dict]:
        """Load queue JSON from disk, returning None if not found."""
        if not self._queue_path.exists():
            return None
        with open(self._queue_path, encoding="utf-8") as f:
            return json.load(f)

    def _save_queue(self, queue_data: dict) -> None:
        """Persist updated queue JSON to disk."""
        self._queue_dir.mkdir(parents=True, exist_ok=True)
        with open(self._queue_path, "w", encoding="utf-8") as f:
            json.dump(queue_data, f, indent=2, ensure_ascii=False)

    def _find_next_ready(self, queue_data: dict) -> Optional[dict]:
        """Return the first queue entry with STATUS_READY status, or None."""
        for entity in queue_data.get("queue", []):
            if entity.get("status") == STATUS_READY:
                return entity
        return None

    def _resolve_source_file(self, source_path_str: str) -> Optional[Path]:
        """
        Resolve the actual source file on the local filesystem.

        Tries in order:
        1. Exact path from queue JSON
        2. Filename-only search under quanta/
        3. Filename-only search under current working directory

        Returns Path if found, None otherwise.
        """
        if not source_path_str:
            return None

        # Try exact path first
        exact = Path(source_path_str)
        if exact.exists():
            return exact

        # Search by filename under quanta/
        filename = exact.name
        if not filename:
            return None

        for search_root in (self.config.quanta_dir, Path.cwd()):
            if not search_root.exists():
                continue
            matches = list(search_root.rglob(filename))
            if matches:
                return matches[0]

        return None

    async def _process_entity_file(
        self, source_file: Path, entity_id: str
    ) -> tuple:
        """
        Process a single entity file through the OneHertzProcessor pipeline.

        Returns (ProcessingResult, output_path) tuple.
        """
        # Use the simplex stage (first stage) for new entity files
        stage = PLEXUS_STAGES[0]

        # Set up a temporary staging area in summaries_dir
        staging_dir = self.config.summaries_dir / "entity_queue_staging" / stage
        staging_dir.mkdir(parents=True, exist_ok=True)

        # Copy file into staging
        staged_file = staging_dir / source_file.name
        shutil.copy2(str(source_file), str(staged_file))

        # Run one hertz cycle
        plexus_root = staging_dir.parent
        cycle = await self._pipeline.run_cycle(stage, plexus_root)

        if cycle:
            output_path = self.config.summaries_dir / f"{entity_id}_entity_queue.json"
            return cycle.result, output_path

        # Fallback: process directly without staging
        pipeline = ConversationParser(self.config) + PatternExtractor(self.config)
        result = await pipeline.process_file(source_file)
        result.aggregate_patterns()
        result.aggregate_entities()
        result.aggregate_topics()
        result.generate_verification_seal()
        output_path = self.config.summaries_dir / f"{entity_id}_entity_queue.json"
        result.save(output_path)
        return result, output_path


async def _cli_main(action: str, queue_json: Optional[Path]) -> None:
    """CLI entry: run one queue cycle or print queue status."""
    config = CrawlerConfig()
    processor = EntityQueueProcessor(config, queue_file=queue_json)

    if action == "status":
        status = processor.queue_status()
        print("\n∰ Entity Queue Status")
        print(f"  Queue: {status.get('queue_path')}")
        print(f"  Total: {status.get('total')}")
        print(f"  Counts: {status.get('counts')}")
        print()
        for entry in status.get("entries", []):
            print(f"  [{entry['status']:20s}] {entry['id']} — {entry['name']}")
        print()
    else:
        # Default: run one cycle
        print("\n∰ Entity Queue Cycle")
        print("-" * 50)
        result = await processor.run_cycle()
        if result:
            print()
            print(f"  Entity:  {result.entity_id}")
            print(f"  Status:  {result.previous_status} → {result.new_status}")
            if result.output_path:
                print(f"  Output:  {result.output_path}")
            print()
            print("∰ Cycle complete. ∞")
        else:
            print("∰ No ready entities in queue. ∞")


if __name__ == "__main__":
    import sys

    action_arg = sys.argv[1] if len(sys.argv) > 1 else "run"
    queue_arg = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    asyncio.run(_cli_main(action_arg, queue_arg))
