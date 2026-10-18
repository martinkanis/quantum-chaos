"""Estimators of the correlation matrix from a short history: the raw sample one and two cleaned ones."""

from __future__ import annotations

from enum import Enum

import numpy as np

from randommatrix.marchenko_pastur import NoiseBand, market_mode_noise_variance


class Estimator(Enum):
    SAMPLE = "sample"
    CLIPPED = "clipped"
    LINEAR_SHRINKAGE = "linear-shrinkage"


def sample_covariance(returns: np.ndarray) -> np.ndarray:
    """E = XᵀX / T; the simulated returns have zero mean, so no mean is subtracted (it would cost a degree of
    freedom and shift the noise band)."""
    return returns.T @ returns / len(returns)


def clipped_covariance(sample: np.ndarray, observation_count: int) -> np.ndarray:
    """Eigenvalue clipping: eigenvalues inside the noise band are replaced by their average, which keeps the trace;
    eigenvalues above the band and all eigenvectors stay."""
    eigenvalues, eigenvectors = np.linalg.eigh(sample)
    band = NoiseBand(len(sample) / observation_count, market_mode_noise_variance(eigenvalues))
    is_noise = eigenvalues <= band.upper
    cleaned = eigenvalues.copy()
    cleaned[is_noise] = eigenvalues[is_noise].mean()
    return (eigenvectors * cleaned) @ eigenvectors.T


def shrinkage_intensity(returns: np.ndarray) -> float:
    """Ledoit–Wolf (2004) estimate of the optimal weight of the target m·I, between 0 and 1."""
    observation_count, asset_count = returns.shape
    sample = sample_covariance(returns)
    scale = np.trace(sample) / asset_count
    distance = _squared_norm(sample - scale * np.eye(asset_count))
    squared_lengths = np.sum(returns ** 2, axis=1)
    # Σ_t ‖x_t x_tᵀ − E‖² expanded, so the T outer products never have to be built.
    spread = (np.sum(squared_lengths ** 2) / asset_count - observation_count * _squared_norm(sample))
    sampling_error = min(spread / observation_count ** 2, distance)
    return sampling_error / distance


def linear_shrinkage_covariance(returns: np.ndarray) -> np.ndarray:
    """(1 − δ)·E + δ·m·I with m the average variance and δ the Ledoit–Wolf intensity."""
    sample = sample_covariance(returns)
    intensity = shrinkage_intensity(returns)
    scale = np.trace(sample) / len(sample)
    return (1 - intensity) * sample + intensity * scale * np.eye(len(sample))


def estimate(estimator: Estimator, returns: np.ndarray) -> np.ndarray:
    if estimator is Estimator.SAMPLE:
        return sample_covariance(returns)
    if estimator is Estimator.CLIPPED:
        return clipped_covariance(sample_covariance(returns), len(returns))
    return linear_shrinkage_covariance(returns)


def _squared_norm(matrix: np.ndarray) -> float:
    """Frobenius norm normalised by the dimension, ‖A‖² = tr(AAᵀ) / N, as in Ledoit and Wolf."""
    return float(np.sum(matrix ** 2) / len(matrix))
