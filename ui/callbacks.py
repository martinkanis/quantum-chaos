from __future__ import annotations

import logging
from typing import List, Optional, Tuple

import pandas as pd
from dash import Dash, Input, Output, State, dcc, no_update

from montecarlo.portfolio import PortfolioValidationError
from montecarlo.simulation import SimulationParametersError, simulate
from ui import ids
from ui.form_parsing import (
    CORRELATION_ROW_LABEL_COLUMN,
    EMPTY_ASSET_ROW,
    Row,
    asset_names,
    build_parameters,
    build_portfolio,
    default_correlation_rows,
    has_valid_names,
    weight_sum_percent,
)
from ui.portfolio_page import correlation_table_columns
from ui.results import build_results

WEIGHT_SUM_TARGET = 100.0
WEIGHT_SUM_TOLERANCE = 1e-6
CSV_FILE_NAME = "monte_carlo_final_values.csv"

logger = logging.getLogger(__name__)


def register_callbacks(app: Dash) -> None:
    app.callback(
        Output(ids.ASSET_TABLE, "data"),
        Input(ids.ADD_ASSET_BUTTON, "n_clicks"),
        State(ids.ASSET_TABLE, "data"),
        prevent_initial_call=True,
    )(add_asset_row)

    app.callback(
        Output(ids.WEIGHT_SUM_TEXT, "children"),
        Output(ids.WEIGHT_SUM_TEXT, "className"),
        Input(ids.ASSET_TABLE, "data"),
    )(describe_weight_sum)

    app.callback(
        Output(ids.CORRELATION_TABLE, "data"),
        Output(ids.CORRELATION_TABLE, "columns"),
        Input(ids.ASSET_TABLE, "data"),
        Input(ids.PAIRWISE_CORRELATION_SLIDER, "value"),
    )(reset_correlation_table)

    app.callback(
        Output(ids.RESULTS, "children"),
        Output(ids.FINAL_VALUES_STORE, "data"),
        Output(ids.ERROR_MESSAGE, "children"),
        Input(ids.RUN_BUTTON, "n_clicks"),
        State(ids.ASSET_TABLE, "data"),
        State(ids.CORRELATION_TABLE, "data"),
        State(ids.INITIAL_VALUE_INPUT, "value"),
        State(ids.MONTHLY_CONTRIBUTION_INPUT, "value"),
        State(ids.YEARS_SLIDER, "value"),
        State(ids.SIMULATION_COUNT_SLIDER, "value"),
        State(ids.SEED_DROPDOWN, "value"),
        prevent_initial_call=True,
    )(run_simulation)

    app.callback(
        Output(ids.DOWNLOAD, "data"),
        Input(ids.DOWNLOAD_BUTTON, "n_clicks"),
        State(ids.FINAL_VALUES_STORE, "data"),
        prevent_initial_call=True,
    )(download_final_values)


def add_asset_row(_clicks: int, asset_rows: List[Row]) -> List[Row]:
    return asset_rows + [dict(EMPTY_ASSET_ROW)]


def describe_weight_sum(asset_rows: List[Row]) -> Tuple[str, str]:
    weight_sum = weight_sum_percent(asset_rows)
    is_complete = abs(weight_sum - WEIGHT_SUM_TARGET) < WEIGHT_SUM_TOLERANCE
    text = f"Součet vah: {weight_sum:.2f} % (musí být 100 %)"
    return text, "weight-sum ok" if is_complete else "weight-sum invalid"


def reset_correlation_table(asset_rows: List[Row], pairwise_correlation: float) -> Tuple[List[Row], List[dict]]:
    """Rebuilds the matrix whenever assets change; per-pair edits reset because the pairs changed."""
    names = asset_names(asset_rows)
    if not has_valid_names(names):
        return [], [{"id": CORRELATION_ROW_LABEL_COLUMN, "name": "Nejdřív vyplň unikátní názvy aktiv"}]

    return default_correlation_rows(names, pairwise_correlation), correlation_table_columns(names)


def run_simulation(
    _clicks: int,
    asset_rows: List[Row],
    correlation_rows: List[Row],
    initial_value: Optional[float],
    monthly_contribution: Optional[float],
    years: Optional[int],
    simulation_count: Optional[int],
    seed: Optional[float],
):
    try:
        parameters = build_parameters(initial_value, monthly_contribution, years, simulation_count, seed)
        portfolio = build_portfolio(asset_rows, correlation_rows)
    except (PortfolioValidationError, SimulationParametersError) as error:
        return None, None, str(error)

    logger.info(
        "Running simulation: assets=%d years=%d simulations=%d",
        len(portfolio.assets), parameters.years, parameters.simulation_count,
    )
    result = simulate(portfolio, parameters)
    return build_results(result), result.final_values.tolist(), ""


def download_final_values(_clicks: int, final_values: Optional[List[float]]):
    if not final_values:
        return no_update
    frame = pd.DataFrame({"final_value": final_values})
    return dcc.send_data_frame(frame.to_csv, CSV_FILE_NAME, index_label="simulation")
