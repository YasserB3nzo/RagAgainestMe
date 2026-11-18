HINTS = {
    "term_frequencies": [
        "You built exactly this counting pattern in module 1 (count_by).",
        "Counter from collections does it in one call.",
        "Return a plain dict: dict(Counter(tokens)).",
    ],
    "document_frequencies": [
        "Like term_frequencies, but each document may add at most 1 per term.",
        "Turn each document into a set before counting, so repeats inside one document disappear.",
        "Loop over documents, then over set(document), and add 1 to df[term].",
    ],
    "idf": [
        "Get n with df.get(term, 0) so unknown terms work.",
        "Translate the formula literally. Watch the parentheses: the + 1 is added AFTER the division.",
        "math.log(x) is the natural log (ln).",
    ],
    "bm25_scores": [
        "Prepare once, before looping over documents: N, avgdl, the df dict (problem 2). Handle the two "
        "edge cases (no documents, avgdl == 0) right after computing them.",
        "For each document: compute its term frequencies (problem 1) and its length |D|. Then loop over "
        "set(query_tokens) and add one term per query word that appears in the document.",
        "One term of the sum: idf(q, df, N) * tf * (k1 + 1) / (tf + k1 * (1 - b + b * len(doc) / avgdl)). "
        "Skip it when tf is 0.",
    ],
    "top_k": [
        "Pair every score with its index: enumerate(scores).",
        "Keep only pairs with score > 0.",
        "Sort with key=lambda p: (-p[1], p[0]) and slice [:k].",
    ],
}
