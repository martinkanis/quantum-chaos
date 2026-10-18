"""Minimum-variance portfolio and how much its risk is misjudged when built from an estimated matrix."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class RiskComparison:
    """Variances of the portfolio built from the estimate, all relative to the best attainable variance."""

    in_sample: float
    """What the estimate promises: wᵀEw."""
    out_of_sample: float
    """What the portfolio really delivers: wᵀCw with the true matrix C."""

    @property
    def underestimation(self) -> float:
        """How many times the real variance exceeds the promised one."""
        return self.out_of_sample / self.in_sample


def min_variance_weights(covariance: np.ndarray) -> np.ndarray:
    """w = C⁻¹1 / (1ᵀC⁻¹1): fully invested, short positions allowed."""
    unnormalised = np.linalg.solve(covariance, np.ones(len(covariance)))
    return unnormalised / unnormalised.sum()


def portfolio_variance(weights: np.ndarray, covariance: np.ndarray) -> float:
    return float(weights @ covariance @ weights)


def compare_risk(estimated: np.ndarray, true: np.ndarray) -> RiskComparison:
    optimal = portfolio_variance(min_variance_weights(true), true)
    weights = min_variance_weights(estimated)
    return RiskComparison(
        in_sample=portfolio_variance(weights, estimated) / optimal,
        out_of_sample=portfolio_variance(weights, true) / optimal,
    )


def predicted_in_sample(ratio: float) -> float:
    """Large-N limit of the promised variance for the raw sample matrix and IID returns: 1 − q.

    Bouchaud and Potters (arXiv:0910.1205, eq. 29) state it for a random return predictor; the tests show it holds
    for the minimum-variance portfolio of the factor market too."""
    return 1 - ratio


def predicted_out_of_sample(ratio: float) -> float:
    """Large-N limit of the realised variance for the raw sample matrix and IID returns: 1 / (1 − q)."""
    return 1 / (1 - ratio)
