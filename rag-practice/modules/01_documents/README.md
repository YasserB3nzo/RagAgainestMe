# Module 01 · Files, documents & metadata

## Where this fits

Before anything gets embedded, your system has to decide **which files to read** and wrap each one
in a **document**: the text plus facts about it (its path, the commit it came from, its language).
Those facts are called **metadata**.

Metadata is what makes citations possible later. An answer that says "see `auth.py`, lines 4–6 at
commit `a1b2c3d`" is built entirely from metadata you attach here.

Build plan link: **step 04** (register a repository, skip binaries and dependency folders) and
**step 05** (validated document models).

## Ideas to know

- **Eligible files**: your assistant indexes Python and Markdown. Folders like `.git`, `node_modules`,
  `__pycache__` and virtual environments are noise. Indexing them wastes time and pollutes search.
- **A document** is a plain dict here. In your real project it becomes a Pydantic model.
- **Filtering by metadata** is how you later say "search only commit `a1b2c3d`" so two versions of
  the same repository never get mixed.

## Python you'll need

```python
"docs/guide.md".endswith((".py", ".md"))   # endswith accepts a tuple of options
"a/b/c.py".split("/")                      # ['a', 'b', 'c.py']
any(x > 3 for x in [1, 5])                 # True if at least one item matches
"Hello".lower()                            # 'hello'
"a\nb\n".splitlines()                      # ['a', 'b']

def f(**conditions):                       # collects keyword arguments into a dict
    return conditions
f(commit="a1", language="python")          # {'commit': 'a1', 'language': 'python'}

for key, value in conditions.items(): ...  # loop over a dict's pairs
counts.get(key, 0)                         # value for key, or 0 if missing
```

## In the real project you'll call

- `pathlib.Path(repo).rglob("*")` to walk every file in a folder
- `git rev-parse HEAD` (via `subprocess`) to read the current commit
- Pydantic `BaseModel` to validate each document

## Problems

1. `is_eligible`: should this file be indexed?
2. `make_document`: wrap a file into a document dict
3. `filter_documents`: keep documents whose metadata matches
4. `count_by`: count documents per metadata value
