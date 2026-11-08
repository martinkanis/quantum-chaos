import numpy as np
import pytest
from dash import no_update

from gbs.chip_charts import SELECTED_COLOR, ChipInteraction, chip_figure
from gbs.chip_geometry import INTERNAL_SHIFTER_AT, column_x
from gbs.chip_hover_texts import INPUT_CLICK_HINT, MZI_CLICK_HINT, SHIFTER_CLICK_HINT
from gbs.chip_parts import ChipPart, ClickedPart, SelectedShifter, clicked_part
from gbs.chip_programming import ChipTarget, build_setup, design_phases, read_out
from gbs.photonic_chip import light_flow, random_phases
from ui.chip_interaction_callbacks import (
    describe_laser_button,
    select_chip_part,
    shown_phase,
    toggle_laser,
    written_phase,
)
from ui.chip_selection import DEFAULT_SELECTED_SHIFTER, parse_selected_shifter, selected_shifter_data
from ui.chip_simulator_content import SOURCE_OFF_LABEL, SOURCE_ON_LABEL

SETUP = build_setup(ChipTarget.SPREAD_EVENLY, 0.0, 1)
PHASES = design_phases(SETUP)
THETA_2 = SelectedShifter(ChipPart.INTERNAL_SHIFTER, 1)


def interactive_figure(selected: SelectedShifter = THETA_2):
    return chip_figure(SETUP.chip, PHASES, light_flow(SETUP.chip, PHASES, (0,)), interaction=ChipInteraction(selected))


def click_on(figure, part: ChipPart, index: int) -> dict:
    """clickData as dcc.Graph sends it for the point of the part."""
    for trace in figure.data:
        for values in trace.customdata:
            if tuple(values[-2:]) == (part.value, index):
                return {"points": [{"customdata": list(values)}]}
    raise AssertionError(f"{part} {index} není v obrázku čipu")


@pytest.mark.parametrize("part, index", [
    (ChipPart.INPUT, 2), (ChipPart.INTERNAL_SHIFTER, 3), (ChipPart.EXTERNAL_SHIFTER, 0), (ChipPart.MZI, 5),
    (ChipPart.COUPLER, 4), (ChipPart.DETECTOR, 1), (ChipPart.WAVEGUIDE, 3),
])
def test_kliknuti_na_cip_pozna_soucastku_a_jeji_cislo(part, index):
    assert clicked_part(click_on(interactive_figure(), part, index)) == ClickedPart(part, index)


def test_kliknuti_mimo_soucastku_nic_nevybere():
    assert clicked_part(None) is None
    assert clicked_part({"points": []}) is None
    assert clicked_part({"points": [{"customdata": ["1", "neznámé", 0]}]}) is None


def test_klik_na_vstup_tam_presune_a_zapne_laser_klik_na_mzi_vybere_jeho_theta():
    figure = interactive_figure()

    assert select_chip_part(click_on(figure, ChipPart.INPUT, 3)) == dict(selected=no_update, laser=3, laser_on=True)
    assert select_chip_part(click_on(figure, ChipPart.EXTERNAL_SHIFTER, 4))["selected"] == {"part": "phi", "mzi": 4}
    assert select_chip_part(click_on(figure, ChipPart.MZI, 2))["selected"] == {"part": "theta", "mzi": 2}
    assert select_chip_part(click_on(figure, ChipPart.COUPLER, 2)) == dict(
        selected=no_update, laser=no_update, laser_on=no_update,
    )


def test_vybrany_posouvac_svitic_ramecek_a_napovedy_jen_na_klikacim_cipu():
    figure = interactive_figure()
    quiet = chip_figure(SETUP.chip, PHASES, light_flow(SETUP.chip, PHASES, (0,)))
    frames = [shape for shape in figure.layout.shapes if shape.line.color == SELECTED_COLOR]
    hints = {values[-3] for trace in figure.data for values in trace.customdata}

    slot = SETUP.chip.slots[THETA_2.mzi]
    shifter_x = column_x(slot.column, INTERNAL_SHIFTER_AT)

    assert len(frames) == 1 and frames[0].x0 < shifter_x < frames[0].x1
    assert {INPUT_CLICK_HINT, SHIFTER_CLICK_HINT, MZI_CLICK_HINT} <= hints
    assert not any(shape.line.color == SELECTED_COLOR for shape in quiet.layout.shapes)
    assert not any(INPUT_CLICK_HINT in values for trace in quiet.data for values in trace.customdata)


def test_posuvnik_nad_cipem_zapise_jen_vybranou_fazi_a_po_vyberu_ukaze_jeji_hodnotu():
    internal, external = [0.1, 0.2, 0.3], [1.1, 1.2, 1.3]

    written = written_phase(SelectedShifter(ChipPart.EXTERNAL_SHIFTER, 1), 2.71828, 3)
    shown = shown_phase(THETA_2, internal, external, 3)

    assert written["external"] == [no_update, 2.7183, no_update] and written["internal"] == [no_update] * 3
    assert shown["value"] == 0.2 and shown["title"] == "θ2 · MZI 2 (světlovody 2 a 3) – dělení světla"


def test_ulozeny_vyber_mimo_novy_cip_spadne_na_theta1():
    assert parse_selected_shifter(selected_shifter_data(THETA_2), 6) == THETA_2
    assert parse_selected_shifter({"part": "phi", "mzi": 9}, 6) == DEFAULT_SELECTED_SHIFTER
    assert parse_selected_shifter(None, 6) == DEFAULT_SELECTED_SHIFTER


def test_vypnuty_laser_cip_zhasne_a_tlacitko_rika_co_udela():
    dark = read_out(SETUP, PHASES, None)

    assert dark.flow.input_modes == () and not any(dark.flow.detected)
    assert dark.match == read_out(SETUP, PHASES, 0).match
    assert toggle_laser(1, True) is False and toggle_laser(2, False) is True
    assert describe_laser_button(True) == SOURCE_OFF_LABEL and describe_laser_button(False) == SOURCE_ON_LABEL


def test_nahodne_faze_jsou_v_rozsahu_a_pro_kazdy_mzi():
    phases = random_phases(6, np.random.default_rng(3))

    assert len(phases.internal) == len(phases.external) == 15
    assert all(0 <= phase < 2 * np.pi for phase in phases.internal + phases.external)
