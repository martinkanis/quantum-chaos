"""Gaussian expectation E[(w·X)^d], X ~ N(0, Σ): exact, GBS-based and classical Monte Carlo estimates."""

from __future__ import annotations

from dataclasses import dataclass
from math import factorial, prod
from typing import List, Sequence, Tuple

import numpy as np

from gbs.hafnian import hafnian, repeated_submatrix
from gbs.sampler import GbsProgram, pattern_distribution, patterns_with_total

ALLOWED_DEGREES = (2, 4, 6)
MC_CHUNK_SIZE = 100_000


class MomentProblemError(ValueError):
    """Raised when the moment problem is not supported."""


@dataclass(frozen=True)
class MomentProblem:
    covariance: np.ndarray
    weights: np.ndarray
    degree: int

    def __post_init__(self) -> None:
        if self.degree not in ALLOWED_DEGREES:
            raise MomentProblemError(f"Stupeň momentu musí být jeden z {ALLOWED_DEGREES}.")
        if self.covariance.shape != (len(self.weights), len(self.weights)):
            raise MomentProblemError("Rozměr kovarianční matice neodpovídá počtu vah.")
        if self.portfolio_variance <= 0:
            raise MomentProblemError(
                "Portfolio má nulový rozptyl wᵀΣw, takže moment je nula a relativní chybu nejde spočítat. "
                "Dej váhu aspoň jednomu aktivu s nenulovou volatilitou."
            )

    @property
    def portfolio_variance(self) -> float:
        return float(self.weights @ self.covariance @ self.weights)

    def monomials(self) -> Tuple[np.ndarray, np.ndarray]:
        """Multinomial expansion (w·x)^d = Σ_n c_n x^n over patterns with |n| = d."""
        patterns = patterns_with_total(len(self.weights), self.degree)
        coefficients = np.array([_multinomial(pattern) * np.prod(self.weights**pattern) for pattern in patterns])
        return patterns, coefficients

    def closed_form(self) -> float:
        """(d−1)!! · (wᵀΣw)^(d/2), used to cross-check the hafnian route."""
        return _double_factorial(self.degree - 1) * self.portfolio_variance ** (self.degree / 2)


@dataclass(frozen=True)
class HafnianTerm:
    pattern: np.ndarray
    coefficient: float
    hafnian: float

    @property
    def contribution(self) -> float:
        return self.coefficient * self.hafnian


@dataclass(frozen=True)
class ConvergenceStudy:
    sample_sizes: np.ndarray
    exact: float
    gbs_relative_rmse: np.ndarray
    mc_relative_rmse: np.ndarray
    gbs_trajectory: np.ndarray
    """Estimates of the first repetition, one per sample size."""
    mc_trajectory: np.ndarray
    useful_shot_fraction: float
    """Share of GBS shots with exactly d photons — only those carry information."""
    patterns: np.ndarray
    pattern_probabilities: np.ndarray
    observed_pattern_counts: np.ndarray
    """Pattern counts of the first repetition after the largest sample size."""
    gbs_error_constant: float
    """√N × relative RMSE of the GBS estimator predicted for large N."""
    mc_error_constant: float
    """√N × relative RMSE of classical Monte Carlo predicted for large N."""


def hafnian_terms(problem: MomentProblem) -> List[HafnianTerm]:
    """Wick–Isserlis theorem: E[x^n] = Haf(Σ_n), so the moment is a weighted sum of hafnians."""
    patterns, coefficients = problem.monomials()
    return [
        HafnianTerm(
            pattern=pattern,
            coefficient=float(coefficient),
            hafnian=hafnian(repeated_submatrix(problem.covariance, pattern)),
        )
        for pattern, coefficient in zip(patterns, coefficients)
    ]


def exact_expectation_via_hafnians(problem: MomentProblem) -> float:
    return float(sum(term.contribution for term in hafnian_terms(problem)))


def gbs_estimate(
    problem: MomentProblem, program: GbsProgram, pattern_counts: np.ndarray, shot_count: int
) -> float:
    """Recovers Haf(Σ_n) = scale^(−d/2) · √(p(n) · n! · Π cosh r) from observed pattern frequencies."""
    patterns, coefficients = problem.monomials()
    frequencies = pattern_counts / shot_count
    pattern_factorials = np.array([prod(factorial(int(photons)) for photons in pattern) for pattern in patterns])
    hafnian_estimates = np.sqrt(frequencies * pattern_factorials * program.normalization)
    return float(coefficients @ hafnian_estimates) * program.scale ** (-problem.degree / 2)


def classical_mc_estimate(problem: MomentProblem, samples: np.ndarray) -> float:
    return float(np.mean((samples @ problem.weights) ** problem.degree))


