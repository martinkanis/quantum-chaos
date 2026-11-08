import time
import tracemalloc
from itertools import combinations_with_replacement
from math import comb, factorial
from typing import Any

import numpy as np
import pytest

from gbs.boson_sampling import output_patterns, permanent, random_unitary, transition_matrix
from gbs.chip_boson_sampling import (
    MAX_PATTERNS,
    PhotonKind,
    SamplingStudy,
    all_pattern_permanents,
    complete_homogeneous,
    gaussian_estimator_values,
    occupied_outputs,
    pattern_count,
    pattern_distribution,
    run_sampling_study,
)
from gbs.chip_parts import czech_percent
from gbs.chip_programming import ChipTarget, target_unitary
from gbs.chip_sampling_charts import convergence_chart
from gbs.photonic_chip import ChipError, mzi_count
from ui import ids
from ui.chip_sampling_callbacks import describe_pattern_count, parse_sampling_form, run_boson_sampling
from ui.chip_sampling_content import (
    EXACT_HINT,
    MAX_SAMPLING_MODE_COUNT,
    MIN_SAMPLING_MODE_COUNT,
    PHOTON_OPTIONS,
    SAMPLING_ANCHOR,
    SAMPLING_INTRO,
    SAMPLING_TOPIC,
)
from ui.chip_sampling_results import build_sampling_results, czech_count, czech_decimal
from ui.chip_simulator_content import TOPICS
from ui.chip_simulator_page import build_chip_simulator_page
from tests.test_chip_simulator_page import component_ids, texts_in

TEST_DRAWS_SEED = 7


def sampling_study(*args: Any) -> SamplingStudy:
    """run_sampling_study whose shots and Gaussian vectors are seeded, so that the tests are deterministic."""
    return run_sampling_study(*args, draws=np.random.default_rng(TEST_DRAWS_SEED))


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


def test_dvojice_fotonu_v_haarove_interferometru_skonci_spolu_s_pravdepodobnosti_dve_ku_m_plus_jedna():
    modes, draws = 5, 2000
    rng = np.random.default_rng(11)
    bosons, particles = [], []
    for _ in range(draws):
        unitary = random_unitary(modes, rng)
        bosons.append(1 - pattern_distribution(unitary, 2, PhotonKind.INDISTINGUISHABLE).collision_free_share)
        particles.append(1 - pattern_distribution(unitary, 2, PhotonKind.DISTINGUISHABLE).collision_free_share)

    assert np.allclose(bosons, 2 * np.array(particles))
    assert abs(np.mean(bosons) - 2 / (modes + 1)) < 4 * np.std(bosons) / np.sqrt(draws)
    assert "dvojice skončí spolu s pravděpodobností $2/(m+1)$, rozlišitelná $1/(m+1)$" in text_of(SAMPLING_TOPIC)


def collision_numbers(modes: int, photons: int):
    bosons = sampling_study(ChipTarget.RANDOM, 0.0, 1, modes, photons, PhotonKind.INDISTINGUISHABLE, 10)
    particles = sampling_study(ChipTarget.RANDOM, 0.0, 1, modes, photons, PhotonKind.DISTINGUISHABLE, 10)
    return (
        bosons.crowding, czech_percent(bosons.target.collision_free_share),
        czech_percent(particles.sampler.collision_free_share),
        round(bosons.target.bunching, 2), round(particles.sampler.bunching, 2),
    )


def test_cisla_o_kolizich_ve_vykladu_odpovidaji_vypoctu():
    text = text_of(SAMPLING_TOPIC)

    assert collision_numbers(64, 4) == (0.25, "81,6 %", "90,3 %", 1.22, 1.10)
    assert collision_numbers(16, 8) == (4.0, "2,6 %", "13,7 %", 18.5, 4.10)
    assert ("64 světlovody a 4 fotony ($n^2/m = 0{,}25$) bez kolize 81,6 % výstřelů, u rozlišitelných fotonů 90,3 %, "
            "a $\\mu = 1{,}22$ proti $1{,}10$") in text
    assert "($n^2/m = 4$) je to jen 2,6 % proti 13,7 % a $\\mu = 18{,}5$ proti $4{,}10$" in text


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
    ideal = sampling_study(ChipTarget.RANDOM, 0.0, 1, 8, 4, PhotonKind.INDISTINGUISHABLE, 20_000)
    fabricated = sampling_study(ChipTarget.RANDOM, 0.08, 1, 8, 4, PhotonKind.INDISTINGUISHABLE, 20_000)
    fewer_shots = sampling_study(ChipTarget.RANDOM, 0.08, 1, 8, 4, PhotonKind.INDISTINGUISHABLE, 1_000)

    assert abs(ideal.bias) < 1e-9
    assert abs(ideal.estimate - ideal.target.bunching) < 4 * ideal.standard_error
    assert abs(fabricated.bias) > 0.01 and fabricated.bias == fewer_shots.bias
    assert abs(fabricated.estimate - fabricated.sampler.bunching) < 4 * fabricated.standard_error


