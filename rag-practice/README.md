# RAG practice

13 small modules (52 problems) of easy coding problems, in the style of LeetCode. Together they build the bare
minimum you need before starting the *RAG Against the Machine* build plan. Everything is plain Python
and runs offline: no API keys, no downloads, nothing to install.

Each module has:
- `README.md`: a short guide (what it is, why RAG needs it, the Python you'll use)
- `exercise.py`: the problems. Replace each `raise NotImplementedError` with your code.
- `tests.py`: the checks your code must pass
- `hints.py`: hints, revealed one at a time by the runner. No solutions anywhere.

## The website (recommended)

```bash
cd rag-practice
python3 server.py          # opens http://localhost:8765 in your browser
```

It's laid out like LeetCode: the problem on the left (Description / Guide / Hints), the editor on the right,
and the test results below it, with one tab per test case.

- **Run code** (`Ctrl+'`) runs your code in the **Playground** tab, with no tests: your functions are
  already loaded, so write any calls you like (`print(is_eligible("a.py"))`) and see the output or the error.
  Each problem starts with an example call; the ↺ Example button brings it back.
- **Run tests** (`Ctrl+Enter`) tests the current problem. **Submit** (`Ctrl+Shift+Enter`) tests the whole module.
- Your code saves automatically into `modules/*/exercise.py`, so the website and the terminal
  commands below always agree.
- `print()` output shows up under **Stdout** for each test case.
- The ↺ button resets one problem to its starter code (originals are kept in `.original/`).
- Press `Ctrl+C` in the terminal to stop the server.

## The terminal version

```bash
cd rag-practice
python3 rag.py                       # progress overview
python3 rag.py next                  # where to continue
python3 rag.py learn 1               # read the guide for module 1
python3 rag.py test 1                # run module 1's tests
python3 rag.py test 1 is_eligible    # test one problem only
python3 rag.py hint 1 is_eligible    # next hint for a problem (run again for more)
```

The loop: **learn → edit `exercise.py` in your editor → test → hint if stuck → test again.**

## The modules

| # | Module | What you build | Build plan step |
|---|---|---|---|
| 01 | Files & metadata | pick files, wrap them as documents, filter | 04, 05 |
| 02 | Source spans & offsets | lines ↔ characters ↔ bytes (Unicode-safe) | 05, 06 |
| 03 | Tokenization | code-aware tokens: `getUserName` → get, user, name | 10, 11 |
| 04 | Chunking with overlap | line windows with exact spans | 06, 07 |
| 05 | Markdown structure | sections, heading paths, `search_text` vs `text` | 07, 15 |
| 06 | IDs & change detection | deterministic chunk IDs, added/changed/deleted | 08, 23 |
| 07 | Vector math | dot, norm, normalize, cosine, pooling | 11 |
| 08 | Embeddings | a toy embedding model, batching | 11 |
| 09 | Vector store | points, top-k search, payload filters, delete | 12, 23 |
| 10 | BM25 | tf, df, idf, the BM25 score | 10 |
| 11 | Hybrid search | RRF fusion, score scales, deduplication | 13 |
| 12 | Reranking | a toy cross-scorer, rerank, before/after ranks | 14 |
| 13 | Answer & evaluation | evidence IDs, citation checks, Recall@k, **the full pipeline** | 09, 16, 17 |

Later modules can reuse your earlier solutions (`from toolkit import module`). Module 13's capstone
wires modules 03–12 together into a working retriever.

## Rules of thumb

- Read the problem's docstring and examples before writing anything.
- Use `print()` freely while you work. The tests don't mind.
- If you're stuck after the last hint, write down what you tried and ask for a code review rather
  than a solution.
