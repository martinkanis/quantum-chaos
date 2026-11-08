"""Callbacks of the chip simulator: the number of waveguides rebuilds the phase sliders, buttons set them, every
control redraws the chip and its readout."""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional, Sequence

import numpy as np
from dash import ALL, Dash, Input, Output, State, ctx, no_update

from gbs.bench import Bench, DetectorKind, LightSource, Losses, compatible_detector
from gbs.chip_charts import ChipInteraction, chip_figure
from gbs.chip_programming import ChipSetup, ChipTarget, build_setup, calibrated_phases, design_phases, read_out
from gbs.photonic_chip import ChipError, MeshPhases, mzi_count, random_phases, zero_phases
from ui import ids
from ui.chip_selection import parse_selected_shifter
from ui.chip_bench_content import MAX_CHIP_UNIT
from ui.chip_bench_page import DEFAULT_LASER_INPUT, laser_options
from ui.chip_bench_results import build_bench_readout
from ui.chip_simulator_content import MAX_LAB_MODE_COUNT, MIN_LAB_MODE_COUNT
from ui.chip_simulator_page import phase_cards, phase_slider_id
from ui.chip_simulator_results import build_chip_readout
from ui.navigation import CHIP_SIMULATOR_PATH

logger = logging.getLogger(__name__)

PHASE_DECIMALS = 4
"""Sliders show the phases rounded; on the ideal chip the rounding costs less than 0,01 % of the match."""
INTERNAL_SLIDERS = phase_slider_id(ids.CHIP_INTERNAL_PHASE, ALL)
EXTERNAL_SLIDERS = phase_slider_id(ids.CHIP_EXTERNAL_PHASE, ALL)
MODE_COUNT_MESSAGE = f"Počet světlovodů musí být celé číslo od {MIN_LAB_MODE_COUNT} do {MAX_LAB_MODE_COUNT}."
LASER_INPUT_MESSAGE = "Vyber vstup, do kterého svítí zdroj."
CHIP_UNIT_MESSAGE = f"Číslo kusu čipu musí být celé číslo od 0 do {MAX_CHIP_UNIT}."


def register_chip_simulator_callbacks(app: Dash) -> None:
    app.callback(
        output=dict(
            phase_cards=Output(ids.CHIP_PHASE_GRID, "children"),
            laser_options=Output(ids.CHIP_LASER_RADIO, "options"),
            laser=Output(ids.CHIP_LASER_RADIO, "value"),
        ),
        inputs=dict(mode_count=Input(ids.CHIP_MODE_COUNT_INPUT, "value")),
        state=dict(current_laser=State(ids.CHIP_LASER_RADIO, "value")),
        prevent_initial_call=True,
    )(resize_chip)
    app.callback(
        output=dict(
            internal=Output(INTERNAL_SLIDERS, "value"),
            external=Output(EXTERNAL_SLIDERS, "value"),
            error=Output(ids.CHIP_ERROR_MESSAGE, "children", allow_duplicate=True),
        ),
        inputs=dict(
            _program_clicks=Input(ids.CHIP_PROGRAM_BUTTON, "n_clicks"),
            _calibrate_clicks=Input(ids.CHIP_CALIBRATE_BUTTON, "n_clicks"),
            _reset_clicks=Input(ids.CHIP_RESET_BUTTON, "n_clicks"),
            _random_clicks=Input(ids.CHIP_RANDOM_BUTTON, "n_clicks"),
        ),
        state=dict(setup_form=setup_form_inputs(State), current_internal=State(INTERNAL_SLIDERS, "value")),
        prevent_initial_call=True,
    )(program_chip)
    app.callback(
        output=dict(
            figure=Output(ids.CHIP_FIGURE, "figure"),
            readout=Output(ids.CHIP_READOUT, "children"),
            bench_readout=Output(ids.CHIP_BENCH_READOUT, "children"),
            error=Output(ids.CHIP_ERROR_MESSAGE, "children"),
        ),
        inputs=dict(
            pathname=Input(ids.URL, "pathname"),
            setup_form=setup_form_inputs(Input),
            bench_form=bench_form_inputs(Input),
            selected=Input(ids.CHIP_SELECTED_SHIFTER, "data"),
            phases=phase_inputs(Input),
        ),
        state=dict(current_readout=State(ids.CHIP_READOUT, "children")),
    )(show_chip)


