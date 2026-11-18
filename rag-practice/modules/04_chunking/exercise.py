"""
Module 04 · Chunking with overlap

    Read the guide:   python rag.py learn 4
    Run the tests:    python rag.py test 4
    Get a hint:       python rag.py hint 4 <problem>

Replace each `raise NotImplementedError` with your solution.
"""


# ─────────────────────────────────────────────────────────────────────
# Problem 1 · line_windows                                       (easy)
# ─────────────────────────────────────────────────────────────────────
def line_windows(n_lines: int, size: int, overlap: int) -> list[tuple[int, int]]:
    """
    Return (start, end) line ranges, 1-based and inclusive, covering lines 1..n_lines.
      - each window has `size` lines (the last one may be shorter)
      - the next window starts `size - overlap` lines after the previous start
      - stop as soon as a window reaches line n_lines
    Return [] when n_lines is 0.
    Raise ValueError if size < 1, overlap < 0, or overlap >= size.

    Example 1:  line_windows(10, 4, 1)  -> [(1, 4), (4, 7), (7, 10)]
    Example 2:  line_windows(9, 4, 1)   -> [(1, 4), (4, 7), (7, 9)]
    Example 3:  line_windows(3, 4, 1)   -> [(1, 3)]
    """
    raise NotImplementedError


# ─────────────────────────────────────────────────────────────────────
# Problem 2 · make_chunks                                        (easy)
# ─────────────────────────────────────────────────────────────────────
def make_chunks(path: str, text: str, size: int, overlap: int) -> list[dict]:
    """
    Cut a file into chunks using line_windows(). Lines come from text.splitlines().
    Each chunk is a dict with exactly these keys:
        "path"        the file path
        "start_line"  first line (1-based)
        "end_line"    last line (inclusive)
        "text"        those lines joined with "\\n"

    Example:
        make_chunks("a.py", "l1\\nl2\\nl3\\n", size=2, overlap=0)
        -> [{"path": "a.py", "start_line": 1, "end_line": 2, "text": "l1\\nl2"},
            {"path": "a.py", "start_line": 3, "end_line": 3, "text": "l3"}]
    """
    raise NotImplementedError


# ─────────────────────────────────────────────────────────────────────
# Problem 3 · find_chunks                                        (easy)
# ─────────────────────────────────────────────────────────────────────
def find_chunks(chunks: list[dict], path: str, line: int) -> list[dict]:
    """
    Return every chunk from `path` whose line range contains `line`, in their original order.
    Because of overlap, a line can be in more than one chunk.

    Example:
        chunks for lines (1-4), (4-7), (7-10) of "a.py"
        find_chunks(chunks, "a.py", 4)  -> the first two chunks
        find_chunks(chunks, "b.py", 4)  -> []
    """
    raise NotImplementedError
