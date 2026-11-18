from checks import expect

PROBLEMS = [
    ("tokenize", "lowercase words and numbers"),
    ("split_identifier", "getUserName -> get, user, name"),
    ("code_tokenize", "whole identifiers plus their parts"),
    ("build_vocab", "give every token an ID"),
    ("encode", "turn tokens into IDs"),
]


def test_tokenize__examples(ex):
    expect(ex.tokenize("Hello, World 42!"), ["hello", "world", "42"], 'tokenize("Hello, World 42!")')
    expect(ex.tokenize("hash_password(salt)"), ["hash", "password", "salt"], 'tokenize("hash_password(salt)")')
    expect(ex.tokenize("getUser"), ["getuser"], 'tokenize("getUser")')


def test_tokenize__empty_and_symbols(ex):
    expect(ex.tokenize(""), [], 'tokenize("")')
    expect(ex.tokenize("  ... !! "), [], 'tokenize("  ... !! ")')


def test_tokenize__multiline(ex):
    expect(ex.tokenize("Run with\nDocker:\tport 8000"), ["run", "with", "docker", "port", "8000"],
           'tokenize("Run with\\nDocker:\\tport 8000")')


def test_split_identifier__camel_case(ex):
    expect(ex.split_identifier("getUserName"), ["get", "user", "name"], 'split_identifier("getUserName")')
    expect(ex.split_identifier("hashPassword"), ["hash", "password"], 'split_identifier("hashPassword")')


def test_split_identifier__snake_and_kebab(ex):
    expect(ex.split_identifier("parse_HTTP_response"), ["parse", "http", "response"],
           'split_identifier("parse_HTTP_response")')
    expect(ex.split_identifier("total-price"), ["total", "price"], 'split_identifier("total-price")')


def test_split_identifier__acronyms(ex):
    expect(ex.split_identifier("HTTPServer"), ["http", "server"], 'split_identifier("HTTPServer")')
    expect(ex.split_identifier("XMLHttpRequest"), ["xml", "http", "request"], 'split_identifier("XMLHttpRequest")')


def test_split_identifier__digits_and_dunders(ex):
    expect(ex.split_identifier("v2Api"), ["v2", "api"], 'split_identifier("v2Api")')
    expect(ex.split_identifier("__init__"), ["init"], 'split_identifier("__init__")')
    expect(ex.split_identifier("simple"), ["simple"], 'split_identifier("simple")')


def test_code_tokenize__examples(ex):
    expect(ex.code_tokenize("def hashPassword(salt):"), ["def", "hashpassword", "hash", "password", "salt"],
           'code_tokenize("def hashPassword(salt):")')
    expect(ex.code_tokenize("x = get_user()"), ["x", "get_user", "get", "user"],
           'code_tokenize("x = get_user()")')


def test_code_tokenize__dunder_keeps_both(ex):
    expect(ex.code_tokenize("def __init__(self):"), ["def", "__init__", "init", "self"],
           'code_tokenize("def __init__(self):")')


def test_code_tokenize__empty(ex):
    expect(ex.code_tokenize("() => {}"), [], 'code_tokenize("() => {}")')


def test_build_vocab__example(ex):
    expect(ex.build_vocab([["cart", "total"], ["total", "tax"]]), {"cart": 1, "total": 2, "tax": 3},
           'build_vocab([["cart", "total"], ["total", "tax"]])')


def test_build_vocab__repeats_in_one_list(ex):
    expect(ex.build_vocab([["a", "a", "b"], [], ["b", "c"]]), {"a": 1, "b": 2, "c": 3},
           'build_vocab([["a", "a", "b"], [], ["b", "c"]])')


def test_build_vocab__empty(ex):
    expect(ex.build_vocab([]), {}, "build_vocab([])")


def test_encode__example(ex):
    expect(ex.encode(["tax", "refund", "cart"], {"cart": 1, "total": 2, "tax": 3}), [3, 0, 1],
           'encode(["tax", "refund", "cart"], vocab)')


def test_encode__empty(ex):
    expect(ex.encode([], {"a": 1}), [], "encode([], vocab)")
