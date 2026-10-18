"""Share of random problems where GBS-I needs fewer samples than plain Monte Carlo (arXiv:2502.19362, §4, Fig. 2).

Matrices B = U·diag(λ)·Uᵀ with U uniformly random orthogonal and λ_i ~ U(0, 1) are weighted by the Vandermonde
determinant |Δ(λ)|; coefficient vectors are uniform on the unit sphere. The share is computed twice: with the
variance factor t^(−2K) that follows from the estimator and with t^(−4K) as printed in Theorem 3.5.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import prod
from typing import Tuple

import numpy as np

from gbs.hafnian_squared import variance_model

PERCENT = 100


@dataclass(frozen=True)
class AdvantageShare:
    mode_count: int
    degree: int
    derived_percent: float
    printed_percent: float
    median_scale: float
    """Median of the rescaling t; t^(−2K) and t^(−4K) differ only when t is far from 1."""
    median_variance_ratio: float
    """Median of V_MC / V_GBS-I with the derived factor."""


def advantage_share(
    mode_count: int, degree: int, matrix_count: int, coefficient_count: int, rng: np.random.Generator
) -> AdvantageShare:
    derived_wins = printed_wins = total_weight = 0.0
    scales, ratios = [], []
    for _ in range(matrix_count):
        covariance, weight = random_device_matrix(mode_count, rng)
        model = variance_model(covariance, degree)
        scales.append(model.rescaling.scale)
        for _ in range(coefficient_count):
            comparison = model.compare(_unit_vector(len(model.patterns), rng))
            derived_wins += weight * (comparison.mc_relative_variance > comparison.gbs_i_relative_variance)
            printed_wins += weight * (comparison.mc_relative_variance > comparison.printed_gbs_i_relative_variance)
            total_weight += weight
            ratios.append(comparison.mc_relative_variance / comparison.gbs_i_relative_variance)
    return AdvantageShare(
        mode_count=mode_count,
        degree=degree,
        derived_percent=float(PERCENT * derived_wins / total_weight),
        printed_percent=float(PERCENT * printed_wins / total_weight),
        median_scale=float(np.median(scales)),
        median_variance_ratio=float(np.median(ratios)),
    )


def random_device_matrix(mode_count: int, rng: np.random.Generator) -> Tuple[np.ndarray, float]:
    """B = U·diag(λ)·Uᵀ and its weight |Δ(λ)| in the measure of the paper."""
    orthogonal, triangular = np.linalg.qr(rng.normal(size=(mode_count, mode_count)))
    orthogonal = orthogonal * np.sign(np.diag(triangular))
    eigenvalues = rng.uniform(0, 1, mode_count)
    weight = abs(prod(
        eigenvalues[first] - eigenvalues[second]
        for first in range(mode_count) for second in range(first + 1, mode_count)
    ))
    return orthogonal @ np.diag(eigenvalues) @ orthogonal.T, float(weight)


def _unit_vector(size: int, rng: np.random.Generator) -> np.ndarray:
    vector = rng.normal(size=size)
    return vector / np.linalg.norm(vector)
