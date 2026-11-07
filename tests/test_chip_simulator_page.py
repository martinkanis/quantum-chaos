import itertools

import numpy as np
import pytest

from gbs.boson_sampling import permanent
from gbs.chip_charts import chip_figure
from gbs.chip_programming import ChipTarget, build_setup, design_phases, read_out, target_unitary
from gbs.photonic_chip import ChipError, MeshPhases, ideal_chip, mzi_count, mzi_matrix, pattern_match, transfer_matrix
from gbs.photonic_chip import transmission, zero_phases
from ui import ids
from ui.chip_simulator_callbacks import (
    parse_laser_input,
    parse_phases,
    parse_setup,
    phases_for_button,
    should_draw_chip,
    PHASE_DECIMALS,
)
from ui.chip_simulator_content import (
    FABRICATION,
    LAB_ANCHOR,
    LAB_INTRO,
    MESH,
    PHASES_HINT,
    PHOTONS,
    PROGRAMMING,
    SOURCES_ANCHOR,
    TARGET_LABELS,
    TOPICS,
)
from ui.chip_simulator_page import build_chip_simulator_page, external_phase_slider_ids, internal_phase_slider_ids
from ui.chip_simulator_results import build_chip_readout
from ui.navigation import CHIP_SIMULATOR_PATH, PRIMER_APPENDICES_PATH
from ui.study_progress import describe_pager
from ui.theory_content import all_sources
from ui.topic_catalog import breadcrumb_trail
from tests.test_topics import active_links, visible_pages

SETUP_FORM = {"target": ChipTarget.SPREAD_EVENLY.value, "split_spread": 0.0, "seed": 1}
HADAMARD = np.array([[1, 1, 1, 1], [1, -1, 1, -1], [1, 1, -1, -1], [1, -1, -1, 1]]) / 2


def text_of(topic) -> str:
    return " ".join((topic.in_short + " " + topic.explanation).split())


def component_ids(component):
    if getattr(component, "id", None):
        yield component.id
    children = getattr(component, "children", None)
    for child in children if isinstance(children, (list, tuple)) else [children]:
        if child is not None and not isinstance(child, str):
            yield from component_ids(child)


def texts_in(component):
    children = getattr(component, "children", None)
    for child in children if isinstance(children, (list, tuple)) else [children]:
        if isinstance(child, str):
            yield child
        elif child is not None:
            yield from texts_in(child)


def coincidence(unitary, inputs, outputs) -> float:
    return abs(permanent(unitary[np.ix_(outputs, inputs)])) ** 2


def test_simulator_je_v_tematu_fotonika_hned_za_skripty():
    _, step_label, links, _, _ = describe_pager(CHIP_SIMULATOR_PATH, None)

    assert visible_pages(CHIP_SIMULATOR_PATH) == [ids.CHIP_SIMULATOR_PAGE]
    assert active_links(CHIP_SIMULATOR_PATH) == [ids.NAV_PHOTONICS_MENU]
    assert step_label == "Fotonika · krok 6 / 12"
    assert links[0].children.href == PRIMER_APPENDICES_PATH
    assert [label for label, _ in breadcrumb_trail(ids.CHIP_SIMULATOR_PAGE)] == [
        "Témata", "Fotonika a GBS", "Simulátor fotonického čipu",
    ]


def test_stranka_ma_laborator_kapitoly_s_unikatnimi_kotvami_a_zdroje_bez_opakovani():
    page_ids = list(component_ids(build_chip_simulator_page()))
    anchors = [topic.anchor for topic in TOPICS]
    sources = all_sources(TOPICS)

    assert set(anchors + [LAB_ANCHOR, SOURCES_ANCHOR]) <= set(page_ids)
    assert len(page_ids) == len(set(page_ids))
    assert all(anchor.startswith("cip-") for anchor in anchors + [LAB_ANCHOR, SOURCES_ANCHOR])
    assert len(sources) == len(set(sources))
    assert all(topic.in_short.strip() and topic.explanation.strip() and topic.further_reading for topic in TOPICS)


def test_kazdy_mzi_ma_posuvnik_theta_i_phi_a_kazdy_cil_popisek():
    page_ids = set(component_ids(build_chip_simulator_page()))

    assert len(internal_phase_slider_ids()) == len(external_phase_slider_ids()) == mzi_count(4) == 6
    assert set(internal_phase_slider_ids()) | set(external_phase_slider_ids()) <= page_ids
    assert set(TARGET_LABELS) == set(ChipTarget)


def test_tlacitka_nastavi_navrh_doladeni_a_nulove_faze():
    setup = parse_setup({**SETUP_FORM, "split_spread": 0.03})
    designed = phases_for_button(ids.CHIP_PROGRAM_BUTTON, setup)
    calibrated = phases_for_button(ids.CHIP_CALIBRATE_BUTTON, setup)

    assert phases_for_button(ids.CHIP_RESET_BUTTON, setup) == zero_phases(4)
    assert designed == design_phases(setup)
    assert read_out(setup, calibrated, 0).match > read_out(setup, designed, 0).match


def test_zaokrouhlene_faze_na_posuvnicich_drzi_shodu_na_idealnim_cipu():
    setup = parse_setup(SETUP_FORM)
    designed = design_phases(setup)
    rounded = MeshPhases(
        tuple(round(phase, PHASE_DECIMALS) for phase in designed.internal),
        tuple(round(phase, PHASE_DECIMALS) for phase in designed.external),
    )

    assert read_out(setup, rounded, 0).match > 0.9999


