import hashlib

from checks import expect

PROBLEMS = [
    ("content_hash", "fingerprint a text"),
    ("chunk_id", "a deterministic ID for a chunk"),
    ("detect_changes", "compare two repository snapshots"),
]


def test_content_hash__known_value(ex):
    expect(ex.content_hash("hello"), "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
           'content_hash("hello")')


def test_content_hash__unicode(ex):
    expect(ex.content_hash("café 🙂"), hashlib.sha256("café 🙂".encode("utf-8")).hexdigest(),
           'content_hash("café 🙂")')


def test_content_hash__one_character_changes_everything(ex):
    a, b = ex.content_hash("def f(): return 1"), ex.content_hash("def f(): return 2")
    expect(a != b, True, "hashes of two different texts must differ")
    expect(len(a), 64, "length of a SHA-256 hex digest")


def test_chunk_id__value(ex):
    key = "tiny-shop:a1b2c3d:auth.py:4-6"
    expect(ex.chunk_id("tiny-shop", "a1b2c3d", "auth.py", 4, 6), hashlib.sha256(key.encode()).hexdigest()[:16],
           'chunk_id("tiny-shop", "a1b2c3d", "auth.py", 4, 6)')


def test_chunk_id__deterministic(ex):
    a = ex.chunk_id("r", "c1", "x.py", 1, 10)
    b = ex.chunk_id("r", "c1", "x.py", 1, 10)
    expect(a, b, "calling chunk_id twice with the same input")
    expect(len(a), 16, "length of a chunk id")


def test_chunk_id__depends_on_every_part(ex):
    base = ex.chunk_id("r", "c1", "x.py", 1, 10)
    others = [ex.chunk_id("r2", "c1", "x.py", 1, 10), ex.chunk_id("r", "c2", "x.py", 1, 10),
              ex.chunk_id("r", "c1", "y.py", 1, 10), ex.chunk_id("r", "c1", "x.py", 2, 10),
              ex.chunk_id("r", "c1", "x.py", 1, 11)]
    expect(all(o != base for o in others), True, "changing repo, commit, path or lines must change the id")


def test_detect_changes__example(ex):
    expect(ex.detect_changes({"a.py": "h1", "b.py": "h2"}, {"a.py": "h1", "b.py": "h9", "c.py": "h3"}),
           {"added": ["c.py"], "deleted": [], "changed": ["b.py"], "unchanged": ["a.py"]},
           "detect_changes(docstring example)")


def test_detect_changes__deleted_and_sorted(ex):
    old = {"z.py": "1", "m.py": "2", "a.py": "3"}
    new = {"m.py": "2"}
    expect(ex.detect_changes(old, new), {"added": [], "deleted": ["a.py", "z.py"], "changed": [], "unchanged": ["m.py"]},
           "detect_changes when two files were deleted")


def test_detect_changes__first_index(ex):
    expect(ex.detect_changes({}, {"b.py": "1", "a.py": "2"}),
           {"added": ["a.py", "b.py"], "deleted": [], "changed": [], "unchanged": []},
           "detect_changes({}, new): everything is added")
