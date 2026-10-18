"""GBS-I estimator of Andersen & Shan for μ = Σ_{|I|=2K} a_I·Haf(B_I)² and its classical alternatives.

The integral is μ = E[f(p, q)] with f(p, q) = Σ a_I·p^I·q^I and p, q independent N(0, B) (arXiv:2502.19336, §2.1).
Plain Monte Carlo averages f over Gaussian scenarios, GBS-I averages a_I·I!·t^(−2K)/d_t over photon patterns
sampled from the rescaled device tB (arXiv:2502.19362, §3.2), and the exact value follows from Gaussian moments.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import factorial, prod

import numpy as np

from gbs.gaussian_moments import moment_table, moment_table_size
from gbs.sampler import patterns_with_total

MAX_MODES = 5
MAX_DEGREE = 10
MAX_MOMENT_TABLE_SIZE = 3_000_000
"""Bound on (4K + 1)^N, the number of Gaussian moments needed for the Monte Carlo variance."""
SYMMETRY_TOLERANCE = 1e-10
BISECTION_STEPS = 200
SPECTRUM_MARGIN = 1e-12
MC_CHUNK_SIZE = 50_000
PAPER_EXAMPLE_MATRIX = np.array([[0.3421, 0.3364, 0.3244], [0.3364, 0.3392, 0.3225], [0.3244, 0.3225, 0.3520]])
"""Matrix B of Example 6.1 in arXiv:2502.19336 (eigenvalues ≈ 0.9999, 0.029 and 0.0042)."""


class HafSquaredProblemError(ValueError):
    """Raised when the problem is invalid or too large for the exact computation."""


@dataclass(frozen=True)
class HafSquaredProblem:
    covariance: np.ndarray
    degree: int
    """K: every pattern I has |I| = 2K photons."""
    coefficients: np.ndarray
    """a_I in the order of degree_patterns(mode_count, degree)."""

    def __post_init__(self) -> None:
        _validate_covariance(self.covariance)
        if not 1 <= self.degree <= MAX_DEGREE:
            raise HafSquaredProblemError(f"Stupeň K musí být mezi 1 a {MAX_DEGREE}.")
        if len(self.coefficients) != len(self.patterns):
            raise HafSquaredProblemError(
                f"Úloha potřebuje {len(self.patterns)} koeficientů a_I, zadáno je {len(self.coefficients)}."
            )
        if moment_table_size([4 * self.degree] * self.mode_count) > MAX_MOMENT_TABLE_SIZE:
            raise HafSquaredProblemError(
                "Úloha je na přesný výpočet rozptylu příliš velká – sniž K nebo počet módů."
            )

    @property
    def mode_count(self) -> int:
        return self.covariance.shape[0]

    @property
    def patterns(self) -> np.ndarray:
        return degree_patterns(self.mode_count, self.degree)


@dataclass(frozen=True)
class PhotonRescaling:
    """Device kernel tB with mean photon number 2K, the optimum of both GBS estimators (arXiv:2502.19362, Prop. 3.2)."""

    scale: float
    normalization: float
    """d_t = Π_n √(1 − t²λ_n²)."""


@dataclass(frozen=True)
class EstimatorComparison:
    exact_value: float
    mc_relative_variance: float
    """Variance of one Monte Carlo scenario divided by μ²."""
    gbs_i_relative_variance: float
    """Variance of one GBS-I shot divided by μ², with the factor t^(−2K) that follows from the estimator."""
    printed_gbs_i_relative_variance: float
    """The same with t^(−4K) as printed in Theorem 3.5 of arXiv:2502.19362 and used in the authors' code."""
    rescaling: PhotonRescaling
    pattern_count: int
    """Number of hafnians the exact evaluation needs."""
    useful_shot_fraction: float
    """Probability that a shot has exactly 2K photons; all other shots contribute zero."""


def degree_patterns(mode_count: int, degree: int) -> np.ndarray:
    return patterns_with_total(mode_count, 2 * degree)


def uniform_problem(covariance: np.ndarray, degree: int) -> HafSquaredProblem:
    """All a_I = 1: μ = Σ_{|I|=2K} Haf(B_I)²."""
    return HafSquaredProblem(covariance, degree, np.ones(len(degree_patterns(covariance.shape[0], degree))))


def rescale_to_degree(covariance: np.ndarray, degree: int) -> PhotonRescaling:
    """t with Σ t²λ²/(1 − t²λ²) = 2K, found by bisection on (0, 1/λ_max)."""
    eigenvalues = np.linalg.eigvalsh(covariance)
    low, high = 0.0, (1 - SPECTRUM_MARGIN) / eigenvalues.max()
    for _ in range(BISECTION_STEPS):
        scale = (low + high) / 2
        if _mean_photon_number(eigenvalues, scale) < 2 * degree:
            low = scale
        else:
            high = scale
    scale = (low + high) / 2
    return PhotonRescaling(scale=scale, normalization=float(np.prod(np.sqrt(1 - (scale * eigenvalues) ** 2))))


