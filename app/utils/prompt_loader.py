"""Utility for loading markdown prompt files."""

from functools import lru_cache
from pathlib import Path

# Base directory for the markdown files (root of the project)
BASE_DIR = Path(__file__).parent.parent.parent


@lru_cache
def load_markdown_file(filename: str) -> str:
    """Read a markdown file from the root directory and return its content.

    Args:
        filename: Name of the file with extension (e.g., 'rules.md').

    Returns:
        The content of the file as a string.
    """
    file_path = BASE_DIR / filename
    if not file_path.exists():
        return f"File {filename} not found."

    with open(file_path, encoding="utf-8") as f:
        return f.read()


def get_full_context() -> dict[str, str]:
    """Load all necessary context files for the prompt.

    Returns:
        A dictionary with the contents of the context files.
    """
    return {
        "rules": load_markdown_file("rules.md"),
        "system_prompt": load_markdown_file("system_prompt.md"),
        "trend_context": load_markdown_file("trend_context.md"),
        "database": load_markdown_file("database.md"),
    }
