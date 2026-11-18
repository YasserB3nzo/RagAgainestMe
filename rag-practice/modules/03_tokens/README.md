# Module 03 · Tokenization (code-aware)

## Where this fits

Search can't compare raw text. It compares **tokens**: small pieces such as words. Keyword search
(BM25, module 10) matches tokens exactly, so how you cut text into tokens decides what can be found.

Code makes this harder. A user asks *"where is the password hashed?"* but the code says
`hashPassword` or `hash_password`. A plain tokenizer produces `hashpassword`, which never matches
`hash` or `password`. The fix is to **split identifiers** into their parts *and* keep the whole name,
so both "hash password" and an exact-symbol search for `hashPassword` work.

Build plan link: **step 10** ("identifier tokenization") and **step 11** (tokens are also the first
step inside an embedding model).

## Ideas to know

- **Lowercasing** makes `Docker` and `docker` the same token.
- **snake_case** splits on `_`. **camelCase** splits where a lowercase letter meets an uppercase one.
  **Acronyms** like `HTTPServer` split before the last capital: `http` + `server`.
- **Vocabulary**: every distinct token gets a number (an ID). Models work with these IDs, never with
  strings. ID 0 is usually reserved for "unknown token".

## Python you'll need

```python
import re
re.findall(r"[a-z]+", "ab1cd")           # ['ab', 'cd']: every match of the pattern
re.split(r"[_\-]+", "a_b-c")             # ['a', 'b', 'c']
re.sub(r"(\d)", r"<\1>", "a1b2")         # 'a<1>b<2>': \1 reuses what group 1 matched
"Hello".lower()
[w for w in words if w]                  # drop empty strings
```

Patterns used above: `[a-z]` is one lowercase letter, `+` means "one or more", `\d` is a digit,
and parentheses `( )` create a group you can reuse with `\1`, `\2`.

## In the real project you'll call

- For BM25: your own `code_tokenize` from this module (no library knows your code conventions)
- For embeddings: the model's own tokenizer, which runs automatically inside `model.encode(...)`

## Problems

1. `tokenize`: lowercase words and numbers
2. `split_identifier`: `getUserName` → `get`, `user`, `name`
3. `code_tokenize`: keep whole identifiers and add their parts
4. `build_vocab`: give every token an ID
5. `encode`: turn tokens into IDs
