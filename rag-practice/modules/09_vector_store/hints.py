HINTS = {
    "add": [
        "Two checks before storing: is the id already a key in self.points? Does the vector length match?",
        "To learn the existing dimension, look at any stored point's vector (only if the store isn't empty).",
        "Store it as self.points[id] = {'vector': vector, 'payload': payload}.",
    ],
    "search": [
        "Loop over self.points.items(), compute a score for each, and build a list of result dicts.",
        "Use cosine from module 7: module(7).cosine(query, point['vector']).",
        "Sort with key=lambda r: (-r['score'], r['id']) and return the first k with [:k].",
    ],
    "filtered_search": [
        "Don't copy search(). Reuse it: the difference is only WHICH points take part.",
        "A point matches when all(payload.get(key) == value for key, value in where.items()).",
        "One clean way: write a private helper _rank(query, points, k) that both methods call. Another: "
        "build a temporary VectorStore containing only the matching points and call its search().",
    ],
    "delete_where": [
        "Never delete from a dict while looping over it. First collect the ids to delete, then delete them.",
        "Matching works exactly like in filtered_search, with `conditions` instead of `where`.",
        "Return len(ids_to_delete) after deleting them with `del self.points[pid]`.",
    ],
}
