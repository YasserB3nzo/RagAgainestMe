# Module 02 · Source spans & offsets

## Where this fits

A citation is only useful if it points to the **exact place** in the original file. Your build plan
says: *"Every stored source range reproduces the original substring, including non-ASCII files."*

Positions in text can be counted in three ways, and you'll convert between them all the time:

| Unit | Example for `"café\nok"` | Who uses it |
|---|---|---|
| **Character offset** | `"o"` is at offset 5 | Python strings: `text[5]` |
| **Line number** (1-based) | `"o"` is on line 2 | Humans, editors, citations |
| **Byte offset** (UTF-8) | `"o"` is at byte 6 | Tree-sitter, files on disk |

`é` is **1 character** but **2 bytes** in UTF-8, so after an accented letter the character and byte
offsets drift apart. An emoji like `🙂` is 1 character and 4 bytes.

Build plan link: **step 05** (preserve original source locations) and **step 06** (Tree-sitter gives
byte offsets that you must convert).

## Ideas to know

- **Offsets start at 0, line numbers start at 1.** Mixing them up is the classic off-by-one bug.
- **Half-open spans** `[start, end)`: `start` is included and `end` is not, exactly like Python
  slicing. `text[start:end]` is the chunk. The span's last character sits at `end - 1`.
- A new line starts right **after** each `"\n"`.

## Python you'll need

```python
enumerate("ab\nc")                 # (0,'a'), (1,'b'), (2,'\n'), (3,'c')
"ab\ncd".count("\n", 0, 4)         # count newlines in text[0:4]
"café".encode("utf-8")             # b'caf\xc3\xa9' (5 bytes)
len("café".encode("utf-8"))        # 5
b"caf\xc3\xa9"[:4].decode("utf-8") # raises UnicodeDecodeError: cut in the middle of é
raise ValueError("offset out of range")
```

## In the real project you'll call

- Tree-sitter's `node.start_byte` / `node.end_byte` and `node.start_point` (row, column)
- Your own helpers from this module to turn those into character offsets and line ranges

## Problems

1. `line_starts`: where does each line start?
2. `line_of_offset`: which line is this character on?
3. `span_to_lines`: which lines does a span cover?
4. `char_to_byte`: character offset → byte offset
5. `byte_to_char`: byte offset → character offset
