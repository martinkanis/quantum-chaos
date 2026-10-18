import numpy as np
import pytest

from randommatrix.cleaning import (
    Estimator,
    clipped_covariance,
    estimate,
    sample_covariance,
    shrinkage_intensity,
)
from randommatrix.factor_market import FactorMarket, FactorMarketError
from randommatrix.marchenko_pastur import NoiseBand, market_mode_noise_variance
from randommatrix.min_variance import compare_risk, min_variance_weights, predicted_in_sample, predicted_out_of_sample
from randommatrix.study import run_study

PURE_NOISE = dict(market_loading=0.0, sector_loading=0.0)


def test_pas_sumu_ma_meze_podle_marcenka_a_pastura():
    band = NoiseBand(ratio=0.25)

    assert (band.lower, band.upper) == pytest.approx((0.25, 2.25))
    assert NoiseBand(ratio=0.25, variance=0.5).upper == pytest.approx(1.125)


def test_hustota_marcenka_a_pastura_je_normovana():
    band = NoiseBand(ratio=0.4, variance=0.7)
    grid = np.linspace(band.lower, band.upper, 200_001)

    assert np.trapezoid(band.density(grid), grid) == pytest.approx(1, abs=1e-3)
    assert band.density(np.array([band.upper + 0.1]))[0] == 0


def test_vlastni_cisla_ciste_nahodne_matice_lezi_v_pasu_sumu():
    market = FactorMarket(400, **PURE_NOISE)
    returns = market.simulate_returns(1000, np.random.default_rng(1))
    eigenvalues = np.linalg.eigvalsh(sample_covariance(returns))
    band = NoiseBand(ratio=0.4)

    assert np.mean((eigenvalues > 0.95 * band.lower) & (eigenvalues < 1.05 * band.upper)) == 1


def test_trh_ma_trzni_a_sektorovou_korelaci():
    market = FactorMarket(20, sector_count=2)
    correlation = market.true_correlation()

    assert np.diag(correlation) == pytest.approx(np.ones(20))
    assert correlation[0, 1] == pytest.approx(0.41)
    assert correlation[0, 19] == pytest.approx(0.25)
    assert market.idiosyncratic_variance == pytest.approx(0.59)


def test_simulovane_vynosy_maji_skutecnou_korelaci():
    market = FactorMarket(10, sector_count=2)
    returns = market.simulate_returns(4000, np.random.default_rng(2))

    assert sample_covariance(returns) == pytest.approx(market.true_correlation(), abs=0.1)


def test_trh_odmitne_nesmyslne_zadani_s_ceskou_hlaskou():
    with pytest.raises(FactorMarketError, match="Počet akcií"):
        FactorMarket(5)
    with pytest.raises(FactorMarketError, match="β² \\+ γ²"):
        FactorMarket(50, market_loading=0.8, sector_loading=0.7)
    with pytest.raises(FactorMarketError, match="pod 0,90"):
        run_study(FactorMarket(400), 400, seed=1)


def test_odhad_rozptylu_sumu_ubere_trzni_mod():
    assert market_mode_noise_variance(np.array([0.5, 0.5, 0.5, 2.5])) == pytest.approx(0.375)


def test_orezani_zachova_stopu_i_vlastni_cisla_nad_pasem():
    market = FactorMarket(100)
    returns = market.simulate_returns(250, np.random.default_rng(3))
    sample = sample_covariance(returns)
    cleaned = clipped_covariance(sample, len(returns))

    assert np.trace(cleaned) == pytest.approx(np.trace(sample))
    assert np.linalg.eigvalsh(cleaned)[-1] == pytest.approx(np.linalg.eigvalsh(sample)[-1])


def test_intenzita_shrinkage_je_mezi_nulou_a_jednickou_a_u_cisteho_sumu_velka():
    noise = FactorMarket(100, **PURE_NOISE).simulate_returns(200, np.random.default_rng(4))
    long_history = FactorMarket(20).simulate_returns(4000, np.random.default_rng(5))

    assert 0.8 < shrinkage_intensity(noise) <= 1
    assert 0 <= shrinkage_intensity(long_history) < 0.1


def test_portfolio_s_minimalnim_rozptylem_je_plne_investovane_a_ze_skutecne_matice_optimalni():
    correlation = FactorMarket(30).true_correlation()
    risk = compare_risk(correlation, correlation)

    assert min_variance_weights(correlation).sum() == pytest.approx(1)
    assert (risk.in_sample, risk.out_of_sample) == pytest.approx((1, 1))


def test_surova_matice_slibuje_1_minus_q_a_dodava_1_lomeno_1_minus_q():
    market = FactorMarket(200)
    rng = np.random.default_rng(6)
    risks = [
        compare_risk(sample_covariance(market.simulate_returns(400, rng)), market.true_correlation())
        for _ in range(10)
    ]

    assert np.mean([risk.in_sample for risk in risks]) == pytest.approx(predicted_in_sample(0.5), rel=0.05)
    assert np.mean([risk.out_of_sample for risk in risks]) == pytest.approx(predicted_out_of_sample(0.5), rel=0.05)


def test_vycistena_matice_dava_mensi_skutecne_riziko_nez_surova():
    market = FactorMarket(200)
    returns = market.simulate_returns(400, np.random.default_rng(7))
    true = market.true_correlation()
    out_of_sample = {estimator: compare_risk(estimate(estimator, returns), true).out_of_sample for estimator in Estimator}

    assert out_of_sample[Estimator.CLIPPED] < out_of_sample[Estimator.SAMPLE]
    assert out_of_sample[Estimator.LINEAR_SHRINKAGE] < out_of_sample[Estimator.SAMPLE]


def test_beh_laboratore_je_se_stejnym_seedem_opakovatelny():
    first = run_study(FactorMarket(50), 250, seed=42)
    second = run_study(FactorMarket(50), 250, seed=42)

    assert first.ratio == pytest.approx(0.2)
    assert np.array_equal(first.spectrum.eigenvalues, second.spectrum.eigenvalues)
    assert first.spectrum.count_above_band >= 1
    assert first.sweep.out_of_sample[Estimator.SAMPLE][-1] > first.sweep.out_of_sample[Estimator.SAMPLE][0]
