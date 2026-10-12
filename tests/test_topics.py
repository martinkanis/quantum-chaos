from dash import dcc

from ui import ids
from ui.academy_page import ACADEMY_SECTIONS, build_academy_page
from ui.breadcrumbs import describe_location
from ui.navigation import (
    ACADEMY_PATH,
    ACTIVE_LINK_CLASS,
    GUIDE_PATH,
    NAV_LINK_IDS,
    PAGE_BY_PATH,
    PAGE_IDS,
    PORTFOLIO_PATH,
    TOPICS_PATH,
    VISIBLE,
    show_page,
)
from ui.topic_catalog import MONTE_CARLO_TOPIC, RESEARCH_TOPICS, breadcrumb_trail
from ui.topics_page import build_topics_page


def visible_pages(pathname):
    styles = show_page(pathname)[: len(PAGE_IDS)]
    return [page_id for page_id, style in zip(PAGE_IDS, styles) if style == VISIBLE]


def active_links(pathname):
    link_classes = show_page(pathname)[len(PAGE_IDS):]
    return [link_id for link_id, link_class in zip(NAV_LINK_IDS, link_classes) if link_class == ACTIVE_LINK_CLASS]


def links_in(component):
    if isinstance(component, dcc.Link):
        yield component.href
    children = getattr(component, "children", None)
    for child in children if isinstance(children, list) else [children]:
        if child is not None and not isinstance(child, str):
            yield from links_in(child)


def test_uvodni_strankou_jsou_temata_a_vedle_nich_quantum_academy():
    assert visible_pages(TOPICS_PATH) == [ids.TOPICS_PAGE]
    assert visible_pages(ACADEMY_PATH) == [ids.ACADEMY_PAGE]
    assert visible_pages(PORTFOLIO_PATH) == [ids.PORTFOLIO_PAGE]
    assert active_links(TOPICS_PATH) == [ids.NAV_TOPICS_LINK]
    assert active_links(ACADEMY_PATH) == [ids.NAV_ACADEMY_LINK]


def test_tema_monte_carlo_obsahuje_vsechny_stranky_aplikace():
    topic_pages = {page.page_id for topic in RESEARCH_TOPICS for page in topic.pages}

    assert topic_pages == set(PAGE_IDS) - {ids.TOPICS_PAGE, ids.ACADEMY_PAGE}
    assert all(PAGE_BY_PATH[page.path] == page.page_id for page in MONTE_CARLO_TOPIC.pages)


def test_stranka_temat_odkazuje_na_kazdou_stranku_tematu():
    links = set(links_in(build_topics_page()))

    assert {page.path for page in MONTE_CARLO_TOPIC.pages} | {ACADEMY_PATH} <= links


def test_drobeckova_navigace_ukaze_tema_i_nadrazenou_stranku():
    trail = breadcrumb_trail(ids.GUIDE_PAGE)

    assert [label for label, _ in trail] == [
        "Témata", "Monte Carlo a modifikované Monte Carlo", "3 · Výhoda GBS", "Průvodce pro začínajícího doktoranda",
    ]
    assert trail[-1][1] is None
    assert describe_location(GUIDE_PATH)[1] == VISIBLE
    assert describe_location(TOPICS_PATH)[0] == []
    assert describe_location(ACADEMY_PATH)[0] == []


def test_quantum_academy_odkazuje_na_quantum_country_looking_glass_a_shtetl_optimized():
    urls = {link.url for section in ACADEMY_SECTIONS for link in section.links}

    assert {
        "https://quantum.country", "https://www.youtube.com/@LookingGlassUniverse", "https://scottaaronson.blog",
    } <= urls
    assert build_academy_page().id == ids.ACADEMY_PAGE
