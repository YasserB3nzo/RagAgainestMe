HINTS = {
    "line_windows": [
        "Validate the settings first. Then handle n_lines == 0.",
        "Keep a `start` variable beginning at 1. Each window ends at min(start + size - 1, n_lines).",
        "After appending a window, stop if its end is n_lines; otherwise move start forward by "
        "size - overlap. A `while True:` loop with a `break` fits well.",
    ],
    "make_chunks": [
        "Split the text into lines once, then ask line_windows for the ranges.",
        "Line numbers are 1-based but list indexes are 0-based: line `start` is lines[start - 1].",
        "The slice lines[start - 1:end] gives exactly lines start..end (the slice end is exclusive, "
        "which cancels out the 1-based offset).",
    ],
    "find_chunks": [
        "Keep chunks that pass two tests: same path, and the line falls inside the range.",
        "'Inside' includes both ends: start_line <= line <= end_line. Python allows that chained comparison.",
        "A list comprehension with both conditions joined by `and` is enough.",
    ],
}
