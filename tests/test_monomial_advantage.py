from math import prod

import numpy as np
import pytest

from gbs.advantage_lab import run_lab
from gbs.benchmark_problems import BENCHMARK_PROBLEMS, equicorrelated_matrix, find_benchmark
from gbs.gaussian_moments import moment_table
from gbs.hafnian import hafnian, repeated_submatrix
from gbs.monomial_problem import (
    MonomialProblem,
    MonomialProblemError,
    compare_variances,
    degree_sweep,
    gbs_p_estimate,
)
from gbs.monomial_study import run_monomial_study
from gbs.photon_tuning import TuningMode
from gbs.sampler import GbsProgram, pattern_probability

COVARIANCE = np.array([[1.0, 0.4, 0.2], [0.4, 2.0, -0.3], [0.2, -0.3, 0.5]])


def double_factorial(value):
    return prod(range(value, 0, -2))


def problem(covariance, exponents):
    names = tuple(f"X{index + 1}" for index in range(len(exponents)))
    return MonomialProblem(covariance=np.array(covariance, dtype=float), exponents=exponents, variable_names=names)


@pytest.mark.parametrize("pattern", [(2, 0, 0), (1, 1, 0), (2, 1, 1), (2, 2, 2), (3, 1, 2), (0, 4, 2)])
def test_moment_z_rekurze_se_rovna_hafnianu(pattern):
    table = moment_table(COVARIANCE, (3, 4, 2))

    assert table[pattern] == pytest.approx(hafnian(repeated_submatrix(COVARIANCE, pattern)))


def test_moment_jedne_promenne_je_dvojity_faktorial():
    variance = 0.04

    assert moment_table(np.array([[variance]]), (20,))[20] == pytest.approx(double_factorial(19) * variance**10)


def test_rozptyl_monte_carla_pro_x20_odpovida_vzorci():
    comparison = compare_variances(problem([[1.0]], (20,)), TuningMode.PER_MODE)

    assert comparison.exact == pytest.approx(654_729_075)
    assert comparison.mc_relative_variance == pytest.approx(double_factorial(39) / double_factorial(19) ** 2 - 1)


def test_pravdepodobnost_vzoru_odpovida_vzorci_gbs_s_hafnianem():
    exponents = (2, 1, 1)
    nonnegative = COVARIANCE.clip(0)
    comparison = compare_variances(problem(nonnegative, exponents), TuningMode.PER_MODE)
    encoding = comparison.encoding
    program = GbsProgram(
        covariance=nonnegative, scale=1.0, squeezing=encoding.squeezing, interferometer=encoding.interferometer,
    )

    assert comparison.pattern_probability == pytest.approx(pattern_probability(program, np.array(exponents)))


def test_ladeni_po_modech_posle_do_kazdeho_modu_tolik_fotonu_kolik_je_exponent():
    exponents = (6, 4, 2)
    encoding = compare_variances(problem(COVARIANCE, exponents), TuningMode.PER_MODE).encoding

    np.testing.assert_allclose(encoding.mean_photons_per_output_mode, exponents, atol=1e-4)


def test_ladeni_jako_v_clanku_posle_celkem_tolik_fotonu_jaky_je_stupen():
    encoding = compare_variances(problem(COVARIANCE, (6, 4, 2)), TuningMode.TOTAL).encoding

    assert encoding.mean_photons_per_output_mode.sum() == pytest.approx(12)
    assert np.ptp(encoding.mode_scales) == pytest.approx(0)


@pytest.mark.parametrize("benchmark", BENCHMARK_PROBLEMS, ids=lambda benchmark: benchmark.key)
def test_ladeni_po_modech_neni_nikdy_horsi_nez_ladeni_z_clanku(benchmark):
    per_mode = compare_variances(benchmark.problem, TuningMode.PER_MODE)
    total = compare_variances(benchmark.problem, TuningMode.TOTAL)

    assert per_mode.pattern_probability >= total.pattern_probability * (1 - 1e-9)


def test_odhad_gbs_p_z_presne_pravdepodobnosti_vrati_presnou_hodnotu():
    exponents = (8, 8)
    comparison = compare_variances(problem(equicorrelated_matrix(2, 0.5), exponents), TuningMode.PER_MODE)

    assert gbs_p_estimate(comparison.encoding, exponents, comparison.pattern_probability) == pytest.approx(
        comparison.exact
    )


@pytest.mark.parametrize("benchmark", BENCHMARK_PROBLEMS, ids=lambda benchmark: benchmark.key)
def test_vsech_pet_pripravenych_uloh_je_pro_gbs_vyhodnych(benchmark):
    assert compare_variances(benchmark.problem, TuningMode.PER_MODE).advantage > 10


