from math import prod

import numpy as np
import pytest

from gbs.demo import gbs_error_constants, useful_shot_fractions
from gbs.expectation import (
    MomentProblem,
    MomentProblemError,
    classical_mc_estimate,
    exact_expectation_via_hafnians,
    gbs_estimate,
    gbs_relative_error_constant,
    hafnian_terms,
    mc_relative_error_constant,
    run_convergence_study,
)
from gbs.hafnian import hafnian, hafnian_expansion, repeated_submatrix
from gbs.sampler import (
    GbsProgramError,
    pattern_distribution,
    program_from_covariance,
    sample_shots,
    total_photon_distribution,
)

COVARIANCE = np.array([[0.04, 0.012, 0.006], [0.012, 0.0225, 0.003], [0.006, 0.003, 0.01]])
WEIGHTS = np.array([0.5, 0.3, 0.2])


def test_hafnian_2x2_je_mimodiagonalni_prvek():
    assert hafnian(np.array([[9.0, 2.5], [2.5, 7.0]])) == 2.5


@pytest.mark.parametrize("size, matchings", [(2, 1), (4, 3), (6, 15), (8, 105)])
def test_hafnian_matice_jednicek_je_pocet_perfektnich_parovani(size, matchings):
    assert hafnian(np.ones((size, size))) == matchings


def test_hafnian_liche_matice_je_nula():
    assert hafnian(np.ones((3, 3))) == 0.0


def test_wickova_veta_dava_ctvrty_moment_normalniho_rozdeleni():
    sigma_squared = 0.3
    assert hafnian(repeated_submatrix(np.array([[sigma_squared]]), [4])) == pytest.approx(3 * sigma_squared**2)


def test_program_zakoduje_kovarianci_do_jadra_zarizeni():
    program = program_from_covariance(COVARIANCE, squeezing_strength=0.6)

    np.testing.assert_allclose(program.kernel, program.scale * COVARIANCE, atol=1e-12)
    assert np.tanh(program.squeezing).max() == pytest.approx(0.6)


def test_pravdepodobnosti_vzoru_odpovidaji_rozdeleni_celkoveho_poctu_fotonu():
    program = program_from_covariance(COVARIANCE, squeezing_strength=0.7)
    totals = total_photon_distribution(program, max_total=6)

    for total in (2, 4, 6):
        _, probabilities = pattern_distribution(program, total)
        assert probabilities.sum() == pytest.approx(totals[total], rel=1e-9)
    assert totals[1] == totals[3] == 0.0


def test_rozdeleni_celkoveho_poctu_fotonu_se_blizi_jedne():
    program = program_from_covariance(COVARIANCE, squeezing_strength=0.3)

    assert total_photon_distribution(program, max_total=40).sum() == pytest.approx(1.0, abs=1e-9)


def test_odmitne_zapornou_korelaci_kvuli_znamenkovemu_problemu():
    covariance = np.array([[0.04, -0.01], [-0.01, 0.02]])
    with pytest.raises(GbsProgramError, match="znaménko"):
        program_from_covariance(covariance, squeezing_strength=0.5)


def test_odmitne_prilis_mnoho_modu():
    with pytest.raises(GbsProgramError, match="nejvýše"):
        program_from_covariance(np.eye(7), squeezing_strength=0.5)


@pytest.mark.parametrize("degree", [2, 4, 6])
def test_hafnianova_cesta_souhlasi_s_uzavrenym_vzorcem(degree):
    problem = MomentProblem(covariance=COVARIANCE, weights=WEIGHTS, degree=degree)

    assert exact_expectation_via_hafnians(problem) == pytest.approx(problem.closed_form(), rel=1e-12)


@pytest.mark.parametrize("degree", [2, 4, 6])
def test_gbs_estimator_s_presnymi_cetnostmi_vrati_presnou_hodnotu(degree):
    problem = MomentProblem(covariance=COVARIANCE, weights=WEIGHTS, degree=degree)
    program = program_from_covariance(COVARIANCE, squeezing_strength=0.5)
    _, probabilities = pattern_distribution(program, degree)
    shot_count = 1_000_000

    estimate = gbs_estimate(problem, program, probabilities * shot_count, shot_count)

    assert estimate == pytest.approx(problem.closed_form(), rel=1e-9)


def test_odmitne_nepodporovany_stupen():
    with pytest.raises(MomentProblemError):
        MomentProblem(covariance=COVARIANCE, weights=WEIGHTS, degree=3)


def test_klasicke_mc_konverguje_k_presne_hodnote():
    problem = MomentProblem(covariance=COVARIANCE, weights=WEIGHTS, degree=2)
    samples = np.random.default_rng(1).multivariate_normal(np.zeros(3), COVARIANCE, size=200_000)

    assert classical_mc_estimate(problem, samples) == pytest.approx(problem.closed_form(), rel=0.02)


def test_studie_konvergence_snizuje_chybu_s_poctem_vzorku():
    problem = MomentProblem(covariance=COVARIANCE, weights=WEIGHTS, degree=4)
    program = program_from_covariance(COVARIANCE, squeezing_strength=0.6)

    study = run_convergence_study(problem, program, [1_000, 100_000], repetitions=10, rng=np.random.default_rng(2))

    assert study.gbs_relative_rmse[-1] < study.gbs_relative_rmse[0]
    assert study.mc_relative_rmse[-1] < study.mc_relative_rmse[0]
    assert study.gbs_relative_rmse[-1] < 0.1
    assert 0 < study.useful_shot_fraction < 1