def test_cip_se_kresli_pri_zmene_ovladace_a_poprve_na_sve_strance():
    assert should_draw_chip(internal_phase_slider_ids()[0], "/", current_readout=["už nakresleno"])
    assert should_draw_chip(None, CHIP_SIMULATOR_PATH, current_readout=None)
    assert not should_draw_chip(None, "/", current_readout=None)
    assert not should_draw_chip(ids.URL, CHIP_SIMULATOR_PATH, current_readout=["už nakresleno"])


def test_neplatne_vstupy_formulare_maji_ceskou_hlasku():
    with pytest.raises(ChipError, match="cíl"):
        parse_setup({**SETUP_FORM, "target": None})
    with pytest.raises(ChipError, match="čip"):
        parse_setup({**SETUP_FORM, "split_spread": "hodně"})
    with pytest.raises(ChipError, match="celé číslo"):
        parse_setup({**SETUP_FORM, "seed": 1.5})
    with pytest.raises(ChipError, match="radiánech"):
        parse_phases([0.0] * 5 + [None], [0.0] * 6)
    with pytest.raises(ChipError, match="vstup 1 až 4"):
        parse_laser_input(None)


def test_schema_cipu_ukazuje_laser_vstup_a_svetlo_na_detektorech():
    setup = parse_setup(SETUP_FORM)
    phases = design_phases(setup)
    readout = read_out(setup, phases, input_mode=1)
    labels = [annotation.text for annotation in chip_figure(setup.chip, phases, readout.flow).layout.annotations]

    assert "<b>laser ▸ 2</b>" in labels
    assert labels.count("<b>25,0 %</b>") == 4
    assert "MZI 6" in labels
    assert "100,0 %" in list(texts_in(build_chip_readout(readout)))


def test_cisla_v_navodu_odpovidaji_vypoctu():
    zero = transmission(transfer_matrix(ideal_chip(4), zero_phases(4)))

    assert np.allclose(zero[:, 0], [0, 0, 0, 1])
    assert pattern_match(zero, np.full((4, 4), 0.25)) == pytest.approx(0.25)
    assert "vstup 1 jde na výstup 4" in " ".join(LAB_INTRO.split())
    assert "je proto shoda jen 25 %" in " ".join(LAB_INTRO.split())
    assert "Shoda 25 % u nulových fází" in text_of(PROGRAMMING)


def test_popisky_fazi_a_sit_odpovidaji_mzi():
    assert abs(mzi_matrix(0.0, 0.0)[1, 0]) ** 2 == pytest.approx(1.0)
    assert abs(mzi_matrix(np.pi / 2, 0.0)[1, 0]) ** 2 == pytest.approx(0.5)
    assert abs(mzi_matrix(np.pi, 0.0)[0, 0]) ** 2 == pytest.approx(1.0)
    assert "(0 = vše do sousedního světlovodu, π/2 = půl na půl, π = rovně)" in PHASES_HINT
    assert mzi_count(4) == 6 and "Pro $N = 4$ to dělá 6 MZI a 12 fází." in text_of(MESH)


def test_pruchod_rozklad_posle_dvakrat_krizem_v_mzi_1_a_4():
    internal = design_phases(build_setup(ChipTarget.PASS_THROUGH, 0.0, seed=1)).internal
    crossed = [number for number, theta in enumerate(internal, start=1) if np.isclose(theta, 0.0)]

    assert crossed == [1, 4]
    assert np.allclose(np.delete(internal, [0, 3]), np.pi)
    assert "MZI 1 a 4 nechá v křížovém stavu" in text_of(PROGRAMMING)


def test_fourierova_a_hadamardova_matice_rozlisi_az_dva_fotony():
    fourier = target_unitary(ChipTarget.SPREAD_EVENLY, 4, np.random.default_rng(0))

    assert np.allclose(transmission(fourier), 0.25) and np.allclose(transmission(HADAMARD), 0.25)
    assert coincidence(fourier, inputs=[0, 1], outputs=[0, 1]) == pytest.approx(0.125)
    assert coincidence(HADAMARD, inputs=[0, 1], outputs=[0, 1]) == pytest.approx(0.0)
    assert "s pravděpodobností 12,5 %, Hadamardova nikdy" in text_of(PHOTONS)


def test_ztrata_krizoveho_stavu_v_textu_sedi_se_vzorcem():
    leak = (1 - 2 * 0.53) ** 2

    assert f"{100 * leak:.2f}".replace(".", "{,}") == "0{,}36"
    assert "(1 - 2 \\cdot 0{,}53)^2 = 0{,}36$ %" in text_of(FABRICATION)


def test_dvoufotonove_pravdepodobnosti_fourierovy_matice_daji_dohromady_jedna():
    fourier = target_unitary(ChipTarget.SPREAD_EVENLY, 4, np.random.default_rng(0))
    total = sum(
        coincidence(fourier, [0, 1], list(outputs)) / (2 if outputs[0] == outputs[1] else 1)
        for outputs in itertools.combinations_with_replacement(range(4), 2)
    )

    assert total == pytest.approx(1.0)
