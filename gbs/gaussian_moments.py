"""Exact Gaussian moments E[x^n] for x ~ N(0, Σ) and every exponent pattern n up to a bound."""

from __future__ import annotations

from math import prod
from typing import Sequence

import numpy as np


def moment_table_size(max_exponents: Sequence[int]) -> int:
    return prod(int(exponent) + 1 for exponent in max_exponents)


def moment_table(covariance: np.ndarray, max_exponents: Sequence[int]) -> np.ndarray:
    """Array M with M[n] = E[x^n] = Haf(Σ_n) for all patterns n ≤ max_exponents (componentwise).

    Stein's lemma E[x_m·g(x)] = Σ_b Σ_mb·E[∂_b g(x)] peels off one factor of the last variable:
    M[n, j] = Σ_b Σ_mb·n_b·M[n − e_b, j − 1] + Σ_mm·(j − 1)·M[n, j − 2]. Every slice along the last axis is
    therefore a vectorised update of the two previous slices, and the work grows with the table size
    Π(n_i + 1) instead of with the number of perfect matchings.
    """
    if len(max_exponents) == 0:
        return np.array(1.0)
    lower = moment_table(covariance[:-1, :-1], max_exponents[:-1])
    last_power = int(max_exponents[-1])
    table = np.zeros(lower.shape + (last_power + 1,))
    table[..., 0] = lower
    for power in range(1, last_power + 1):
        current = np.zeros(lower.shape)
        for other in range(lower.ndim):
            current += covariance[-1, other] * _shifted_times_index(table[..., power - 1], axis=other)
        if power >= 2:
            current += covariance[-1, -1] * (power - 1) * table[..., power - 2]
        table[..., power] = current
    return table


def _shifted_times_index(values: np.ndarray, axis: int) -> np.ndarray:
    """T[n] = n_axis · values[n − e_axis], zero where n_axis = 0."""
    shifted = np.zeros_like(values)
    target = [slice(None)] * values.ndim
    source = [slice(None)] * values.ndim
    target[axis] = slice(1, None)
    source[axis] = slice(None, -1)
    shifted[tuple(target)] = values[tuple(source)]
    index_shape = [1] * values.ndim
    index_shape[axis] = values.shape[axis]
    return shifted * np.arange(values.shape[axis]).reshape(index_shape)
