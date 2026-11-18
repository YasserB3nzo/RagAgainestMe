HINTS = {
    "overlap_score": [
        "Turn both token lists into sets first.",
        "If either set is empty, return 0.0 before dividing.",
        "len(a & b) is |A ∩ B|. Divide by math.sqrt(len(a) * len(b)).",
    ],
    "rerank": [
        "score_fn is a function. Call it like any other: score_fn(query, candidate['text']).",
        "Build new dicts with {**candidate, 'rerank_score': score}. That copies, so the input stays unchanged.",
        "sorted(..., key=lambda c: -c['rerank_score']) is stable, so ties keep their original order. "
        "Then slice [:keep].",
    ],
    "rank_changes": [
        "Build a lookup from id to old rank first, using enumerate(before, start=1).",
        "Then loop over enumerate(after, start=1) to get each new rank.",
        "old_rank.get(id) returns None automatically for ids that weren't in `before`.",
    ],
}
