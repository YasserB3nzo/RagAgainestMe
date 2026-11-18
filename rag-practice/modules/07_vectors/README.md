# Module 07 · Vector math & cosine similarity

## Where this fits

Once text becomes vectors, "how similar are these two texts?" becomes "how similar are these two
lists of numbers?". The database does this math for you millions of times per second, but your build
plan says: *"Calculate cosine similarity on a few vectors yourself before relying on database search."*
That's this module.

Build plan link: **step 11** (normalization) and **step 12** (similarity scores).

## The formulas

For vectors `a` and `b` of the same length:

| Name | Formula | Meaning |
|---|---|---|
| Dot product | `a·b = a₁b₁ + a₂b₂ + … + aₙbₙ` | multiply pairs, add them up |
| Norm (length) | `‖a‖ = √(a₁² + a₂² + … + aₙ²)` | how long the arrow is |
| Normalize | `a / ‖a‖` (each number divided by the norm) | same direction, length 1 |
| Cosine similarity | `a·b / (‖a‖ × ‖b‖)` | 1 = same direction, 0 = unrelated |
| Mean pooling | average of several vectors, position by position | many token vectors → one chunk vector |

Worked example (the one from our conversation): with dimensions `[animal, small/cute, vehicle]`,
`cat = [0.9, 0.6, 0.0]`, `kitten = [0.8, 0.9, 0.0]`, `car = [0.0, 0.1, 0.9]`:
- cosine(cat, kitten) ≈ **0.967**
- cosine(cat, car) ≈ **0.061**

## Ideas to know

- After normalizing, `cosine(a, b) == dot(a, b)`. That's why vector databases ask whether your
  vectors are normalized: it saves a division per comparison.
- A **zero vector** `[0, 0, 0]` has length 0. Dividing by it would crash, so handle it explicitly.
- Two vectors of different lengths come from different models or a bug. Raise an error, don't guess.

## Python you'll need

```python
import math
math.sqrt(16)                      # 4.0
zip([1, 2], [3, 4])                # pairs: (1, 3), (2, 4)
sum(x * y for x, y in zip(a, b))   # add up a generated sequence
[x / 2 for x in v]                 # transform every element
list(zip(*[[1, 2], [3, 4]]))       # [(1, 3), (2, 4)]: "columns" of a list of rows
```

## In the real project you'll call

- `numpy` (`a @ b`, `np.linalg.norm`) when you inspect vectors yourself
- Qdrant computes cosine inside `client.query_points(...)`, configured with `Distance.COSINE`

## Problems

1. `dot`
2. `norm`
3. `normalize`
4. `cosine`
5. `mean_pool`
