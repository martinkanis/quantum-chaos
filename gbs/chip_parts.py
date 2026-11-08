"""Parts of the drawn chip a reader can point at: inputs, waveguides, phase shifters, couplers, MZIs and detectors.

Each kind of part is one invisible Plotly trace. Its hover template describes the part (gbs/chip_hover_texts.py),
and the customdata of every point ends with the kind of part and its number, so that a click can tell what it hit.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Optional, Tuple

import plotly.graph_objects as go

from gbs.bench import LightSource
from gbs.chip_geometry import (
    EXTERNAL_SHIFTER_AT,
    FIRST_COUPLER_CENTER,
    INTERNAL_SHIFTER_AT,
    LEAD_LENGTH,
    MAX_SHIFTER_MODES,
    SECOND_COUPLER_CENTER,
    chip_end,
    column_x,
    label_room,
    modes_outside_mzis,
    wire_y,
)
from gbs.chip_hover_texts import (
    COUPLER_HOVER,
    EXTERNAL_SHIFTER_HOVER,
    INPUT_CLICK_HINT,
    INPUT_HOVER,
    INTERNAL_SHIFTER_HOVER,
    LASER_DETECTOR_HOVER,
    MZI_CLICK_HINT,
    MZI_HOVER,
    PHOTON_DETECTOR_HOVER,
    SHIFTER_CLICK_HINT,
    WAVEGUIDE_HOVER,
)
from gbs.photonic_chip import Chip, LightFlow, MeshPhases, mzi_matrix, split_ratios

HOVER_MARKER_SIZE = 24
NO_HINT = ""


class ChipPart(str, Enum):
    INPUT = "vstup"
    WAVEGUIDE = "svetlovod"
    EXTERNAL_SHIFTER = "phi"
    INTERNAL_SHIFTER = "theta"
    COUPLER = "delic"
    MZI = "mzi"
    DETECTOR = "detektor"


@dataclass(frozen=True)
class ClickedPart:
    part: ChipPart
    index: int
    """The waveguide of inputs, waveguides and detectors, the MZI of shifters, couplers and MZIs; counted from 0."""


@dataclass(frozen=True)
class SelectedShifter:
    part: ChipPart
    """ChipPart.INTERNAL_SHIFTER (θ) or ChipPart.EXTERNAL_SHIFTER (φ)."""
    mzi: int


HoverSpot = Tuple[float, float, int, Tuple[str, ...]]
"""Position of an invisible hover target, the waveguide or MZI it belongs to, and the values its description
template reads from customdata."""


def add_part_hovers(
    figure: go.Figure, chip: Chip, phases: MeshPhases, flow: LightFlow, source: LightSource, is_clickable: bool,
) -> None:
    """Every part of the chip describes itself on hover. Shared text sits in the template once per kind of part, so
    even large chips stay small; on a clickable chip inputs, shifters and MZIs also say what a click does."""
    input_hint, shifter_hint, mzi_hint = (
        (INPUT_CLICK_HINT, SHIFTER_CLICK_HINT, MZI_CLICK_HINT) if is_clickable else (NO_HINT, NO_HINT, NO_HINT)
    )
    _add_hover_trace(figure, ChipPart.INPUT, _input_spots(flow, chip.mode_count, source, input_hint), INPUT_HOVER)
    _add_hover_trace(figure, ChipPart.WAVEGUIDE, _waveguide_spots(chip, flow, source), WAVEGUIDE_HOVER)
    if chip.mode_count <= MAX_SHIFTER_MODES:
        external, internal = _shifter_spots(chip, phases, shifter_hint)
        _add_hover_trace(figure, ChipPart.EXTERNAL_SHIFTER, external, EXTERNAL_SHIFTER_HOVER)
        _add_hover_trace(figure, ChipPart.INTERNAL_SHIFTER, internal, INTERNAL_SHIFTER_HOVER)
    _add_hover_trace(figure, ChipPart.COUPLER, _coupler_spots(chip), COUPLER_HOVER)
    _add_hover_trace(figure, ChipPart.MZI, _mzi_spots(chip, phases, mzi_hint), MZI_HOVER)
    detector_hover = LASER_DETECTOR_HOVER if source == LightSource.LASER else PHOTON_DETECTOR_HOVER
    _add_hover_trace(figure, ChipPart.DETECTOR, _detector_spots(flow, chip.mode_count, source), detector_hover)


def clicked_part(click_data: Any) -> Optional[ClickedPart]:
    """The part a click on the chip hit (clickData of dcc.Graph), None if the click carries no part."""
    points = click_data.get("points") if isinstance(click_data, dict) else None
    values = points[0].get("customdata") if points and isinstance(points[0], dict) else None
    if not isinstance(values, list) or len(values) < 2:
        return None
    part, index = values[-2], values[-1]
    if part not in {known.value for known in ChipPart} or not isinstance(index, int):
        return None
    return ClickedPart(ChipPart(part), index)


def _add_hover_trace(figure: go.Figure, part: ChipPart, spots: List[HoverSpot], template: str) -> None:
    xs, ys, indices, values = zip(*spots)
    figure.add_trace(go.Scatter(
        x=xs, y=ys, customdata=[(*shown, part.value, index) for shown, index in zip(values, indices)],
        hovertemplate=template + "<extra></extra>", mode="markers",
        marker=dict(size=HOVER_MARKER_SIZE, color="rgba(0, 0, 0, 0)"),
    ))


def _input_spots(flow: LightFlow, mode_count: int, source: LightSource, hint: str) -> List[HoverSpot]:
    x = -LEAD_LENGTH - label_room(mode_count) / 2
    return [
        (x, wire_y(mode, mode_count), mode, (str(mode + 1), _input_state(mode in flow.input_modes, source), hint))
        for mode in range(mode_count)
    ]


def _input_state(is_lit: bool, source: LightSource) -> str:
    if source == LightSource.LASER:
        return "Svítí sem laser." if is_lit else "Sem nic nesvítí."
    return "Sem vstupuje jeden foton." if is_lit else "Prázdný vstup, žádný foton."


def _detector_spots(flow: LightFlow, mode_count: int, source: LightSource) -> List[HoverSpot]:
    x = chip_end(mode_count) + LEAD_LENGTH + label_room(mode_count) / 2
    return [
        (x, wire_y(mode, mode_count), mode, (str(mode + 1), detected_label(flow.detected[mode], source)))
        for mode in range(mode_count)
    ]


def _waveguide_spots(chip: Chip, flow: LightFlow, source: LightSource) -> List[HoverSpot]:
    """On the input and output leads and wherever a waveguide passes a column without an MZI."""
    spots: List[HoverSpot] = []
    end = chip_end(chip.mode_count)
    for mode in range(chip.mode_count):
        y = wire_y(mode, chip.mode_count)
        spots.append((-LEAD_LENGTH / 2, y, mode, _waveguide_values(mode, flow.columns[0][mode], source)))
        spots.append((end + LEAD_LENGTH / 2, y, mode, _waveguide_values(mode, flow.detected[mode], source)))
    for column in range(chip.mode_count):
        for mode in modes_outside_mzis(chip, column):
            spots.append((
                column_x(column, 0.5), wire_y(mode, chip.mode_count), mode,
                _waveguide_values(mode, flow.columns[column][mode], source),
            ))
    return spots


def _waveguide_values(mode: int, light: float, source: LightSource) -> Tuple[str, ...]:
    if source == LightSource.LASER:
        return str(mode + 1), f"Teče tudy {czech_percent(light)} světla."
    return str(mode + 1), f"Teče tudy průměrně {detected_label(light, source)} fotonu."


def _shifter_spots(chip: Chip, phases: MeshPhases, hint: str) -> Tuple[List[HoverSpot], List[HoverSpot]]:
    external: List[HoverSpot] = []
    internal: List[HoverSpot] = []
    for index, slot in enumerate(chip.slots):
        upper_y = wire_y(slot.upper_mode, chip.mode_count)
        number = str(index + 1)
        external.append((
            column_x(slot.column, EXTERNAL_SHIFTER_AT), upper_y, index,
            (number, czech_phase(phases.external[index]), hint),
        ))
        internal.append((
            column_x(slot.column, INTERNAL_SHIFTER_AT), upper_y, index,
            (number, czech_phase(phases.internal[index]), hint),
        ))
    return external, internal


def _coupler_spots(chip: Chip) -> List[HoverSpot]:
    spots: List[HoverSpot] = []
    for index, (slot, ratios) in enumerate(zip(chip.slots, split_ratios(chip))):
        y = (wire_y(slot.upper_mode, chip.mode_count) + wire_y(slot.lower_mode, chip.mode_count)) / 2
        for order, (center, ratio) in enumerate(zip((FIRST_COUPLER_CENTER, SECOND_COUPLER_CENTER), ratios), start=1):
            spots.append((column_x(slot.column, center), y, index, (str(index + 1), str(order), czech_percent(ratio))))
    return spots


def _mzi_spots(chip: Chip, phases: MeshPhases, hint: str) -> List[HoverSpot]:
    spots: List[HoverSpot] = []
    for index, slot in enumerate(chip.slots):
        internal, external = phases.internal[index], phases.external[index]
        cross_share = abs(mzi_matrix(internal, external, chip.split_angles[index])[1, 0]) ** 2
        spots.append((
            column_x(slot.column, INTERNAL_SHIFTER_AT), wire_y(slot.upper_mode, chip.mode_count) - 0.5, index,
            (str(index + 1), str(slot.upper_mode + 1), str(slot.lower_mode + 1), czech_phase(internal),
             czech_phase(external), czech_percent(cross_share), hint),
        ))
    return spots


def detected_label(detected: float, source: LightSource) -> str:
    if source == LightSource.LASER:
        return czech_percent(detected)
    return f"{detected:.2f}".replace(".", ",")


def czech_phase(value: float) -> str:
    return f"{value:.2f}".replace(".", ",")


def czech_percent(share: float) -> str:
    return f"{100 * share:.1f} %".replace(".", ",")
