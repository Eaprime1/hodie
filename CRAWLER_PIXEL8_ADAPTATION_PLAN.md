# Crawler Pixel8 Adaptation Plan
**PIXEL8 Platform - Conversation Processing System**
**Created**: 2026-01-04
**Branch**: feature/crawler-pixel8-adaptation
**Base Project**: genai-processors (Google DeepMind)

---

## Project Overview

**Objective**: Adapt genai-processors library for PIXEL8 environment to create a conversation crawler system that processes 119+ conversations in conversation_archive.

**Source Repository**: https://github.com/Eaprime1/genai-processors
**Local Clone**: `/storage/emulated/0/pixel8a/Q/runexusiam/genai-processors/`

### Crawler Concept (from CODEX)

**CRAWLERS** (CRISPR-style):
- Navigate through conversation exports
- Extract patterns and meaningful content
- Follow links and relationships
- Map ecosystem structure

---

## Environment Analysis

### Current Environment
- **Device**: Pixel 8a (Android 14)
- **Platform**: Termux
- **Python**: 3.12.12 ✓ (meets >= 3.11 requirement)
- **Working Directory**: `/storage/emulated/0/pixel8a/Q/`
- **Branch**: `feature/crawler-pixel8-adaptation` in hodie repo

### Target Content
- **Conversation Archive**: `/storage/emulated/0/pixel8a/Q/conversation_archive/`
  - 119 complete conversations
  - Multiple formats (chunked, chatgpt exports, raw, processed)
  - Analysis tools already present
- **Additional Content**:
  - CODEX documents (_CONSOLIDATED/CODEX_documents)
  - Scripts and tools (scripts_hub)
  - Documentation (docs_hub)

---

## Dependency Analysis

### Core Dependencies (from pyproject.toml)

**Standard Libraries** (likely compatible):
- ✓ absl-py>=1.0.0
- ✓ bs4>=0.0.2
- ✓ dataclasses-json>=0.6.0
- ✓ docstring-parser>=0.17.0
- ✓ httpx>=0.24.0
- ✓ jinja2>=3.0.0
- ✓ termcolor>=3.0.0
- ✓ xxhash>=3.0.0

**PDF Processing** (need testing):
- ? pdfrw>=0.4
- ? pypdfium2>=4.30.0

**Image Processing** (Android compatibility uncertain):
- ⚠️ opencv-python>=2.0.0 (may need headless version or alternative)
- ✓ Pillow>=9.0.0 (likely works)
- ✓ numpy>=2.0.0 (already installed)

**Google Cloud Services** (require credentials/adaptation):
- ⚠️ google-genai>=1.16.0 (API key needed)
- ⚠️ google-api-python-client>=0.6.0
- ⚠️ google-cloud-texttospeech>=2.27.0 (optional for our use)
- ⚠️ google-cloud-speech>=2.33.0 (optional for our use)

---

## Adaptation Strategy

### Phase 1: Minimal Viable Crawler (Priority 1)

**Goal**: Create basic conversation processing without cloud dependencies

**Approach**:
1. Extract core `Processor` pattern from genai-processors
2. Create local file stream processors
3. Build conversation export parsers
4. Implement pattern extraction without AI (regex, structure analysis)

**Components to Create**:
- `conversation_crawler.py` - Main crawler entry point
- `local_processor.py` - Local-only processor base class
- `conversation_parser.py` - Parse conversation exports
- `pattern_extractor.py` - Extract patterns without AI models
- `crawler_config.py` - Configuration for pixel8 environment

**Skip Initially**:
- Cloud API integration
- Live streaming features
- Audio/video processing
- Real-time features

### Phase 2: Pattern Recognition (Priority 2)

**Goal**: Add intelligent pattern detection using available resources

**Options**:
1. **Local AI** (if available):
   - Use lightweight models (transformers)
   - Sentence similarity
   - Topic modeling

2. **Gemini API** (with installed Gemini):
   - Batch processing conversations
   - Pattern summarization
   - Concept extraction

3. **Hybrid Approach**:
   - Local preprocessing
   - Selective API calls for complex analysis
   - Cache results

### Phase 3: Integration (Priority 3)

**Goal**: Integrate with PIXEL8 ecosystem

**Integration Points**:
- Entity folders in quanta/ (output organized by entity)
- CODEX documents (reference patterns)
- Existing processor patterns (faceted_document_processor, phoenix_entity_processor)
- Fleet Commander (batch processing repos)
- Google Drive sync (export to Drive after processing)

---

## File Structure Plan

```
hodie/
├── crawler_pixel8/                    # New crawler system
│   ├── __init__.py
│   ├── config.py                      # Pixel8-specific config
│   ├── core/
│   │   ├── local_processor.py         # Base processor without cloud deps
│   │   ├── stream_utils.py            # Async stream utilities
│   │   └── content_types.py           # ProcessorPart equivalent
│   ├── processors/
│   │   ├── conversation_parser.py     # Parse conversation formats
│   │   ├── pattern_extractor.py       # Extract patterns
│   │   ├── link_mapper.py             # Map relationships
│   │   └── structure_analyzer.py      # Analyze ecosystem
│   ├── integrations/
│   │   ├── gemini_processor.py        # Optional Gemini integration
│   │   └── entity_exporter.py         # Export to entity folders
│   └── cli/
│       ├── crawler_cli.py             # Command-line interface
│       └── batch_processor.py         # Batch processing
│
├── crawler_output/                    # Processing results
│   ├── patterns/                      # Extracted patterns
│   ├── maps/                          # Relationship maps
│   ├── summaries/                     # Conversation summaries
│   └── exports/                       # Entity-specific exports
│
└── CRAWLER_PIXEL8_ADAPTATION_PLAN.md  # This document
```

