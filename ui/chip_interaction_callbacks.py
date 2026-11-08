"""Callbacks that make the chip of laboratory 1 clickable: a click on an input moves the laser, a click on a shifter or
an MZI selects it for the slider above the chip, and the laser can be switched off."""

from __future__ import annotations

from typing import Any, Sequence

from dash import Dash, Input, Output, State, ctx, no_update

from gbs.chip_parts import ChipPart, SelectedShifter, clicked_part
from gbs.photonic_chip import ChipError
from ui import ids
from ui.chip_selection import parse_selected_shifter, selected_shifter_data, selected_shifter_title, selection_for_click
from ui.chip_simulator_callbacks import (
    EXTERNAL_SLIDERS,
    INTERNAL_SLIDERS,
    PHASE_DECIMALS,
    form_number,
    parse_mode_count,
)
from ui.chip_simulator_content import SOURCE_OFF_LABEL, SOURCE_ON_LABEL

SELECTED_PHASE_MESSAGE = "Fáze vybraného posouvače musí být číslo v radiánech; nastav posuvník znovu."


def register_chip_interaction_callbacks(app: Dash) -> None:
    app.callback(
        output=dict(
            selected=Output(ids.CHIP_SELECTED_SHIFTER, "data"),
            laser=Output(ids.CHIP_LASER_RADIO, "value", allow_duplicate=True),
            laser_on=Output(ids.CHIP_LASER_ON, "data", allow_duplicate=True),
        ),
        inputs=dict(click_data=Input(ids.CHIP_FIGURE, "clickData")),
        prevent_initial_call=True,
    )(select_chip_part)
    app.callback(
        output=dict(
            value=Output(ids.CHIP_SELECTED_PHASE_SLIDER, "value"),
            title=Output(ids.CHIP_SELECTED_PHASE_TITLE, "children"),
            internal=Output(INTERNAL_SLIDERS, "value", allow_duplicate=True),
            external=Output(EXTERNAL_SLIDERS, "value", allow_duplicate=True),
        ),
        inputs=dict(
            selected=Input(ids.CHIP_SELECTED_SHIFTER, "data"),
            selected_value=Input(ids.CHIP_SELECTED_PHASE_SLIDER, "value"),
            internal=Input(INTERNAL_SLIDERS, "value"),
            external=Input(EXTERNAL_SLIDERS, "value"),
        ),
        state=dict(mode_count=State(ids.CHIP_MODE_COUNT_INPUT, "value")),
        prevent_initial_call=True,
    )(sync_selected_phase)
    app.callback(
        Output(ids.CHIP_LASER_ON, "data"),
        Input(ids.CHIP_LASER_BUTTON, "n_clicks"),
        State(ids.CHIP_LASER_ON, "data"),
        prevent_initial_call=True,
    )(toggle_laser)
    app.callback(
        Output(ids.CHIP_LASER_BUTTON, "children"),
        Input(ids.CHIP_LASER_ON, "data"),
        prevent_initial_call=True,
    )(describe_laser_button)


def select_chip_part(click_data: Any) -> dict:
    """An input takes the laser (and switches it on), a shifter or an MZI becomes the selected shifter."""
    unchanged = dict(selected=no_update, laser=no_update, laser_on=no_update)
    clicked = clicked_part(click_data)
    if clicked is None:
        return unchanged
    if clicked.part == ChipPart.INPUT:
        return dict(unchanged, laser=clicked.index, laser_on=True)
    shifter = selection_for_click(clicked)
    if shifter is None:
        return unchanged
    return dict(unchanged, selected=selected_shifter_data(shifter))


def sync_selected_phase(
    selected: Any, selected_value: Any, internal: Sequence[Any], external: Sequence[Any], mode_count: Any,
) -> dict:
    """One callback for both directions, so that the slider above the chip and the one in the list never chase
    each other: moving the selected slider writes its phase into the list, anything else reads it from there."""
    shifter = parse_selected_shifter(selected, len(internal))
    if ctx.triggered_id == ids.CHIP_SELECTED_PHASE_SLIDER:
        return written_phase(shifter, selected_value, len(internal))
    return shown_phase(shifter, internal, external, mode_count)


def written_phase(shifter: SelectedShifter, selected_value: Any, mzi_total: int) -> dict:
    unchanged = [no_update] * mzi_total
    try:
        phase = round(form_number(selected_value, SELECTED_PHASE_MESSAGE), PHASE_DECIMALS)
    except ChipError:
        # The slider always sends a number; anything else leaves the chip as it is.
        return dict(value=no_update, title=no_update, internal=unchanged, external=unchanged)
    written = [phase if index == shifter.mzi else no_update for index in range(mzi_total)]
    is_internal = shifter.part == ChipPart.INTERNAL_SHIFTER
    return dict(
        value=no_update, title=no_update,
        internal=written if is_internal else unchanged, external=unchanged if is_internal else written,
    )


def shown_phase(shifter: SelectedShifter, internal: Sequence[Any], external: Sequence[Any], mode_count: Any) -> dict:
    unchanged = [no_update] * len(internal)
    phases = internal if shifter.part == ChipPart.INTERNAL_SHIFTER else external
    try:
        title = selected_shifter_title(shifter, parse_mode_count(mode_count))
    except ChipError:
        # An invalid number of waveguides is reported under the chip; the sliders still belong to the old chip.
        title = no_update
    return dict(value=phases[shifter.mzi], title=title, internal=unchanged, external=unchanged)


def toggle_laser(_clicks: Any, laser_on: Any) -> bool:
    return not bool(laser_on)


def describe_laser_button(laser_on: Any) -> str:
    return SOURCE_OFF_LABEL if laser_on else SOURCE_ON_LABEL
