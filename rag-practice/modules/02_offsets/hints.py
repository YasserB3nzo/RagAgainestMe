HINTS = {
    "line_starts": [
        "Start your list with 0, because line 1 always starts at offset 0.",
        "Walk through the text with enumerate() so you get both the offset and the character.",
        "Every time the character is '\\n' at offset i, the next line starts at i + 1: append that.",
    ],
    "line_of_offset": [
        "Check the range first and raise ValueError if the offset is outside 0..len(text).",
        "The line number is 1 plus the number of newlines that come BEFORE the offset.",
        "str.count('\\n', 0, offset) counts newlines in text[0:offset]. Because the slice stops before "
        "`offset`, a newline exactly at `offset` is not counted, which is what you want.",
    ],
    "span_to_lines": [
        "Reuse line_of_offset from problem 2. You can call your own functions.",
        "Validate 0 <= start <= end <= len(text) first.",
        "The first line is the line of `start`. The last line is the line of `end - 1` (the last character "
        "inside the span), unless the span is empty.",
    ],
    "char_to_byte": [
        "Bytes only exist after encoding. Which part of the text comes before the offset?",
        "Slice the text up to char_offset, encode that slice as UTF-8, and measure it.",
        "Don't forget the ValueError when char_offset is outside 0..len(text).",
    ],
    "byte_to_char": [
        "Do the reverse of char_to_byte: encode the whole text, cut the bytes, decode the cut part back.",
        "The number of characters in the decoded part is your answer.",
        "If the cut lands inside a character, .decode('utf-8') raises UnicodeDecodeError. Catch it with "
        "try/except and raise ValueError instead. Check the range against len(encoded bytes) first.",
    ],
}
