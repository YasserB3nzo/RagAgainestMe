# Module 06 · Deterministic IDs & change detection

## Where this fits

Every chunk needs an **ID**: the vector database stores points by ID, citations refer to IDs, and
evaluation labels refer to IDs.

If IDs were random, re-indexing the same repository would produce different IDs every time. Your
evaluation labels would break, and you couldn't tell "this chunk changed" from "this chunk was
re-created". So IDs are **deterministic**: computed from facts about the chunk, so the same input
always gives the same ID.

**Hashes** also detect changes cheaply: if a file's hash is the same as last time, nothing in it
changed and you can skip re-embedding it.

Build plan link: **step 08** (*"Unchanged inputs produce consistent chunk IDs"*) and **step 23**
(incremental indexing with file hashes: added, changed, deleted).

## Ideas to know

- A **hash function** (like SHA-256) turns any text into a fixed-length fingerprint. Same text →
  same hash, always. Change one character → completely different hash.
- A hash isn't encryption. You can't get the text back from it, and that's fine: you only compare.
- A chunk's identity = repository + commit + path + line range. Hash those together.

## Python you'll need

```python
import hashlib
h = hashlib.sha256("hello".encode("utf-8"))   # hash functions take BYTES, not str
h.hexdigest()                                  # '2cf24dba5fb0a30e...' (64 hex characters)
h.hexdigest()[:16]                             # first 16 characters
f"{repo}:{commit}"                             # f-strings build a key from several values
set(old) - set(new)                            # keys in old but not in new
sorted({"b", "a"})                             # ['a', 'b']
```

## In the real project you'll call

- `hashlib.sha256` (exactly like here)
- Qdrant accepts UUIDs or integers as point IDs. `uuid.uuid5(namespace, key)` turns your
  deterministic key into a UUID the same way.

## Problems

1. `content_hash`: fingerprint a text
2. `chunk_id`: a deterministic ID for a chunk
3. `detect_changes`: compare two snapshots of a repository
