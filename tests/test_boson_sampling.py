import numpy as np
import pytest

from gbs.boson_sampling import (
    BosonSamplingError,
    BosonSamplingProblem,
    estimate,
    output_patterns,
    permanent,
    random_unitary,
    reference_problem,
)


def test_permanent_2x2_je_soucet_obou_parovani():
    assert permanent(np.array([[1.0, 2.0], [3.0, 4.0]])) == pytest.approx(1 * 4 + 2 * 3)


@pytest.mark.parametrize("size", [1, 2, 3, 4, 5])
def test_permanent_matice_jednicek_je_faktorial(size):
    assert permanent(np.ones((size, size))) == pytest.approx(np.prod(range(1, size + 1)))


def test_pravdepodobnosti_vzoru_davaji_dohromady_jedna():
    problem = reference_problem()

    assert estimate(problem).probabilities.sum() == pytest.approx(1.0, abs=1e-12)


def test_odhad_je_nevychyleny():
    result = estimate(reference_problem())

    assert result.probabilities @ result.shot_values == pytest.approx(result.exact_value, rel=1e-12)


def test_referencni_uloha_dava_stejna_cisla_jako_simulace_v_percevalu():
    result = estimate(reference_problem())

    assert result.exact_value == pytest.approx(1.807639, abs=1e-6)
    assert result.relative_variance == pytest.approx(0.6759, abs=1e-4)


def test_vzorkovany_odhad_konverguje_k_presne_hodnote():
    problem = reference_problem()
    result = estimate(problem)
    shots = 200_000
    counts = np.random.default_rng(1).multinomial(shots, result.probabilities)

    sampled = counts @ result.shot_values / shots

    assert sampled == pytest.approx(result.exact_value, rel=4 * np.sqrt(result.relative_variance / shots))


def test_odmitne_matici_ktera_neni_unitarni():
    with pytest.raises(BosonSamplingError, match="unitární"):
        BosonSamplingProblem(np.ones((3, 3)), photons=2, coefficients=np.ones(len(output_patterns(3, 2))))


def test_nahodna_unitarni_matice_je_unitarni():
    unitary = random_unitary(5, np.random.default_rng(2))

    np.testing.assert_allclose(unitary.conj().T @ unitary, np.eye(5), atol=1e-12)
