"""
Module 05 · Structure-aware chunking (Markdown)

    Read the guide:   python rag.py learn 5
    Run the tests:    python rag.py test 5
    Get a hint:       python rag.py hint 5 <problem>

Replace each `raise NotImplementedError` with your solution.
"""
import re


# ─────────────────────────────────────────────────────────────────────
# Problem 1 · split_sections                                   (medium)
# ─────────────────────────────────────────────────────────────────────
def split_sections(markdown: str) -> list[dict]:
    """
    Split Markdown into sections, one per heading.

    - A heading is a line: 1 to 6 "#", then a space, then the title.
    - Lines inside a fenced code block (between lines starting with ```) are never headings.
    - Each section is {"heading_path": [...titles from top level down...], "text": body}
      where body is the lines under the heading (until the next heading), joined with "\\n"
      and stripped.
    - Text before the first heading forms a section with heading_path [].
    - Skip sections whose body is empty after stripping.

    Example:
        split_sections("# A\\na\\n## B\\nb\\n### C\\nc\\n## D\\nd")
        -> [{"heading_path": ["A"], "text": "a"},
            {"heading_path": ["A", "B"], "text": "b"},
            {"heading_path": ["A", "B", "C"], "text": "c"},
            {"heading_path": ["A", "D"], "text": "d"}]
    """
    raise NotImplementedError


# ─────────────────────────────────────────────────────────────────────
# Problem 2 · pack                                               (easy)
# ─────────────────────────────────────────────────────────────────────
def pack(pieces: list[str], max_chars: int, sep: str = " ") -> list[str]:
    """
    Greedily join pieces (with `sep` between them) into chunks of at most max_chars characters.
    Keep adding pieces to the current chunk while the result still fits; otherwise start a new one.
    A single piece longer than max_chars becomes its own chunk (never split a piece).

    Example 1:  pack(["aa", "bb", "cc"], 5)              -> ["aa bb", "cc"]
    Example 2:  pack(["aaaaaa", "b"], 4)                 -> ["aaaaaa", "b"]
    Example 3:  pack(["a", "b"], 4, sep="\\n\\n")          -> ["a\\n\\nb"]
    """
    raise NotImplementedError


# ─────────────────────────────────────────────────────────────────────
# Problem 3 · section_chunks                                     (easy)
# ─────────────────────────────────────────────────────────────────────
def section_chunks(markdown: str, path: str, max_chars: int) -> list[dict]:
    """
    Turn Markdown into chunks:
      1. split it into sections with split_sections()
      2. split each section's text into paragraphs (separated by blank lines), stripped,
         dropping empty ones
      3. pack() each section's paragraphs with sep="\\n\\n"
      4. make one dict per packed piece:
            "path"          the path
            "heading_path"  the section's heading path
            "text"          the packed piece (original text, used for citations)
            "search_text"   " > ".join(heading_path) + "\\n" + text
                            (just text when heading_path is empty)

    Example search_text:
        "Tiny Shop > Run with Docker\\nBuild the image, then start the container..."
    """
    raise NotImplementedError
