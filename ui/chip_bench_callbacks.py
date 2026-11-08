"""Callbacks of the optical bench in laboratory 1: the detectors follow the source, a new piece of the chip, and a
run of single photons counted by the detectors."""

from __future__ import annotations

from typing import Any, Dict, Optional, Sequence

import numpy as np
from dash import Dash, Input, Output, State, ctx, html

from gbs.bench import DetectorKind, LightSource, compatible_detector, count_photons, registered_shares
from gbs.chip_programming import read_out
from gbs.photonic_chip import ChipError, mzi_count
from ui import ids
from ui.chip_bench_content import MAX_CHIP_UNIT
from ui.chip_bench_page import detector_options
from ui.chip_bench_results import SOURCE_OFF_TEXT, build_photon_counts
from ui.chip_simulator_callbacks import (
    bench_form_inputs,
    form_whole_number,
    parse_bench,
    parse_laser_input,
    parse_phases,
    parse_setup,
    phase_inputs,
    setup_form_inputs,
)
from ui.navigation import HIDDEN, VISIBLE

SHOTS_MESSAGE = "Vyber počet fotonů ze seznamu."


def register_chip_bench_callbacks(app: Dash) -> None:
    app.callback(
        Output(ids.CHIP_DETECTOR_RADIO, "options"),
        Output(ids.CHIP_DETECTOR_RADIO, "value"),
        Input(ids.CHIP_SOURCE_RADIO, "value"),
        State(ids.CHIP_DETECTOR_RADIO, "value"),
        prevent_initial_call=True,
    )(match_detector_to_source)
    app.callback(
        Output(ids.CHIP_PHOTON_CONTROLS, "style"),
        Input(ids.CHIP_SOURCE_RADIO, "value"),
    )(show_photon_controls)
    app.callback(
        Output(ids.CHIP_UNIT_INPUT, "value"),
        Input(ids.CHIP_NEW_UNIT_BUTTON, "n_clicks"),
        prevent_initial_call=True,
    )(new_chip_unit)
    app.callback(
        Output(ids.CHIP_PHOTON_COUNTS, "children"),
        inputs=dict(
            _shoot_clicks=Input(ids.CHIP_PHOTON_SHOOT_BUTTON, "n_clicks"),
            setup_form=setup_form_inputs(Input),
            bench_form=bench_form_inputs(Input),
            phases=phase_inputs(Input),
        ),
        state=dict(shots=State(ids.CHIP_PHOTON_SHOTS_DROPDOWN, "value")),
        prevent_initial_call=True,
    )(photon_counts)


def match_detector_to_source(source: Any, current: Any) -> tuple:
    """Detectors that do not suit the source are disabled, and a disabled choice moves to one that suits it."""
    light_source = _light_source(source)
    try:
        detector = compatible_detector(light_source, DetectorKind(current))
    except ValueError:
        detector = compatible_detector(light_source, DetectorKind.PHOTODIODE)
    return detector_options(light_source), detector.value


def show_photon_controls(source: Any) -> dict:
    return VISIBLE if source == LightSource.PHOTONS.value else HIDDEN


def new_chip_unit(_clicks: Optional[int]) -> int:
    """Another fabricated piece of the same design, as the lab would pick one from the drawer."""
    return int(np.random.default_rng().integers(1, MAX_CHIP_UNIT + 1))


def photon_counts(
    _shoot_clicks: Optional[int], setup_form: Dict[str, Any], bench_form: Dict[str, Any],
    phases: Dict[str, Sequence[Any]], shots: Any,
) -> Optional[html.Div]:
    """Counts of a run of photons; any change of the chip or the bench clears them, they would no longer match."""
    if ctx.triggered_id != ids.CHIP_PHOTON_SHOOT_BUTTON:
        return None
    try:
        setup = parse_setup(setup_form)
        bench = parse_bench(bench_form)
        source_input = parse_laser_input(bench_form["source_input"])
        mesh_phases = parse_phases(phases["internal"], phases["external"])
        shot_count = form_whole_number(shots, SHOTS_MESSAGE)
    except ChipError as error:
        return html.P(str(error), className="error-message")
    mode_count = setup.chip.mode_count
    if not bench_form["source_on"]:
        return html.P(SOURCE_OFF_TEXT, className="hint")
    if source_input >= mode_count or len(mesh_phases.internal) != mzi_count(mode_count):
        # The chip is being resized; its new phases and inputs arrive with the next callback.
        return None
    chip_shares = read_out(setup, mesh_phases, source_input).chip_transmission[:, source_input]
    registered = registered_shares(chip_shares, bench.losses, bench.detector, mode_count)
    try:
        counts = count_photons(registered, bench.detector, shot_count, np.random.default_rng())
    except ChipError as error:
        return html.P(str(error), className="error-message")
    return build_photon_counts(counts)


def _light_source(value: Any) -> LightSource:
    try:
        return LightSource(value)
    except ValueError:
        return LightSource.LASER
