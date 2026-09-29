import numpy as np
import pytest

from gbs.demo import DemoParametersError, run_gbs_demo, sample_sizes_up_to
from gbs.expectation import MomentProblem
from ui import ids
from ui.caveats_content import CAVEATS
from ui.caveats_page import build_caveats_page
from ui.form_parsing import DEFAULT_ASSET_ROWS, asset_names, build_portfolio, default_correlation_rows
from ui.gbs_callbacks import should_run
from ui.gbs_results import build_gbs_results, monomial_label, wick_formula
from ui.navigation import (
    ACTIVE_LINK_CLASS,
    CAVEATS_PATH,
    GBS_PATH,
    NAV_LINK_IDS,
    PAGE_IDS,
    PORTFOLIO_PATH,
    THEORY_PATH,
    VISIBLE,
    caveat_href,
    show_page,
    theory_href,
)
from ui.theory_content import TOPICS
from ui.theory_page import build_theory_page

NAMES = asset_names(DEFAULT_ASSET_ROWS)


def default_problem(degree):
    portfolio = build_portfolio(DEFAULT_ASSET_ROWS, default_correlation_rows(NAMES, 0.2))
    return MomentProblem(covariance=portfolio.covariance(), weights=portfolio.weights, degree=degree)


def test_velikosti_vzorku_rostou_az_do_maxima():
    sizes = sample_sizes_up_to(100_000)

    assert sizes[0] == 100 and sizes[-1] == 100_000
    assert np.all(np.diff(sizes) > 0)


@pytest.mark.parametrize("max_sample_size", [100, 2_000_000])
def test_odmitne_pocet_vzorku_mimo_rozsah(max_sample_size):
    with pytest.raises(DemoParametersError):
        sample_sizes_up_to(max_sample_size)


@pytest.mark.parametrize("degree", [2, 4, 6])
def test_vysledky_gbs_stranky_se_vykresli(degree):
    run = run_gbs_demo(default_problem(degree), squeezing_strength=0.7, max_sample_size=10_000, seed=42)

    results = build_gbs_results(run, NAMES)

    assert len(results.children) == 6


def test_stejny_seed_da_stejny_gbs_beh():
    first = run_gbs_demo(default_problem(4), squeezing_strength=0.7, max_sample_size=10_000, seed=1)
    second = run_gbs_demo(default_problem(4), squeezing_strength=0.7, max_sample_size=10_000, seed=1)

    np.testing.assert_array_equal(first.study.gbs_trajectory, second.study.gbs_trajectory)


def visible_pages(pathname):
    styles = show_page(pathname)[: len(PAGE_IDS)]
    return [page_id for page_id, style in zip(PAGE_IDS, styles) if style == VISIBLE]


def active_links(pathname):
    link_classes = show_page(pathname)[len(PAGE_IDS):]
    return [link_id for link_id, link_class in zip(NAV_LINK_IDS, link_classes) if link_class == ACTIVE_LINK_CLASS]


def test_navigace_ukaze_prave_jednu_stranku_podle_adresy():
    assert visible_pages(PORTFOLIO_PATH) == [ids.PORTFOLIO_PAGE]
    assert visible_pages(GBS_PATH) == [ids.GBS_PAGE]
    assert visible_pages(CAVEATS_PATH) == [ids.CAVEATS_PAGE]
    assert visible_pages(THEORY_PATH) == [ids.THEORY_PAGE]
    assert visible_pages("/neexistuje") == [ids.PORTFOLIO_PAGE]


def test_podstranky_gbs_zvyrazni_v_navigaci_gbs():
    assert active_links(CAVEATS_PATH) == [ids.NAV_GBS_LINK]
    assert active_links(THEORY_PATH) == [ids.NAV_GBS_LINK]


def test_kazdy_hacek_ma_unikatni_kotvu_a_vlastni_sekci():
    anchors = [caveat.anchor for caveat in CAVEATS]
    page = build_caveats_page()
    section_ids = [child.id for child in page.children if getattr(child, "id", None)]

    assert len(set(anchors)) == len(anchors)
    assert section_ids == anchors
    assert caveat_href(anchors[0]) == f"{CAVEATS_PATH}#{anchors[0]}"


def test_kazdy_hacek_ma_shrnuti_vysvetleni_i_doporuceni():
    for caveat in CAVEATS:
        assert caveat.summary.strip() and caveat.explanation.strip() and caveat.remedies.strip()


def test_gbs_simulace_bezi_po_kliknuti_nebo_pri_prvnim_zobrazeni_stranky():
    assert should_run(ids.GBS_RUN_BUTTON, PORTFOLIO_PATH, current_results=["hotovo"])
    assert should_run(None, GBS_PATH, current_results=None)
    assert not should_run(ids.URL, GBS_PATH, current_results=["hotovo"])
    assert not should_run(None, PORTFOLIO_PATH, current_results=None)


def test_kazde_tema_teorie_ma_unikatni_kotvu_a_vlastni_sekci():
    anchors = [topic.anchor for topic in TOPICS]
    page = build_theory_page()
    section_ids = [child.id for child in page.children if getattr(child, "id", None)]

    assert len(set(anchors)) == len(anchors)
    assert section_ids == anchors
    assert theory_href(anchors[0]) == f"{THEORY_PATH}#{anchors[0]}"


def test_kazde_tema_teorie_ma_shrnuti_vyklad_i_literaturu():
    for topic in TOPICS:
        assert topic.in_short.strip() and topic.explanation.strip() and topic.further_reading.strip()


def test_monom_a_wickuv_rozklad_se_zobrazi_citelne():
    assert monomial_label([2, 1, 0]) == "X₁²X₂"
    assert wick_formula([2, 2, 0]) == "Σ₁₁Σ₂₂ + 2Σ₁₂²"
    assert wick_formula([4, 0, 0]) == "3Σ₁₁²"
    assert wick_formula([2, 1, 1]) == "Σ₁₁Σ₂₃ + 2Σ₁₂Σ₁₃"
