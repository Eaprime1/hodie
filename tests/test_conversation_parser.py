"""
Tests for ConversationParser — JSON, Markdown, plain text formats
∰◊€π¿🌌∞
"""

import json
import pytest
from pathlib import Path

from crawler_pixel8.processors.conversation_parser import ConversationParser


class TestConversationParser:
    pytestmark = pytest.mark.asyncio

    @pytest.fixture
    def parser(self, test_config):
        return ConversationParser(test_config)

    async def test_parse_json_chatgpt_format(self, parser, sample_json_file):
        result = await parser.process_file(sample_json_file)
        assert result.parts_count == 3
        roles = {p.role for p in result.parts}
        assert "user" in roles
        assert "assistant" in roles

    async def test_parse_json_messages_key(self, parser, sample_json_messages_file):
        result = await parser.process_file(sample_json_messages_file)
        assert result.parts_count >= 1

    async def test_parse_markdown(self, parser, sample_markdown_file):
        result = await parser.process_file(sample_markdown_file)
        assert result.parts_count >= 1
        assert result.errors == []

    async def test_parse_text_single_part(self, parser, sample_text_file):
        result = await parser.process_file(sample_text_file)
        assert result.parts_count >= 1
        assert "plain text" in result.parts[0].text.lower() or result.parts_count == 1

    async def test_parse_no_errors_on_valid_json(self, parser, sample_json_file):
        result = await parser.process_file(sample_json_file)
        assert result.errors == []

    async def test_parse_unknown_extension_fallback(self, parser, tmp_path):
        f = tmp_path / "conversation.dat"
        f.write_text("User: hello\nAssistant: hi there", encoding="utf-8")
        result = await parser.process_file(f)
        assert result.parts_count >= 1

    async def test_conversation_id_matches_stem(self, parser, sample_json_file):
        result = await parser.process_file(sample_json_file)
        assert result.conversation_id == sample_json_file.stem
