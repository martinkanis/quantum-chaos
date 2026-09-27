from __future__ import annotations

from typing import List, Sequence, Tuple

import numpy as np


def hafnian(matrix: np.ndarray) -> float:
    """Sum over all perfect matchings of the product of matched entries.

    Exponential in the matrix size; intended for the small matrices (≤ 10 rows) of this demo.
    """
    size = matrix.shape[0]
    if size % 2:
        return 0.0
    return _hafnian_of_indices(matrix.tolist(), tuple(range(size)))


def repeated_submatrix(matrix: np.ndarray, pattern: Sequence[int]) -> np.ndarray:
    """Matrix with row/column i repeated pattern[i] times (the A_n of GBS literature)."""
    indices = np.repeat(np.arange(len(pattern)), pattern)
    return matrix[np.ix_(indices, indices)]


def _hafnian_of_indices(matrix: List[List[float]], indices: Tuple[int, ...]) -> float:
    if not indices:
        return 1.0
    first, rest = indices[0], indices[1:]
    total = 0.0
    for position, partner in enumerate(rest):
        remaining = rest[:position] + rest[position + 1:]
        total += matrix[first][partner] * _hafnian_of_indices(matrix, remaining)
    return total
