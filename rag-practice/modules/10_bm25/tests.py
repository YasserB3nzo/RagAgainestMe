from checks import expect, expect_close

PROBLEMS = [
    ("term_frequencies", "count terms in one document"),
    ("document_frequencies", "count documents per term"),
    ("idf", "rare terms are worth more"),
    ("bm25_scores", "score every document"),
    ("top_k", "best results first"),
]

DOCS = [["hash", "password", "salt"],
        ["cart", "total", "price", "tax"],
        ["password", "reset", "email", "password"]]
DF = {"hash": 1, "password": 2, "salt": 1, "cart": 1, "total": 1, "price": 1, "tax": 1, "reset": 1, "email": 1}


def test_term_frequencies__example(ex):
    expect(ex.term_frequencies(["password", "salt", "password"]), {"password": 2, "salt": 1},
           'term_frequencies(["password", "salt", "password"])')


def test_term_frequencies__empty(ex):
    expect(ex.term_frequencies([]), {}, "term_frequencies([])")


def test_document_frequencies__example(ex):
    expect(ex.document_frequencies([["a", "b", "a"], ["b"], ["c"]]), {"a": 1, "b": 2, "c": 1},
           'document_frequencies([["a", "b", "a"], ["b"], ["c"]])')


def test_document_frequencies__corpus(ex):
    expect(ex.document_frequencies(DOCS), DF, "document_frequencies(DOCS)")


def test_idf__examples(ex):
    expect_close(ex.idf("password", DF, 3), 0.4700036292, 'idf("password", DF, 3)')
    expect_close(ex.idf("salt", DF, 3), 0.9808292530, 'idf("salt", DF, 3)')


def test_idf__unknown_term(ex):
    expect_close(ex.idf("banana", DF, 3), 2.0794415417, 'idf("banana", DF, 3): a term in no document')


def test_idf__rare_beats_common(ex):
    expect(ex.idf("salt", DF, 3) > ex.idf("password", DF, 3), True, "a rarer term must get a higher idf")


def test_bm25_scores__example(ex):
    expect_close(ex.bm25_scores(["password", "salt"], DOCS), [1.5801150203, 0.0, 0.6523709680],
                 'bm25_scores(["password", "salt"], DOCS)')


def test_bm25_scores__distinct_query_terms(ex):
    expect_close(ex.bm25_scores(["password", "password"], DOCS), [0.5118851408, 0.0, 0.6523709680],
                 'bm25_scores(["password", "password"], DOCS): repeated query term counts once')


def test_bm25_scores__custom_parameters(ex):
    expect_close(ex.bm25_scores(["hash"], DOCS, k1=1.2, b=0.0), [0.9808292530, 0.0, 0.0],
                 'bm25_scores(["hash"], DOCS, k1=1.2, b=0.0)')


def test_bm25_scores__edge_cases(ex):
    expect(ex.bm25_scores(["x"], []), [], 'bm25_scores(["x"], [])')
    expect_close(ex.bm25_scores(["x"], [[], []]), [0.0, 0.0], 'bm25_scores(["x"], [[], []])')
    expect_close(ex.bm25_scores([], DOCS), [0.0, 0.0, 0.0], "bm25_scores([], DOCS)")


def test_top_k__example(ex):
    expect(ex.top_k([0.2, 0.0, 1.5, 0.2], 3), [(2, 1.5), (0, 0.2), (3, 0.2)], "top_k([0.2, 0.0, 1.5, 0.2], 3)")


def test_top_k__skips_zero_and_limits(ex):
    expect(ex.top_k([0.0, 3.0, 0.0, 1.0], 1), [(1, 3.0)], "top_k([0.0, 3.0, 0.0, 1.0], 1)")
    expect(ex.top_k([0.0, 0.0], 5), [], "top_k([0.0, 0.0], 5)")
