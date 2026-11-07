"""Page of the photonic chip simulator: controls, the chip with the laser light, phase sliders and the explanation."""

from __future__ import annotations

from typing import Any, List, Tuple

import numpy as np
from dash import dcc, html

from gbs.chip_boson_sampling import PhotonKind
from gbs.chip_charts import LightSource, empty_chip_figure
from gbs.photonic_chip import MODE_COUNT, mesh_slots
from ui import ids
from ui.chip_animation import light_animation_controls
from ui.chip_simulator_content import (
    ANIMATION_HINT,
    CHIP_OPTIONS,
    CHIP_SEEDS,
    DEFAULT_TARGET,
    IN_SHORT,
    LAB_ANCHOR,
    LAB_INTRO,
    LEAD,
    MAX_LAB_MODE_COUNT,
    MIN_LAB_MODE_COUNT,
    MODE_COUNT_HINT,
    PHASES_HINT,
    SEED_HINT,
    SOURCES_ANCHOR,
    TARGET_LABELS,
    TITLE,
    TOPICS,
)
from ui.chip_sampling_content import (
    DEFAULT_MODE_COUNT,
    DEFAULT_PHOTONS,
    DEFAULT_SHOTS,
    MAX_SAMPLING_MODE_COUNT,
    MIN_SAMPLING_MODE_COUNT,
    PHOTON_KIND_LABELS,
    PHOTON_OPTIONS,
    SAMPLING_ANCHOR,
    SAMPLING_CHIP_OPTIONS,
    SAMPLING_INTRO,
    SAMPLING_MODE_COUNT_HINT,
    SAMPLING_SEED_HINT,
    SAMPLING_SEEDS,
    SAMPLING_TARGET_LABELS,
    SAMPLING_TITLE,
    SHOT_OPTIONS,
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


def phase_slider_id(kind: str, mzi: Any) -> dict:
    """kind is ids.CHIP_INTERNAL_PHASE (θ) or ids.CHIP_EXTERNAL_PHASE (φ); mzi is its index, or ALL in callbacks."""
    return {"type": ids.CHIP_PHASE_SLIDER, "kind": kind, "mzi": mzi}


def laser_options(mode_count: int) -> List[dict]:
    return [{"label": str(mode + 1), "value": mode} for mode in range(mode_count)]


def phase_cards(mode_count: int) -> List[html.Div]:
    """One card per MZI with its θ and φ, all at zero, in the order of the mesh."""
    cards: List[html.Div] = []
    for index, slot in enumerate(mesh_slots(mode_count)):
        number = index + 1
        cards.append(html.Div(className="chip-phase-card", children=[
            html.Strong(f"MZI {number} · světlovody {slot.upper_mode + 1} a {slot.lower_mode + 1}"),
            labelled(f"θ{number} – dělení světla", _phase_slider(ids.CHIP_INTERNAL_PHASE, index)),
            labelled(f"φ{number} – fáze horního vstupu", _phase_slider(ids.CHIP_EXTERNAL_PHASE, index)),
        ]))
    return cards


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
            _sampling_section(),
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
            light_animation_controls(ids.CHIP_FIGURE, LightSource.LASER),
            html.Div(className="chip-figure", children=dcc.Graph(
                id=ids.CHIP_FIGURE, figure=empty_chip_figure(), style={"minWidth": CHIP_FIGURE_MIN_WIDTH},
                config={"displayModeBar": False, "responsive": True},
            )),
            html.P(ANIMATION_HINT, className="hint small"),
            html.Div(id=ids.CHIP_READOUT),
            _phase_sliders(),
        ],
    )


def _sampling_section() -> html.Section:
    return html.Section(
        id=SAMPLING_ANCHOR,
        className="card",
        children=[
            html.H2(SAMPLING_TITLE),
            dcc.Markdown(SAMPLING_INTRO, mathjax=True),
            _sampling_controls(),
            html.Button("Spustit boson sampling", id=ids.CHIP_SAMPLING_RUN_BUTTON, className="primary-button"),
            html.Div(id=ids.CHIP_SAMPLING_ERROR_MESSAGE, className="error-message"),
            dcc.Loading(html.Div(id=ids.CHIP_SAMPLING_RESULTS), type="circle"),
        ],
    )


