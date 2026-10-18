"""Marchenko–Pastur law: the eigenvalue spectrum of a correlation matrix estimated from pure noise."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class NoiseBand:
    """Interval that holds the eigenvalues of an N×N sample correlation matrix of T independent noise series."""

    ratio: float
    """q = N / T, assets per observation; the law needs q < 1."""
    variance: float = 1.0
    """σ² of the noise; below 1 when part of the variance is explained by real factors."""

    @property
    def lower(self) -> float:
        return self.variance * (1 - np.sqrt(self.ratio)) ** 2

    @property
    def upper(self) -> float:
        return self.variance * (1 + np.sqrt(self.ratio)) ** 2

    def density(self, eigenvalues: np.ndarray) -> np.ndarray:
        """Probability density of an eigenvalue; zero outside the band."""
        inside = np.clip((self.upper - eigenvalues) * (eigenvalues - self.lower), 0, None)
        return np.sqrt(inside) / (2 * np.pi * self.ratio * self.variance * eigenvalues)


def market_mode_noise_variance(eigenvalues: np.ndarray) -> float:
    """σ² left for noise once the largest eigenvalue (the market mode) is taken out: 1 − λ_max / N.

    Laloux et al. (1999) fit σ² to the bulk; this recipe uses the data only and needs no knowledge of the
    true factors."""
    return 1 - float(np.max(eigenvalues)) / len(eigenvalues)
