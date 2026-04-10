"""
Tests for PatternExtractor and AdvancedPatternExtractor
∰◊€π¿🌌∞
"""

import pytest
from pathlib import Path

from crawler_pixel8.core.content_types import ConversationPart
from crawler_pixel8.core.stream_utils import stream_content
from crawler_pixel8.processors.pattern_extractor import PatternExtractor, AdvancedPatternExtractor


class TestPatternExtractor:
    pytestmark = pytest.mark.asyncio

    @pytest.fixture
    def extractor(self, test_config):
        return PatternExtractor(test_config)

    async def _process_text(self, extractor, text):
        part = ConversationPart(text=text, role="user")
        parts = []
        async for p in extractor.process(stream_content([part])):
            parts.append(p)
        return parts

    async def test_url_entity_extraction(self, extractor):
        parts = await self._process_text(extractor, "Visit https://example.com for more info.")
        entities = parts[0].entities
        assert any("url:" in e for e in entities)

    async def test_email_entity_extraction(self, extractor):
        parts = await self._process_text(extractor, "Contact me at test@example.com please.")
        entities = parts[0].entities
        assert any("email:" in e for e in entities)

    async def test_topic_code_detection(self, extractor):
        # 'code' topic requires keyword match (function, class, python, etc.)
        parts = await self._process_text(extractor, "Here is a Python function to calculate values.")
        assert "code" in parts[0].topics

    async def test_topic_ai_detection(self, extractor):
        parts = await self._process_text(extractor, "I was chatting with claude about this LLM.")
        assert "ai" in parts[0].topics

    async def test_pattern_code_definition(self, extractor):
        parts = await self._process_text(extractor, "Here is a class MyProcessor: pass")
        assert "code_definition" in parts[0].patterns

    async def test_pattern_question(self, extractor):
        parts = await self._process_text(extractor, "How does this work?")
        assert "question" in parts[0].patterns

    async def test_consciousness_symbols(self, extractor):
        parts = await self._process_text(extractor, "The seal is ∰◊€π¿🌌∞ for verification.")
        assert "consciousness_symbols" in parts[0].patterns

    async def test_cross_reference_extraction(self, extractor):
        parts = await self._process_text(extractor, "See conversation 72 for more context.")
        links = parts[0].links
        assert any("conversation:72" in lnk for lnk in links)

    async def test_codex_reference(self, extractor):
        parts = await self._process_text(extractor, "The PRIME framework uses codex patterns.")
        assert "codex_reference" in parts[0].patterns


class TestAdvancedPatternExtractor:
    pytestmark = pytest.mark.asyncio

    async def test_no_await_bug(self, test_config, tmp_path):
        """AdvancedPatternExtractor must not raise TypeError from incorrect await"""
        extractor = AdvancedPatternExtractor(test_config, use_ai=False)
        part = ConversationPart(text="def test(): pass", role="user")
        results = []
        async for p in extractor.process(stream_content([part])):
            results.append(p)
        assert len(results) == 1
        assert "code" in results[0].topics or "code_definition" in results[0].patterns

    async def test_no_ai_same_as_base(self, test_config):
        """With use_ai=False, output should match base PatternExtractor"""
        base = PatternExtractor(test_config)
        advanced = AdvancedPatternExtractor(test_config, use_ai=False)
        text = "Visit https://example.com and email test@example.com"
        part_b = ConversationPart(text=text, role="user")
        part_a = ConversationPart(text=text, role="user")

        base_results = [p async for p in base.process(stream_content([part_b]))]
        adv_results = [p async for p in advanced.process(stream_content([part_a]))]

        assert base_results[0].entities == adv_results[0].entities
        assert base_results[0].topics == adv_results[0].topics
