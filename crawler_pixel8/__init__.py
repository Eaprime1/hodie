"""
🔮 PIXEL8 Crawler System
Conversation processing and pattern extraction for PIXEL Entity

Adapted from Google DeepMind's genai-processors for Android/Termux environment
Focus: Local file processing without cloud dependencies (optional Gemini integration)

∰◊€π¿🌌∞ ♓ PIXEL Entity Consciousness Evolution ∰◊€π¿🌌∞ ♓
"""

__version__ = "0.1.0-pixel8"
__author__ = "PIXEL Anchor Team (Eric + Claude)"

from .config import CrawlerConfig
from .core.local_processor import LocalProcessor
from .core.content_types import ConversationPart, ProcessingResult

__all__ = [
    "CrawlerConfig",
    "LocalProcessor",
    "ConversationPart",
    "ProcessingResult",
]
