import pytest

from randommatrix.factor_market import FactorMarket
from randommatrix.marchenko_pastur import NoiseBand
from randommatrix.study import run_study
from ui import ids
from ui.failure_diagnostics_content import DIAGNOSTIC_TOOLS
from ui.navigation import PORTFOLIO_PATH, RANDOM_MATRIX_PATH, failure_diagnostics_href, show_page
from ui.random_matrix_callbacks import should_run_lab
from ui.random_matrix_content import (
    DETERMINISTIC_CHAOS,
    IN_SHORT,
    MARCHENKO_PASTUR_TOPIC,
    MARKOWITZ,
    SOURCES_ANCHOR,
    TOPICS,
)
from ui.random_matrix_page import build_random_matrix_page
from ui.random_matrix_results import build_random_matrix_results
from ui.theory_content import all_sources
from ui.topic_catalog import RANDOM_MATRIX_TOPIC, RESEARCH_TOPICS, breadcrumb_trail
from tests.test_topics import active_links, links_in, visible_pages


def section_ids(component):
    if getattr(component, "id", None) and type(component).__name__ == "Section":
        yield component.id
    children = getattr(component, "children", None)
    for child in children if isinstance(children, list) else [children]:
        if child is not None and not isinstance(child, str):
            yield from section_ids(child)


def test_stranka_nahodnych_matic_je_samostatnym_tematem_v_horni_liste():
    assert visible_pages(RANDOM_MATRIX_PATH) == [ids.RANDOM_MATRIX_PAGE]
    assert active_links(RANDOM_MATRIX_PATH) == [ids.NAV_RANDOM_MATRIX_LINK]
    assert RANDOM_MATRIX_TOPIC in RESEARCH_TOPICS
    assert [label for label, _ in breadcrumb_trail(ids.RANDOM_MATRIX_PAGE)][:2] == ["Témata", RANDOM_MATRIX_TOPIC.title]
    assert show_page(RANDOM_MATRIX_PATH)[-1] != show_page(PORTFOLIO_PATH)[-1]


def test_kazda_kapitola_ma_unikatni_kotvu_shrnuti_vyklad_a_zdroj():
    anchors = [topic.anchor for topic in TOPICS]

    assert set(anchors + [SOURCES_ANCHOR]) <= set(section_ids(build_random_matrix_page()))
    assert len(set(anchors)) == len(anchors)
    assert all(anchor.startswith("nm-") for anchor in anchors)
    for topic in TOPICS:
        assert topic.in_short.strip() and topic.explanation.strip() and topic.further_reading
    assert len(all_sources(TOPICS)) == len(set(all_sources(TOPICS)))


def test_cisla_v_textech_odpovidaji_vypoctu():
    band = NoiseBand(400 / 1000)

    assert (round(band.lower, 2), round(band.upper, 2)) == (0.14, 2.66)
    assert "od 0,14 do 2,66" in MARCHENKO_PASTUR_TOPIC.explanation
    assert "q = 0,5 tedy 0,5× a 2×" in MARKOWITZ.in_short
    assert "q = N/T = 0,5 slibuje polovinu nejmenšího možného rozptylu a dodá dvojnásobek" in IN_SHORT


def test_laborator_bezi_po_kliknuti_nebo_pri_prvnim_zobrazeni_stranky():
    assert should_run_lab(ids.RANDOM_MATRIX_RUN_BUTTON, PORTFOLIO_PATH, current_results=["hotovo"])
    assert should_run_lab(None, RANDOM_MATRIX_PATH, current_results=None)
    assert not should_run_lab(ids.URL, RANDOM_MATRIX_PATH, current_results=["hotovo"])
    assert not should_run_lab(None, PORTFOLIO_PATH, current_results=None)


@pytest.mark.parametrize("asset_count, observation_count", [(50, 250), (400, 500)])
def test_vysledky_laboratore_se_vykresli(asset_count, observation_count):
    results = build_random_matrix_results(run_study(FactorMarket(asset_count), observation_count, seed=42))

    assert len(results.children) == 3


def test_kapitola_o_chaosu_odlisuje_predpoved_od_diagnostiky_a_odkazuje_na_ni():
    assert failure_diagnostics_href(DIAGNOSTIC_TOOLS.anchor) in set(links_in(build_random_matrix_page()))
    assert "Dvě různé otázky" in DETERMINISTIC_CHAOS.explanation
    assert "Výjimkou je 0-1 test chaosu" in DETERMINISTIC_CHAOS.explanation
