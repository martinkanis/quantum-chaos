import numpy as np
import pytest

from gbs.advantage_share import advantage_share
from gbs.hafnian import hafnian, repeated_submatrix
from gbs.hafnian_squared import (
    PAPER_EXAMPLE_MATRIX,
    HafSquaredProblem,
    HafSquaredProblemError,
    compare_estimators,
    degree_patterns,
    rescale_to_degree,
    simulate_gbs_i,
    simulate_mc,
    uniform_problem,
    variance_model,
)
from gbs.sampler import program_from_covariance, total_photon_distribution

EXAMPLE_6_1 = PAPER_EXAMPLE_MATRIX
SMALL_MATRIX = np.array([[0.5, 0.2, 0.1], [0.2, 0.4, 0.15], [0.1, 0.15, 0.3]])


def random_problem(degree, seed):
    rng = np.random.default_rng(seed)
    coefficients = rng.normal(size=len(degree_patterns(3, degree)))
    return HafSquaredProblem(SMALL_MATRIX, degree, coefficients)


def test_presna_hodnota_je_soucet_ctvercu_hafnianu():
    problem = random_problem(degree=2, seed=1)
    expected = sum(
        coefficient * hafnian(repeated_submatrix(SMALL_MATRIX, pattern)) ** 2
        for coefficient, pattern in zip(problem.coefficients, problem.patterns)
    )

    assert compare_estimators(problem).exact_value == pytest.approx(expected, rel=1e-12)


def test_preskalovani_da_stredni_pocet_fotonu_2k():
    rescaling = rescale_to_degree(EXAMPLE_6_1, degree=4)
    eigenvalues = np.linalg.eigvalsh(EXAMPLE_6_1) * rescaling.scale

    assert np.sum(eigenvalues**2 / (1 - eigenvalues**2)) == pytest.approx(8, rel=1e-9)
    assert rescaling.normalization == pytest.approx(np.prod(np.sqrt(1 - eigenvalues**2)))


def test_pravdepodobnosti_vzoru_sedi_s_nezavislym_simulatorem_fotonu():
    model = variance_model(SMALL_MATRIX, degree=3)
    eigenvalue_max = np.linalg.eigvalsh(SMALL_MATRIX).max()
    program = program_from_covariance(SMALL_MATRIX, squeezing_strength=model.rescaling.scale * eigenvalue_max)

    assert model.pattern_probabilities().sum() == pytest.approx(total_photon_distribution(program, 6)[6], rel=1e-9)


def test_gbs_i_je_nevychyleny_a_jeho_rozptyl_obsahuje_t_na_minus_2k_ne_minus_4k():
    problem = random_problem(degree=3, seed=2)
    model = variance_model(problem.covariance, problem.degree)
    probabilities = model.pattern_probabilities()
    shot_values = model.shot_values(problem.coefficients)
    comparison = model.compare(problem.coefficients)
    exact = comparison.exact_value
    enumerated_relative_variance = (probabilities @ shot_values**2 - exact**2) / exact**2

    assert probabilities @ shot_values == pytest.approx(exact, rel=1e-12)
    assert comparison.gbs_i_relative_variance == pytest.approx(enumerated_relative_variance, rel=1e-9)
    assert abs(model.rescaling.scale - 1) > 0.1
    assert comparison.printed_gbs_i_relative_variance != pytest.approx(enumerated_relative_variance, rel=0.01)


def test_simulace_gbs_i_i_monte_carla_konverguji_k_presne_hodnote():
    problem = uniform_problem(SMALL_MATRIX, degree=2)
    comparison = compare_estimators(problem)
    samples = 200_000

    gbs_estimate = simulate_gbs_i(problem, samples, np.random.default_rng(3))
    mc_estimate = simulate_mc(problem, samples, np.random.default_rng(4))

    gbs_tolerance = 4 * np.sqrt(comparison.gbs_i_relative_variance / samples)
    mc_tolerance = 4 * np.sqrt(comparison.mc_relative_variance / samples)
    assert gbs_estimate == pytest.approx(comparison.exact_value, rel=gbs_tolerance)
    assert mc_estimate == pytest.approx(comparison.exact_value, rel=mc_tolerance)


def test_u_prikladu_6_1_roste_rozptyl_monte_carla_mnohem_rychleji_nez_gbs_i():
    low, high = (compare_estimators(uniform_problem(EXAMPLE_6_1, degree)) for degree in (2, 6))

    assert high.mc_relative_variance / high.gbs_i_relative_variance > 10 * (
        low.mc_relative_variance / low.gbs_i_relative_variance
    )


def test_odmitne_matici_ktera_neni_kovariancni():
    with pytest.raises(HafSquaredProblemError):
        HafSquaredProblem(np.array([[1.0, 2.0], [2.0, 1.0]]), 1, np.ones(3))


def test_oprava_vzorce_nemeni_zaver_ze_gbs_i_casto_vyhrava():
    share = advantage_share(mode_count=3, degree=3, matrix_count=10, coefficient_count=50, rng=np.random.default_rng(5))

    assert share.derived_percent > 90 and share.printed_percent > 90
    assert share.median_variance_ratio > 1