def test_cisla_v_popisech_uloh_odpovidaji_vypoctu():
    def per_mode(key):
        return compare_variances(find_benchmark(key).problem, TuningMode.PER_MODE)

    def total(key):
        return compare_variances(find_benchmark(key).problem, TuningMode.TOTAL)

    assert per_mode("extremni-moment").advantage == pytest.approx(72_000, rel=0.01)
    assert 1 / per_mode("extremni-moment").pattern_probability == pytest.approx(42, rel=0.02)
    assert 1 / per_mode("spolecny-extrem").pattern_probability == pytest.approx(250, rel=0.01)
    assert per_mode("nesoumerny-monom").pattern_probability / total("nesoumerny-monom").pattern_probability == (
        pytest.approx(3, rel=0.02)
    )
    assert 1 / total("historie-usa").advantage == pytest.approx(250, rel=0.03)
    assert per_mode("historie-usa").advantage == pytest.approx(170, rel=0.03)
    assert per_mode("trzni-faktor").advantage == pytest.approx(60, rel=0.01)


def test_soucin_mnoha_promennych_s_exponentem_1_vyhraje_monte_carlo():
    comparison = compare_variances(problem(equicorrelated_matrix(6, 0.6), (1,) * 6), TuningMode.PER_MODE)

    assert 1 / comparison.advantage == pytest.approx(6.4, rel=0.02)


def test_rozptyl_podle_stupne_roste_u_monte_carla_mnohem_rychleji_nez_u_gbs():
    sweep = degree_sweep(find_benchmark("spolecny-extrem").problem)
    advantages = sweep.mc_relative_variances / sweep.gbs_relative_variances[TuningMode.PER_MODE]

    assert 16 in sweep.degrees
    assert np.all(np.diff(sweep.mc_relative_variances) > 0)
    assert advantages[0] < 1 < advantages[-1]


@pytest.mark.parametrize(
    ("covariance", "exponents", "message"),
    [
        ([[1.0, 0.5], [0.5, 1.0]], (3, 2), "musí být sudý"),
        ([[1.0, -0.5], [-0.5, 1.0]], (3, 1), "nezáporné"),
        ([[1.0, 2.0], [2.0, 1.0]], (2, 2), "pozitivně semidefinitní"),
        ([[1.0]], (42,), "nejvýš 40"),
        ([[1.0, 0.0], [0.0, 1.0]], (0, 0), "kladný"),
        ([[1.0, 0.0], [0.0, 1.0]], (1, 1), "nulová"),
    ],
)
def test_neplatna_uloha_skonci_srozumitelnou_chybou(covariance, exponents, message):
    with pytest.raises(MonomialProblemError, match=message):
        compare_variances(problem(covariance, exponents), TuningMode.PER_MODE)


def test_se_sudymi_exponenty_nevadi_zaporne_korelace():
    comparison = compare_variances(problem([[1.0, -0.5], [-0.5, 1.0]], (4, 2)), TuningMode.PER_MODE)

    assert comparison.exact > 0


def test_promenna_s_exponentem_0_se_do_zarizeni_nenahrava():
    comparison = compare_variances(problem(COVARIANCE, (4, 0, 2)), TuningMode.PER_MODE)

    assert len(comparison.encoding.mode_scales) == 2
    assert comparison.exact == pytest.approx(hafnian(repeated_submatrix(COVARIANCE, (4, 0, 2))))


def test_simulace_gbs_p_konverguje_k_presne_hodnote():
    benchmark = find_benchmark("spolecny-extrem")
    comparison = compare_variances(benchmark.problem, TuningMode.PER_MODE)

    study = run_monomial_study(benchmark.problem, comparison, [1_000, 100_000], 20, np.random.default_rng(1))

    assert study.gbs_relative_rmse[-1] < study.gbs_relative_rmse[0]
    assert study.gbs_relative_rmse[-1] * np.sqrt(100_000) == pytest.approx(study.gbs_error_constant, rel=0.5)
    assert np.median(study.gbs_final_estimates) / study.exact == pytest.approx(1, abs=0.05)


def test_stejny_seed_da_stejny_beh_laboratore():
    benchmark = find_benchmark("nesoumerny-monom")

    first = run_lab(benchmark.problem, TuningMode.PER_MODE, max_sample_size=10_000, seed=3)
    second = run_lab(benchmark.problem, TuningMode.PER_MODE, max_sample_size=10_000, seed=3)

    np.testing.assert_array_equal(first.study.gbs_final_estimates, second.study.gbs_final_estimates)
    np.testing.assert_array_equal(first.study.mc_final_estimates, second.study.mc_final_estimates)
