"""
Pattern Extractor for PIXEL8 Crawler
Extracts patterns, entities, and topics from conversations
Local processing without AI models (rule-based initially)
"""

from typing import AsyncIterable, Set
import re
from collections import Counter

from ..core.local_processor import LocalProcessor
from ..core.content_types import ConversationPart


class PatternExtractor(LocalProcessor):
    """
    Extracts patterns from conversation content using rule-based approaches
    Can be enhanced with Gemini API or local AI models later
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Pattern definitions
        self.entity_patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'url': r'https?://[^\s]+',
            'file_path': r'(?:/[\w.-]+)+/?',
            'code_block': r'```[\s\S]*?```',
            'mention': r'@\w+',
            'hashtag': r'#\w+',
        }

        # Topic keywords (can be expanded)
        self.topic_keywords = {
            'code': ['function', 'class', 'variable', 'code', 'programming', 'python', 'javascript'],
            'ai': ['AI', 'model', 'gemini', 'claude', 'chatgpt', 'LLM', 'agent'],
            'pixel8': ['pixel', 'android', 'termux', 'mobile', 'device'],
            'processing': ['process', 'parse', 'extract', 'analyze', 'convert'],
            'conversation': ['conversation', 'dialogue', 'chat', 'message', 'response'],
            'file': ['file', 'document', 'folder', 'directory', 'path'],
            'framework': ['framework', 'system', 'architecture', 'structure'],
            'entity': ['entity', 'consciousness', 'processor', 'crawler'],
        }

    async def process(
        self,
        content: AsyncIterable[ConversationPart]
    ) -> AsyncIterable[ConversationPart]:
        """
        Extract patterns from each conversation part
        """
        async for part in content:
            # Extract entities
            for entity_type, pattern in self.entity_patterns.items():
                matches = re.findall(pattern, part.text)
                for match in matches:
                    part.add_entity(f"{entity_type}:{match}")

            # Extract topics
            text_lower = part.text.lower()
            for topic, keywords in self.topic_keywords.items():
                if any(keyword.lower() in text_lower for keyword in keywords):
                    part.add_topic(topic)

            # Extract patterns (common phrases, technical terms)
            patterns = self._extract_technical_patterns(part.text)
            for pattern in patterns:
                part.add_pattern(pattern)

            # Extract potential cross-references
            links = self._extract_cross_references(part.text)
            for link in links:
                part.add_link(link)

            yield part

    def _extract_technical_patterns(self, text: str) -> Set[str]:
        """Extract technical patterns and common phrases"""
        patterns = set()

        # Code-related patterns
        if 'def ' in text or 'class ' in text:
            patterns.add('code_definition')

        if 'import ' in text or 'from ' in text:
            patterns.add('code_import')

        if 'error' in text.lower() or 'exception' in text.lower():
            patterns.add('error_discussion')

        if '?' in text or 'how' in text.lower():
            patterns.add('question')

        if 'create' in text.lower() or 'build' in text.lower() or 'implement' in text.lower():
            patterns.add('implementation_request')

        if 'explain' in text.lower() or 'understand' in text.lower():
            patterns.add('explanation_request')

        # PIXEL8 specific patterns
        if 'processor' in text.lower():
            patterns.add('processor_discussion')

        if 'crawler' in text.lower():
            patterns.add('crawler_discussion')

        if 'entity' in text.lower() and ('consciousness' in text.lower() or 'pixel' in text.lower()):
            patterns.add('entity_consciousness')

        # CODEX patterns
        if 'prime' in text.lower() or 'codex' in text.lower():
            patterns.add('codex_reference')

        if any(sym in text for sym in ['∰', '◊', '€', 'π', '¿', '🌌', '∞']):
            patterns.add('consciousness_symbols')

        return patterns

    def _extract_cross_references(self, text: str) -> Set[str]:
        """Extract references to other conversations or documents"""
        links = set()

        # File references
        file_refs = re.findall(r'(?:file|document|conversation):\s*([^\s,;]+)', text, re.IGNORECASE)
        links.update(file_refs)

        # Explicit references like "see conversation 72"
        conv_refs = re.findall(r'conversation\s+(\d+|[A-Za-z0-9_-]+)', text, re.IGNORECASE)
        links.update(f"conversation:{ref}" for ref in conv_refs)

        # Document references
        doc_refs = re.findall(r'(?:in|see|refer to)\s+([A-Z][A-Za-z0-9_]+\.md)', text)
        links.update(f"doc:{ref}" for ref in doc_refs)

        return links


class AdvancedPatternExtractor(PatternExtractor):
    """
    Enhanced pattern extractor with optional AI integration
    Can use Gemini API or local models for better pattern recognition
    """

    def __init__(self, *args, use_ai=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.use_ai = use_ai and self.config.use_gemini

    async def process(
        self,
        content: AsyncIterable[ConversationPart]
    ) -> AsyncIterable[ConversationPart]:
        """
        Extract patterns with optional AI enhancement
        """
        async for part in await super().process(content):
            if self.use_ai and self.config.gemini_api_key:
                # TODO: Add Gemini API integration for enhanced pattern extraction
                # For now, just use base patterns
                pass

            yield part