def _sampling_controls() -> html.Div:
    return html.Div(
        className="control-grid",
        children=[
            html.Div(className="field", children=[
                html.Label("Světlovody"),
                dcc.Input(
                    id=ids.CHIP_SAMPLING_MODES_INPUT, type="number", min=MIN_SAMPLING_MODE_COUNT,
                    max=MAX_SAMPLING_MODE_COUNT, step=1, value=DEFAULT_MODE_COUNT, debounce=True,
                ),
                html.P(SAMPLING_MODE_COUNT_HINT, className="hint small"),
            ]),
            html.Div(className="field", children=[
                html.Label("Fotony na vstupu"),
                _dropdown(ids.CHIP_SAMPLING_PHOTONS_DROPDOWN, [(str(count), count) for count in PHOTON_OPTIONS],
                          DEFAULT_PHOTONS),
                html.P(id=ids.CHIP_SAMPLING_PATTERN_COUNT, className="hint small"),
            ]),
            labelled("Interferometr", _dropdown(
                ids.CHIP_SAMPLING_TARGET_DROPDOWN,
                [(label, target.value) for target, label in SAMPLING_TARGET_LABELS.items()],
                next(iter(SAMPLING_TARGET_LABELS)).value,
            )),
            labelled("Čip", _dropdown(ids.CHIP_SAMPLING_FABRICATION_DROPDOWN, list(SAMPLING_CHIP_OPTIONS),
                                      SAMPLING_CHIP_OPTIONS[0][1])),
            labelled("Druh fotonů", dcc.RadioItems(
                id=ids.CHIP_SAMPLING_KIND_RADIO,
                options=[{"label": label, "value": kind.value} for kind, label in PHOTON_KIND_LABELS.items()],
                value=PhotonKind.INDISTINGUISHABLE.value, className="radio-list",
            )),
            labelled("Počet výstřelů", _dropdown(
                ids.CHIP_SAMPLING_SHOTS_DROPDOWN, [(f"{shots:,}".replace(",", " "), shots) for shots in SHOT_OPTIONS],
                DEFAULT_SHOTS,
            )),
            html.Div(className="field", children=[
                html.Label("Seed"),
                _dropdown(ids.CHIP_SAMPLING_SEED_DROPDOWN, [(str(seed), seed) for seed in SAMPLING_SEEDS],
                          SAMPLING_SEEDS[0]),
                html.P(SAMPLING_SEED_HINT, className="hint small"),
            ]),
        ],
    )


def _dropdown(component_id: str, options: List[Tuple[str, Any]], value: Any) -> dcc.Dropdown:
    return dcc.Dropdown(
        id=component_id, options=[{"label": label, "value": option} for label, option in options], value=value,
        clearable=False, searchable=False,
    )


def _controls() -> html.Div:
    return html.Div(
        className="control-grid",
        children=[
            html.Div(className="field", children=[
                html.Label("Počet světlovodů"),
                dcc.Input(
                    id=ids.CHIP_MODE_COUNT_INPUT, type="number", min=MIN_LAB_MODE_COUNT, max=MAX_LAB_MODE_COUNT, step=1,
                    value=MODE_COUNT, debounce=True, className="chip-mode-count",
                ),
                html.P(MODE_COUNT_HINT, className="hint small"),
            ]),
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
                options=laser_options(MODE_COUNT), value=DEFAULT_LASER_INPUT, inline=True, className="chip-laser-radio",
            )),
        ],
    )


def _phase_sliders() -> html.Details:
    return html.Details(open=True, className="chip-phases", children=[
        html.Summary("Fáze ručně"),
        html.P(PHASES_HINT, className="hint small"),
        html.Div(id=ids.CHIP_PHASE_GRID, className="chip-phase-grid", children=phase_cards(MODE_COUNT)),
    ])


def _phase_slider(kind: str, mzi: int) -> dcc.Slider:
    return dcc.Slider(
        id=phase_slider_id(kind, mzi), min=0, max=2 * np.pi, step=PHASE_STEP, value=0, marks=PHASE_MARKS,
        updatemode="mouseup",
    )
