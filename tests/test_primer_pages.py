import re
from collections import Counter

from ui import ids
from ui.academy_page import ACADEMY_SECTIONS
from ui.navigation import PAGE_BY_PATH, PRIMER_APPENDICES_PATH, PRIMER_BASICS_PATH, PRIMER_GBS_PATH
from ui.primer_content import BIBLIOGRAPHY
from ui.primer_page import PRIMER_CHAPTERS, build_primer_page, cited_numbers, markdown_text, section_heading
from ui.study_progress import describe_pager
from ui.topic_catalog import PHOTONICS_TOPIC, breadcrumb_trail, study_path

TAG = re.compile(r"\\tag\{([^}]*)\}")
SWALLOWED_BRACKET = re.compile(r"\\begin\{\w+\}\s*\[")
"""MathJax reads a bracket right after \\begin{aligned} as its option and drops it; {}[ keeps it."""
FORBIDDEN = ("\\boldsymbol", "\\bm{", "\\coloneqq", "\\eqref", "\\ref{", "\\label", "\\unicode", "\\ket", "\\bra{",
             "\\braket", "\\[", "\\]")
CHAPTER_PREFIXES = {
    ids.PRIMER_BASICS_PAGE: ("1",),
    ids.PRIMER_GAUSSIAN_STATES_PAGE: ("2",),
    ids.PRIMER_PHASE_SPACE_PAGE: ("3",),
    ids.PRIMER_GBS_PAGE: ("4",),
    ids.PRIMER_APPENDICES_PAGE: ("A", "B"),
}


def texts(chapter):
    return [chapter.intro] + [section.body for section in chapter.sections]


def tags(chapter):
    return [tag for text in texts(chapter) for tag in TAG.findall(text)]


def display_blocks(text):
    """Contents of the $$ … $$ blocks, whose delimiters must stand on lines of their own."""
    blocks, current = [], None
    for line in text.split("\n"):
        if line.strip() == "$$":
            if current is None:
                current = []
            else:
                blocks.append("\n".join(current))
                current = None
        elif current is not None:
            current.append(line)
    assert current is None, "neuzavřený blok $$"
    return blocks


def test_kapitoly_maji_sekce_s_unikatnimi_kotvami_v_poradi_originalu():
    anchors = [section.anchor for chapter in PRIMER_CHAPTERS.values() for section in chapter.sections]

    assert list(PRIMER_CHAPTERS) == [
        ids.PRIMER_BASICS_PAGE, ids.PRIMER_GAUSSIAN_STATES_PAGE, ids.PRIMER_PHASE_SPACE_PAGE, ids.PRIMER_GBS_PAGE,
        ids.PRIMER_APPENDICES_PAGE,
    ]
    assert all(anchor.startswith("skripta-") for anchor in anchors) and len(anchors) == len(set(anchors))
    assert all(section.body.strip() and section.title for chapter in PRIMER_CHAPTERS.values()
               for section in chapter.sections)
    for page_id, chapter in PRIMER_CHAPTERS.items():
        numbered = [section.number for section in chapter.sections if section.number]
        assert all(number.startswith(CHAPTER_PREFIXES[page_id]) for number in numbered), page_id


def test_rovnice_jsou_cislovane_jako_v_originalu_bez_mezer_a_opakovani():
    every_tag = [tag for chapter in PRIMER_CHAPTERS.values() for tag in tags(chapter)]

    assert len(every_tag) == len(set(every_tag)), [tag for tag, count in Counter(every_tag).items() if count > 1]
    for page_id, chapter in PRIMER_CHAPTERS.items():
        for prefix in CHAPTER_PREFIXES[page_id]:
            numbers = [int(re.match(r"\d+", tag.split(".")[1]).group())
                       for tag in tags(chapter) if tag.split(".")[0] == prefix]
            # Sub-equations such as (3.8a) and (3.8b) share their number.
            distinct = [number for index, number in enumerate(numbers) if not index or number != numbers[index - 1]]
            if distinct:
                assert distinct == list(range(1, max(distinct) + 1)), (page_id, prefix)


def test_vzorce_pouzivaji_jen_to_co_mathjax_v_aplikaci_umi():
    for chapter in PRIMER_CHAPTERS.values():
        for text in texts(chapter):
            blocks = display_blocks(text)
            assert all(len(TAG.findall(block)) <= 1 for block in blocks)
            assert len(TAG.findall(text)) == sum(len(TAG.findall(block)) for block in blocks)
            assert not [macro for macro in FORBIDDEN if macro in text], chapter.label
            assert not SWALLOWED_BRACKET.search(text), (chapter.label, SWALLOWED_BRACKET.search(text))
            assert all(line.strip() == "$$" for line in text.split("\n") if "$$" in line), chapter.label
            assert '"""' not in text


def test_citace_odkazuji_na_existujici_literaturu_originalu():
    for chapter in PRIMER_CHAPTERS.values():
        assert all(1 <= number <= len(BIBLIOGRAPHY) for number in cited_numbers(chapter)), chapter.label
    assert 29 in cited_numbers(PRIMER_CHAPTERS[ids.PRIMER_BASICS_PAGE])


def test_stranky_kapitol_maji_obsah_sekce_a_citovanou_literaturu():
    for page_id, chapter in PRIMER_CHAPTERS.items():
        page = build_primer_page(page_id)
        section_ids = [child.id for child in page.children if getattr(child, "id", None)]

        assert section_ids == [section.anchor for section in chapter.sections]
        assert page.children[1].children.startswith(chapter.label)
    assert section_heading(PRIMER_CHAPTERS[ids.PRIMER_APPENDICES_PAGE].sections[-1]).startswith("Dodatek B: ")


def test_skripta_jsou_prvnich_pet_kroku_tematu_fotonika_a_vede_na_ne_akademie():
    path = [page.page_id for page in study_path(PHOTONICS_TOPIC)]
    _, step_label, _, _, _ = describe_pager(PRIMER_BASICS_PATH, None)
    academy = next(section for section in ACADEMY_SECTIONS if section.title.startswith("Fotonika"))

    assert path[:5] == list(PRIMER_CHAPTERS)
    assert path[5:] == [
        ids.PHOTONICS_LANDSCAPE_PAGE, ids.PSIQUANTUM_PAGE, ids.PIQUASSO_PAGE, ids.WALTHER_LECTURE_PAGE,
        ids.GHZ_STATES_PAGE,
    ]
    assert step_label == "Fotonika · krok 1 / 10"
    assert PAGE_BY_PATH[PRIMER_GBS_PATH] == ids.PRIMER_GBS_PAGE
    assert all(path_ in academy.tldr for path_, page_id in PAGE_BY_PATH.items() if page_id in PRIMER_CHAPTERS)
    assert PRIMER_APPENDICES_PATH in academy.tldr
    assert [label for label, _ in breadcrumb_trail(ids.PRIMER_GBS_PAGE)] == [
        "Témata", "Fotonika a GBS", "Skripta 4: Gaussian Boson Sampling",
    ]


def test_hranate_zavorky_mimo_vzorce_kod_a_odkazy_zustanou_v_textu_videt():
    text = "Viz [29] a [Na obrázku: $\\theta_1$ až $[a, b]$] a [web](https://app.piquasso.com/).\n$$\n[x, p]\n$$\n`[0, 1]`"

    assert markdown_text(text) == (
        "Viz \\[29\\] a \\[Na obrázku: $\\theta_1$ až $[a, b]$\\] a [web](https://app.piquasso.com/).\n"
        "$$\n[x, p]\n$$\n`[0, 1]`"
    )
