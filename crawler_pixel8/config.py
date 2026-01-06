"""
Configuration for PIXEL8 Crawler System
Pixel8-specific paths and settings for conversation processing
"""

from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional
import os


@dataclass
class CrawlerConfig:
    """Configuration for PIXEL8 Crawler operations"""

    # Base paths
    base_dir: Path = field(default_factory=lambda: Path("/storage/emulated/0/pixel8a/Q"))
    hodie_dir: Path = field(default_factory=lambda: Path("/storage/emulated/0/pixel8a/Q/hodie"))

    # Input paths (defaults to current directory if not specified)
    conversation_archive: Optional[Path] = None
    codex_documents: Path = field(
        default_factory=lambda: Path("/storage/emulated/0/pixel8a/Q/hodie/_CONSOLIDATED/CODEX_documents")
    )

    # Output paths
    crawler_output: Path = field(
        default_factory=lambda: Path("/storage/emulated/0/pixel8a/Q/hodie/crawler_output")
    )
    patterns_dir: Path = field(
        default_factory=lambda: Path("/storage/emulated/0/pixel8a/Q/hodie/crawler_output/patterns")
    )
    maps_dir: Path = field(
        default_factory=lambda: Path("/storage/emulated/0/pixel8a/Q/hodie/crawler_output/maps")
    )
    summaries_dir: Path = field(
        default_factory=lambda: Path("/storage/emulated/0/pixel8a/Q/hodie/crawler_output/summaries")
    )
    exports_dir: Path = field(
        default_factory=lambda: Path("/storage/emulated/0/pixel8a/Q/hodie/crawler_output/exports")
    )

    # Entity integration
    quanta_dir: Path = field(
        default_factory=lambda: Path("/storage/emulated/0/pixel8a/Q/hodie/quanta")
    )

    # Processing settings
    batch_size: int = 10
    max_concurrent: int = 3  # Mobile device constraint
    chunk_size: int = 1000  # Characters per processing chunk

    # Feature flags
    use_gemini: bool = False  # Optional Gemini API integration
    use_local_ai: bool = False  # Optional local AI models
    extract_patterns: bool = True
    map_relationships: bool = True
    generate_summaries: bool = True

    # Logging
    log_level: str = "INFO"
    log_file: Optional[Path] = None

    # Conversation formats to process
    supported_formats: List[str] = field(
        default_factory=lambda: [
            "chatgpt",  # ChatGPT export format
            "claude",   # Claude conversation format
            "json",     # Generic JSON exports
            "md",       # Markdown conversations
            "txt",      # Plain text exports
        ]
    )

    def __post_init__(self):
        """Ensure all directories exist and set defaults"""
        # Default conversation_archive to current directory if not specified
        if self.conversation_archive is None:
            self.conversation_archive = Path.cwd()

        # Ensure all directories exist
        for attr_name in dir(self):
            if attr_name.endswith('_dir') or attr_name in ('crawler_output',):
                path = getattr(self, attr_name)
                if isinstance(path, Path):
                    path.mkdir(parents=True, exist_ok=True)

    @property
    def gemini_api_key(self) -> Optional[str]:
        """Get Gemini API key from environment"""
        return os.getenv("GEMINI_API_KEY")

    def get_conversation_paths(self, search_dir: Optional[Path] = None) -> List[Path]:
        """
        Get all conversation files from archive or specified directory

        Args:
            search_dir: Optional directory to search (uses conversation_archive if not specified)
        """
        conversations = []
        target_dir = search_dir or self.conversation_archive

        if target_dir and target_dir.exists():
            # Find all supported format files
            for format_type in self.supported_formats:
                conversations.extend(
                    target_dir.rglob(f"*.{format_type}")
                )
        return sorted(conversations)

    def prompt_for_folder(self) -> Path:
        """Prompt user for folder location interactively"""
        print("\n📁 Select conversation folder:")
        print(f"   Current directory: {Path.cwd()}")
        print(f"   Conversation archive: {self.conversation_archive}")
        print()

        choice = input("Enter folder path (or press Enter for current directory): ").strip()

        if not choice:
            return Path.cwd()

        folder_path = Path(choice).expanduser().resolve()
        if not folder_path.exists():
            print(f"⚠️  Warning: {folder_path} does not exist")
            create = input("Create it? (y/n): ").strip().lower()
            if create == 'y':
                folder_path.mkdir(parents=True, exist_ok=True)
                print(f"✓ Created {folder_path}")
            else:
                print("Using current directory instead")
                return Path.cwd()

        return folder_path

    def get_entity_folders(self) -> List[Path]:
        """Get all entity folders in quanta"""
        if not self.quanta_dir.exists():
            return []
        return [d for d in self.quanta_dir.iterdir() if d.is_dir()]


# Default configuration instance
default_config = CrawlerConfig()
