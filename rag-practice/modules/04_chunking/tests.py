from checks import expect, expect_raises
from data import REPO

PROBLEMS = [
    ("line_windows", "compute (start, end) line ranges"),
    ("make_chunks", "cut a file into chunk dicts"),
    ("find_chunks", "which chunks contain a line?"),
]


def test_line_windows__examples(ex):
    expect(ex.line_windows(10, 4, 1), [(1, 4), (4, 7), (7, 10)], "line_windows(10, 4, 1)")
    expect(ex.line_windows(9, 4, 1), [(1, 4), (4, 7), (7, 9)], "line_windows(9, 4, 1)")
    expect(ex.line_windows(3, 4, 1), [(1, 3)], "line_windows(3, 4, 1)")


def test_line_windows__no_overlap(ex):
    expect(ex.line_windows(6, 2, 0), [(1, 2), (3, 4), (5, 6)], "line_windows(6, 2, 0)")


def test_line_windows__exact_fit(ex):
    expect(ex.line_windows(4, 4, 2), [(1, 4)], "line_windows(4, 4, 2)")


def test_line_windows__empty_file(ex):
    expect(ex.line_windows(0, 4, 1), [], "line_windows(0, 4, 1)")


def test_line_windows__bad_settings(ex):
    expect_raises(ValueError, ex.line_windows, 5, 3, 3, what="overlap == size would never move forward")
    expect_raises(ValueError, ex.line_windows, 5, 0, 0, what="size 0")
    expect_raises(ValueError, ex.line_windows, 5, 3, -1, what="negative overlap")


def test_make_chunks__docstring_example(ex):
    expect(ex.make_chunks("a.py", "l1\nl2\nl3\n", 2, 0),
           [{"path": "a.py", "start_line": 1, "end_line": 2, "text": "l1\nl2"},
            {"path": "a.py", "start_line": 3, "end_line": 3, "text": "l3"}],
           'make_chunks("a.py", "l1\\nl2\\nl3\\n", 2, 0)')


def test_make_chunks__real_file(ex):
    lines = REPO["cart.py"].splitlines()
    chunks = ex.make_chunks("cart.py", REPO["cart.py"], 5, 1)
    expect([(c["start_line"], c["end_line"]) for c in chunks], [(1, 5), (5, 9), (9, 13), (13, 14)],
           "line ranges of cart.py chunks (size 5, overlap 1)")
    expect(chunks[-1]["text"], "\n".join(lines[12:14]), "text of the last chunk")
    expect(chunks[0]["text"].splitlines()[0], lines[0], "first line of the first chunk")


def test_make_chunks__empty_text(ex):
    expect(ex.make_chunks("empty.py", "", 5, 1), [], 'make_chunks("empty.py", "", 5, 1)')


CHUNKS = [
    {"path": "a.py", "start_line": 1, "end_line": 4, "text": "..."},
    {"path": "a.py", "start_line": 4, "end_line": 7, "text": "..."},
    {"path": "a.py", "start_line": 7, "end_line": 10, "text": "..."},
    {"path": "b.py", "start_line": 1, "end_line": 4, "text": "..."},
]


def test_find_chunks__overlap_line(ex):
    expect(ex.find_chunks(CHUNKS, "a.py", 4), CHUNKS[:2], 'find_chunks(CHUNKS, "a.py", 4)')


def test_find_chunks__single(ex):
    expect(ex.find_chunks(CHUNKS, "a.py", 9), [CHUNKS[2]], 'find_chunks(CHUNKS, "a.py", 9)')
    expect(ex.find_chunks(CHUNKS, "b.py", 2), [CHUNKS[3]], 'find_chunks(CHUNKS, "b.py", 2)')


def test_find_chunks__none(ex):
    expect(ex.find_chunks(CHUNKS, "a.py", 11), [], 'find_chunks(CHUNKS, "a.py", 11)')
    expect(ex.find_chunks(CHUNKS, "c.py", 1), [], 'find_chunks(CHUNKS, "c.py", 1)')
