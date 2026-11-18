"""
Module 01 · Files, documents & metadata

    Read the guide:   python rag.py learn 1
    Run the tests:    python rag.py test 1
    Get a hint:       python rag.py hint 1 <problem>

Replace each `raise NotImplementedError` with your solution.
"""

IGNORED_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}


# ─────────────────────────────────────────────────────────────────────
# Problem 1 · is_eligible                                        (easy)
# ─────────────────────────────────────────────────────────────────────
SKIP_DIRS = {"node_modules", ".venv", "venv", "build", "dist", "__pycache__", "vendor", "third_party",".git"}

def is_eligible(path: str) -> bool:
    list_of = path.split("/")
    for folder in list_of:
        if folder in SKIP_DIRS:
            return False
        
    file_name = list_of[-1]
    if file_name.lower().endswith((".py", ".md")):
      return True

    return False

    """
    Return True if the file at `path` should be indexed.
   
    A file is eligible when:
      - its name ends with ".py" or ".md" (any letter case: ".MD" counts), and
      - none of the folders in its path is in IGNORED_DIRS.

    Paths always use "/" as the separator.

    Example 1:  is_eligible("src/auth.py")                   -> True
    Example 2:  is_eligible("docs/Guide.MD")                 -> True
    Example 3:  is_eligible("logo.png")                      -> False
    Example 4:  is_eligible("node_modules/lib/index.py")     -> False
    Example 5:  is_eligible("src/venv_helpers.py")           -> True   (a file name, not a folder)
    """
    raise NotImplementedError


# ─────────────────────────────────────────────────────────────────────
# Problem 2 · make_document                                      (easy)
# ─────────────────────────────────────────────────────────────────────
def make_document(path: str, text: str, commit: str) -> dict:
    #l = path.split("/")
    if path.lower().endswith((".py", ".md")):
        
    
    
    
    
    
    
    
    
    raise NotImplementedError


# ─────────────────────────────────────────────────────────────────────
# Problem 3 · filter_documents                                   (easy)
# ─────────────────────────────────────────────────────────────────────
def filter_documents(docs: list[dict], **conditions) -> list[dict]:
    """
    Return the documents where EVERY condition matches: doc[key] == value.
    Keep the original order. A document missing a key does not match.
    With no conditions, return all documents.

    Example:
        filter_documents(docs, commit="a1b2c3d", language="python")
        -> only the Python documents from commit a1b2c3d
    """
    raise NotImplementedError


# ─────────────────────────────────────────────────────────────────────
# Problem 4 · count_by                                           (easy)
# ─────────────────────────────────────────────────────────────────────
def count_by(docs: list[dict], key: str) -> dict:
    """
    Count how many documents have each value of `key`.
    Documents without that key are counted under "unknown".

    Example:
        count_by(docs, "language") -> {"python": 2, "markdown": 1}
    """
    raise NotImplementedError
