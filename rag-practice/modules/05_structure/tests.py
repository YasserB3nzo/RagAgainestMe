from checks import expect
from data import REPO

PROBLEMS = [
    ("split_sections", "Markdown -> sections with heading paths"),
    ("pack", "greedy packing under a size limit"),
    ("section_chunks", "sections -> chunks with search_text"),
]


def test_split_sections__hierarchy(ex):
    expect(ex.split_sections("# A\na\n## B\nb\n### C\nc\n## D\nd"),
           [{"heading_path": ["A"], "text": "a"},
            {"heading_path": ["A", "B"], "text": "b"},
            {"heading_path": ["A", "B", "C"], "text": "c"},
            {"heading_path": ["A", "D"], "text": "d"}],
           'split_sections("# A\\na\\n## B\\nb\\n### C\\nc\\n## D\\nd")')


def test_split_sections__text_before_first_heading(ex):
    expect(ex.split_sections("intro\n# A\na"),
           [{"heading_path": [], "text": "intro"}, {"heading_path": ["A"], "text": "a"}],
           'split_sections("intro\\n# A\\na")')


def test_split_sections__skips_empty_sections(ex):
    expect(ex.split_sections("# A\n\n## B\nb\n"), [{"heading_path": ["A", "B"], "text": "b"}],
           'split_sections("# A\\n\\n## B\\nb\\n")')


def test_split_sections__code_fence_comment_is_not_a_heading(ex):
    md = "# Setup\n```bash\n# install deps\npip install x\n```\n"
    expect(ex.split_sections(md),
           [{"heading_path": ["Setup"], "text": "```bash\n# install deps\npip install x\n```"}],
           "a '#' line inside ``` fences")


def test_split_sections__hash_without_space(ex):
    expect(ex.split_sections("# A\n#not a heading"), [{"heading_path": ["A"], "text": "#not a heading"}],
           'split_sections("# A\\n#not a heading")')


def test_split_sections__real_readme(ex):
    got = ex.split_sections(REPO["README.md"])
    expect([s["heading_path"] for s in got],
           [["Tiny Shop"], ["Tiny Shop", "Install"], ["Tiny Shop", "Run with Docker"], ["Tiny Shop", "Security"]],
           "heading paths of README.md")
    expect(got[2]["text"], "Build the image, then start the container with docker compose up.\n"
                           "The shop listens on port 8000.", "text of the Docker section")


def test_pack__examples(ex):
    expect(ex.pack(["aa", "bb", "cc"], 5), ["aa bb", "cc"], 'pack(["aa", "bb", "cc"], 5)')
    expect(ex.pack(["aaaaaa", "b"], 4), ["aaaaaa", "b"], 'pack(["aaaaaa", "b"], 4)')


def test_pack__custom_separator(ex):
    expect(ex.pack(["a", "b"], 4, sep="\n\n"), ["a\n\nb"], 'pack(["a", "b"], 4, sep="\\n\\n")')
    expect(ex.pack(["a", "b"], 3, sep="\n\n"), ["a", "b"], 'pack(["a", "b"], 3, sep="\\n\\n")')


def test_pack__everything_fits(ex):
    expect(ex.pack(["x", "y", "z"], 100), ["x y z"], 'pack(["x", "y", "z"], 100)')


def test_pack__empty(ex):
    expect(ex.pack([], 10), [], "pack([], 10)")


def test_section_chunks__readme(ex):
    got = ex.section_chunks(REPO["README.md"], "README.md", 300)
    expect(len(got), 4, "number of chunks for README.md (max 300 chars)")
    docker = got[2]
    expect(docker["path"], "README.md", "path of the Docker chunk")
    expect(docker["heading_path"], ["Tiny Shop", "Run with Docker"], "heading_path of the Docker chunk")
    expect(docker["search_text"],
           "Tiny Shop > Run with Docker\nBuild the image, then start the container with docker compose up.\n"
           "The shop listens on port 8000.", "search_text of the Docker chunk")
    expect(docker["text"].startswith("Build the image"), True, "text must not include the heading path")


def test_section_chunks__packs_paragraphs(ex):
    md = "# Guide\n\npara one is here.\n\npara two is here.\n\npara three."
    got = ex.section_chunks(md, "g.md", 40)
    expect([c["text"] for c in got], ["para one is here.\n\npara two is here.", "para three."],
           "texts for 3 paragraphs packed into 40 chars")


def test_section_chunks__no_heading(ex):
    got = ex.section_chunks("just text", "n.md", 50)
    expect(got, [{"path": "n.md", "heading_path": [], "text": "just text", "search_text": "just text"}],
           'section_chunks("just text", "n.md", 50)')
