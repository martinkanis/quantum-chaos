"""Callbacks of the photon loss page: the description of the chosen problem and the lab run."""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from dash import Dash, Input, Output, State, ctx, no_update

from gbs.benchmark_problems import find_benchmark
from gbs.loss_study import run_loss_study
from gbs.monomial_problem import MonomialProblemError
from gbs.photon_loss import PhotonLossError
from gbs.photon_tuning import TuningError
from ui import ids
from ui.advantage_form import parse_tuning_mode
from ui.navigation import PHOTON_LOSS_PATH
from ui.photon_loss_content import PERCENT, typical_bench_transmission
from ui.photon_loss_results import build_photon_loss_results

logger = logging.getLogger(__name__)

EXPECTED_INPUT_ERRORS = (MonomialProblemError, TuningError, PhotonLossError)


def register_photon_loss_callbacks(app: Dash) -> None:
    app.callback(
        Output(ids.PHOTON_LOSS_PROBLEM_DESCRIPTION, "children"),
        Input(ids.PHOTON_LOSS_PROBLEM_DROPDOWN, "value"),
        prevent_initial_call=True,
    )(describe_problem)

    app.callback(
        output=dict(
            results=Output(ids.PHOTON_LOSS_RESULTS, "children"),
            error=Output(ids.PHOTON_LOSS_ERROR_MESSAGE, "children"),
        ),
        inputs=dict(_clicks=Input(ids.PHOTON_LOSS_RUN_BUTTON, "n_clicks"), pathname=Input(ids.URL, "pathname")),
        state=dict(
            current_results=State(ids.PHOTON_LOSS_RESULTS, "children"),
            form=dict(
                problem=State(ids.PHOTON_LOSS_PROBLEM_DROPDOWN, "value"),
                tuning=State(ids.PHOTON_LOSS_TUNING_RADIO, "value"),
                transmission_percent=State(ids.PHOTON_LOSS_TRANSMISSION_SLIDER, "value"),
            ),
        ),
    )(run_photon_loss_lab)


def describe_problem(benchmark_key: str):
    try:
        return find_benchmark(benchmark_key).description
    except KeyError:
        logger.warning("Unknown benchmark problem selected: %s", benchmark_key)
        return no_update


def run_photon_loss_lab(_clicks: Optional[int], pathname: str, current_results: Any, form: Dict[str, Any]) -> dict:
    if not should_run_lab(ctx.triggered_id, pathname, current_results):
        return dict(results=no_update, error=no_update)
    try:
        benchmark = find_benchmark(form["problem"])
        mode = parse_tuning_mode(form["tuning"])
        transmission = parse_transmission(form["transmission_percent"])
        logger.info(
            "Running photon loss lab: problem=%s tuning=%s transmission=%.3f", benchmark.key, mode.value, transmission,
        )
        study = run_loss_study(benchmark.problem, mode, transmission)
    except KeyError:
        return dict(results=None, error="Vyber jednu z připravených úloh.")
    except EXPECTED_INPUT_ERRORS as error:
        return dict(results=None, error=str(error))
    bench_transmission = typical_bench_transmission(len(study.exponents))
    return dict(results=build_photon_loss_results(study, bench_transmission), error="")


def parse_transmission(percent: Any) -> float:
    try:
        return float(percent) / PERCENT
    except (TypeError, ValueError) as error:
        raise PhotonLossError("Nastav propustnost posuvníkem.") from error


def should_run_lab(triggered_id: Optional[str], pathname: str, current_results: Any) -> bool:
    """Runs on an explicit click, or automatically the first time the page is shown."""
    if triggered_id == ids.PHOTON_LOSS_RUN_BUTTON:
        return True
    return pathname == PHOTON_LOSS_PATH and not current_results
