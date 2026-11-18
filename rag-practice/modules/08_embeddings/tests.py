import math

from checks import expect, expect_close, expect_raises
from data import WORD_VECTORS

PROBLEMS = [
    ("embed_text", "text -> one normalized vector"),
    ("most_similar", "closest words to a word"),
    ("batched", "split a list into batches"),
]


def _cos(a, b):
    na, nb = math.sqrt(sum(x * x for x in a)), math.sqrt(sum(x * x for x in b))
    return sum(x * y for x, y in zip(a, b)) / (na * nb) if na and nb else 0.0


def test_embed_text__docstring_example(ex):
    expect_close(ex.embed_text("Hash the password!", WORD_VECTORS), [0.9847836, 0.0, 0.0, 0.1737853],
                 'embed_text("Hash the password!", WORD_VECTORS)')


def test_embed_text__single_word(ex):
    v = WORD_VECTORS["docker"]
    length = math.sqrt(sum(x * x for x in v))
    expect_close(ex.embed_text("Docker", WORD_VECTORS), [x / length for x in v], 'embed_text("Docker", ...)')


def test_embed_text__unknown_words(ex):
    expect_close(ex.embed_text("the weather is nice", WORD_VECTORS), [0.0, 0.0, 0.0, 0.0],
                 "embed_text with no known words")
    expect_close(ex.embed_text("", WORD_VECTORS), [0.0, 0.0, 0.0, 0.0], 'embed_text("")')


def test_embed_text__meaning_beats_wording(ex):
    q = ex.embed_text("how are passwords hashed", WORD_VECTORS)
    good = ex.embed_text("Passwords are never stored in plain text. They are hashed with a salt.", WORD_VECTORS)
    bad = ex.embed_text("Build the image, then start the container with docker compose up.", WORD_VECTORS)
    expect(_cos(q, good) > 0.95, True, "the password question should be very close to the security paragraph")
    expect(_cos(q, good) > _cos(q, bad), True, "the security paragraph should beat the docker paragraph")


TABLE = {"cat": [0.9, 0.6, 0.0], "kitten": [0.8, 0.9, 0.0], "puppy": [0.7, 0.9, 0.0], "car": [0.0, 0.1, 0.9]}


def test_most_similar__example(ex):
    expect(ex.most_similar("cat", TABLE, 2), ["kitten", "puppy"], 'most_similar("cat", TABLE, 2)')


def test_most_similar__excludes_itself(ex):
    expect(ex.most_similar("car", TABLE, 3)[0] != "car", True, "a word must not be its own neighbour")
    expect(len(ex.most_similar("car", TABLE, 3)), 3, "number of results")


def test_most_similar__ties_alphabetical(ex):
    expect(ex.most_similar("docker", WORD_VECTORS, 3), ["deploy", "install", "pip"],
           'most_similar("docker", WORD_VECTORS, 3): four words tie at 1.0')


def test_most_similar__unknown_word(ex):
    expect_raises(ValueError, ex.most_similar, "banana", TABLE, 2, what='most_similar("banana", ...)')


def test_batched__example(ex):
    expect(ex.batched([1, 2, 3, 4, 5], 2), [[1, 2], [3, 4], [5]], "batched([1, 2, 3, 4, 5], 2)")


def test_batched__exact_and_empty(ex):
    expect(ex.batched(["a", "b", "c", "d"], 2), [["a", "b"], ["c", "d"]], 'batched(["a","b","c","d"], 2)')
    expect(ex.batched([], 3), [], "batched([], 3)")
    expect(ex.batched([1], 10), [[1]], "batched([1], 10)")


def test_batched__bad_size(ex):
    expect_raises(ValueError, ex.batched, [1, 2], 0, what="batched([1, 2], 0)")
