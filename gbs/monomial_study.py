"""Repeated simulation of plain Monte Carlo and of the GBS-P estimator for a monomial expectation E[x^n]."""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Sequence

import numpy as np

from gbs.expectation import relative_rmse
from gbs.monomial_problem import MonomialProblem, VarianceComparison, gbs_p_estimate

MC_CHUNK_SIZE = 100_000


@dataclass(frozen=True)
class MonomialStudy:
    sample_sizes: np.ndarray
    exact: float
    gbs_relative_rmse: np.ndarray
    mc_relative_rmse: np.ndarray
    gbs_final_estimates: np.ndarray
    """Estimate of every repetition after the largest sample size."""
    mc_final_estimates: np.ndarray
    gbs_error_constant: float
    """√N × relative RMSE of GBS-P predicted for large N."""
    mc_error_constant: float
    """√N × relative RMSE of plain Monte Carlo."""


def run_monomial_study(
    problem: MonomialProblem,
    comparison: VarianceComparison,
    sample_sizes: Sequence[int],
    repetitions: int,
    rng: np.random.Generator,
) -> MonomialStudy:
    used = problem.used_variables()
    exponents = np.array(used.exponents)
    sizes = np.asarray(sample_sizes, dtype=int)
    gbs_estimates = np.array([_gbs_estimates_along(comparison, exponents, sizes, rng) for _ in range(repetitions)])
    mc_estimates = np.array([_mc_estimates_along(used.covariance, exponents, sizes, rng) for _ in range(repetitions)])
    return MonomialStudy(
        sample_sizes=sizes,
        exact=comparison.exact,
        gbs_relative_rmse=relative_rmse(gbs_estimates, comparison.exact),
        mc_relative_rmse=relative_rmse(mc_estimates, comparison.exact),
        gbs_final_estimates=gbs_estimates[:, -1],
        mc_final_estimates=mc_estimates[:, -1],
        gbs_error_constant=sqrt(comparison.gbs_relative_variance),
        mc_error_constant=sqrt(comparison.mc_relative_variance),
    )


def _gbs_estimates_along(
    comparison: VarianceComparison, exponents: np.ndarray, sizes: np.ndarray, rng: np.random.Generator
) -> np.ndarray:
    """Only the number of shots showing exactly the pattern n matters, so it is drawn from the binomial distribution.

    Shots are drawn incrementally, so every sample size reuses the previous shots.
    """
    pattern_count = 0
    previous_size = 0
    estimates = []
    for size in sizes:
        pattern_count += rng.binomial(size - previous_size, comparison.pattern_probability)
        previous_size = size
        estimates.append(gbs_p_estimate(comparison.encoding, exponents, pattern_count / size))
    return np.array(estimates)


def _mc_estimates_along(
    covariance: np.ndarray, exponents: np.ndarray, sizes: np.ndarray, rng: np.random.Generator
) -> np.ndarray:
    running_sum = 0.0
    previous_size = 0
    estimates = []
    for size in sizes:
        running_sum += _sum_of_monomials(covariance, exponents, size - previous_size, rng)
        previous_size = size
        estimates.append(running_sum / size)
    return np.array(estimates)


def _sum_of_monomials(
    covariance: np.ndarray, exponents: np.ndarray, sample_count: int, rng: np.random.Generator
) -> float:
    """Samples in chunks to keep memory bounded for millions of scenarios."""
    mean = np.zeros(len(exponents))
    total = 0.0
    remaining = sample_count
    while remaining > 0:
        chunk = min(remaining, MC_CHUNK_SIZE)
        samples = rng.multivariate_normal(mean, covariance, size=chunk, method="eigh")
        total += float(np.sum(np.prod(samples**exponents, axis=1)))
        remaining -= chunk
    return total
