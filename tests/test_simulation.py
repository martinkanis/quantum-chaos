import numpy as np
import pytest

from montecarlo.metrics import percentile_bands, summarize
from montecarlo.portfolio import Asset, Portfolio, uniform_correlation
from montecarlo.simulation import SimulationParameters, SimulationParametersError, simulate


def single_asset_portfolio(expected_return, volatility):
    asset = Asset(name="A", weight=1.0, expected_return=expected_return, volatility=volatility)
    return Portfolio(assets=(asset,), correlation=np.eye(1))


def make_parameters(**overrides):
    values = dict(initial_value=1000.0, monthly_contribution=0.0, years=2, simulation_count=500, seed=1)
    values.update(overrides)
    return SimulationParameters(**values)


def test_vraci_cesty_se_spravnym_rozmerem_a_pocatecni_hodnotou():
    result = simulate(single_asset_portfolio(0.05, 0.1), make_parameters())

    assert result.paths.shape == (500, 25)
    assert np.all(result.paths[:, 0] == 1000.0)


def test_bez_volatility_roste_deterministicky_o_ocekavany_vynos():
    result = simulate(single_asset_portfolio(0.10, 0.0), make_parameters(years=3))

    np.testing.assert_allclose(result.final_values, 1000.0 * 1.10**3)


def test_mesicni_vklady_se_pricitaji_k_vlozenemu_kapitalu():
    parameters = make_parameters(monthly_contribution=100.0, years=1)
    result = simulate(single_asset_portfolio(0.0, 0.0), parameters)

    assert result.total_contributed == 1000.0 + 12 * 100.0
    np.testing.assert_allclose(result.final_values, 2200.0)


def test_stejny_seed_da_stejne_vysledky():
    portfolio = single_asset_portfolio(0.07, 0.2)

    first = simulate(portfolio, make_parameters(seed=7))
    second = simulate(portfolio, make_parameters(seed=7))

    np.testing.assert_array_equal(first.paths, second.paths)


def test_prumerny_rocni_vynos_odpovida_zadanemu_ocekavanemu_vynosu():
    parameters = make_parameters(years=1, simulation_count=10_000, seed=3)
    result = simulate(single_asset_portfolio(0.08, 0.2), parameters)

    assert result.final_values.mean() / 1000.0 == pytest.approx(1.08, abs=0.01)


def test_diverzifikace_nekorelovanych_aktiv_snizuje_rozptyl():
    assets = tuple(Asset(name=f"A{i}", weight=0.25, expected_return=0.05, volatility=0.2) for i in range(4))
    diversified = Portfolio(assets=assets, correlation=uniform_correlation(4, 0.0))
    concentrated = single_asset_portfolio(0.05, 0.2)
    parameters = make_parameters(simulation_count=5_000)

    assert simulate(diversified, parameters).final_values.std() < simulate(concentrated, parameters).final_values.std()


@pytest.mark.parametrize(
    "overrides",
    [
        dict(initial_value=-1.0),
        dict(monthly_contribution=-1.0),
        dict(initial_value=0.0, monthly_contribution=0.0),
        dict(years=0),
        dict(years=41),
        dict(simulation_count=0),
        dict(simulation_count=10_001),
    ],
)
def test_odmitne_neplatne_parametry(overrides):
    with pytest.raises(SimulationParametersError):
        make_parameters(**overrides)


def test_metriky_rizika_jsou_konzistentni():
    result = simulate(single_asset_portfolio(0.05, 0.25), make_parameters(simulation_count=5_000))
    metrics = summarize(result)

    assert metrics.percentile_5 < metrics.median < metrics.percentile_95
    assert metrics.value_at_risk == pytest.approx(metrics.total_contributed - metrics.percentile_5)
    assert metrics.conditional_value_at_risk >= metrics.value_at_risk
    assert 0.0 < metrics.probability_of_loss < 1.0


def test_cagr_se_nepocita_pri_mesicnich_vkladech():
    result = simulate(single_asset_portfolio(0.05, 0.1), make_parameters(monthly_contribution=50.0))

    assert summarize(result).median_annual_return is None


def test_percentilova_pasma_jsou_serazena():
    result = simulate(single_asset_portfolio(0.05, 0.2), make_parameters())
    bands = percentile_bands(result)

    assert np.all(bands[5] <= bands[50]) and np.all(bands[50] <= bands[95])
