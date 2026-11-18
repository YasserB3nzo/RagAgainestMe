# Module 11 · Hybrid search: fusion & deduplication

## Where this fits

You now have two searches: vectors (meaning) and BM25 (exact words). Each finds things the other
misses. **Hybrid search** merges their result lists into one.

The problem: their scores live on **different scales**. A cosine is between −1 and 1, and a BM25
score can be 0.4 or 12.7. Adding them directly lets BM25 dominate. Two fixes:

1. **Min-max normalization**: rescale each list's scores to 0–1, then combine. Simple, but sensitive
   to outliers.
2. **Reciprocal Rank Fusion (RRF)**: ignore the scores entirely and use only the **ranks**. Your build
   plan uses this one.

```
RRF score(doc) = Σ over each list that contains doc:  1 / (k + rank)        (rank starts at 1, k = 60)
```

A document ranked well in **both** lists collects two big contributions and rises to the top.

After fusion, the same evidence often appears **twice**: overlapping chunks (module 04) or the same
lines found by both searches. **Deduplicate** before the reranker and the LLM see it.

Build plan link: **step 13** (*"rank fusion, candidate selection, deduplication and incompatible
score scales"*).

## Ideas to know

- k = 60 is the usual constant. A larger k flattens the difference between rank 1 and rank 10.
- Two line ranges `[s1, e1]` and `[s2, e2]` overlap when `s1 <= e2 and s2 <= e1`.
- When deduplicating, keep the **first** (best-ranked) chunk and drop later ones that overlap it.

## Python you'll need

```python
scores = {"a": 0.5, "b": 0.9}
sorted(scores, key=lambda i: (-scores[i], i))     # ['b', 'a']
for rank, item in enumerate(["x", "y"], start=1):  # rank starts at 1
    ...
totals[item] = totals.get(item, 0.0) + 1 / (k + rank)
max(scores.values()), min(scores.values())
```

## In the real project you'll call

- Qdrant's built-in fusion: `client.query_points(..., prefetch=[dense, sparse], query=FusionQuery(fusion=Fusion.RRF))`
- Your own dedup step, because only you know your chunk spans

## Problems

1. `ranking`: scores dict → ordered list of ids
2. `rrf`: fuse several rankings
3. `min_max`: rescale scores to 0–1
4. `dedupe_overlapping`: drop chunks that overlap a better one
