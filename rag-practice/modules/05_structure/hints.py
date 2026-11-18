HINTS = {
    "split_sections": [
        "Read the text line by line and keep some state: the current heading path, the lines of the "
        "current body, and whether you are inside a code fence.",
        "When a line starts with ``` flip the in-fence flag and treat the line as normal body text. "
        "Only check for headings when you are NOT in a fence. When you hit a heading, first save the "
        "section you were building (if its body isn't empty), then start a new one.",
        "Keep a stack of (level, title). On a heading of level L, pop entries while the top has level >= L, "
        "then push (L, title). The heading path is the list of titles in the stack. Don't forget to save "
        "the last section after the loop ends.",
    ],
    "pack": [
        "Keep a `current` chunk being built, and a list of finished chunks.",
        "For each piece: if there is no current chunk, it becomes the current chunk. Otherwise, compute the "
        "length the chunk WOULD have if you added sep + piece.",
        "If that length is <= max_chars, extend current; else move current to the finished list and start "
        "over with this piece. After the loop, don't forget the last current chunk (if any).",
    ],
    "section_chunks": [
        "This one is mostly glue: call split_sections, then pack, then build dicts.",
        "Split a section's text into paragraphs with re.split on a blank-line pattern (see the guide), then "
        "strip each one and drop the empty ones.",
        "Build search_text with a conditional: join the heading path with ' > ' and add '\\n' + text, or "
        "use the text alone when the path is empty.",
    ],
}
