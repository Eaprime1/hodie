"""
Local Processor Base Class for PIXEL8 Crawler
Simplified processor pattern without cloud dependencies
Adapted from genai-processors Processor concept
"""

from abc import ABC, abstractmethod
from typing import AsyncIterable, Optional
from pathlib import Path
import logging
import time

from .content_types import ConversationPart, ProcessingResult
from .stream_utils import stream_content
from ..config import CrawlerConfig


class LocalProcessor(ABC):
    """
    Base class for local conversation processors
    Inspired by genai-processors Processor but designed for local file processing
    """

    def __init__(self, config: Optional[CrawlerConfig] = None):
        """
        Initialize processor

        Args:
            config: Crawler configuration (uses default if not provided)
        """
        from ..config import default_config
        self.config = config or default_config
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Set up logging for this processor"""
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(getattr(logging, self.config.log_level))

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    @abstractmethod
    async def process(
        self,
        content: AsyncIterable[ConversationPart]
    ) -> AsyncIterable[ConversationPart]:
        """
        Process a stream of conversation parts

        Args:
            content: Async stream of ConversationParts

        Yields:
            Processed ConversationParts
        """
        pass

    async def process_file(self, file_path: Path) -> ProcessingResult:
        """
        Process a single conversation file

        Args:
            file_path: Path to conversation file

        Returns:
            ProcessingResult with aggregated data
        """
        start_time = time.time()
        result = ProcessingResult(
            source_file=file_path,
            conversation_id=file_path.stem
        )

        try:
            self.logger.info(f"Processing file: {file_path}")

            # Read and parse file (to be implemented by subclasses)
            parts = await self._parse_file(file_path)

            # Process through the processor pipeline
            processed_parts = []
            async for part in self.process(stream_content(parts)):
                processed_parts.append(part)

            result.parts = processed_parts
            result.parts_count = len(processed_parts)

            # Aggregate patterns, entities, topics
            result.aggregate_patterns()
            result.aggregate_entities()
            result.aggregate_topics()

            # Generate verification seal
            result.generate_verification_seal()

            self.logger.info(
                f"Processed {result.parts_count} parts from {file_path.name}"
            )
            self.logger.info(f"Verification seal: {result.verification_seal}")

        except Exception as e:
            error_msg = f"Error processing {file_path}: {str(e)}"
            self.logger.error(error_msg)
            result.add_error(error_msg)

        result.processing_time = time.time() - start_time
        return result

    async def _parse_file(self, file_path: Path) -> list[ConversationPart]:
        """
        Parse a conversation file into ConversationParts
        Default implementation - subclasses should override for specific formats

        Args:
            file_path: Path to file

        Returns:
            List of ConversationParts
        """
        # Default: treat entire file as single part
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        return [
            ConversationPart(
                text=content,
                source_file=file_path,
                conversation_id=file_path.stem
            )
        ]

    async def process_batch(
        self,
        file_paths: list[Path],
        max_concurrent: Optional[int] = None
    ) -> list[ProcessingResult]:
        """
        Process multiple files

        Args:
            file_paths: List of file paths to process
            max_concurrent: Maximum concurrent processing (uses config if not provided)

        Returns:
            List of ProcessingResults
        """
        import asyncio

        max_concurrent = max_concurrent or self.config.max_concurrent

        self.logger.info(
            f"Processing {len(file_paths)} files with max {max_concurrent} concurrent"
        )

        results = []
        semaphore = asyncio.Semaphore(max_concurrent)

        async def process_with_semaphore(path):
            async with semaphore:
                return await self.process_file(path)

        # Process all files
        tasks = [process_with_semaphore(path) for path in file_paths]
        results = await asyncio.gather(*tasks)

        successful = sum(1 for r in results if not r.errors)
        self.logger.info(
            f"Batch processing complete: {successful}/{len(results)} successful"
        )

        return results

    def __add__(self, other: "LocalProcessor") -> "ChainedProcessor":
        """
        Chain processors together using + operator
        Inspired by genai-processors processor chaining
        """
        return ChainedProcessor(self, other)


class ChainedProcessor(LocalProcessor):
    """
    Chains two processors together
    Output of first becomes input of second
    """

    def __init__(self, first: LocalProcessor, second: LocalProcessor):
        super().__init__(first.config)
        self.first = first
        self.second = second

    async def process(
        self,
        content: AsyncIterable[ConversationPart]
    ) -> AsyncIterable[ConversationPart]:
        """Process through both processors in sequence"""
        intermediate = self.first.process(content)
        final = self.second.process(intermediate)
        async for part in final:
            yield part


class IdentityProcessor(LocalProcessor):
    """
    Pass-through processor for testing
    Returns input unchanged
    """

    async def process(
        self,
        content: AsyncIterable[ConversationPart]
    ) -> AsyncIterable[ConversationPart]:
        """Pass through unchanged"""
        async for part in content:
            yield part
