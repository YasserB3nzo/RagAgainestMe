from checks import expect, expect_close, expect_raises
from data import QUESTIONS, REPO

PROBLEMS = [
    ("build_context", "numbered evidence blocks"),
    ("extract_citations", "find [E1]-style IDs"),
    ("validate_citations", "valid vs invented citations"),
    ("recall_at_k", "measure retrieval"),
    ("search_pipeline", "capstone: the whole retriever"),
]

CODE = {"path": "auth.py", "start_line": 4, "end_line": 6, "text": "def hash_password(...):\n    ..."}
DOC = {"path": "README.md", "heading_path": ["Tiny Shop", "Security"], "text": "Passwords are hashed."}
PLAIN = {"path": "notes.md", "heading_path": [], "text": "loose text"}


def test_build_context__single_code_chunk(ex):
    context, evidence = ex.build_context([CODE])
    expect(context, "[E1] auth.py:4-6\ndef hash_password(...):\n    ...", "context for one code chunk")
    expect(evidence, {"E1": CODE}, "evidence for one code chunk")


def test_build_context__three_kinds(ex):
    context, evidence = ex.build_context([CODE, DOC, PLAIN])
    expect(context,
           "[E1] auth.py:4-6\ndef hash_password(...):\n    ...\n\n"
           "[E2] README.md > Tiny Shop > Security\nPasswords are hashed.\n\n"
           "[E3] notes.md\nloose text",
           "context for a code chunk, a Markdown chunk and a plain chunk")
    expect(list(evidence), ["E1", "E2", "E3"], "evidence ids")
    expect(evidence["E2"], DOC, 'evidence["E2"]')


def test_build_context__empty(ex):
    expect(ex.build_context([]), ("", {}), "build_context([])")


def test_extract_citations__example(ex):
    expect(ex.extract_citations("Hashed with SHA-256 [E2]. Salted too [E1][E2]."), ["E2", "E1"],
           "extract_citations(docstring example)")


def test_extract_citations__multi_digit_and_noise(ex):
    expect(ex.extract_citations("See [E12], not E3 or [e4] or [X1]."), ["E12"], "only [E<number>] counts")
    expect(ex.extract_citations("No sources."), [], "an answer without citations")


def test_validate_citations__example(ex):
    expect(ex.validate_citations("See [E1] and [E7].", {"E1": CODE, "E2": DOC}), {"valid": ["E1"], "invalid": ["E7"]},
           "validate_citations(docstring example)")


def test_validate_citations__order_and_duplicates(ex):
    expect(ex.validate_citations("[E9] [E2] [E1] [E9]", {"E1": CODE, "E2": DOC}),
           {"valid": ["E2", "E1"], "invalid": ["E9"]}, "order of first appearance, no duplicates")


def test_recall_at_k__example(ex):
    expect_close(ex.recall_at_k(["c4", "c1", "c9", "c2"], ["c1", "c2"], 3), 0.5, "recall_at_k(docstring example)")


def test_recall_at_k__full_and_zero(ex):
    expect_close(ex.recall_at_k(["c4", "c1", "c9", "c2"], ["c1", "c2"], 4), 1.0, "k = 4 finds both")
    expect_close(ex.recall_at_k(["c4"], ["c1"], 5), 0.0, "nothing relevant retrieved")


def test_recall_at_k__no_relevant(ex):
    expect_raises(ValueError, ex.recall_at_k, ["c1"], [], 3, what="recall with no relevant ids")


def test_search_pipeline__returns_chunks(ex):
    got = ex.search_pipeline(QUESTIONS[0]["question"], REPO, k=3)
    expect(isinstance(got, list) and 1 <= len(got) <= 3, True, "search_pipeline returns a list of at most k chunks")
    expect(all("path" in c and "text" in c for c in got), True, 'every result keeps "path" and "text"')


def test_search_pipeline__finds_the_right_file(ex):
    for q in QUESTIONS:
        got = ex.search_pipeline(q["question"], REPO, k=3)
        expect(got[0]["path"], q["answer_path"], f'first result for "{q["question"]}"')


def test_search_pipeline__exact_symbol(ex):
    got = ex.search_pipeline("where is login_user defined?", REPO, k=3)
    expect(got[0]["path"], "auth.py", "first result for an exact-symbol question")
    expect("login_user" in got[0]["text"], True, "the first chunk must contain login_user")
