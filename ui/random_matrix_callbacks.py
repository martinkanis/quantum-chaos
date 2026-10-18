"""Callback of the random matrix page: simulate the market and show the spectrum and the portfolio risks."""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from dash import Dash, Input, Output, State, ctx, no_update

from montecarlo.simulation import SimulationParametersError
from randommatrix.factor_market import FactorMarket, FactorMarketError
from randommatrix.study import run_study
from ui import ids
from ui.form_parsing import parse_seed
from ui.navigation import RANDOM_MATRIX_PATH
from ui.random_matrix_results import build_random_matrix_results

logger = logging.getLogger(__name__)

EXPECTED_INPUT_ERRORS = (FactorMarketError, SimulationParametersError)


def register_random_matrix_callbacks(app: Dash) -> None:
    app.callback(
        output=dict(
            results=Output(ids.RANDOM_MATRIX_RESULTS, "children"),
            error=Output(ids.RANDOM_MATRIX_ERROR_MESSAGE, "children"),
        ),
        inputs=dict(_clicks=Input(ids.RANDOM_MATRIX_RUN_BUTTON, "n_clicks"), pathname=Input(ids.URL, "pathname")),
        state=dict(
            current_results=State(ids.RANDOM_MATRIX_RESULTS, "children"),
            form=dict(
                asset_count=State(ids.RANDOM_MATRIX_ASSET_COUNT_DROPDOWN, "value"),
                observation_count=State(ids.RANDOM_MATRIX_OBSERVATION_COUNT_DROPDOWN, "value"),
                seed=State(ids.RANDOM_MATRIX_SEED_DROPDOWN, "value"),
            ),
        ),
    )(run_random_matrix_lab)


def run_random_matrix_lab(_clicks: Optional[int], pathname: str, current_results: Any, form: Dict[str, Any]) -> dict:
    if not should_run_lab(ctx.triggered_id, pathname, current_results):
        return dict(results=no_update, error=no_update)

    asset_count = int(form["asset_count"])
    observation_count = int(form["observation_count"])
    logger.info("Running random matrix lab: assets=%d observations=%d", asset_count, observation_count)
    try:
        study = run_study(FactorMarket(asset_count), observation_count, parse_seed(form["seed"]))
    except EXPECTED_INPUT_ERRORS as error:
        return dict(results=None, error=str(error))
    return dict(results=build_random_matrix_results(study), error="")


def should_run_lab(triggered_id: Optional[str], pathname: str, current_results: Any) -> bool:
    """Runs on an explicit click, or automatically the first time the page is shown."""
    if triggered_id == ids.RANDOM_MATRIX_RUN_BUTTON:
        return True
    return pathname == RANDOM_MATRIX_PATH and not current_results
