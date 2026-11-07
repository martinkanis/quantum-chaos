"""Drawing of the photonic chip: waveguides, Mach–Zehnder interferometers and the light flowing through them."""

from __future__ import annotations

from collections import defaultdict
from enum import Enum
from typing import Dict, List, Tuple

import plotly.graph_objects as go

from gbs.photonic_chip import Chip, LightFlow, MeshPhases, MziSlot, mzi_matrix

COLUMN_WIDTH = 1.6
LEAD_LENGTH = 0.5
COUPLER_GAP = 0.07
"""Half the distance of the two waveguides inside a directional coupler (the mode spacing is 1)."""
EXTERNAL_SHIFTER_AT = 0.07
FIRST_BEND = (0.14, 0.24)
FIRST_COUPLER_CENTER = 0.30
SECOND_BEND_FROM_FIRST = (0.36, 0.46)
INTERNAL_SHIFTER_AT = 0.50
SECOND_BEND = (0.54, 0.64)
SECOND_COUPLER_CENTER = 0.70
LAST_BEND = (0.76, 0.86)
"""Positions along one column as fractions of its width: φ, coupler, arms with θ, coupler, way out."""
SHIFTER_SIZE = (0.11, 0.18)
LABEL_OFFSET = 0.24
PORT_LABEL_ROOM = 1.0
PORT_LABEL_ROOM_PER_COLUMN = 0.16
"""Room left and right of the chip for the input labels and the detected shares; wide chips are drawn smaller, so
their labels need more of the axis."""
LIGHT_THRESHOLD = 1e-3
LIGHT_LEVELS = 20
"""Waveguides with similar light share one shape, so even 120 MZIs stay a few dozen shapes."""
MAX_LABELLED_MODES = 4
"""Larger chips are drawn without phase shifters and labels, which would no longer fit."""
COMPACT_ROW_HEIGHT = 40
COORDINATE_DECIMALS = 3

CHIP_BACKGROUND = "#0b1220"
CHIP_BORDER = "#25324a"
WAVEGUIDE_COLOR = "#2f3d57"
LABEL_COLOR = "#9fb0c8"
LIGHT_RGB = "80, 220, 255"
LIGHT_CORE_RGB = "215, 250, 255"
LASER_COLOR = "#ff4d8d"
INTERNAL_SHIFTER_COLOR = "#b794f6"
EXTERNAL_SHIFTER_COLOR = "#f6ad55"
FIGURE_HEIGHT = 380


class LightSource(str, Enum):
    LASER = "laser"
    PHOTONS = "fotony"
    """One photon in each input; the detectors show the mean number of photons."""


def chip_figure(chip: Chip, phases: MeshPhases, flow: LightFlow, source: LightSource = LightSource.LASER) -> go.Figure:
    figure = go.Figure()
    _add_chip_outline(figure, chip.mode_count)
    _add_light(figure, _lead_pieces(flow, chip.mode_count) + _mesh_pieces(chip, flow))
    if chip.mode_count <= MAX_LABELLED_MODES:
        for index, slot in enumerate(chip.slots):
            _add_mzi_labels(figure, slot, index, phases, chip.mode_count)
    _add_hover_points(figure, chip, phases)
    _add_port_labels(figure, flow, chip.mode_count, source)
    figure.update_layout(
        height=figure_height(chip.mode_count),
        margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor=CHIP_BACKGROUND,
        plot_bgcolor=CHIP_BACKGROUND,
        showlegend=False,
        dragmode=False,
        xaxis=dict(
            visible=False, fixedrange=True,
            range=[-LEAD_LENGTH - _label_room(chip.mode_count),
                   _chip_end(chip.mode_count) + LEAD_LENGTH + _label_room(chip.mode_count)],
        ),
        yaxis=dict(visible=False, fixedrange=True, range=[-0.6, chip.mode_count - 0.4]),
    )
    return figure


def empty_chip_figure() -> go.Figure:
    """Dark placeholder of the right height until the chip is first drawn, so the page does not flash white."""
    figure = go.Figure()
    figure.update_layout(
        height=FIGURE_HEIGHT, margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor=CHIP_BACKGROUND,
        plot_bgcolor=CHIP_BACKGROUND, xaxis=dict(visible=False), yaxis=dict(visible=False),
    )
    return figure


def _label_room(mode_count: int) -> float:
    return max(PORT_LABEL_ROOM, PORT_LABEL_ROOM_PER_COLUMN * mode_count)


def figure_height(mode_count: int) -> int:
    return max(FIGURE_HEIGHT, COMPACT_ROW_HEIGHT * mode_count + 60)


def _wire_y(mode: int, mode_count: int) -> float:
    """Waveguide 1 on top."""
    return float(mode_count - 1 - mode)


def _x(column: int, fraction: float) -> float:
    """Rounded, because the coordinates end up as text in SVG paths sent to the browser."""
    return round((column + fraction) * COLUMN_WIDTH, COORDINATE_DECIMALS)


