HINTS = {
    "is_eligible": [
        "There are two separate checks: the extension, and the folders. The file is eligible only if both pass.",
        "For the extension, lowercase the path first, then use endswith with a tuple of the two allowed endings.",
        "For the folders, split the path on '/'. Everything except the LAST piece is a folder name; "
        "the last piece is the file name. Check whether any folder name is in IGNORED_DIRS.",
    ],
    "make_document": [
        "Build and return one dict literal. Four keys are copied straight from the arguments; only "
        "'language' and 'n_lines' need a little work.",
        "For 'language', lowercase the path and check what it ends with (if / elif / else).",
        "For 'n_lines', try str.splitlines() on the three examples in the docstring and look at the length "
        "of what it returns.",
    ],
    "filter_documents": [
        "conditions is a normal dict, for example {'commit': 'a1', 'language': 'python'}.",
        "Loop over the documents. For each one, decide 'does it match every condition?' and keep it if yes.",
        "doc.get(key) returns None when the key is missing, so a missing key never equals the wanted value. "
        "all(...) over conditions.items() answers 'does every condition match?'.",
    ],
    "count_by": [
        "Start with an empty dict and add 1 to the right entry for each document.",
        "doc.get(key, 'unknown') gives you the value to count, with 'unknown' when the key is missing.",
        "counts[value] = counts.get(value, 0) + 1 increases a count even the first time you see a value. "
        "(collections.Counter also works if you know it.)",
    ],
}
