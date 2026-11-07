import time
from itertools import combinations_with_replacement
from math import factorial

import numpy as np
import pytest

from gbs.boson_sampling import output_patterns, permanent, random_unitary, transition_matrix
from gbs.chip_boson_sampling import (
    MAX_PATTERNS,
    PhotonKind,
    complete_homogeneous,
    gaussian_estimator_values,
    pattern_count,
    pattern_distribution,
    run_sampling_study,
)
from gbs.chip_programming import ChipTarget, target_unitary
from gbs.photonic_chip import ChipError
from ui import ids
from ui.chip_sampling_callbacks import describe_pattern_count, parse_sampling_form
from ui.chip_sampling_content import SAMPLING_ANCHOR, SAMPLING_INTRO, SAMPLING_TOPIC
from ui.chip_sampling_results import build_sampling_results, czech_decimal
from ui.chip_simulator_content import TOPICS
from ui.chip_simulator_page import build_chip_simulator_page
from tests.test_chip_simulator_page import component_ids, texts_in

FOURIER = target_unitary(ChipTarget.SPREAD_EVENLY, 4, np.random.default_rng(0))
SAMPLING_FORM = {
    "mode_count": 8, "photons": 3, "target": ChipTarget.RANDOM.value, "split_spread": 0.0,
    "kind": PhotonKind.INDISTINGUISHABLE.value, "shots": 1000, "seed": 1,
}


def text_of(topic) -> str:
    return " ".join((topic.in_short + " " + topic.explanation).split())


def test_permanenty_vsech_vzoru_naraz_odpovidaji_ryserovi_po_jednom():
    unitary = random_unitary(5, np.random.default_rng(1))
    distribution = pattern_distribution(unitary, 3, PhotonKind.INDISTINGUISHABLE)
    one_by_one = np.array([abs(permanent(transition_matrix(unitary, pattern, 3))) ** 2 for pattern in distribution.patterns])

    assert np.array_equal(distribution.patterns, output_patterns(5, 3))
    assert np.allclose(distribution.probabilities * distribution.multiplicities, one_by_one)
    assert distribution.probabilities.sum() == pytest.approx(1.0)


def test_rozlisitelne_fotony_maji_permanent_z_absolutnich_hodnot_a_take_soucet_jedna():
    unitary = random_unitary(5, np.random.default_rng(2))
    distribution = pattern_distribution(unitary, 3, PhotonKind.DISTINGUISHABLE)
    one_by_one = np.array([
        permanent(np.abs(transition_matrix(unitary, pattern, 3)) ** 2).real for pattern in distribution.patterns
    ])

    assert np.allclose(distribution.probabilities * distribution.multiplicities, one_by_one)
    assert distribution.probabilities.sum() == pytest.approx(1.0)


@pytest.mark.parametrize("photons", [2, 3, 4])
def test_vsechny_fotony_v_jednom_vystupu_jsou_u_bosonu_n_faktorialkrat_castejsi(photons):
    unitary = random_unitary(6, np.random.default_rng(photons))
    bosons = pattern_distribution(unitary, photons, PhotonKind.INDISTINGUISHABLE)
    particles = pattern_distribution(unitary, photons, PhotonKind.DISTINGUISHABLE)
    all_together = bosons.patterns.max(axis=1) == photons

    assert np.allclose(bosons.probabilities[all_together], factorial(photons) * particles.probabilities[all_together])


def test_fourier_se_dvema_fotony_ma_mu_jedna_a_pul_a_rozlisitelne_ctvrt():
    bosons = pattern_distribution(FOURIER, 2, PhotonKind.INDISTINGUISHABLE)
    particles = pattern_distribution(FOURIER, 2, PhotonKind.DISTINGUISHABLE)

    assert bosons.bunching == pytest.approx(1.5) and particles.bunching == pytest.approx(1.25)
    assert bosons.relative_variance == pytest.approx(1 / 9)
    assert "vyjde $\\mu = 1{,}5$, fotony tedy skončí spolu v polovině výstřelů" in text_of(SAMPLING_TOPIC)
    assert "Rozlišitelné fotony dají $\\mu = 1{,}25$, spolu skončí jen ve čtvrtině" in text_of(SAMPLING_TOPIC)


def test_uplny_homogenni_polynom_je_soucet_vsech_monomu_daneho_stupne():
    values = np.random.default_rng(3).normal(size=(5, 4)) + 1j
    explicit = [
        sum(np.prod(row[list(modes)]) for modes in combinations_with_replacement(range(4), 3)) for row in values
    ]

    assert np.allclose(complete_homogeneous(values, 3), explicit)


@pytest.mark.parametrize("unitary, photons", [(FOURIER, 2), (random_unitary(4, np.random.default_rng(5)), 3)])
def test_klasicke_monte_carlo_z_gaussovskych_vektoru_ma_stredni_hodnotu_mu(unitary, photons):
    values = gaussian_estimator_values(unitary, photons, 400_000, np.random.default_rng(7))
    mu = pattern_distribution(unitary, photons, PhotonKind.INDISTINGUISHABLE).bunching

    assert abs(values.mean() - mu) < 4 * values.std() / np.sqrt(len(values))


