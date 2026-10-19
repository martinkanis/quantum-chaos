"""Single-photon (Fock-state) boson sampling as a 'modified Monte Carlo' – the permanent analogue of GBS-I.

Photonic machines built on single-photon sources (Quandela, ORCA, QuiX) cannot prepare squeezed light, so they
sample P(S) = |Perm(U_{S,T})|² / S! instead of hafnians (input T: one photon in each of the first n modes).
The importance estimator of Andersen & Shan (arXiv:2502.19336, Def. 3.3) works for any sampler with
P(S) = w_S·φ(S): here it estimates μ = Σ_S a_S·|Perm(U_{S,T})|² from shots with value Z(S) = a_S·S!.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import factorial, prod
from typing import Sequence

import numpy as np

from gbs.sampler import patterns_with_total

MAX_PHOTONS = 8
UNITARITY_TOLERANCE = 1e-9


class BosonSamplingError(ValueError):
    """Raised when the interferometer or the photon number is invalid."""


@dataclass(frozen=True)
class BosonSamplingProblem:
    unitary: np.ndarray
    """Interferometer U (modes × modes); photons enter the first `photons` modes."""
    photons: int
    coefficients: np.ndarray
    """a_S in the order of output_patterns(modes, photons)."""

    def __post_init__(self) -> None:
        modes = self.unitary.shape[0]
        if self.unitary.shape != (modes, modes):
            raise BosonSamplingError("Interferometr musí být čtvercová matice.")
        if not np.allclose(self.unitary.conj().T @ self.unitary, np.eye(modes), atol=UNITARITY_TOLERANCE):
            raise BosonSamplingError("Interferometr musí být unitární matice.")
        if not 1 <= self.photons <= min(modes, MAX_PHOTONS):
            raise BosonSamplingError(f"Počet fotonů musí být mezi 1 a {min(modes, MAX_PHOTONS)}.")
        if len(self.coefficients) != len(self.patterns):
            raise BosonSamplingError(
                f"Úloha potřebuje {len(self.patterns)} koeficientů a_S, zadáno je {len(self.coefficients)}."
            )

    @property
    def modes(self) -> int:
        return self.unitary.shape[0]

    @property
    def patterns(self) -> np.ndarray:
        return output_patterns(self.modes, self.photons)


@dataclass(frozen=True)
class BosonSamplingEstimate:
    exact_value: float
    """μ = Σ_S a_S·|Perm(U_{S,T})|²."""
    probabilities: np.ndarray
    """P(S) = |Perm(U_{S,T})|² / S! for every output pattern."""
    shot_values: np.ndarray
    """Z(S) = a_S·S!, what one shot with pattern S contributes."""

    @property
    def relative_variance(self) -> float:
        """Variance of one shot divided by μ²."""
        second_moment = float(self.probabilities @ self.shot_values**2)
        return second_moment / self.exact_value**2 - 1


def output_patterns(modes: int, photons: int) -> np.ndarray:
    return patterns_with_total(modes, photons)


def permanent(matrix: np.ndarray) -> complex:
    """Ryser's formula, O(2^n·n²); enough for the handful of photons of today's devices."""
    size = matrix.shape[0]
    if size == 0:
        return 1.0
    total = 0j
    for subset in range(1, 1 << size):
        columns = [column for column in range(size) if subset >> column & 1]
        total += (-1) ** len(columns) * np.prod(matrix[:, columns].sum(axis=1))
    return (-1) ** size * total


def transition_matrix(unitary: np.ndarray, pattern: Sequence[int], photons: int) -> np.ndarray:
    """U_{S,T}: row i of U repeated S_i times, columns of the input modes 0 … n−1."""
    rows = np.repeat(np.arange(len(pattern)), pattern)
    return unitary[np.ix_(rows, np.arange(photons))]


def estimate(problem: BosonSamplingProblem) -> BosonSamplingEstimate:
    patterns = problem.patterns
    permanent_squares = np.array([
        abs(permanent(transition_matrix(problem.unitary, pattern, problem.photons))) ** 2 for pattern in patterns
    ])
    factorials = np.array([prod(factorial(int(count)) for count in pattern) for pattern in patterns], dtype=float)
    return BosonSamplingEstimate(
        exact_value=float(problem.coefficients @ permanent_squares),
        probabilities=permanent_squares / factorials,
        shot_values=problem.coefficients * factorials,
    )


def random_unitary(modes: int, rng: np.random.Generator) -> np.ndarray:
    """Haar-random unitary: QR of a complex Gaussian matrix with the phases of R moved into Q."""
    gaussian = rng.normal(size=(modes, modes)) + 1j * rng.normal(size=(modes, modes))
    unitary, triangular = np.linalg.qr(gaussian)
    return unitary * (np.diag(triangular) / abs(np.diag(triangular)))


REFERENCE_MODES = 6
REFERENCE_PHOTONS = 3
REFERENCE_SEED = 7


def reference_problem() -> BosonSamplingProblem:
    """The instance of scripts/perceval_boson_sampling.py: Haar-random 6-mode interferometer, 3 photons, a_S ~ U(0.5, 1.5)."""
    rng = np.random.default_rng(REFERENCE_SEED)
    unitary = random_unitary(REFERENCE_MODES, rng)
    coefficients = rng.uniform(0.5, 1.5, len(output_patterns(REFERENCE_MODES, REFERENCE_PHOTONS)))
    return BosonSamplingProblem(unitary=unitary, photons=REFERENCE_PHOTONS, coefficients=coefficients)
