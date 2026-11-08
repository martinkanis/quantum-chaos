import pytest
from dash import no_update

from gbs.benchmark_problems import find_benchmark
from gbs.loss_study import run_loss_study
from gbs.photon_loss import PhotonLossError
from gbs.photon_tuning import TuningMode
from ui import ids
from ui.knowledge_map_content import MAP_LABELS, RELATIONS
from ui.navigation import ADVANTAGE_PATH, FAILURE_DIAGNOSTICS_PATH, PHOTON_LOSS_PATH, PORTFOLIO_PATH
from ui.photon_loss_callbacks import describe_problem, parse_transmission, should_run_lab
from ui.photon_loss_content import (
    BENCHMARK_STUDIES,
    CORRECTION,
    EXAMPLE,
    EXAMPLE_TRANSMISSION,
    IN_SHORT,
    LAB_ANCHOR,
    NAIVE_BIAS,
    SIMULABILITY,
    SOURCES_ANCHOR,
    THRESHOLD_DETECTORS,
    TOPICS,
    advantage_table,
    bias_table,
    collision_free_click_ratios,
    signed_percent,
    typical_bench_transmission,
)
from ui.photon_loss_page import DEFAULT_TRANSMISSION_PERCENT, build_photon_loss_page
from ui.photon_loss_results import build_photon_loss_results
from ui.theory_content import all_sources
from ui.topic_catalog import RESEARCH_DIRECTIONS_TOPIC, breadcrumb_trail
from tests.test_random_matrix_page import section_ids
from tests.test_topics import active_links, links_in, visible_pages


def test_stranka_ztrat_je_podstrankou_diagnostiky_ve_vlastnim_vyzkumu():
    assert visible_pages(PHOTON_LOSS_PATH) == [ids.PHOTON_LOSS_PAGE]
    assert active_links(PHOTON_LOSS_PATH) == [ids.NAV_RESEARCH_MENU]
    assert [label for label, _ in breadcrumb_trail(ids.PHOTON_LOSS_PAGE)] == [
        "Témata", "Vlastní výzkum", "Kdy odhad rizika přes GBS selže", "Ztráty fotonů: čtvrtý zdroj chyby",
    ]
    assert breadcrumb_trail(ids.PHOTON_LOSS_PAGE)[2][1] == FAILURE_DIAGNOSTICS_PATH
    assert ids.PHOTON_LOSS_PAGE in {page.page_id for page in RESEARCH_DIRECTIONS_TOPIC.pages}
    assert MAP_LABELS[ids.PHOTON_LOSS_PAGE] == "Ztráty fotonů"
    assert any(ids.PHOTON_LOSS_PAGE in (relation.source, relation.target) for relation in RELATIONS)


def test_kazda_kapitola_ma_unikatni_kotvu_shrnuti_vyklad_a_zdroje():
    anchors = [topic.anchor for topic in TOPICS]
    page = build_photon_loss_page()

    assert set(anchors + [SOURCES_ANCHOR, LAB_ANCHOR]) <= set(section_ids(page))
    assert len(set(anchors)) == len(anchors)
    assert all(anchor.startswith("zt-") for anchor in anchors)
    for topic in TOPICS:
        assert topic.in_short.strip() and topic.explanation.strip() and topic.further_reading
    assert len(all_sources(TOPICS)) == len(set(all_sources(TOPICS)))
    assert {FAILURE_DIAGNOSTICS_PATH, ADVANTAGE_PATH} <= set(links_in(page))


def flattened(text):
    """Markdown joins the lines of a paragraph, so the tests compare phrases the same way."""
    return " ".join(text.split())


def test_cisla_v_textech_odpovidaji_vypoctu():
    small = next(point for point in EXAMPLE.sweep if point.transmission == 0.99)
    moderate = next(point for point in EXAMPLE.sweep if point.transmission == EXAMPLE_TRANSMISSION)

    assert small.naive_bias == pytest.approx(-0.071, abs=0.001)
    assert moderate.naive_bias == pytest.approx(-0.271, abs=0.001)
    assert "o 7 % už při 1 % ztrát a o 27 % při 10 % ztrát" in IN_SHORT
    assert "z 880× na 12×" in IN_SHORT and "330× víc výstřelů" in IN_SHORT
    assert "η_c ≈ 0,49" in IN_SHORT and "kolem 1 %" in IN_SHORT
    assert "z 880× na 12×" in CORRECTION.in_short
    assert "| 2 · E[X₁⁸X₂⁸] | 16 | −7 % | −22 % | −27 % |" in bias_table()
    assert "| 2 · E[X₁⁸X₂⁸] | 880× méně | 210× méně | 12× méně | 330× víc |" in advantage_table()
    assert "odhad 12× vyšší než správná hodnota" in flattened(THRESHOLD_DETECTORS.explanation)
    assert collision_free_click_ratios()[1] == pytest.approx(2.33, abs=0.01)
    assert "2,3× vyšší" in THRESHOLD_DETECTORS.in_short
    assert "kliků 5,4× vyšší než $p(1, 1)$ a odhad 2,3× vyšší" in flattened(THRESHOLD_DETECTORS.explanation)
    assert "mezi 0,7 % a 1,4 % propustnosti" in flattened(SIMULABILITY.explanation)
    assert "propustnost kolem 43 %" in flattened(CORRECTION.explanation)
    assert typical_bench_transmission(2) == pytest.approx(0.431, abs=0.001)
    assert bias_table() in NAIVE_BIAS.explanation and advantage_table() in CORRECTION.explanation


def test_vychozi_propustnost_odpovida_prikladu_v_textech():
    assert DEFAULT_TRANSMISSION_PERCENT / 100 == EXAMPLE_TRANSMISSION
    assert set(BENCHMARK_STUDIES) == {"extremni-moment", "spolecny-extrem", "nesoumerny-monom", "historie-usa",
                                      "trzni-faktor"}


def test_laborator_bezi_po_kliknuti_nebo_pri_prvnim_zobrazeni_stranky():
    assert should_run_lab(ids.PHOTON_LOSS_RUN_BUTTON, PORTFOLIO_PATH, current_results=["hotovo"])
    assert should_run_lab(None, PHOTON_LOSS_PATH, current_results=None)
    assert not should_run_lab(ids.URL, PHOTON_LOSS_PATH, current_results=["hotovo"])
    assert not should_run_lab(None, PORTFOLIO_PATH, current_results=None)


def test_popis_ulohy_a_propustnost_se_prevedou_z_formulare():
    assert "1928–2023" in describe_problem("historie-usa")
    assert describe_problem("neexistuje") is no_update
    assert parse_transmission(90) == pytest.approx(0.9)
    with pytest.raises(PhotonLossError, match="posuvníkem"):
        parse_transmission(None)


def boundary_tiles(results):
    boundaries = results.children[3]
    return boundaries.children[1].children


@pytest.mark.parametrize("transmission", [1.0, 0.9, 0.3])
def test_vysledky_laboratore_se_vykresli(transmission):
    study = run_loss_study(find_benchmark("historie-usa").problem, TuningMode.PER_MODE, transmission)

    results = build_photon_loss_results(study, typical_bench_transmission(3))

    assert len(results.children) == 5
    assert len(boundary_tiles(results)) == 4
    assert len(boundary_tiles(build_photon_loss_results(study, bench_transmission=None))) == 3


def test_procenta_se_znamenkem_jsou_cesky():
    assert signed_percent(-0.271) == "−27 %"
    assert signed_percent(0.12345, 1) == "+12,3 %"
