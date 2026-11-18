from checks import expect, expect_close

PROBLEMS = [
    ("overlap_score", "the toy cross-scorer"),
    ("rerank", "re-sort candidates with any scorer"),
    ("rank_changes", "compare rankings before and after"),
]


def test_overlap_score__example(ex):
    expect_close(ex.overlap_score(["new", "employees", "vacation", "days"],
                                  ["new", "employees", "receive", "22", "days", "days"]),
                 0.6708204, "overlap_score(docstring example)")


def test_overlap_score__identical_and_disjoint(ex):
    expect_close(ex.overlap_score(["a", "b"], ["b", "a"]), 1.0, "same tokens")
    expect_close(ex.overlap_score(["a", "b"], ["c"]), 0.0, "no shared tokens")


def test_overlap_score__empty(ex):
    expect_close(ex.overlap_score([], ["a"]), 0.0, "empty query")
    expect_close(ex.overlap_score(["a"], []), 0.0, "empty chunk")


def test_overlap_score__uses_sets(ex):
    expect_close(ex.overlap_score(["a", "a", "a"], ["a", "b"]), 0.7071068, "repeated tokens count once")


CANDIDATES = [
    {"id": "a", "text": "xx"},
    {"id": "b", "text": "xxxx"},
    {"id": "c", "text": "xxx"},
    {"id": "d", "text": "yyyy"},
]


def _by_length(q, text):
    return len(text)


def test_rerank__docstring_example(ex):
    got = ex.rerank("q", CANDIDATES[:2], _by_length, keep=1)
    expect(got, [{"id": "b", "text": "xxxx", "rerank_score": 4}], "rerank(docstring example)")


def test_rerank__order_and_ties(ex):
    got = ex.rerank("q", CANDIDATES, _by_length, keep=4)
    expect([c["id"] for c in got], ["b", "d", "c", "a"], "ids after rerank (b and d tie: original order kept)")


def test_rerank__passes_query(ex):
    seen = []
    ex.rerank("my question", CANDIDATES[:1], lambda q, t: seen.append((q, t)) or 0.0, keep=1)
    expect(seen, [("my question", "xx")], "score_fn must receive (query, candidate text)")


def test_rerank__does_not_modify_input(ex):
    original = [dict(c) for c in CANDIDATES]
    ex.rerank("q", CANDIDATES, _by_length, keep=2)
    expect(CANDIDATES, original, "input candidates must stay unchanged")


def test_rank_changes__example(ex):
    expect(ex.rank_changes(["a", "b", "c"], ["c", "a", "z"]), {"c": (3, 1), "a": (1, 2), "z": (None, 3)},
           'rank_changes(["a", "b", "c"], ["c", "a", "z"])')


def test_rank_changes__empty(ex):
    expect(ex.rank_changes(["a"], []), {}, 'rank_changes(["a"], [])')
