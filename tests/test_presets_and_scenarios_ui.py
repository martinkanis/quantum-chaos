import pytest
from dash import no_update

from montecarlo.historical_returns import AssetClass
from montecarlo.presets import DEFAULT_CLASSES, DEFAULT_PRESET, LONG_RUN_PRESET, PREDEFINED_ASSETS
from montecarlo.scenarios import STRESS_SCENARIOS, ScenarioValidationError
from ui.callbacks import add_selected_asset, add_stress_scenario_row, describe_stress_scenarios
from ui.form_parsing import (
    CLASS_COLUMN,
    DEFAULT_ASSET_ROWS,
    NAME_COLUMN,
    RETURN_COLUMN,
    VOLATILITY_COLUMN,
    WEIGHT_COLUMN,
    build_scenarios,
    scenario_rows,
)
from ui.market_presets import SliderRange, add_predefined_asset, apply_preset, find_preset, slider_correlation
from ui.portfolio_page import DEFAULT_PAIRWISE_CORRELATION

PERCENT = 100


def test_vychozi_predvolba_odpovida_vychozimu_formulari():
    for row in DEFAULT_ASSET_ROWS:
        asset_class = AssetClass(row[CLASS_COLUMN])
        assert row[RETURN_COLUMN] == pytest.approx(DEFAULT_PRESET.expected_returns[asset_class] * PERCENT)
        assert row[VOLATILITY_COLUMN] == pytest.approx(DEFAULT_PRESET.volatilities[asset_class] * PERCENT)
    assert DEFAULT_PRESET.mean_correlation(DEFAULT_CLASSES) == pytest.approx(DEFAULT_PAIRWISE_CORRELATION)


def test_predvolba_vyplni_radky_podle_tridy_a_radek_bez_tridy_necha():
    preset = find_preset("stagflace-1973-1981")
    rows = DEFAULT_ASSET_ROWS + [{"name": "Bitcoin", CLASS_COLUMN: None, VOLATILITY_COLUMN: 80}]

    updated = apply_preset(rows, preset)

    assert updated[2][VOLATILITY_COLUMN] == round(preset.volatilities[AssetClass.GOLD] * PERCENT, 1)
    assert updated[0][RETURN_COLUMN] == round(preset.expected_returns[AssetClass.STOCKS] * PERCENT, 1)
    assert updated[3] == rows[3]


def test_korelace_predvolby_se_zaokrouhli_na_krok_a_orizne_na_rozsah_posuvniku():
    preset = find_preset("stagflace-1973-1981")

    assert slider_correlation(preset, DEFAULT_ASSET_ROWS, SliderRange(-0.5, 1.0, 0.05)) == -0.25
    assert slider_correlation(preset, DEFAULT_ASSET_ROWS, SliderRange(0.0, 1.0, 0.05)) == 0.0


def test_scenare_ukazou_dopad_na_vychozi_portfolio_vcetne_castky():
    figure, message = describe_stress_scenarios(DEFAULT_ASSET_ROWS, scenario_rows(list(STRESS_SCENARIOS)), 1_000_000)
    bars = figure.data[0]

    assert message == ""
    assert len(bars.x) == len(STRESS_SCENARIOS)
    assert bars.y[0] == "1931 – Velká hospodářská krize"
    assert bars.x[0] == pytest.approx(-0.28810)
    assert "(-288 100 Kč)" in bars.text[0]


def test_scenare_vyzaduji_tridu_u_kazdeho_aktiva():
    rows = DEFAULT_ASSET_ROWS[:2] + [{**DEFAULT_ASSET_ROWS[2], CLASS_COLUMN: None}]

    figure, message = describe_stress_scenarios(rows, scenario_rows(list(STRESS_SCENARIOS)), 1_000_000)

    assert figure is no_update
    assert "Zlato" in message


def test_vlastni_scenar_musi_mit_vyplnene_vynosy_vsech_trid():
    row = scenario_rows(list(STRESS_SCENARIOS[:1]))[0]
    row[AssetClass.BONDS.value] = None

    with pytest.raises(ScenarioValidationError, match="dluhopisy"):
        build_scenarios([row])


def test_tabulka_scenaru_vrati_puvodni_vynosy():
    scenarios = build_scenarios(scenario_rows(list(STRESS_SCENARIOS)))

    for parsed, original in zip(scenarios, STRESS_SCENARIOS):
        for asset_class in AssetClass:
            assert parsed.returns[asset_class] == pytest.approx(original.returns[asset_class])


def test_pridane_vlastni_scenare_maji_unikatni_nazvy():
    rows = scenario_rows(list(STRESS_SCENARIOS))
    rows = add_stress_scenario_row(1, add_stress_scenario_row(1, rows))

    scenarios = build_scenarios(rows)

    assert [scenario.name for scenario in scenarios[-2:]] == ["Vlastní scénář 21", "Vlastní scénář 22"]


def test_scenare_se_stejnym_nazvem_se_odmitnou():
    rows = scenario_rows(list(STRESS_SCENARIOS[:1])) * 2

    with pytest.raises(ScenarioValidationError, match="unikátní"):
        build_scenarios(rows)


def test_vychozi_predvolba_necha_tridu_kterou_nepokryva():
    real_estate = {NAME_COLUMN: "Nemovitosti", CLASS_COLUMN: AssetClass.REAL_ESTATE.value, VOLATILITY_COLUMN: 9}

    assert apply_preset([real_estate], DEFAULT_PRESET) == [real_estate]


def test_aktivum_z_nabidky_dostane_dlouhodobe_parametry_a_unikatni_nazev():
    gold = next(asset for asset in PREDEFINED_ASSETS if asset.asset_class == AssetClass.GOLD)

    added = add_predefined_asset(DEFAULT_ASSET_ROWS, gold)[-1]

    assert added[NAME_COLUMN] == "Zlato 2"
    assert added[CLASS_COLUMN] == AssetClass.GOLD.value
    assert added[WEIGHT_COLUMN] == 0
    assert added[VOLATILITY_COLUMN] == round(LONG_RUN_PRESET.volatilities[AssetClass.GOLD] * PERCENT, 1)


def test_vyber_z_nabidky_prida_radek_a_vycisti_vyber():
    rows, selected = add_selected_asset(PREDEFINED_ASSETS[0].name, DEFAULT_ASSET_ROWS)

    assert len(rows) == len(DEFAULT_ASSET_ROWS) + 1
    assert selected is None
    assert add_selected_asset(None, DEFAULT_ASSET_ROWS) == (no_update, no_update)
