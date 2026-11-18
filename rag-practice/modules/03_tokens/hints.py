HINTS = {
    "tokenize": [
        "Lowercase first, then find the pieces you want instead of splitting on what you don't want.",
        "re.findall returns every match of a pattern as a list.",
        "The pattern needs 'one or more characters from the set a to z or 0 to 9'. A character set is "
        "written in square brackets, and 'one or more' is a + after it.",
    ],
    "split_identifier": [
        "Do it in two stages: first insert a separator (like a space) at every camelCase boundary, then "
        "split on spaces, '_' and '-' all at once.",
        "Each boundary rule becomes one re.sub with two groups: group 1 is the character before the "
        "boundary, group 2 the character(s) after. The replacement puts a space between \\1 and \\2.",
        "Rule A: group 1 is a lowercase letter or digit, group 2 an uppercase letter. Rule B: group 1 is "
        "one or more uppercase letters, group 2 is an uppercase letter followed by a lowercase one. Apply "
        "A then B, split with re.split on a set of separators, lowercase, and drop empty strings.",
    ],
    "code_tokenize": [
        "Use re.findall with a pattern for letters (upper AND lower), digits and underscore.",
        "Call your split_identifier on each raw match (before lowercasing, or the camelCase is gone).",
        "Append raw.lower() first, then extend with the parts only if parts != [raw.lower()].",
    ],
    "build_vocab": [
        "Loop over every list, then over every token in it.",
        "Only add a token the first time you see it: check `if token not in vocab`.",
        "The next ID is always len(vocab) + 1 at the moment you add a new token.",
    ],
    "encode": [
        "One output number per input token, in the same order.",
        "vocab.get(token, 0) returns 0 for unknown tokens.",
        "A list comprehension does it in one line.",
    ],
}
