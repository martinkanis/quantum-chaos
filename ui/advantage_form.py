"""Matrix table of the advantage lab: one row per variable with its name, exponent and row of Σ."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Set, Tuple

import numpy as np

from gbs.monomial_problem import MonomialProblem, MonomialProblemError
from gbs.photon_tuning import TuningMode

VARIABLE_COLUMN = "variable"
EXPONENT_COLUMN = "exponent"
DEFAULT_NEW_EXPONENT = 2

Row = Dict[str, Any]
Cell = Tuple[int, int]


def covariance_column_id(index: int) -> str:
    return f"sigma_{index}"


def matrix_rows(problem: MonomialProblem) -> List[Row]:
    return [
        {
            VARIABLE_COLUMN: name,
            EXPONENT_COLUMN: power,
            **{covariance_column_id(column): float(value) for column, value in enumerate(problem.covariance[row])},
        }
        for row, (name, power) in enumerate(zip(problem.variable_names, problem.exponents))
    ]


def matrix_columns(rows: List[Row]) -> List[dict]:
    names = variable_names(rows)
    return [
        {"id": VARIABLE_COLUMN, "name": "Proměnná", "type": "text"},
        {"id": EXPONENT_COLUMN, "name": "Exponent", "type": "numeric"},
    ] + [
        {"id": covariance_column_id(index), "name": f"Σ · {name}", "type": "numeric"}
        for index, name in enumerate(names)
    ]


def variable_names(rows: List[Row]) -> List[str]:
    return [str(row.get(VARIABLE_COLUMN) or "").strip() or f"X{index + 1}" for index, row in enumerate(rows)]


def resized_rows(rows: List[Row], count: int) -> List[Row]:
    """Keeps the entries of the remaining variables; a new variable starts uncorrelated with unit variance."""
    resized = [_trimmed_row(row, count) for row in rows[:count]]
    for index in range(len(resized), count):
        new_row: Row = {VARIABLE_COLUMN: f"X{index + 1}", EXPONENT_COLUMN: DEFAULT_NEW_EXPONENT}
        new_row.update({covariance_column_id(column): 0.0 for column in range(count)})
        new_row[covariance_column_id(index)] = 1.0
        for other in resized:
            other[covariance_column_id(index)] = 0.0
        resized.append(new_row)
    return resized


def symmetrized_rows(rows: List[Row], previous_rows: Optional[List[Row]]) -> Optional[List[Row]]:
    """Copies every edited off-diagonal entry to its mirror cell; None when the matrix is already symmetric.

    Without a previous version (e.g. a freshly loaded table) the upper triangle wins.
    """
    size = len(rows)
    edited = _edited_cells(rows, previous_rows) if previous_rows and len(previous_rows) == size else None
    symmetric = [dict(row) for row in rows]
    changed = False
    for row in range(size):
        for column in range(size):
            if row == column:
                continue
            source_row, source_column = _mirror_source(row, column, edited)
            value = rows[source_row].get(covariance_column_id(source_column))
            if symmetric[row].get(covariance_column_id(column)) != value:
                symmetric[row][covariance_column_id(column)] = value
                changed = True
    return symmetric if changed else None


def build_monomial_problem(rows: List[Row]) -> MonomialProblem:
    names = tuple(variable_names(rows))
    if len(set(names)) != len(names):
        raise MonomialProblemError("Názvy proměnných musí být unikátní.")
    exponents = tuple(_exponent(row, name) for row, name in zip(rows, names))
    return MonomialProblem(covariance=_covariance(rows), exponents=exponents, variable_names=names)


def parse_tuning_mode(value: Any) -> TuningMode:
    try:
        return TuningMode(value)
    except ValueError as error:
        raise MonomialProblemError(f"Neznámé nastavení stlačení: {value}.") from error


def _trimmed_row(row: Row, count: int) -> Row:
    trimmed = {VARIABLE_COLUMN: row.get(VARIABLE_COLUMN), EXPONENT_COLUMN: row.get(EXPONENT_COLUMN)}
    trimmed.update({covariance_column_id(column): row.get(covariance_column_id(column)) for column in range(count)})
    return trimmed


def _edited_cells(rows: List[Row], previous_rows: List[Row]) -> Set[Cell]:
    size = len(rows)
    return {
        (row, column)
        for row in range(size)
        for column in range(size)
        if rows[row].get(covariance_column_id(column)) != previous_rows[row].get(covariance_column_id(column))
    }


def _mirror_source(row: int, column: int, edited: Optional[Set[Cell]]) -> Cell:
    """The cell whose value both mirror cells should hold: the edited one, otherwise the upper triangle."""
    if edited is not None and (row, column) in edited and (column, row) not in edited:
        return row, column
    if edited is not None and (column, row) in edited and (row, column) not in edited:
        return column, row
    return (row, column) if row < column else (column, row)


def _exponent(row: Row, name: str) -> int:
    value = _number(row.get(EXPONENT_COLUMN))
    if value is None or not float(value).is_integer():
        raise MonomialProblemError(f"Exponent proměnné '{name}' musí být celé číslo.")
    return int(value)


def _covariance(rows: List[Row]) -> np.ndarray:
    """Built from the diagonal and the upper triangle, so a half-finished edit cannot make it asymmetric."""
    size = len(rows)
    matrix = np.zeros((size, size))
    for row in range(size):
        for column in range(row, size):
            value = _number(rows[row].get(covariance_column_id(column)))
            if value is None:
                raise MonomialProblemError("Vyplň všechny prvky matice na diagonále a nad ní.")
            matrix[row, column] = matrix[column, row] = value
    return matrix


def _number(value: Any) -> Optional[float]:
    if isinstance(value, bool) or value is None or value == "":
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if np.isfinite(number) else None
