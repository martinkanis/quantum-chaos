import pytest

from montecarlo.historical_returns import (
    ANNUAL_RETURNS_PERCENT,
    FIRST_YEAR,
    LAST_YEAR,
    AssetClass,
    annual_returns,
    period_statistics,
)
from montecarlo.presets import DEFAULT_CLASSES, DEFAULT_PRESET, MARKET_PRESETS
from montecarlo.scenarios import STRESS_SCENARIOS, StressScenario, portfolio_return

DEFAULT_WEIGHTS = [0.6, 0.3, 0.1]
DEFAULT_PORTFOLIO_CLASSES = [AssetClass.STOCKS, AssetClass.BONDS, AssetClass.GOLD]


def test_historicka_data_pokryvaji_kazdy_rok_1928_az_2023():
    assert (FIRST_YEAR, LAST_YEAR) == (1928, 2023)
    assert sorted(ANNUAL_RETURNS_PERCENT) == list(range(1928, 2024))


def test_rocni_vynosy_jsou_v_desetinnych_cislech():
    assert annual_returns(2008) == {
        AssetClass.STOCKS: -0.3655,
        AssetClass.BILLS: 0.0137,
        AssetClass.BONDS: 0.201,
        AssetClass.CORPORATE_BONDS: -0.0354,
        AssetClass.REAL_ESTATE: -0.12,
        AssetClass.GOLD: 0.0432,
    }


def test_vychozi_portfolio_by_v_roce_2008_ztratilo_asi_15_procent():
    scenario = next(scenario for scenario in STRESS_SCENARIOS if scenario.year == 2008)

    assert portfolio_return(DEFAULT_WEIGHTS, DEFAULT_PORTFOLIO_CLASSES, scenario) == pytest.approx(-0.15468)


def test_vlastni_scenar_pocita_kazde_aktivum_podle_jeho_tridy():
    scenario = StressScenario(
        name="Jen akcie padají",
        returns={AssetClass.STOCKS: -0.2, AssetClass.BONDS: 0.0, AssetClass.GOLD: 0.0},
    )

    assert portfolio_return([0.5, 0.5], [AssetClass.STOCKS, AssetClass.STOCKS], scenario) == pytest.approx(-0.2)


def test_katalog_ma_20_historickych_let_s_popisem_a_daty_ze_zdroje():
    years = [scenario.year for scenario in STRESS_SCENARIOS]

    assert len(STRESS_SCENARIOS) == 20
    assert years == sorted(set(years))
    for scenario in STRESS_SCENARIOS:
        assert scenario.name and scenario.description
        assert scenario.returns == annual_returns(scenario.year)


def test_statistiky_obdobi_odpovidaji_rocnim_vynosum():
    statistics = period_statistics([2021, 2022])

    assert statistics.expected_returns[AssetClass.STOCKS] == pytest.approx((0.2847 - 0.1804) / 2)
    assert statistics.correlations[(AssetClass.STOCKS, AssetClass.BONDS)] == pytest.approx(1.0)
    assert len(statistics.correlations) == 15


def test_historicke_predvolby_berou_parametry_ze_sveho_obdobi():
    for preset in MARKET_PRESETS:
        if preset.period is None:
            continue
        first_year, last_year = preset.period
        statistics = period_statistics(range(first_year, last_year + 1))

        assert preset.volatilities == statistics.volatilities
        assert preset.mean_correlation(set(AssetClass)) == pytest.approx(statistics.mean_correlation)


def test_predvolby_maji_unikatni_klic_a_parametry_pro_sve_tridy():
    keys = [preset.key for preset in MARKET_PRESETS]

    assert len(set(keys)) == len(keys)
    assert MARKET_PRESETS[0] is DEFAULT_PRESET
    assert set(DEFAULT_PRESET.expected_returns) == set(DEFAULT_PRESET.volatilities) == set(DEFAULT_CLASSES)
    for preset in MARKET_PRESETS[1:]:
        assert set(preset.expected_returns) == set(preset.volatilities) == set(AssetClass)
        assert all(volatility > 0 for volatility in preset.volatilities.values())


def test_prumerna_korelace_bere_jen_pary_trid_z_portfolia():
    preset = MARKET_PRESETS[1]
    pair = (AssetClass.STOCKS, AssetClass.REAL_ESTATE)

    assert preset.mean_correlation({AssetClass.STOCKS, AssetClass.REAL_ESTATE}) == preset.correlations[pair]
    assert preset.mean_correlation({AssetClass.GOLD}) == pytest.approx(preset.mean_correlation(set(AssetClass)))
