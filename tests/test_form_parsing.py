import numpy as np
import pytest

from montecarlo.portfolio import PortfolioValidationError
from montecarlo.simulation import SimulationParametersError
from ui.form_parsing import (
    DEFAULT_ASSET_ROWS,
    NAME_COLUMN,
    RANDOM_SEED,
    RETURN_COLUMN,
    VOLATILITY_COLUMN,
    WEIGHT_COLUMN,
    build_parameters,
    build_portfolio,
    correlation_column_id,
    default_correlation_rows,
    weight_sum_percent,
)

NAMES = ["Akcie svět", "Dluhopisy", "Zlato"]


def test_prevede_vychozi_formular_na_portfolio_v_desetinnych_cislech():
    portfolio = build_portfolio(DEFAULT_ASSET_ROWS, default_correlation_rows(NAMES, 0.2))

    np.testing.assert_allclose(portfolio.weights, [0.6, 0.3, 0.1])
    np.testing.assert_allclose(portfolio.expected_returns, [0.07, 0.03, 0.04])


def test_korelacni_matice_se_bere_z_horniho_trojuhelniku():
    rows = default_correlation_rows(NAMES, 0.0)
    rows[0][correlation_column_id(1)] = 0.5
    rows[1][correlation_column_id(0)] = -0.9

    portfolio = build_portfolio(DEFAULT_ASSET_ROWS, rows)

    assert portfolio.correlation[0, 1] == portfolio.correlation[1, 0] == 0.5


def test_odmitne_nevyplnenou_vahu():
    rows = [dict(row) for row in DEFAULT_ASSET_ROWS]
    rows[0][WEIGHT_COLUMN] = None

    with pytest.raises(PortfolioValidationError, match="Akcie svět"):
        build_portfolio(rows, default_correlation_rows(NAMES, 0.0))


def test_odmitne_aktivum_bez_nazvu():
    rows = DEFAULT_ASSET_ROWS + [{NAME_COLUMN: "", WEIGHT_COLUMN: 0, RETURN_COLUMN: 5, VOLATILITY_COLUMN: 10}]

    with pytest.raises(PortfolioValidationError, match="název"):
        build_portfolio(rows, default_correlation_rows(NAMES, 0.0))


def test_odmitne_korelacni_matici_ktera_neodpovida_aktivum():
    with pytest.raises(PortfolioValidationError, match="neodpovídá"):
        build_portfolio(DEFAULT_ASSET_ROWS, default_correlation_rows(NAMES[:2], 0.0))


def test_soucet_vah_ignoruje_prazdne_bunky():
    assert weight_sum_percent([{WEIGHT_COLUMN: 40}, {WEIGHT_COLUMN: None}, {WEIGHT_COLUMN: "abc"}]) == 40


def test_prazdny_seed_znamena_nahodnou_simulaci():
    assert build_parameters(1000, 0, 5, 100, None).seed is None


def test_volba_nahodny_z_dropdownu_znamena_nahodnou_simulaci():
    assert build_parameters(1000, 0, 5, 100, RANDOM_SEED).seed is None


def test_seed_z_dropdownu_se_pouzije():
    assert build_parameters(1000, 0, 5, 100, 42).seed == 42


@pytest.mark.parametrize("seed", [-1, 1.5, "abc"])
def test_odmitne_neplatny_seed(seed):
    with pytest.raises(SimulationParametersError, match="Seed"):
        build_parameters(1000, 0, 5, 100, seed)


def test_odmitne_prazdnou_pocatecni_investici():
    with pytest.raises(SimulationParametersError, match="Počáteční investice"):
        build_parameters(None, 0, 5, 100, None)
