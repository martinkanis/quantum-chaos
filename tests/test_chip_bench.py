import numpy as np
import pytest

from gbs.bench import (
    DETECTORS,
    Bench,
    DetectorKind,
    LightSource,
    Losses,
    bench_transmission,
    compatible_detector,
    count_photons,
    loss_db,
    registered_shares,
)
from gbs.chip_programming import ChipTarget, build_setup
from gbs.photonic_chip import ChipError, MODE_COUNT
from ui import ids
from ui.chip_bench_callbacks import match_detector_to_source, show_photon_controls
from ui.chip_bench_content import BENCH_TOPIC, DEFAULT_COUPLING_LOSS_DB, DEFAULT_WAVEGUIDE_LOSS_DB_PER_CM, REDDY_2020
from ui.chip_bench_results import build_bench_readout
from ui.chip_simulator_callbacks import parse_bench
from ui.chip_simulator_content import TOPICS
from ui.chip_simulator_page import build_chip_simulator_page
from ui.navigation import HIDDEN, VISIBLE
from tests.test_chip_simulator_page import component_ids, texts_in

DEFAULT_LOSSES = Losses(DEFAULT_COUPLING_LOSS_DB, DEFAULT_WAVEGUIDE_LOSS_DB_PER_CM)
BENCH_FORM = {
    "source": LightSource.LASER.value, "detector": DetectorKind.PHOTODIODE.value, "coupling_db": 1.5,
    "waveguide_db_per_cm": 1.0, "source_input": 0, "source_on": True,
}
FOURIER_COLUMN = np.full(4, 0.25)


def topic_text() -> str:
    return " ".join((BENCH_TOPIC.in_short + " " + BENCH_TOPIC.explanation).split())


def test_cisla_ve_vykladu_pracovniho_stolu_sedi_s_vypoctem():
    text = topic_text()
    transmission = bench_transmission(DEFAULT_LOSSES, MODE_COUNT)
    efficiencies = {kind: DETECTORS[kind].efficiency for kind in DetectorKind}

    assert loss_db(DEFAULT_LOSSES, MODE_COUNT) == pytest.approx(3.4)
    assert round(100 * transmission) == 46 and "ztratí 3,4 dB a propustí asi 46 % světla" in text
    assert round(100 * transmission * efficiencies[DetectorKind.PHOTODIODE]) == 37 and "asi 37 % světla laseru" in text
    assert efficiencies == {DetectorKind.PHOTODIODE: 0.8, DetectorKind.APD: 0.2, DetectorKind.SNSPD: 0.9}
    assert "u nás 80 %" in text and "účinnost 20 %" in text and "účinnost 90 %" in text
    assert DETECTORS[DetectorKind.APD].dark_click_probability == 1e-4 and "$10^{-4}$" in text
    assert DETECTORS[DetectorKind.SNSPD].dark_click_probability == 1e-6 and "$10^{-6}$" in text
    assert efficiencies[DetectorKind.SNSPD] / efficiencies[DetectorKind.APD] == pytest.approx(4.5)
    assert "zhruba 4,5krát méně fotonů" in text and "98 %" in text and "98%" in REDDY_2020.citation


def test_kapitola_pracovniho_stolu_je_ve_vykladu_pred_boson_samplingem():
    assert TOPICS[-2] == BENCH_TOPIC
    assert len({topic.anchor for topic in TOPICS}) == len(TOPICS)


def test_ztraty_zmensi_vsechny_vystupy_stejne_a_detektor_jen_cast_zaznamena():
    registered = registered_shares(FOURIER_COLUMN, DEFAULT_LOSSES, DETECTORS[DetectorKind.SNSPD], MODE_COUNT)

    assert np.allclose(registered / registered.sum(), FOURIER_COLUMN)
    assert registered.sum() == pytest.approx(bench_transmission(DEFAULT_LOSSES, MODE_COUNT) * 0.9)
    assert bench_transmission(Losses(0.0, 0.0), 8) == 1.0


def test_detektor_se_ridi_zdrojem():
    assert compatible_detector(LightSource.PHOTONS, DetectorKind.PHOTODIODE) == DetectorKind.SNSPD
    assert compatible_detector(LightSource.PHOTONS, DetectorKind.APD) == DetectorKind.APD
    assert compatible_detector(LightSource.LASER, DetectorKind.SNSPD) == DetectorKind.PHOTODIODE
    with pytest.raises(ChipError, match="Fotodioda měří jen laser"):
        Bench(LightSource.PHOTONS, DetectorKind.PHOTODIODE, DEFAULT_LOSSES)


