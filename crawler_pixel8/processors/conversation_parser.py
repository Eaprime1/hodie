"""
Conversation Parser for PIXEL8 Crawler
Parses various conversation export formats into ConversationParts
"""

from typing import AsyncIterable, Optional
from pathlib import Path
import json
import re
from datetime import datetime

from ..core.local_processor import LocalProcessor
from ..core.content_types import ConversationPart


class ConversationParser(LocalProcessor):
    """
    Parses conversation files into structured ConversationParts
    Supports: ChatGPT exports, Claude exports, JSON, Markdown, Plain text
    """

    async def process(
        self,
        content: AsyncIterable[ConversationPart]
    ) -> AsyncIterable[ConversationPart]:
        """
        Process stream - for parser, this is just pass-through
        Real parsing happens in _parse_file
        """
        async for part in content:
            yield part

    async def _parse_file(self, file_path: Path) -> list[ConversationPart]:
        """
        Parse conversation file based on format

        Detects format from file extension and content
        """
        self.logger.info(f"Parsing conversation file: {file_path}")

        suffix = file_path.suffix.lower()

        try:
            if suffix == '.json':
                return await self._parse_json(file_path)
            elif suffix == '.md':
                return await self._parse_markdown(file_path)
            elif suffix in ['.txt', '.text']:
                return await self._parse_text(file_path)
            else:
                # Try to detect format from content
                return await self._parse_auto_detect(file_path)

        except Exception as e:
            self.logger.error(f"Failed to parse {file_path}: {e}")
            # Fall back to single part
            return await super()._parse_file(file_path)

    async def _parse_json(self, file_path: Path) -> list[ConversationPart]:
        """Parse JSON conversation export"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        parts = []
        conversation_id = file_path.stem

        # ChatGPT format detection
        if isinstance(data, list):
            # List of message objects
            for idx, msg in enumerate(data):
                parts.append(self._parse_message_object(msg, conversation_id, idx, file_path))

        elif isinstance(data, dict):
            # Check for common conversation structures
            if 'messages' in data:
                for idx, msg in enumerate(data['messages']):
                    parts.append(self._parse_message_object(msg, conversation_id, idx, file_path))

            elif 'turns' in data:
                for idx, turn in enumerate(data['turns']):
                    parts.append(self._parse_message_object(turn, conversation_id, idx, file_path))

            else:
                # Single message or unknown format
                parts.append(
                    ConversationPart(
                        text=json.dumps(data, indent=2),
                        source_file=file_path,
                        conversation_id=conversation_id,
                        turn_number=0
                    )
                )

        return parts

    def _parse_message_object(
        self,
        msg: dict,
        conversation_id: str,
        idx: int,
        file_path: Path
    ) -> ConversationPart:
        """Parse a single message object from JSON"""

        # Extract text content (try various field names)
        text = msg.get('content', msg.get('text', msg.get('message', '')))
        if isinstance(text, dict):
            # Claude format: content can be an object
            text = text.get('text', str(text))

        # Extract role
        role = msg.get('role', msg.get('author', msg.get('speaker', 'unknown')))

        # Extract timestamp
        timestamp = None
        ts_field = msg.get('timestamp', msg.get('created_at', msg.get('time')))
        if ts_field:
            try:
                if isinstance(ts_field, (int, float)):
                    timestamp = datetime.fromtimestamp(ts_field)
                else:
                    timestamp = datetime.fromisoformat(str(ts_field))
            except:
                pass

        # Extract metadata
        metadata = {k: v for k, v in msg.items() if k not in ['content', 'text', 'message', 'role', 'timestamp']}

        return ConversationPart(
            text=str(text),
            role=role,
            timestamp=timestamp,
            source_file=file_path,
            conversation_id=conversation_id,
            turn_number=idx,
            metadata=metadata
        )

    async def _parse_markdown(self, file_path: Path) -> list[ConversationPart]:
        """Parse markdown conversation"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        parts = []
        conversation_id = file_path.stem

        # Pattern: ## Role or **Role:** or [Role]:
        role_patterns = [
            r'^##\s*(\w+):?\s*$',  # ## User:
            r'^\*\*(\w+)\*\*:',     # **User**:
            r'^\[(\w+)\]:',         # [User]:
        ]

        current_role = 'unknown'
        current_text = []
        turn_number = 0

        for line in content.split('\n'):
            # Check if this line indicates a role change
            role_found = False
            for pattern in role_patterns:
                match = re.match(pattern, line.strip(), re.IGNORECASE)
                if match:
                    # Save previous turn if exists
                    if current_text:
                        parts.append(
                            ConversationPart(
                                text='\n'.join(current_text).strip(),
                                role=current_role.lower(),
                                source_file=file_path,
                                conversation_id=conversation_id,
                                turn_number=turn_number
                            )
                        )
                        turn_number += 1
                        current_text = []

                    # Update role
                    current_role = match.group(1)
                    role_found = True
                    break

            if not role_found:
                # Add to current text
                current_text.append(line)

        # Add final turn
        if current_text:
            parts.append(
                ConversationPart(
                    text='\n'.join(current_text).strip(),
                    role=current_role.lower(),
                    source_file=file_path,
                    conversation_id=conversation_id,
                    turn_number=turn_number
                )
            )

        return parts if parts else await super()._parse_file(file_path)

    async def _parse_text(self, file_path: Path) -> list[ConversationPart]:
        """Parse plain text conversation"""
        # Similar to markdown but less structured
        # Look for patterns like "User:", "Assistant:", etc.
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        parts = []
        conversation_id = file_path.stem

        # Simple pattern: "Role: " at start of line
        role_pattern = r'^([A-Z][a-z]+):\s+'

        current_role = 'unknown'
        current_text = []
        turn_number = 0

        for line in content.split('\n'):
            match = re.match(role_pattern, line)
            if match:
                # Save previous turn
                if current_text:
                    parts.append(
                        ConversationPart(
                            text='\n'.join(current_text).strip(),
                            role=current_role.lower(),
                            source_file=file_path,
                            conversation_id=conversation_id,
                            turn_number=turn_number
                        )
                    )
                    turn_number += 1
                    current_text = []

                # Update role and start new text
                current_role = match.group(1)
                current_text.append(line[match.end():])
            else:
                current_text.append(line)

        # Add final turn
        if current_text:
            parts.append(
                ConversationPart(
                    text='\n'.join(current_text).strip(),
                    role=current_role.lower(),
                    source_file=file_path,
                    conversation_id=conversation_id,
                    turn_number=turn_number
                )
            )

        return parts if parts else await super()._parse_file(file_path)

    async def _parse_auto_detect(self, file_path: Path) -> list[ConversationPart]:
        """
        Auto-detect format from content
        Try JSON first, then markdown, then text
        """
        try:
            return await self._parse_json(file_path)
        except:
            pass

        try:
            return await self._parse_markdown(file_path)
        except:
            pass

        return await self._parse_text(file_path)
