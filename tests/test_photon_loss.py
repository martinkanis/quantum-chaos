from math import comb, exp, factorial, log

import numpy as np
import pytest

from gbs.benchmark_problems import find_benchmark
from gbs.hafnian import hafnian, repeated_submatrix
from gbs.loss_study import SIMULATION_ERROR, TRANSMISSIONS, run_loss_study, simulable_transmission
from gbs.monomial_problem import MonomialProblem, compare_variances
from gbs.photon_loss import (
    PhotonLossError,
    click_probability,
    correction_second_moments,
    correction_values,
    critical_transmission,
    extra_photons_within_limit,
    ideal_patterns,
    lossy_target,
    survival_weights,
)
from gbs.photon_tuning import TuningMode, tune_encoding

COVARIANCE = np.array([[1.0, 0.5], [0.5, 1.0]])


def problem(covariance, exponents):
    names = tuple(f"X{index + 1}" for index in range(len(exponents)))
    return MonomialProblem(covariance=np.array(covariance, dtype=float), exponents=exponents, variable_names=names)


def mixed_state_probability(encoding, transmission, pattern):
    """p(n) = Haf(A_n) / (n!·√det σ_Q) for the lossy Gaussian state (Hamilton et al. 2017), independent of thinning.

    Squeezed vacua squeezed along x, the real interferometer O on both quadratures, loss σ → ησ + (1 − η)·I/2,
    then the complex basis a = (x + ip)/√2, σ_Q = σ + I/2 and A = X·(I − σ_Q⁻¹) with the index of every mode repeated
    for a and for a†.
    """
    modes = len(pattern)
    rotation = encoding.interferometer
    zero = np.zeros((modes, modes))
    squeezed = np.block([
        [rotation @ np.diag(np.exp(-2 * encoding.squeezing) / 2) @ rotation.T, zero],
        [zero, rotation @ np.diag(np.exp(2 * encoding.squeezing) / 2) @ rotation.T],
    ])
    quadratures = transmission * squeezed + (1 - transmission) * np.eye(2 * modes) / 2
    to_complex = np.block([[np.eye(modes), 1j * np.eye(modes)], [np.eye(modes), -1j * np.eye(modes)]]) / np.sqrt(2)
    sigma_q = to_complex @ quadratures @ to_complex.conj().T + np.eye(2 * modes) / 2
    swap = np.block([[zero, np.eye(modes)], [np.eye(modes), zero]])
    kernel = swap @ (np.eye(2 * modes) - np.linalg.inv(sigma_q))
    value = hafnian(repeated_submatrix(kernel, list(pattern) * 2))
    value /= np.prod([factorial(count) for count in pattern]) * np.sqrt(np.linalg.det(sigma_q))
    assert abs(value.imag) < 1e-12
    return float(value.real)


def binomial(count, successes, probability):
    return comb(count, successes) * probability**successes * (1 - probability) ** (count - successes)


@pytest.mark.parametrize("exponents", [(2, 2), (3, 1), (2, 0), (4, 2)])
@pytest.mark.parametrize("transmission", [1.0, 0.9, 0.6])
def test_zredene_rozdeleni_se_shoduje_s_hafnianem_smiseneho_stavu(exponents, transmission):
    encoding = tune_encoding(COVARIANCE, exponents, TuningMode.PER_MODE)
    ideal = ideal_patterns(COVARIANCE, encoding, exponents, extra_photons=40)

    target = lossy_target(ideal, transmission)

    assert target.probability == pytest.approx(mixed_state_probability(encoding, transmission, exponents), rel=1e-9)
    assert target.probability_tail_share < 1e-9


def test_bez_ztrat_vyjde_idealni_pravdepodobnost_i_rozptyl():
    used = find_benchmark("historie-usa").problem.used_variables()
    comparison = compare_variances(used, TuningMode.PER_MODE)
    ideal = ideal_patterns(used.covariance, comparison.encoding, used.exponents, extra_photons=20)

    target = lossy_target(ideal, 1.0)

    assert target.probability == pytest.approx(comparison.pattern_probability, rel=1e-12)
    assert target.correction_relative_variance(comparison.pattern_probability) == pytest.approx(
        comparison.gbs_relative_variance, rel=1e-9
    )
    assert target.correction_converged and target.correction_tail_share == 0


@pytest.mark.parametrize("transmission", [1.0, 0.9, 0.5, 0.2])
def test_oprava_ztrat_je_nestranna_a_jeji_druhy_moment_sedi(transmission):
    target, max_count = 3, 14
    values = correction_values(target, transmission, max_count)
    second_moments = correction_second_moments(target, transmission, max_count)
    weights = survival_weights(target, transmission, max_count)

    for sent in range(max_count + 1):
        mean = sum(binomial(sent, detected, transmission) * values[detected] for detected in range(sent + 1))
        second = sum(binomial(sent, detected, transmission) * values[detected] ** 2 for detected in range(sent + 1))
        assert mean == pytest.approx(1.0 if sent == target else 0.0, abs=1e-8)
        assert second_moments[sent] == pytest.approx(second, rel=1e-9, abs=1e-300)
        assert weights[sent] == pytest.approx(binomial(sent, target, transmission) if sent >= target else 0.0)


