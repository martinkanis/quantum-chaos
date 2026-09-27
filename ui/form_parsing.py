"""Converts raw values from the web form into validated domain objects."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import numpy as np

from montecarlo.portfolio import Asset, Portfolio, PortfolioValidationError, uniform_correlation
from montecarlo.simulation import SimulationParameters, SimulationParametersError

PERCENT = 100

NAME_COLUMN = "name"
WEIGHT_COLUMN = "weight"
RETURN_COLUMN = "expected_return"
VOLATILITY_COLUMN = "volatility"
CORRELATION_ROW_LABEL_COLUMN = "asset"
RANDOM_SEED = "random"

Row = Dict[str, Any]

DEFAULT_ASSET_ROWS: List[Row] = [
    {NAME_COLUMN: "Akcie svět", WEIGHT_COLUMN: 60, RETURN_COLUMN: 7, VOLATILITY_COLUMN: 16},
    {NAME_COLUMN: "Dluhopisy", WEIGHT_COLUMN: 30, RETURN_COLUMN: 3, VOLATILITY_COLUMN: 5},
    {NAME_COLUMN: "Zlato", WEIGHT_COLUMN: 10, RETURN_COLUMN: 4, VOLATILITY_COLUMN: 15},
]
EMPTY_ASSET_ROW: Row = {NAME_COLUMN: "", WEIGHT_COLUMN: 0, RETURN_COLUMN: 5, VOLATILITY_COLUMN: 10}


def asset_names(asset_rows: List[Row]) -> List[str]:
    return [str(row.get(NAME_COLUMN) or "").strip() for row in asset_rows]


def has_valid_names(names: List[str]) -> bool:
    return bool(names) and all(names) and len(set(names)) == len(names)


def weight_sum_percent(asset_rows: List[Row]) -> float:
    return sum(_as_number(row.get(WEIGHT_COLUMN)) or 0.0 for row in asset_rows)


def correlation_column_id(index: int) -> str:
    return f"asset_{index}"


def default_correlation_rows(names: List[str], pairwise_correlation: float) -> List[Row]:
    matrix = uniform_correlation(len(names), pairwise_correlation)
    return [
        {
            CORRELATION_ROW_LABEL_COLUMN: name,
            **{correlation_column_id(column): matrix[row, column] for column in range(len(names))},
        }
        for row, name in enumerate(names)
    ]


def build_portfolio(asset_rows: List[Row], correlation_rows: List[Row]) -> Portfolio:
    names = asset_names(asset_rows)
    if not has_valid_names(names):
        raise PortfolioValidationError("Každé aktivum musí mít vyplněný a unikátní název.")
    assets = tuple(_build_asset(name, row) for name, row in zip(names, asset_rows))
    correlation = _correlation_matrix(correlation_rows, asset_count=len(assets))
    return Portfolio(assets=assets, correlation=correlation)


def build_parameters(
    initial_value: Any, monthly_contribution: Any, years: Any, simulation_count: Any, seed: Any
) -> SimulationParameters:
    return SimulationParameters(
        initial_value=_required_parameter(initial_value, "Počáteční investice"),
        monthly_contribution=_required_parameter(monthly_contribution, "Měsíční vklad"),
        years=int(_required_parameter(years, "Investiční horizont")),
        simulation_count=int(_required_parameter(simulation_count, "Počet simulací")),
        seed=parse_seed(seed),
    )


def _build_asset(name: str, row: Row) -> Asset:
    label = name or "bez názvu"
    return Asset(
        name=name,
        weight=_required_asset_value(row, WEIGHT_COLUMN, label) / PERCENT,
        expected_return=_required_asset_value(row, RETURN_COLUMN, label) / PERCENT,
        volatility=_required_asset_value(row, VOLATILITY_COLUMN, label) / PERCENT,
    )


def _correlation_matrix(correlation_rows: List[Row], asset_count: int) -> np.ndarray:
    """Builds a symmetric matrix from the upper triangle, so users edit each pair only once."""
    if len(correlation_rows) != asset_count:
        raise PortfolioValidationError("Korelační matice neodpovídá aktivům — oprav názvy aktiv.")

    matrix = np.eye(asset_count)
    for row in range(asset_count):
        for column in range(row + 1, asset_count):
            value = _as_number(correlation_rows[row].get(correlation_column_id(column)))
            if value is None:
                raise PortfolioValidationError("Všechny korelace nad diagonálou musí být čísla.")
            matrix[row, column] = matrix[column, row] = value
    return matrix


def _required_asset_value(row: Row, column: str, asset_label: str) -> float:
    value = _as_number(row.get(column))
    if value is None:
        raise PortfolioValidationError(
            f"Aktivum '{asset_label}' nemá vyplněnou váhu, výnos nebo volatilitu."
        )
    return value


def _required_parameter(value: Any, label: str) -> float:
    number = _as_number(value)
    if number is None:
        raise SimulationParametersError(f"Parametr '{label}' musí být číslo.")
    return number


def parse_seed(value: Any) -> Optional[int]:
    """None means a fresh random seed on every run."""
    if value is None or value == "" or value == RANDOM_SEED:
        return None
    number = _as_number(value)
    if number is None or number < 0 or not float(number).is_integer():
        raise SimulationParametersError("Seed musí být nezáporné celé číslo, nebo prázdný.")
    return int(number)


def _as_number(value: Any) -> Optional[float]:
    if isinstance(value, bool):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if np.isfinite(number) else None
