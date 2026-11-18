HINTS = {
    "content_hash": [
        "hashlib.sha256 needs bytes. How do you turn a str into bytes?",
        "Encode with 'utf-8', pass the result to hashlib.sha256(...).",
        "Call .hexdigest() on the hash object to get the 64-character string.",
    ],
    "chunk_id": [
        "First build the key string exactly as the docstring shows. An f-string is perfect for this.",
        "Then reuse content_hash from problem 1 on that key.",
        "Slice the result: [:16] keeps the first 16 characters.",
    ],
    "detect_changes": [
        "Think in sets of paths: set(old) gives the old paths, set(new) the new ones.",
        "Added = new minus old. Deleted = old minus new. The paths in both are new & old (intersection).",
        "Split the paths in both into changed / unchanged by comparing old[path] with new[path]. Wrap "
        "each list in sorted(...).",
    ],
}
