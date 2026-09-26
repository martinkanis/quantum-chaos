import numpy as np
import pytest

from montecarlo.portfolio import Asset, Portfolio, PortfolioValidationError, uniform_correlation


def make_assets(*weights):
    return tuple(
        Asset(name=f"A{index}", weight=weight, expected_return=0.05, volatility=0.1)
        for index, weight in enumerate(weights)
    )


def test_prijme_validni_portfolio():
    portfolio = Portfolio(assets=make_assets(0.6, 0.4), correlation=uniform_correlation(2, 0.3))

    np.testing.assert_allclose(portfolio.weights, [0.6, 0.4])


def test_odmitne_soucet_vah_ruzny_od_sta_procent():
    with pytest.raises(PortfolioValidationError, match="Součet vah"):
        Portfolio(assets=make_assets(0.6, 0.3), correlation=uniform_correlation(2, 0.0))


def test_odmitne_duplicitni_nazvy_aktiv():
    assets = (
        Asset(name="X", weight=0.5, expected_return=0.05, volatility=0.1),
        Asset(name="X", weight=0.5, expected_return=0.05, volatility=0.1),
    )
    with pytest.raises(PortfolioValidationError, match="unikátní"):
        Portfolio(assets=assets, correlation=uniform_correlation(2, 0.0))


def test_odmitne_zapornou_volatilitu():
    assets = (Asset(name="X", weight=1.0, expected_return=0.05, volatility=-0.1),)
    with pytest.raises(PortfolioValidationError, match="Volatilita"):
        Portfolio(assets=assets, correlation=np.eye(1))


def test_odmitne_korelacni_matici_spatneho_rozmeru():
    with pytest.raises(PortfolioValidationError, match="rozměr"):
        Portfolio(assets=make_assets(0.5, 0.5), correlation=np.eye(3))


def test_odmitne_korelacni_matici_ktera_neni_pozitivne_semidefinitni():
    contradictory = np.array([[1.0, 0.9, -0.9], [0.9, 1.0, 0.9], [-0.9, 0.9, 1.0]])
    with pytest.raises(PortfolioValidationError, match="semidefinitní"):
        Portfolio(assets=make_assets(0.4, 0.3, 0.3), correlation=contradictory)


def test_kovariance_odpovida_volatilitam_a_korelaci():
    assets = (
        Asset(name="A", weight=0.5, expected_return=0.05, volatility=0.1),
        Asset(name="B", weight=0.5, expected_return=0.05, volatility=0.2),
    )
    portfolio = Portfolio(assets=assets, correlation=uniform_correlation(2, 0.5))

    np.testing.assert_allclose(portfolio.covariance(), [[0.01, 0.01], [0.01, 0.04]])