@dataclass(frozen=True)
class VarianceModel:
    """Hafnians of one matrix and degree; evaluating many coefficient vectors then costs only dot products."""

    degree: int
    patterns: np.ndarray
    hafnians: np.ndarray
    """Haf(B_I) for every pattern with 2K photons."""
    pair_hafnians: np.ndarray
    """Haf(B_{I+J}) for every pair of patterns."""
    rescaling: PhotonRescaling

    def compare(self, coefficients: np.ndarray) -> EstimatorComparison:
        exact_value = float(coefficients @ self.hafnians**2)
        mc_second_moment = float(coefficients @ self.pair_hafnians**2 @ coefficients)
        weighted_sum = float(np.sum(coefficients**2 * _pattern_factorials(self.patterns) * self.hafnians**2))
        gbs_second_moment = weighted_sum / self.rescaling.normalization
        derived_factor = self.rescaling.scale ** (-2 * self.degree)
        printed_factor = self.rescaling.scale ** (-4 * self.degree)
        return EstimatorComparison(
            exact_value=exact_value,
            mc_relative_variance=_relative_variance(mc_second_moment, exact_value),
            gbs_i_relative_variance=_relative_variance(derived_factor * gbs_second_moment, exact_value),
            printed_gbs_i_relative_variance=_relative_variance(printed_factor * gbs_second_moment, exact_value),
            rescaling=self.rescaling,
            pattern_count=len(self.patterns),
            useful_shot_fraction=float(self.pattern_probabilities().sum()),
        )

    def pattern_probabilities(self) -> np.ndarray:
        """P_tB(I) = d_t/I!·Haf((tB)_I)² = d_t/I!·t^(2K)·Haf(B_I)² for every pattern with 2K photons."""
        scale_factor = self.rescaling.scale ** (2 * self.degree)
        return self.rescaling.normalization * scale_factor * self.hafnians**2 / _pattern_factorials(self.patterns)

    def shot_values(self, coefficients: np.ndarray) -> np.ndarray:
        """Value a_I·I!·t^(−2K)/d_t that one shot with pattern I contributes to the GBS-I average."""
        scale_factor = self.rescaling.scale ** (-2 * self.degree)
        return coefficients * _pattern_factorials(self.patterns) * scale_factor / self.rescaling.normalization


def variance_model(covariance: np.ndarray, degree: int) -> VarianceModel:
    patterns = degree_patterns(covariance.shape[0], degree)
    table = moment_table(covariance, [4 * degree] * covariance.shape[0])
    return VarianceModel(
        degree=degree,
        patterns=patterns,
        hafnians=np.array([table[tuple(pattern)] for pattern in patterns]),
        pair_hafnians=np.array([[table[tuple(first + second)] for second in patterns] for first in patterns]),
        rescaling=rescale_to_degree(covariance, degree),
    )


def compare_estimators(problem: HafSquaredProblem) -> EstimatorComparison:
    return variance_model(problem.covariance, problem.degree).compare(problem.coefficients)


def simulate_gbs_i(problem: HafSquaredProblem, shot_count: int, rng: np.random.Generator) -> float:
    """GBS-I with an emulated ideal device: patterns are drawn from the exact distribution."""
    model = variance_model(problem.covariance, problem.degree)
    probabilities = model.pattern_probabilities()
    outcome_probabilities = np.append(probabilities, max(0.0, 1.0 - probabilities.sum()))
    counts = rng.multinomial(shot_count, outcome_probabilities / outcome_probabilities.sum())
    return float(counts[:-1] @ model.shot_values(problem.coefficients)) / shot_count


def simulate_mc(problem: HafSquaredProblem, scenario_count: int, rng: np.random.Generator) -> float:
    """Plain Monte Carlo: average of f(p, q) = Σ a_I·(p·q)^I over independent Gaussian scenarios."""
    total = 0.0
    remaining = scenario_count
    mean = np.zeros(problem.mode_count)
    while remaining > 0:
        chunk = min(remaining, MC_CHUNK_SIZE)
        p = rng.multivariate_normal(mean, problem.covariance, size=chunk, method="eigh")
        q = rng.multivariate_normal(mean, problem.covariance, size=chunk, method="eigh")
        monomials = np.prod((p * q)[:, None, :] ** problem.patterns[None, :, :], axis=2)
        total += float(np.sum(monomials @ problem.coefficients))
        remaining -= chunk
    return total / scenario_count


def _pattern_factorials(patterns: np.ndarray) -> np.ndarray:
    return np.array([prod(factorial(int(photons)) for photons in pattern) for pattern in patterns], dtype=float)


def _mean_photon_number(eigenvalues: np.ndarray, scale: float) -> float:
    squared = (scale * eigenvalues) ** 2
    return float(np.sum(squared / (1 - squared)))


def _relative_variance(second_moment: float, exact_value: float) -> float:
    return (second_moment - exact_value**2) / exact_value**2


def _validate_covariance(covariance: np.ndarray) -> None:
    if covariance.ndim != 2 or covariance.shape[0] != covariance.shape[1]:
        raise HafSquaredProblemError("Matice B musí být čtvercová.")
    if not 1 <= covariance.shape[0] <= MAX_MODES:
        raise HafSquaredProblemError(f"Počet módů musí být mezi 1 a {MAX_MODES}.")
    if not np.allclose(covariance, covariance.T, atol=SYMMETRY_TOLERANCE):
        raise HafSquaredProblemError("Matice B musí být symetrická.")
    if np.linalg.eigvalsh(covariance).min() <= 0:
        raise HafSquaredProblemError("Matice B musí být pozitivně definitní (kovarianční matice).")
