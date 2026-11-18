from checks import expect, expect_raises
from data import REPO

PROBLEMS = [
    ("line_starts", "where does each line start?"),
    ("line_of_offset", "which line is this character on?"),
    ("span_to_lines", "which lines does a span cover?"),
    ("char_to_byte", "character offset -> byte offset"),
    ("byte_to_char", "byte offset -> character offset"),
]


def test_line_starts__examples(ex):
    expect(ex.line_starts("ab\ncd\n"), [0, 3, 6], 'line_starts("ab\\ncd\\n")')
    expect(ex.line_starts("abc"), [0], 'line_starts("abc")')
    expect(ex.line_starts(""), [0], 'line_starts("")')


def test_line_starts__empty_lines(ex):
    expect(ex.line_starts("\n\nx"), [0, 1, 2], 'line_starts("\\n\\nx")')


def test_line_of_offset__examples(ex):
    for offset, line in [(0, 1), (2, 1), (3, 2), (5, 2)]:
        expect(ex.line_of_offset("ab\ncd", offset), line, f'line_of_offset("ab\\ncd", {offset})')


def test_line_of_offset__after_final_newline(ex):
    expect(ex.line_of_offset("ab\ncd\n", 6), 3, 'line_of_offset("ab\\ncd\\n", 6)')


def test_line_of_offset__out_of_range(ex):
    expect_raises(ValueError, ex.line_of_offset, "abc", 4, what='line_of_offset("abc", 4)')
    expect_raises(ValueError, ex.line_of_offset, "abc", -1, what='line_of_offset("abc", -1)')


def test_span_to_lines__docstring_example(ex):
    text = "import os\n\ndef f():\n    return 1\n"
    start, end = text.index("def"), text.index("1") + 1
    expect(ex.span_to_lines(text, start, end), (3, 4), "span of the function f")


def test_span_to_lines__real_file(ex):
    text = REPO["auth.py"]
    start = text.index("def hash_password")
    end = text.index("hexdigest()") + len("hexdigest()")
    expect(ex.span_to_lines(text, start, end), (4, 6), "span of hash_password in auth.py")


def test_span_to_lines__span_ending_with_newline(ex):
    text = "a\nb\nc\n"
    expect(ex.span_to_lines(text, 0, 4), (1, 2), 'span_to_lines("a\\nb\\nc\\n", 0, 4) covers "a\\nb\\n"')


def test_span_to_lines__empty_span(ex):
    expect(ex.span_to_lines("a\nb", 2, 2), (2, 2), 'span_to_lines("a\\nb", 2, 2)')


def test_span_to_lines__invalid(ex):
    expect_raises(ValueError, ex.span_to_lines, "abc", 2, 1, what="start after end")
    expect_raises(ValueError, ex.span_to_lines, "abc", 0, 9, what="end beyond the text")


def test_char_to_byte__examples(ex):
    expect(ex.char_to_byte("cafe ok", 5), 5, 'char_to_byte("cafe ok", 5)')
    expect(ex.char_to_byte("café ok", 5), 6, 'char_to_byte("café ok", 5)')
    expect(ex.char_to_byte("a🙂b", 2), 5, 'char_to_byte("a🙂b", 2)')


def test_char_to_byte__edges(ex):
    expect(ex.char_to_byte("héllo", 0), 0, 'char_to_byte("héllo", 0)')
    expect(ex.char_to_byte("héllo", 5), 6, 'char_to_byte("héllo", 5)')
    expect_raises(ValueError, ex.char_to_byte, "abc", 4, what='char_to_byte("abc", 4)')


def test_byte_to_char__examples(ex):
    expect(ex.byte_to_char("café ok", 6), 5, 'byte_to_char("café ok", 6)')
    expect(ex.byte_to_char("a🙂b", 5), 2, 'byte_to_char("a🙂b", 5)')
    expect(ex.byte_to_char("abc", 3), 3, 'byte_to_char("abc", 3)')


def test_byte_to_char__middle_of_character(ex):
    expect_raises(ValueError, ex.byte_to_char, "a🙂b", 2, what='byte_to_char("a🙂b", 2)')
    expect_raises(ValueError, ex.byte_to_char, "é", 1, what='byte_to_char("é", 1)')


def test_byte_to_char__out_of_range(ex):
    expect_raises(ValueError, ex.byte_to_char, "abc", 4, what='byte_to_char("abc", 4)')
    expect_raises(ValueError, ex.byte_to_char, "abc", -1, what='byte_to_char("abc", -1)')


def test_byte_to_char__round_trip(ex):
    text = "naïve 🙂 café\nfin"
    for i in range(len(text) + 1):
        expect(ex.byte_to_char(text, ex.char_to_byte(text, i)), i, f"round trip for character offset {i}")
