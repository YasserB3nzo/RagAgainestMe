from checks import expect, expect_close, expect_raises

PROBLEMS = [
    ("add", "store a point"),
    ("search", "top-k by cosine similarity"),
    ("filtered_search", "search with a payload filter"),
    ("delete_where", "remove points that match"),
]


def _store(ex):
    s = ex.VectorStore()
    s.add("a", [1.0, 0.0], {"path": "auth.py", "commit": "c1"})
    s.add("b", [0.0, 1.0], {"path": "cart.py", "commit": "c1"})
    s.add("c", [1.0, 1.0], {"path": "auth.py", "commit": "c2"})
    s.add("d", [-1.0, 0.0], {"path": "README.md", "commit": "c2"})
    return s


def test_add__stores_points(ex):
    s = _store(ex)
    expect(len(s), 4, "len(store) after 4 adds")
    expect(s.points["b"]["payload"], {"path": "cart.py", "commit": "c1"}, 'store.points["b"]["payload"]')


def test_add__duplicate_id(ex):
    s = _store(ex)
    expect_raises(ValueError, s.add, "a", [0.5, 0.5], {}, what='adding id "a" twice')


def test_add__wrong_dimension(ex):
    s = _store(ex)
    expect_raises(ValueError, s.add, "e", [1.0, 0.0, 0.0], {}, what="adding a 3-number vector to a 2-number store")


def test_search__top_two(ex):
    got = _store(ex).search([1.0, 0.0], k=2)
    expect([r["id"] for r in got], ["a", "c"], "ids from search([1, 0], k=2)")
    expect_close([r["score"] for r in got], [1.0, 0.7071068], "scores from search([1, 0], k=2)")
    expect(got[0]["payload"], {"path": "auth.py", "commit": "c1"}, "payload of the best result")


def test_search__full_ranking(ex):
    got = _store(ex).search([1.0, 0.0], k=10)
    expect([r["id"] for r in got], ["a", "c", "b", "d"], "all ids, best first (k bigger than the store)")


def test_search__ties_by_id(ex):
    s = ex.VectorStore()
    for pid in ["z", "m", "a"]:
        s.add(pid, [0.0, 2.0], {})
    expect([r["id"] for r in s.search([0.0, 1.0], k=3)], ["a", "m", "z"], "equal scores sorted by id")


def test_search__empty_store(ex):
    expect(ex.VectorStore().search([1.0, 0.0], k=3), [], "search on an empty store")


def test_filtered_search__by_commit(ex):
    got = _store(ex).filtered_search([1.0, 0.0], k=5, where={"commit": "c2"})
    expect([r["id"] for r in got], ["c", "d"], 'filtered_search(where={"commit": "c2"})')


def test_filtered_search__two_conditions(ex):
    got = _store(ex).filtered_search([0.0, 1.0], k=5, where={"commit": "c1", "path": "auth.py"})
    expect([r["id"] for r in got], ["a"], 'filtered_search(where={"commit": "c1", "path": "auth.py"})')


def test_filtered_search__nothing_matches(ex):
    expect(_store(ex).filtered_search([1.0, 0.0], k=5, where={"commit": "zzz"}), [], "a filter that matches nothing")


def test_delete_where__by_path(ex):
    s = _store(ex)
    expect(s.delete_where(path="auth.py"), 2, 'delete_where(path="auth.py") return value')
    expect(sorted(s.points), ["b", "d"], "ids left after deleting auth.py")


def test_delete_where__two_conditions(ex):
    s = _store(ex)
    expect(s.delete_where(path="auth.py", commit="c2"), 1, 'delete_where(path="auth.py", commit="c2")')
    expect(sorted(s.points), ["a", "b", "d"], "ids left")


def test_delete_where__nothing(ex):
    s = _store(ex)
    expect(s.delete_where(path="nope.py"), 0, 'delete_where(path="nope.py")')
    expect(len(s), 4, "store size unchanged")
