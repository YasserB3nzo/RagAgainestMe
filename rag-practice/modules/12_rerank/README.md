# Module 12 · Reranking

## Where this fits

Retrieval (modules 09–11) is fast because each chunk's vector was computed **separately**, long
before the question arrived. That's a **bi-encoder**. It's fast but rough.

A **reranker** (a **cross-encoder**) reads the question and one chunk **together** and outputs a single
relevance score. It's precise but slow, so it only runs on the few candidates retrieval already found:

```
millions of chunks ──retrieval──▶ ~20 candidates ──rerank──▶ best 3–5 ──▶ LLM
```

Your build plan's warning: *"A reranker cannot recover evidence missing from its candidate set."* If
retrieval missed the right chunk, reranking can't bring it back.

Build plan link: **step 14** (*"bi-encoders versus cross-encoders, joint scoring, batching and
latency… before/after rankings"*).

## The toy reranker: Otsuka–Ochiai overlap

You can't train a cross-encoder here, so you'll write a scorer with the same **shape**: it looks at
the question and the chunk **together**. It's the formula you asked about earlier:

```
                |A ∩ B|              A = set of question tokens
overlap(A, B) = ─────────────        B = set of chunk tokens
                √(|A| × |B|)
```

Example: A = {new, employees, vacation, days}, B = {new, employees, receive, 22, days}
→ 3 shared / √(4 × 5) = **0.67**

Your `rerank` function takes the scorer as a **parameter** (`score_fn`). Later you can pass a real
cross-encoder without changing `rerank` at all.

## Python you'll need

```python
a, b = {"x", "y"}, {"y", "z"}
a & b                                # {'y'}: intersection
len(a & b)
def apply(fn, value):                # functions can be passed like any value
    return fn(value)
{**chunk, "rerank_score": 0.9}       # a NEW dict: copy of chunk + one more key
sorted(items, key=lambda c: -c["rerank_score"])   # sorted() is stable: ties keep their order
{item: i for i, item in enumerate(items, start=1)}  # item -> rank
```

## In the real project you'll call

```python
from sentence_transformers import CrossEncoder
model = CrossEncoder("BAAI/bge-reranker-v2-m3")
scores = model.predict([(question, c["text"]) for c in candidates], batch_size=16)
```
`lambda q, text: model.predict([(q, text)])[0]` can be passed straight into your `rerank`.

## Problems

1. `overlap_score`: the toy cross-scorer
2. `rerank`: re-sort candidates with any scorer
3. `rank_changes`: compare rankings before and after
