"""Drawing of the photonic chip: waveguides, Mach–Zehnder interferometers and the light flowing through them."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Dict, List, NamedTuple, Optional, Sequence, Tuple

import plotly.graph_objects as go

from gbs.bench import LightSource
from gbs.chip_geometry import (
    COORDINATE_DECIMALS,
    COUPLER_GAP,
    EXTERNAL_SHIFTER_AT,
    FIRST_BEND,
    FIRST_COUPLER_CENTER,
    INTERNAL_SHIFTER_AT,
    LAST_BEND,
    LEAD_LENGTH,
    MAX_SHIFTER_MODES,
    SECOND_BEND,
    SECOND_BEND_FROM_FIRST,
    SECOND_COUPLER_CENTER,
    chip_end,
    column_x,
    label_room,
    modes_outside_mzis,
    wire_y,
)
from gbs.chip_parts import ChipPart, SelectedShifter, add_part_hovers, czech_phase, detected_label
from gbs.photonic_chip import Chip, LightFlow, MeshPhases, MziSlot, estimated_transit_seconds

SHIFTER_SIZE = (0.11, 0.18)
LABEL_OFFSET = 0.24
LIGHT_THRESHOLD = 1e-3
LIGHT_LEVELS = 20
"""Waveguides with similar light share one shape, so even 120 MZIs stay a few dozen shapes."""
MAX_LABELLED_MODES = 4
"""The values of the phases are written next to the shifters only on small chips, elsewhere they would not fit."""
COMPACT_ROW_HEIGHT = 40

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
SELECTED_COLOR = "#ff4d8d"
SELECTED_FILL = "rgba(255, 77, 141, 0.28)"
HOVER_LABEL = dict(bgcolor="#16213a", bordercolor=CHIP_BORDER, font=dict(color="#e8eef8", size=12), align="left")


@dataclass(frozen=True)
class ChipInteraction:
    """The chip answers clicks (laboratory 1): hover texts say what a click does and the selected shifter glows."""
    selected: SelectedShifter


def chip_figure(
    chip: Chip, phases: MeshPhases, flow: LightFlow, source: LightSource = LightSource.LASER,
    interaction: Optional[ChipInteraction] = None,
) -> go.Figure:
    figure = go.Figure()
    _add_chip_outline(figure, chip.mode_count)
    pieces = _lead_pieces(flow, chip.mode_count) + _mesh_pieces(chip, flow)
    waveguide_shape = _add_waveguides(figure, pieces)
    light_shapes = _add_light(figure, pieces)
    if chip.mode_count <= MAX_SHIFTER_MODES:
        for index, slot in enumerate(chip.slots):
            _add_mzi_labels(figure, slot, index, phases, chip.mode_count)
    if interaction is not None:
        _add_selection(figure, chip, interaction.selected)
    add_part_hovers(figure, chip, phases, flow, source, is_clickable=interaction is not None)
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
            range=[-LEAD_LENGTH - label_room(chip.mode_count),
                   chip_end(chip.mode_count) + LEAD_LENGTH + label_room(chip.mode_count)],
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


def figure_height(mode_count: int) -> int:
    return max(FIGURE_HEIGHT, COMPACT_ROW_HEIGHT * mode_count + 60)


def _add_chip_outline(figure: go.Figure, mode_count: int) -> None:
    figure.add_shape(
        type="rect", x0=-0.25, x1=chip_end(mode_count) + 0.25, y0=-0.45, y1=mode_count - 0.55,
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
    end = chip_end(mode_count)
    pieces: List[Piece] = []
    for mode in range(mode_count):
        y = wire_y(mode, mode_count)
        pieces.append(((Segment(-LEAD_LENGTH, 0.0, y, y),), flow.columns[0][mode]))
        pieces.append(((Segment(end, end + LEAD_LENGTH, y, y),), flow.detected[mode]))
    return pieces


def _mesh_pieces(chip: Chip, flow: LightFlow) -> List[Piece]:
    pieces: List[Piece] = []
    for column in range(chip.mode_count):
        for index, slot in enumerate(chip.slots):
            if slot.column == column:
                pieces.extend(_mzi_pieces(chip, flow, index))
        for mode in modes_outside_mzis(chip, column):
            y = wire_y(mode, chip.mode_count)
            pieces.append(((Segment(column_x(column, 0), column_x(column, 1), y, y),), flow.columns[column][mode]))
    return pieces


def _mzi_pieces(chip: Chip, flow: LightFlow, index: int) -> List[Piece]:
    slot = chip.slots[index]
    light = flow.mzis[index]
    pieces: List[Piece] = []
    for side, mode in enumerate((slot.upper_mode, slot.lower_mode)):
        paths = _mzi_waveguide(slot.column, wire_y(mode, chip.mode_count), _coupled_y(slot, side, chip.mode_count))
        pieces.extend(zip(paths, (light.entering[side], light.inside[side], light.leaving[side])))
    return pieces


def _coupled_y(slot: MziSlot, side: int, mode_count: int) -> float:
    middle = (wire_y(slot.upper_mode, mode_count) + wire_y(slot.lower_mode, mode_count)) / 2
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
    points = [(column_x(column, fraction), y) for fraction, y in waypoints]
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
        "end": chip_end(mode_count) + LEAD_LENGTH,
        "top": wire_y(0, mode_count),
        "lanes": [
            [
                round(_light_strength(intensity), COORDINATE_DECIMALS),
                *(value for segment in segments for value in segment),
            ]
            for segments, intensity in _lit_pieces(pieces)
        ],
    }


def _add_mzi_labels(figure: go.Figure, slot: MziSlot, index: int, phases: MeshPhases, mode_count: int) -> None:
    upper_y = wire_y(slot.upper_mode, mode_count)
    shows_values = mode_count <= MAX_LABELLED_MODES
    _add_shifter(
        figure, column_x(slot.column, INTERNAL_SHIFTER_AT), upper_y,
        f"θ{index + 1} {czech_phase(phases.internal[index])}" if shows_values else None, INTERNAL_SHIFTER_COLOR,
    )
    _add_shifter(
        figure, column_x(slot.column, EXTERNAL_SHIFTER_AT), upper_y,
        f"φ{index + 1} {czech_phase(phases.external[index])}" if shows_values else None, EXTERNAL_SHIFTER_COLOR,
    )
    figure.add_annotation(
        x=column_x(slot.column, INTERNAL_SHIFTER_AT), y=upper_y - 0.5, text=f"MZI {index + 1}", showarrow=False,
        font=dict(color=LABEL_COLOR, size=10),
    )


def _add_selection(figure: go.Figure, chip: Chip, selected: SelectedShifter) -> None:
    """A glowing frame around the selected shifter, where the chip draws its shifters."""
    if chip.mode_count > MAX_SHIFTER_MODES or not 0 <= selected.mzi < len(chip.slots):
        return
    slot = chip.slots[selected.mzi]
    position = INTERNAL_SHIFTER_AT if selected.part == ChipPart.INTERNAL_SHIFTER else EXTERNAL_SHIFTER_AT
    x, y = column_x(slot.column, position), wire_y(slot.upper_mode, chip.mode_count)
    width, height = SHIFTER_SIZE
    figure.add_shape(
        type="rect", x0=x - width, x1=x + width, y0=y - height, y1=y + height,
        line=dict(color=SELECTED_COLOR, width=2.5), fillcolor=SELECTED_FILL,
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


def _add_port_labels(figure: go.Figure, flow: LightFlow, mode_count: int, source: LightSource) -> None:
    """All labels in one update: add_annotation revalidates every earlier annotation, O(N²) on large chips."""
    end = chip_end(mode_count) + LEAD_LENGTH
    labels: List[dict] = []
    for mode in range(mode_count):
        y = wire_y(mode, mode_count)
        is_lit = mode in flow.input_modes
        labels.append(dict(
            x=-LEAD_LENGTH - 0.08, y=y, xanchor="right", showarrow=False,
            text=f"<b>{source.value if source == LightSource.LASER else 'foton'} ▸ {mode + 1}</b>" if is_lit
            else f"vstup {mode + 1}",
            font=dict(color=LASER_COLOR if is_lit else LABEL_COLOR, size=11),
        ))
        detected = flow.detected[mode]
        labels.append(dict(
            x=end + 0.08, y=y, xanchor="left", showarrow=False, text=f"<b>{detected_label(detected, source)}</b>",
            font=dict(color=f"rgb({LIGHT_CORE_RGB})" if detected >= LIGHT_THRESHOLD else LABEL_COLOR, size=11),
        ))
    labels.append(dict(
        x=end + 0.08, y=mode_count - 0.5, xanchor="left", showarrow=False,
        text="detektory" if source == LightSource.LASER else "průměr fotonů", font=dict(color=LABEL_COLOR, size=10),
    ))
    figure.update_layout(annotations=[*figure.layout.annotations, *labels])