def _chip_end(mode_count: int) -> float:
    return mode_count * COLUMN_WIDTH


def _add_chip_outline(figure: go.Figure, mode_count: int) -> None:
    figure.add_shape(
        type="rect", x0=-0.25, x1=_chip_end(mode_count) + 0.25, y0=-0.45, y1=mode_count - 0.55,
        line=dict(color=CHIP_BORDER, width=1), fillcolor="rgba(255, 255, 255, 0.015)",
    )


Piece = Tuple[str, float]
"""SVG path of a piece of waveguide and the light on it."""


def _lead_pieces(flow: LightFlow, mode_count: int) -> List[Piece]:
    end = _chip_end(mode_count)
    pieces: List[Piece] = []
    for mode in range(mode_count):
        y = _wire_y(mode, mode_count)
        pieces.append((f"M {-LEAD_LENGTH},{y} H 0", flow.columns[0][mode]))
        pieces.append((f"M {end},{y} H {end + LEAD_LENGTH}", flow.detected[mode]))
    return pieces


def _mesh_pieces(chip: Chip, flow: LightFlow) -> List[Piece]:
    pieces: List[Piece] = []
    for column in range(chip.mode_count):
        modes_in_mzis = set()
        for index, slot in enumerate(chip.slots):
            if slot.column == column:
                pieces.extend(_mzi_pieces(chip, flow, index))
                modes_in_mzis.update((slot.upper_mode, slot.lower_mode))
        for mode in sorted(set(range(chip.mode_count)) - modes_in_mzis):
            y = _wire_y(mode, chip.mode_count)
            pieces.append((f"M {_x(column, 0)},{y} H {_x(column, 1)}", flow.columns[column][mode]))
    return pieces


def _mzi_pieces(chip: Chip, flow: LightFlow, index: int) -> List[Piece]:
    slot = chip.slots[index]
    light = flow.mzis[index]
    pieces: List[Piece] = []
    for side, mode in enumerate((slot.upper_mode, slot.lower_mode)):
        paths = _mzi_waveguide(slot.column, _wire_y(mode, chip.mode_count), _coupled_y(slot, side, chip.mode_count))
        pieces.extend(zip(paths, (light.entering[side], light.inside[side], light.leaving[side])))
    return pieces


def _coupled_y(slot: MziSlot, side: int, mode_count: int) -> float:
    middle = (_wire_y(slot.upper_mode, mode_count) + _wire_y(slot.lower_mode, mode_count)) / 2
    return round(middle + COUPLER_GAP if side == 0 else middle - COUPLER_GAP, COORDINATE_DECIMALS)


def _mzi_waveguide(column: int, arm_y: float, coupled_y: float) -> Tuple[str, str, str]:
    """SVG paths of one waveguide of an MZI, split at the centres of the two couplers where the light mixes."""
    def x(fraction: float) -> float:
        return _x(column, fraction)

    def bend(start: float, end: float, from_y: float, to_y: float) -> str:
        middle = round((x(start) + x(end)) / 2, COORDINATE_DECIMALS)
        return f"C {middle},{from_y} {middle},{to_y} {x(end)},{to_y}"

    entering = (
        f"M {x(0)},{arm_y} H {x(FIRST_BEND[0])} {bend(*FIRST_BEND, arm_y, coupled_y)} H {x(FIRST_COUPLER_CENTER)}"
    )
    inside = (
        f"M {x(FIRST_COUPLER_CENTER)},{coupled_y} H {x(SECOND_BEND_FROM_FIRST[0])} "
        f"{bend(*SECOND_BEND_FROM_FIRST, coupled_y, arm_y)} H {x(SECOND_BEND[0])} "
        f"{bend(*SECOND_BEND, arm_y, coupled_y)} H {x(SECOND_COUPLER_CENTER)}"
    )
    leaving = (
        f"M {x(SECOND_COUPLER_CENTER)},{coupled_y} H {x(LAST_BEND[0])} {bend(*LAST_BEND, coupled_y, arm_y)} H {x(1)}"
    )
    return entering, inside, leaving


def _add_light(figure: go.Figure, pieces: List[Piece]) -> None:
    """Dark waveguides; light glows over them, wider and brighter the more of it there is (at most 1)."""
    figure.add_shape(type="path", path=" ".join(path for path, _ in pieces), line=dict(color=WAVEGUIDE_COLOR, width=2))
    for level, paths in sorted(_paths_by_light_level(pieces).items()):
        intensity = level / LIGHT_LEVELS
        joined = " ".join(paths)
        figure.add_shape(
            type="path", path=joined,
            line=dict(color=f"rgba({LIGHT_RGB}, {0.12 + 0.3 * intensity:.3f})", width=3 + 12 * intensity),
        )
        figure.add_shape(
            type="path", path=joined,
            line=dict(color=f"rgba({LIGHT_CORE_RGB}, {0.25 + 0.75 * intensity:.3f})", width=1.2 + 2 * intensity),
        )


