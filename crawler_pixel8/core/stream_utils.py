"""
Stream utilities for PIXEL8 Crawler
Async stream processing adapted from genai-processors
"""

from typing import AsyncIterable, Iterable, List, Union
from .content_types import ConversationPart


async def stream_content(
    content: Union[Iterable[ConversationPart], List[ConversationPart]]
) -> AsyncIterable[ConversationPart]:
    """
    Convert an iterable of ConversationParts to an async stream
    Adapted from genai-processors streams.stream_content
    """
    for part in content:
        yield part


async def merge_streams(
    *streams: AsyncIterable[ConversationPart]
) -> AsyncIterable[ConversationPart]:
    """
    Merge multiple async streams into one
    Simple sequential merge (not parallel to keep it lightweight)
    """
    for stream in streams:
        async for part in stream:
            yield part


async def chunk_stream(
    stream: AsyncIterable[ConversationPart],
    chunk_size: int = 10
) -> AsyncIterable[List[ConversationPart]]:
    """
    Chunk a stream into batches for batch processing
    """
    chunk = []
    async for part in stream:
        chunk.append(part)
        if len(chunk) >= chunk_size:
            yield chunk
            chunk = []

    # Yield remaining parts
    if chunk:
        yield chunk


async def filter_stream(
    stream: AsyncIterable[ConversationPart],
    predicate: callable
) -> AsyncIterable[ConversationPart]:
    """
    Filter stream based on predicate function
    """
    async for part in stream:
        if predicate(part):
            yield part
