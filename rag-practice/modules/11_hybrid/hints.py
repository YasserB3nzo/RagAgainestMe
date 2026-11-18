HINTS = {
    "ranking": [
        "sorted() over a dict sorts its keys.",
        "You need a key function that sorts by score descending, then id ascending.",
        "key=lambda i: (-scores[i], i)",
    ],
    "rrf": [
        "Keep a totals dict: id -> fused score so far.",
        "For every ranking, use enumerate(ranking, start=1) so the first id has rank 1, and add "
        "1 / (k + rank) to that id's total.",
        "At the end, sort the ids like in problem 1 (you can call ranking(totals)) and return "
        "[(id, totals[id]) for id in that order].",
    ],
    "min_max": [
        "Handle the empty dict first, then find the smallest and largest score.",
        "If largest == smallest, dividing would crash: return 1.0 for every id instead.",
        "Otherwise build a new dict with (score - lo) / (hi - lo) for each id.",
    ],
    "dedupe_overlapping": [
        "Keep a list of kept chunks. For each incoming chunk, ask: does it overlap ANY kept chunk?",
        "Write a small helper overlaps(a, b): False if either has no 'start_line' or the paths differ; "
        "otherwise compare the ranges.",
        "Ranges [s1, e1] and [s2, e2] overlap when s1 <= e2 and s2 <= e1. Use any(...) over the kept list.",
    ],
}
