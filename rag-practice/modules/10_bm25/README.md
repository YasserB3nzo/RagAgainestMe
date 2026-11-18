# Module 10 · BM25 keyword search

## Where this fits

BM25 is the classic keyword search, and your build plan makes it the **first baseline**: before any
embedding, you must be able to measure plain keyword search. It's also the half of hybrid search that
catches **exact words**: function names, error codes, `hashPassword`.

Build plan link: **step 10** (*"lexical search, term frequency, document frequency and identifier
tokenization… a measured baseline"*).

## The formula, piece by piece

**1. Term frequency (tf)**: how many times a term appears in one document.
More occurrences → more relevant, but with diminishing returns (the 10th "password" adds little).

**2. Document frequency (df)**: in how many documents a term appears at least once.

**3. Inverse document frequency (idf)**: rare terms are worth more than common ones.

```
idf(term) = ln( (N - df + 0.5) / (df + 0.5) + 1 )        N = number of documents
```

**4. The BM25 score** of document D for a query:

```
             idf(q) × tf × (k1 + 1)
score(D) = Σ  ─────────────────────────────────────────
           q   tf + k1 × (1 - b + b × |D| / avgdl)
```

- sum over each **distinct** query term `q` that appears in D (terms with tf = 0 add nothing)
- `|D|` = number of tokens in D, `avgdl` = average number of tokens per document
- `k1` (≈1.5) controls how fast extra occurrences stop helping
- `b` (≈0.75) controls how much long documents are penalized (b = 0 means no penalty)

## Ideas to know

- In module 11, you'll fuse BM25 with vector search. **Their scores use different scales.** A BM25
  score of 7.3 and a cosine of 0.82 can't be compared directly.
- A document with score 0 shares no term with the query. Don't return it as a result.
- Tokenization decides everything: BM25 only sees what your tokenizer (module 03) gives it.

## Python you'll need

```python
import math
math.log(2.718281828)                    # ≈ 1.0 (natural log, written ln)
from collections import Counter
Counter(["a", "b", "a"])                 # Counter({'a': 2, 'b': 1})
dict(Counter(["a", "b", "a"]))           # {'a': 2, 'b': 1}
set(["a", "b", "a"])                     # {'a', 'b'}: each term once
enumerate(["x", "y"])                    # (0, 'x'), (1, 'y')
```

## In the real project you'll call

- `rank_bm25.BM25Okapi(tokenized_docs).get_scores(query_tokens)` (the same formula)
- Or BGE-M3's **learned sparse** vectors in Qdrant, which play the same role with learned weights

## Problems

1. `term_frequencies`
2. `document_frequencies`
3. `idf`
4. `bm25_scores`
5. `top_k`
