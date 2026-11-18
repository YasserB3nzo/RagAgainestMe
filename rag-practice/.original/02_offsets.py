"""
Module 02 · Source spans & offsets

    Read the guide:   python rag.py learn 2
    Run the tests:    python rag.py test 2
    Get a hint:       python rag.py hint 2 <problem>

Replace each `raise NotImplementedError` with your solution.
"""


# ─────────────────────────────────────────────────────────────────────
# Problem 1 · line_starts                                        (easy)
# ─────────────────────────────────────────────────────────────────────
def line_starts(text: str) -> list[int]:
    """
    Return the character offset where each line starts.
    Line 1 always starts at 0. Every "\\n" at offset i starts a new line at i + 1.

    Example 1:  line_starts("ab\\ncd\\n")  -> [0, 3, 6]
    Example 2:  line_starts("abc")        -> [0]
    Example 3:  line_starts("")           -> [0]
    """
    raise NotImplementedError


# ─────────────────────────────────────────────────────────────────────
# Problem 2 · line_of_offset                                     (easy)
# ─────────────────────────────────────────────────────────────────────
def line_of_offset(text: str, offset: int) -> int:
    """
    Return the 1-based line number of the character at `offset`.
    A "\\n" belongs to the line it ends.
    offset == len(text) is allowed (it's the end position).
    Raise ValueError if offset < 0 or offset > len(text).

    With text = "ab\\ncd":
        offset 0 ('a')  -> 1
        offset 2 ('\\n') -> 1
        offset 3 ('c')  -> 2
        offset 5 (end)  -> 2
    """
    raise NotImplementedError


# ─────────────────────────────────────────────────────────────────────
# Problem 3 · span_to_lines                                      (easy)
# ─────────────────────────────────────────────────────────────────────
def span_to_lines(text: str, start: int, end: int) -> tuple[int, int]:
    """
    For the half-open span [start, end) return (first_line, last_line), both 1-based.
    The last character of the span is at end - 1.
    For an empty span (start == end) return (line, line) for the line of `start`.
    Raise ValueError unless 0 <= start <= end <= len(text).

    Example:
        text = "import os\\n\\ndef f():\\n    return 1\\n"
        start = text.index("def")
        end = text.index("1") + 1
        span_to_lines(text, start, end) -> (3, 4)
    """
    raise NotImplementedError


# ─────────────────────────────────────────────────────────────────────
# Problem 4 · char_to_byte                                       (easy)
# ─────────────────────────────────────────────────────────────────────
def char_to_byte(text: str, char_offset: int) -> int:
    """
    Convert a character offset into a UTF-8 byte offset.
    Raise ValueError if char_offset < 0 or char_offset > len(text).

    Example 1:  char_to_byte("cafe ok", 5)  -> 5   (plain ASCII: same number)
    Example 2:  char_to_byte("café ok", 5)  -> 6   ("é" takes 2 bytes)
    Example 3:  char_to_byte("a🙂b", 2)      -> 5   ("🙂" takes 4 bytes)
    """
    raise NotImplementedError


# ─────────────────────────────────────────────────────────────────────
# Problem 5 · byte_to_char                                     (medium)
# ─────────────────────────────────────────────────────────────────────
def byte_to_char(text: str, byte_offset: int) -> int:
    """
    Convert a UTF-8 byte offset into a character offset (the reverse of char_to_byte).
    Raise ValueError if:
      - byte_offset < 0 or byte_offset > the number of bytes, or
      - byte_offset lands in the MIDDLE of a multi-byte character.

    Example 1:  byte_to_char("café ok", 6)  -> 5
    Example 2:  byte_to_char("a🙂b", 5)      -> 2
    Example 3:  byte_to_char("a🙂b", 2)      -> ValueError (inside the emoji)
    """
    raise NotImplementedError
