from dash import dcc

from ui import ids
from ui.navigation import CAVEATS_PATH, GBS_PATH, HIDDEN, THEORY_PATH, TOPICS_PATH, VISIBLE
from ui.reading_time import WORDS_PER_MINUTE, reading_minutes
from ui.study_progress import NOT_STUDIED_LABEL, STUDIED_LABEL, describe_pager, toggle_current_page, toggle_page
from ui.topic_catalog import MONTE_CARLO_TOPIC, next_unstudied_page, study_path, study_step
from ui.topics_page import progress_label, topic_cards

ALL_TOPIC_PAGE_IDS = [page.page_id for page in study_path(MONTE_CARLO_TOPIC)]


def texts_in(component):
    if isinstance(component, str):
        yield component
        return
    children = getattr(component, "children", None)
    for child in children if isinstance(children, list) else [children]:
        if child is not None:
            yield from texts_in(child)


def hrefs_in(component):
    if isinstance(component, dcc.Link):
        yield component.href
    children = getattr(component, "children", None)
    for child in children if isinstance(children, list) else [children]:
        if child is not None and not isinstance(child, str):
            yield from hrefs_in(child)


def test_doporucene_poradi_radi_podstranky_hned_za_stranku_kterou_vysvetluji():
    assert ALL_TOPIC_PAGE_IDS == [
        ids.PORTFOLIO_PAGE, ids.GBS_PAGE, ids.THEORY_PAGE, ids.CAVEATS_PAGE, ids.ADVANTAGE_PAGE, ids.GUIDE_PAGE,
    ]


def test_krok_studia_zna_predchozi_a_dalsi_stranku():
    step = study_step(ids.THEORY_PAGE)

    assert (step.number, step.total) == (3, 6)
    assert step.previous.page_id == ids.GBS_PAGE
    assert step.next.page_id == ids.CAVEATS_PAGE
    assert study_step(ids.PORTFOLIO_PAGE).previous is None
    assert study_step(ids.GUIDE_PAGE).next is None
    assert study_step(ids.TOPICS_PAGE) is None


def test_oznaceni_stranky_jako_prostudovane_se_prepina():
    assert toggle_page([], ids.GBS_PAGE) == [ids.GBS_PAGE]
    assert toggle_page([ids.GBS_PAGE, ids.THEORY_PAGE], ids.GBS_PAGE) == [ids.THEORY_PAGE]
    assert toggle_current_page(1, THEORY_PATH, None) == [ids.THEORY_PAGE]


def test_stranku_mimo_temata_nejde_oznacit():
    assert toggle_current_page(1, TOPICS_PATH, [ids.GBS_PAGE]) == [ids.GBS_PAGE]


def test_karta_dalsiho_kroku_je_jen_na_strankach_temat():
    assert describe_pager(TOPICS_PATH, None)[0] == HIDDEN

    style, step_label, links, button_label, _ = describe_pager(GBS_PATH, [ids.GBS_PAGE])

    assert style == VISIBLE
    assert step_label.endswith("krok 2 / 6")
    assert list(hrefs_in(links[0])) == [MONTE_CARLO_TOPIC.pages[0].path]
    assert list(hrefs_in(links[1])) == [THEORY_PATH]
    assert button_label == STUDIED_LABEL
    assert describe_pager(CAVEATS_PATH, [])[3] == NOT_STUDIED_LABEL


def test_tema_nabidne_dalsi_neprostudovanou_stranku_a_ukaze_postup():
    cards = topic_cards([ids.PORTFOLIO_PAGE, ids.THEORY_PAGE])
    texts = " ".join(text for card in cards for text in texts_in(card))

    assert next_unstudied_page(MONTE_CARLO_TOPIC, [ids.PORTFOLIO_PAGE]).page_id == ids.GBS_PAGE
    assert next_unstudied_page(MONTE_CARLO_TOPIC, ALL_TOPIC_PAGE_IDS) is None
    assert progress_label(2, 6) in texts
    assert "Pokračuj: 2 · Monte Carlo na GBS →" in texts


def test_doba_cteni_se_odvozuje_z_poctu_slov():
    assert reading_minutes(["slovo " * WORDS_PER_MINUTE]) == 1
    assert reading_minutes(["slovo " * (WORDS_PER_MINUTE + 1)]) == 2
    assert reading_minutes([""]) == 1
