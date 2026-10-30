import re

from ui.generated_topics import GENERATED_TOPICS
from ui.layout import build_layout
from ui.lazy_pages import LAZY_PAGE_IDS, built_page
from ui.navigation import PAGE_BY_PATH
from ui.photonics_landscape_content import TOPICS as PHOTONICS_TOPICS
from ui.primer_page import PRIMER_CHAPTERS
from ui.ghz_states_content import TOPICS as GHZ_TOPICS
from ui.psiquantum_content import TOPICS as PSIQUANTUM_TOPICS
from ui.walther_lecture_content import TOPICS as WALTHER_TOPICS

APP_LINK = re.compile(r"\]\((/[^)\s#]*)(?:#([^)\s]+))?\)")
"""A Markdown link to a page of the app, „[text](/cesta#kotva)“; assets/text_links.js opens it inside the app."""


def components(component):
    yield component
    children = getattr(component, "children", None)
    for child in children if isinstance(children, (list, tuple)) else [children]:
        if child is not None and not isinstance(child, str):
            yield from components(child)


def reading_texts():
    for topic in GENERATED_TOPICS:
        yield topic.in_short
        yield from (section.body for section in topic.sections)
    for chapter in PRIMER_CHAPTERS.values():
        yield chapter.intro
        yield from (section.body for section in chapter.sections)
    for topic in (*PHOTONICS_TOPICS, *WALTHER_TOPICS, *GHZ_TOPICS, *PSIQUANTUM_TOPICS):
        yield topic.in_short
        yield topic.explanation


def page_ids_on(page_id):
    page = built_page(page_id) if page_id in LAZY_PAGE_IDS else next(
        component for component in components(build_layout()) if getattr(component, "id", None) == page_id
    )
    return {getattr(component, "id", None) for component in components(page)}


def test_odkazy_v_textech_vedou_na_existujici_stranky_a_kotvy():
    links = sorted({link for text in reading_texts() for link in APP_LINK.findall(text)})

    assert links
    for path, anchor in links:
        assert path in PAGE_BY_PATH, f"Odkaz na neexistující stránku {path}"
        if anchor:
            assert anchor in page_ids_on(PAGE_BY_PATH[path]), f"Odkaz na neexistující kotvu {path}#{anchor}"
