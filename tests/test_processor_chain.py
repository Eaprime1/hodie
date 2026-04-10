"""
Tests for processor chaining, batch processing, and IdentityProcessor
∰◊€π¿🌌∞
"""

import json
import pytest
from pathlib import Path

from crawler_pixel8.core.local_processor import ChainedProcessor, IdentityProcessor
from crawler_pixel8.core.content_types import ConversationPart
from crawler_pixel8.core.stream_utils import stream_content
from crawler_pixel8.processors.conversation_parser import ConversationParser
from crawler_pixel8.processors.pattern_extractor import PatternExtractor


class TestIdentityProcessor:
    pytestmark = pytest.mark.asyncio

    async def test_passthrough_unchanged(self, test_config):
        identity = IdentityProcessor(test_config)
        parts = [
            ConversationPart(text="hello", role="user"),
            ConversationPart(text="world", role="assistant"),
        ]
        results = [p async for p in identity.process(stream_content(parts))]
        assert len(results) == 2
        assert results[0].text == "hello"
        assert results[1].text == "world"


class TestProcessorChain:
    pytestmark = pytest.mark.asyncio

    async def test_chain_operator_type(self, test_config):
        parser = ConversationParser(test_config)
        extractor = PatternExtractor(test_config)
        pipeline = parser + extractor
        assert isinstance(pipeline, ChainedProcessor)

    async def test_chain_processes_file(self, test_config, sample_json_file):
        parser = ConversationParser(test_config)
        extractor = PatternExtractor(test_config)
        pipeline = parser + extractor
        result = await pipeline.process_file(sample_json_file)
        assert result.parts_count > 0
        assert result.errors == []

    async def test_chain_extracts_patterns(self, test_config, sample_json_file):
        pipeline = ConversationParser(test_config) + PatternExtractor(test_config)
        result = await pipeline.process_file(sample_json_file)
        result.aggregate_patterns()
        result.aggregate_topics()
        # Conversation has Python content — should detect code topic
        combined_topics = result.key_topics
        combined_patterns = result.key_patterns
        assert len(combined_topics) > 0 or len(combined_patterns) > 0

    async def test_triple_chain(self, test_config):
        """Three processors chained: identity + identity + identity"""
        a = IdentityProcessor(test_config)
        b = IdentityProcessor(test_config)
        c = IdentityProcessor(test_config)
        pipeline = a + b + c
        parts = [ConversationPart(text="test", role="user")]
        results = [p async for p in pipeline.process(stream_content(parts))]
        assert len(results) == 1


class TestBatchProcessing:
    pytestmark = pytest.mark.asyncio

    async def test_batch_returns_all_results(self, test_config, tmp_path):
        # Create two JSON files
        for i in range(2):
            data = [{"role": "user", "content": f"message {i}"}]
            f = tmp_path / f"conv_{i}.json"
            f.write_text(json.dumps(data), encoding="utf-8")

        pipeline = ConversationParser(test_config) + PatternExtractor(test_config)
        files = list(tmp_path.glob("*.json"))
        results = await pipeline.process_batch(files)

        assert len(results) == 2
        assert all(r.parts_count >= 1 for r in results)

    async def test_batch_respects_max_concurrent(self, test_config, tmp_path):
        """Batch with max_concurrent=1 should still return all results"""
        for i in range(3):
            data = [{"role": "user", "content": f"msg {i}"}]
            f = tmp_path / f"conv_{i}.json"
            f.write_text(json.dumps(data), encoding="utf-8")

        pipeline = ConversationParser(test_config)
        files = list(tmp_path.glob("*.json"))
        results = await pipeline.process_batch(files, max_concurrent=1)
        assert len(results) == 3
