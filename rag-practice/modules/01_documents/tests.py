from checks import expect

PROBLEMS = [
    ("is_eligible", "should this file be indexed?"),
    ("make_document", "wrap a file into a document"),
    ("filter_documents", "keep documents that match"),
    ("count_by", "count documents per value"),
]


def test_is_eligible__python_file(ex):
    expect(ex.is_eligible("src/auth.py"), True, 'is_eligible("src/auth.py")')


def test_is_eligible__markdown_any_case(ex):
    expect(ex.is_eligible("docs/Guide.MD"), True, 'is_eligible("docs/Guide.MD")')


def test_is_eligible__other_extensions(ex):
    expect(ex.is_eligible("logo.png"), False, 'is_eligible("logo.png")')
    expect(ex.is_eligible("notes.pyc"), False, 'is_eligible("notes.pyc")')
    expect(ex.is_eligible("python"), False, 'is_eligible("python")')


def test_is_eligible__ignored_folders(ex):
    expect(ex.is_eligible("node_modules/lib/index.py"), False, 'is_eligible("node_modules/lib/index.py")')
    expect(ex.is_eligible("app/.venv/site.py"), False, 'is_eligible("app/.venv/site.py")')
    expect(ex.is_eligible(".git/hooks/pre_commit.py"), False, 'is_eligible(".git/hooks/pre_commit.py")')


def test_is_eligible__name_is_not_a_folder(ex):
    expect(ex.is_eligible("src/venv_helpers.py"), True, 'is_eligible("src/venv_helpers.py")')
    expect(ex.is_eligible("build.md"), True, 'is_eligible("build.md")')


def test_make_document__python(ex):
    expect(ex.make_document("auth.py", "import os\n", "a1b2c3d"),
           {"path": "auth.py", "text": "import os\n", "commit": "a1b2c3d", "language": "python", "n_lines": 1},
           'make_document("auth.py", "import os\\n", "a1b2c3d")')


def test_make_document__markdown_and_unknown(ex):
    expect(ex.make_document("README.MD", "# Hi", "c1")["language"], "markdown", "language of README.MD")
    expect(ex.make_document("data.json", "{}", "c1")["language"], "unknown", "language of data.json")


def test_make_document__line_counts(ex):
    expect(ex.make_document("a.py", "", "c")["n_lines"], 0, 'n_lines for ""')
    expect(ex.make_document("a.py", "a\nb", "c")["n_lines"], 2, 'n_lines for "a\\nb"')
    expect(ex.make_document("a.py", "a\nb\n", "c")["n_lines"], 2, 'n_lines for "a\\nb\\n"')
    expect(ex.make_document("a.py", "a\n\nb\n", "c")["n_lines"], 3, 'n_lines for "a\\n\\nb\\n"')


def test_make_document__keeps_text_unchanged(ex):
    text = "  def f():\n\treturn 1  \n"
    expect(ex.make_document("a.py", text, "c")["text"], text, "text must not be modified")


DOCS = [
    {"path": "auth.py", "commit": "a1", "language": "python"},
    {"path": "README.md", "commit": "a1", "language": "markdown"},
    {"path": "auth.py", "commit": "b2", "language": "python"},
    {"path": "notes.txt", "commit": "b2"},
]


def test_filter_documents__one_condition(ex):
    expect([d["path"] for d in ex.filter_documents(DOCS, commit="a1")], ["auth.py", "README.md"],
           'paths from filter_documents(DOCS, commit="a1")')


def test_filter_documents__all_conditions_must_match(ex):
    got = ex.filter_documents(DOCS, commit="b2", language="python")
    expect(got, [DOCS[2]], 'filter_documents(DOCS, commit="b2", language="python")')


def test_filter_documents__missing_key_does_not_match(ex):
    got = ex.filter_documents(DOCS, language="markdown")
    expect(got, [DOCS[1]], 'filter_documents(DOCS, language="markdown")')


def test_filter_documents__no_conditions(ex):
    expect(ex.filter_documents(DOCS), DOCS, "filter_documents(DOCS) with no conditions")


def test_count_by__language(ex):
    expect(ex.count_by(DOCS, "language"), {"python": 2, "markdown": 1, "unknown": 1}, 'count_by(DOCS, "language")')


def test_count_by__commit(ex):
    expect(ex.count_by(DOCS, "commit"), {"a1": 2, "b2": 2}, 'count_by(DOCS, "commit")')


def test_count_by__empty(ex):
    expect(ex.count_by([], "commit"), {}, 'count_by([], "commit")')
