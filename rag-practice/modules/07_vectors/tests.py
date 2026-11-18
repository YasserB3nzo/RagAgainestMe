from checks import expect, expect_close, expect_raises

PROBLEMS = [
    ("dot", "dot product"),
    ("norm", "vector length"),
    ("normalize", "scale to length 1"),
    ("cosine", "cosine similarity"),
    ("mean_pool", "average several vectors"),
]

CAT, KITTEN, CAR = [0.9, 0.6, 0.0], [0.8, 0.9, 0.0], [0.0, 0.1, 0.9]


def test_dot__example(ex):
    expect_close(ex.dot([1, 2, 3], [4, 5, 6]), 32, "dot([1, 2, 3], [4, 5, 6])")


def test_dot__cat_kitten(ex):
    expect_close(ex.dot(CAT, KITTEN), 1.26, "dot(cat, kitten)")


def test_dot__length_mismatch(ex):
    expect_raises(ValueError, ex.dot, [1, 2], [1, 2, 3], what="dot of vectors with different lengths")


def test_norm__examples(ex):
    expect_close(ex.norm([3, 4]), 5.0, "norm([3, 4])")
    expect_close(ex.norm([0, 0, 0]), 0.0, "norm([0, 0, 0])")
    expect_close(ex.norm(CAT), 1.0816653826, "norm(cat)")


def test_normalize__example(ex):
    expect_close(ex.normalize([3, 4]), [0.6, 0.8], "normalize([3, 4])")


def test_normalize__has_length_one(ex):
    v = ex.normalize([2, -1, 7, 0.5])
    expect_close(sum(x * x for x in v) ** 0.5, 1.0, "length of a normalized vector")


def test_normalize__zero_vector(ex):
    expect_close(ex.normalize([0, 0]), [0, 0], "normalize([0, 0])")


def test_normalize__returns_new_list(ex):
    original = [3, 4]
    ex.normalize(original)
    expect(original, [3, 4], "the input list must not be modified")


def test_cosine__cat_kitten_car(ex):
    expect_close(ex.cosine(CAT, KITTEN), 0.9673722, "cosine(cat, kitten)")
    expect_close(ex.cosine(CAT, CAR), 0.0612564, "cosine(cat, car)")


def test_cosine__direction_not_length(ex):
    expect_close(ex.cosine([1, 2], [10, 20]), 1.0, "cosine([1, 2], [10, 20]): same direction")
    expect_close(ex.cosine([1, 0], [-1, 0]), -1.0, "cosine([1, 0], [-1, 0]): opposite")
    expect_close(ex.cosine([1, 0], [0, 5]), 0.0, "cosine([1, 0], [0, 5]): perpendicular")


def test_cosine__zero_vector(ex):
    expect_close(ex.cosine([0, 0], [1, 1]), 0.0, "cosine with a zero vector")


def test_cosine__length_mismatch(ex):
    expect_raises(ValueError, ex.cosine, [1, 2], [1, 2, 3], what="cosine of vectors with different lengths")


def test_mean_pool__example(ex):
    expect_close(ex.mean_pool([[1, 2], [3, 4], [5, 0]]), [3.0, 2.0], "mean_pool([[1, 2], [3, 4], [5, 0]])")


def test_mean_pool__single(ex):
    expect_close(ex.mean_pool([[0.5, -1]]), [0.5, -1.0], "mean_pool([[0.5, -1]])")


def test_mean_pool__errors(ex):
    expect_raises(ValueError, ex.mean_pool, [], what="mean_pool([])")
    expect_raises(ValueError, ex.mean_pool, [[1, 2], [1]], what="mean_pool with different lengths")
