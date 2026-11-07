"""Drawing of the photonic chip: waveguides, Mach–Zehnder interferometers and the light flowing through them."""

from __future__ import annotations

from collections import defaultdict
from enum import Enum
from typing import Any, Dict, List, NamedTuple, Optional, Sequence, Tuple

import plotly.graph_objects as go

from gbs.chip_hover_texts import (
    COUPLER_HOVER,
    EXTERNAL_SHIFTER_HOVER,
    INPUT_HOVER,
    INTERNAL_SHIFTER_HOVER,
    LASER_DETECTOR_HOVER,
    MZI_HOVER,
    PHOTON_DETECTOR_HOVER,
    WAVEGUIDE_HOVER,
)
from gbs.photonic_chip import Chip, LightFlow, MeshPhases, MziSlot, estimated_transit_seconds, mzi_matrix, split_ratios

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
"""The values of the phases are written next to the shifters only on small chips, elsewhere they would not fit."""
MAX_SHIFTER_MODES = 8
"""Larger chips are drawn without phase shifters, which would no longer fit."""
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
HOVER_MARKER_SIZE = 24
HOVER_LABEL = dict(bgcolor="#16213a", bordercolor=CHIP_BORDER, font=dict(color="#e8eef8", size=12), align="left")


class LightSource(str, Enum):
    LASER = "laser"
    PHOTONS = "fotony"
    """One photon in each input; the detectors show the mean number of photons."""