def test_rozptyl_opravy_roste_se_ztratami_a_pod_kritickou_propustnosti_diverguje():
    study = run_loss_study(find_benchmark("extremni-moment").problem, TuningMode.PER_MODE, 0.9)
    variances = [point.corrected_relative_variance for point in study.sweep if point.correction_converged]
    converged = {point.transmission: point.correction_converged for point in study.sweep}

    assert study.sweep[0].transmission == 1.0
    assert variances == sorted(variances)
    assert len(variances) >= 10
    assert converged[0.9] and converged[0.8]
    assert not converged[0.4] and not converged[0.1]
    assert all(point.probability_reliable for point in study.sweep if point.transmission >= 0.4)
    assert all(point.naive_bias < 0 for point in study.sweep[1:] if point.probability_reliable)
    assert study.chosen.naive_bias == pytest.approx(-0.287, abs=0.002)


def test_kriticka_propustnost_odpovida_pomeru_vrstev_u_jednoho_modu():
    encoding = tune_encoding(np.array([[1.0]]), (2,), TuningMode.PER_MODE)
    ideal = ideal_patterns(np.array([[1.0]]), encoding, (2,), extra_photons=60)
    strongest = float(np.tanh(encoding.squeezing).max())

    assert critical_transmission(encoding) == pytest.approx(strongest / (1 + strongest))
    assert critical_transmission(encoding) < 0.5
    assert lossy_target(ideal, 0.9).correction_converged
    assert not lossy_target(ideal, critical_transmission(encoding) - 0.05).correction_converged


def test_hranice_qi_vyhovuje_jejich_nerovnosti_a_s_presnou_simulaci_mizi():
    encoding = tune_encoding(COVARIANCE, (2, 2), TuningMode.PER_MODE)
    squeezing = float(encoding.squeezing.max())
    squeezers = int((encoding.squeezing > 1e-9).sum())
    boundary = simulable_transmission(encoding)

    def qi_left_side(transmission):
        variance = transmission * exp(-2 * squeezing) + 1 - transmission
        return 1 / np.cosh(0.5 * log(1 / variance))

    right_side = exp(-(SIMULATION_ERROR**2) / (4 * squeezers))
    assert qi_left_side(0.99 * boundary) > right_side > qi_left_side(1.01 * boundary)
    assert 0 < boundary < 0.05
    assert simulable_transmission(encoding, error=1e-6) < 1e-5


def test_prahove_detektory_vidi_cilovy_vzor_casteji_nez_padne():
    used = problem(COVARIANCE, (1, 1))
    comparison = compare_variances(used, TuningMode.PER_MODE)
    ideal = ideal_patterns(used.covariance, comparison.encoding, used.exponents, extra_photons=40)

    assert click_probability(ideal, 1.0) > comparison.pattern_probability
    assert click_probability(ideal, 0.7) < click_probability(ideal, 1.0)
    assert ideal.tail_probability < 1e-4


def test_studie_zahrne_celou_radu_propustnosti_a_zvolenou_propustnost():
    study = run_loss_study(find_benchmark("spolecny-extrem").problem, TuningMode.PER_MODE, 0.95)

    assert tuple(point.transmission for point in study.sweep) == TRANSMISSIONS
    assert study.chosen.transmission == 0.95
    assert study.advantage(study.sweep[0]) == pytest.approx(study.comparison.advantage)
    assert study.advantage(study.chosen) < study.comparison.advantage
    assert not study.resolvable_by_threshold_detectors
    assert study.extra_photons == extra_photons_within_limit(study.exponents)
    assert 0 < study.simulable_transmission < study.critical_transmission < 0.5


@pytest.mark.parametrize("transmission", [0.0, 1.5, -0.1])
def test_propustnost_mimo_rozsah_skonci_ceskou_hlaskou(transmission):
    encoding = tune_encoding(COVARIANCE, (2, 2), TuningMode.PER_MODE)
    ideal = ideal_patterns(COVARIANCE, encoding, (2, 2), extra_photons=8)

    with pytest.raises(PhotonLossError, match="Propustnost"):
        lossy_target(ideal, transmission)


def test_prilis_velka_uloha_skonci_ceskou_hlaskou():
    with pytest.raises(PhotonLossError, match="příliš velká"):
        extra_photons_within_limit((10, 10, 10, 10, 10, 10))
