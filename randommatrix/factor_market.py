"""Synthetic stock market with a known true correlation matrix: one market factor, equal sectors and noise."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

MIN_ASSETS = 10
MAX_ASSETS = 400
MAX_OBSERVATIONS = 4000
DEFAULT_SECTOR_COUNT = 10
MARKET_LOADING = 0.5
"""Correlation 0.25 between any two stocks (our choice of a plausible value, not fitted to data)."""
SECTOR_LOADING = 0.4
"""Adds 0.16, so stocks within a sector correlate at 0.41."""


class FactorMarketError(ValueError):
    """Raised when the requested market or history is outside the supported range."""


@dataclass(frozen=True)
class FactorMarket:
    """Unit-variance returns r_i = β·f + γ·g_sector(i) + √(1 − β² − γ²)·ε_i with independent standard normal
    factors, so the covariance and the correlation matrix coincide."""

    asset_count: int
    sector_count: int = DEFAULT_SECTOR_COUNT
    market_loading: float = MARKET_LOADING
    sector_loading: float = SECTOR_LOADING

    def __post_init__(self) -> None:
        if not MIN_ASSETS <= self.asset_count <= MAX_ASSETS:
            raise FactorMarketError(f"Počet akcií musí být {MIN_ASSETS}–{MAX_ASSETS}.")
        if not 1 <= self.sector_count <= self.asset_count:
            raise FactorMarketError("Počet sektorů musí být alespoň 1 a nejvýš počet akcií.")
        if self.market_loading ** 2 + self.sector_loading ** 2 >= 1:
            raise FactorMarketError("Faktory nesmí vysvětlit celý rozptyl, β² + γ² musí být menší než 1.")

    @property
    def idiosyncratic_variance(self) -> float:
        return 1 - self.market_loading ** 2 - self.sector_loading ** 2

    @property
    def sectors(self) -> np.ndarray:
        """Sector index of every stock; sectors differ in size by at most one stock."""
        return np.arange(self.asset_count) * self.sector_count // self.asset_count

    def true_correlation(self) -> np.ndarray:
        same_sector = self.sectors[:, None] == self.sectors[None, :]
        correlation = self.market_loading ** 2 + self.sector_loading ** 2 * same_sector
        np.fill_diagonal(correlation, 1.0)
        return correlation

    def simulate_returns(self, observation_count: int, rng: np.random.Generator) -> np.ndarray:
        """T × N matrix of returns, one row per day."""
        if not 2 <= observation_count <= MAX_OBSERVATIONS:
            raise FactorMarketError(f"Počet pozorování musí být 2–{MAX_OBSERVATIONS}.")
        market = rng.standard_normal((observation_count, 1))
        sector_factors = rng.standard_normal((observation_count, self.sector_count))
        noise = rng.standard_normal((observation_count, self.asset_count))
        return (
            self.market_loading * market
            + self.sector_loading * sector_factors[:, self.sectors]
            + np.sqrt(self.idiosyncratic_variance) * noise
        )
