"""
Module 07 · Vector math & cosine similarity

    Read the guide:   python rag.py learn 7
    Run the tests:    python rag.py test 7
    Get a hint:       python rag.py hint 7 <problem>

Replace each `raise NotImplementedError` with your solution.
"""
import math


# ─────────────────────────────────────────────────────────────────────
# Problem 1 · dot                                                (easy)
# ─────────────────────────────────────────────────────────────────────
def dot(a: list[float], b: list[float]) -> float:
    """
    Return the dot product of a and b.
    Raise ValueError if they have different lengths.

    Example:  dot([1, 2, 3], [4, 5, 6])  -> 32   (4 + 10 + 18)
    """
    raise NotImplementedError


# ─────────────────────────────────────────────────────────────────────
# Problem 2 · norm                                               (easy)
# ─────────────────────────────────────────────────────────────────────
def norm(v: list[float]) -> float:
    """
    Return the length (Euclidean norm) of v.

    Example:  norm([3, 4])  -> 5.0
    """
    raise NotImplementedError


# ─────────────────────────────────────────────────────────────────────
# Problem 3 · normalize                                          (easy)
# ─────────────────────────────────────────────────────────────────────
def normalize(v: list[float]) -> list[float]:
    """
    Return a NEW list: v scaled to length 1 (each number divided by the norm).
    A zero vector is returned unchanged (as a new list).

    Example 1:  normalize([3, 4])   -> [0.6, 0.8]
    Example 2:  normalize([0, 0])   -> [0, 0]
    """
    raise NotImplementedError


# ─────────────────────────────────────────────────────────────────────
# Problem 4 · cosine                                             (easy)
# ─────────────────────────────────────────────────────────────────────
def cosine(a: list[float], b: list[float]) -> float:
    """
    Return the cosine similarity of a and b.
    Return 0.0 if either vector has length 0.
    Raise ValueError if they have different lengths.

    Example 1:  cosine([0.9, 0.6, 0.0], [0.8, 0.9, 0.0])  -> 0.9673...   (cat vs kitten)
    Example 2:  cosine([0.9, 0.6, 0.0], [0.0, 0.1, 0.9])  -> 0.0612...   (cat vs car)
    Example 3:  cosine([1, 0], [-1, 0])                    -> -1.0
    """
    raise NotImplementedError


# ─────────────────────────────────────────────────────────────────────
# Problem 5 · mean_pool                                          (easy)
# ─────────────────────────────────────────────────────────────────────
def mean_pool(vectors: list[list[float]]) -> list[float]:
    """
    Average several vectors position by position (this is "pooling" in an embedding model:
    many token vectors -> one vector for the whole text).
    Raise ValueError if the list is empty or the vectors have different lengths.

    Example:  mean_pool([[1, 2], [3, 4], [5, 0]])  -> [3.0, 2.0]
    """
    raise NotImplementedError
