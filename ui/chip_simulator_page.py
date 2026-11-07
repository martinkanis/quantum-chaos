"""Page of the photonic chip simulator: controls, the chip with the laser light, phase sliders and the explanation."""

from __future__ import annotations

from typing import List, Tuple

import numpy as np
from dash import dcc, html

from gbs.chip_charts import empty_chip_figure
from gbs.photonic_chip import MODE_COUNT, mesh_slots
from ui import ids
from ui.chip_simulator_content import (
    CHIP_OPTIONS,
    CHIP_SEEDS,
    DEFAULT_TARGET,
    IN_SHORT,
    LAB_ANCHOR,
    LAB_INTRO,
    LEAD,
    PHASES_HINT,
    SEED_HINT,
    SOURCES_ANCHOR,
    TARGET_LABELS,
    TITLE,
    TOPICS,
)
from ui.components import labelled
from ui.navigation import HIDDEN, chip_simulator_href
from ui.topic_sections import sources_section, table_of_contents, topic_section

PHASE_STEP = 0.0001
PHASE_MARKS = {0: "0", np.pi / 2: "π/2", np.pi: "π", 3 * np.pi / 2: "3π/2", 2 * np.pi: "2π"}
CHIP_FIGURE_MIN_WIDTH = "680px"
"""Narrower screens scroll the chip sideways instead of squeezing its labels into each other."""
DEFAULT_LASER_INPUT = 0
"""Index of the waveguide the laser shines into; the page counts waveguides from 1."""


def internal_phase_slider_ids() -> Tuple[str, ...]:
    return tuple(f"{ids.CHIP_INTERNAL_PHASE_SLIDER_PREFIX}{number}" for number in _mzi_numbers())


def external_phase_slider_ids() -> Tuple[str, ...]:
    return tuple(f"{ids.CHIP_EXTERNAL_PHASE_SLIDER_PREFIX}{number}" for number in _mzi_numbers())


def _mzi_numbers() -> range:
    return range(1, len(mesh_slots(MODE_COUNT)) + 1)


def build_chip_simulator_page() -> html.Div:
    return html.Div(
        id=ids.CHIP_SIMULATOR_PAGE,
        className="gbs-page",
        style=HIDDEN,
        children=[
            html.H1(TITLE),
            html.P(LEAD, className="lead"),
            html.Div(className="in-short", children=[html.Strong("V kostce: "), dcc.Markdown(IN_SHORT, mathjax=True)]),
            table_of_contents(TOPICS, chip_simulator_href, SOURCES_ANCHOR),
            _lab_section(),
            *[topic_section(number, topic) for number, topic in enumerate(TOPICS, start=1)],
            sources_section(TOPICS, SOURCES_ANCHOR),
        ],
    )


def _lab_section() -> html.Section:
    return html.Section(
        id=LAB_ANCHOR,
        className="card",
        children=[
            html.H2("Laboratoř: naprogramuj čip"),
            dcc.Markdown(LAB_INTRO, mathjax=True, link_target="_blank"),
            _controls(),
            html.Div(className="chip-buttons", children=[
                html.Button("Naprogramovat podle návrhu", id=ids.CHIP_PROGRAM_BUTTON, className="primary-button"),
                html.Button("Doladit na tomto čipu", id=ids.CHIP_CALIBRATE_BUTTON, className="secondary-button"),
                html.Button("Vynulovat fáze", id=ids.CHIP_RESET_BUTTON, className="secondary-button"),
            ]),
            html.Div(id=ids.CHIP_ERROR_MESSAGE, className="error-message"),
            html.Div(className="chip-figure", children=dcc.Graph(
                id=ids.CHIP_FIGURE, figure=empty_chip_figure(), style={"minWidth": CHIP_FIGURE_MIN_WIDTH},
                config={"displayModeBar": False, "responsive": True},
            )),
            html.Div(id=ids.CHIP_READOUT),
            _phase_sliders(),
        ],
    )


def _controls() -> html.Div:
    return html.Div(
        className="control-grid",
        children=[
            labelled("Cíl: co má čip se světlem udělat", dcc.Dropdown(
                id=ids.CHIP_TARGET_DROPDOWN,
                options=[{"label": label, "value": target.value} for target, label in TARGET_LABELS.items()],
                value=DEFAULT_TARGET.value, clearable=False, searchable=False,
            )),
            labelled("Čip", dcc.Dropdown(
                id=ids.CHIP_FABRICATION_DROPDOWN,
                options=[{"label": label, "value": spread} for label, spread in CHIP_OPTIONS],
                value=CHIP_OPTIONS[0][1], clearable=False, searchable=False,
            )),
            html.Div(className="field", children=[
                html.Label("Seed"),
                dcc.Dropdown(
                    id=ids.CHIP_SEED_DROPDOWN, options=[{"label": str(seed), "value": seed} for seed in CHIP_SEEDS],
                    value=CHIP_SEEDS[0], clearable=False, searchable=False,
                ),
                html.P(SEED_HINT, className="hint small"),
            ]),
            labelled("Laser svítí do vstupu", dcc.RadioItems(
                id=ids.CHIP_LASER_RADIO,
                options=[{"label": str(mode + 1), "value": mode} for mode in range(MODE_COUNT)],
                value=DEFAULT_LASER_INPUT, inline=True, className="chip-laser-radio",
            )),
        ],
    )


def _phase_sliders() -> html.Details:
    cards: List[html.Div] = []
    for slot, internal_id, external_id in zip(
        mesh_slots(MODE_COUNT), internal_phase_slider_ids(), external_phase_slider_ids()
    ):
        number = len(cards) + 1
        cards.append(html.Div(className="chip-phase-card", children=[
            html.Strong(f"MZI {number} · světlovody {slot.upper_mode + 1} a {slot.lower_mode + 1}"),
            labelled(f"θ{number} – dělení světla", _phase_slider(internal_id)),
            labelled(f"φ{number} – fáze horního vstupu", _phase_slider(external_id)),
        ]))
    return html.Details(open=True, className="chip-phases", children=[
        html.Summary("Fáze ručně"),
        html.P(PHASES_HINT, className="hint small"),
        html.Div(className="chip-phase-grid", children=cards),
    ])


def _phase_slider(component_id: str) -> dcc.Slider:
    return dcc.Slider(
        id=component_id, min=0, max=2 * np.pi, step=PHASE_STEP, value=0, marks=PHASE_MARKS, updatemode="mouseup",
    )
