# Module 09 · A vector store with payload filters

## Where this fits

A vector database stores **points**. Each point has:
- an **id** (module 06)
- a **vector** (module 08)
- a **payload**: the metadata and text you want back (path, lines, commit, original text)

Searching means: score every point against the query vector, sort, return the top **k**. A **filter**
narrows which points are allowed before scoring, for example "only commit `a1b2c3d`".

You'll build a tiny in-memory version. It checks every point (a "flat" search), which is exactly
what Qdrant does for small collections. HNSW only speeds it up for millions of points.

Build plan link: **step 12** (*"collections, points, payload filters… Dense and sparse search work
independently without mixing repository revisions"*) and **step 23** (deleting stale chunks).

## Ideas to know

- **Same dimension for every point.** A collection is created for one vector size, and anything
  else is rejected.
- **Filter first, then rank.** A filter isn't a score. It removes points before ranking. Remember the
  board's warning: *"A bad filter can remove the correct answer before the vector search even starts."*
- **Deterministic order**: sort by score (highest first), and break ties by id so results are
  reproducible.

## Python you'll need

```python
class Box:
    def __init__(self):
        self.items = {}              # state lives on self
    def put(self, key, value):
        self.items[key] = value
b = Box(); b.put("x", 1)

all(payload.get(k) == v for k, v in where.items())   # does the payload match every condition?
results.sort(key=lambda r: (-r["score"], r["id"]))   # in-place sort
[k for k in d if cond(k)]                            # collect keys first...
del d[key]                                           # ...then delete (never while looping over d)
```

## In the real project you'll call

```python
client.upsert(collection_name="chunks", points=[PointStruct(id=..., vector=..., payload=...)])
client.query_points(collection_name="chunks", query=vector, limit=5,
                    query_filter=Filter(must=[FieldCondition(key="commit", match=MatchValue(value="a1b2c3d"))]))
client.delete(collection_name="chunks", points_selector=FilterSelector(filter=...))
```
Your three methods map one to one onto these calls.

## Problems

1. `add`: store a point
2. `search`: top-k by cosine similarity
3. `filtered_search`: search with a payload filter
4. `delete_where`: remove points that match a filter
