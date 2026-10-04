from __future__ import annotations

import logging
from typing import List, Optional, Tuple

import pandas as pd
from dash import Dash, Input, Output, State, dcc, no_update

from montecarlo.charts import stress_scenario_chart
from montecarlo.historical_returns import AssetClass
from montecarlo.portfolio import PortfolioValidationError
from montecarlo.scenarios import ScenarioValidationError, StressScenario, portfolio_return
from montecarlo.simulation import SimulationParametersError, simulate
from ui import ids
from ui.components import ASSET_CLASS_LABELS
from ui.form_parsing import (
    CORRELATION_ROW_LABEL_COLUMN,
    EMPTY_ASSET_ROW,
    Row,
    asset_names,
    build_parameters,
    build_portfolio,
    build_scenario_holdings,
    build_scenarios,
    default_correlation_rows,
    has_valid_names,
    optional_amount,
    weight_sum_percent,
)
from ui.market_presets import (
    add_predefined_asset,
    apply_preset,
    find_predefined_asset,
    find_preset,
    preset_summary,
    slider_correlation,
)
from ui.navigation import HIDDEN, VISIBLE
from ui.portfolio_page import CORRELATION_SLIDER, correlation_table_columns
from ui.results import build_results, format_money
from ui.stress_scenarios import custom_scenario_row

WEIGHT_SUM_TARGET = 100.0
WEIGHT_SUM_TOLERANCE = 1e-6
CSV_FILE_NAME = "monte_carlo_final_values.csv"
PERCENT = 100

logger = logging.getLogger(__name__)


def register_callbacks(app: Dash) -> None:
    app.callback(
        Output(ids.ASSET_TABLE, "data"),
        Input(ids.ADD_ASSET_BUTTON, "n_clicks"),
        State(ids.ASSET_TABLE, "data"),
        prevent_initial_call=True,
    )(add_asset_row)

    app.callback(
        Output(ids.ASSET_TABLE, "data", allow_duplicate=True),
        Output(ids.PAIRWISE_CORRELATION_SLIDER, "value"),
        Output(ids.MARKET_PRESET_SUMMARY, "children"),
        Input(ids.MARKET_PRESET_DROPDOWN, "value"),
        State(ids.ASSET_TABLE, "data"),
        prevent_initial_call=True,
    )(apply_market_preset)

    app.callback(
        Output(ids.ASSET_TABLE, "data", allow_duplicate=True),
        Output(ids.PREDEFINED_ASSET_DROPDOWN, "value"),
        Input(ids.PREDEFINED_ASSET_DROPDOWN, "value"),
        State(ids.ASSET_TABLE, "data"),
        prevent_initial_call=True,
    )(add_selected_asset)

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
        Output(ids.DOWNLOAD_BUTTON, "style"),
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
        Output(ids.STRESS_SCENARIO_TABLE, "data"),
        Input(ids.ADD_STRESS_SCENARIO_BUTTON, "n_clicks"),
        State(ids.STRESS_SCENARIO_TABLE, "data"),
        prevent_initial_call=True,
    )(add_stress_scenario_row)

    app.callback(
        Output(ids.STRESS_SCENARIO_CHART, "figure"),
        Output(ids.STRESS_SCENARIO_MESSAGE, "children"),
        Input(ids.ASSET_TABLE, "data"),
        Input(ids.STRESS_SCENARIO_TABLE, "data"),
        Input(ids.INITIAL_VALUE_INPUT, "value"),
    )(describe_stress_scenarios)

    app.callback(
        Output(ids.DOWNLOAD, "data"),
        Input(ids.DOWNLOAD_BUTTON, "n_clicks"),
        State(ids.FINAL_VALUES_STORE, "data"),
        prevent_initial_call=True,
    )(download_final_values)


def add_asset_row(_clicks: int, asset_rows: List[Row]) -> List[Row]:
    return asset_rows + [dict(EMPTY_ASSET_ROW)]


def apply_market_preset(preset_key: str, asset_rows: List[Row]) -> Tuple[List[Row], float, str]:
    preset = find_preset(preset_key)
    correlation = slider_correlation(preset, asset_rows, CORRELATION_SLIDER)
    return apply_preset(asset_rows, preset), correlation, preset_summary(preset, asset_rows, correlation)


def add_selected_asset(asset_name: Optional[str], asset_rows: List[Row]):
    """Clearing the dropdown afterwards lets the same asset be picked again."""
    if not asset_name:
        return no_update, no_update
    return add_predefined_asset(asset_rows, find_predefined_asset(asset_name)), None


def add_stress_scenario_row(_clicks: int, scenario_rows: List[Row]) -> List[Row]:
    return scenario_rows + [custom_scenario_row(len(scenario_rows))]


def describe_stress_scenarios(asset_rows: List[Row], scenario_rows: List[Row], initial_value: Optional[float]):
    try:
        weights, asset_classes = build_scenario_holdings(asset_rows)
        scenarios = build_scenarios(scenario_rows)
    except (PortfolioValidationError, ScenarioValidationError) as error:
        return no_update, str(error)

    returns = [portfolio_return(weights, asset_classes, scenario) for scenario in scenarios]
    amount = optional_amount(initial_value)
    figure = stress_scenario_chart(
        [scenario.name for scenario in scenarios],
        returns,
        [_scenario_bar_text(scenario_return, amount) for scenario_return in returns],
        [_scenario_hover_text(scenario) for scenario in scenarios],
    )
    return figure, ""


def _scenario_bar_text(scenario_return: float, amount: Optional[float]) -> str:
    percent = f"{scenario_return * PERCENT:+.1f} %"
    return f"{percent} ({format_money(scenario_return * amount)} Kč)" if amount else percent


def _scenario_hover_text(scenario: StressScenario) -> str:
    class_returns = ", ".join(
        f"{ASSET_CLASS_LABELS[asset_class].lower()} {scenario.returns[asset_class] * PERCENT:+.1f} %"
        for asset_class in AssetClass
    )
    return "<br>".join(part for part in (f"<b>{scenario.name}</b>", scenario.description, class_returns) if part)


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
        return None, None, str(error), HIDDEN

    logger.info(
        "Running simulation: assets=%d years=%d simulations=%d",
        len(portfolio.assets), parameters.years, parameters.simulation_count,
    )
    result = simulate(portfolio, parameters)
    return build_results(result), result.final_values.tolist(), "", VISIBLE


def download_final_values(_clicks: int, final_values: Optional[List[float]]):
    if not final_values:
        return no_update
    frame = pd.DataFrame({"final_value": final_values})
    return dcc.send_data_frame(frame.to_csv, CSV_FILE_NAME, index_label="simulation")
