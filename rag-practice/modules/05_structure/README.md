# Module 05 · Structure-aware chunking (Markdown)

## Where this fits

Cutting every N lines (module 04) ignores meaning. Documentation already has structure: **headings**.
A chunk that knows it lives under `Tiny Shop > Run with Docker` is far easier to find than a loose
paragraph that says "start the container".

This module splits Markdown into **sections** by heading, keeps the **heading path** (the chain of
parent headings), and packs paragraphs into chunks that fit a size limit.

You'll also store two texts per chunk:
- `text`: the **original** passage, used as citation evidence
- `search_text`: heading path + text, used only for searching

Build plan link: **step 07** (chunks retain heading context) and **step 15** (*"Store context_prefix,
search_text and original_text separately. Generated descriptions are not original source evidence."*).

## Ideas to know

- A heading is a line starting with 1 to 6 `#` followed by a space. More `#` = deeper level.
- **Heading path**: when you meet a level-2 heading, it replaces any previous level-2 (or deeper)
  heading, but keeps the level-1 heading above it.
- Inside a fenced code block (between two ```` ``` ```` lines) a line like `# install deps` is a
  **comment, not a heading**. Real READMEs are full of these.
- **Greedy packing**: add pieces to the current chunk while it still fits; when the next piece won't
  fit, start a new chunk.

## Python you'll need

```python
import re
m = re.match(r"(#+) (.*)", "## Install")
m.group(1), m.group(2)                  # ('##', 'Install')
re.match(r"(#+) (.*)", "hello")         # None: no match
re.split(r"\n\s*\n", "a\n\nb\n  \nc")   # ['a', 'b', 'c']: split on blank lines
stack = [(1, "A"), (2, "B")]
stack.pop()                             # removes and returns (2, 'B')
" > ".join(["A", "B"])                  # 'A > B'
```

## In the real project you'll call

- A Markdown parser (for example `markdown-it-py`) instead of your regex, for full syntax support
- Your own packing logic: libraries split text, but deciding what context to keep is your design

## Problems

1. `split_sections`: Markdown → sections with heading paths
2. `pack`: greedy packing of pieces under a size limit
3. `section_chunks`: sections → chunks with `text` and `search_text`