def chip_figure(chip: Chip, phases: MeshPhases, flow: LightFlow, source: LightSource = LightSource.LASER) -> go.Figure:
    figure = go.Figure()
    _add_chip_outline(figure, chip.mode_count)
    pieces = _lead_pieces(flow, chip.mode_count) + _mesh_pieces(chip, flow)
    waveguide_shape = _add_waveguides(figure, pieces)
    light_shapes = _add_light(figure, pieces)
    if chip.mode_count <= MAX_SHIFTER_MODES:
        for index, slot in enumerate(chip.slots):
            _add_mzi_labels(figure, slot, index, phases, chip.mode_count)
    _add_part_hovers(figure, chip, phases, flow, source)
    _add_port_labels(figure, flow, chip.mode_count, source)
    figure.update_layout(
        height=figure_height(chip.mode_count),
        margin=dict(t=10, b=10, l=10, r=10),
        paper_bgcolor=CHIP_BACKGROUND,
        plot_bgcolor=CHIP_BACKGROUND,
        showlegend=False,
        dragmode=False,
        hoverlabel=HOVER_LABEL,
        xaxis=dict(
            visible=False, fixedrange=True,
            range=[-LEAD_LENGTH - _label_room(chip.mode_count),
                   _chip_end(chip.mode_count) + LEAD_LENGTH + _label_room(chip.mode_count)],
        ),
        yaxis=dict(visible=False, fixedrange=True, range=[-0.6, chip.mode_count - 0.4]),
        meta={"lightAnimation": _light_animation(chip.mode_count, pieces, waveguide_shape, light_shapes)},
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


class Segment(NamedTuple):
    """A stretch of waveguide, straight when both ends are equally high, otherwise an S-bend."""
    start_x: float
    end_x: float
    start_y: float
    end_y: float


Piece = Tuple[Tuple[Segment, ...], float]
"""Segments of a piece of waveguide, left to right, and the light on it."""


def _lead_pieces(flow: LightFlow, mode_count: int) -> List[Piece]:
    end = _chip_end(mode_count)
    pieces: List[Piece] = []
    for mode in range(mode_count):
        y = _wire_y(mode, mode_count)
        pieces.append(((Segment(-LEAD_LENGTH, 0.0, y, y),), flow.columns[0][mode]))
        pieces.append(((Segment(end, end + LEAD_LENGTH, y, y),), flow.detected[mode]))
    return pieces


def _mesh_pieces(chip: Chip, flow: LightFlow) -> List[Piece]:
    pieces: List[Piece] = []
    for column in range(chip.mode_count):
        for index, slot in enumerate(chip.slots):
            if slot.column == column:
                pieces.extend(_mzi_pieces(chip, flow, index))
        for mode in _modes_outside_mzis(chip, column):
            y = _wire_y(mode, chip.mode_count)
            pieces.append(((Segment(_x(column, 0), _x(column, 1), y, y),), flow.columns[column][mode]))
    return pieces


def _modes_outside_mzis(chip: Chip, column: int) -> List[int]:
    """Waveguides that pass the column straight, at the edge of the mesh."""
    in_mzis = {mode for slot in chip.slots if slot.column == column for mode in (slot.upper_mode, slot.lower_mode)}
    return sorted(set(range(chip.mode_count)) - in_mzis)


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


def _mzi_waveguide(
    column: int, arm_y: float, coupled_y: float,
) -> Tuple[Tuple[Segment, ...], Tuple[Segment, ...], Tuple[Segment, ...]]:
    """One waveguide of an MZI, split at the centres of the two couplers where the light mixes."""
    entering = _route(column, (
        (0.0, arm_y), (FIRST_BEND[0], arm_y), (FIRST_BEND[1], coupled_y), (FIRST_COUPLER_CENTER, coupled_y),
    ))
    inside = _route(column, (
        (FIRST_COUPLER_CENTER, coupled_y), (SECOND_BEND_FROM_FIRST[0], coupled_y), (SECOND_BEND_FROM_FIRST[1], arm_y),
        (SECOND_BEND[0], arm_y), (SECOND_BEND[1], coupled_y), (SECOND_COUPLER_CENTER, coupled_y),
    ))
    leaving = _route(column, (
        (SECOND_COUPLER_CENTER, coupled_y), (LAST_BEND[0], coupled_y), (LAST_BEND[1], arm_y), (1.0, arm_y),
    ))
    return entering, inside, leaving


def _route(column: int, waypoints: Sequence[Tuple[float, float]]) -> Tuple[Segment, ...]:
    """Segments between waypoints given as (fraction of the column width, height)."""
    points = [(_x(column, fraction), y) for fraction, y in waypoints]
    return tuple(
        Segment(start_x, end_x, start_y, end_y)
        for (start_x, start_y), (end_x, end_y) in zip(points, points[1:])
    )


def _svg_path(segments: Sequence[Segment]) -> str:
    """An S-bend is a cubic Bézier with horizontal tangents at both ends; assets/chip_animation.js follows the same
    curve."""
    commands = [f"M {segments[0].start_x},{segments[0].start_y}"]
    for segment in segments:
        if segment.start_y == segment.end_y:
            commands.append(f"H {segment.end_x}")
        else:
            middle = round((segment.start_x + segment.end_x) / 2, COORDINATE_DECIMALS)
            commands.append(
                f"C {middle},{segment.start_y} {middle},{segment.end_y} {segment.end_x},{segment.end_y}"
            )
    return " ".join(commands)


def _add_waveguides(figure: go.Figure, pieces: List[Piece]) -> int:
    """Dark waveguides under the light; returns the index of their shape."""
    figure.add_shape(
        type="path", path=" ".join(_svg_path(segments) for segments, _ in pieces),
        line=dict(color=WAVEGUIDE_COLOR, width=2),
    )
    return len(figure.layout.shapes) - 1


def _add_light(figure: go.Figure, pieces: List[Piece]) -> List[int]:
    """Light glows over the waveguides, wider and brighter the more of it there is; returns the indices of its
    shapes, which the animation reveals from left to right."""
    first_shape = len(figure.layout.shapes)
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
    return list(range(first_shape, len(figure.layout.shapes)))


def _paths_by_light_level(pieces: List[Piece]) -> Dict[int, List[str]]:
    levels: Dict[int, List[str]] = defaultdict(list)
    for segments, intensity in _lit_pieces(pieces):
        levels[max(1, round(_light_strength(intensity) * LIGHT_LEVELS))].append(_svg_path(segments))
    return levels


def _lit_pieces(pieces: List[Piece]) -> List[Piece]:
    return [(segments, intensity) for segments, intensity in pieces if intensity >= LIGHT_THRESHOLD]


def _light_strength(intensity: float) -> float:
    """More than one photon on average in a waveguide glows like one."""
    return min(intensity, 1.0)


def _light_animation(
    mode_count: int, pieces: List[Piece], waveguide_shape: int, light_shapes: List[int],
) -> Dict[str, Any]:
    """What assets/chip_animation.js needs to send the light through the chip: which shapes to reveal, where the
    light starts and ends, how long real light takes (our estimate), and each lit piece of waveguide as
    [light, x0, x1, y0, y1, x0, x1, y0, y1, ...]."""
    return {
        "transitSeconds": estimated_transit_seconds(mode_count),
        "waveguideShape": waveguide_shape,
        "lightShapes": light_shapes,
        "start": -LEAD_LENGTH,
        "end": _chip_end(mode_count) + LEAD_LENGTH,
        "top": _wire_y(0, mode_count),
        "lanes": [
            [
                round(_light_strength(intensity), COORDINATE_DECIMALS),
                *(value for segment in segments for value in segment),
            ]
            for segments, intensity in _lit_pieces(pieces)
        ],
    }


def _add_mzi_labels(figure: go.Figure, slot: MziSlot, index: int, phases: MeshPhases, mode_count: int) -> None:
    upper_y = _wire_y(slot.upper_mode, mode_count)
    shows_values = mode_count <= MAX_LABELLED_MODES
    _add_shifter(
        figure, _x(slot.column, INTERNAL_SHIFTER_AT), upper_y,
        f"θ{index + 1} {czech_phase(phases.internal[index])}" if shows_values else None, INTERNAL_SHIFTER_COLOR,
    )
    _add_shifter(
        figure, _x(slot.column, EXTERNAL_SHIFTER_AT), upper_y,
        f"φ{index + 1} {czech_phase(phases.external[index])}" if shows_values else None, EXTERNAL_SHIFTER_COLOR,
    )
    figure.add_annotation(
        x=_x(slot.column, INTERNAL_SHIFTER_AT), y=upper_y - 0.5, text=f"MZI {index + 1}", showarrow=False,
        font=dict(color=LABEL_COLOR, size=10),
    )


def _add_shifter(figure: go.Figure, x: float, y: float, label: Optional[str], color: str) -> None:
    """Phase shifter on the upper waveguide, where the waveguide never bends, with its value above it if given."""
    width, height = SHIFTER_SIZE
    figure.add_shape(
        type="rect", x0=x - width / 2, x1=x + width / 2, y0=y - height / 2, y1=y + height / 2,
        line=dict(color=color, width=1.5), fillcolor="rgba(11, 18, 32, 0.6)",
    )
    if label is None:
        return
    figure.add_annotation(
        x=x, y=y + LABEL_OFFSET, text=label, showarrow=False,
        font=dict(color=color, size=10),
    )


HoverSpot = Tuple[float, float, Tuple[str, ...]]
"""Position of an invisible hover target and the values its description template reads from customdata."""


def _add_part_hovers(figure: go.Figure, chip: Chip, phases: MeshPhases, flow: LightFlow, source: LightSource) -> None:
    """Every part of the chip describes itself on hover: inputs, waveguides, phase shifters, couplers, MZIs and
    detectors. Shared text sits in the template once per kind of part, so even large chips stay small."""
    _add_hover_trace(figure, _input_spots(flow, chip.mode_count, source), INPUT_HOVER)
    _add_hover_trace(figure, _waveguide_spots(chip, flow, source), WAVEGUIDE_HOVER)
    if chip.mode_count <= MAX_SHIFTER_MODES:
        external, internal = _shifter_spots(chip, phases)
        _add_hover_trace(figure, external, EXTERNAL_SHIFTER_HOVER)
        _add_hover_trace(figure, internal, INTERNAL_SHIFTER_HOVER)
    _add_hover_trace(figure, _coupler_spots(chip), COUPLER_HOVER)
    _add_hover_trace(figure, _mzi_spots(chip, phases), MZI_HOVER)
    detector_hover = LASER_DETECTOR_HOVER if source == LightSource.LASER else PHOTON_DETECTOR_HOVER
    _add_hover_trace(figure, _detector_spots(flow, chip.mode_count, source), detector_hover)


def _add_hover_trace(figure: go.Figure, spots: List[HoverSpot], template: str) -> None:
    xs, ys, values = zip(*spots)
    figure.add_trace(go.Scatter(
        x=xs, y=ys, customdata=values, hovertemplate=template + "<extra></extra>", mode="markers",
        marker=dict(size=HOVER_MARKER_SIZE, color="rgba(0, 0, 0, 0)"),
    ))


def _input_spots(flow: LightFlow, mode_count: int, source: LightSource) -> List[HoverSpot]:
    x = -LEAD_LENGTH - _label_room(mode_count) / 2
    return [
        (x, _wire_y(mode, mode_count), (str(mode + 1), _input_state(mode in flow.input_modes, source)))
        for mode in range(mode_count)
    ]


def _input_state(is_lit: bool, source: LightSource) -> str:
    if source == LightSource.LASER:
        return "Svítí sem laser." if is_lit else "Sem nic nesvítí."
    return "Sem vstupuje jeden foton." if is_lit else "Prázdný vstup, žádný foton."


def _detector_spots(flow: LightFlow, mode_count: int, source: LightSource) -> List[HoverSpot]:
    x = _chip_end(mode_count) + LEAD_LENGTH + _label_room(mode_count) / 2
    return [
        (x, _wire_y(mode, mode_count), (str(mode + 1), _detected_label(flow.detected[mode], source)))
        for mode in range(mode_count)
    ]


def _waveguide_spots(chip: Chip, flow: LightFlow, source: LightSource) -> List[HoverSpot]:
    """On the input and output leads and wherever a waveguide passes a column without an MZI."""
    spots: List[HoverSpot] = []
    end = _chip_end(chip.mode_count)
    for mode in range(chip.mode_count):
        y = _wire_y(mode, chip.mode_count)
        spots.append((-LEAD_LENGTH / 2, y, _waveguide_values(mode, flow.columns[0][mode], source)))
        spots.append((end + LEAD_LENGTH / 2, y, _waveguide_values(mode, flow.detected[mode], source)))
    for column in range(chip.mode_count):
        for mode in _modes_outside_mzis(chip, column):
            spots.append((
                _x(column, 0.5), _wire_y(mode, chip.mode_count),
                _waveguide_values(mode, flow.columns[column][mode], source),
            ))
    return spots


def _waveguide_values(mode: int, light: float, source: LightSource) -> Tuple[str, ...]:
    if source == LightSource.LASER:
        return str(mode + 1), f"Teče tudy {czech_percent(light)} světla."
    return str(mode + 1), f"Teče tudy průměrně {_detected_label(light, source)} fotonu."


def _shifter_spots(chip: Chip, phases: MeshPhases) -> Tuple[List[HoverSpot], List[HoverSpot]]:
    external: List[HoverSpot] = []
    internal: List[HoverSpot] = []
    for index, slot in enumerate(chip.slots):
        upper_y = _wire_y(slot.upper_mode, chip.mode_count)
        number = str(index + 1)
        external.append((
            _x(slot.column, EXTERNAL_SHIFTER_AT), upper_y, (number, czech_phase(phases.external[index])),
        ))
        internal.append((
            _x(slot.column, INTERNAL_SHIFTER_AT), upper_y, (number, czech_phase(phases.internal[index])),
        ))
    return external, internal


def _coupler_spots(chip: Chip) -> List[HoverSpot]:
    spots: List[HoverSpot] = []
    for index, (slot, ratios) in enumerate(zip(chip.slots, split_ratios(chip))):
        y = (_wire_y(slot.upper_mode, chip.mode_count) + _wire_y(slot.lower_mode, chip.mode_count)) / 2
        for order, (center, ratio) in enumerate(zip((FIRST_COUPLER_CENTER, SECOND_COUPLER_CENTER), ratios), start=1):
            spots.append((_x(slot.column, center), y, (str(index + 1), str(order), czech_percent(ratio))))
    return spots


def _mzi_spots(chip: Chip, phases: MeshPhases) -> List[HoverSpot]:
    spots: List[HoverSpot] = []
    for index, slot in enumerate(chip.slots):
        internal, external = phases.internal[index], phases.external[index]
        cross_share = abs(mzi_matrix(internal, external, chip.split_angles[index])[1, 0]) ** 2
        spots.append((
            _x(slot.column, INTERNAL_SHIFTER_AT), _wire_y(slot.upper_mode, chip.mode_count) - 0.5,
            (str(index + 1), str(slot.upper_mode + 1), str(slot.lower_mode + 1), czech_phase(internal),
             czech_phase(external), czech_percent(cross_share)),
        ))
    return spots


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
