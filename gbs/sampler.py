"""Classical simulation of an ideal (lossless, photon-number-resolving) Gaussian boson sampler."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations_with_replacement
from math import factorial
from typing import List, Optional, Tuple

import numpy as np

from gbs.hafnian import hafnian, repeated_submatrix

MAX_MODES = 6
SYMMETRY_TOLERANCE = 1e-10


class GbsProgramError(ValueError):
    """Raised when a covariance matrix cannot be encoded into the simulated sampler."""


@dataclass(frozen=True)
class GbsProgram:
    """Device settings encoding the kernel B = scale · Σ = U · diag(tanh r) · Uᵀ."""

    covariance: np.ndarray
    scale: float
    squeezing: np.ndarray
    interferometer: np.ndarray

    @property
    def mode_count(self) -> int:
        return len(self.squeezing)

    @property
    def kernel(self) -> np.ndarray:
        return self.interferometer @ np.diag(np.tanh(self.squeezing)) @ self.interferometer.T

    @property
    def mean_photon_number(self) -> float:
        return float(np.sum(np.sinh(self.squeezing) ** 2))

    @property
    def normalization(self) -> float:
        return float(np.prod(np.cosh(self.squeezing)))


def program_from_covariance(covariance: np.ndarray, squeezing_strength: float) -> GbsProgram:
    """Encodes Σ into squeezers and an interferometer via its eigen (Takagi) decomposition.

    squeezing_strength ∈ (0, 1) sets tanh of the largest squeezing parameter.
    """
    _validate_covariance(covariance)
    if not 0 < squeezing_strength < 1:
        raise GbsProgramError("Síla stlačení musí ležet v intervalu (0, 1).")

    eigenvalues, eigenvectors = np.linalg.eigh(covariance)
    eigenvalues = np.clip(eigenvalues, 0.0, None)
    scale = squeezing_strength / eigenvalues.max()
    return GbsProgram(
        covariance=covariance,
        scale=float(scale),
        squeezing=np.arctanh(scale * eigenvalues),
        interferometer=eigenvectors,
    )


def pattern_probability(program: GbsProgram, pattern: np.ndarray) -> float:
    """p(n) = Haf(B_n)² / (n! · Π cosh r_j) for a pure Gaussian state."""
    pattern_hafnian = hafnian(repeated_submatrix(program.kernel, pattern))
    return pattern_hafnian**2 / (_pattern_factorial(pattern) * program.normalization)


def patterns_with_total(mode_count: int, total: int) -> np.ndarray:
    return np.array(
        [
            np.bincount(modes, minlength=mode_count)
            for modes in combinations_with_replacement(range(mode_count), total)
        ],
        dtype=int,
    ).reshape(-1, mode_count)


def pattern_distribution(program: GbsProgram, total: int) -> Tuple[np.ndarray, np.ndarray]:
    patterns = patterns_with_total(program.mode_count, total)
    probabilities = np.array([pattern_probability(program, pattern) for pattern in patterns])
    return patterns, probabilities


def total_photon_distribution(program: GbsProgram, max_total: int) -> np.ndarray:
    """P(total = t) for t = 0..max_total.

    The interferometer conserves photon number, so the total is a sum of independent
    single-mode squeezed-vacuum counts and needs no hafnians.
    """
    distribution = np.zeros(max_total + 1)
    distribution[0] = 1.0
    for squeezing in program.squeezing:
        distribution = np.convolve(distribution, squeezed_vacuum_distribution(squeezing, max_total))[: max_total + 1]
    return distribution


def sample_shots(
    program: GbsProgram, shot_count: int, rng: np.random.Generator, max_listed_total: int
) -> List[Optional[np.ndarray]]:
    """Draws individual detector readouts; shots with more than max_listed_total photons are None."""
    total_probabilities = total_photon_distribution(program, max_listed_total)
    outcome_probabilities = np.append(total_probabilities, max(0.0, 1.0 - total_probabilities.sum()))
    totals = rng.choice(len(outcome_probabilities), size=shot_count, p=outcome_probabilities / outcome_probabilities.sum())

    distributions = {}
    shots: List[Optional[np.ndarray]] = []
    for total in totals:
        if total > max_listed_total:
            shots.append(None)
            continue
        if total not in distributions:
            distributions[total] = pattern_distribution(program, int(total))
        patterns, probabilities = distributions[total]
        shots.append(patterns[rng.choice(len(patterns), p=probabilities / probabilities.sum())])
    return shots


def squeezed_vacuum_distribution(squeezing: float, max_total: int) -> np.ndarray:
    distribution = np.zeros(max_total + 1)
    tanh_squared = np.tanh(squeezing) ** 2
    for pairs in range(max_total // 2 + 1):
        photons = 2 * pairs
        pair_weight = factorial(photons) / (2**pairs * factorial(pairs)) ** 2
        distribution[photons] = pair_weight * tanh_squared**pairs / np.cosh(squeezing)
    return distribution


def _pattern_factorial(pattern: np.ndarray) -> int:
    result = 1
    for photons in pattern:
        result *= factorial(int(photons))
    return result


def _validate_covariance(covariance: np.ndarray) -> None:
    rows, columns = covariance.shape
    if rows != columns:
        raise GbsProgramError("Kovarianční matice musí být čtvercová.")
    if rows > MAX_MODES:
        raise GbsProgramError(
            f"Simulace GBS zvládne nejvýše {MAX_MODES} aktiv (módů), portfolio jich má {rows}."
        )
    if not np.allclose(covariance, covariance.T, atol=SYMMETRY_TOLERANCE):
        raise GbsProgramError("Kovarianční matice musí být symetrická.")
    if np.any(covariance < 0):
        raise GbsProgramError(
            "GBS odhad z četností vyžaduje nezáporné korelace: měření dává |Haf|², "
            "takže znaménko hafniánu nelze zjistit (tzv. znaménkový problém)."
        )
    if np.linalg.eigvalsh(covariance).max() <= 0:
        raise GbsProgramError("Kovarianční matice musí mít alespoň jednu kladnou varianci.")
