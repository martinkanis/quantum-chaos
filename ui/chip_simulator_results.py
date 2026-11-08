"""Readout of the chip simulator: how well the chip matches the target and both transfer maps side by side."""

from __future__ import annotations

from typing import Sequence

import numpy as np
from dash import html

from gbs.chip_parts import czech_percent
from gbs.chip_programming import ChipReadout
from ui.chip_simulator_content import DEVIATION_HINT, MATCH_HINT, MATRIX_HINT
from ui.components import metric_tile

CELL_RGB = "42, 111, 219"
DARK_CELL_SHARE = 0.55
"""Cells with at least this share of light get white text on the dark blue."""


def build_chip_readout(readout: ChipReadout) -> html.Div:
    input_modes = readout.flow.input_modes
    return html.Div(children=[
        html.Div(className="chip-readout-row", children=[
            html.Div(className="chip-metrics", children=[
                metric_tile("Shoda s cílem", czech_percent(readout.match), MATCH_HINT),
                metric_tile("Největší odchylka", _percentage_points(readout.largest_deviation), DEVIATION_HINT),
            ]),
            _transfer_table("Cíl |V_ij|²", readout.target_transmission, input_modes),
            _transfer_table("Čip |U_ij|²", readout.chip_transmission, input_modes),
        ]),
        html.P(MATRIX_HINT, className="hint small"),
    ])


def _transfer_table(title: str, shares: np.ndarray, input_modes: Sequence[int]) -> html.Table:
    mode_count = shares.shape[0]
    header = html.Tr([html.Th("výstup \\ vstup")] + [
        html.Th(str(column + 1), className=_laser_class(column, input_modes)) for column in range(mode_count)
    ])
    rows = [
        html.Tr([html.Th(str(row + 1))] + [
            _cell(float(shares[row, column]), _laser_class(column, input_modes)) for column in range(mode_count)
        ])
        for row in range(mode_count)
    ]
    return html.Table(className="chip-matrix", children=[html.Caption(title), html.Thead(header), html.Tbody(rows)])


def _cell(share: float, class_name: str) -> html.Td:
    return html.Td(
        f"{share:.2f}".replace(".", ","),
        className=class_name,
        style={
            "backgroundColor": f"rgba({CELL_RGB}, {0.85 * share:.3f})",
            "color": "#ffffff" if share >= DARK_CELL_SHARE else "inherit",
        },
    )


def _laser_class(column: int, input_modes: Sequence[int]) -> str:
    return "laser-column" if column in input_modes else ""


def _percentage_points(share: float) -> str:
    return f"{100 * share:.1f} p. b.".replace(".", ",", 1)
