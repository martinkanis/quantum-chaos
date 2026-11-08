"""Layout of the optical bench in laboratory 1: the source, the detectors, the losses and the fabricated piece of the
chip; below the chip what the detectors register."""

from __future__ import annotations

from typing import List

from dash import dcc, html

from gbs.bench import DETECTORS, MAX_COUPLING_LOSS_DB, MAX_WAVEGUIDE_LOSS_DB_PER_CM, DetectorKind, LightSource
from gbs.photonic_chip import MODE_COUNT
from ui import ids
from ui.chip_bench_content import (
    BENCH_HINT,
    BENCH_TITLE,
    DEFAULT_CHIP_UNIT,
    DEFAULT_COUPLING_LOSS_DB,
    DEFAULT_PHOTON_SHOTS,
    DEFAULT_WAVEGUIDE_LOSS_DB_PER_CM,
    DETECTOR_LABELS,
    LOSS_STEP_DB,
    MAX_CHIP_UNIT,
    PHOTON_SHOT_OPTIONS,
    SOURCE_LABELS,
)
from ui.chip_simulator_content import CHIP_OPTIONS
from ui.components import labelled
from ui.navigation import HIDDEN

DEFAULT_LASER_INPUT = 0
"""Index of the waveguide the source shines into; the page counts waveguides from 1."""
COUPLING_LOSS_MARKS = {0: "0", 3: "3", 6: "6", 10: "10 dB"}
WAVEGUIDE_LOSS_MARKS = {0: "0", 1: "1", 3: "3", 5: "5 dB/cm"}


def laser_options(mode_count: int) -> List[dict]:
    return [{"label": str(mode + 1), "value": mode} for mode in range(mode_count)]


def source_options() -> List[dict]:
    return [{"label": _option_label(*SOURCE_LABELS[source]), "value": source.value} for source in LightSource]


def detector_options(source: LightSource) -> List[dict]:
    """Every detector, the ones that do not suit the source disabled."""
    return [
        {
            "label": _option_label(*DETECTOR_LABELS[kind]),
            "value": kind.value,
            "disabled": DETECTORS[kind].counts_photons != (source == LightSource.PHOTONS),
        }
        for kind in DetectorKind
    ]


def _option_label(name: str, description: str) -> html.Span:
    return html.Span([html.Strong(name), html.Span(f" – {description}", className="chip-option-description")])


def bench_controls() -> html.Details:
    return html.Details(open=True, className="chip-bench", children=[
        html.Summary(BENCH_TITLE),
        html.Div(className="control-grid", children=[
            labelled("Zdroj", dcc.RadioItems(
                id=ids.CHIP_SOURCE_RADIO, options=source_options(), value=LightSource.LASER.value,
                className="radio-list",
            )),
            labelled("Detektory", dcc.RadioItems(
                id=ids.CHIP_DETECTOR_RADIO, options=detector_options(LightSource.LASER),
                value=DetectorKind.PHOTODIODE.value, className="radio-list",
            )),
            labelled("Zdroj svítí do vstupu", dcc.RadioItems(
                id=ids.CHIP_LASER_RADIO, options=laser_options(MODE_COUNT), value=DEFAULT_LASER_INPUT, inline=True,
                className="chip-laser-radio",
            )),
            _losses(),
            _chip_piece(),
        ]),
        html.P(BENCH_HINT, className="hint small"),
    ])


def _losses() -> html.Div:
    return html.Div(className="field", children=[
        html.Label("Ztráty"),
        html.Span("vazba vlákno–čip, na jeden přechod", className="chip-option-description"),
        dcc.Slider(
            id=ids.CHIP_COUPLING_LOSS_SLIDER, min=0, max=MAX_COUPLING_LOSS_DB, step=LOSS_STEP_DB,
            value=DEFAULT_COUPLING_LOSS_DB, marks=COUPLING_LOSS_MARKS, updatemode="mouseup",
        ),
        html.Span("útlum ve světlovodech", className="chip-option-description"),
        dcc.Slider(
            id=ids.CHIP_WAVEGUIDE_LOSS_SLIDER, min=0, max=MAX_WAVEGUIDE_LOSS_DB_PER_CM, step=LOSS_STEP_DB,
            value=DEFAULT_WAVEGUIDE_LOSS_DB_PER_CM, marks=WAVEGUIDE_LOSS_MARKS, updatemode="mouseup",
        ),
    ])


def _chip_piece() -> html.Div:
    return html.Div(className="field", children=[
        html.Label("Čip"),
        dcc.Dropdown(
            id=ids.CHIP_FABRICATION_DROPDOWN,
            options=[{"label": label, "value": spread} for label, spread in CHIP_OPTIONS],
            value=CHIP_OPTIONS[0][1], clearable=False, searchable=False,
        ),
        html.Div(className="chip-unit", children=[
            html.Span("kus č.", className="chip-option-description"),
            dcc.Input(
                id=ids.CHIP_UNIT_INPUT, type="number", min=0, max=MAX_CHIP_UNIT, step=1, value=DEFAULT_CHIP_UNIT,
                debounce=True,
            ),
            html.Button("Jiný kus", id=ids.CHIP_NEW_UNIT_BUTTON, className="secondary-button"),
        ]),
    ])


def bench_readout_panel() -> html.Div:
    """What the detectors register; the photon counter is there only for single photons."""
    return html.Div(className="chip-bench-readout", children=[
        html.H3("Co zaznamenají detektory"),
        html.Div(id=ids.CHIP_BENCH_READOUT),
        html.Div(id=ids.CHIP_PHOTON_CONTROLS, style=HIDDEN, children=[
            html.Div(className="chip-buttons", children=[
                dcc.Dropdown(
                    id=ids.CHIP_PHOTON_SHOTS_DROPDOWN,
                    options=[{"label": f"{shots:,} fotonů".replace(",", " "), "value": shots}
                             for shots in PHOTON_SHOT_OPTIONS],
                    value=DEFAULT_PHOTON_SHOTS, clearable=False, searchable=False, className="chip-shots-dropdown",
                ),
                html.Button("Vystřelit fotony", id=ids.CHIP_PHOTON_SHOOT_BUTTON, className="primary-button"),
            ]),
            dcc.Loading(html.Div(id=ids.CHIP_PHOTON_COUNTS), type="circle"),
        ]),
    ])