def setup_form_inputs(dependency: type) -> Dict[str, Any]:
    """The chip and what it should do."""
    return dict(
        mode_count=dependency(ids.CHIP_MODE_COUNT_INPUT, "value"),
        target=dependency(ids.CHIP_TARGET_DROPDOWN, "value"),
        split_spread=dependency(ids.CHIP_FABRICATION_DROPDOWN, "value"),
        seed=dependency(ids.CHIP_SEED_DROPDOWN, "value"),
        chip_unit=dependency(ids.CHIP_UNIT_INPUT, "value"),
    )


def bench_form_inputs(dependency: type) -> Dict[str, Any]:
    """The source, where it shines, whether it is on, the losses and the detectors."""
    return dict(
        source=dependency(ids.CHIP_SOURCE_RADIO, "value"),
        detector=dependency(ids.CHIP_DETECTOR_RADIO, "value"),
        coupling_db=dependency(ids.CHIP_COUPLING_LOSS_SLIDER, "value"),
        waveguide_db_per_cm=dependency(ids.CHIP_WAVEGUIDE_LOSS_SLIDER, "value"),
        source_input=dependency(ids.CHIP_LASER_RADIO, "value"),
        source_on=dependency(ids.CHIP_LASER_ON, "data"),
    )


def phase_inputs(dependency: type) -> Dict[str, Any]:
    return dict(internal=dependency(INTERNAL_SLIDERS, "value"), external=dependency(EXTERNAL_SLIDERS, "value"))


def resize_chip(mode_count: Any, current_laser: Any) -> dict:
    """Sliders at zero and laser inputs for the new number of waveguides; the laser stays where the chip still has
    a waveguide."""
    try:
        count = parse_mode_count(mode_count)
    except ChipError:
        # show_chip reads the same input and shows the message; the old sliders stay until the number is valid.
        return dict(phase_cards=no_update, laser_options=no_update, laser=no_update)
    laser = current_laser if _is_waveguide_of(current_laser, count) else DEFAULT_LASER_INPUT
    return dict(phase_cards=phase_cards(count), laser_options=laser_options(count), laser=laser)


def _is_waveguide_of(value: Any, mode_count: int) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and 0 <= value < mode_count


def program_chip(
    _program_clicks: Optional[int], _calibrate_clicks: Optional[int], _reset_clicks: Optional[int],
    _random_clicks: Optional[int], setup_form: Dict[str, Any], current_internal: Sequence[Any],
) -> dict:
    unchanged = dict(internal=[no_update] * len(current_internal), external=[no_update] * len(current_internal))
    try:
        phases = phases_for_button(ctx.triggered_id, parse_setup(setup_form))
    except ChipError as error:
        return dict(unchanged, error=str(error))
    if len(phases.internal) != len(current_internal):
        # The sliders still belong to the previous number of waveguides; resize_chip is replacing them.
        return dict(unchanged, error=no_update)
    return dict(internal=_rounded(phases.internal), external=_rounded(phases.external), error="")


def phases_for_button(button_id: Optional[str], setup: ChipSetup) -> MeshPhases:
    if button_id == ids.CHIP_RESET_BUTTON:
        return zero_phases(setup.chip.mode_count)
    if button_id == ids.CHIP_RANDOM_BUTTON:
        return random_phases(setup.chip.mode_count, np.random.default_rng())
    if button_id == ids.CHIP_CALIBRATE_BUTTON:
        logger.info("Calibrating chip phases on a fabricated chip with %d waveguides", setup.chip.mode_count)
        return calibrated_phases(setup)
    return design_phases(setup)


