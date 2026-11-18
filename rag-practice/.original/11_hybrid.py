"""
Module 11 · Hybrid search: fusion & deduplication

    Read the guide:   python rag.py learn 11
    Run the tests:    python rag.py test 11
    Get a hint:       python rag.py hint 11 <problem>

Replace each `raise NotImplementedError` with your solution.
"""


# ─────────────────────────────────────────────────────────────────────
# Problem 1 · ranking                                            (easy)
# ─────────────────────────────────────────────────────────────────────
def ranking(scores: dict[str, float]) -> list[str]:
    """
    Return the ids ordered by score, highest first. Break ties by id (alphabetical).

    Example:  ranking({"a": 0.2, "b": 0.9, "c": 0.2})  -> ["b", "a", "c"]
    """
    raise NotImplementedError


# ─────────────────────────────────────────────────────────────────────
# Problem 2 · rrf                                                (easy)
# ─────────────────────────────────────────────────────────────────────
def rrf(rankings: list[list[str]], k: int = 60) -> list[tuple[str, float]]:
    """
    Reciprocal Rank Fusion. Each ranking is a list of ids, best first (rank 1).
    Every id gets the sum of 1 / (k + rank) over the rankings that contain it.
    Return (id, score) pairs, highest score first; break ties by id.

    Example:
        rrf([["x", "y"], ["y"]], k=1)
        x: 1/(1+1) = 0.5
        y: 1/(1+2) + 1/(1+1) = 0.8333...
        -> [("y", 0.8333...), ("x", 0.5)]
    """
    raise NotImplementedError


# ─────────────────────────────────────────────────────────────────────
# Problem 3 · min_max                                            (easy)
# ─────────────────────────────────────────────────────────────────────
def min_max(scores: dict[str, float]) -> dict[str, float]:
    """
    Rescale scores to the range 0..1:  (score - min) / (max - min).
    If every score is equal, give every id 1.0. An empty dict returns {}.

    Example:  min_max({"a": 2.0, "b": 12.0, "c": 7.0})  -> {"a": 0.0, "b": 1.0, "c": 0.5}
    """
    raise NotImplementedError


# ─────────────────────────────────────────────────────────────────────
# Problem 4 · dedupe_overlapping                                 (easy)
# ─────────────────────────────────────────────────────────────────────
def dedupe_overlapping(chunks: list[dict]) -> list[dict]:
    """
    `chunks` is ranked, best first. Keep a chunk unless it overlaps a chunk you already kept.
    Two chunks overlap when they have the same "path" AND both have line ranges
    ("start_line", "end_line", inclusive) that share at least one line.
    Chunks without "start_line" never overlap anything.

    Example:
        [auth.py 4-6, auth.py 6-9, cart.py 4-6, auth.py 10-12]
        -> [auth.py 4-6, cart.py 4-6, auth.py 10-12]     (6-9 shares line 6 with 4-6)
    """
    raise NotImplementedError