def test_prepnuti_zdroje_zakaze_nevhodne_detektory_a_ukaze_citac():
    options, detector = match_detector_to_source(LightSource.PHOTONS.value, DetectorKind.PHOTODIODE.value)
    disabled = {option["value"]: option["disabled"] for option in options}

    assert detector == DetectorKind.SNSPD.value
    assert disabled == {"fotodioda": True, "apd": False, "snspd": False}
    assert match_detector_to_source(LightSource.LASER.value, DetectorKind.APD.value)[1] == DetectorKind.PHOTODIODE.value
    assert show_photon_controls(LightSource.PHOTONS.value) == VISIBLE and show_photon_controls("laser") == HIDDEN
    assert parse_bench({**BENCH_FORM, "source": "fotony"}).detector_kind == DetectorKind.SNSPD


@pytest.mark.parametrize("coupling, waveguide, message", [(-1, 1, "vazby"), (12, 1, "vazby"), (1, 6, "Útlum")])
def test_ztraty_mimo_rozsah_maji_ceskou_hlasku(coupling, waveguide, message):
    with pytest.raises(ChipError, match=message):
        parse_bench({**BENCH_FORM, "coupling_db": coupling, "waveguide_db_per_cm": waveguide})


def test_citace_fotonu_v_prumeru_trefi_ocekavane_cetnosti():
    detector = DETECTORS[DetectorKind.APD]
    registered = registered_shares(np.array([0.7, 0.2, 0.1, 0.0]), DEFAULT_LOSSES, detector, MODE_COUNT)
    counts = count_photons(registered, detector, 100_000, np.random.default_rng(4))

    assert counts.expected == pytest.approx(100_000 * (registered + (1 - registered) * 1e-4))
    assert np.all(np.abs(counts.clicks - counts.expected) < 5 * np.sqrt(counts.expected) + 1)
    assert counts.silent_shots == pytest.approx(100_000 * (1 - registered.sum()), rel=0.02)


def test_fotodioda_fotony_nepocita():
    with pytest.raises(ChipError, match="Fotodioda jednotlivé fotony nezaznamená"):
        count_photons(FOURIER_COLUMN, DETECTORS[DetectorKind.PHOTODIODE], 100, np.random.default_rng(0))


def test_odpocet_stolu_pro_laser_fotony_i_vypnuty_zdroj():
    laser = list(texts_in(build_bench_readout(parse_bench(BENCH_FORM), FOURIER_COLUMN, MODE_COUNT)))
    photons = list(texts_in(build_bench_readout(parse_bench({**BENCH_FORM, "source": "fotony"}), FOURIER_COLUMN, 4)))
    off = list(texts_in(build_bench_readout(parse_bench(BENCH_FORM), None, MODE_COUNT)))

    assert any(text.startswith("Stůl propustí 45,7 % světla: ztráta 3,4 dB") for text in laser)
    assert "Změří fotodioda" in laser and "9,1 %" in laser
    assert "Cvaknutí na jeden foton" in photons and any(text.startswith("Žádný detektor necvakne") for text in photons)
    assert off == ["Zdroj je vypnutý, detektory nic nezaznamenají."]


def test_jiny_kus_cipu_ma_jine_vyrobni_chyby_ale_stejny_cil():
    first = build_setup(ChipTarget.RANDOM, 0.08, 3, 4, chip_unit=1)
    second = build_setup(ChipTarget.RANDOM, 0.08, 3, 4, chip_unit=2)

    assert np.allclose(first.target, second.target)
    assert first.chip.split_angles != second.chip.split_angles
    assert build_setup(ChipTarget.RANDOM, 0.08, 3, 4).chip == build_setup(ChipTarget.RANDOM, 0.08, 3, 4, 3).chip


def test_pracovni_stul_ma_na_strance_vsechna_ovladani():
    page_ids = set(component_ids(build_chip_simulator_page()))

    assert {
        ids.CHIP_SOURCE_RADIO, ids.CHIP_DETECTOR_RADIO, ids.CHIP_COUPLING_LOSS_SLIDER, ids.CHIP_WAVEGUIDE_LOSS_SLIDER,
        ids.CHIP_UNIT_INPUT, ids.CHIP_NEW_UNIT_BUTTON, ids.CHIP_BENCH_READOUT, ids.CHIP_PHOTON_SHOOT_BUTTON,
        ids.CHIP_PHOTON_COUNTS, ids.CHIP_FABRICATION_DROPDOWN, ids.CHIP_LASER_RADIO,
    } <= page_ids
