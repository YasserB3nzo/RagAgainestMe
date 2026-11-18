# Module 13 · Answer, citations & evaluation

## Where this fits

This is the last stretch before the LLM:

1. **Build the context**: number every retrieved chunk as evidence `[E1]`, `[E2]`… with its location.
2. The LLM answers and cites evidence IDs: *"Passwords are hashed with SHA-256 [E1]."*
3. **Validate citations**: an ID the model invented (`[E7]` when there are only 3) must be rejected.
4. **Evaluate retrieval** with Recall@k: did the right chunk make it into the top k at all?
5. **Glue everything** into one `search_pipeline()` that calls your earlier modules.

The LLM call itself is a single function call. Everything around it is your code.

Build plan link: **step 09** (Recall@k), **step 16** (context builder), **step 17** (*"assign evidence
IDs, validate returned citation IDs and resolve them to commit, file path and line range"*).

## A prompt built from your context

```
You answer questions about the repository using ONLY the evidence below.
Cite evidence like [E1] after each claim. If the evidence is not enough, say so.

[E1] auth.py:1-8
import hashlib
...

Question: Which function hashes the password with SHA-256?
```

## Ideas to know

- **Location format**: `path:start-end` for code chunks, `path > Heading > Sub` for Markdown chunks.
- **Recall@k** = (relevant items found in the top k) / (all relevant items). It measures retrieval
  alone. A great answer generated from lucky evidence doesn't count.
- **A valid citation isn't automatically a true one.** `[E1]` can exist and still not support the
  claim. That's why the plan adds manual review and RAGAS faithfulness on top.

## Python you'll need

```python
import re
re.findall(r"\[(E\d+)\]", "see [E2] and [E10]")   # ['E2', 'E10']: only the group is returned
"\n\n".join(blocks)
set(a[:3]) & set(b)                               # what's in both
from toolkit import module                        # your earlier solutions
module(4).make_chunks(...)
```

## In the real project you'll call

- Your LLM (Qwen3) through its chat API: `response = client.chat.completions.create(messages=[...])`
- RAGAS for faithfulness. Your own `recall_at_k` for retrieval benchmarks.

## Problems

1. `build_context`: numbered evidence blocks
2. `extract_citations`: find `[E1]`-style IDs in an answer
3. `validate_citations`: split them into valid and invalid
4. `recall_at_k`: measure retrieval
5. `search_pipeline`: the capstone, wiring modules 03–12 together
