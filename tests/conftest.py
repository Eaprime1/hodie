"""
Shared fixtures for PIXEL8 Crawler test suite
∰◊€π¿🌌∞
"""

import json
import pytest
from pathlib import Path

from crawler_pixel8.config import CrawlerConfig


@pytest.fixture
def test_config(tmp_path):
    """CrawlerConfig with all output dirs pointed at tmp_path"""
    config = CrawlerConfig(
        conversation_archive=tmp_path,
        crawler_output=tmp_path / "crawler_output",
        patterns_dir=tmp_path / "crawler_output/patterns",
        maps_dir=tmp_path / "crawler_output/maps",
        summaries_dir=tmp_path / "crawler_output/summaries",
        exports_dir=tmp_path / "crawler_output/exports",
        quanta_dir=tmp_path / "quanta",
    )
    return config


@pytest.fixture
def sample_json_file(tmp_path):
    """ChatGPT-format JSON conversation with 3 turns"""
    data = [
        {"role": "user", "content": "Hello, can you help me write a Python function?"},
        {"role": "assistant", "content": "Of course! Here is a simple def greet(name): function example."},
        {"role": "user", "content": "Thanks! How do I import it from another file?"},
    ]
    filepath = tmp_path / "test_conversation.json"
    filepath.write_text(json.dumps(data), encoding="utf-8")
    return filepath


@pytest.fixture
def sample_json_messages_file(tmp_path):
    """JSON with 'messages' key (alternate format)"""
    data = {
        "title": "Test Conversation",
        "messages": [
            {"role": "user", "content": "What is an AI agent?"},
            {"role": "assistant", "content": "An AI agent uses an LLM model to reason and act."},
        ],
    }
    filepath = tmp_path / "test_messages.json"
    filepath.write_text(json.dumps(data), encoding="utf-8")
    return filepath


@pytest.fixture
def sample_markdown_file(tmp_path):
    """Markdown conversation with User/Assistant headers"""
    content = """# Test Conversation

**User:** Hello Claude, how does the crawler work?

**Assistant:** The PIXEL8 crawler processes conversation files through a pipeline.

**User:** Can you show me an example with entity extraction?

**Assistant:** Yes, entities like URLs (https://example.com) and emails (test@example.com) are extracted automatically.
"""
    filepath = tmp_path / "test_conversation.md"
    filepath.write_text(content, encoding="utf-8")
    return filepath


@pytest.fixture
def sample_text_file(tmp_path):
    """Plain text conversation"""
    content = "This is a plain text conversation about Python programming and crawler systems.\n"
    filepath = tmp_path / "test_conversation.txt"
    filepath.write_text(content, encoding="utf-8")
    return filepath
