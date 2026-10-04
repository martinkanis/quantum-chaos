"""Loading a covariance matrix into a Gaussian boson sampler as B = D·Σ·D with squeezing tuned to a target pattern."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Sequence, Tuple

import numpy as np

BISECTION_STEPS = 200
NEWTON_MAX_STEPS = 60
PHOTON_TOLERANCE = 1e-6
"""Tuning stops once every mean photon number is this close to its target."""
ACCEPTABLE_PHOTON_ERROR = 1e-4
"""Rounding can stall the line search near the optimum; a residual this small is still a converged tuning."""
HESSIAN_STEP = 1e-6
ARMIJO_FRACTION = 1e-4
MIN_LINE_SEARCH_STEP = 1e-12


class TuningError(ValueError):
    """Raised when the squeezing cannot be tuned for the given matrix."""


class TuningMode(str, Enum):
    TOTAL = "celkem"
    """Andersen & Shan: one common scale, mean total photon number equal to the degree."""
    PER_MODE = "po-modech"
    """Our extension: mean photon number in every output mode equal to its exponent."""


@dataclass(frozen=True)
class DeviceEncoding:
    """Kernel B = D·Σ·D = O·diag(tanh r)·Oᵀ loaded into the squeezers (r) and the interferometer (O)."""

    mode_scales: np.ndarray
    """Diagonal of D."""
    tanh_squeezing: np.ndarray
    interferometer: np.ndarray

    @property
    def squeezing(self) -> np.ndarray:
        return np.arctanh(self.tanh_squeezing)

    @property
    def log_normalization(self) -> float:
        """log Π cosh r_j, the normalisation of the GBS distribution."""
        return float(-0.5 * np.sum(np.log1p(-self.tanh_squeezing**2)))

    @property
    def mean_photons_per_output_mode(self) -> np.ndarray:
        return _mean_photons_per_output_mode(self.tanh_squeezing, self.interferometer)

    @property
    def mean_photons_per_squeezer(self) -> np.ndarray:
        return np.sinh(self.squeezing) ** 2


def tune_encoding(covariance: np.ndarray, exponents: Sequence[int], mode: TuningMode) -> DeviceEncoding:
    if mode is TuningMode.TOTAL:
        return tune_total_photons(covariance, int(np.sum(exponents)))
    return tune_photons_per_mode(covariance, exponents)


def encode(covariance: np.ndarray, mode_scales: np.ndarray) -> DeviceEncoding:
    tanh_squeezing, interferometer = _kernel_spectrum(covariance, mode_scales)
    if tanh_squeezing.max() >= 1:
        raise TuningError("Zmenšená matice B musí mít vlastní čísla menší než 1, jinak ji nejde nahrát do zařízení.")
    return DeviceEncoding(mode_scales=mode_scales, tanh_squeezing=tanh_squeezing, interferometer=interferometer)


def tune_total_photons(covariance: np.ndarray, degree: int) -> DeviceEncoding:
    """B = γ·Σ with γ chosen so that the mean total photon number equals the degree (Andersen & Shan).

    The mean photon number Σ_j (γλ_j)² / (1 − (γλ_j)²) grows monotonically in γ ∈ (0, 1/λ_max).
    """
    eigenvalues = np.clip(np.linalg.eigvalsh(covariance), 0.0, None)
    lower, upper = 0.0, 1.0 / eigenvalues.max()
    for _ in range(BISECTION_STEPS):
        middle = (lower + upper) / 2
        tanh_squared = (middle * eigenvalues) ** 2
        if np.sum(tanh_squared / (1 - tanh_squared)) < degree:
            lower = middle
        else:
            upper = middle
    return encode(covariance, np.full(len(covariance), np.sqrt(lower)))


def tune_photons_per_mode(covariance: np.ndarray, exponents: Sequence[int]) -> DeviceEncoding:
    """D maximising p(n); at the optimum the mean photon number of every output mode equals its exponent.

    log p(n) = 2·Σ n_i·log d_i + ½·Σ_j log(1 − tanh² r_j) + const, and its gradient in log d_i is
    2·(n_i − ⟨n_i⟩). Newton's method with a backtracking line search starts from the standardised matrix
    tuned like Andersen & Shan, so it never ends worse than that tuning.
    """
    objective = _TuningObjective(covariance, np.asarray(exponents, dtype=float))
    point = objective.evaluate(_standardised_start(covariance, int(np.sum(exponents))))
    for _ in range(NEWTON_MAX_STEPS):
        if point.photon_error < PHOTON_TOLERANCE:
            break
        improved = objective.line_search(point, objective.ascent_direction(point))
        if improved is None:
            break
        point = improved
    if point.photon_error >= ACCEPTABLE_PHOTON_ERROR:
        raise TuningError("Stlačení se pro tuto matici nepodařilo naladit; zkus jiné exponenty nebo matici.")
    return encode(covariance, np.exp(point.log_scales))


@dataclass(frozen=True)
class _TuningPoint:
    log_scales: np.ndarray
    value: float
    """log p(n) up to a constant; −∞ outside the loadable region."""
    gradient: np.ndarray
    """Half of the gradient of value: n_i − ⟨n_i⟩."""

    @property
    def photon_error(self) -> float:
        return float(np.abs(self.gradient).max())


@dataclass(frozen=True)
class _TuningObjective:
    covariance: np.ndarray
    targets: np.ndarray

    def evaluate(self, log_scales: np.ndarray) -> _TuningPoint:
        tanh_squeezing, interferometer = _kernel_spectrum(self.covariance, np.exp(log_scales))
        if tanh_squeezing.max() >= 1:
            return _TuningPoint(log_scales, -np.inf, np.zeros_like(self.targets))
        value = 2 * float(self.targets @ log_scales) + 0.5 * float(np.sum(np.log1p(-tanh_squeezing**2)))
        gradient = self.targets - _mean_photons_per_output_mode(tanh_squeezing, interferometer)
        return _TuningPoint(log_scales, value, gradient)

    def ascent_direction(self, point: _TuningPoint) -> np.ndarray:
        """Newton direction from a finite-difference Hessian, or the gradient where Newton would not ascend."""
        size = len(point.log_scales)
        hessian = np.empty((size, size))
        for index in range(size):
            step = np.zeros(size)
            step[index] = HESSIAN_STEP
            forward = self.evaluate(point.log_scales + step).gradient
            backward = self.evaluate(point.log_scales - step).gradient
            hessian[:, index] = (forward - backward) / (2 * HESSIAN_STEP)
        try:
            direction = -np.linalg.solve((hessian + hessian.T) / 2, point.gradient)
        except np.linalg.LinAlgError:
            return point.gradient
        return direction if direction @ point.gradient > 0 else point.gradient

    def line_search(self, point: _TuningPoint, direction: np.ndarray) -> Optional[_TuningPoint]:
        """Backtracking until the Armijo condition holds; None when even tiny steps do not improve."""
        slope = float(point.gradient @ direction)
        step = 1.0
        while step >= MIN_LINE_SEARCH_STEP:
            candidate = self.evaluate(point.log_scales + step * direction)
            if candidate.value >= point.value + ARMIJO_FRACTION * step * slope:
                return candidate
            step /= 2
        return None


def _standardised_start(covariance: np.ndarray, degree: int) -> np.ndarray:
    deviations = np.sqrt(np.diag(covariance))
    correlation = covariance / np.outer(deviations, deviations)
    common_scale = tune_total_photons(correlation, degree).mode_scales
    return np.log(common_scale) - np.log(deviations)


def _kernel_spectrum(covariance: np.ndarray, mode_scales: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    kernel = mode_scales[:, None] * covariance * mode_scales[None, :]
    eigenvalues, eigenvectors = np.linalg.eigh(kernel)
    return np.clip(eigenvalues, 0.0, None), eigenvectors


def _mean_photons_per_output_mode(tanh_squeezing: np.ndarray, interferometer: np.ndarray) -> np.ndarray:
    """⟨n_i⟩ = [O·diag(sinh² r)·Oᵀ]_ii: squeezer j sends sinh² r_j photons, split by |O_ij|²."""
    tanh_squared = tanh_squeezing**2
    return (interferometer**2) @ (tanh_squared / (1 - tanh_squared))
