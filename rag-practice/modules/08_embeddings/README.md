# Module 08 · Embeddings (with a toy model)

## Where this fits

An embedding model turns a text into one vector. Inside, it does three things you already know:
1. **tokenize** the text (module 03)
2. look up a **vector per token**, which the model learned during training
3. **pool** the token vectors into one vector (module 07) and usually **normalize** it

A real model like BGE-M3 also runs a transformer between steps 2 and 3, so each token's vector
depends on its neighbours. This module skips that part and keeps the rest: a **toy model** made of a
lookup table, `WORD_VECTORS` in `common/data.py`, with 4 dimensions you can read:
`[security, shopping, setup, general]`.

Build plan link: **step 11** (generate dense vectors in **batches**, normalization, input limits).

## Ideas to know

- **Same model for chunks and questions.** Vectors from different models live in different spaces.
- Words the model doesn't know are skipped here. Real tokenizers never fail like that: they cut an
  unknown word into known sub-pieces (`hashlib` → `hash` + `lib`).
- **Batching**: models are much faster on 32 texts at once than on 1 text 32 times. You split the
  list of chunks into batches before calling the model.

## Reusing your earlier work

You can call your own solutions from earlier modules:

```python
from toolkit import module
tokens = module(3).tokenize("Hash the password")    # your tokenizer
pooled = module(7).mean_pool([[1, 2], [3, 4]])      # your pooling
```

This is real RAG work: small, tested pieces glued together.

## Python you'll need

```python
from data import WORD_VECTORS             # the toy model's table
WORD_VECTORS["password"]                  # [0.9, 0.0, 0.0, 0.1]
"cart" in WORD_VECTORS                    # True
next(iter(WORD_VECTORS.values()))         # any one vector (to learn the dimension)
[0.0] * 4                                 # [0.0, 0.0, 0.0, 0.0]
sorted(items, key=lambda w: (-score[w], w))  # highest score first, ties alphabetical
items[0:3], items[3:6]                    # slicing in steps
range(0, 10, 4)                           # 0, 4, 8
```

## In the real project you'll call

```python
from FlagEmbedding import BGEM3FlagModel
model = BGEM3FlagModel("BAAI/bge-m3")
out = model.encode(texts, batch_size=32, return_dense=True, return_sparse=True)
```
`out["dense_vecs"]` holds one normalized 1024-number vector per text. Everything in this module
happens inside that one call.

## Problems

1. `embed_text`: text → one normalized vector (toy model)
2. `most_similar`: which words are closest to this one?
3. `batched`: split a list into batches
