"""
Configuration for PIXEL8 Crawler System
Pixel8-specific paths and settings for conversation processing
"""

from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional
import logging
import os
import re


def _parse_location_config(location: str) -> Dict[str, str]:
    """
    Parse a .locations/{location}/config.sh file and extract exported variables.

    Looks for lines of the form:
        export VARIABLE_NAME="value"
        export VARIABLE_NAME='value'
        export VARIABLE_NAME=value

    Args:
        location: Location name (e.g. "mulberry", "pixel8a", "codespaces")

    Returns:
        Dict of variable names to their string values. Empty dict on any error.
    """
    # Search relative to this file's repo root, then cwd
    repo_root = Path(__file__).resolve().parent.parent
    config_file = repo_root / ".locations" / location / "config.sh"
    if not config_file.exists():
        config_file = Path.cwd() / ".locations" / location / "config.sh"
    if not config_file.exists():
        return {}

    # Three alternatives: double-quoted, single-quoted, or bare (no spaces/comment)
    export_re = re.compile(
        r'^export\s+([A-Z_][A-Z0-9_]*)='
        r'(?:"([^"]*)"'
        r"|'([^']*)'"
        r'|([^\s#]*))'
        r'\s*(?:#.*)?$'
    )

    result: Dict[str, str] = {}
    try:
        with open(config_file, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                match = export_re.match(line)
                if match:
                    # Take whichever capture group matched (double, single, or bare)
                    value = match.group(2) or match.group(3) or match.group(4) or ""
                    result[match.group(1)] = value
    except OSError:
        pass
    return result


#: Locations that have a corresponding .locations/{name}/config.sh file.
KNOWN_LOCATIONS = ("mulberry", "pixel8a", "codespaces")


def _resolve_hodie_path() -> Path:
    """
    Resolve the hodie directory.

    Priority:
    1. HODIE_PATH env var (explicit override — all locations)
    2. HODIE_LOCATION env var → parse .locations/{location}/config.sh for HODIE_PATH
    3. HODIE_LOCATION == "pixel8a" → pixel8a hardcoded fallback
    4. Fall back to Path.cwd() (CI, testing, unknown environments)
    """
    if hodie_path := os.getenv("HODIE_PATH"):
        return Path(hodie_path)
    location = os.getenv("HODIE_LOCATION", "")
    if location:
        loc_vars = _parse_location_config(location)
        if loc_hodie := loc_vars.get("HODIE_PATH"):
            return Path(loc_hodie)
    if location == "pixel8a":
        return Path("/storage/emulated/0/pixel8a/Q/hodie")
    return Path.cwd()


def _resolve_base_dir() -> Path:
    """Resolve the Q root directory (parent of hodie_dir).

    Priority:
    1. Q_ROOT env var (explicit override)
    2. HODIE_LOCATION env var → parse .locations/{location}/config.sh for Q_ROOT
    3. HODIE_LOCATION == "pixel8a" → pixel8a hardcoded fallback
    4. Fall back to Path.cwd()
    """
    if q_root := os.getenv("Q_ROOT"):
        return Path(q_root)
    location = os.getenv("HODIE_LOCATION", "")
    if location:
        loc_vars = _parse_location_config(location)
        if loc_root := loc_vars.get("Q_ROOT"):
            return Path(loc_root)
    if location == "pixel8a":
        return Path("/storage/emulated/0/pixel8a/Q")
    return Path.cwd()


@dataclass
class CrawlerConfig:
    """Configuration for PIXEL8 Crawler operations"""

    # Location identity — set by env_setup.sh or auto-detected
    location_name: str = field(default_factory=lambda: os.getenv("ENV_NAME", "unknown"))

    # Base paths — overridden by HODIE_PATH / Q_ROOT env vars when set
    base_dir: Path = field(default_factory=_resolve_base_dir)
    hodie_dir: Path = field(default_factory=_resolve_hodie_path)

    # Input paths (defaults to current directory if not specified)
    conversation_archive: Optional[Path] = None
    codex_documents: Path = field(
        default_factory=lambda: _resolve_hodie_path() / "_CONSOLIDATED/CODEX_documents"
    )

    # Output paths — all relative to hodie_dir
    crawler_output: Path = field(
        default_factory=lambda: _resolve_hodie_path() / "crawler_output"
    )
    patterns_dir: Path = field(
        default_factory=lambda: _resolve_hodie_path() / "crawler_output/patterns"
    )
    maps_dir: Path = field(
        default_factory=lambda: _resolve_hodie_path() / "crawler_output/maps"
    )
    summaries_dir: Path = field(
        default_factory=lambda: _resolve_hodie_path() / "crawler_output/summaries"
    )
    exports_dir: Path = field(
        default_factory=lambda: _resolve_hodie_path() / "crawler_output/exports"
    )

    # Entity integration
    quanta_dir: Path = field(
        default_factory=lambda: _resolve_hodie_path() / "quanta"
    )

    # Processing settings
    batch_size: int = 10
    max_concurrent: int = field(
        default_factory=lambda: int(os.getenv("HQ_MAX_CONCURRENT", "3"))
    )  # Mobile constraint default; HQ raises this via env
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

        # Ensure all directories exist (best-effort — skips paths that can't be created)
        _log = logging.getLogger(__name__)
        for attr_name in dir(self):
            if attr_name.endswith('_dir') or attr_name in ('crawler_output',):
                path = getattr(self, attr_name)
                if isinstance(path, Path):
                    try:
                        path.mkdir(parents=True, exist_ok=True)
                    except PermissionError:
                        _log.debug("Skipping unwritable path %s (PermissionError)", path)
                    except OSError as exc:
                        _log.warning("Could not create directory %s: %s", path, exc)

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
