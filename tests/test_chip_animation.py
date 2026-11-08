import re
from pathlib import Path
from typing import Tuple

import numpy as np
import plotly.graph_objects as go
import pytest

from gbs.chip_boson_sampling import PhotonKind, run_sampling_study
from gbs.chip_charts import WAVEGUIDE_COLOR, chip_figure
from gbs.bench import LightSource
from gbs.chip_programming import ChipTarget, build_setup, design_phases
from gbs.photonic_chip import ESTIMATED_COLUMN_TRANSIT_SECONDS, MODE_COUNT, estimated_transit_seconds, light_flow
from ui import ids
from ui.chip_animation import ANIMATION_CLASS
from ui.chip_sampling_results import build_sampling_results
from ui.chip_simulator_content import ANIMATION_HINT
from ui.chip_simulator_page import build_chip_simulator_page
from tests.test_chip_simulator_page import component_ids

ANIMATION_SCRIPT = Path(__file__).resolve().parent.parent / "assets" / "chip_animation.js"
LIGHT_COLORS = ("rgba(80, 220, 255", "rgba(215, 250, 255")


def laser_animation(target: ChipTarget, laser_input: int) -> Tuple[go.Figure, dict]:
    setup = build_setup(target, 0.0, 1)
    phases = design_phases(setup)
    figure = chip_figure(setup.chip, phases, light_flow(setup.chip, phases, (laser_input,)))
    return figure, figure.layout.meta["lightAnimation"]


def segments_of(lane):
    return [lane[index:index + 4] for index in range(1, len(lane), 4)]


def light_at(animation: dict, x: float) -> float:
    return sum(
        lane[0] for lane in animation["lanes"]
        if any(start <= x < end for start, end, _, _ in segments_of(lane))
    )


def animation_controls(component):
    if getattr(component, "className", None) == ANIMATION_CLASS:
        yield component.to_plotly_json()["props"]
    children = getattr(component, "children", None)
    for child in children if isinstance(children, (list, tuple)) else [children]:
        if child is not None and not isinstance(child, str):
            yield from animation_controls(child)


@pytest.mark.parametrize("target", list(ChipTarget))
def test_cela_svetla_laseru_prochazi_kazdym_rezem_cipu_a_animace_nema_mezery(target):
    _, animation = laser_animation(target, 0)

    for x in np.linspace(animation["start"], animation["end"], 400, endpoint=False):
        assert light_at(animation, x) == pytest.approx(1.0, abs=0.01)


def test_kazda_draha_animace_je_souvisla_zleva_doprava():
    _, animation = laser_animation(ChipTarget.RANDOM, 2)

    for lane in animation["lanes"]:
        segments = segments_of(lane)
        assert all(start < end for start, end, _, _ in segments)
        for (_, end, _, end_y), (start, _, start_y, _) in zip(segments, segments[1:]):
            assert (end, end_y) == (start, start_y)


@pytest.mark.parametrize("mode_count", [2, 4, 8])
def test_skutecny_cas_pruchodu_animace_cte_z_obrazku_podle_velikosti_cipu(mode_count):
    setup = build_setup(ChipTarget.RANDOM, 0.0, 1, mode_count)
    phases = design_phases(setup)
    figure = chip_figure(setup.chip, phases, light_flow(setup.chip, phases, (0,)))

    assert figure.layout.meta["lightAnimation"]["transitSeconds"] == estimated_transit_seconds(mode_count)


def test_animace_odkryva_prave_tvary_svetla_a_meri_podle_svetlovodu():
    figure, animation = laser_animation(ChipTarget.SPREAD_EVENLY, 1)
    light_shapes = [
        index for index, shape in enumerate(figure.layout.shapes)
        if shape.line.color and shape.line.color.startswith(LIGHT_COLORS)
    ]

    assert animation["lightShapes"] == light_shapes
    assert figure.layout.shapes[animation["waveguideShape"]].line.color == WAVEGUIDE_COLOR
    assert animation["top"] == MODE_COUNT - 1


def test_odhad_skutecneho_pruchodu_v_textu_sedi_s_vypoctem_a_se_snimkem_obrazovky():
    frame_rate = int(re.search(r"FRAME_SECONDS = 1 / (\d+);", ANIMATION_SCRIPT.read_text()).group(1))
    hint = " ".join(ANIMATION_HINT.split())

    assert ESTIMATED_COLUMN_TRANSIT_SECONDS == pytest.approx(10e-12)
    assert estimated_transit_seconds(MODE_COUNT) == pytest.approx(40e-12)
    assert "proletí asi za 10 ps a celý čip se 4 světlovody zhruba za 40 ps" in hint
    assert f"(asi {round(1000 / frame_rate)} ms)" in hint


def test_ovladani_animace_je_u_cipu_v_laboratori_i_u_vystrelu_fotonu():
    page_controls = list(animation_controls(build_chip_simulator_page()))
    study = run_sampling_study(ChipTarget.RANDOM, 0.0, 1, 8, 3, PhotonKind.INDISTINGUISHABLE, 100)
    results = build_sampling_results(study)
    result_controls = list(animation_controls(results))

    assert [(props["data-graph"], props["data-source"]) for props in page_controls] == [
        (ids.CHIP_FIGURE, LightSource.LASER.value),
    ]
    assert [(props["data-graph"], props["data-source"]) for props in result_controls] == [
        (ids.CHIP_SAMPLING_FIGURE, LightSource.PHOTONS.value),
    ]
    assert ids.CHIP_SAMPLING_FIGURE in set(component_ids(results))
