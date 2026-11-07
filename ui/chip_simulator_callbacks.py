"""Callbacks of the chip simulator: buttons set the phase sliders, every control redraws the chip and its readout."""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional, Sequence

from dash import Dash, Input, Output, State, ctx, no_update

from gbs.chip_charts import chip_figure
from gbs.chip_programming import ChipSetup, ChipTarget, build_setup, calibrated_phases, design_phases, read_out
from gbs.photonic_chip import MODE_COUNT, ChipError, MeshPhases, zero_phases
from ui import ids
from ui.chip_simulator_page import external_phase_slider_ids, internal_phase_slider_ids
from ui.chip_simulator_results import build_chip_readout
from ui.navigation import CHIP_SIMULATOR_PATH

logger = logging.getLogger(__name__)

PHASE_DECIMALS = 4
"""Sliders show the phases rounded; on the ideal chip the rounding costs less than 0,01 % of the match."""


def register_chip_simulator_callbacks(app: Dash) -> None:
    app.callback(
        output=dict(
            internal=[Output(slider_id, "value") for slider_id in internal_phase_slider_ids()],
            external=[Output(slider_id, "value") for slider_id in external_phase_slider_ids()],
            error=Output(ids.CHIP_ERROR_MESSAGE, "children", allow_duplicate=True),
        ),
        inputs=dict(
            _program_clicks=Input(ids.CHIP_PROGRAM_BUTTON, "n_clicks"),
            _calibrate_clicks=Input(ids.CHIP_CALIBRATE_BUTTON, "n_clicks"),
            _reset_clicks=Input(ids.CHIP_RESET_BUTTON, "n_clicks"),
        ),
        state=dict(setup_form=_setup_form(State)),
        prevent_initial_call=True,
    )(program_chip)
    app.callback(
        output=dict(
            figure=Output(ids.CHIP_FIGURE, "figure"),
            readout=Output(ids.CHIP_READOUT, "children"),
            error=Output(ids.CHIP_ERROR_MESSAGE, "children"),
        ),
        inputs=dict(
            pathname=Input(ids.URL, "pathname"),
            setup_form=_setup_form(Input),
            laser=Input(ids.CHIP_LASER_RADIO, "value"),
            internal=[Input(slider_id, "value") for slider_id in internal_phase_slider_ids()],
            external=[Input(slider_id, "value") for slider_id in external_phase_slider_ids()],
        ),
        state=dict(current_readout=State(ids.CHIP_READOUT, "children")),
    )(show_chip)


def _setup_form(dependency: type) -> Dict[str, Any]:
    return dict(
        target=dependency(ids.CHIP_TARGET_DROPDOWN, "value"),
        split_spread=dependency(ids.CHIP_FABRICATION_DROPDOWN, "value"),
        seed=dependency(ids.CHIP_SEED_DROPDOWN, "value"),
    )


def program_chip(
    _program_clicks: Optional[int], _calibrate_clicks: Optional[int], _reset_clicks: Optional[int],
    setup_form: Dict[str, Any],
) -> dict:
    slider_count = len(internal_phase_slider_ids())
    try:
        phases = phases_for_button(ctx.triggered_id, parse_setup(setup_form))
    except ChipError as error:
        return dict(internal=[no_update] * slider_count, external=[no_update] * slider_count, error=str(error))
    return dict(internal=_rounded(phases.internal), external=_rounded(phases.external), error="")


def phases_for_button(button_id: Optional[str], setup: ChipSetup) -> MeshPhases:
    if button_id == ids.CHIP_RESET_BUTTON:
        return zero_phases(MODE_COUNT)
    if button_id == ids.CHIP_CALIBRATE_BUTTON:
        logger.info("Calibrating chip phases on a fabricated chip")
        return calibrated_phases(setup)
    return design_phases(setup)


def show_chip(
    pathname: str, setup_form: Dict[str, Any], laser: Any, internal: Sequence[Any], external: Sequence[Any],
    current_readout: Any,
) -> dict:
    if not should_draw_chip(ctx.triggered_id, pathname, current_readout):
        return dict(figure=no_update, readout=no_update, error=no_update)
    try:
        setup = parse_setup(setup_form)
        phases = parse_phases(internal, external)
        readout = read_out(setup, phases, parse_laser_input(laser))
    except ChipError as error:
        return dict(figure=no_update, readout=no_update, error=str(error))
    return dict(figure=chip_figure(setup.chip, phases, readout.flow), readout=build_chip_readout(readout), error="")


def should_draw_chip(triggered_id: Optional[str], pathname: str, current_readout: Any) -> bool:
    """Redraws on every change of a control, and the first time the page is shown."""
    if triggered_id is not None and triggered_id != ids.URL:
        return True
    return pathname == CHIP_SIMULATOR_PATH and not current_readout


def parse_setup(setup_form: Dict[str, Any]) -> ChipSetup:
    try:
        target = ChipTarget(setup_form["target"])
    except ValueError as error:
        raise ChipError("Vyber cíl ze seznamu.") from error
    split_spread = form_number(setup_form["split_spread"], "Vyber čip ze seznamu.")
    seed = form_whole_number(setup_form["seed"], "Seed musí být celé číslo.")
    return build_setup(target, split_spread, seed)


def parse_phases(internal: Sequence[Any], external: Sequence[Any]) -> MeshPhases:
    message = "Každá fáze musí být číslo v radiánech; nastav posuvník znovu."
    return MeshPhases(
        tuple(form_number(value, message) for value in internal),
        tuple(form_number(value, message) for value in external),
    )


def parse_laser_input(value: Any) -> int:
    return form_whole_number(value, f"Vyber vstup 1 až {MODE_COUNT}, do kterého svítí laser.")


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


def _rounded(phases: Sequence[float]) -> list:
    return [round(phase, PHASE_DECIMALS) for phase in phases]
