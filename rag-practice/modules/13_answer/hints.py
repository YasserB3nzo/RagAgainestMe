HINTS = {
    "build_context": [
        "Loop with enumerate(chunks, start=1) so you get 1, 2, 3 for the evidence numbers.",
        "Write a small helper that returns the location string, with the three cases from the docstring "
        "checked in order (start_line first, then a non-empty heading_path, then just the path).",
        "Collect the blocks in a list and join them with '\\n\\n' at the end. Fill the evidence dict in "
        "the same loop.",
    ],
    "extract_citations": [
        "re.findall with a group returns only what the group matched.",
        "The pattern is a literal [, then a group made of E and one or more digits, then a literal ]. "
        "Square brackets must be escaped with a backslash.",
        "Remove duplicates while keeping order: append an id only if it isn't in your output list yet.",
    ],
    "validate_citations": [
        "Reuse extract_citations: it already gives unique IDs in order.",
        "An ID is valid when `id in evidence`.",
        "Two list comprehensions over the same extracted list, one with `in` and one with `not in`.",
    ],
    "recall_at_k": [
        "Check for an empty relevant list first.",
        "Only the first k retrieved IDs count: retrieved_ids[:k].",
        "len(set(top_k) & set(relevant)) / len(set(relevant))",
    ],
    "search_pipeline": [
        "Write the steps from the docstring as five comments first, then fill each one in. Load the modules "
        "once at the top: tok = module(3), chunking = module(4), ... Print intermediate results while you "
        "work (len(chunks), the first ranking...).",
        "Keep a dict id -> chunk. BM25 gives scores in chunk order; top_k gives (index, score) pairs, so "
        "map index -> chunks[index]['id']. The VectorStore search returns dicts with an 'id'. Ask for "
        "k=len(chunks) in both so the rankings are complete.",
        "rrf returns (id, score) pairs: turn them back into chunk dicts, dedupe, slice [:6]. For reranking, "
        "score_fn can be: lambda q, text: rr.overlap_score(tok.code_tokenize(q), tok.code_tokenize(text)).",
    ],
}