@pytest.mark.parametrize("target", [ChipTarget.RANDOM, ChipTarget.SPREAD_EVENLY])
def test_rozlisitelne_fotony_v_prikladech_simulatoru_mu_snizi(target):
    for seed in range(1, 6):
        study = sampling_study(target, 0.0, seed, 16, 6, PhotonKind.DISTINGUISHABLE, 100)

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
        (modes, photons) for modes in range(MIN_SAMPLING_MODE_COUNT, MAX_SAMPLING_MODE_COUNT + 1)
        for photons in PHOTON_OPTIONS
        if photons <= modes and pattern_count(modes, photons) <= MAX_PATTERNS
    ]
    return [max(allowed), max(allowed, key=lambda task: (task[1], pattern_count(*task)))]


@pytest.mark.parametrize("modes, photons", largest_allowed_tasks())
def test_nejvetsi_ulohy_dobehnou_do_peti_sekund_a_vejdou_se_do_pameti(modes, photons):
    tracemalloc.start()
    started = time.perf_counter()
    study = sampling_study(ChipTarget.RANDOM, 0.08, 1, modes, photons, PhotonKind.INDISTINGUISHABLE, 100_000)
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
    for invalid in (1, 65, 12.5, None):
        with pytest.raises(ChipError, match="od 2 do 64"):
            parse_sampling_form({**SAMPLING_FORM, "mode_count": invalid})
    assert describe_pattern_count(65, 3) == "Počet světlovodů musí být celé číslo od 2 do 64."
    limits = f"({MIN_SAMPLING_MODE_COUNT} až {MAX_SAMPLING_MODE_COUNT})"
    assert f"počet světlovodů {limits}" in " ".join(SAMPLING_INTRO.split())
    assert describe_pattern_count(17, 8) == "735 471 možných výstupních vzorů."


def test_vysledky_ukazuji_oba_odhady_a_prvni_vystrely():
    study = sampling_study(ChipTarget.SPREAD_EVENLY, 0.0, 1, 4, 2, PhotonKind.INDISTINGUISHABLE, 1000)
    texts = list(texts_in(build_sampling_results(study)))

    assert "1,50" in texts and "10" in texts
    assert any(text.startswith("Boson sampling, 1 000 výstřelů") for text in texts)
    assert any(text.startswith("výstupy ") and "→ Z = " in text for text in texts)
    assert any(text.startswith("Bez kolize, n²/m = 1,00") for text in texts) and "50,0 % (čip 50,0 %)" in texts
    assert czech_decimal(1502.27) == "1 502,27" and czech_decimal(0.01482) == "0,0148"


def test_cisla_v_podkapitole_o_spdc_sedi_s_vypoctem():
    text = text_of(SAMPLING_TOPIC)
    pair_probability, photons, inputs = 0.01, 4, 16
    fixed_inputs = pair_probability ** photons
    scattershot = comb(inputs, photons) * fixed_inputs * (1 - pair_probability) ** (inputs - photons)

    assert "Pro $p = 1$ %" in text and "Pro 16 vstupů, čtyři fotony a $p = 1$ %" in text
    assert fixed_inputs == pytest.approx(1e-8) and "je to $10^{-8}$" in text
    assert f"{scattershot:.1e}" == "1.6e-05" and r"asi $1{,}6 \cdot 10^{-5}$" in text
    assert round(scattershot / fixed_inputs, -2) == 1600 and "zhruba 1 600krát častěji" in text


def test_kazde_spusteni_losuje_nove_vystrely_na_stejnem_interferometru():
    form = {**SAMPLING_FORM, "mode_count": 16, "photons": 6}
    runs = [list(texts_in(run_boson_sampling(1, form)["results"])) for _ in range(2)]
    first_shots = [[text for text in texts if text.startswith("výstupy ")] for texts in runs]
    exact_mu = [texts[texts.index("Přesné μ ⓘ") + 1] for texts in runs]

    assert len(first_shots[0]) == 8 and first_shots[0] != first_shots[1]
    assert exact_mu[0] == exact_mu[1]


def test_graf_konvergence_jde_prepnout_na_linearni_osu_x_a_priblizit_osu_y_kolem_mu():
    study = sampling_study(ChipTarget.RANDOM, 0.0, 1, 16, 6, PhotonKind.INDISTINGUISHABLE, 10_000)
    figure = convergence_chart(study)
    x_menu, y_menu = figure.layout.updatemenus
    y_changes = {button.label: button.args[0] for button in y_menu.buttons}
    around = y_changes["Y kolem μ"]["yaxis.range"]
    chip_curve = np.array(figure.data[1].y)
    settled = chip_curve[len(chip_curve) // 2:]
    exact = study.target.bunching

    assert [button.args[0]["xaxis.type"] for button in x_menu.buttons] == ["log", "linear"]
    assert list(y_changes["Y 0 až 2μ"]["yaxis.range"]) == [0, 2 * exact]
    assert y_changes["Y vše"] == {"yaxis.autorange": True}
    assert around[0] < min(exact, settled.min()) and max(exact, settled.max()) < around[1]
    assert 5 * (around[1] - around[0]) < 2 * exact
    assert figure.layout.separators == ", "
