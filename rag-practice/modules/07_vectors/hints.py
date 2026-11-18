HINTS = {
    "dot": [
        "Check the lengths first.",
        "zip(a, b) walks through both lists side by side.",
        "Multiply each pair and add everything up with sum(...).",
    ],
    "norm": [
        "The norm is the square root of the sum of the squares.",
        "Squares: x * x (or x ** 2) for each x.",
        "Notice that norm(v) is the square root of dot(v, v). You can reuse problem 1.",
    ],
    "normalize": [
        "Compute the norm once and keep it in a variable.",
        "If the norm is 0, return list(v): a copy, not the same list.",
        "Otherwise build a new list with every element divided by the norm.",
    ],
    "cosine": [
        "Reuse dot and norm from problems 1 and 2. dot already raises ValueError on mismatched lengths.",
        "Compute both norms. If either is 0, return 0.0 before dividing.",
        "Return dot(a, b) / (norm(a) * norm(b)).",
    ],
    "mean_pool": [
        "Check that the list isn't empty and that every vector has the same length as the first.",
        "You need one average per POSITION. zip(*vectors) gives you the columns: all first numbers, "
        "then all second numbers, and so on.",
        "For each column: sum(column) / len(vectors).",
    ],
}