def _paths_by_light_level(pieces: List[Piece]) -> Dict[int, List[str]]:
    levels: Dict[int, List[str]] = defaultdict(list)
    for path, intensity in pieces:
        if intensity >= LIGHT_THRESHOLD:
            levels[max(1, round(min(intensity, 1.0) * LIGHT_LEVELS))].append(path)
    return levels


def _add_mzi_labels(figure: go.Figure, slot: MziSlot, index: int, phases: MeshPhases, mode_count: int) -> None:
    upper_y = _wire_y(slot.upper_mode, mode_count)
    _add_shifter(
        figure, _x(slot.column, INTERNAL_SHIFTER_AT), upper_y, f"θ{index + 1} {czech_phase(phases.internal[index])}",
        INTERNAL_SHIFTER_COLOR,
    )
    _add_shifter(
        figure, _x(slot.column, EXTERNAL_SHIFTER_AT), upper_y, f"φ{index + 1} {czech_phase(phases.external[index])}",
        EXTERNAL_SHIFTER_COLOR,
    )
    figure.add_annotation(
        x=_x(slot.column, INTERNAL_SHIFTER_AT), y=upper_y - 0.5, text=f"MZI {index + 1}", showarrow=False,
        font=dict(color=LABEL_COLOR, size=10),
    )


def _add_shifter(figure: go.Figure, x: float, y: float, label: str, color: str) -> None:
    """Phase shifter on the upper waveguide with its value above it, where the waveguide never bends."""
    width, height = SHIFTER_SIZE
    figure.add_shape(
        type="rect", x0=x - width / 2, x1=x + width / 2, y0=y - height / 2, y1=y + height / 2,
        line=dict(color=color, width=1.5), fillcolor="rgba(11, 18, 32, 0.6)",
    )
    figure.add_annotation(
        x=x, y=y + LABEL_OFFSET, text=label, showarrow=False,
        font=dict(color=color, size=10),
    )


def _add_hover_points(figure: go.Figure, chip: Chip, phases: MeshPhases) -> None:
    texts: List[str] = []
    xs: List[float] = []
    ys: List[float] = []
    for index, slot in enumerate(chip.slots):
        internal, external = phases.internal[index], phases.external[index]
        cross_share = abs(mzi_matrix(internal, external, chip.split_angles[index])[1, 0]) ** 2
        texts.append(
            f"MZI {index + 1}: světlovody {slot.upper_mode + 1} a {slot.lower_mode + 1}<br>"
            f"θ = {czech_phase(internal)} rad, φ = {czech_phase(external)} rad<br>"
            f"ze světlovodu {slot.upper_mode + 1} přejde vedle {czech_percent(cross_share)} světla"
        )
        xs.append(_x(slot.column, INTERNAL_SHIFTER_AT))
        ys.append(_wire_y(slot.upper_mode, chip.mode_count) - 0.5)
    figure.add_trace(go.Scatter(
        x=xs, y=ys, mode="markers", marker=dict(size=28, color="rgba(0, 0, 0, 0)"),
        hovertext=texts, hoverinfo="text",
    ))


def _add_port_labels(figure: go.Figure, flow: LightFlow, mode_count: int, source: LightSource) -> None:
    end = _chip_end(mode_count) + LEAD_LENGTH
    for mode in range(mode_count):
        y = _wire_y(mode, mode_count)
        is_lit = mode in flow.input_modes
        figure.add_annotation(
            x=-LEAD_LENGTH - 0.08, y=y, xanchor="right", showarrow=False,
            text=f"<b>{source.value if source == LightSource.LASER else 'foton'} ▸ {mode + 1}</b>" if is_lit
            else f"vstup {mode + 1}",
            font=dict(color=LASER_COLOR if is_lit else LABEL_COLOR, size=11),
        )
        detected = flow.detected[mode]
        figure.add_annotation(
            x=end + 0.08, y=y, xanchor="left", showarrow=False, text=f"<b>{_detected_label(detected, source)}</b>",
            font=dict(color=f"rgb({LIGHT_CORE_RGB})" if detected >= LIGHT_THRESHOLD else LABEL_COLOR, size=11),
        )
    figure.add_annotation(
        x=end + 0.08, y=mode_count - 0.5, xanchor="left", showarrow=False,
        text="detektory" if source == LightSource.LASER else "průměr fotonů", font=dict(color=LABEL_COLOR, size=10),
    )


def _detected_label(detected: float, source: LightSource) -> str:
    if source == LightSource.LASER:
        return czech_percent(detected)
    return f"{detected:.2f}".replace(".", ",")


def czech_phase(value: float) -> str:
    return f"{value:.2f}".replace(".", ",")


def czech_percent(share: float) -> str:
    return f"{100 * share:.1f} %".replace(".", ",")
