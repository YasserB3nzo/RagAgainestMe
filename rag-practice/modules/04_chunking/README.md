# Module 04 · Chunking with overlap

## Where this fits

An embedding model reads a limited amount of text, and a search result should be small enough to
point at one idea. So every file is cut into **chunks**. Each chunk keeps its **path and line range**,
so the answer can later cite `cart.py:11-14`.

**Overlap** repeats a few lines between neighbouring chunks. Without it, a function cut in half loses
its context: the `def` line lands in one chunk and the `return` in the next.

Build plan link: **step 06** (oversized definitions are split into smaller *contiguous original spans*,
which is what you do here) and **step 07** (passage size, overlap, context loss).

## Ideas to know

- **Size**: how many lines per chunk. Too small and chunks mean nothing on their own. Too big and the
  important line drowns in the rest.
- **Step** = size − overlap. With size 4 and overlap 1 the windows start on lines 1, 4, 7…
- The last window can be shorter. Stop as soon as a window reaches the last line.
- Overlap means one line can live in **two chunks**. Remember that in module 11 (deduplication).

```
lines:   1  2  3  4  5  6  7  8  9  10
chunk 1: [1 ---- 4]
chunk 2:          [4 ---- 7]
chunk 3:                   [7 ---- 10]
```

## Python you'll need

```python
lines = "a\nb\nc".splitlines()       # ['a', 'b', 'c']
lines[0:2]                           # ['a', 'b']: line 1 is index 0!
"\n".join(["a", "b"])                # 'a\nb'
min(7, 5)                            # 5
while True:
    ...
    if done:
        break
```

## In the real project you'll call

- Tree-sitter to find function and class boundaries (step 06). Line windows like these are the
  fallback for definitions that are too long.
- Libraries like LangChain's `RecursiveCharacterTextSplitter` do the same job for plain text.

## Problems

1. `line_windows`: compute the (start, end) line ranges
2. `make_chunks`: cut a file into chunk dicts
3. `find_chunks`: which chunks contain a given line?
