from __future__ import annotations

from typing import Dict, Iterator, List, Sequence, Tuple

import numpy as np

MatrixEntry = Tuple[int, int]
EntryProduct = Tuple[MatrixEntry, ...]


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


def hafnian_expansion(pattern: Sequence[int]) -> Dict[EntryProduct, int]:
    """Haf(A_n) written out as products of entries of A, with equal products merged.

    Every perfect matching of the repeated indices picks one product: pattern (2, 2) repeats the indices as
    (0, 0, 1, 1) and gives A₀₀·A₁₁ once and A₀₁·A₀₁ twice. Keys are sorted index pairs, values multiplicities.
    """
    indices = tuple(int(index) for index in np.repeat(np.arange(len(pattern)), pattern))
    expansion: Dict[EntryProduct, int] = {}
    for matching in _perfect_matchings(indices):
        product = tuple(sorted(matching))
        expansion[product] = expansion.get(product, 0) + 1
    return expansion


def _perfect_matchings(indices: Tuple[int, ...]) -> Iterator[List[MatrixEntry]]:
    if not indices:
        yield []
        return
    first, rest = indices[0], indices[1:]
    for position, partner in enumerate(rest):
        remaining = rest[:position] + rest[position + 1:]
        for matching in _perfect_matchings(remaining):
            yield [(first, partner)] + matching


def _hafnian_of_indices(matrix: List[List[float]], indices: Tuple[int, ...]) -> float:
    if not indices:
        return 1.0
    first, rest = indices[0], indices[1:]
    total = 0.0
    for position, partner in enumerate(rest):
        remaining = rest[:position] + rest[position + 1:]
        total += matrix[first][partner] * _hafnian_of_indices(matrix, remaining)
    return total
