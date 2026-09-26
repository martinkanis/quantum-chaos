from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import numpy as np

WEIGHT_SUM_TOLERANCE = 1e-6
CORRELATION_TOLERANCE = 1e-8


class PortfolioValidationError(ValueError):
    """Raised when portfolio inputs violate a domain rule."""


@dataclass(frozen=True)
class Asset:
    """One portfolio position. Rates are annual and expressed as fractions (0.07 = 7 %)."""

    name: str
    weight: float
    expected_return: float
    volatility: float


@dataclass(frozen=True)
class Portfolio:
    assets: Tuple[Asset, ...]
    correlation: np.ndarray

    def __post_init__(self) -> None:
        _validate_assets(self.assets)
        _validate_correlation(self.correlation, asset_count=len(self.assets))

    @property
    def weights(self) -> np.ndarray:
        return np.array([asset.weight for asset in self.assets])

    @property
    def expected_returns(self) -> np.ndarray:
        return np.array([asset.expected_return for asset in self.assets])

    @property
    def volatilities(self) -> np.ndarray:
        return np.array([asset.volatility for asset in self.assets])

    def covariance(self) -> np.ndarray:
        return np.outer(self.volatilities, self.volatilities) * self.correlation


def uniform_correlation(asset_count: int, pairwise_correlation: float) -> np.ndarray:
    matrix = np.full((asset_count, asset_count), pairwise_correlation, dtype=float)
    np.fill_diagonal(matrix, 1.0)
    return matrix


def _validate_assets(assets: Tuple[Asset, ...]) -> None:
    if not assets:
        raise PortfolioValidationError("Portfolio musí obsahovat alespoň jedno aktivum.")

    names = [asset.name.strip() for asset in assets]
    if any(not name for name in names):
        raise PortfolioValidationError("Každé aktivum musí mít vyplněný název.")
    if len(set(names)) != len(names):
        raise PortfolioValidationError("Názvy aktiv musí být unikátní.")

    for asset in assets:
        if asset.weight < 0:
            raise PortfolioValidationError(f"Váha aktiva '{asset.name}' nesmí být záporná.")
        if asset.volatility < 0:
            raise PortfolioValidationError(f"Volatilita aktiva '{asset.name}' nesmí být záporná.")

    weight_sum = sum(asset.weight for asset in assets)
    if abs(weight_sum - 1.0) > WEIGHT_SUM_TOLERANCE:
        raise PortfolioValidationError(
            f"Součet vah musí být 100 %, aktuálně je {weight_sum * 100:.2f} %."
        )


def _validate_correlation(correlation: np.ndarray, asset_count: int) -> None:
    if correlation.shape != (asset_count, asset_count):
        raise PortfolioValidationError(
            f"Korelační matice musí mít rozměr {asset_count}×{asset_count}, "
            f"má {correlation.shape}."
        )
    if not np.allclose(correlation, correlation.T, atol=CORRELATION_TOLERANCE):
        raise PortfolioValidationError("Korelační matice musí být symetrická.")
    if not np.allclose(np.diag(correlation), 1.0, atol=CORRELATION_TOLERANCE):
        raise PortfolioValidationError("Diagonála korelační matice musí být 1.")
    if np.any(np.abs(correlation) > 1.0 + CORRELATION_TOLERANCE):
        raise PortfolioValidationError("Korelace musí ležet v intervalu [-1, 1].")

    smallest_eigenvalue = np.linalg.eigvalsh(correlation).min()
    if smallest_eigenvalue < -CORRELATION_TOLERANCE:
        raise PortfolioValidationError(
            "Korelační matice není pozitivně semidefinitní — zadané korelace si odporují."
        )
