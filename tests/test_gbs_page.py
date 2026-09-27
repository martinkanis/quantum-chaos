import numpy as np
import pytest

from gbs.demo import DemoParametersError, run_gbs_demo, sample_sizes_up_to
from gbs.expectation import MomentProblem
from ui import ids
from ui.form_parsing import DEFAULT_ASSET_ROWS, asset_names, build_portfolio, default_correlation_rows
from ui.gbs_callbacks import should_run
from ui.gbs_results import build_gbs_results
from ui.navigation import GBS_PATH, HIDDEN, PORTFOLIO_PATH, VISIBLE, show_page

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


def test_navigace_ukaze_gbs_stranku_jen_na_jeji_adrese():
    assert show_page(GBS_PATH)[:2] == (HIDDEN, VISIBLE)
    assert show_page(PORTFOLIO_PATH)[:2] == (VISIBLE, HIDDEN)
    assert show_page("/neexistuje")[:2] == (VISIBLE, HIDDEN)


def test_gbs_simulace_bezi_po_kliknuti_nebo_pri_prvnim_zobrazeni_stranky():
    assert should_run(ids.GBS_RUN_BUTTON, PORTFOLIO_PATH, current_results=["hotovo"])
    assert should_run(None, GBS_PATH, current_results=None)
    assert not should_run(ids.URL, GBS_PATH, current_results=["hotovo"])
    assert not should_run(None, PORTFOLIO_PATH, current_results=None)
