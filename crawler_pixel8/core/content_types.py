"""
Content types for PIXEL8 Crawler
Simplified ProcessorPart concept without cloud dependencies
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from pathlib import Path
import json


@dataclass
class ConversationPart:
    """
    A piece of content from a conversation
    Simplified alternative to genai ProcessorPart for local processing
    """

    # Core content
    text: str = ""
    role: str = "unknown"  # user, assistant, system
    timestamp: Optional[datetime] = None

    # Metadata
    source_file: Optional[Path] = None
    conversation_id: Optional[str] = None
    turn_number: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    # Processing results
    patterns: List[str] = field(default_factory=list)
    entities: List[str] = field(default_factory=list)
    topics: List[str] = field(default_factory=list)
    links: List[str] = field(default_factory=list)

    def __post_init__(self):
        """Ensure timestamp exists"""
        if self.timestamp is None:
            self.timestamp = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "text": self.text,
            "role": self.role,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "source_file": str(self.source_file) if self.source_file else None,
            "conversation_id": self.conversation_id,
            "turn_number": self.turn_number,
            "metadata": self.metadata,
            "patterns": self.patterns,
            "entities": self.entities,
            "topics": self.topics,
            "links": self.links,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConversationPart":
        """Create from dictionary"""
        # Handle timestamp conversion
        if data.get("timestamp"):
            data["timestamp"] = datetime.fromisoformat(data["timestamp"])

        # Handle Path conversion
        if data.get("source_file"):
            data["source_file"] = Path(data["source_file"])

        return cls(**data)

    def add_pattern(self, pattern: str):
        """Add a detected pattern"""
        if pattern not in self.patterns:
            self.patterns.append(pattern)

    def add_entity(self, entity: str):
        """Add a detected entity"""
        if entity not in self.entities:
            self.entities.append(entity)

    def add_topic(self, topic: str):
        """Add a detected topic"""
        if topic not in self.topics:
            self.topics.append(topic)

    def add_link(self, link: str):
        """Add a cross-reference link"""
        if link not in self.links:
            self.links.append(link)


@dataclass
class ProcessingResult:
    """
    Results from processing a conversation or batch of conversations
    """

    # Source information
    source_file: Optional[Path] = None
    conversation_id: Optional[str] = None
    processed_at: datetime = field(default_factory=datetime.now)

    # Processing metadata
    parts_count: int = 0
    processing_time: float = 0.0
    errors: List[str] = field(default_factory=list)

    # Extracted content
    parts: List[ConversationPart] = field(default_factory=list)
    summary: str = ""
    key_patterns: List[str] = field(default_factory=list)
    key_entities: List[str] = field(default_factory=list)
    key_topics: List[str] = field(default_factory=list)

    # Relationships
    related_conversations: List[str] = field(default_factory=list)
    cross_references: Dict[str, List[str]] = field(default_factory=dict)

    # Output paths
    output_files: Dict[str, Path] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "source_file": str(self.source_file) if self.source_file else None,
            "conversation_id": self.conversation_id,
            "processed_at": self.processed_at.isoformat(),
            "parts_count": self.parts_count,
            "processing_time": self.processing_time,
            "errors": self.errors,
            "parts": [part.to_dict() for part in self.parts],
            "summary": self.summary,
            "key_patterns": self.key_patterns,
            "key_entities": self.key_entities,
            "key_topics": self.key_topics,
            "related_conversations": self.related_conversations,
            "cross_references": self.cross_references,
            "output_files": {k: str(v) for k, v in self.output_files.items()},
        }

    def save(self, output_path: Path):
        """Save results to JSON file"""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

    @classmethod
    def load(cls, input_path: Path) -> "ProcessingResult":
        """Load results from JSON file"""
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Convert parts
        if "parts" in data:
            data["parts"] = [ConversationPart.from_dict(p) for p in data["parts"]]

        # Convert timestamps
        if "processed_at" in data:
            data["processed_at"] = datetime.fromisoformat(data["processed_at"])

        # Convert paths
        if data.get("source_file"):
            data["source_file"] = Path(data["source_file"])

        if "output_files" in data:
            data["output_files"] = {k: Path(v) for k, v in data["output_files"].items()}

        return cls(**data)

    def add_error(self, error: str):
        """Add an error message"""
        self.errors.append(f"{datetime.now().isoformat()}: {error}")

    def aggregate_patterns(self):
        """Aggregate patterns from all parts"""
        all_patterns = []
        for part in self.parts:
            all_patterns.extend(part.patterns)

        # Count occurrences and sort
        pattern_counts = {}
        for pattern in all_patterns:
            pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1

        # Get top patterns
        self.key_patterns = sorted(
            pattern_counts.keys(),
            key=lambda x: pattern_counts[x],
            reverse=True
        )[:20]  # Top 20 patterns

    def aggregate_entities(self):
        """Aggregate entities from all parts"""
        all_entities = []
        for part in self.parts:
            all_entities.extend(part.entities)

        # Deduplicate and sort
        self.key_entities = sorted(list(set(all_entities)))

    def aggregate_topics(self):
        """Aggregate topics from all parts"""
        all_topics = []
        for part in self.parts:
            all_topics.extend(part.topics)

        # Count occurrences and sort
        topic_counts = {}
        for topic in all_topics:
            topic_counts[topic] = topic_counts.get(topic, 0) + 1

        # Get top topics
        self.key_topics = sorted(
            topic_counts.keys(),
            key=lambda x: topic_counts[x],
            reverse=True
        )[:10]  # Top 10 topics