def test_vystrely_maji_sudy_pocet_fotonu():
    program = program_from_covariance(COVARIANCE, squeezing_strength=0.7)
    shots = sample_shots(program, shot_count=50, rng=np.random.default_rng(3), max_listed_total=8)

    assert all(shot is None or shot.sum() % 2 == 0 for shot in shots)


def test_hafnianove_cleny_scitaji_na_presnou_hodnotu():
    problem = MomentProblem(covariance=COVARIANCE, weights=WEIGHTS, degree=4)
    terms = hafnian_terms(problem)

    assert len(terms) == 15
    assert sum(term.contribution for term in terms) == pytest.approx(problem.closed_form(), rel=1e-12)


def test_studie_vraci_pozorovane_cetnosti_vzoru():
    problem = MomentProblem(covariance=COVARIANCE, weights=WEIGHTS, degree=2)
    program = program_from_covariance(COVARIANCE, squeezing_strength=0.6)

    study = run_convergence_study(problem, program, [5_000], repetitions=1, rng=np.random.default_rng(4))

    assert study.observed_pattern_counts.shape == (len(study.patterns),)
    assert study.observed_pattern_counts.sum() == pytest.approx(5_000 * study.useful_shot_fraction, rel=0.2)


def test_podil_uzitecnych_vystrelu_je_pravdepodobnost():
    fractions = useful_shot_fractions(COVARIANCE, [0.1, 0.5, 0.9], degrees=[2, 4])

    assert set(fractions) == {2, 4}
    assert all(np.all((values > 0) & (values < 1)) for values in fractions.values())
    assert fractions[4][0] < fractions[4][-1]


def test_wickuv_rozklad_slouci_stejna_parovani():
    assert hafnian_expansion([2, 2]) == {((0, 0), (1, 1)): 1, ((0, 1), (0, 1)): 2}


@pytest.mark.parametrize("pattern", [[4, 0, 0], [3, 1, 0], [2, 1, 1], [2, 2, 2], [1, 1, 1, 1, 1, 1]])
def test_wickuv_rozklad_dava_hafnian_a_pocet_parovani(pattern):
    covariance = np.diag([0.04, 0.02, 0.01, 0.03, 0.05, 0.06])[: len(pattern), : len(pattern)] + 0.004
    expansion = hafnian_expansion(pattern)

    value = sum(count * prod(covariance[i, j] for i, j in product) for product, count in expansion.items())

    assert value == pytest.approx(hafnian(repeated_submatrix(covariance, pattern)), rel=1e-12)
    assert sum(expansion.values()) == prod(range(sum(pattern) - 1, 0, -2))


def test_lichy_pocet_cinitelu_nema_zadne_parovani():
    assert hafnian_expansion([2, 1]) == {}


@pytest.mark.parametrize("degree, expected", [(2, np.sqrt(2)), (4, np.sqrt(96) / 3), (6, np.sqrt(10170) / 15)])
def test_konstanta_chyby_mc_zavisi_jen_na_stupni(degree, expected):
    assert mc_relative_error_constant(degree) == pytest.approx(expected)


def test_konstanta_chyby_gbs_pro_jedno_aktivum_je_dana_podilem_uzitecnych_vystrelu():
    covariance = np.array([[0.04]])
    program = program_from_covariance(covariance, squeezing_strength=0.6)
    problem = MomentProblem(covariance=covariance, weights=np.array([1.0]), degree=4)
    useful_fraction = total_photon_distribution(program, max_total=4)[4]

    assert gbs_relative_error_constant(problem, program) == pytest.approx(0.5 * np.sqrt(1 / useful_fraction - 1))


def test_konstanta_chyby_gbs_neklesne_pod_mez_danou_zahozenymi_vystrely():
    problem = MomentProblem(covariance=COVARIANCE, weights=WEIGHTS, degree=4)
    program = program_from_covariance(COVARIANCE, squeezing_strength=0.7)
    useful_fraction = pattern_distribution(program, 4)[1].sum()

    assert gbs_relative_error_constant(problem, program) >= 0.5 * np.sqrt(1 / useful_fraction - 1)


def test_teoreticke_konstanty_chyby_odpovidaji_simulaci():
    problem = MomentProblem(covariance=COVARIANCE, weights=WEIGHTS, degree=4)
    program = program_from_covariance(COVARIANCE, squeezing_strength=0.7)
    shot_count = 100_000

    study = run_convergence_study(problem, program, [shot_count], repetitions=100, rng=np.random.default_rng(5))

    assert study.gbs_relative_rmse[-1] * np.sqrt(shot_count) == pytest.approx(study.gbs_error_constant, rel=0.2)
    assert study.mc_relative_rmse[-1] * np.sqrt(shot_count) == pytest.approx(study.mc_error_constant, rel=0.2)


def test_silnejsi_stlaceni_zmensi_konstantu_chyby_gbs():
    constants = gbs_error_constants(COVARIANCE, WEIGHTS, [0.3, 0.9], degrees=[4])

    assert constants[4][0] > constants[4][1] > 0


def test_odmitne_portfolio_s_nulovym_rozptylem():
    covariance = np.diag([0.0, 0.04])
    with pytest.raises(MomentProblemError, match="rozptyl"):
        MomentProblem(covariance=covariance, weights=np.array([1.0, 0.0]), degree=4)
