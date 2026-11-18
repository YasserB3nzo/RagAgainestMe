"""
Module 06 · Deterministic IDs & change detection

    Read the guide:   python rag.py learn 6
    Run the tests:    python rag.py test 6
    Get a hint:       python rag.py hint 6 <problem>

Replace each `raise NotImplementedError` with your solution.
"""
import hashlib


# ─────────────────────────────────────────────────────────────────────
# Problem 1 · content_hash                                       (easy)
# ─────────────────────────────────────────────────────────────────────
def content_hash(text: str) -> str:
    """
    Return the SHA-256 hash of the text (encoded as UTF-8) as a 64-character hex string.

    Example:
        content_hash("hello")
        -> "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
    """
    raise NotImplementedError


# ─────────────────────────────────────────────────────────────────────
# Problem 2 · chunk_id                                           (easy)
# ─────────────────────────────────────────────────────────────────────
def chunk_id(repo: str, commit: str, path: str, start_line: int, end_line: int) -> str:
    """
    Return a deterministic 16-character ID for a chunk:
    the first 16 characters of content_hash() applied to the key

        "{repo}:{commit}:{path}:{start_line}-{end_line}"

    Example:
        chunk_id("tiny-shop", "a1b2c3d", "auth.py", 4, 6)
        -> the first 16 characters of content_hash("tiny-shop:a1b2c3d:auth.py:4-6")
    """
    raise NotImplementedError


# ─────────────────────────────────────────────────────────────────────
# Problem 3 · detect_changes                                     (easy)
# ─────────────────────────────────────────────────────────────────────
def detect_changes(old: dict[str, str], new: dict[str, str]) -> dict[str, list[str]]:
    """
    `old` and `new` map file paths to content hashes (before and after an update).
    Return a dict with four keys, each a SORTED list of paths:
        "added"      in new but not in old
        "deleted"    in old but not in new
        "changed"    in both, with a different hash
        "unchanged"  in both, with the same hash

    Example:
        detect_changes({"a.py": "h1", "b.py": "h2"}, {"a.py": "h1", "b.py": "h9", "c.py": "h3"})
        -> {"added": ["c.py"], "deleted": [], "changed": ["b.py"], "unchanged": ["a.py"]}
    """
    raise NotImplementedError
