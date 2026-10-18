"""How the GBS advantage for a portfolio moment depends on the spectrum of the correlation matrix."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence, Tuple

import numpy as np

from gbs.expectation import MomentProblem, gbs_error_breakdown, mc_relative_error_constant
from gbs.sampler import program_from_covariance


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
    """(c_MC / c_GBS)²: how many times fewer samples GBS needs for the same relative error; below 1 it needs more."""
    useful_shot_share: float
    """At the best strength: share of shots with exactly `degree` photons."""
    pattern_mismatch: float
    """At the best strength: Σ share² / p(n | total = degree), 1 for a perfect match."""
    cancellation: float
    """Σ |share|: how many times the terms of the moment's expansion outweigh their sum."""


def equicorrelated(asset_count: int, correlation: float) -> np.ndarray:
    """Unit variances and one common pairwise correlation: a market mode along (1, …, 1) and N − 1 equal noise
    eigenvalues."""
    return (1 - correlation) * np.eye(asset_count) + correlation * np.ones((asset_count, asset_count))


def equal_weights(asset_count: int) -> np.ndarray:
    """Equally weighted portfolio; for an equicorrelated matrix it lies exactly along the market mode."""
    return np.full(asset_count, 1 / asset_count)


def long_short_weights(asset_count: int) -> np.ndarray:
    """Alternating long and short positions; for an even number of assets orthogonal to the market mode."""
    return np.array([(-1) ** index for index in range(asset_count)]) / asset_count


def spectrum_savings(
    weights: np.ndarray, correlations: Sequence[float], degrees: Sequence[int], strengths: Sequence[float]
) -> Tuple[SpectrumSaving, ...]:
    """For every correlation and degree the best squeezing strength on the grid; the device is programmed with
    the covariance matrix of the assets, as on page 2."""
    asset_count = len(weights)
    savings = []
    for correlation in correlations:
        covariance = equicorrelated(asset_count, correlation)
        for degree in degrees:
            problem = MomentProblem(covariance=covariance, weights=weights, degree=degree)
            breakdowns = [gbs_error_breakdown(problem, program_from_covariance(covariance, s)) for s in strengths]
            best = int(np.argmin([breakdown.relative_error_constant for breakdown in breakdowns]))
            breakdown = breakdowns[best]
            savings.append(SpectrumSaving(
                correlation=correlation,
                degree=degree,
                market_mode_share=(1 + (asset_count - 1) * correlation) / asset_count,
                best_strength=float(strengths[best]),
                sample_saving=(mc_relative_error_constant(degree) / breakdown.relative_error_constant) ** 2,
                useful_shot_share=breakdown.useful_shot_share,
                pattern_mismatch=breakdown.pattern_mismatch,
                cancellation=breakdown.cancellation,
            ))
    return tuple(savings)
