"""Callbacks of page 3: the matrix table, the lab run and the Qiskit download."""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Tuple

from dash import Dash, Input, Output, State, ctx, dcc, no_update

from gbs.advantage_lab import run_lab
from gbs.benchmark_problems import find_benchmark
from gbs.demo import DemoParametersError
from gbs.monomial_problem import MonomialProblem, MonomialProblemError
from gbs.photon_tuning import TuningError, TuningMode
from gbs.qiskit_export import SCRIPT_FILE_NAME, QiskitExportError, QubitEmulation, build_qiskit_script, emulation_for
from montecarlo.simulation import SimulationParametersError
from ui import ids
from ui.advantage_form import (
    Row,
    build_monomial_problem,
    matrix_columns,
    matrix_rows,
    parse_tuning_mode,
    resized_rows,
    symmetrized_rows,
)
from ui.advantage_results import build_advantage_results
from ui.form_parsing import parse_seed
from ui.navigation import ADVANTAGE_PATH

logger = logging.getLogger(__name__)

EXPECTED_INPUT_ERRORS = (MonomialProblemError, TuningError, DemoParametersError, SimulationParametersError)


def register_advantage_callbacks(app: Dash) -> None:
    app.callback(
        Output(ids.ADVANTAGE_MATRIX_TABLE, "data", allow_duplicate=True),
        Output(ids.ADVANTAGE_VARIABLE_COUNT_DROPDOWN, "value"),
        Output(ids.ADVANTAGE_PROBLEM_DESCRIPTION, "children"),
        Input(ids.ADVANTAGE_PROBLEM_DROPDOWN, "value"),
        prevent_initial_call=True,
    )(apply_benchmark)

    app.callback(
        Output(ids.ADVANTAGE_MATRIX_TABLE, "data", allow_duplicate=True),
        Input(ids.ADVANTAGE_VARIABLE_COUNT_DROPDOWN, "value"),
        State(ids.ADVANTAGE_MATRIX_TABLE, "data"),
        prevent_initial_call=True,
    )(resize_matrix)

    app.callback(
        Output(ids.ADVANTAGE_MATRIX_TABLE, "data"),
        Output(ids.ADVANTAGE_MATRIX_TABLE, "columns"),
        Input(ids.ADVANTAGE_MATRIX_TABLE, "data"),
        State(ids.ADVANTAGE_MATRIX_TABLE, "data_previous"),
        State(ids.ADVANTAGE_MATRIX_TABLE, "columns"),
        prevent_initial_call=True,
    )(normalize_matrix_table)

    app.callback(
        output=dict(
            results=Output(ids.ADVANTAGE_RESULTS, "children"), error=Output(ids.ADVANTAGE_ERROR_MESSAGE, "children"),
        ),
        inputs=dict(_clicks=Input(ids.ADVANTAGE_RUN_BUTTON, "n_clicks"), pathname=Input(ids.URL, "pathname")),
        state=dict(
            current_results=State(ids.ADVANTAGE_RESULTS, "children"),
            form=dict(
                rows=State(ids.ADVANTAGE_MATRIX_TABLE, "data"),
                tuning=State(ids.ADVANTAGE_TUNING_RADIO, "value"),
                max_sample_size=State(ids.ADVANTAGE_MAX_SHOTS_DROPDOWN, "value"),
                seed=State(ids.ADVANTAGE_SEED_DROPDOWN, "value"),
            ),
        ),
    )(run_advantage_lab)

    app.callback(
        Output(ids.QISKIT_DOWNLOAD, "data"),
        Output(ids.QISKIT_DOWNLOAD_MESSAGE, "children"),
        Input(ids.QISKIT_DOWNLOAD_BUTTON, "n_clicks"),
        State(ids.ADVANTAGE_MATRIX_TABLE, "data"),
        State(ids.ADVANTAGE_TUNING_RADIO, "value"),
        State(ids.ADVANTAGE_SEED_DROPDOWN, "value"),
        prevent_initial_call=True,
    )(download_qiskit_script)


def apply_benchmark(benchmark_key: str):
    try:
        benchmark = find_benchmark(benchmark_key)
    except KeyError:
        logger.warning("Unknown benchmark problem selected: %s", benchmark_key)
        return no_update, no_update, no_update
    rows = matrix_rows(benchmark.problem)
    return rows, len(rows), benchmark.description


def resize_matrix(variable_count: int, rows: List[Row]):
    if not rows or variable_count == len(rows):
        return no_update
    return resized_rows(rows, int(variable_count))


def normalize_matrix_table(rows: List[Row], previous_rows: Optional[List[Row]], columns: List[dict]):
    """Mirrors edits across the diagonal and keeps the column headers in step with the variable names."""
    symmetric = symmetrized_rows(rows, previous_rows)
    new_columns = matrix_columns(rows)
    return (
        no_update if symmetric is None else symmetric,
        no_update if new_columns == columns else new_columns,
    )


def run_advantage_lab(_clicks: Optional[int], pathname: str, current_results: Any, form: Dict[str, Any]) -> dict:
    if not should_run_lab(ctx.triggered_id, pathname, current_results):
        return dict(results=no_update, error=no_update)

    try:
        problem = build_monomial_problem(form["rows"])
        mode = parse_tuning_mode(form["tuning"])
        logger.info(
            "Running advantage lab: variables=%d degree=%d tuning=%s max_samples=%s",
            len(problem.exponents), problem.degree, mode.value, form["max_sample_size"],
        )
        run = run_lab(problem, mode, int(form["max_sample_size"]), parse_seed(form["seed"]))
    except EXPECTED_INPUT_ERRORS as error:
        return dict(results=None, error=str(error))
    emulation, emulation_error = _emulation_plan(problem, mode)
    return dict(results=build_advantage_results(run, emulation, emulation_error), error="")


def download_qiskit_script(_clicks: int, rows: List[Row], tuning: str, seed: Any):
    try:
        script = build_qiskit_script(build_monomial_problem(rows), parse_tuning_mode(tuning), parse_seed(seed))
    except (*EXPECTED_INPUT_ERRORS, QiskitExportError) as error:
        return no_update, str(error)
    return (
        dcc.send_string(script, SCRIPT_FILE_NAME),
        f"Staženo: {SCRIPT_FILE_NAME}. Spusť ho příkazem python {SCRIPT_FILE_NAME}.",
    )


def should_run_lab(triggered_id: Optional[str], pathname: str, current_results: Any) -> bool:
    """Runs on an explicit click, or automatically the first time page 3 is shown."""
    if triggered_id == ids.ADVANTAGE_RUN_BUTTON:
        return True
    return pathname == ADVANTAGE_PATH and not current_results


def _emulation_plan(problem: MonomialProblem, mode: TuningMode) -> Tuple[Optional[QubitEmulation], str]:
    try:
        return emulation_for(problem, mode), ""
    except (QiskitExportError, TuningError) as error:
        return None, str(error)
