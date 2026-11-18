"""Starter code for the website's playground ("Run code" button).

Problems whose docstring example is a plain call get `print(<that call>)` automatically.
The ones below need some setup first (sample data, an object to call a method on, ...).
Keys are "<module number>/<problem name>".
"""

_DOCS = '''docs = [
    {"path": "auth.py", "commit": "a1b2c3d", "language": "python"},
    {"path": "cart.py", "commit": "a1b2c3d", "language": "python"},
    {"path": "README.md", "commit": "a1b2c3d", "language": "markdown"},
    {"path": "old.py", "commit": "0000000", "language": "python"},
    {"path": "notes"},
]
'''

_STORE = '''store = VectorStore()
store.add("a", [1.0, 0.0], {"path": "auth.py", "commit": "a1"})
store.add("b", [0.0, 1.0], {"path": "cart.py", "commit": "a1"})
store.add("c", [1.0, 1.0], {"path": "cart.py", "commit": "b2"})
'''

STARTERS = {
    "01/filter_documents": _DOCS + '\nprint(filter_documents(docs, commit="a1b2c3d", language="python"))\n',
    "01/count_by": _DOCS + '\nprint(count_by(docs, "language"))\n',
    "02/line_of_offset": 'text = "ab\\ncd"\nfor offset in range(len(text) + 1):\n'
                         '    print(offset, repr(text[offset:offset + 1]), line_of_offset(text, offset))\n',
    "02/span_to_lines": 'text = "import os\\n\\ndef f():\\n    return 1\\n"\nstart = text.index("def")\n'
                        'end = text.index("1") + 1\nprint(span_to_lines(text, start, end))\n',
    "04/find_chunks": 'chunks = [\n    {"path": "a.py", "start_line": 1, "end_line": 4},\n'
                      '    {"path": "a.py", "start_line": 4, "end_line": 7},\n'
                      '    {"path": "a.py", "start_line": 7, "end_line": 10},\n]\n'
                      'print(find_chunks(chunks, "a.py", 4))\nprint(find_chunks(chunks, "b.py", 4))\n',
    "05/section_chunks": 'markdown = """# Tiny Shop\nA small demo shop.\n\n## Run with Docker\n'
                         'Build the image, then start the container.\n\nIt listens on port 8000."""\n\n'
                         'for chunk in section_chunks(markdown, "README.md", max_chars=60):\n    print(chunk)\n',
    "08/most_similar": 'table = {"cat": [0.9, 0.6, 0], "kitten": [0.8, 0.9, 0], "puppy": [0.7, 0.9, 0], "car": [0, 0.1, 0.9]}\n'
                       'print(most_similar("cat", table, 2))\n',
    "09/add": 'store = VectorStore()\nstore.add("c1", [1.0, 0.0], {"path": "auth.py", "commit": "a1"})\n'
              'print(len(store), store.points)\n',
    "09/search": _STORE + '\nprint(store.search([1.0, 0.0], k=2))\n',
    "09/filtered_search": _STORE + '\nprint(store.filtered_search([1.0, 0.0], k=3, where={"commit": "a1"}))\n',
    "09/delete_where": _STORE + '\nprint(store.delete_where(path="cart.py", commit="a1"))\nprint(store.points)\n',
    "10/bm25_scores": 'docs = [["hash", "password", "salt"],\n        ["cart", "total", "price", "tax"],\n'
                      '        ["password", "reset", "email", "password"]]\nprint(bm25_scores(["password", "salt"], docs))\n',
    "11/dedupe_overlapping": 'chunks = [\n    {"path": "auth.py", "start_line": 4, "end_line": 6},\n'
                             '    {"path": "auth.py", "start_line": 6, "end_line": 9},\n'
                             '    {"path": "cart.py", "start_line": 4, "end_line": 6},\n'
                             '    {"path": "auth.py", "start_line": 10, "end_line": 12},\n]\n'
                             'for chunk in dedupe_overlapping(chunks):\n    print(chunk)\n',
    "13/validate_citations": 'evidence = {"E1": "chunk one", "E2": "chunk two"}\n'
                             'print(validate_citations("See [E1] and [E7].", evidence))\n',
    "13/search_pipeline": 'from data import REPO\n\nfor chunk in search_pipeline("where is login_user defined?", REPO):\n'
                          '    print(chunk["path"], chunk.get("start_line"), "|", chunk["text"][:60].replace("\\n", " "))\n',
}