def test_klasicky_rozptyl_je_o_rady_vetsi_a_s_fotony_roste_rychleji():
    unitary = random_unitary(8, np.random.default_rng(1))
    ratios = []
    for photons in (2, 3, 4):
        distribution = pattern_distribution(unitary, photons, PhotonKind.INDISTINGUISHABLE)
        values = gaussian_estimator_values(unitary, photons, 50_000, np.random.default_rng(photons))
        ratios.append(values.var() / distribution.bunching**2 / distribution.relative_variance)

    assert ratios[0] > 100 and ratios == sorted(ratios)


def test_ideal_trefi_mu_a_vyrobeny_cip_ma_systematickou_chybu_nezavislou_na_vystrelech():
    ideal = run_sampling_study(ChipTarget.RANDOM, 0.0, 1, 8, 4, PhotonKind.INDISTINGUISHABLE, 20_000)
    fabricated = run_sampling_study(ChipTarget.RANDOM, 0.08, 1, 8, 4, PhotonKind.INDISTINGUISHABLE, 20_000)
    fewer_shots = run_sampling_study(ChipTarget.RANDOM, 0.08, 1, 8, 4, PhotonKind.INDISTINGUISHABLE, 1_000)

    assert abs(ideal.bias) < 1e-9
    assert abs(ideal.estimate - ideal.target.bunching) < 4 * ideal.standard_error
    assert abs(fabricated.bias) > 0.01 and fabricated.bias == fewer_shots.bias
    assert abs(fabricated.estimate - fabricated.sampler.bunching) < 4 * fabricated.standard_error


@pytest.mark.parametrize("target", [ChipTarget.RANDOM, ChipTarget.SPREAD_EVENLY])
def test_rozlisitelne_fotony_v_prikladech_simulatoru_mu_snizi(target):
    for seed in range(1, 6):
        study = run_sampling_study(target, 0.0, seed, 16, 6, PhotonKind.DISTINGUISHABLE, 100)

        assert study.sampler.bunching < study.target.bunching


def test_pocty_vzoru_v_navodu_sedi_a_vetsi_ulohu_simulator_odmitne():
    assert pattern_count(16, 6) == 54_264 and pattern_count(16, 7) == 170_544 <= MAX_PATTERNS
    assert "54 264 možných výstupních vzorů, se 7 fotony 170 544" in " ".join(SAMPLING_INTRO.split())
    with pytest.raises(ChipError, match="490 314 výstupních vzorů"):
        pattern_distribution(random_unitary(16, np.random.default_rng(0)), 8, PhotonKind.INDISTINGUISHABLE)


def test_nejvetsi_uloha_dobehne_hluboko_pod_limitem_callbacku():
    started = time.perf_counter()
    study = run_sampling_study(ChipTarget.RANDOM, 0.08, 1, 16, 7, PhotonKind.INDISTINGUISHABLE, 100_000)
    build_sampling_results(study)

    assert time.perf_counter() - started < 10
    assert len(study.target.patterns) == 170_544


def test_laborator_ma_vlastni_sekci_a_kapitolu_ve_vykladu():
    page_ids = set(component_ids(build_chip_simulator_page()))

    assert {SAMPLING_ANCHOR, SAMPLING_TOPIC.anchor, ids.CHIP_SAMPLING_RUN_BUTTON, ids.CHIP_SAMPLING_RESULTS} <= page_ids
    assert TOPICS[-1] == SAMPLING_TOPIC


def test_formular_hlida_vstupy_a_ukaze_pocet_vzoru():
    assert parse_sampling_form(SAMPLING_FORM).photons == 3
    assert describe_pattern_count(16, 6) == "54 264 možných výstupních vzorů."
    assert "víc než 200 000" in describe_pattern_count(16, 8)
    with pytest.raises(ChipError, match="druh fotonů"):
        parse_sampling_form({**SAMPLING_FORM, "kind": None})
    with pytest.raises(ChipError, match="výstřelů"):
        parse_sampling_form({**SAMPLING_FORM, "shots": "hodně"})


def test_vysledky_ukazuji_oba_odhady_a_prvni_vystrely():
    study = run_sampling_study(ChipTarget.SPREAD_EVENLY, 0.0, 1, 4, 2, PhotonKind.INDISTINGUISHABLE, 1000)
    texts = list(texts_in(build_sampling_results(study)))

    assert "1,50" in texts and "10" in texts
    assert any(text.startswith("Boson sampling, 1 000 výstřelů") for text in texts)
    assert any(text.startswith("výstupy ") and "→ Z = " in text for text in texts)
    assert czech_decimal(1502.27) == "1 502,27" and czech_decimal(0.01482) == "0,0148"
