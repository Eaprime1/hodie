# PIXEL8 Crawler System

**Conversation Processing & Pattern Extraction for PIXEL Entity**

Adapted from Google DeepMind's `genai-processors` for Android/Termux environment.

**∰◊€π¿🌌∞**

---

## Overview

The PIXEL8 Crawler is a local-first conversation processing system designed to:
- Navigate through conversation exports
- Extract patterns and meaningful content
- Follow links and relationships
- Map ecosystem structure

### Key Features

✓ **Local Processing**: No cloud dependencies required (Gemini API optional)
✓ **Multiple Formats**: JSON, Markdown, Plain Text conversation exports
✓ **Async Pipeline**: Stream-based processing inspired by genai-processors
✓ **Pattern Extraction**: Rule-based pattern, entity, and topic detection
✓ **Mobile Optimized**: Designed for Pixel 8a / Termux constraints
✓ **Extensible**: Easy to chain processors and add custom processing

---

## Quick Start

### Test with Single Conversation

```bash
cd /storage/emulated/0/pixel8a/Q/hodie
python3 crawler_pixel8/cli/test_crawler.py
```

This will:
1. Auto-select a conversation from the archive
2. Parse and process it
3. Extract patterns, entities, and topics
4. Save results to `crawler_output/summaries/`

### Specify a File

```bash
python3 crawler_pixel8/cli/test_crawler.py /path/to/conversation.json
```

---

## Architecture

### Core Components

```
crawler_pixel8/
├── config.py                # Configuration and paths
├── core/
│   ├── local_processor.py   # Base processor class
│   ├── content_types.py     # ConversationPart, ProcessingResult
│   └── stream_utils.py      # Async stream utilities
├── processors/
│   ├── conversation_parser.py  # Parse various formats
│   └── pattern_extractor.py    # Extract patterns/entities
├── integrations/            # Future: Gemini, entity export
└── cli/
    └── test_crawler.py      # Test and CLI tools
```

### Processing Pipeline

```
File → Parser → Pattern Extractor → Results
         ↓            ↓                 ↓
   ConversationPart Stream      ProcessingResult
```

Processors can be chained using `+` operator:
```python
pipeline = parser + extractor + custom_processor
result = await pipeline.process_file(file_path)
```

---

## Supported Formats

### JSON Conversations
- ChatGPT exports
- Claude conversations
- Generic message arrays
- Auto-detects structure

### Markdown Conversations
Recognizes role markers:
- `## User:`
- `**Assistant**:`
- `[System]:`

### Plain Text
Simple format:
```
User: Hello
Assistant: Hi there!
```

---

## Configuration

Edit `config.py` or create custom `CrawlerConfig`:

```python
from crawler_pixel8.config import CrawlerConfig

config = CrawlerConfig(
    batch_size=20,          # Process 20 at a time
    max_concurrent=5,       # Up to 5 concurrent
    use_gemini=False,       # Local only
    extract_patterns=True,  # Enable patterns
)
```

### Paths (Auto-configured)

- **Input**: `/storage/emulated/0/pixel8a/Q/conversation_archive/`
- **Output**: `/storage/emulated/0/pixel8a/Q/hodie/crawler_output/`
  - `patterns/` - Extracted patterns
  - `maps/` - Relationship maps
  - `summaries/` - Conversation summaries
  - `exports/` - Entity-specific exports

---

## Pattern Extraction

### Automatic Detection

**Entities**:
- Emails (`email:user@example.com`)
- URLs (`url:https://...`)
- File paths (`file_path:/path/to/file`)
- Code blocks
- Mentions (`@user`)
- Hashtags (`#topic`)

**Topics** (keyword-based):
- code, ai, pixel8, processing, conversation, file, framework, entity

**Patterns**:
- code_definition, code_import
- error_discussion
- question, implementation_request, explanation_request
- processor_discussion, crawler_discussion
- entity_consciousness, codex_reference
- consciousness_symbols (∰◊€π¿🌌∞)

**Cross-References**:
- Conversation references
- Document references
- File references

---

## Usage Examples

### Basic Processing