def show_chip(
    pathname: str, setup_form: Dict[str, Any], bench_form: Dict[str, Any], selected: Any,
    phases: Dict[str, Sequence[Any]], current_readout: Any,
) -> dict:
    unchanged = dict(figure=no_update, readout=no_update, bench_readout=no_update, error=no_update)
    if not should_draw_chip(ctx.triggered_id, pathname, current_readout):
        return unchanged
    try:
        setup = parse_setup(setup_form)
        bench = parse_bench(bench_form)
        source_input = parse_laser_input(bench_form["source_input"])
        mesh_phases = parse_phases(phases["internal"], phases["external"])
    except ChipError as error:
        return dict(unchanged, error=str(error))
    mode_count = setup.chip.mode_count
    if source_input >= mode_count:
        # The chip just lost the waveguide the source shines into; resize_chip moves the source to input 1.
        return unchanged
    if len(mesh_phases.internal) != mzi_count(mode_count):
        # Sliders of the previous chip; resize_chip replaces them with sliders at zero, so the new chip starts there.
        mesh_phases = zero_phases(mode_count)
    is_on = bool(bench_form["source_on"])
    readout = read_out(setup, mesh_phases, source_input if is_on else None)
    interaction = ChipInteraction(parse_selected_shifter(selected, mzi_count(mode_count)))
    figure = chip_figure(setup.chip, mesh_phases, readout.flow, bench.source, interaction)
    chip_shares = readout.chip_transmission[:, source_input] if is_on else None
    return dict(
        figure=figure, readout=build_chip_readout(readout),
        bench_readout=build_bench_readout(bench, chip_shares, mode_count), error="",
    )


def should_draw_chip(triggered_id: Any, pathname: str, current_readout: Any) -> bool:
    """Redraws on every change of a control, and the first time the page is shown."""
    if triggered_id is not None and triggered_id != ids.URL:
        return True
    return pathname == CHIP_SIMULATOR_PATH and not current_readout


def parse_setup(setup_form: Dict[str, Any]) -> ChipSetup:
    try:
        target = ChipTarget(setup_form["target"])
    except ValueError as error:
        raise ChipError("Vyber cíl ze seznamu.") from error
    mode_count = parse_mode_count(setup_form["mode_count"])
    split_spread = form_number(setup_form["split_spread"], "Vyber čip ze seznamu.")
    seed = form_whole_number(setup_form["seed"], "Seed musí být celé číslo.")
    chip_unit = form_whole_number_between(setup_form["chip_unit"], 0, MAX_CHIP_UNIT, CHIP_UNIT_MESSAGE)
    return build_setup(target, split_spread, seed, mode_count, chip_unit)


def parse_bench(bench_form: Dict[str, Any]) -> Bench:
    """The detector follows the source even before its radio has caught up: a photodiode for the laser, a photon
    counter for single photons."""
    try:
        source = LightSource(bench_form["source"])
        detector = DetectorKind(bench_form["detector"])
    except ValueError as error:
        raise ChipError("Vyber zdroj a detektor ze seznamu.") from error
    losses = Losses(
        form_number(bench_form["coupling_db"], "Ztráta vazby vlákno–čip musí být číslo v dB."),
        form_number(bench_form["waveguide_db_per_cm"], "Útlum světlovodů musí být číslo v dB/cm."),
    )
    return Bench(source, compatible_detector(source, detector), losses)


def parse_mode_count(value: Any) -> int:
    return form_whole_number_between(value, MIN_LAB_MODE_COUNT, MAX_LAB_MODE_COUNT, MODE_COUNT_MESSAGE)


def parse_phases(internal: Sequence[Any], external: Sequence[Any]) -> MeshPhases:
    message = "Každá fáze musí být číslo v radiánech; nastav posuvník znovu."
    return MeshPhases(
        tuple(form_number(value, message) for value in internal),
        tuple(form_number(value, message) for value in external),
    )


def parse_laser_input(value: Any) -> int:
    laser_input = form_whole_number(value, LASER_INPUT_MESSAGE)
    if laser_input < 0:
        raise ChipError(LASER_INPUT_MESSAGE)
    return laser_input


def form_number(value: Any, message: str) -> float:
    """A number from a form control; anything else raises ChipError with the message for the reader."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ChipError(message)
    return float(value)


def form_whole_number(value: Any, message: str) -> int:
    number = form_number(value, message)
    if not number.is_integer():
        raise ChipError(message)
    return int(number)


def form_whole_number_between(value: Any, minimum: int, maximum: int, message: str) -> int:
    number = form_whole_number(value, message)
    if not minimum <= number <= maximum:
        raise ChipError(message)
    return number


def _rounded(phases: Sequence[float]) -> list:
    return [round(phase, PHASE_DECIMALS) for phase in phases]