def mc_relative_error_constant(degree: int) -> float:
    """√N × relative RMSE of classical Monte Carlo for E[L^d].

    L is Gaussian, so var(L^d) / E[L^d]² = (2d−1)!! / ((d−1)!!)² − 1 for every portfolio.
    """
    return float(np.sqrt(_double_factorial(2 * degree - 1) / _double_factorial(degree - 1) ** 2 - 1))


def gbs_relative_error_constant(problem: MomentProblem, program: GbsProgram) -> float:
    """√N × relative RMSE of gbs_estimate for large N (delta method).

    As in importance sampling, every pattern adds share² / p(n), where share is its part of the moment, so
    patterns carrying much of the moment but rarely observed dominate; the ½ comes from the square root.
    """
    _, probabilities = pattern_distribution(program, problem.degree)
    contributions = np.array([term.contribution for term in hafnian_terms(problem)])
    shares = contributions / contributions.sum()
    observable = probabilities > 0
    return 0.5 * float(np.sqrt(np.sum(shares[observable] ** 2 / probabilities[observable]) - 1))


def run_convergence_study(
    problem: MomentProblem,
    program: GbsProgram,
    sample_sizes: Sequence[int],
    repetitions: int,
    rng: np.random.Generator,
) -> ConvergenceStudy:
    sizes = np.asarray(sample_sizes, dtype=int)
    patterns, probabilities = pattern_distribution(program, problem.degree)
    useful_probability = float(probabilities.sum())
    exact = problem.closed_form()

    gbs_runs = [_gbs_estimates_along(problem, program, sizes, probabilities, rng) for _ in range(repetitions)]
    gbs_estimates = np.array([estimates for estimates, _ in gbs_runs])
    mc_estimates = np.array([_mc_estimates_along(problem, sizes, rng) for _ in range(repetitions)])

    return ConvergenceStudy(
        sample_sizes=sizes,
        exact=exact,
        gbs_relative_rmse=_relative_rmse(gbs_estimates, exact),
        mc_relative_rmse=_relative_rmse(mc_estimates, exact),
        gbs_trajectory=gbs_estimates[0],
        mc_trajectory=mc_estimates[0],
        useful_shot_fraction=useful_probability,
        patterns=patterns,
        pattern_probabilities=probabilities,
        observed_pattern_counts=gbs_runs[0][1],
        gbs_error_constant=gbs_relative_error_constant(problem, program),
        mc_error_constant=mc_relative_error_constant(problem.degree),
    )


def _gbs_estimates_along(
    problem: MomentProblem,
    program: GbsProgram,
    sizes: np.ndarray,
    probabilities: np.ndarray,
    rng: np.random.Generator,
) -> Tuple[np.ndarray, np.ndarray]:
    """Draws shots incrementally so that every sample size reuses the previous shots.

    Only the number of shots with exactly d photons matters, so it is drawn directly from
    the binomial distribution instead of simulating every discarded shot.
    """
    useful_probability = probabilities.sum()
    conditional_probabilities = probabilities / useful_probability
    pattern_counts = np.zeros(len(probabilities))
    previous_size = 0
    estimates = []
    for size in sizes:
        useful_shots = rng.binomial(size - previous_size, useful_probability)
        pattern_counts += rng.multinomial(useful_shots, conditional_probabilities)
        previous_size = size
        estimates.append(gbs_estimate(problem, program, pattern_counts, size))
    return np.array(estimates), pattern_counts


def _mc_estimates_along(problem: MomentProblem, sizes: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    running_sum = 0.0
    previous_size = 0
    estimates = []
    for size in sizes:
        running_sum += _sum_of_powers(problem, size - previous_size, rng)
        previous_size = size
        estimates.append(running_sum / size)
    return np.array(estimates)


def _sum_of_powers(problem: MomentProblem, sample_count: int, rng: np.random.Generator) -> float:
    """Samples in chunks to keep memory bounded for millions of samples."""
    mean = np.zeros(len(problem.weights))
    total = 0.0
    remaining = sample_count
    while remaining > 0:
        chunk = min(remaining, MC_CHUNK_SIZE)
        samples = rng.multivariate_normal(mean, problem.covariance, size=chunk, method="eigh")
        total += float(np.sum((samples @ problem.weights) ** problem.degree))
        remaining -= chunk
    return total


def _relative_rmse(estimates: np.ndarray, exact: float) -> np.ndarray:
    return np.sqrt(np.mean((estimates - exact) ** 2, axis=0)) / abs(exact)


def _multinomial(pattern: np.ndarray) -> int:
    result = factorial(int(pattern.sum()))
    for photons in pattern:
        result //= factorial(int(photons))
    return result


def _double_factorial(value: int) -> int:
    return prod(range(value, 0, -2)) if value > 0 else 1
