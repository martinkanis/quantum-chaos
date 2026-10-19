from dash import dcc, html

from ui import ids
from ui.literature_review_content import KEY_FINDINGS, REVIEW_QUESTIONS, SOURCES_ANCHOR, TOPICS
from ui.literature_review_page import RELATED_PAGES, REVIEW_QUESTIONS_ANCHOR, build_literature_review_page
from ui.navigation import (
    ACTIVE_LINK_CLASS,
    LITERATURE_REVIEW_PATH,
    NAV_LINK_IDS,
    PAGE_BY_PATH,
    PAGE_IDS,
    PHOTONIC_HARDWARE_PATH,
    literature_review_href,
    show_page,
)
from ui.study_progress import describe_pager
from ui.theory_content import all_sources
from ui.topic_catalog import LITERATURE_REVIEW_TOPIC, RESEARCH_TOPICS, breadcrumb_trail

PAGE_ANCHORS = [topic.anchor for topic in TOPICS] + [REVIEW_QUESTIONS_ANCHOR, SOURCES_ANCHOR]


def section_ids(page):
    return [child.id for child in page.children if getattr(child, "id", None)]


def test_reserse_je_samostatne_tema_na_strance_temat_i_v_horni_liste():
    link_classes = show_page(LITERATURE_REVIEW_PATH)[len(PAGE_IDS):len(PAGE_IDS) + len(NAV_LINK_IDS)]
    active_links = [link_id for link_id, link_class in zip(NAV_LINK_IDS, link_classes) if link_class == ACTIVE_LINK_CLASS]

    assert active_links == [ids.NAV_LITERATURE_REVIEW_LINK]
    assert LITERATURE_REVIEW_TOPIC in RESEARCH_TOPICS
    assert PAGE_BY_PATH[LITERATURE_REVIEW_PATH] == ids.LITERATURE_REVIEW_PAGE
    assert [label for label, _ in breadcrumb_trail(ids.LITERATURE_REVIEW_PAGE)] == [
        "Témata", LITERATURE_REVIEW_TOPIC.title, LITERATURE_REVIEW_TOPIC.pages[0].title,
    ]


def test_kazda_kapitola_reserse_ma_unikatni_kotvu_a_vlastni_sekci():
    page = build_literature_review_page()

    assert section_ids(page) == PAGE_ANCHORS
    assert len(set(PAGE_ANCHORS)) == len(PAGE_ANCHORS)
    assert all(anchor.startswith("reserse-") for anchor in PAGE_ANCHORS if anchor != SOURCES_ANCHOR)


def test_tldr_i_kontrolni_otazky_odkazuji_na_existujici_kapitoly():
    anchors = {topic.anchor for topic in TOPICS}

    assert KEY_FINDINGS and REVIEW_QUESTIONS
    assert {finding.anchor for finding in KEY_FINDINGS} <= anchors
    assert {question.anchor for question in REVIEW_QUESTIONS} <= anchors
    assert set(RELATED_PAGES) <= anchors


def test_kazda_kontrolni_otazka_ma_odpoved_a_kazda_kapitola_zdroj():
    for question in REVIEW_QUESTIONS:
        assert question.question.endswith("?") and question.answer.strip()
    for topic in TOPICS:
        assert topic.in_short.strip() and topic.explanation.strip() and topic.further_reading
    assert len(all_sources(TOPICS)) == len(set(all_sources(TOPICS)))


def test_odpovedi_jsou_schovane_v_rozbalovacich_blocich():
    page = build_literature_review_page()
    review_card = next(child for child in page.children if getattr(child, "id", None) == REVIEW_QUESTIONS_ANCHOR)
    questions = [child for child in review_card.children if isinstance(child, html.Details)]

    assert len(questions) == len(REVIEW_QUESTIONS)
    assert all(isinstance(question.children[0], html.Summary) for question in questions)
    assert all(isinstance(question.children[-1], dcc.Link) for question in questions)
    assert literature_review_href(REVIEW_QUESTIONS_ANCHOR).startswith(LITERATURE_REVIEW_PATH)


def test_reserse_je_prvnim_krokem_sveho_tematu_a_vede_na_fotonicky_hardware():
    style, step_label, links, _, _ = describe_pager(LITERATURE_REVIEW_PATH, None)

    assert step_label.endswith("krok 1 / 2")
    assert links[0].children is None
    assert links[1].children.href == PHOTONIC_HARDWARE_PATH
