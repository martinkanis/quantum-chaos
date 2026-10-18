"""How the GBS advantage for a portfolio moment depends on the spectrum of the correlation matrix."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence, Tuple

import numpy as np

from gbs.demo import gbs_error_constants
from gbs.expectation import mc_relative_error_constant


@dataclass(frozen=True)
class SpectrumSaving:
    correlation: float
    """Pairwise correlation ρ of the equicorrelated assets."""
    degree: int
    market_mode_share: float
    """Share of the total variance in the largest eigenvalue, (1 + (N − 1)ρ) / N."""
    best_strength: float
    """Squeezing strength from the grid with the smallest GBS error."""
    sample_saving: float
    """(c_MC / c_GBS)²: how many times fewer samples GBS needs for the same relative error."""


def equicorrelated(asset_count: int, correlation: float) -> np.ndarray:
    """Unit variances and one common pairwise correlation: a market mode and N − 1 equal noise eigenvalues."""
    return (1 - correlation) * np.eye(asset_count) + correlation * np.ones((asset_count, asset_count))


def spectrum_savings(
    asset_count: int, correlations: Sequence[float], degrees: Sequence[int], strengths: Sequence[float]
) -> Tuple[SpectrumSaving, ...]:
    """Equally weighted portfolio; for every correlation and degree the best squeezing strength on the grid."""
    weights = np.full(asset_count, 1 / asset_count)
    savings = []
    for correlation in correlations:
        covariance = equicorrelated(asset_count, correlation)
        constants = gbs_error_constants(covariance, weights, strengths, degrees)
        for degree in degrees:
            best = int(np.argmin(constants[degree]))
            savings.append(SpectrumSaving(
                correlation=correlation,
                degree=degree,
                market_mode_share=(1 + (asset_count - 1) * correlation) / asset_count,
                best_strength=float(strengths[best]),
                sample_saving=(mc_relative_error_constant(degree) / constants[degree][best]) ** 2,
            ))
    return tuple(savings)
