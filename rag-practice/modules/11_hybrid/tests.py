from checks import expect, expect_close

PROBLEMS = [
    ("ranking", "scores -> ordered ids"),
    ("rrf", "fuse several rankings"),
    ("min_max", "rescale scores to 0..1"),
    ("dedupe_overlapping", "drop overlapping chunks"),
]


def test_ranking__example(ex):
    expect(ex.ranking({"a": 0.2, "b": 0.9, "c": 0.2}), ["b", "a", "c"], 'ranking({"a": 0.2, "b": 0.9, "c": 0.2})')


def test_ranking__negative_and_empty(ex):
    expect(ex.ranking({"x": -1.0, "y": 0.0}), ["y", "x"], 'ranking({"x": -1.0, "y": 0.0})')
    expect(ex.ranking({}), [], "ranking({})")


def _check_fused(got, expected, what):
    expect([i for i, _ in got], [i for i, _ in expected], what + " (ids)")
    expect_close([s for _, s in got], [s for _, s in expected], what + " (scores)")


def test_rrf__docstring_example(ex):
    _check_fused(ex.rrf([["x", "y"], ["y"]], k=1), [("y", 0.8333333), ("x", 0.5)], 'rrf([["x", "y"], ["y"]], k=1)')


def test_rrf__default_k(ex):
    _check_fused(ex.rrf([["a", "b", "c"], ["b", "c", "d"]]),
                 [("b", 0.0325224), ("c", 0.0320020), ("a", 0.0163934), ("d", 0.0158730)],
                 'rrf([["a", "b", "c"], ["b", "c", "d"]])')


def test_rrf__ties_by_id(ex):
    _check_fused(ex.rrf([["q"], ["p"]], k=60), [("p", 1 / 61), ("q", 1 / 61)], 'rrf([["q"], ["p"]])')


def test_rrf__empty(ex):
    expect(ex.rrf([]), [], "rrf([])")


def test_min_max__example(ex):
    got = ex.min_max({"a": 2.0, "b": 12.0, "c": 7.0})
    expect(sorted(got), ["a", "b", "c"], "keys of the result")
    expect_close([got["a"], got["b"], got["c"]], [0.0, 1.0, 0.5], 'min_max({"a": 2.0, "b": 12.0, "c": 7.0})')


def test_min_max__all_equal_and_empty(ex):
    expect(ex.min_max({"a": 3.0, "b": 3.0}), {"a": 1.0, "b": 1.0}, 'min_max({"a": 3.0, "b": 3.0})')
    expect(ex.min_max({}), {}, "min_max({})")


def _c(path, s=None, e=None):
    return {"path": path, "start_line": s, "end_line": e} if s else {"path": path}


def test_dedupe_overlapping__example(ex):
    chunks = [_c("auth.py", 4, 6), _c("auth.py", 6, 9), _c("cart.py", 4, 6), _c("auth.py", 10, 12)]
    expect(ex.dedupe_overlapping(chunks), [chunks[0], chunks[2], chunks[3]], "dedupe_overlapping(docstring example)")


def test_dedupe_overlapping__contained_range(ex):
    chunks = [_c("a.py", 1, 20), _c("a.py", 5, 6), _c("a.py", 21, 22)]
    expect(ex.dedupe_overlapping(chunks), [chunks[0], chunks[2]], "a range inside a kept range is dropped")


def test_dedupe_overlapping__keeps_best_first(ex):
    chunks = [_c("a.py", 5, 8), _c("a.py", 1, 5)]
    expect(ex.dedupe_overlapping(chunks), [chunks[0]], "the first (best-ranked) chunk wins")


def test_dedupe_overlapping__chunks_without_lines(ex):
    chunks = [_c("README.md"), _c("README.md"), _c("a.py", 1, 3)]
    expect(ex.dedupe_overlapping(chunks), chunks, "chunks without line ranges are always kept")
