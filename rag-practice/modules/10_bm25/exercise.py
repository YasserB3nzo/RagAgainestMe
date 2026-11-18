"""
Module 10 · BM25 keyword search

    Read the guide:   python rag.py learn 10
    Run the tests:    python rag.py test 10
    Get a hint:       python rag.py hint 10 <problem>

Replace each `raise NotImplementedError` with your solution.
"""
import math
from collections import Counter  # noqa: F401


# ─────────────────────────────────────────────────────────────────────
# Problem 1 · term_frequencies                                   (easy)
# ─────────────────────────────────────────────────────────────────────
def term_frequencies(tokens: list[str]) -> dict[str, int]:
    """
    Count how many times each token appears.

    Example:  term_frequencies(["password", "salt", "password"])  -> {"password": 2, "salt": 1}
    """
    raise NotImplementedError


# ─────────────────────────────────────────────────────────────────────
# Problem 2 · document_frequencies                               (easy)
# ─────────────────────────────────────────────────────────────────────
def document_frequencies(docs_tokens: list[list[str]]) -> dict[str, int]:
    """
    For each term, count in how many documents it appears (at least once).
    A term repeated inside one document still counts once for that document.

    Example:
        document_frequencies([["a", "b", "a"], ["b"], ["c"]])  -> {"a": 1, "b": 2, "c": 1}
    """
    raise NotImplementedError


# ─────────────────────────────────────────────────────────────────────
# Problem 3 · idf                                                (easy)
# ─────────────────────────────────────────────────────────────────────
def idf(term: str, df: dict[str, int], n_docs: int) -> float:
    """
    BM25 inverse document frequency:
        ln( (n_docs - n + 0.5) / (n + 0.5) + 1 )      where n = df.get(term, 0)

    Example (3 documents, "password" in 2 of them):
        idf("password", {"password": 2, "salt": 1}, 3)  -> 0.4700...
        idf("salt", {"password": 2, "salt": 1}, 3)      -> 0.9808...
    """
    raise NotImplementedError


# ─────────────────────────────────────────────────────────────────────
# Problem 4 · bm25_scores                                      (medium)
# ─────────────────────────────────────────────────────────────────────
def bm25_scores(query_tokens: list[str], docs_tokens: list[list[str]],
                k1: float = 1.5, b: float = 0.75) -> list[float]:
    """
    Return one BM25 score per document, in the same order as docs_tokens (formula in the guide).
      - use each DISTINCT query term once
      - return [] when there are no documents
      - if every document is empty (avgdl == 0), return 0.0 for each document

    Example:
        docs = [["hash", "password", "salt"],
                ["cart", "total", "price", "tax"],
                ["password", "reset", "email", "password"]]
        bm25_scores(["password", "salt"], docs)  -> [1.5801..., 0.0, 0.6523...]
    """
    raise NotImplementedError


# ─────────────────────────────────────────────────────────────────────
# Problem 5 · top_k                                              (easy)
# ─────────────────────────────────────────────────────────────────────
def top_k(scores: list[float], k: int) -> list[tuple[int, float]]:
    """
    Return up to k (index, score) pairs with the highest scores, best first.
    Skip scores <= 0 (those documents share no term with the query).
    Break ties by the smaller index.

    Example:  top_k([0.2, 0.0, 1.5, 0.2], 3)  -> [(2, 1.5), (0, 0.2), (3, 0.2)]
    """
    raise NotImplementedError
