"""Text processing utilities for chunking and cleaning data."""

import re

from langchain_text_splitters import MarkdownTextSplitter


def clean_text(text: str) -> str:
    """Normalize whitespace and clean up raw text.

    Args:
        text: The raw input string.

    Returns:
        The cleaned string.
    """
    # Remove excessive consecutive newlines
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Remove leading/trailing whitespace
    return text.strip()


def chunk_markdown(
    text: str, chunk_size: int = 500, chunk_overlap: int = 50
) -> list[str]:
    """Split markdown text into distinct chunks.

    Args:
        text: The raw markdown text.
        chunk_size: Maximum characters per chunk.
        chunk_overlap: Overlap between consecutive chunks.

    Returns:
        A list of markdown chunks.
    """
    cleaned = clean_text(text)

    # Use LangChain's Markdown text splitter to respect markdown boundaries
    splitter = MarkdownTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    chunks = splitter.split_text(cleaned)
    return chunks