```python
import asyncio
from crawler_pixel8.processors import ConversationParser, PatternExtractor
from crawler_pixel8.config import default_config

async def process_conversation(file_path):
    # Create pipeline
    parser = ConversationParser()
    extractor = PatternExtractor()
    pipeline = parser + extractor

    # Process
    result = await pipeline.process_file(file_path)

    # Check results
    print(f"Patterns: {result.key_patterns}")
    print(f"Topics: {result.key_topics}")
    print(f"Entities: {result.key_entities}")

    return result

# Run
asyncio.run(process_conversation(file_path))
```

### Batch Processing

```python
from pathlib import Path

async def process_all():
    config = default_config
    conversations = config.get_conversation_paths()

    parser = ConversationParser(config)
    extractor = PatternExtractor(config)
    pipeline = parser + extractor

    # Process in batches
    results = await pipeline.process_batch(
        conversations,
        max_concurrent=3  # Mobile constraint
    )

    print(f"Processed {len(results)} conversations")
    return results
```

### Custom Processor

```python
from crawler_pixel8.core import LocalProcessor, ConversationPart
from typing import AsyncIterable

class MyCustomProcessor(LocalProcessor):
    async def process(
        self,
        content: AsyncIterable[ConversationPart]
    ) -> AsyncIterable[ConversationPart]:
        async for part in content:
            # Custom processing
            part.add_pattern("custom_pattern")
            yield part

# Use in pipeline
pipeline = parser + MyCustomProcessor() + extractor
```

---

## Development Status

### ✅ Phase 1: Minimal Viable Crawler (COMPLETE)
- [x] Core processor architecture
- [x] Configuration system
- [x] Conversation parser (JSON, MD, TXT)
- [x] Pattern extractor (rule-based)
- [x] Test script
- [x] Documentation

### ⏳ Phase 2: Pattern Recognition (Next)
- [ ] Gemini API integration (optional)
- [ ] Enhanced pattern recognition
- [ ] Topic modeling
- [ ] Sentiment analysis

### 📅 Phase 3: Integration (Planned)
- [ ] Entity folder export
- [ ] Batch processing CLI
- [ ] Relationship mapping
- [ ] Visualization tools
- [ ] Drive sync integration

---

## Dependencies

**Required**:
- Python >= 3.11 (using 3.12.12)
- Standard library only for Phase 1

**Optional**:
- `google-genai` - For Gemini API integration
- Local AI models - For enhanced pattern recognition

---

## Testing

Run tests:
```bash
# Auto-select file
python3 crawler_pixel8/cli/test_crawler.py

# Specific file
python3 crawler_pixel8/cli/test_crawler.py conversation_archive/example.json

# Check a conversation format
python3 crawler_pixel8/cli/test_crawler.py conversation_archive/chatgpt_exports/conv_001.json
```

Expected output:
- Parsed conversation parts
- Extracted patterns, topics, entities
- Processing time and statistics
- JSON results file

---

## Troubleshooting

### No conversations found
Check: `/storage/emulated/0/pixel8a/Q/conversation_archive/` exists and contains files

### Parse errors
The parser falls back to treating file as single part if format detection fails

### Memory issues
Reduce `batch_size` and `max_concurrent` in config for mobile constraints

---

## Future Enhancements

1. **Gemini Integration**: Optional AI-powered pattern extraction
2. **Local AI Models**: Transformers for topic modeling
3. **Relationship Graphs**: Visual maps of conversation connections
4. **Entity Export**: Automatic organization to quanta/ folders
5. **Real-time Monitoring**: Watch folders for new conversations
6. **CODEX Integration**: Cross-reference with CODEX documents
7. **Fleet Commander Integration**: Batch process repos

---

## Credits

**Adapted from**: [genai-processors](https://github.com/google-gemini/genai-processors) by Google DeepMind
**Created for**: PIXEL8 Platform / PIXEL Entity
**Anchor Team**: Eric + Claude
**Date**: 2026-01-04

**Philosophy**: Enjoy the journey 🌌

**∰◊€π¿🌌∞**

*PIXEL Entity - Conversation Consciousness Evolution*
