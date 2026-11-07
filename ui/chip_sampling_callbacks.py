"""Callbacks of the boson sampling lab: the number of output patterns, and the run of both Monte Carlo estimates."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Dict, Optional

from dash import Dash, Input, Output, State

from gbs.chip_boson_sampling import MAX_PATTERNS, PhotonKind, SamplingStudy, pattern_count, run_sampling_study
from gbs.chip_programming import ChipTarget
from gbs.photonic_chip import ChipError
from ui import ids
from ui.chip_sampling_results import build_sampling_results, czech_count
from ui.chip_simulator_callbacks import form_number, form_whole_number

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SamplingForm:
    mode_count: int
    photons: int
    target: ChipTarget
    split_spread: float
    kind: PhotonKind
    shots: int
    seed: int


def register_chip_sampling_callbacks(app: Dash) -> None:
    app.callback(
        Output(ids.CHIP_SAMPLING_PATTERN_COUNT, "children"),
        Input(ids.CHIP_SAMPLING_MODES_DROPDOWN, "value"),
        Input(ids.CHIP_SAMPLING_PHOTONS_DROPDOWN, "value"),
    )(describe_pattern_count)
    app.callback(
        output=dict(
            results=Output(ids.CHIP_SAMPLING_RESULTS, "children"),
            error=Output(ids.CHIP_SAMPLING_ERROR_MESSAGE, "children"),
        ),
        inputs=dict(_clicks=Input(ids.CHIP_SAMPLING_RUN_BUTTON, "n_clicks")),
        state=dict(form=dict(
            mode_count=State(ids.CHIP_SAMPLING_MODES_DROPDOWN, "value"),
            photons=State(ids.CHIP_SAMPLING_PHOTONS_DROPDOWN, "value"),
            target=State(ids.CHIP_SAMPLING_TARGET_DROPDOWN, "value"),
            split_spread=State(ids.CHIP_SAMPLING_FABRICATION_DROPDOWN, "value"),
            kind=State(ids.CHIP_SAMPLING_KIND_RADIO, "value"),
            shots=State(ids.CHIP_SAMPLING_SHOTS_DROPDOWN, "value"),
            seed=State(ids.CHIP_SAMPLING_SEED_DROPDOWN, "value"),
        )),
        prevent_initial_call=True,
    )(run_boson_sampling)


def describe_pattern_count(mode_count: Any, photons: Any) -> str:
    try:
        count = pattern_count(
            form_whole_number(mode_count, "Vyber počet světlovodů."), form_whole_number(photons, "Vyber počet fotonů."),
        )
    except ChipError as error:
        return str(error)
    if count > MAX_PATTERNS:
        return f"{czech_count(count)} výstupních vzorů, víc než {czech_count(MAX_PATTERNS)}, které simulátor spočítá."
    return f"{czech_count(count)} možných výstupních vzorů."


def run_boson_sampling(_clicks: Optional[int], form: Dict[str, Any]) -> dict:
    try:
        sampling_form = parse_sampling_form(form)
        study = _run_study(sampling_form)
    except ChipError as error:
        return dict(results=None, error=str(error))
    return dict(results=build_sampling_results(study), error="")


def parse_sampling_form(form: Dict[str, Any]) -> SamplingForm:
    try:
        target = ChipTarget(form["target"])
        kind = PhotonKind(form["kind"])
    except ValueError as error:
        raise ChipError("Vyber interferometr a druh fotonů ze seznamu.") from error
    return SamplingForm(
        mode_count=form_whole_number(form["mode_count"], "Vyber počet světlovodů ze seznamu."),
        photons=form_whole_number(form["photons"], "Vyber počet fotonů ze seznamu."),
        target=target,
        split_spread=form_number(form["split_spread"], "Vyber čip ze seznamu."),
        kind=kind,
        shots=form_whole_number(form["shots"], "Vyber počet výstřelů ze seznamu."),
        seed=form_whole_number(form["seed"], "Seed musí být celé číslo."),
    )


def _run_study(form: SamplingForm) -> SamplingStudy:
    logger.info(
        "Boson sampling on the chip: modes=%d photons=%d shots=%d kind=%s spread=%.2f",
        form.mode_count, form.photons, form.shots, form.kind.value, form.split_spread,
    )
    return run_sampling_study(
        form.target, form.split_spread, form.seed, form.mode_count, form.photons, form.kind, form.shots,
    )
