"""
Tests for ConversationPart and ProcessingResult content types
∰◊€π¿🌌∞
"""

import json
import pytest
from datetime import datetime
from pathlib import Path

from crawler_pixel8.core.content_types import ConversationPart, ProcessingResult


class TestConversationPart:
    def test_timestamp_auto_set(self):
        part = ConversationPart(text="hello")
        assert part.timestamp is not None
        assert isinstance(part.timestamp, datetime)

    def test_add_pattern_deduplicates(self):
        part = ConversationPart(text="hello")
        part.add_pattern("code_definition")
        part.add_pattern("code_definition")
        assert part.patterns.count("code_definition") == 1

    def test_add_entity_deduplicates(self):
        part = ConversationPart(text="hello")
        part.add_entity("url:https://example.com")
        part.add_entity("url:https://example.com")
        assert part.entities.count("url:https://example.com") == 1

    def test_add_topic_deduplicates(self):
        part = ConversationPart(text="hello")
        part.add_topic("code")
        part.add_topic("code")
        assert part.topics.count("code") == 1

    def test_to_dict_roundtrip(self):
        part = ConversationPart(
            text="test content",
            role="user",
            conversation_id="conv-1",
            turn_number=0,
        )
        part.add_pattern("question")
        part.add_topic("code")
        data = part.to_dict()
        restored = ConversationPart.from_dict(data)
        assert restored.text == part.text
        assert restored.role == part.role
        assert restored.patterns == part.patterns
        assert restored.topics == part.topics


class TestProcessingResult:
    def _make_result_with_parts(self):
        result = ProcessingResult(conversation_id="test-conv")
        for i in range(3):
            part = ConversationPart(text=f"turn {i}", role="user", turn_number=i)
            part.add_pattern("question")
            part.add_topic("code")
            part.add_entity(f"url:https://example{i}.com")
            result.parts.append(part)
        return result

    def test_aggregate_patterns(self):
        result = self._make_result_with_parts()
        result.aggregate_patterns()
        assert "question" in result.key_patterns

    def test_aggregate_topics(self):
        result = self._make_result_with_parts()
        result.aggregate_topics()
        assert "code" in result.key_topics

    def test_aggregate_entities(self):
        result = self._make_result_with_parts()
        result.aggregate_entities()
        assert len(result.key_entities) == 3

    def test_verification_seal_format(self):
        result = self._make_result_with_parts()
        result.parts_count = len(result.parts)
        result.aggregate_patterns()
        result.aggregate_topics()
        seal = result.generate_verification_seal()
        assert seal.startswith("∰◊€π¿🌌∞-PIXEL8-")
        # Hash portion is 16 hex chars
        hash_part = seal.split("-PIXEL8-")[1]
        assert len(hash_part) == 16
        assert all(c in "0123456789abcdef" for c in hash_part)
        assert result.pixel8_verified is True

    def test_save_and_load_roundtrip(self, tmp_path):
        result = self._make_result_with_parts()
        result.parts_count = len(result.parts)
        result.aggregate_patterns()
        result.aggregate_topics()
        result.aggregate_entities()
        result.generate_verification_seal()

        output_path = tmp_path / "result.json"
        result.save(output_path)
        assert output_path.exists()

        loaded = ProcessingResult.load(output_path)
        assert loaded.conversation_id == result.conversation_id
        assert loaded.parts_count == result.parts_count
        assert loaded.verification_seal == result.verification_seal
        assert loaded.pixel8_verified is True
        assert len(loaded.parts) == len(result.parts)
