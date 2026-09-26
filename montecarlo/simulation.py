from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np

from montecarlo.portfolio import Portfolio

MONTHS_PER_YEAR = 12
MAX_SIMULATION_COUNT = 10_000
MAX_YEARS = 40


class SimulationParametersError(ValueError):
    """Raised when simulation parameters are outside the supported range."""


@dataclass(frozen=True)
class SimulationParameters:
    initial_value: float
    monthly_contribution: float
    years: int
    simulation_count: int
    seed: Optional[int] = None

    def __post_init__(self) -> None:
        if self.initial_value < 0:
            raise SimulationParametersError("Počáteční investice nesmí být záporná.")
        if self.monthly_contribution < 0:
            raise SimulationParametersError("Měsíční vklad nesmí být záporný.")
        if self.initial_value == 0 and self.monthly_contribution == 0:
            raise SimulationParametersError("Zadej počáteční investici nebo měsíční vklad.")
        if not 1 <= self.years <= MAX_YEARS:
            raise SimulationParametersError(f"Horizont musí být 1–{MAX_YEARS} let.")
        if not 1 <= self.simulation_count <= MAX_SIMULATION_COUNT:
            raise SimulationParametersError(
                f"Počet simulací musí být 1–{MAX_SIMULATION_COUNT}."
            )

    @property
    def month_count(self) -> int:
        return self.years * MONTHS_PER_YEAR

    @property
    def total_contributed(self) -> float:
        return self.initial_value + self.monthly_contribution * self.month_count


@dataclass(frozen=True)
class SimulationResult:
    paths: np.ndarray
    """Portfolio value per simulation (rows) and month (columns, month 0 = start)."""
    total_contributed: float

    @property
    def final_values(self) -> np.ndarray:
        return self.paths[:, -1]


def simulate(portfolio: Portfolio, parameters: SimulationParameters) -> SimulationResult:
    """Simulate portfolio value paths with correlated geometric Brownian motion.

    The portfolio is rebalanced to its target weights every month and the monthly
    contribution is added at the end of each month.
    """
    rng = np.random.default_rng(parameters.seed)
    monthly_drift, monthly_covariance = _monthly_log_return_moments(portfolio)
    weights = portfolio.weights

    paths = np.empty((parameters.simulation_count, parameters.month_count + 1))
    paths[:, 0] = parameters.initial_value

    for month in range(1, parameters.month_count + 1):
        log_returns = rng.multivariate_normal(
            monthly_drift, monthly_covariance, size=parameters.simulation_count, method="eigh"
        )
        portfolio_returns = np.expm1(log_returns) @ weights
        paths[:, month] = paths[:, month - 1] * (1 + portfolio_returns) + parameters.monthly_contribution

    return SimulationResult(paths=paths, total_contributed=parameters.total_contributed)


def _monthly_log_return_moments(portfolio: Portfolio) -> tuple[np.ndarray, np.ndarray]:
    time_step = 1 / MONTHS_PER_YEAR
    annual_log_drift = np.log1p(portfolio.expected_returns) - 0.5 * portfolio.volatilities**2
    return annual_log_drift * time_step, portfolio.covariance() * time_step