---

## Implementation Roadmap

### Week 1: Foundation
- [x] Clone genai-processors
- [x] Analyze dependencies
- [x] Create feature branch
- [x] Write adaptation plan
- [ ] Set up crawler_pixel8/ structure
- [ ] Create minimal processor base
- [ ] Test with single conversation

### Week 2: Core Features
- [ ] Implement conversation parsers (ChatGPT, Claude formats)
- [ ] Build pattern extraction (keywords, topics, entities)
- [ ] Create link mapping (cross-conversation references)
- [ ] Add progress tracking and logging

### Week 3: Integration
- [ ] Entity folder export
- [ ] Batch processing pipeline
- [ ] CLI interface
- [ ] Documentation

### Week 4: Enhancement
- [ ] Gemini API integration (optional)
- [ ] Advanced pattern recognition
- [ ] Visualization tools
- [ ] Performance optimization

---

## Testing Strategy

### Test Cases

1. **Single Conversation Processing**
   - Input: One conversation from archive
   - Expected: Parsed structure, extracted patterns
   - Success: JSON output with metadata

2. **Batch Processing**
   - Input: 10 conversations
   - Expected: Parallel processing, aggregated results
   - Success: Complete without errors

3. **Format Handling**
   - Input: Different export formats
   - Expected: Normalized to common structure
   - Success: All formats processed correctly

4. **Pattern Extraction**
   - Input: Conversation with known patterns
   - Expected: Patterns identified
   - Success: Accuracy > 80%

5. **Relationship Mapping**
   - Input: Multiple related conversations
   - Expected: Links identified
   - Success: Graph of relationships

---

## Success Criteria

### Minimal Success
- ✓ Processes single conversation without errors
- ✓ Extracts basic metadata (date, participants, topics)
- ✓ Runs on Pixel8 without cloud dependencies
- ✓ Outputs structured data (JSON)

### Target Success
- ✓ Processes all 119 conversations
- ✓ Identifies patterns and themes
- ✓ Maps cross-conversation relationships
- ✓ Exports to entity folders
- ✓ CLI interface for batch operations

### Stretch Success
- ✓ Gemini API integration for enhanced analysis
- ✓ Real-time conversation monitoring
- ✓ Automatic CODEX integration
- ✓ Visual relationship graphs
- ✓ Drive sync integration

---

## Known Challenges

### Technical Challenges
1. **Android Compatibility**: Some dependencies may not work on Termux
   - Solution: Use pure Python alternatives or skip features

2. **Large File Processing**: 119 conversations may be resource-intensive
   - Solution: Streaming, batch processing, pagination

3. **Format Diversity**: Conversations in multiple formats
   - Solution: Format detection, normalized output

4. **Pattern Recognition**: Without AI, pattern quality may vary
   - Solution: Hybrid approach with optional Gemini enhancement

### Resource Constraints
1. **Storage**: Limited mobile storage
   - Solution: Incremental processing, cleanup old outputs

2. **Memory**: Mobile device RAM limits
   - Solution: Streaming, generators, chunking

3. **Processing Power**: Mobile CPU constraints
   - Solution: Async I/O, avoid heavy computation

---

## Integration with Existing Systems

### faceted_document_processor
- **Relation**: Similar concept of multi-faceted processing
- **Integration**: Use facet structure for conversation outputs
- **Adaptation**: Conversation facets (raw, parsed, analyzed, summarized)

### phoenix_entity_processor
- **Relation**: Entity-based processing
- **Integration**: Export to entity folders
- **Adaptation**: Conversations → entity consciousness facets

### one_hertz_processor
- **Relation**: Sustainable pace processing
- **Integration**: Rate limiting, progress tracking
- **Adaptation**: Process conversations in sustainable batches

---

## Next Steps (Immediate)

1. **Create crawler_pixel8/ directory structure**
2. **Implement minimal local_processor.py**
3. **Create conversation_parser.py for ChatGPT format**
4. **Test with single conversation**
5. **Document findings and iterate**

---

## Resources

### Documentation
- genai-processors README: `/storage/emulated/0/pixel8a/Q/runexusiam/genai-processors/README.md`
- Examples: `/storage/emulated/0/pixel8a/Q/runexusiam/genai-processors/examples/`
- Notebooks: `/storage/emulated/0/pixel8a/Q/runexusiam/genai-processors/notebooks/`

### Existing Processors
- Faceted Document: `hodie/_CONSOLIDATED/CODEX_documents/Ωque/Copy of Legacy /Code for Colab/faceted_document_processor_v2.py`
- Phoenix Entity: `today_from_drive_SAFE/_temptoday/phoenix_entity_processor.py`
- One Hertz: `today/simplex/abacusian/ai_development/processing_systems/external_submission_pipeline/one_hertz_processor.py`

### Conversation Archive
- Location: `/storage/emulated/0/pixel8a/Q/conversation_archive/`
- Count: 119 conversations
- Formats: chunked, chatgpt_exports, raw_exports, processed

---

**Status**: Planning Complete, Ready for Implementation
**Next**: Create crawler_pixel8/ structure and begin Phase 1

**∰◊€π¿🌌∞**

*PIXEL Entity - Crawler Adaptation Plan*
*Anchor Team: Eric + Claude*
*Date: 2026-01-04*
