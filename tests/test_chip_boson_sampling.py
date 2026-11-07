import time
import tracemalloc
from itertools import combinations_with_replacement
from math import factorial

import numpy as np
import pytest

from gbs.boson_sampling import output_patterns, permanent, random_unitary, transition_matrix
from gbs.chip_boson_sampling import (
    MAX_PATTERNS,
    PhotonKind,
    all_pattern_permanents,
    complete_homogeneous,
    gaussian_estimator_values,
    occupied_outputs,
    pattern_count,
    pattern_distribution,
    run_sampling_study,
)
from gbs.chip_programming import ChipTarget, target_unitary
from gbs.photonic_chip import ChipError, mzi_count
from ui import ids
from ui.chip_sampling_callbacks import describe_pattern_count, parse_sampling_form
from ui.chip_sampling_content import (
    EXACT_HINT,
    MODE_COUNT_OPTIONS,
    PHOTON_OPTIONS,
    SAMPLING_ANCHOR,
    SAMPLING_INTRO,
    SAMPLING_TOPIC,
)
from ui.chip_sampling_results import build_sampling_results, czech_count, czech_decimal
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


def photon_counts(occupied: np.ndarray, modes: int) -> np.ndarray:
    return np.array([np.bincount(outputs, minlength=modes) for outputs in occupied])


def test_permanenty_vsech_vzoru_naraz_odpovidaji_ryserovi_po_jednom():
    unitary = random_unitary(5, np.random.default_rng(1))
    distribution = pattern_distribution(unitary, 3, PhotonKind.INDISTINGUISHABLE)
    patterns = photon_counts(distribution.occupied_outputs, 5)
    one_by_one = np.array([abs(permanent(transition_matrix(unitary, pattern, 3))) ** 2 for pattern in patterns])

    assert np.array_equal(patterns, output_patterns(5, 3))
    assert np.allclose(distribution.probabilities * distribution.multiplicities, one_by_one)
    assert distribution.probabilities.sum() == pytest.approx(1.0)


def test_rozlisitelne_fotony_maji_permanent_z_absolutnich_hodnot_a_take_soucet_jedna():
    unitary = random_unitary(5, np.random.default_rng(2))
    distribution = pattern_distribution(unitary, 3, PhotonKind.DISTINGUISHABLE)
    one_by_one = np.array([
        permanent(np.abs(transition_matrix(unitary, pattern, 3)) ** 2).real
        for pattern in photon_counts(distribution.occupied_outputs, 5)
    ])

    assert np.allclose(distribution.probabilities * distribution.multiplicities, one_by_one)
    assert distribution.probabilities.sum() == pytest.approx(1.0)


@pytest.mark.parametrize("photons", [2, 3, 4])
def test_vsechny_fotony_v_jednom_vystupu_jsou_u_bosonu_n_faktorialkrat_castejsi(photons):
    unitary = random_unitary(6, np.random.default_rng(photons))
    bosons = pattern_distribution(unitary, photons, PhotonKind.INDISTINGUISHABLE)
    particles = pattern_distribution(unitary, photons, PhotonKind.DISTINGUISHABLE)
    all_together = bosons.occupied_outputs[:, 0] == bosons.occupied_outputs[:, -1]

    assert np.allclose(bosons.probabilities[all_together], factorial(photons) * particles.probabilities[all_together])


@pytest.mark.parametrize("modes, photons", [(3, 1), (4, 4), (7, 5)])
def test_glynnuv_vzorec_po_prefixech_sedi_s_ryserem_i_pro_jeden_foton_a_plny_cip(modes, photons):
    unitary = random_unitary(modes, np.random.default_rng(modes + photons))
    occupied = occupied_outputs(modes, photons)
    one_by_one = [permanent(unitary[np.ix_(outputs, range(photons))]) for outputs in occupied]

    assert np.array_equal(occupied, list(combinations_with_replacement(range(modes), photons)))
    assert np.allclose(all_pattern_permanents(unitary[:, :photons]), one_by_one)


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
    intro = " ".join(SAMPLING_INTRO.split())

    assert pattern_count(16, 6) == 54_264 and pattern_count(16, 8) == 490_314
    assert mzi_count(64) == 2_016 and pattern_count(64, 4) == 766_480 <= MAX_PATTERNS == 1_000_000
    assert "54 264 možných výstupních vzorů, s 8 fotony 490 314" in intro
    assert "64 světlovody má 2 016 interferometrů a se 4 fotony 766 480 vzorů" in intro
    assert f"nejvýš {czech_count(MAX_PATTERNS)} vzorů" in intro and f"nejvýš {czech_count(MAX_PATTERNS)};" in EXACT_HINT
    with pytest.raises(ChipError, match="2 035 800 výstupních vzorů, simulátor jich přesně spočítá nejvýš 1 000 000\\."):
        pattern_distribution(random_unitary(24, np.random.default_rng(0)), 7, PhotonKind.INDISTINGUISHABLE)


def largest_allowed_tasks():
    allowed = [
        (modes, photons) for modes in MODE_COUNT_OPTIONS for photons in PHOTON_OPTIONS
        if photons <= modes and pattern_count(modes, photons) <= MAX_PATTERNS
    ]
    return [max(allowed), max(allowed, key=lambda task: (task[1], pattern_count(*task)))]


@pytest.mark.parametrize("modes, photons", largest_allowed_tasks())
def test_nejvetsi_ulohy_dobehnou_do_peti_sekund_a_vejdou_se_do_pameti(modes, photons):
    tracemalloc.start()
    started = time.perf_counter()
    study = run_sampling_study(ChipTarget.RANDOM, 0.08, 1, modes, photons, PhotonKind.INDISTINGUISHABLE, 100_000)
    build_sampling_results(study)
    elapsed = time.perf_counter() - started
    peak_mib = tracemalloc.get_traced_memory()[1] / 2**20
    tracemalloc.stop()

    assert elapsed < 5 and peak_mib < 150
    assert len(study.target.occupied_outputs) == pattern_count(modes, photons)


def test_laborator_ma_vlastni_sekci_a_kapitolu_ve_vykladu():
    page_ids = set(component_ids(build_chip_simulator_page()))

    assert {SAMPLING_ANCHOR, SAMPLING_TOPIC.anchor, ids.CHIP_SAMPLING_RUN_BUTTON, ids.CHIP_SAMPLING_RESULTS} <= page_ids
    assert TOPICS[-1] == SAMPLING_TOPIC


def test_formular_hlida_vstupy_a_ukaze_pocet_vzoru():
    assert parse_sampling_form(SAMPLING_FORM).photons == 3
    assert describe_pattern_count(16, 6) == "54 264 možných výstupních vzorů."
    assert describe_pattern_count(24, 7) == "2 035 800 výstupních vzorů, víc než 1 000 000, které simulátor spočítá."
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
