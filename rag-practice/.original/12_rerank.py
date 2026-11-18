"""
Module 12 · Reranking

    Read the guide:   python rag.py learn 12
    Run the tests:    python rag.py test 12
    Get a hint:       python rag.py hint 12 <problem>

Replace each `raise NotImplementedError` with your solution.
"""
import math
from typing import Callable


# ─────────────────────────────────────────────────────────────────────
# Problem 1 · overlap_score                                      (easy)
# ─────────────────────────────────────────────────────────────────────
def overlap_score(query_tokens: list[str], chunk_tokens: list[str]) -> float:
    """
    Otsuka–Ochiai coefficient on the SETS of tokens:
        |A ∩ B| / sqrt(|A| × |B|)
    Return 0.0 if either set is empty.

    Example:
        overlap_score(["new", "employees", "vacation", "days"],
                      ["new", "employees", "receive", "22", "days", "days"])
        -> 3 / sqrt(4 * 5) = 0.6708...
    """
    raise NotImplementedError


# ─────────────────────────────────────────────────────────────────────
# Problem 2 · rerank                                             (easy)
# ─────────────────────────────────────────────────────────────────────
def rerank(query: str, candidates: list[dict], score_fn: Callable[[str, str], float],
           keep: int) -> list[dict]:
    """
    Score every candidate with score_fn(query, candidate["text"]).
    Return the best `keep` candidates, highest score first, as NEW dicts:
    a copy of each candidate plus a "rerank_score" key.
    Candidates with equal scores keep their original order. Do not modify the input dicts.

    Example:
        rerank("q", [{"id": "a", "text": "xx"}, {"id": "b", "text": "xxxx"}],
               score_fn=lambda q, text: len(text), keep=1)
        -> [{"id": "b", "text": "xxxx", "rerank_score": 4}]
    """
    raise NotImplementedError


# ─────────────────────────────────────────────────────────────────────
# Problem 3 · rank_changes                                       (easy)
# ─────────────────────────────────────────────────────────────────────
def rank_changes(before: list[str], after: list[str]) -> dict[str, tuple]:
    """
    For every id in `after`, return (old_rank, new_rank), both 1-based.
    old_rank is None if the id wasn't in `before`.

    Example:
        rank_changes(["a", "b", "c"], ["c", "a", "z"])
        -> {"c": (3, 1), "a": (1, 2), "z": (None, 3)}
    """
    raise NotImplementedError
