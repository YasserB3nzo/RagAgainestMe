HINTS = {
    "embed_text": [
        "Three steps, three earlier tools: tokenize (module 3), mean_pool and normalize (module 7). "
        "Load them with module(3) and module(7).",
        "After tokenizing, keep the vectors of tokens that are `in word_vectors`. If that list is empty, "
        "return [0.0] * dim, where dim is the length of any vector in the table.",
        "Otherwise return normalize(mean_pool(known_vectors)).",
    ],
    "most_similar": [
        "Check `word in word_vectors` first. Then compare its vector with every OTHER word's vector.",
        "Your cosine from module 7 gives the score. Build a list of (score, other_word) or a dict.",
        "Sort with key=lambda w: (-score[w], w): the minus sign puts high scores first, and the word "
        "breaks ties alphabetically. Then slice [:n].",
    ],
    "batched": [
        "Validate size, then walk through the list in steps of `size`.",
        "range(0, len(items), size) gives the start index of every batch.",
        "items[start:start + size] is one batch. Slicing past the end is safe in Python.",
    ],
}
