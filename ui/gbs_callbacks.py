from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from dash import Dash, Input, Output, State, ctx, no_update

from gbs.demo import DemoParametersError, run_gbs_demo
from gbs.expectation import MomentProblem, MomentProblemError
from gbs.sampler import GbsProgramError
from montecarlo.portfolio import PortfolioValidationError
from montecarlo.simulation import SimulationParametersError
from ui import ids
from ui.form_parsing import build_portfolio, parse_seed
from ui.gbs_results import build_gbs_results
from ui.navigation import GBS_PATH

logger = logging.getLogger(__name__)

EXPECTED_INPUT_ERRORS = (
    PortfolioValidationError,
    SimulationParametersError,
    GbsProgramError,
    MomentProblemError,
    DemoParametersError,
)


def register_gbs_callbacks(app: Dash) -> None:
    app.callback(
        output=dict(results=Output(ids.GBS_RESULTS, "children"), error=Output(ids.GBS_ERROR_MESSAGE, "children")),
        inputs=dict(
            _clicks=Input(ids.GBS_RUN_BUTTON, "n_clicks"),
            pathname=Input(ids.URL, "pathname"),
        ),
        state=dict(
            current_results=State(ids.GBS_RESULTS, "children"),
            form=dict(
                asset_rows=State(ids.ASSET_TABLE, "data"),
                correlation_rows=State(ids.CORRELATION_TABLE, "data"),
                degree=State(ids.GBS_DEGREE_RADIO, "value"),
                squeezing_strength=State(ids.GBS_STRENGTH_SLIDER, "value"),
                max_sample_size=State(ids.GBS_MAX_SHOTS_DROPDOWN, "value"),
                seed=State(ids.GBS_SEED_DROPDOWN, "value"),
            ),
        ),
    )(run_gbs_simulation)


def run_gbs_simulation(_clicks: Optional[int], pathname: str, current_results: Any, form: Dict[str, Any]) -> dict:
    if not should_run(ctx.triggered_id, pathname, current_results):
        return dict(results=no_update, error=no_update)

    try:
        portfolio = build_portfolio(form["asset_rows"], form["correlation_rows"])
        problem = MomentProblem(
            covariance=portfolio.covariance(), weights=portfolio.weights, degree=int(form["degree"])
        )
        seed = parse_seed(form["seed"])
    except EXPECTED_INPUT_ERRORS as error:
        return dict(results=None, error=str(error))

    logger.info(
        "Running GBS demo: modes=%d degree=%d strength=%s max_samples=%s",
        len(portfolio.assets), problem.degree, form["squeezing_strength"], form["max_sample_size"],
    )
    try:
        run = run_gbs_demo(problem, float(form["squeezing_strength"]), int(form["max_sample_size"]), seed)
    except EXPECTED_INPUT_ERRORS as error:
        return dict(results=None, error=str(error))
    return dict(results=build_gbs_results(run, [asset.name for asset in portfolio.assets]), error="")


def should_run(triggered_id: Optional[str], pathname: str, current_results: Any) -> bool:
    """Runs on an explicit click, or automatically the first time the GBS page is shown."""
    if triggered_id == ids.GBS_RUN_BUTTON:
        return True
    return pathname == GBS_PATH and not current_results
